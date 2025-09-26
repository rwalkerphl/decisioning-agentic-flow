# Getting Started - Decisioning Agentic Flow

## 🚀 Quick Start Guide

### Prerequisites

**System Requirements:**
- Python 3.9 or higher
- 4GB RAM minimum (8GB recommended)
- Internet connection for package installation

**Optional:**
- Oracle Database access (for real data analysis)
- MCP (Model Context Protocol) setup for live data connections

### Installation

**1. Clone the Repository**
```bash
git clone https://github.com/rwalkerphl/decisioning-agentic-flow.git
cd decisioning-agentic-flow
```

**2. Install Dependencies**
```bash
pip install -r requirements.txt
```

**3. Verify Installation**
```bash
python decisioning_flow.py
```

### First Run

**1. Run Complete Analysis**
```bash
python decisioning_flow.py
```

This will:
- Initialize the orchestrator
- Deploy 5 autonomous agents
- Generate business intelligence insights
- Create interactive dashboard
- Produce executive summary

**2. View Results**

Generated files:
- `decisioning_results.json` - Complete analysis
- `executive_summary.json` - Leadership summary
- `dashboards/decisioning_dashboard.py` - Interactive dashboard

**3. Launch Dashboard**
```bash
streamlit run dashboards/decisioning_dashboard.py
```

Access at: http://localhost:8501

## 🎯 Understanding the Output

### Executive Summary Structure
```json
{
  "situation_assessment": {
    "business_health": "Assessment of current state",
    "urgency_level": "Priority level for action",
    "strategic_position": "Competitive positioning",
    "immediate_risk": "Critical risks identified"
  },
  "key_decisions_required": [
    {
      "decision": "Strategic decision name",
      "action": "Specific action required",
      "timeline": "Implementation timeframe",
      "owner": "Responsible party",
      "success_metric": "Measurable outcome"
    }
  ],
  "financial_projections": {
    "current_state": "Current financial position",
    "projected_improvement": "Expected outcomes"
  }
}
```

### Agent Results Structure
Each agent produces:
- **Insights**: Business intelligence discoveries
- **Recommendations**: Actionable advice
- **Confidence Score**: Reliability metric (0-1)
- **Execution Time**: Performance metric

## 🔧 Configuration

### Basic Configuration (`config/bi_config.json`)

```json
{
  "project": {
    "name": "your-project-name",
    "description": "Project description"
  },
  "data_sources": [
    {
      "name": "your_data_source",
      "type": "oracle_mcp",
      "enabled": true,
      "config": {
        "schema": "YOUR_SCHEMA",
        "connection_name": "your_connection"
      }
    }
  ],
  "agents": {
    "discovery_agent": {
      "enabled": true,
      "timeout": 300
    }
  }
}
```

### Adding New Data Sources

**1. Oracle Database**
```json
{
  "name": "production_db",
  "type": "oracle_mcp",
  "config": {
    "schema": "PRODUCTION",
    "connection_name": "prod-oracle"
  }
}
```

**2. API Source (Future)**
```json
{
  "name": "crm_api",
  "type": "api_connector",
  "config": {
    "base_url": "https://api.crm.com",
    "auth_type": "bearer_token"
  }
}
```

## 🤖 Agent System

### Agent Execution Flow

1. **Discovery Agent** (📊)
   - Catalogs data sources
   - Assesses data quality
   - Maps business entities

2. **Intelligence Agent** (💼)
   - Calculates business KPIs
   - Generates health scores
   - Identifies performance gaps

3. **Strategy Agent** (🔍)
   - Recognizes patterns
   - Identifies opportunities
   - Assesses strategic risks

4. **Decision Agent** (⚡)
   - Synthesizes recommendations
   - Prioritizes actions
   - Creates implementation plans

5. **Visualization Agent** (📈)
   - Generates dashboards
   - Creates executive reports
   - Builds interactive charts

### Customizing Agent Behavior

**Agent Configuration Options:**
```json
{
  "agents": {
    "discovery_agent": {
      "enabled": true,
      "timeout": 300,
      "retry_attempts": 3,
      "cache_duration": "24h"
    },
    "intelligence_agent": {
      "enabled": true,
      "parallel_queries": true,
      "metrics": [
        "financial_health",
        "operational_efficiency"
      ]
    }
  }
}
```

## 📊 Dashboard Features

### Executive Dashboard Components

**1. Critical Alerts**
- Business health warnings
- Urgent action requirements
- Risk notifications

**2. Key Metrics**
- Business health score
- Financial indicators
- Performance benchmarks

**3. Strategic Decisions**
- Prioritized action items
- Implementation timelines
- Success metrics

**4. Financial Intelligence**
- Cash flow projections
- Recovery scenarios
- Trend analysis

**5. Agent Insights**
- Tabbed view of agent findings
- Detailed recommendations
- Confidence indicators

### Dashboard Customization

**Modify Dashboard Components:**
Edit `dashboards/decisioning_dashboard.py`:

```python
# Add custom metrics
custom_metrics = {
    "metric_name": "value",
    "delta": "change",
    "delta_color": "normal"
}

st.metric(
    custom_metrics["metric_name"],
    custom_metrics["value"],
    delta=custom_metrics["delta"]
)
```

## 🔄 Automation

### Scheduled Analysis

**1. Create Cron Job**
```bash
# Run analysis daily at 6 AM
0 6 * * * cd /path/to/decisioning-agentic-flow && python decisioning_flow.py
```

**2. Auto-Push Results**
```bash
# Use the automation script
./auto_push.sh
```

### Continuous Integration

**GitHub Actions Example:**
```yaml
name: Daily Business Intelligence
on:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM
jobs:
  analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Analysis
        run: python decisioning_flow.py
      - name: Update Results
        run: git add . && git commit -m "Daily analysis update"
```

## 🚨 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Ensure Python path includes src
export PYTHONPATH="${PYTHONPATH}:./src"
```

**2. Missing Dependencies**
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

**3. Dashboard Won't Start**
```bash
# Check Streamlit installation
pip install streamlit --upgrade
streamlit --version
```

**4. Configuration Errors**
- Verify JSON syntax in `config/bi_config.json`
- Check data source connections
- Validate agent configurations

### Performance Optimization

**1. Agent Timeout Settings**
- Increase timeout for complex data sources
- Enable parallel execution where possible

**2. Dashboard Performance**
- Use caching for expensive operations
- Limit data visualization complexity

**3. Memory Management**
- Monitor agent result sizes
- Clear old result files regularly

## 📈 Next Steps

### Immediate Actions
1. **Run first analysis** to understand your baseline
2. **Review executive summary** for critical decisions
3. **Share dashboard** with stakeholders
4. **Configure data sources** for your environment

### Advanced Usage
1. **Connect real data sources** (Oracle, APIs)
2. **Customize agent algorithms** for your domain
3. **Set up automated reporting** schedules
4. **Plan CrewAI migration** for production scaling

### Integration Opportunities
1. **Business Intelligence Tools**: Connect to Tableau, PowerBI
2. **Notification Systems**: Slack, email alerts for critical findings
3. **Data Warehouses**: Integrate with Snowflake, BigQuery
4. **Decision Support**: Embed in executive workflows

---

**Ready to transform your business intelligence with autonomous agents!** 🎯🚀