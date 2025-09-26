import io
import json
import logging
import time
import os
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from fdk import response
import anthropic

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueryRouterAgent:
    """AI-powered query router using Claude Sonnet for intelligent routing and response synthesis"""

    def __init__(self, config: Dict):
        self.config = config
        self.name = "query_router"

        # Initialize Claude client
        claude_api_key = config.get('claude_api_key') or os.environ.get('CLAUDE_API_KEY')
        if not claude_api_key:
            raise ValueError("Claude API key is required for AI-powered routing")

        self.claude_client = anthropic.Anthropic(api_key=claude_api_key)

        # Configuration
        self.model = config.get('claude_model', 'claude-3-5-sonnet-20241022')
        self.max_tokens = config.get('max_tokens', 2000)
        self.enable_conversation_history = config.get('enable_conversation_history', True)
        self.enable_parallel_routing = config.get('enable_parallel_routing', True)

        # Initialize agent registry
        self.agent_registry = self._initialize_agent_registry()

        # Conversation state (in production, this would be stored in a database)
        self.conversation_history = []
        self.dashboard_context = {}

    def execute(self, input_data: Dict) -> Dict:
        """Execute query routing and response synthesis"""
        start_time = time.time()

        try:
            logger.info(f"Starting {self.name} agent execution")

            # Extract question and context
            question = input_data.get('question', '')
            user_context = input_data.get('user_context', {})
            dashboard_state = input_data.get('dashboard_state', {})

            if not question:
                return self._create_error_response("No question provided", time.time() - start_time)

            # Update dashboard context
            self.dashboard_context.update(dashboard_state)

            # Process the question
            result = asyncio.run(self._process_question_async(question, user_context))

            execution_time = time.time() - start_time

            return {
                'agent_name': self.name,
                'status': 'success',
                'data': result,
                'execution_time': execution_time,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Query router agent failed: {str(e)}")
            return self._create_error_response(str(e), execution_time)

    async def _process_question_async(self, question: str, user_context: Dict = None) -> Dict:
        """Process user question and route to appropriate agents"""

        # Step 1: Analyze the question with Claude
        logger.info("Analyzing question with Claude Sonnet")
        analysis = await self._analyze_question_with_claude(question, user_context)

        # Step 2: Route to appropriate agents (simulated for now)
        logger.info("Routing to specialized agents")
        agent_responses = await self._route_to_agents(analysis)

        # Step 3: Synthesize final response
        logger.info("Synthesizing response with Claude")
        final_response = await self._synthesize_response(question, analysis, agent_responses)

        # Step 4: Update conversation history
        if self.enable_conversation_history:
            self._update_conversation_history(question, final_response)

        return final_response

    async def _analyze_question_with_claude(self, question: str, user_context: Dict) -> Dict:
        """Use Claude to deeply understand the question"""

        context_prompt = f"""
        You are an AI business intelligence router analyzing user questions to determine the best approach for answering them.

        Dashboard Context: {json.dumps(self.dashboard_context, indent=2)}
        Recent Conversation: {json.dumps(self.conversation_history[-3:] if self.conversation_history else [], indent=2)}
        User Context: {json.dumps(user_context or {}, indent=2)}

        User Question: "{question}"

        Analyze this question and provide a structured response with:

        1. INTENT_CLASSIFICATION:
           - Type: [analytical, operational, strategic, forecasting, explanatory, comparative, diagnostic]
           - Urgency: [low, medium, high, critical]
           - Complexity: [simple, moderate, complex, multi-faceted]
           - Time_Horizon: [current, historical, forecasting, real-time]
           - Business_Domain: [financial, operational, customer, strategic, market]

        2. DATA_REQUIREMENTS:
           - Primary_Entities: [projects, customers, financials, operations, market_data]
           - Metrics_Needed: [specific KPIs, calculations, aggregations required]
           - Time_Range: [specific dates, periods, or real-time data needed]
           - Granularity: [daily, weekly, monthly, quarterly, yearly]
           - Data_Sources: [which databases or systems need to be queried]

        3. AGENT_ROUTING:
           - Primary_Agent: [intelligence, discovery, strategy, forecasting, decision, visualization]
           - Supporting_Agents: [list of additional agents needed]
           - Coordination_Type: [sequential, parallel, hierarchical]
           - Estimated_Complexity: [1-10 scale]
           - Expected_Response_Time: [seconds estimate]

        4. RESPONSE_REQUIREMENTS:
           - Format: [narrative, tabular, visual, interactive, conversational]
           - Detail_Level: [executive_summary, detailed_analysis, comprehensive_report]
           - Visualization_Needs: [charts, graphs, dashboards, interactive_elements]
           - Follow_Up_Potential: [likely follow-up questions]

        5. BUSINESS_CONTEXT:
           - Strategic_Relevance: [how this relates to business strategy]
           - Decision_Impact: [what business decisions this might influence]
           - Stakeholder_Interest: [who would be interested in this answer]
           - Risk_Sensitivity: [how sensitive this topic is for the business]

        6. AI_REASONING_NEEDS:
           - Pattern_Recognition: [whether advanced pattern detection is needed]
           - Causal_Analysis: [if cause-and-effect relationships need identification]
           - Predictive_Elements: [forecasting or prediction requirements]
           - Anomaly_Detection: [if unusual patterns should be highlighted]

        Respond in valid JSON format only. Be precise and specific in your analysis.
        """

        try:
            response = await self.claude_client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{"role": "user", "content": context_prompt}]
            )

            # Parse Claude's response
            analysis_text = response.content[0].text
            analysis = json.loads(analysis_text)

            logger.info(f"Question analysis completed: {analysis.get('INTENT_CLASSIFICATION', {}).get('Type', 'unknown')}")
            return analysis

        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse Claude response as JSON: {e}")
            return self._fallback_question_analysis(question)
        except Exception as e:
            logger.error(f"Claude analysis failed: {e}")
            return self._fallback_question_analysis(question)

    async def _route_to_agents(self, analysis: Dict) -> Dict:
        """Route question to appropriate agents (simulated responses for now)"""

        routing = analysis.get('AGENT_ROUTING', {})
        primary_agent = routing.get('Primary_Agent', 'intelligence')
        supporting_agents = routing.get('Supporting_Agents', [])
        coordination_type = routing.get('Coordination_Type', 'sequential')

        logger.info(f"Routing to primary agent: {primary_agent}, supporting: {supporting_agents}")

        # For now, simulate agent responses based on the analysis
        # In production, these would be actual calls to specialized agent functions
        agent_responses = {}

        # Simulate primary agent response
        if primary_agent in self.agent_registry:
            agent_responses[primary_agent] = await self._simulate_agent_response(primary_agent, analysis)

        # Simulate supporting agent responses
        for agent_name in supporting_agents:
            if agent_name in self.agent_registry and agent_name != primary_agent:
                agent_responses[agent_name] = await self._simulate_agent_response(agent_name, analysis)

        return agent_responses

    async def _simulate_agent_response(self, agent_name: str, analysis: Dict) -> Dict:
        """Simulate specialized agent response based on their capabilities"""

        agent_info = self.agent_registry.get(agent_name, {})
        capabilities = agent_info.get('capabilities', [])

        # Generate a realistic response based on agent type
        if agent_name == 'intelligence':
            return {
                'agent_name': 'intelligence',
                'analysis_type': 'financial_operational',
                'key_metrics': {
                    'revenue_trend': '+12.5% QoQ',
                    'cash_flow_health': 'Concerning - 40% collection rate',
                    'profitability': '80.06% gross margin (excellent)',
                    'operational_efficiency': '92% project completion rate'
                },
                'insights': [
                    'Strong profitability but critical cash flow challenges',
                    'Collection efficiency significantly below industry standard',
                    'Revenue growth trending positive but cash timing misaligned'
                ],
                'confidence_score': 0.89
            }

        elif agent_name == 'strategy':
            return {
                'agent_name': 'strategy',
                'analysis_type': 'strategic_positioning',
                'strategic_insights': {
                    'competitive_position': 'Strong value delivery, pricing power',
                    'market_opportunities': 'Expansion limited by cash constraints',
                    'risk_factors': 'Customer concentration, payment timing'
                },
                'recommendations': [
                    'Implement milestone billing to improve cash flow timing',
                    'Diversify customer base to reduce concentration risk',
                    'Consider factoring or invoice financing for working capital'
                ],
                'confidence_score': 0.83
            }

        elif agent_name == 'forecasting':
            return {
                'agent_name': 'forecasting',
                'analysis_type': 'predictive_analytics',
                'forecasts': {
                    'revenue_projection': '+15% growth next quarter',
                    'cash_flow_forecast': 'Improvement expected with collection focus',
                    'risk_scenarios': 'Best: +20% growth, Worst: Cash crunch in 60 days'
                },
                'predictions': [
                    'Q1 revenue likely to exceed $1.2M based on pipeline',
                    'Cash flow crisis probable without collection improvements',
                    'Customer churn risk elevated for payment-delayed accounts'
                ],
                'confidence_score': 0.76
            }

        else:
            # Generic response for other agents
            return {
                'agent_name': agent_name,
                'analysis_type': 'specialized_analysis',
                'capabilities_used': capabilities,
                'insights': [f'{agent_name} analysis completed with relevant insights'],
                'confidence_score': 0.80
            }

    async def _synthesize_response(self, question: str, analysis: Dict, agent_responses: Dict) -> Dict:
        """Use Claude to synthesize a coherent response from multiple agents"""

        synthesis_prompt = f"""
        You are an executive AI assistant synthesizing insights from multiple business intelligence agents.

        Original Question: "{question}"
        Question Analysis: {json.dumps(analysis, indent=2)}
        Agent Responses: {json.dumps(agent_responses, indent=2)}

        Synthesize these agent responses into a comprehensive, executive-level answer that directly addresses the user's question.

        Provide:

        1. DIRECT_ANSWER:
           - Clear, specific response to the question asked
           - Key numbers, facts, and metrics that matter
           - Bottom-line assessment or conclusion
           - Confidence level in this answer (0-1)

        2. BUSINESS_IMPLICATIONS:
           - What this means for business performance and strategy
           - Impact on key stakeholders and decisions
           - Risks and opportunities identified
           - Strategic considerations for leadership

        3. RECOMMENDED_ACTIONS:
           - Specific, prioritized next steps
           - Timeline and urgency for each action
           - Resources, budget, or stakeholders required
           - Success metrics to track progress

        4. SUPPORTING_EVIDENCE:
           - Key data points and trends supporting the conclusion
           - Relevant benchmarks or historical context
           - Quality and reliability of the underlying data
           - Areas where more data might be needed

        5. FOLLOW_UP_OPPORTUNITIES:
           - Related questions the user should consider asking
           - Deeper analysis that would be valuable
           - Monitoring and tracking recommendations
           - Early warning indicators to watch

        6. VISUALIZATION_RECOMMENDATIONS:
           - Specific charts, dashboards, or reports that would help
           - Interactive elements that would add value
           - Real-time monitoring suggestions
           - Data presentation best practices for this topic

        Make the response:
        - Conversational and engaging
        - Executive-level (strategic, not just tactical)
        - Immediately actionable
        - Honest about uncertainties and limitations
        - Forward-looking where appropriate

        Respond in valid JSON format.
        """

        try:
            response = await self.claude_client.messages.create(
                model=self.model,
                max_tokens=2500,
                messages=[{"role": "user", "content": synthesis_prompt}]
            )

            synthesized_text = response.content[0].text
            synthesized = json.loads(synthesized_text)

            # Add response metadata
            synthesized['RESPONSE_METADATA'] = {
                'original_question': question,
                'agents_consulted': list(agent_responses.keys()),
                'response_timestamp': datetime.now().isoformat(),
                'synthesis_confidence': self._calculate_overall_confidence(agent_responses),
                'complexity_handled': analysis.get('AGENT_ROUTING', {}).get('Estimated_Complexity', 5),
                'processing_time_seconds': time.time() - self.start_time if hasattr(self, 'start_time') else 0
            }

            logger.info("Response synthesis completed successfully")
            return synthesized

        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse synthesis response as JSON: {e}")
            return self._fallback_response_synthesis(question, agent_responses)
        except Exception as e:
            logger.error(f"Response synthesis failed: {e}")
            return self._fallback_response_synthesis(question, agent_responses)

    def _fallback_question_analysis(self, question: str) -> Dict:
        """Fallback analysis when Claude is unavailable"""
        logger.info("Using fallback question analysis")

        # Simple keyword-based analysis
        question_lower = question.lower()

        if any(word in question_lower for word in ['why', 'cause', 'reason', 'because']):
            intent_type = 'diagnostic'
        elif any(word in question_lower for word in ['what if', 'predict', 'forecast', 'future']):
            intent_type = 'forecasting'
        elif any(word in question_lower for word in ['how', 'improve', 'optimize', 'better']):
            intent_type = 'strategic'
        elif any(word in question_lower for word in ['revenue', 'profit', 'cash', 'financial']):
            intent_type = 'analytical'
        else:
            intent_type = 'explanatory'

        return {
            'INTENT_CLASSIFICATION': {
                'Type': intent_type,
                'Urgency': 'medium',
                'Complexity': 'moderate',
                'Time_Horizon': 'current'
            },
            'AGENT_ROUTING': {
                'Primary_Agent': 'intelligence',
                'Supporting_Agents': ['strategy'],
                'Coordination_Type': 'sequential',
                'Estimated_Complexity': 5
            },
            'RESPONSE_REQUIREMENTS': {
                'Format': 'conversational',
                'Detail_Level': 'executive_summary'
            }
        }

    def _fallback_response_synthesis(self, question: str, agent_responses: Dict) -> Dict:
        """Fallback response when Claude synthesis fails"""
        logger.info("Using fallback response synthesis")

        # Extract key insights from agent responses
        all_insights = []
        for response in agent_responses.values():
            if 'insights' in response:
                all_insights.extend(response['insights'])

        return {
            'DIRECT_ANSWER': {
                'response': f"Based on analysis of your question '{question}', here are the key findings from our business intelligence agents.",
                'confidence': 0.75
            },
            'BUSINESS_IMPLICATIONS': {
                'summary': 'Multiple factors identified requiring attention',
                'key_insights': all_insights[:3]  # Top 3 insights
            },
            'RECOMMENDED_ACTIONS': [
                'Review detailed agent findings',
                'Prioritize actions based on business impact',
                'Monitor key metrics for progress'
            ],
            'RESPONSE_METADATA': {
                'original_question': question,
                'agents_consulted': list(agent_responses.keys()),
                'response_timestamp': datetime.now().isoformat(),
                'fallback_mode': True
            }
        }

    def _calculate_overall_confidence(self, agent_responses: Dict) -> float:
        """Calculate overall confidence from agent responses"""
        confidences = []
        for response in agent_responses.values():
            if 'confidence_score' in response:
                confidences.append(response['confidence_score'])

        return sum(confidences) / len(confidences) if confidences else 0.75

    def _update_conversation_history(self, question: str, response: Dict):
        """Update conversation history"""
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'answer': response.get('DIRECT_ANSWER', {}).get('response', ''),
            'agents_involved': response.get('RESPONSE_METADATA', {}).get('agents_consulted', [])
        })

        # Keep only last 10 conversations
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]

    def _initialize_agent_registry(self) -> Dict:
        """Initialize registry of available AI agents"""
        return {
            'intelligence': {
                'description': 'Financial and operational intelligence analysis',
                'capabilities': ['financial_analysis', 'kpi_calculation', 'trend_analysis'],
                'specialties': ['revenue', 'profitability', 'cash_flow', 'efficiency']
            },
            'discovery': {
                'description': 'Data discovery and pattern recognition',
                'capabilities': ['data_exploration', 'anomaly_detection', 'relationship_mapping'],
                'specialties': ['data_quality', 'hidden_patterns', 'correlations']
            },
            'strategy': {
                'description': 'Strategic analysis and market insights',
                'capabilities': ['strategic_planning', 'competitive_analysis', 'market_trends'],
                'specialties': ['positioning', 'opportunities', 'threats', 'scenarios']
            },
            'forecasting': {
                'description': 'Predictive analytics and forecasting',
                'capabilities': ['time_series_analysis', 'predictive_modeling', 'scenario_planning'],
                'specialties': ['revenue_forecasting', 'demand_planning', 'risk_modeling']
            },
            'decision': {
                'description': 'Decision support and optimization',
                'capabilities': ['decision_trees', 'optimization', 'trade_off_analysis'],
                'specialties': ['resource_allocation', 'prioritization', 'trade_offs']
            },
            'visualization': {
                'description': 'Dynamic visualization and dashboard creation',
                'capabilities': ['chart_generation', 'dashboard_design', 'interactive_elements'],
                'specialties': ['executive_dashboards', 'drill_down', 'real_time_charts']
            }
        }

    def _create_error_response(self, error_message: str, execution_time: float) -> Dict:
        """Create standardized error response"""
        return {
            'agent_name': self.name,
            'status': 'error',
            'error': error_message,
            'execution_time': execution_time,
            'timestamp': datetime.now().isoformat()
        }

def handler(ctx, data: io.BytesIO = None):
    """OCI Function handler for Query Router Agent"""

    try:
        # Parse input data
        if data and data.getvalue():
            input_data = json.loads(data.getvalue())
        else:
            input_data = {}

        logger.info("Query Router Agent function invoked")

        # Extract configuration from environment
        config = {
            'claude_api_key': os.environ.get('CLAUDE_API_KEY'),
            'claude_model': os.environ.get('CLAUDE_MODEL', 'claude-3-5-sonnet-20241022'),
            'max_tokens': int(os.environ.get('MAX_TOKENS', '2000')),
            'enable_conversation_history': os.environ.get('ENABLE_CONVERSATION_HISTORY', 'true').lower() == 'true',
            'enable_parallel_routing': os.environ.get('ENABLE_PARALLEL_ROUTING', 'true').lower() == 'true'
        }

        # Merge with input config
        config.update(input_data.get('config', {}))

        # Initialize and execute agent
        agent = QueryRouterAgent(config)
        result = agent.execute(input_data)

        return response.Response(
            ctx,
            response_data=json.dumps(result, default=str),
            headers={"Content-Type": "application/json"}
        )

    except Exception as e:
        logger.error(f"Query Router Agent function failed: {str(e)}")
        error_result = {
            "agent_name": "query_router",
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

        return response.Response(
            ctx,
            response_data=json.dumps(error_result),
            headers={"Content-Type": "application/json"},
            status_code=500
        )