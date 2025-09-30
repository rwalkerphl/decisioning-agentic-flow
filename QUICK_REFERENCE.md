# Goose Quick Reference - Decisioning System

## 🚀 Essential Commands

### Installation
```bash
# Install Goose
pipx install goose-ai

# Verify installation
goose --version

# First-time setup
goose configure
```

### Basic Usage
```bash
# Interactive mode
goose

# Run specific workflow
goose --workflow=full_analysis

# Run with specific config
goose --config=/path/to/config.yaml

# Run with verbose logging
goose --log-level=DEBUG
```

### Common Tasks
```bash
# In interactive Goose prompt:
> Connect to oracle-fusion-demo
> List all tables
> Analyze financial health and create report
> Show top 3 critical actions
> Generate executive dashboard
> exit
```

---

## 📁 File Locations

```
decisioning-agentic-flow/
├── .goose/
│   └── config.yaml              # Main Goose configuration
├── .goosehints                  # Business logic & context
├── goose_extensions/            # Custom agent extensions (optional)
│   ├── discovery_agent.py
│   ├── intelligence_agent.py
│   ├── strategy_agent.py
│   ├── decision_agent.py
│   └── visualization_agent.py
├── decisioning_results.json    # Analysis results
├── executive_summary.json      # Executive decisions
└── logs/
    └── goose_decisioning.log   # Execution logs
```

---

## ⚙️ Configuration Snippets

### Basic MCP Server Setup
```yaml
# .goose/config.yaml
mcp_servers:
  oracle-fusion-demo:
    command: python
    args: ["-m", "mcp_oracle_connector"]
    env:
      DB_HOST: ${ORACLE_HOST}
      DB_USER: ${ORACLE_USER}
      DB_PASSWORD: ${ORACLE_PASSWORD}
```

### Simple Workflow
```yaml
workflows:
  full_analysis:
    description: "Complete strategic analysis"
    steps:
      - task: "Discover all data sources from oracle-fusion-demo"
      - task: "Calculate business intelligence metrics"
      - task: "Identify strategic patterns and risks"
      - task: "Generate prioritized recommendations"
      - task: "Create executive dashboard"
```

### Multi-Model Configuration
```yaml
provider:
  models:
    reasoning: claude-sonnet-4-5-20250929  # Complex tasks
    execution: claude-sonnet-4-20250514    # Standard tasks
    summarization: claude-haiku-20250305   # Quick summaries
```

---

## 🎯 Natural Language Patterns

### Analysis Requests
```
"Analyze our Oracle database and create strategic recommendations"

"Connect to oracle-fusion-demo and perform discovery analysis"

"Calculate business health score and identify critical issues"

"What are the top 3 actions we should take to improve cash flow?"

"Show me customers with highest payment risk"
```

### Data Queries
```
"List all tables in the database with row counts"

"Find customers with overdue invoices >90 days"

"Calculate collection rate and compare to 85% benchmark"

"Show revenue trends for the past 12 months"
```

### Report Generation
```
"Create an executive summary with top 3 critical actions"

"Generate a dashboard showing financial health metrics"

"Build a 30/60/90 day implementation roadmap"

"Export results to decisioning_results.json"
```

---

## 🐍 Python API Usage

### Basic Execution
```python
from goose import Goose
import asyncio

async def run_analysis():
    # Initialize Goose
    goose = Goose(config=".goose/config.yaml")
    
    # Execute workflow
    result = await goose.execute_workflow("full_analysis")
    
    print(f"Health Score: {result['intelligence']['health_score']}")
    return result

# Run
asyncio.run(run_analysis())
```

### Individual Agent Execution
```python
async def quick_health_check():
    goose = Goose()
    
    # Just run discovery and intelligence
    discovery = await goose.execute("discovery_agent", 
                                   mcp_server="oracle-fusion-demo")
    
    intelligence = await goose.execute("intelligence_agent",
                                      context=discovery)
    
    return intelligence['health_score']
```

### Custom Task
```python
async def analyze_customer(customer_id: str):
    goose = Goose()
    
    result = await goose.execute(
        task=f"Analyze payment history and risk for customer {customer_id}",
        mcp_server="oracle-fusion-demo"
    )
    
    return result
```

---

## 🔍 MCP Server Management

### Check Available Servers
```bash
# In Goose prompt
> list mcp servers
> show mcp server oracle-fusion-demo
```

### Test Connection
```bash
# In Goose prompt
> connect to oracle-fusion-demo
> test connection
> list available resources
```

### Add New MCP Server
```yaml
# Add to .goose/config.yaml
mcp_servers:
  salesforce:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-salesforce"]
    env:
      SALESFORCE_TOKEN: ${SALESFORCE_TOKEN}
```

---

## 📊 Output Formats

### Decisioning Results JSON
```json
{
  "timestamp": "2025-09-29T10:00:00Z",
  "discovery": {
    "tables": [...],
    "quality_score": 87
  },
  "intelligence": {
    "health_score": 65,
    "financial": {...},
    "customers": {...}
  },
  "strategy": {
    "insights": [...],
    "patterns": [...]
  },
  "decision": {
    "decisions": [...],
    "roadmap": {...}
  },
  "visualization": {
    "dashboard_url": "..."
  }
}
```

### Executive Summary JSON
```json
{
  "executive_summary": {
    "health_score": 65,
    "top_3_actions": [
      {
        "priority": "CRITICAL",
        "title": "Emergency Collections Program",
        "impact": "$1.8M recovery",
        "timeline": "48 hours"
      }
    ],
    "value_at_risk": "$2.48M",
    "recovery_potential": "$1.8M"
  }
}
```

---

## 🛠️ Debugging & Troubleshooting

### Check Logs
```bash
# View Goose logs
tail -f logs/goose_decisioning.log

# View with filtering
grep ERROR logs/goose_decisioning.log
```

### Verbose Mode
```bash
# Run with debug logging
goose --log-level=DEBUG --workflow=full_analysis
```

### Test Individual Components
```bash
# Test MCP connection
python -m mcp_oracle_connector --test

# Test workflow syntax
goose --validate-config .goose/config.yaml

# Test agent extension
python goose_extensions/discovery_agent.py
```

### Common Issues

**Issue: "MCP server not found"**
```bash
# Check config
cat .goose/config.yaml | grep -A 5 mcp_servers

# Verify environment variables
env | grep ORACLE

# Test manually
python -m mcp_oracle_connector
```

**Issue: "Workflow timeout"**
```yaml
# Increase timeout in config
workflows:
  full_analysis:
    timeout: 600  # Increase from 300
```

**Issue: "Authentication failed"**
```bash
# Verify API key
echo $ANTHROPIC_API_KEY

# Test authentication
goose --test-auth
```

---

## 🎨 Dashboard Integration

### Launch Dashboard
```bash
# Standard launch
streamlit run dashboards/decisioning_dashboard.py

# Custom port
streamlit run dashboards/decisioning_dashboard.py --server.port=8502

# Auto-reload
streamlit run dashboards/decisioning_dashboard.py --server.fileWatcherType=poll
```

### Trigger Analysis from Dashboard
```python
import streamlit as st
import subprocess

if st.button("🔄 Refresh Analysis"):
    with st.spinner("Running Goose analysis..."):
        result = subprocess.run(
            ['goose', '--workflow=full_analysis'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            st.success("✅ Analysis complete!")
            st.experimental_rerun()
        else:
            st.error("❌ Analysis failed")
```

---

## 📈 Performance Tips

### Speed Optimization
```yaml
# Use faster models for simple tasks
provider:
  models:
    discovery: claude-haiku-20250305      # Fast data discovery
    intelligence: claude-sonnet-4-20250514 # Balanced analysis
    decision: claude-sonnet-4-5-20250929  # Complex synthesis
```

### Caching
```yaml
system:
  performance:
    cache_enabled: true
    cache_ttl: 3600  # 1 hour
```

### Parallel Execution
```yaml
system:
  performance:
    max_concurrent_agents: 3  # Run 3 agents in parallel
```

---

## 🔐 Security Best Practices

### Environment Variables
```bash
# Never commit credentials!
# Use .env file (add to .gitignore)
echo "ANTHROPIC_API_KEY=your-key" >> .env
echo "ORACLE_PASSWORD=your-password" >> .env

# Load in shell
source .env
```

### Secrets Management
```yaml
# Use environment variable references
mcp_servers:
  oracle-fusion-demo:
    env:
      DB_PASSWORD: ${ORACLE_PASSWORD}  # From environment
      # NOT: DB_PASSWORD: "hardcoded_password"
```

---

## 📝 Quick Checklist

### Daily Usage
- [ ] `goose --workflow=full_analysis`
- [ ] Check `decisioning_results.json`
- [ ] Review `executive_summary.json`
- [ ] Launch dashboard
- [ ] Review critical actions

### Weekly Maintenance
- [ ] Check logs for errors
- [ ] Update .goosehints with new business rules
- [ ] Review and optimize workflows
- [ ] Update agent extensions if needed

### Monthly Review
- [ ] Review Goose version for updates
- [ ] Optimize model selection for cost
- [ ] Review and update documentation
- [ ] Backup configuration files

---

## 🎓 Learning Path

1. **Day 1**: Install and basic setup
2. **Day 2**: Run first analysis, understand outputs
3. **Day 3**: Customize .goosehints for your business
4. **Week 2**: Add custom agent extensions
5. **Week 3**: Optimize workflows and performance
6. **Month 2**: Explore advanced features and integrations

---

## 🔗 Quick Links

- **Goose Docs**: https://block.github.io/goose/
- **MCP Docs**: https://modelcontextprotocol.io/
- **GitHub**: https://github.com/block/goose
- **Community**: Discord, GitHub Discussions
- **Your Project**: `/decisioning-agentic-flow/`

---

## 💡 Pro Tips

1. **Use .goosehints extensively** - Put all business logic there
2. **Start with natural language** - Don't write code unless needed
3. **Test incrementally** - Run each agent separately first
4. **Version your config** - Commit .goose/config.yaml to git
5. **Monitor performance** - Check logs regularly
6. **Leverage MCP** - Add new data sources as MCP servers
7. **Keep it simple** - Configuration > Code

---

## 🆘 Emergency Commands

```bash
# Stop all Goose processes
pkill -f goose

# Clear Goose cache
rm -rf ~/.goose/cache/

# Reset configuration
goose configure --reset

# View all running workflows
ps aux | grep goose

# Check system resources
top | grep goose
```

---

**Remember:** When in doubt, check `.goosehints` and `config.yaml` first!

🪿 Keep this handy during your Goose journey!
