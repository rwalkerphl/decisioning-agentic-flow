# Business Intelligence Agentic Flow

An intelligent, multi-source business analytics system using agentic workflows to automatically discover, analyze, and visualize business data with actionable insights.

## 🎯 Project Overview

This project creates an autonomous agentic system that:
- **Discovers** and catalogs data sources automatically
- **Analyzes** business metrics and KPIs across multiple systems
- **Identifies** patterns, anomalies, and improvement opportunities
- **Generates** interactive dashboards and executive reports
- **Recommends** prioritized actions with business impact analysis

## 🏗️ Architecture

### Current Implementation (MVP)
- **Framework**: Claude Code Tasks with Python orchestration
- **Primary Data Source**: Oracle Database via MCP connector
- **Visualization**: Streamlit dashboard
- **Deployment**: Local development, containerized for production

### Migration Path
- **Target Framework**: CrewAI for production multi-agent orchestration
- **Extensible Design**: Plugin architecture for new data sources
- **Scalable Infrastructure**: Cloud-native deployment ready

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run Analysis
```bash
python business_intel_flow.py
```

### View Dashboard
```bash
streamlit run dashboard.py
```

## 📁 Project Structure

```
bi-agentic-flow/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── config/
│   ├── bi_config.json          # Business intelligence configuration
│   └── data_sources.yaml       # Data source definitions
├── src/
│   ├── agents/                 # Individual agent implementations
│   │   ├── discovery_agent.py  # Data discovery and cataloging
│   │   ├── metrics_agent.py    # Business metrics calculation
│   │   ├── pattern_agent.py    # Pattern recognition and insights
│   │   └── viz_agent.py        # Dashboard and visualization
│   ├── orchestration/          # Workflow coordination
│   │   ├── orchestrator.py     # Main workflow orchestrator
│   │   └── task_manager.py     # Task scheduling and management
│   ├── connectors/             # Data source connectors
│   │   ├── oracle_mcp.py       # Oracle MCP connector
│   │   ├── api_connector.py    # Generic API connector
│   │   └── file_connector.py   # File-based data sources
│   └── utils/                  # Utility functions
│       ├── data_models.py      # Unified data models
│       └── helpers.py          # Common helper functions
├── dashboards/                 # Dashboard implementations
│   ├── streamlit_app.py        # Main Streamlit dashboard
│   └── templates/              # Dashboard templates
├── docs/                       # Documentation
│   ├── architecture.md         # System architecture
│   ├── agent_specs.md          # Agent specifications
│   └── crewai_migration.md     # Migration framework
├── tests/                      # Test suite
│   ├── test_agents.py          # Agent unit tests
│   └── test_integration.py     # Integration tests
├── deployment/                 # Deployment configurations
│   ├── docker/                 # Docker configurations
│   └── k8s/                    # Kubernetes manifests
└── examples/                   # Example configurations and outputs
    ├── sample_config.json      # Sample configuration
    └── sample_output.json      # Sample analysis output
```

## 🤖 Agent Ecosystem

### Core Agents

1. **Data Discovery Agent**
   - Auto-discovers available data sources
   - Catalogs schemas and relationships
   - Assesses data quality and completeness

2. **Business Metrics Agent**
   - Calculates financial and operational KPIs
   - Generates health scores and trends
   - Identifies performance gaps

3. **Pattern Recognition Agent**
   - Detects unusual patterns and anomalies
   - Finds cross-source correlations
   - Generates business insights

4. **Visualization Agent**
   - Creates interactive dashboards
   - Generates executive reports
   - Provides drill-down analytics

5. **Orchestrator Agent**
   - Coordinates multi-agent workflows
   - Manages task scheduling and dependencies
   - Aggregates results and insights

### Extensible Design

- **Plugin Architecture**: Easy addition of new agents and data sources
- **Unified Data Model**: Consistent schema mapping across sources
- **Event-Driven**: Reactive to data changes and business events

## 📊 Business Impact

### Current Analysis Results (Oracle FUSION_DEMO)

**Financial Health**
- Revenue: $4.12M
- Gross Margin: 80.06%
- Outstanding AR: $2.48M (⚠️ 98% overdue)

**Key Insights**
- Excellent profitability but critical cash flow crisis
- Collections process needs immediate attention
- Strong operational efficiency (64-day avg project duration)

**Priority Actions**
1. Implement aggressive collections strategy
2. Optimize billing processes
3. Consider receivables factoring for liquidity

## 🔧 Technology Stack

- **Core Language**: Python 3.9+
- **Agent Framework**: Claude Code Tasks (MVP) → CrewAI (Production)
- **Database Connectors**: MCP (Model Context Protocol)
- **Visualization**: Streamlit, Plotly, D3.js
- **Data Processing**: Pandas, NumPy
- **Containerization**: Docker
- **Orchestration**: Kubernetes (production)

## 📈 Roadmap

### Phase 1: MVP (Current)
- [x] Oracle database analysis
- [x] Basic agent workflow
- [x] Streamlit dashboard
- [ ] End-to-end testing

### Phase 2: Multi-Source
- [ ] Additional data source connectors
- [ ] Cross-source correlation analysis
- [ ] Enhanced pattern recognition

### Phase 3: Production
- [ ] CrewAI migration
- [ ] Cloud deployment
- [ ] Real-time processing
- [ ] Advanced ML insights

### Phase 4: Enterprise
- [ ] White-label dashboards
- [ ] API-first architecture
- [ ] Enterprise security
- [ ] Custom business rules engine

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Architecture Documentation](docs/architecture.md)
- [Agent Specifications](docs/agent_specs.md)
- [CrewAI Migration Guide](docs/crewai_migration.md)
- [API Documentation](docs/api.md)

## 📧 Contact

For questions or collaboration opportunities, please open an issue or reach out to the project maintainers.

---

**Built with ❤️ and AI-driven insights**