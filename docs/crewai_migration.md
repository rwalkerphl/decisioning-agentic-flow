# CrewAI Migration Framework

This document outlines the systematic approach to migrate from the MVP Claude Code Tasks implementation to a production-ready CrewAI multi-agent system.

## 🎯 Migration Strategy

### Phase 1: Foundation (Current MVP)
**Claude Code Tasks Implementation**
- Simple orchestration with Python asyncio
- Direct MCP connector usage
- Basic agent coordination
- Streamlit dashboard

### Phase 2: Hybrid Implementation
**Gradual CrewAI Integration**
- Replace orchestrator with CrewAI Crew
- Maintain existing agent logic
- Add CrewAI agent wrappers
- Parallel testing

### Phase 3: Full CrewAI Production
**Complete Migration**
- Native CrewAI agents
- Advanced coordination
- Production deployment
- Monitoring and scaling

## 🏗️ Architecture Comparison

### Current MVP Architecture
```python
# Simple orchestration
class BusinessIntelOrchestrator:
    async def run_analysis(self):
        # Sequential/parallel task execution
        discovery = await self._run_discovery_agent()
        metrics = await self._run_metrics_agent()
        patterns = await self._run_pattern_agent()
        dashboard = await self._run_dashboard_agent()
```

### Target CrewAI Architecture
```python
from crewai import Agent, Task, Crew

# CrewAI implementation
class BusinessIntelCrew:
    def __init__(self):
        self.discovery_agent = self._create_discovery_agent()
        self.metrics_agent = self._create_metrics_agent()
        self.pattern_agent = self._create_pattern_agent()
        self.viz_agent = self._create_visualization_agent()

        self.crew = Crew(
            agents=[self.discovery_agent, self.metrics_agent,
                   self.pattern_agent, self.viz_agent],
            tasks=self._create_tasks(),
            verbose=True
        )
```

## 📋 Migration Mapping

### 1. Agent Conversion

| MVP Agent | CrewAI Equivalent | Migration Complexity |
|-----------|------------------|---------------------|
| DataDiscoveryAgent | Discovery Agent | Low - Direct conversion |
| BusinessMetricsAgent | Analytics Agent | Medium - Add LLM reasoning |
| PatternRecognitionAgent | Insight Agent | High - Add ML capabilities |
| DashboardAgent | Visualization Agent | Medium - Template system |
| Orchestrator | Crew Manager | Low - Framework handles this |

### 2. Task Mapping

```python
# MVP Task Structure
@dataclass
class AgentResult:
    agent_name: str
    task_id: str
    status: str
    data: Dict[str, Any]
    insights: List[str]
    recommendations: List[str]

# CrewAI Task Structure
discovery_task = Task(
    description="Discover and catalog database schema",
    agent=discovery_agent,
    expected_output="JSON schema with tables, relationships, and quality metrics"
)
```

### 3. Tool Integration

```python
# MVP: Direct MCP usage
class OracleMCPConnector:
    def execute_query(self, sql: str):
        # Direct MCP call
        pass

# CrewAI: Tool wrapper
from crewai_tools import BaseTool

class OracleTool(BaseTool):
    name: str = "Oracle Database Query"
    description: str = "Execute SQL queries against Oracle database"

    def _run(self, query: str) -> str:
        # Wrap MCP connector
        return self.mcp_connector.execute_query(query)
```

## 🚀 Implementation Plan

### Step 1: Preparation (Week 1)

```bash
# Install CrewAI dependencies
pip install crewai crewai-tools langchain-openai

# Create hybrid structure
mkdir -p src/crewai_agents/
mkdir -p src/crewai_tools/
mkdir -p src/hybrid_orchestration/
```

### Step 2: Tool Wrappers (Week 2)

```python
# src/crewai_tools/oracle_tool.py
from crewai_tools import BaseTool
from ..connectors.oracle_mcp import OracleMCPConnector

class OracleQueryTool(BaseTool):
    name: str = "oracle_query"
    description: str = "Execute SQL queries against Oracle FUSION_DEMO schema"

    def __init__(self):
        super().__init__()
        self.connector = OracleMCPConnector()

    def _run(self, sql_query: str) -> str:
        """Execute SQL query and return results"""
        try:
            results = self.connector.execute_query(sql_query)
            return f"Query executed successfully. Results: {results}"
        except Exception as e:
            return f"Query failed: {str(e)}"

class SchemaDiscoveryTool(BaseTool):
    name: str = "schema_discovery"
    description: str = "Discover database schema and relationships"

    def _run(self, schema_name: str = "FUSION_DEMO") -> str:
        """Discover and return schema information"""
        discovery_queries = [
            "SELECT table_name FROM user_tables ORDER BY table_name",
            "SELECT COUNT(*) as row_count FROM user_tables"
        ]

        results = {}
        for query in discovery_queries:
            results[query] = self.connector.execute_query(query)

        return str(results)
```

### Step 3: Agent Migration (Week 3)

```python
# src/crewai_agents/discovery_agent.py
from crewai import Agent
from ..crewai_tools.oracle_tool import OracleQueryTool, SchemaDiscoveryTool

def create_discovery_agent():
    return Agent(
        role="Database Discovery Specialist",
        goal="Discover and catalog all available data sources with their schemas and relationships",
        backstory="""You are an expert database analyst who specializes in quickly
        understanding complex database schemas. You can identify key business entities,
        relationships, and data quality issues.""",
        tools=[OracleQueryTool(), SchemaDiscoveryTool()],
        verbose=True,
        allow_delegation=False
    )

# src/crewai_agents/metrics_agent.py
def create_metrics_agent():
    return Agent(
        role="Business Metrics Analyst",
        goal="Calculate comprehensive business KPIs and health scores",
        backstory="""You are a senior business analyst with expertise in financial
        metrics, operational KPIs, and business health assessment. You can identify
        critical business issues and opportunities.""",
        tools=[OracleQueryTool()],
        verbose=True
    )

# src/crewai_agents/insight_agent.py
def create_insight_agent():
    return Agent(
        role="Business Intelligence Specialist",
        goal="Identify patterns, correlations, and actionable business insights",
        backstory="""You are a seasoned business intelligence expert who can spot
        hidden patterns in data and translate them into actionable business recommendations.""",
        tools=[OracleQueryTool()],
        verbose=True
    )
```

### Step 4: Task Definitions (Week 4)

```python
# src/crewai_tasks/business_analysis_tasks.py
from crewai import Task

def create_discovery_task(agent):
    return Task(
        description="""
        Discover and analyze the Oracle FUSION_DEMO database schema:
        1. List all tables with row counts
        2. Identify primary keys and foreign key relationships
        3. Assess data quality and completeness
        4. Identify core business entities (customers, projects, transactions)

        Return a comprehensive JSON report with schema information.
        """,
        agent=agent,
        expected_output="JSON schema report with tables, relationships, and business entities"
    )

def create_metrics_task(agent, discovery_context):
    return Task(
        description=f"""
        Based on the discovered schema: {discovery_context}

        Calculate key business metrics:
        1. Financial health (revenue, costs, margins, AR)
        2. Operational efficiency (project metrics, utilization)
        3. Customer analytics (concentration, payment behavior)
        4. Cash flow analysis (collections, aging)

        Provide business health scores and critical issue identification.
        """,
        agent=agent,
        expected_output="Business metrics report with KPIs, health scores, and issue flags"
    )

def create_insights_task(agent, metrics_context):
    return Task(
        description=f"""
        Based on the business metrics: {metrics_context}

        Generate actionable business insights:
        1. Identify unusual patterns and anomalies
        2. Find correlations across business areas
        3. Prioritize improvement opportunities
        4. Create implementation roadmap

        Focus on high-impact, actionable recommendations.
        """,
        agent=agent,
        expected_output="Business insights report with prioritized recommendations"
    )
```

### Step 5: Crew Assembly (Week 5)

```python
# src/business_intel_crew.py
from crewai import Crew
from .crewai_agents.discovery_agent import create_discovery_agent
from .crewai_agents.metrics_agent import create_metrics_agent
from .crewai_agents.insight_agent import create_insight_agent
from .crewai_tasks.business_analysis_tasks import *

class BusinessIntelligenceCrew:
    def __init__(self):
        # Create agents
        self.discovery_agent = create_discovery_agent()
        self.metrics_agent = create_metrics_agent()
        self.insight_agent = create_insight_agent()

        # Create tasks
        self.discovery_task = create_discovery_task(self.discovery_agent)
        self.metrics_task = create_metrics_task(self.metrics_agent, "{discovery_output}")
        self.insights_task = create_insights_task(self.insight_agent, "{metrics_output}")

        # Assemble crew
        self.crew = Crew(
            agents=[self.discovery_agent, self.metrics_agent, self.insight_agent],
            tasks=[self.discovery_task, self.metrics_task, self.insights_task],
            verbose=True,
            process="sequential"  # Can be changed to "hierarchical" for complex workflows
        )

    def run_analysis(self):
        """Execute the complete business intelligence analysis"""
        return self.crew.kickoff()

# Usage
if __name__ == "__main__":
    crew = BusinessIntelligenceCrew()
    results = crew.run_analysis()
    print(f"Analysis completed: {results}")
```

## 🔄 Testing Strategy

### Parallel Validation
```python
# Test both implementations side by side
async def validate_migration():
    # Run MVP version
    mvp_orchestrator = BusinessIntelOrchestrator()
    mvp_results = await mvp_orchestrator.run_full_analysis()

    # Run CrewAI version
    crewai_crew = BusinessIntelligenceCrew()
    crewai_results = crewai_crew.run_analysis()

    # Compare results
    comparison = compare_results(mvp_results, crewai_results)
    return comparison
```

### Performance Comparison
- **Execution Time**: Measure agent coordination overhead
- **Result Quality**: Compare insight quality and accuracy
- **Resource Usage**: Memory and CPU utilization
- **Error Handling**: Robustness and recovery

## 📊 Benefits of CrewAI Migration

### Enhanced Capabilities
1. **Advanced Agent Coordination**: Hierarchical task delegation
2. **Built-in Memory**: Agent learning and context retention
3. **Tool Integration**: Rich ecosystem of pre-built tools
4. **LLM Integration**: Natural language reasoning in agents
5. **Workflow Flexibility**: Dynamic task creation and routing

### Production Readiness
1. **Scalability**: Built-in support for distributed execution
2. **Monitoring**: Agent performance and health tracking
3. **Error Recovery**: Sophisticated retry and fallback mechanisms
4. **Configuration**: Dynamic agent and task configuration

### Developer Experience
1. **Declarative Syntax**: Clear agent and task definitions
2. **Rich Logging**: Detailed execution traces
3. **Testing Framework**: Built-in testing utilities
4. **Documentation**: Comprehensive API documentation

## 🎯 Success Criteria

### Migration Complete When:
- [ ] All MVP agents converted to CrewAI
- [ ] Results quality maintained or improved
- [ ] Performance within acceptable bounds
- [ ] Full test suite passing
- [ ] Documentation updated
- [ ] Production deployment successful

### Quality Metrics:
- **Functional Equivalence**: 95% result similarity
- **Performance**: <20% execution time increase
- **Reliability**: >99% success rate
- **Maintainability**: Reduced code complexity

This migration framework ensures a smooth transition while maintaining system reliability and improving capabilities for future enhancements.