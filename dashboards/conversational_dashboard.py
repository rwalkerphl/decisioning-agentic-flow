import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import asyncio
import anthropic
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

st.set_page_config(
    page_title="AI-Powered Business Intelligence",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for conversational interface
st.markdown("""
<style>
.metric-container {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 5px solid #ff4b4b;
}
.decision-card {
    background-color: #ffffff;
    padding: 1.5rem;
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin: 1rem 0;
}
.ai-response {
    background-color: #f8f9fa;
    padding: 1.5rem;
    border-radius: 0.8rem;
    border-left: 4px solid #0066cc;
    margin: 1rem 0;
}
.user-question {
    background-color: #e3f2fd;
    padding: 1rem;
    border-radius: 0.8rem;
    border-left: 4px solid #2196f3;
    margin: 1rem 0;
}
.confidence-bar {
    background-color: #e0e0e0;
    border-radius: 10px;
    height: 20px;
    margin: 0.5rem 0;
}
.confidence-fill {
    background-color: #4caf50;
    height: 100%;
    border-radius: 10px;
    transition: width 0.3s ease;
}
.chat-container {
    max-height: 400px;
    overflow-y: auto;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 0.5rem;
    background-color: #fafafa;
}
</style>
""", unsafe_allow_html=True)

class QueryRouterClient:
    """Client for interacting with the Query Router Agent"""

    def __init__(self, claude_api_key: str):
        self.claude_client = anthropic.Anthropic(api_key=claude_api_key)
        self.conversation_history = []

    async def process_question(self, question: str, dashboard_context: Dict = None) -> Dict:
        """Process question using Claude directly (simulating Query Router Agent)"""

        try:
            # For now, we'll simulate the Query Router Agent response
            # In production, this would call the actual OCI Function
            response = await self._simulate_query_router(question, dashboard_context)

            # Update conversation history
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'question': question,
                'response': response
            })

            return response

        except Exception as e:
            return {
                'DIRECT_ANSWER': {
                    'response': f"I apologize, but I encountered an error processing your question: {str(e)}",
                    'confidence': 0.0
                },
                'BUSINESS_IMPLICATIONS': {
                    'summary': 'Unable to analyze due to technical issue'
                },
                'RESPONSE_METADATA': {
                    'error': True,
                    'original_question': question
                }
            }

    async def _simulate_query_router(self, question: str, context: Dict) -> Dict:
        """Simulate Query Router Agent using Claude directly"""

        # Get current business context
        business_context = self._get_business_context()

        prompt = f"""
        You are an AI business intelligence assistant analyzing a user's question about their business data.

        Current Business Context:
        - Outstanding AR: $2.48M (98% overdue)
        - Collection Rate: 40% (vs 85% industry standard)
        - Gross Margin: 80.06% (excellent)
        - Business Health Score: 65/100 (critical)
        - Active Projects: 12 (92% completion rate)
        - Revenue: $4.12M annually

        Dashboard Context: {json.dumps(context or {}, indent=2)}
        Recent Conversation: {json.dumps(self.conversation_history[-2:], indent=2)}

        User Question: "{question}"

        Provide a comprehensive business intelligence response with:

        1. DIRECT_ANSWER:
           - Clear, specific response to the question
           - Key numbers and facts
           - Confidence level (0-1)

        2. BUSINESS_IMPLICATIONS:
           - Strategic impact
           - Risks and opportunities
           - Stakeholder considerations

        3. RECOMMENDED_ACTIONS:
           - Specific next steps
           - Timeline and priority
           - Resources needed

        4. SUPPORTING_EVIDENCE:
           - Data points supporting conclusion
           - Relevant trends
           - Benchmarks or context

        5. FOLLOW_UP_OPPORTUNITIES:
           - Related questions to explore
           - Areas for deeper analysis
           - Monitoring suggestions

        6. VISUALIZATION_RECOMMENDATIONS:
           - Charts or dashboards that would help
           - Interactive elements
           - Real-time monitoring needs

        Make the response conversational, strategic, and immediately actionable.
        Respond in JSON format.
        """

        response = await self.claude_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2500,
            messages=[{"role": "user", "content": prompt}]
        )

        try:
            result = json.loads(response.content[0].text)

            # Add metadata
            result['RESPONSE_METADATA'] = {
                'original_question': question,
                'response_timestamp': datetime.now().isoformat(),
                'confidence': result.get('DIRECT_ANSWER', {}).get('confidence', 0.85),
                'processing_method': 'claude_direct'
            }

            return result

        except json.JSONDecodeError:
            # Fallback response
            return {
                'DIRECT_ANSWER': {
                    'response': response.content[0].text,
                    'confidence': 0.75
                },
                'BUSINESS_IMPLICATIONS': {
                    'summary': 'Analysis completed with AI reasoning'
                },
                'RESPONSE_METADATA': {
                    'original_question': question,
                    'fallback_mode': True
                }
            }

    def _get_business_context(self) -> Dict:
        """Get current business context for analysis"""
        return {
            'financial_health': {
                'outstanding_ar': 2481103,
                'collection_rate': 0.40,
                'gross_margin': 0.8006,
                'revenue_annual': 4120000
            },
            'operational_metrics': {
                'active_projects': 12,
                'completion_rate': 0.92,
                'business_health_score': 65
            },
            'risk_factors': [
                'Cash flow crisis',
                'High overdue AR percentage',
                'Below-industry collection rates'
            ]
        }

@st.cache_data
def load_decisioning_results():
    """Load existing decisioning results"""
    try:
        with open('decisioning_results.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return simulated data if file doesn't exist
        return {
            "agent_results": {
                "discovery": {"insights": ["Data ecosystem analysis completed"]},
                "intelligence": {"insights": ["Financial intelligence generated"]},
                "strategy": {"insights": ["Strategic patterns identified"]},
                "decision": {"insights": ["Decision framework created"]}
            }
        }

def initialize_query_router():
    """Initialize the Query Router client"""

    # Get Claude API key from secrets or environment
    claude_api_key = None

    if hasattr(st, 'secrets') and 'claude_api_key' in st.secrets:
        claude_api_key = st.secrets.claude_api_key

    if not claude_api_key:
        st.error("🔑 Claude API key not configured. Please add it to Streamlit secrets.")
        st.info("Add your Claude API key to `.streamlit/secrets.toml`:")
        st.code('claude_api_key = "your-api-key-here"')
        return None

    return QueryRouterClient(claude_api_key)

def render_ai_assistant():
    """Render the AI assistant interface"""

    st.subheader("🤖 Ask Your Business Intelligence AI")
    st.markdown("Ask questions about your business data in natural language.")

    # Initialize session state
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    if 'query_router' not in st.session_state:
        st.session_state.query_router = initialize_query_router()

    if not st.session_state.query_router:
        return

    # Example questions
    with st.expander("💡 Example Questions"):
        example_questions = [
            "Why is our cash flow declining despite good profits?",
            "Which customers are at highest risk of churning?",
            "What's driving the increase in project costs?",
            "How can we improve our collection efficiency?",
            "What would happen if we lost our top 3 customers?",
            "Where should we focus our sales efforts next quarter?"
        ]

        for question in example_questions:
            if st.button(f"❓ {question}", key=f"example_{hash(question)}"):
                st.session_state.current_question = question
                st.experimental_rerun()

    # Question input
    col1, col2 = st.columns([4, 1])

    with col1:
        question = st.text_input(
            "Ask anything about your business:",
            placeholder="e.g., Why is our collection rate so low?",
            value=st.session_state.get('current_question', ''),
            key="question_input"
        )

    with col2:
        ask_button = st.button("🧠 Ask AI", type="primary")

    # Process question
    if (ask_button or st.session_state.get('current_question')) and question:
        if 'current_question' in st.session_state:
            del st.session_state.current_question

        with st.spinner("🔍 AI is analyzing your question..."):
            # Get dashboard context
            dashboard_context = {
                'current_page': 'conversational_dashboard',
                'visible_metrics': ['revenue', 'cash_flow', 'projects', 'customers'],
                'timestamp': datetime.now().isoformat()
            }

            # Process question asynchronously
            try:
                response = asyncio.run(
                    st.session_state.query_router.process_question(question, dashboard_context)
                )

                # Add to conversation history
                st.session_state.conversation_history.append({
                    'question': question,
                    'response': response,
                    'timestamp': datetime.now()
                })

                # Display response
                display_ai_response(response)

            except Exception as e:
                st.error(f"❌ Error processing question: {str(e)}")

    # Display conversation history
    render_conversation_history()

def display_ai_response(response: Dict):
    """Display AI response in a structured format"""

    # Direct answer
    direct_answer = response.get('DIRECT_ANSWER', {})
    if direct_answer:
        st.markdown('<div class="ai-response">', unsafe_allow_html=True)
        st.markdown("**🎯 Answer:**")
        st.write(direct_answer.get('response', 'No response available'))

        # Confidence indicator
        confidence = direct_answer.get('confidence', response.get('RESPONSE_METADATA', {}).get('confidence', 0.85))
        st.markdown(f"**Confidence:** {confidence:.1%}")

        # Visual confidence bar
        confidence_percent = confidence * 100
        st.markdown(f"""
        <div class="confidence-bar">
            <div class="confidence-fill" style="width: {confidence_percent}%"></div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Create tabs for different aspects of the response
    tabs = st.tabs(["💼 Business Impact", "⚡ Actions", "📊 Evidence", "🔍 Follow-up", "📈 Visualizations"])

    with tabs[0]:
        # Business implications
        implications = response.get('BUSINESS_IMPLICATIONS', {})
        if implications:
            st.markdown("**Strategic Impact:**")
            st.write(implications.get('summary', implications.get('strategic_impact', 'No implications available')))

            if 'risks' in implications:
                st.markdown("**🚨 Risks:**")
                for risk in implications['risks']:
                    st.write(f"• {risk}")

            if 'opportunities' in implications:
                st.markdown("**💡 Opportunities:**")
                for opp in implications['opportunities']:
                    st.write(f"• {opp}")

    with tabs[1]:
        # Recommended actions
        actions = response.get('RECOMMENDED_ACTIONS', [])
        if actions:
            st.markdown("**Immediate Next Steps:**")
            for i, action in enumerate(actions, 1):
                if isinstance(action, dict):
                    st.write(f"{i}. **{action.get('action', 'Action')}**")
                    if 'timeline' in action:
                        st.write(f"   📅 Timeline: {action['timeline']}")
                    if 'impact' in action:
                        st.write(f"   💥 Impact: {action['impact']}")
                else:
                    st.write(f"{i}. {action}")
        else:
            st.info("No specific actions recommended at this time.")

    with tabs[2]:
        # Supporting evidence
        evidence = response.get('SUPPORTING_EVIDENCE', {})
        if evidence:
            st.markdown("**📈 Supporting Data:**")

            if isinstance(evidence, dict):
                for key, value in evidence.items():
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
            else:
                st.write(evidence)
        else:
            st.info("Additional evidence available in detailed analysis.")

    with tabs[3]:
        # Follow-up opportunities
        follow_ups = response.get('FOLLOW_UP_OPPORTUNITIES', [])
        if follow_ups:
            st.markdown("**🔍 Related Questions:**")
            for follow_up in follow_ups:
                if st.button(f"❓ {follow_up}", key=f"followup_{hash(follow_up)}"):
                    st.session_state.current_question = follow_up
                    st.experimental_rerun()
        else:
            st.info("Ask more questions to explore deeper insights.")

    with tabs[4]:
        # Visualization recommendations
        viz_recs = response.get('VISUALIZATION_RECOMMENDATIONS', {})
        if viz_recs:
            st.markdown("**📊 Suggested Visualizations:**")

            if isinstance(viz_recs, dict):
                for viz_type, description in viz_recs.items():
                    st.write(f"• **{viz_type.replace('_', ' ').title()}:** {description}")
            elif isinstance(viz_recs, list):
                for viz in viz_recs:
                    st.write(f"• {viz}")
            else:
                st.write(viz_recs)

            if st.button("📈 Generate Recommended Charts", key="generate_viz"):
                st.info("🚧 Dynamic chart generation coming soon!")
        else:
            st.info("Current visualizations should be sufficient for this analysis.")

def render_conversation_history():
    """Render conversation history"""

    if st.session_state.conversation_history:
        with st.expander(f"💬 Conversation History ({len(st.session_state.conversation_history)} messages)"):
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)

            for i, conversation in enumerate(reversed(st.session_state.conversation_history[-5:])):
                # User question
                st.markdown(f'<div class="user-question">', unsafe_allow_html=True)
                st.markdown(f"**You:** {conversation['question']}")
                st.markdown(f"*{conversation['timestamp'].strftime('%H:%M:%S')}*")
                st.markdown('</div>', unsafe_allow_html=True)

                # AI response summary
                response = conversation['response']
                answer = response.get('DIRECT_ANSWER', {}).get('response', 'Response not available')[:200]
                confidence = response.get('RESPONSE_METADATA', {}).get('confidence', 0.85)

                st.markdown('<div class="ai-response">', unsafe_allow_html=True)
                st.markdown(f"**AI:** {answer}{'...' if len(answer) >= 200 else ''}")
                st.markdown(f"*Confidence: {confidence:.1%}*")
                st.markdown('</div>', unsafe_allow_html=True)

                if i < len(st.session_state.conversation_history) - 1:
                    st.markdown("---")

            st.markdown('</div>', unsafe_allow_html=True)

            # Clear history button
            if st.button("🗑️ Clear History"):
                st.session_state.conversation_history = []
                st.experimental_rerun()

def render_main_dashboard():
    """Render the main dashboard content (existing functionality)"""

    results = load_decisioning_results()

    # Executive Alert Banner
    st.error("🚨 **CRITICAL ALERT**: Cash flow crisis detected - Immediate action required!")

    # Key Decision Metrics
    st.header("📊 Executive Decision Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Business Health Score",
            "65/100",
            delta="Critical",
            delta_color="inverse"
        )

    with col2:
        st.metric(
            "Outstanding AR",
            "$2.48M",
            delta="98% Overdue",
            delta_color="inverse"
        )

    with col3:
        st.metric(
            "Collection Rate",
            "40%",
            delta="vs 85% Industry",
            delta_color="inverse"
        )

    with col4:
        st.metric(
            "Cash Recovery Target",
            "$1.8M",
            delta="60-120 days",
            delta_color="normal"
        )

    # Strategic Decisions Section
    st.header("⚡ Strategic Decisions Required")

    decisions_data = [
        {
            "Decision": "Emergency Collections Program",
            "Timeline": "48 hours",
            "Impact": "$1M+ recovery",
            "Priority": "Critical",
            "Owner": "CFO"
        },
        {
            "Decision": "Milestone Billing Implementation",
            "Timeline": "30 days",
            "Impact": "40% faster cash",
            "Priority": "High",
            "Owner": "Operations"
        },
        {
            "Decision": "Customer Portfolio Optimization",
            "Timeline": "90 days",
            "Impact": "70% bad debt reduction",
            "Priority": "Medium",
            "Owner": "Sales"
        }
    ]

    decisions_df = pd.DataFrame(decisions_data)
    st.dataframe(decisions_df, use_container_width=True)

def main():
    """Main dashboard function"""

    st.title("🤖 AI-Powered Business Intelligence Dashboard")
    st.markdown("**Conversational Intelligence with Autonomous Agents**")

    # Main layout: Dashboard content + AI Assistant
    col1, col2 = st.columns([2, 1])

    with col1:
        render_main_dashboard()

    with col2:
        render_ai_assistant()

    # Sidebar Information
    st.sidebar.header("🤖 AI-Powered System")
    st.sidebar.info("""
    **Conversational Agents:**
    • Query Router Agent (Claude)
    • Intelligence Agent
    • Discovery Agent
    • Strategy Agent
    • Decision Agent
    • Visualization Agent
    """)

    st.sidebar.header("💬 How to Use")
    st.sidebar.write("""
    1. Ask questions in natural language
    2. Get AI-powered insights instantly
    3. Follow up with related questions
    4. Explore suggested visualizations
    """)

    st.sidebar.header("🔄 Last Analysis")
    st.sidebar.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    if st.sidebar.button("🚀 Run New Analysis"):
        st.cache_data.clear()
        st.experimental_rerun()

if __name__ == "__main__":
    main()