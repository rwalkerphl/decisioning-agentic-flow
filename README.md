# Decisioning Agentic Flow

An intelligent decision-making system that uses autonomous agents to discover, analyze, and synthesize multi-source business data into actionable insights and strategic recommendations.

## 🎯 Project Overview

This project creates an autonomous agentic system that:
- **Discovers** and catalogs data sources automatically
- **Analyzes** business metrics and KPIs across multiple systems
- **Identifies** patterns, anomalies, and improvement opportunities
- **Generates** interactive dashboards and executive reports
- **Recommends** prioritized actions with business impact analysis

## 🏗️ Architecture

### Agent Flow Overview

```mermaid
graph TD
    A[🎯 User Request] --> B[🤖 Decisioning Orchestrator]
    B --> C[📊 Discovery Agent]
    B --> D[💼 Intelligence Agent]
    B --> E[🔍 Strategy Agent]
    B --> F[⚡ Decision Agent]
    B --> G[📈 Visualization Agent]

    C --> H[Data Landscape]
    D --> I[Business Metrics]
    E --> J[Strategic Patterns]
    F --> K[Action Framework]
    G --> L[Interactive Dashboard]

    H --> M[🎯 Executive Decisions]
    I --> M
    J --> M
    K --> M
    L --> M

    style B fill:#e1f5fe
    style M fill:#e8f5e8
    style L fill:#fff3e0
```

### Detailed Agent Workflow

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant O as 🤖 Orchestrator
    participant D as 📊 Discovery
    participant I as 💼 Intelligence
    participant S as 🔍 Strategy
    participant Dec as ⚡ Decision
    participant V as 📈 Visualization

    U->>O: Request Strategic Analysis
    O->>D: Phase 1: Data Discovery
    D->>O: Schema & Quality Report

    O->>I: Phase 2: Business Intelligence
    I->>O: KPIs & Health Metrics

    O->>S: Phase 3: Pattern Recognition
    S->>O: Strategic Insights

    O->>Dec: Phase 4: Decision Synthesis
    Dec->>O: Prioritized Actions

    O->>V: Phase 5: Visualization
    V->>O: Interactive Dashboard

    O->>U: 🎯 Strategic Decisions Ready
```

### Current Implementation (MVP)
- **Framework**: Python orchestration with autonomous agents
- **Agent Coordination**: Sequential execution with result synthesis
- **Primary Data Source**: Oracle Database via MCP connector
- **Visualization**: Streamlit interactive dashboard
- **Deployment**: Local development, containerized for production

### Migration Path to CrewAI
- **Target Framework**: CrewAI for advanced multi-agent orchestration
- **Enhanced Coordination**: Hierarchical task delegation and agent memory
- **Extensible Design**: Plugin architecture for new data sources
- **Scalable Infrastructure**: Cloud-native deployment with auto-scaling

📊 **[View Complete Architecture Diagrams](docs/architecture_diagrams.md)**

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run Analysis
```bash
python decisioning_flow.py
```

### View Dashboard
```bash
streamlit run dashboards/decisioning_dashboard.py
```

## 📁 Project Structure

```
decisioning-agentic-flow/
├── README.md                        # Project overview and documentation
├── SETUP.md                         # GitHub setup instructions
├── requirements.txt                 # Python dependencies
├── decisioning_flow.py              # Main entry point
├── setup_github_auth.sh             # GitHub authentication setup
├── auto_push.sh                     # Automated Git workflow
├── config/
│   └── bi_config.json              # Business intelligence configuration
├── src/
│   ├── __init__.py
│   └── orchestration/
│       ├── __init__.py
│       └── orchestrator.py         # Main workflow orchestrator
├── dashboards/
│   ├── decisioning_dashboard.py    # Interactive Streamlit dashboard
│   └── templates/                  # Dashboard templates
├── docs/
│   ├── architecture_diagrams.md    # Complete architecture diagrams
│   └── crewai_migration.md         # CrewAI migration framework
├── logs/                           # System logs
├── decisioning_results.json       # Latest analysis results
└── executive_summary.json         # Executive decision summary
```

## 🤖 Agent Ecosystem

### Core Agents & Capabilities

#### 📊 **Discovery Agent** - Data Intelligence
```
Input: Raw data sources (Oracle, APIs, files)
Process: Schema analysis → Quality assessment → Relationship mapping
Output: Comprehensive data landscape report
Business Value: Identifies data quality issues and optimization opportunities
```

#### 💼 **Intelligence Agent** - Business Analytics
```
Input: Data landscape + business context
Process: Financial analysis → Operational metrics → Customer intelligence
Output: Business health scores and performance insights
Business Value: Quantifies business performance and identifies critical issues
```

#### 🔍 **Strategy Agent** - Pattern Recognition
```
Input: Business intelligence + market context
Process: Pattern detection → Risk analysis → Opportunity identification
Output: Strategic insights and transformation opportunities
Business Value: Uncovers hidden patterns and strategic advantages
```

#### ⚡ **Decision Agent** - Strategic Synthesis
```
Input: All agent outputs + business objectives
Process: Priority analysis → Impact assessment → Resource planning
Output: Prioritized decision framework with timelines
Business Value: Transforms insights into executable strategic actions
```

#### 📈 **Visualization Agent** - Interactive Intelligence
```
Input: Decision framework + analysis results
Process: Chart generation → Dashboard assembly → Report creation
Output: Interactive dashboards and executive reports
Business Value: Makes complex data accessible for decision-making
```

### Agent Intelligence Levels

| Agent | Autonomy | Learning | Business Impact |
|-------|----------|----------|-----------------|
| Discovery | ⭐⭐⭐⭐ | Data Quality | Foundation |
| Intelligence | ⭐⭐⭐⭐⭐ | Business Context | Critical |
| Strategy | ⭐⭐⭐⭐⭐ | Market Patterns | Strategic |
| Decision | ⭐⭐⭐⭐⭐ | Executive Context | Transformational |
| Visualization | ⭐⭐⭐ | User Preferences | Operational |

### Extensible Design

- **Plugin Architecture**: Easy addition of new agents and data sources
- **Unified Data Model**: Consistent schema mapping across sources
- **Event-Driven**: Reactive to data changes and business events

## 📊 Business Impact

### Real-World Analysis Results (Oracle FUSION_DEMO)

#### Financial Intelligence Dashboard
```
┌─────────────────────────────────────────────────────────────┐
│                    EXECUTIVE DASHBOARD                     │
├─────────────────────────────────────────────────────────────┤
│ 🎯 Business Health Score: 65/100 (CRITICAL)               │
│ 💰 Total Revenue: $4.12M (80.06% margin) ✅                │
│ 🚨 Outstanding AR: $2.48M (98% overdue) ⚠️                 │
│ 📈 Collection Rate: 40% (vs 85% industry) ⚠️               │
├─────────────────────────────────────────────────────────────┤
│ IMMEDIATE DECISIONS REQUIRED:                              │
│ ⚡ Emergency Collections Program (48 hours)                │
│ 📋 Milestone Billing Implementation (30 days)              │
│ 👥 Customer Portfolio Optimization (90 days)               │
└─────────────────────────────────────────────────────────────┘
```

#### Strategic Decision Framework
```mermaid
graph LR
    A[💼 Current State<br/>Profitable but<br/>Cash-Constrained] --> B[⚡ Emergency Actions<br/>Collections Program<br/>$1M+ Recovery]

    B --> C[📈 Strategic Moves<br/>Billing Optimization<br/>40% Improvement]

    C --> D[🎯 Target State<br/>Healthy Cash Flow<br/>90% Collection Rate]

    style A fill:#ffcdd2
    style B fill:#fff3e0
    style C fill:#e8f5e8
    style D fill:#c8e6c9
```

### Measurable Business Value

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| Collection Rate | 40% | 90% | +125% |
| Cash Recovery | $0 | $1.8M | $1.8M |
| Overdue AR | 98% | <20% | -80% |
| Billing Velocity | 1.5x | 4.0x | +167% |
| Business Health | 65/100 | 85/100 | +31% |

### Agent-Generated Insights
- **28 Strategic Insights** discovered across all business areas
- **28 Actionable Recommendations** with priority rankings
- **$2.48M Value at Risk** identified and quantified
- **$1.8M+ Recovery Potential** with specific action plans
- **90-day transformation roadmap** with measurable milestones

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

## 🔗 Documentation

- [📊 Complete Architecture Diagrams](docs/architecture_diagrams.md)
- [🤖 CrewAI Migration Guide](docs/crewai_migration.md)
- [🚀 GitHub Setup Instructions](SETUP.md)
- [⚙️ Configuration Guide](config/bi_config.json)

## 📧 Contact

For questions or collaboration opportunities, please open an issue or reach out to the project maintainers.

---

**Built with ❤️ and AI-driven insights**