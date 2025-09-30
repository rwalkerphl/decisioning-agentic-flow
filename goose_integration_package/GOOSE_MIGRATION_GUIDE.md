# Migration Guide: Custom Orchestrator → Goose AI

## 📋 Overview

This guide shows you how to migrate your decisioning-agentic-flow system from a custom Python orchestrator to Block's Goose AI framework, eliminating the need for both your custom orchestration code AND the planned CrewAI migration.

**Migration Benefits:**
- ✅ Eliminate ~500 lines of custom orchestration code
- ✅ Native MCP support (your Oracle connector works immediately)
- ✅ Multi-LLM support with cost optimization
- ✅ CLI, Desktop App, and Python API interfaces
- ✅ Open source with active community (Block-backed)
- ✅ Cancel CrewAI migration (simpler alternative)
- ✅ Production-ready (used at Square, Cash App, etc.)

**Time to Migrate:** 2-4 hours

---

## 🚀 Phase 1: Installation & Setup (30 minutes)

### Step 1.1: Install Goose

```bash
# Method 1: Using pipx (recommended)
pipx install goose-ai

# Method 2: Using pip
pip install goose-ai

# Verify installation
goose --version
```

### Step 1.2: Initial Configuration

```bash
# Navigate to your project
cd decisioning-agentic-flow

# Run Goose configuration wizard
goose configure
```

**Configuration wizard will ask:**
1. **Provider**: Choose "Anthropic"
2. **API Key**: Enter your Anthropic API key (or set ANTHROPIC_API_KEY env var)
3. **Model**: Choose "claude-sonnet-4-5-20250929"
4. **MCP Servers**: We'll configure these manually next

### Step 1.3: Create Goose Directory Structure

```bash
# Create Goose configuration directory
mkdir -p .goose
mkdir -p goose_extensions
mkdir -p dashboards/data
mkdir -p logs

# Copy the configuration files from this migration guide
touch .goose/config.yaml
touch .goosehints
```

### Step 1.4: Configure MCP Server

Edit `.goose/config.yaml` to add your Oracle MCP server:

```yaml
# Copy the config.yaml provided in this migration
# Key section:
mcp_servers:
  oracle-fusion-demo:
    command: python
    args: ["-m", "mcp_oracle_connector"]
    env:
      DB_HOST: ${ORACLE_HOST}
      DB_PORT: ${ORACLE_PORT}
      DB_SERVICE: ${ORACLE_SERVICE}
      DB_USER: ${ORACLE_USER}
      DB_PASSWORD: ${ORACLE_PASSWORD}
```

### Step 1.5: Set Environment Variables

```bash
# Add to your .env or .bashrc
export ANTHROPIC_API_KEY="your-api-key"
export ORACLE_HOST="your-host"
export ORACLE_PORT="1521"
export ORACLE_SERVICE="FUSION_DEMO"
export ORACLE_USER="your-user"
export ORACLE_PASSWORD="your-password"
```

### Step 1.6: Test Basic Setup

```bash
# Test Goose installation
goose

# You should see:
# Welcome to Goose! 🪿
# Type 'help' for available commands

# Test MCP connection (in Goose prompt)
> list available mcp servers
> connect to oracle-fusion-demo
> list tables in database

# Exit Goose
> exit
```

---

## 🔄 Phase 2: Agent Migration (1-2 hours)

### Current Architecture (Before)
```
src/orchestration/orchestrator.py
├── DiscoveryAgent (custom Python class)
├── IntelligenceAgent (custom Python class)
├── StrategyAgent (custom Python class)
├── DecisionAgent (custom Python class)
└── VisualizationAgent (custom Python class)
```

### New Architecture (After)
```
goose_extensions/
├── discovery_agent.py (Goose extension)
├── intelligence_agent.py (Goose extension)
├── strategy_agent.py (Goose extension)
├── decision_agent.py (Goose extension)
└── visualization_agent.py (Goose extension)
```

### Option A: Full Migration (Recommended)

Convert each agent to a Goose extension. This gives you full control and integrates your existing logic.

**Template for Goose Extension:**

```python
# goose_extensions/discovery_agent.py

"""
Discovery Agent - Goose Extension
Discovers and catalogs data sources with quality assessment.
"""

from goose.toolkit import Tool, toolkit
from typing import Dict, Any, List
import json
from datetime import datetime

@toolkit
class DiscoveryAgent:
    """
    Data Discovery and Cataloging Agent
    
    This agent connects to data sources via MCP and performs:
    - Schema analysis
    - Data quality assessment
    - Relationship mapping
    """
    
    def __init__(self):
        self.results = {}
    
    @Tool(description="Discover all tables in the database")
    async def discover_tables(self, mcp_server: str = "oracle-fusion-demo") -> Dict[str, Any]:
        """
        Connect to MCP server and catalog all tables.
        
        Args:
            mcp_server: Name of the MCP server to connect to
            
        Returns:
            Dictionary with table catalog and statistics
        """
        # Your existing discovery logic here
        # Goose handles MCP connection automatically
        
        tables = [
            # Query tables via MCP
            # Example: await mcp.query("SELECT * FROM USER_TABLES")
        ]
        
        return {
            "timestamp": datetime.now().isoformat(),
            "mcp_server": mcp_server,
            "tables": tables,
            "table_count": len(tables),
            "status": "complete"
        }
    
    @Tool(description="Assess data quality for discovered tables")
    async def assess_quality(self, tables: List[str]) -> Dict[str, Any]:
        """
        Perform data quality assessment on tables.
        
        Args:
            tables: List of table names to assess
            
        Returns:
            Quality scores and issues for each table
        """
        # Your existing quality assessment logic
        
        quality_results = {
            "overall_score": 0,
            "tables": {},
            "critical_issues": [],
            "warnings": []
        }
        
        return quality_results
    
    @Tool(description="Save discovery results to file")
    async def save_results(self, results: Dict[str, Any], 
                          filepath: str = "decisioning_results.json"):
        """Save discovery results to JSON file."""
        
        # Load existing results if file exists
        try:
            with open(filepath, 'r') as f:
                all_results = json.load(f)
        except FileNotFoundError:
            all_results = {}
        
        # Add discovery results
        all_results['discovery'] = results
        all_results['discovery']['timestamp'] = datetime.now().isoformat()
        
        # Save
        with open(filepath, 'w') as f:
            json.dump(all_results, f, indent=2)
        
        return {"status": "saved", "filepath": filepath}
```

**Repeat this pattern for all 5 agents:**
1. Copy your existing agent logic
2. Wrap key functions with `@Tool` decorator
3. Add docstrings for Goose to understand capabilities
4. Handle MCP connections naturally (Goose manages this)

### Option B: Natural Language Control (Quick Start)

Skip extension creation initially and just use Goose's natural language interface with your business logic defined in `.goosehints`.

**Workflow:**

```bash
# Start Goose
goose

# Execute your decisioning flow
> I need to perform a complete strategic business analysis on the Oracle FUSION_DEMO database. Follow the decisioning workflow defined in .goosehints file:

1. Discovery Agent: Connect to oracle-fusion-demo MCP server and discover all tables, assess data quality, identify relationships. Save results to decisioning_results.json under 'discovery' key.

2. Intelligence Agent: Based on discovery results, calculate all business metrics including financial health, customer intelligence, and operational metrics. Calculate Business Health Score. Save to decisioning_results.json under 'intelligence' key.

3. Strategy Agent: Analyze the business intelligence to identify strategic patterns, risks, and opportunities. Generate minimum 10 insights. Save to decisioning_results.json under 'strategy' key.

4. Decision Agent: Synthesize all insights into prioritized strategic decisions with business impact. Create 30/60/90 day roadmap. Save executive summary to executive_summary.json.

5. Visualization Agent: Create interactive Streamlit dashboard with all results. Update dashboards/decisioning_dashboard.py.

Follow all business rules and thresholds defined in .goosehints. Complete analysis should take under 5 minutes.
```

**Goose will:**
- Read your .goosehints file for context
- Connect to your MCP server automatically
- Execute each phase sequentially
- Save results to the specified files
- Generate the dashboard

---

## 🔧 Phase 3: Workflow Automation (30 minutes)

### Step 3.1: Define Workflows in Config

Edit `.goose/config.yaml` to add predefined workflows:

```yaml
workflows:
  # Full analysis workflow
  full_analysis:
    description: "Complete end-to-end strategic decision analysis"
    timeout: 300
    steps:
      - name: discovery
        task: |
          Connect to oracle-fusion-demo and discover all tables.
          Assess data quality and identify relationships.
          Save to decisioning_results.json under 'discovery'.
      - name: intelligence
        task: |
          Calculate business intelligence metrics and health score.
          Save to decisioning_results.json under 'intelligence'.
      # ... additional steps
  
  # Quick health check
  health_check:
    description: "Quick financial health assessment"
    timeout: 120
    steps:
      - name: quick_discovery
        task: "Quick data discovery focusing on financial tables"
      - name: health_metrics
        task: "Calculate core financial metrics and health score"
```

### Step 3.2: Execute Workflows

```bash
# Run full analysis workflow
goose --workflow=full_analysis

# Or from Python
python -c "
from goose import Goose
import asyncio

async def run():
    goose = Goose(config='.goose/config.yaml')
    result = await goose.execute_workflow('full_analysis')
    print(f'Analysis complete: {result}')

asyncio.run(run())
"
```

### Step 3.3: Create Convenience Scripts

```bash
# Create run_analysis.sh
cat > run_analysis.sh << 'EOF'
#!/bin/bash
# Decisioning Analysis Runner using Goose

echo "🪿 Starting Goose Decisioning Analysis..."

# Run the full analysis workflow
goose --workflow=full_analysis --log-level=INFO

# Check if successful
if [ $? -eq 0 ]; then
    echo "✅ Analysis complete!"
    echo "📊 Results: decisioning_results.json"
    echo "📈 Dashboard: streamlit run dashboards/decisioning_dashboard.py"
else
    echo "❌ Analysis failed. Check logs/goose_decisioning.log"
    exit 1
fi
EOF

chmod +x run_analysis.sh

# Run it
./run_analysis.sh
```

---

## 📊 Phase 4: Dashboard Integration (30 minutes)

### Step 4.1: Update Dashboard to Read Goose Results

Your existing Streamlit dashboard should already read from `decisioning_results.json` and `executive_summary.json`. Verify the format matches:

```python
# dashboards/decisioning_dashboard.py (no changes needed if format matches)

import streamlit as st
import json

# Load results (same files as before)
with open('decisioning_results.json') as f:
    results = json.load(f)

with open('executive_summary.json') as f:
    summary = json.load(f)

# Render dashboard (your existing code works!)
st.title("🎯 Executive Decision Dashboard")
# ... rest of your dashboard code
```

### Step 4.2: Add Goose Execution Trigger to Dashboard

```python
# Add to your dashboard for on-demand analysis

if st.button("🔄 Refresh Analysis"):
    with st.spinner("Running Goose analysis..."):
        import subprocess
        result = subprocess.run(['goose', '--workflow=full_analysis'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            st.success("✅ Analysis complete! Reloading data...")
            st.experimental_rerun()
        else:
            st.error("❌ Analysis failed. Check logs.")
            st.code(result.stderr)
```

---

## 🧪 Phase 5: Testing & Validation (30 minutes)

### Step 5.1: Run Test Analysis

```bash
# Test the complete workflow
goose --workflow=full_analysis

# Verify outputs
ls -lh decisioning_results.json executive_summary.json
cat executive_summary.json | jq '.executive_summary'
```

### Step 5.2: Compare Results

Run your old system and Goose side-by-side to verify results match:

```bash
# Run old system
python decisioning_flow.py  # Your old orchestrator
mv decisioning_results.json decisioning_results_old.json

# Run Goose system
goose --workflow=full_analysis
mv decisioning_results.json decisioning_results_goose.json

# Compare
diff <(jq -S . decisioning_results_old.json) \
     <(jq -S . decisioning_results_goose.json)
```

### Step 5.3: Performance Benchmarking

```bash
# Time old system
time python decisioning_flow.py

# Time Goose system
time goose --workflow=full_analysis

# Expected: Goose should be comparable or faster due to optimized agent coordination
```

---

## 🗑️ Phase 6: Cleanup (15 minutes)

### Step 6.1: Archive Old Code

```bash
# Create archive directory
mkdir -p archive/pre-goose-migration

# Move old orchestration code
mv src/orchestration/ archive/pre-goose-migration/
mv decisioning_flow.py archive/pre-goose-migration/

# Keep only the configs
mv config/ .  # Keep configs if needed
```

### Step 6.2: Update Documentation

Edit `README.md` to reflect Goose usage:

```markdown
## 🚀 Quick Start

### Prerequisites
```bash
# Install Goose
pipx install goose-ai

# Install Python dependencies
pip install -r requirements.txt
```

### Run Analysis
```bash
# Interactive mode
goose

# Automated workflow
goose --workflow=full_analysis

# Or use the convenience script
./run_analysis.sh
```

### View Dashboard
```bash
streamlit run dashboards/decisioning_dashboard.py
```

## 🤖 Agent Architecture

Powered by [Goose AI](https://github.com/block/goose), an open-source
agent framework from Block. Agents are defined in `goose_extensions/`
and orchestrated via `.goose/config.yaml`.
```

### Step 6.3: Update Requirements

```bash
# Edit requirements.txt - remove orchestration dependencies
# Add Goose (if not using pipx)
cat >> requirements.txt << EOF

# Goose AI Framework
goose-ai>=1.0.0
EOF
```

---

## 🎯 Phase 7: Production Deployment

### Step 7.1: Containerize with Goose

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Install Goose
RUN pip install goose-ai

# Copy project files
WORKDIR /app
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Configure Goose
ENV GOOSE_CONFIG_PATH=/app/.goose/config.yaml

# Run analysis on container start
CMD ["goose", "--workflow=full_analysis"]
```

### Step 7.2: CI/CD Integration

```yaml
# .github/workflows/decisioning-analysis.yml
name: Decisioning Analysis

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  workflow_dispatch:  # Manual trigger

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Goose
        run: pipx install goose-ai
      
      - name: Run Analysis
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          ORACLE_HOST: ${{ secrets.ORACLE_HOST }}
          ORACLE_USER: ${{ secrets.ORACLE_USER }}
          ORACLE_PASSWORD: ${{ secrets.ORACLE_PASSWORD }}
        run: goose --workflow=full_analysis
      
      - name: Upload Results
        uses: actions/upload-artifact@v3
        with:
          name: analysis-results
          path: |
            decisioning_results.json
            executive_summary.json
```

---

## 📊 Migration Checklist

- [ ] **Phase 1: Installation & Setup**
  - [ ] Install Goose
  - [ ] Configure MCP server
  - [ ] Test basic connectivity
  - [ ] Set up environment variables

- [ ] **Phase 2: Agent Migration**
  - [ ] Choose migration strategy (Full vs Natural Language)
  - [ ] Convert agents to Goose extensions (if Full)
  - [ ] Test each agent individually
  - [ ] Verify MCP integration works

- [ ] **Phase 3: Workflow Automation**
  - [ ] Define workflows in config.yaml
  - [ ] Create convenience scripts
  - [ ] Test automated execution
  - [ ] Set up logging

- [ ] **Phase 4: Dashboard Integration**
  - [ ] Verify dashboard reads Goose results
  - [ ] Add refresh trigger (optional)
  - [ ] Test visualization rendering
  - [ ] Update dashboard documentation

- [ ] **Phase 5: Testing & Validation**
  - [ ] Run side-by-side comparison
  - [ ] Benchmark performance
  - [ ] Validate output format
  - [ ] Test error handling

- [ ] **Phase 6: Cleanup**
  - [ ] Archive old orchestration code
  - [ ] Update README and docs
  - [ ] Update requirements.txt
  - [ ] Remove unused dependencies

- [ ] **Phase 7: Production**
  - [ ] Containerize with Goose
  - [ ] Set up CI/CD
  - [ ] Configure monitoring
  - [ ] Deploy to production

---

## 🆘 Troubleshooting

### Issue: "Goose can't find MCP server"

**Solution:**
```bash
# Verify MCP server config
cat .goose/config.yaml | grep -A 10 mcp_servers

# Test MCP server separately
python -m mcp_oracle_connector --test

# Check environment variables
env | grep ORACLE
```

### Issue: "Agent execution times out"

**Solution:**
```yaml
# Increase timeout in config.yaml
workflows:
  full_analysis:
    timeout: 600  # Increase from 300 to 600 seconds
```

### Issue: "Results format doesn't match dashboard"

**Solution:**
```python
# Add format adapter in dashboard
def adapt_goose_results(goose_results):
    """Convert Goose results to expected format."""
    return {
        'discovery': goose_results.get('discovery', {}),
        'intelligence': goose_results.get('intelligence', {}),
        # ... map all fields
    }
```

---

## 🎓 Learning Resources

- **Goose Documentation**: https://block.github.io/goose/
- **MCP Documentation**: https://modelcontextprotocol.io/
- **Goose GitHub**: https://github.com/block/goose
- **Community Discord**: https://discord.gg/goose-ai

---

## 📞 Support

If you encounter issues during migration:

1. **Check logs**: `logs/goose_decisioning.log`
2. **Review Goose docs**: https://block.github.io/goose/docs/
3. **Search issues**: https://github.com/block/goose/issues
4. **Ask community**: Discord or GitHub Discussions

---

## ✅ Success Criteria

Migration is successful when:

- [x] Goose executes full analysis workflow without errors
- [x] Results match previous orchestrator output format
- [x] Dashboard renders correctly with new data
- [x] Execution time is comparable or better (<5 minutes)
- [x] MCP connections work reliably
- [x] All agents complete with expected outputs
- [x] Documentation updated to reflect Goose usage

---

**Estimated Total Migration Time**: 2-4 hours
**Complexity**: Low-Medium
**Risk**: Low (can run side-by-side during transition)
**Value**: High (eliminates custom orchestration + CrewAI migration)

🪿 Happy Goose-ing!
