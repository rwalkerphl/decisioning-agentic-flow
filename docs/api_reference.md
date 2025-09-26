# API Reference - Decisioning Agentic Flow

## 🤖 Core Components

### DecisioningOrchestrator

Main orchestrator class for coordinating autonomous agents.

```python
from src.orchestration.orchestrator import DecisioningOrchestrator

# Initialize orchestrator
orchestrator = DecisioningOrchestrator(config_file="config/bi_config.json")

# Run full analysis
results = await orchestrator.run_decisioning_analysis("strategic_business_health")
```

#### Methods

**`__init__(config_file: str)`**
- **Purpose**: Initialize the orchestrator with configuration
- **Parameters**:
  - `config_file`: Path to JSON configuration file
- **Returns**: DecisioningOrchestrator instance

**`run_decisioning_analysis(analysis_type: str) -> Dict`**
- **Purpose**: Execute complete decisioning workflow
- **Parameters**:
  - `analysis_type`: Type of analysis ("strategic_business_health", "operational_efficiency", etc.)
- **Returns**: Dictionary containing workflow results and agent outputs
- **Example**:
```python
results = await orchestrator.run_decisioning_analysis("strategic_business_health")
print(f"Generated {results['workflow']['total_insights']} insights")
```

## 📊 Data Models

### AgentResult

Standard result format for all agents.

```python
@dataclass
class AgentResult:
    agent_name: str              # Name of the agent
    task_id: str                 # Unique task identifier
    status: str                  # "success", "error", "partial"
    data: Dict[str, Any]         # Agent-specific data
    insights: List[str]          # Business insights discovered
    recommendations: List[str]   # Actionable recommendations
    timestamp: datetime          # Execution timestamp
    execution_time: float        # Time taken in seconds
    confidence_score: float      # Reliability score (0-1)
```

**Usage Example:**
```python
# Access agent results
discovery_result = results["agent_results"]["discovery"]
print(f"Agent: {discovery_result.agent_name}")
print(f"Confidence: {discovery_result.confidence_score}")
print(f"Insights: {discovery_result.insights}")
```

### DataSource

Configuration for data source connections.

```python
@dataclass
class DataSource:
    name: str                    # Data source identifier
    type: str                    # "oracle_mcp", "api", "file"
    config: Dict[str, Any]       # Connection configuration
    enabled: bool = True         # Whether source is active
    status: str = "inactive"     # Connection status
    schema_info: Optional[Dict] = None  # Schema metadata
    last_updated: Optional[datetime] = None  # Last refresh time
    refresh_interval: str = "1h" # Refresh frequency
    priority: int = 1            # Processing priority
```

## 🔧 Configuration API

### Configuration Structure

```json
{
  "project": {
    "name": "string",
    "version": "string",
    "description": "string"
  },
  "data_sources": [
    {
      "name": "string",
      "type": "oracle_mcp|api|file",
      "enabled": true,
      "config": {
        "schema": "string",
        "connection_name": "string",
        "tables": ["string"]
      },
      "refresh_interval": "1h|30m|24h",
      "priority": 1
    }
  ],
  "agents": {
    "discovery_agent": {
      "enabled": true,
      "timeout": 300,
      "retry_attempts": 3,
      "cache_duration": "24h"
    },
    "metrics_agent": {
      "enabled": true,
      "timeout": 600,
      "parallel_queries": true,
      "metrics": ["financial_health", "operational_efficiency"]
    }
  },
  "workflow": {
    "parallel_execution": true,
    "max_concurrent_agents": 4,
    "timeout": 1800
  },
  "output": {
    "format": "json",
    "include_raw_data": false,
    "compress_results": true
  }
}
```

### Configuration Validation

```python
def validate_config(config: Dict) -> bool:
    """Validate configuration structure"""
    required_keys = ["project", "data_sources", "agents"]
    return all(key in config for key in required_keys)

# Usage
with open("config/bi_config.json") as f:
    config = json.load(f)
    if validate_config(config):
        orchestrator = DecisioningOrchestrator()
```

## 🎯 Agent APIs

### Discovery Agent

**Purpose**: Data discovery and cataloging

```python
async def _run_discovery_agent(self) -> AgentResult:
    """
    Discover and analyze data sources

    Returns:
        AgentResult containing:
        - data_ecosystem: Overview of data landscape
        - business_entities: Categorized data structures
        - data_relationships: Foreign key mappings
        - anomaly_flags: Data quality issues
    """
```

**Output Structure:**
```python
{
    "data_ecosystem": {
        "primary_source": "string",
        "total_entities": int,
        "business_domains": ["string"],
        "data_quality_score": float
    },
    "business_entities": {
        "projects": {
            "tables": ["string"],
            "total_records": int,
            "key_metrics": ["string"]
        }
    },
    "data_relationships": {
        "strong_links": int,
        "referential_integrity": float
    },
    "anomaly_flags": ["string"]
}
```

### Intelligence Agent

**Purpose**: Business metrics and KPI analysis

```python
async def _run_intelligence_agent(self) -> AgentResult:
    """
    Analyze business performance metrics

    Returns:
        AgentResult containing:
        - financial_intelligence: Revenue, margin, cash flow analysis
        - operational_intelligence: Efficiency and performance metrics
        - customer_intelligence: Customer behavior and risk analysis
        - competitive_positioning: Market position assessment
    """
```

**Output Structure:**
```python
{
    "financial_intelligence": {
        "revenue_analysis": {
            "total_revenue": float,
            "gross_margin": float,
            "profitability_tier": "string"
        },
        "cash_flow_intelligence": {
            "outstanding_ar": float,
            "collection_efficiency": float,
            "liquidity_risk": "string"
        }
    },
    "operational_intelligence": {
        "project_performance": {
            "delivery_efficiency": float,
            "completion_rate": float
        }
    }
}
```

### Strategy Agent

**Purpose**: Pattern recognition and strategic insights

```python
async def _run_strategy_agent(self) -> AgentResult:
    """
    Identify strategic patterns and opportunities

    Returns:
        AgentResult containing:
        - strategic_patterns: Business model analysis
        - market_positioning: Competitive assessment
        - transformation_opportunities: Improvement initiatives
    """
```

### Decision Agent

**Purpose**: Strategic decision synthesis

```python
async def _run_decision_agent(self) -> AgentResult:
    """
    Synthesize insights into actionable decisions

    Returns:
        AgentResult containing:
        - strategic_decision_framework: Prioritized decisions
        - decision_priorities: Ranked action items
        - success_metrics: Measurable outcomes
        - resource_allocation: Investment requirements
    """
```

### Visualization Agent

**Purpose**: Dashboard and report generation

```python
async def _run_visualization_agent(self) -> AgentResult:
    """
    Generate interactive visualizations

    Returns:
        AgentResult containing:
        - dashboard_components: UI element specifications
        - generated_artifacts: Created files
        - dashboard_url: Access URL
    """
```

## 📈 Dashboard API

### Streamlit Integration

**Core Dashboard Function:**
```python
def main():
    """Main dashboard entry point"""
    st.title("🎯 Decisioning Agentic Flow Dashboard")

    # Load results
    results = load_decisioning_results()

    # Render components
    render_executive_summary(results)
    render_financial_charts(results)
    render_agent_insights(results)
```

**Custom Component Creation:**
```python
def create_custom_metric(title: str, value: str, delta: str = None):
    """Create custom metric display"""
    st.metric(
        label=title,
        value=value,
        delta=delta,
        delta_color="normal"
    )

# Usage
create_custom_metric(
    title="Business Health Score",
    value="65/100",
    delta="Critical"
)
```

**Chart Generation:**
```python
def create_financial_chart(data: Dict) -> go.Figure:
    """Generate financial analysis chart"""
    fig = go.Figure()

    # Add revenue trend
    fig.add_trace(go.Scatter(
        x=data['dates'],
        y=data['revenue'],
        mode='lines+markers',
        name='Revenue',
        line=dict(color='green')
    ))

    return fig

# Usage
chart = create_financial_chart(financial_data)
st.plotly_chart(chart, use_container_width=True)
```

## 🔄 Workflow API

### Custom Analysis Types

```python
# Define custom analysis
ANALYSIS_TYPES = {
    "strategic_business_health": {
        "agents": ["discovery", "intelligence", "strategy", "decision", "visualization"],
        "focus": "comprehensive_strategic_analysis"
    },
    "operational_efficiency": {
        "agents": ["discovery", "intelligence", "decision"],
        "focus": "process_optimization"
    },
    "financial_health": {
        "agents": ["discovery", "intelligence", "visualization"],
        "focus": "financial_metrics_only"
    }
}

# Execute custom analysis
results = await orchestrator.run_decisioning_analysis("operational_efficiency")
```

### Result Processing

```python
def process_agent_results(results: Dict) -> Dict:
    """Process and aggregate agent results"""

    # Extract insights
    all_insights = []
    for agent_name, agent_result in results["agent_results"].items():
        all_insights.extend(agent_result["insights"])

    # Calculate summary metrics
    summary = {
        "total_agents": len(results["agent_results"]),
        "total_insights": len(all_insights),
        "execution_time": results["workflow"]["execution_time"],
        "confidence_avg": calculate_avg_confidence(results)
    }

    return summary
```

## 🔒 Security API

### Authentication

```python
class AuthenticationManager:
    """Manage authentication for sensitive operations"""

    def __init__(self, config_file: str):
        self.config = self.load_auth_config(config_file)

    def authenticate_data_source(self, source_name: str) -> bool:
        """Authenticate access to data source"""
        # Implementation depends on source type
        pass

    def validate_user_permissions(self, user_id: str, operation: str) -> bool:
        """Validate user permissions for operation"""
        # Implementation for user authorization
        pass
```

### Data Privacy

```python
class DataPrivacyManager:
    """Manage data privacy and compliance"""

    def anonymize_data(self, data: Dict) -> Dict:
        """Remove or mask sensitive information"""
        # Remove PII, financial details, etc.
        pass

    def audit_data_access(self, user_id: str, data_accessed: List[str]):
        """Log data access for compliance"""
        # Audit trail implementation
        pass
```

## 🚀 Extension API

### Custom Agents

```python
class CustomAgent:
    """Template for creating custom agents"""

    def __init__(self, config: Dict):
        self.config = config
        self.name = "CustomAgent"

    async def execute(self, input_data: Dict) -> AgentResult:
        """Execute custom agent logic"""

        # Your custom analysis logic here
        insights = ["Custom insight 1", "Custom insight 2"]
        recommendations = ["Custom recommendation 1"]

        return AgentResult(
            agent_name=self.name,
            task_id=f"custom_{int(time.time())}",
            status="success",
            data={"custom_data": "value"},
            insights=insights,
            recommendations=recommendations,
            timestamp=datetime.now(),
            execution_time=1.0,
            confidence_score=0.85
        )

# Register custom agent
orchestrator.register_custom_agent("custom", CustomAgent)
```

### Data Source Connectors

```python
class CustomDataConnector:
    """Template for custom data source connectors"""

    def __init__(self, config: Dict):
        self.config = config

    def connect(self) -> bool:
        """Establish connection to data source"""
        # Connection logic
        pass

    def extract_data(self, query: str) -> Dict:
        """Extract data from source"""
        # Data extraction logic
        pass

    def get_schema(self) -> Dict:
        """Get data source schema"""
        # Schema discovery logic
        pass
```

## 📊 Error Handling

### Exception Types

```python
class DecisioningError(Exception):
    """Base exception for decisioning system"""
    pass

class AgentExecutionError(DecisioningError):
    """Agent execution failed"""
    pass

class DataSourceError(DecisioningError):
    """Data source connection or query failed"""
    pass

class ConfigurationError(DecisioningError):
    """Invalid configuration"""
    pass
```

### Error Recovery

```python
try:
    results = await orchestrator.run_decisioning_analysis()
except AgentExecutionError as e:
    # Handle agent failure
    logger.error(f"Agent failed: {e}")
    # Retry with reduced scope

except DataSourceError as e:
    # Handle data source issues
    logger.error(f"Data source error: {e}")
    # Fall back to cached data

except Exception as e:
    # Handle unexpected errors
    logger.error(f"Unexpected error: {e}")
    # Graceful degradation
```

---

**This API reference provides comprehensive documentation for extending and integrating the Decisioning Agentic Flow system.** 🎯🚀