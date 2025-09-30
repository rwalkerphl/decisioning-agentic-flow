#!/usr/bin/env python3
"""
Goose Integration Example for Decisioning Agentic Flow

This demonstrates how to use Block's Goose AI framework to orchestrate
your decision-making agents with native MCP support.
"""

import json
from pathlib import Path
from typing import Dict, List, Any
import asyncio

# Goose Extension Structure
"""
Your project structure with Goose integration:

decisioning-agentic-flow/
├── .goose/
│   ├── config.yaml              # Goose configuration
│   └── profiles.yaml            # Agent profiles
├── .goosehints                  # Business logic context
├── goose_extensions/
│   ├── __init__.py
│   ├── discovery_extension.py  # Discovery Agent
│   ├── intelligence_extension.py  # Intelligence Agent
│   ├── strategy_extension.py   # Strategy Agent
│   ├── decision_extension.py   # Decision Agent
│   └── visualization_extension.py  # Visualization Agent
└── mcp_servers/
    └── oracle_fusion.json      # MCP server config (existing)
"""

# ==================== GOOSE CONFIG (.goose/config.yaml) ====================
GOOSE_CONFIG = """
# Goose Configuration for Decisioning Agentic Flow
version: 1.0

# LLM Provider Configuration
provider:
  name: anthropic
  model: claude-sonnet-4-5-20250929
  api_key: ${ANTHROPIC_API_KEY}

# MCP Servers (Your existing Oracle connector)
mcp_servers:
  oracle-fusion-demo:
    command: "python"
    args: ["-m", "mcp_oracle_connector"]
    env:
      DB_HOST: "${ORACLE_HOST}"
      DB_PORT: "${ORACLE_PORT}"
      DB_SERVICE: "${ORACLE_SERVICE}"
      DB_USER: "${ORACLE_USER}"
      DB_PASSWORD: "${ORACLE_PASSWORD}"

# Extensions (Your Agents)
extensions:
  developer: true
  computer_controller: true
  
  # Custom agent extensions
  decisioning_agents:
    discovery:
      enabled: true
      priority: 1
      capabilities:
        - schema_analysis
        - data_quality_assessment
        - relationship_mapping
    
    intelligence:
      enabled: true
      priority: 2
      capabilities:
        - financial_analysis
        - operational_metrics
        - customer_intelligence
    
    strategy:
      enabled: true
      priority: 3
      capabilities:
        - pattern_detection
        - risk_analysis
        - opportunity_identification
    
    decision:
      enabled: true
      priority: 4
      capabilities:
        - priority_analysis
        - impact_assessment
        - resource_planning
    
    visualization:
      enabled: true
      priority: 5
      capabilities:
        - chart_generation
        - dashboard_assembly
        - report_creation

# Workflow Configuration
workflows:
  full_analysis:
    description: "Complete strategic decision analysis"
    steps:
      - agent: discovery
        task: "Discover and catalog data sources"
      - agent: intelligence
        task: "Analyze business metrics and KPIs"
      - agent: strategy
        task: "Identify patterns and opportunities"
      - agent: decision
        task: "Generate prioritized recommendations"
      - agent: visualization
        task: "Create interactive dashboard"
"""

# ==================== GOOSE HINTS (.goosehints) ====================
GOOSE_HINTS = """
# Business Context for Decisioning Agents

## Project Overview
You are orchestrating a multi-agent decisioning system that analyzes business data
and generates strategic recommendations. Each agent has a specific role in the
analysis pipeline.

## Data Source
- Primary: Oracle FUSION_DEMO database (accessed via MCP)
- Contains: Financial transactions, customer data, operational metrics

## Business Rules
1. **Discovery Agent**: Focus on data quality, completeness, and relationships
   - Flag tables with >10% null values
   - Identify foreign key relationships
   - Assess data freshness (last update timestamps)

2. **Intelligence Agent**: Calculate key business metrics
   - Revenue recognition and AR aging
   - Customer concentration risk (>20% = high risk)
   - Collection efficiency vs industry benchmarks
   - Profitability by customer/project

3. **Strategy Agent**: Identify strategic patterns
   - Revenue trends and seasonality
   - Customer payment behavior clusters
   - High-value vs high-risk customer segments
   - Operational bottlenecks

4. **Decision Agent**: Prioritize actions by impact
   - Critical: Cash flow impact >$1M or >30 days overdue
   - High: Customer risk or revenue opportunity >$500K
   - Medium: Operational efficiency improvements
   - Low: Long-term strategic initiatives

5. **Visualization Agent**: Create executive-friendly outputs
   - Dashboard must include: Health Score, Key Metrics, Top 3 Actions
   - Use traffic light colors (red/yellow/green) for clarity
   - Include financial impact estimates for all recommendations

## Success Criteria
- Analysis completes in <5 minutes
- Identifies minimum 3 critical actions
- Quantifies business impact in dollars
- Provides 30/60/90 day roadmap

## Output Format
Results should be saved to:
- decisioning_results.json (detailed analysis)
- executive_summary.json (high-level decisions)
- dashboards/data/ (visualization data)
"""

# ==================== PYTHON INTEGRATION ====================

class GooseDecisioningOrchestrator:
    """
    Orchestrator that uses Goose to execute decisioning workflow.
    
    This replaces your custom orchestrator.py with Goose-native execution.
    """
    
    def __init__(self, config_path: Path = Path(".goose/config.yaml")):
        self.config_path = config_path
        self.results = {}
    
    async def run_full_analysis(self, data_source: str = "oracle-fusion-demo"):
        """
        Execute complete decisioning workflow using Goose.
        
        In practice, you would interact with Goose via:
        1. CLI: `goose` command with natural language
        2. Python API: goose.execute() calls
        3. Desktop App: Visual interface
        """
        
        print("🤖 Starting Goose-powered Decisioning Flow...")
        
        # Phase 1: Discovery
        print("\n📊 Phase 1: Discovery Agent")
        discovery_prompt = f"""
        Connect to the {data_source} MCP server and perform comprehensive data discovery:
        
        1. List all tables and their schemas
        2. Assess data quality (null counts, duplicate detection)
        3. Identify relationships between tables
        4. Calculate dataset statistics
        
        Save results to: decisioning_results.json under 'discovery' key
        """
        # In real implementation: await goose.execute(discovery_prompt)
        
        # Phase 2: Intelligence
        print("💼 Phase 2: Intelligence Agent")
        intelligence_prompt = """
        Based on the discovered data, calculate business intelligence metrics:
        
        1. Financial Health:
           - Total revenue and margin analysis
           - Accounts receivable aging (current, 30, 60, 90+ days)
           - Collection rate vs industry benchmark (85%)
        
        2. Customer Intelligence:
           - Customer concentration risk
           - Payment behavior patterns
           - Top customers by revenue and profitability
        
        3. Operational Metrics:
           - Project completion rates
           - Resource utilization
           - Billing velocity
        
        Calculate a Business Health Score (0-100) based on these metrics.
        Save results to: decisioning_results.json under 'intelligence' key
        """
        
        # Phase 3: Strategy
        print("🔍 Phase 3: Strategy Agent")
        strategy_prompt = """
        Analyze the business intelligence to identify strategic patterns:
        
        1. Pattern Detection:
           - Revenue trends and seasonality
           - Customer segment behaviors
           - Risk concentrations
        
        2. Risk Analysis:
           - Cash flow vulnerabilities
           - Customer dependency risks
           - Operational bottlenecks
        
        3. Opportunity Identification:
           - Quick wins for cash improvement
           - Strategic growth opportunities
           - Efficiency enhancements
        
        Generate minimum 10 strategic insights with confidence scores.
        Save results to: decisioning_results.json under 'strategy' key
        """
        
        # Phase 4: Decision
        print("⚡ Phase 4: Decision Agent")
        decision_prompt = """
        Synthesize all insights into prioritized strategic decisions:
        
        1. Categorize by urgency:
           - CRITICAL: Immediate action required (<48 hours)
           - HIGH: This month
           - MEDIUM: This quarter
           - LOW: Strategic/long-term
        
        2. For each decision, include:
           - Specific action description
           - Business impact ($ value)
           - Implementation timeline
           - Resource requirements
           - Success metrics
        
        3. Create 30/60/90 day roadmap
        
        Generate executive summary with top 3 critical actions.
        Save to: executive_summary.json
        """
        
        # Phase 5: Visualization
        print("📈 Phase 5: Visualization Agent")
        visualization_prompt = """
        Create interactive dashboard using the analysis results:
        
        1. Generate Streamlit dashboard with:
           - Executive summary card (Health Score, Key Metrics)
           - Financial overview charts (Revenue, AR Aging)
           - Strategic insights table
           - Decision framework with priorities
           - Recommended actions timeline
        
        2. Export chart data to: dashboards/data/
        3. Update dashboard: dashboards/decisioning_dashboard.py
        
        Use Plotly for interactive charts, color-code by severity.
        """
        
        print("\n✅ Goose Decisioning Flow Complete!")
        print("📊 Results saved to: decisioning_results.json")
        print("📈 Dashboard ready: streamlit run dashboards/decisioning_dashboard.py")
        
        return self.results
    
    def create_goose_extension(self, agent_name: str) -> str:
        """
        Generate a Goose extension for a specific agent.
        
        Extensions are Python modules that Goose can load to add
        custom capabilities.
        """
        
        extension_template = f'''"""
Goose Extension for {agent_name.title()} Agent

This extension provides {agent_name} capabilities to Goose.
"""

from goose.toolkit import Tool, toolkit
from typing import Dict, Any, List
import json

@toolkit
class {agent_name.title()}Tools:
    """Tools for {agent_name} agent operations."""
    
    @Tool(description="Perform {agent_name} analysis on business data")
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute {agent_name} analysis.
        
        Args:
            data: Input data from previous agents or data sources
            
        Returns:
            Analysis results with insights and recommendations
        """
        # Your existing agent logic here
        # This integrates with your current agent implementation
        
        results = {{
            "agent": "{agent_name}",
            "status": "complete",
            "insights": [],
            "recommendations": [],
            "confidence": 0.95
        }}
        
        return results
    
    @Tool(description="Save {agent_name} results to file")
    async def save_results(self, results: Dict[str, Any], filepath: str):
        """Save analysis results to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        return {{"saved": filepath, "status": "success"}}
'''
        return extension_template

# ==================== CLI USAGE EXAMPLES ====================

def print_usage_examples():
    """Show how to use Goose with your decisioning system."""
    
    examples = """
# ==================== USING GOOSE FOR DECISIONING ====================

## 1. Interactive CLI Mode (Recommended for exploration)

$ goose

Welcome to Goose! 🪿

> Connect to my Oracle FUSION_DEMO database and discover all data sources
[Goose uses MCP connector, analyzes schema, generates report]

> Now analyze the financial health - focus on AR aging and collection rates
[Goose calculates metrics, compares to benchmarks]

> What are the top 3 critical actions we should take?
[Goose synthesizes insights, prioritizes recommendations]

> Create an executive dashboard showing these insights
[Goose generates Streamlit dashboard with visualizations]


## 2. Workflow Automation (Production use)

$ goose --workflow=full_analysis --data-source=oracle-fusion-demo
[Goose executes all 5 agents sequentially, saves results]


## 3. Python API Integration

from goose import Goose

async def run_decisioning():
    goose = Goose(config=".goose/config.yaml")
    
    # Execute workflow
    result = await goose.execute_workflow("full_analysis")
    
    # Or individual agents
    discovery = await goose.execute("discovery_agent", 
                                   data_source="oracle-fusion-demo")
    intelligence = await goose.execute("intelligence_agent", 
                                      context=discovery)
    
    return result


## 4. Desktop App (Visual interface)

1. Launch: goose-desktop
2. Load: decisioning-agentic-flow project
3. Configure: MCP servers and agents
4. Run: "Analyze business and create strategic recommendations"
5. View: Interactive results in GUI


## 5. Custom Agent Development

# Create new agent extension
$ cd goose_extensions
$ touch predictive_agent.py

# Implement using @toolkit decorator
# Goose automatically loads and uses it


# ==================== BENEFITS OVER CUSTOM ORCHESTRATOR ====================

✅ Native MCP Integration - Your Oracle connector works immediately
✅ No Custom Orchestration Code - Goose handles agent coordination
✅ Natural Language Interface - Talk to your system in plain English
✅ Multi-LLM Support - Switch between models for different agents
✅ Built-in Monitoring - Agent execution logs and performance tracking
✅ Desktop + CLI + API - Multiple interaction modes
✅ Active Community - Open source with Block backing
✅ Production Ready - Used internally at Block (Square, Cash App)

# ==================== MIGRATION CHECKLIST ====================

[ ] Install Goose: pipx install goose-ai
[ ] Create .goose/config.yaml with your MCP server config
[ ] Write .goosehints with business logic
[ ] Convert existing agents to Goose extensions
[ ] Test workflow: goose --workflow=full_analysis
[ ] Update README with Goose instructions
[ ] Remove custom orchestrator.py (no longer needed!)
[ ] Cancel CrewAI migration (Goose handles it!)
"""
    
    print(examples)


# ==================== MAIN ====================

if __name__ == "__main__":
    print("🪿 Goose Integration Example for Decisioning Agentic Flow\n")
    
    print("=" * 70)
    print("CONFIGURATION FILES")
    print("=" * 70)
    print("\n1. .goose/config.yaml:")
    print("-" * 70)
    print(GOOSE_CONFIG)
    
    print("\n2. .goosehints:")
    print("-" * 70)
    print(GOOSE_HINTS)
    
    print("\n" + "=" * 70)
    print("ORCHESTRATOR EXAMPLE")
    print("=" * 70)
    
    # Show orchestrator
    orchestrator = GooseDecisioningOrchestrator()
    
    print("\n" + "=" * 70)
    print("USAGE EXAMPLES")
    print("=" * 70)
    print_usage_examples()
    
    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("""
1. Install Goose:
   $ pipx install goose-ai

2. Create configuration files shown above in your project

3. Test with your Oracle database:
   $ goose
   > Connect to oracle-fusion-demo and analyze financial health

4. Migrate agents to Goose extensions (optional but recommended)

5. Update your README to reference Goose instead of custom orchestrator

QUESTIONS?
- Goose Docs: https://block.github.io/goose/
- MCP Docs: https://modelcontextprotocol.io/
- GitHub: https://github.com/block/goose
""")
