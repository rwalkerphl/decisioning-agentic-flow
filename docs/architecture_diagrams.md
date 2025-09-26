# Architecture Diagrams - Decisioning Agentic Flow

## 🏗️ Agent Flow Architecture

### High-Level Agent Orchestration

```mermaid
graph TD
    A[User Request] --> B[Decisioning Orchestrator]
    B --> C{Initialize Agents}

    C --> D[Phase 1: Discovery Agent]
    C --> E[Phase 2: Intelligence Agent]
    C --> F[Phase 3: Strategy Agent]
    C --> G[Phase 4: Decision Agent]
    C --> H[Phase 5: Visualization Agent]
    C --> I[Phase 6: Executive Agent]

    D --> J[Data Cataloging]
    E --> K[Business Metrics]
    F --> L[Pattern Recognition]
    G --> M[Decision Synthesis]
    H --> N[Dashboard Generation]
    I --> O[Executive Summary]

    J --> P[Results Storage]
    K --> P
    L --> P
    M --> P
    N --> P
    O --> P

    P --> Q[Interactive Dashboard]
    P --> R[Executive Report]
    P --> S[Strategic Actions]

    style B fill:#e1f5fe
    style P fill:#f3e5f5
    style Q fill:#e8f5e8
    style R fill:#fff3e0
    style S fill:#fce4ec
```

### Detailed Agent Workflow

```mermaid
sequenceDiagram
    participant User
    participant Orchestrator
    participant Discovery as Discovery Agent
    participant Intelligence as Intelligence Agent
    participant Strategy as Strategy Agent
    participant Decision as Decision Agent
    participant Visualization as Visualization Agent
    participant Executive as Executive Agent

    User->>Orchestrator: Request Analysis
    Orchestrator->>Discovery: Phase 1: Catalog Data Sources
    Discovery->>Discovery: Schema Discovery & Quality Assessment
    Discovery->>Orchestrator: Data Landscape Report

    Orchestrator->>Intelligence: Phase 2: Analyze Business Metrics
    Intelligence->>Intelligence: Calculate KPIs & Health Scores
    Intelligence->>Orchestrator: Business Intelligence Report

    Orchestrator->>Strategy: Phase 3: Recognize Patterns
    Strategy->>Strategy: Identify Strategic Opportunities
    Strategy->>Orchestrator: Strategic Insights Report

    Orchestrator->>Decision: Phase 4: Synthesize Decisions
    Decision->>Decision: Generate Prioritized Actions
    Decision->>Orchestrator: Decision Framework

    Orchestrator->>Visualization: Phase 5: Create Dashboards
    Visualization->>Visualization: Generate Interactive Charts
    Visualization->>Orchestrator: Dashboard Components

    Orchestrator->>Executive: Phase 6: Executive Summary
    Executive->>Executive: Synthesize Leadership Report
    Executive->>Orchestrator: Strategic Recommendations

    Orchestrator->>User: Complete Analysis Results
```

## 🤖 Individual Agent Architecture

### Discovery Agent - Data Intelligence

```mermaid
graph LR
    A[Data Sources] --> B[Discovery Agent]
    B --> C[Schema Analysis]
    B --> D[Quality Assessment]
    B --> E[Relationship Mapping]

    C --> F[Table Catalog]
    D --> G[Quality Scores]
    E --> H[Business Entity Map]

    F --> I[Discovery Report]
    G --> I
    H --> I

    I --> J[Data Landscape Intelligence]

    style B fill:#bbdefb
    style I fill:#e8f5e8
```

### Intelligence Agent - Business Analytics

```mermaid
graph LR
    A[Discovery Output] --> B[Intelligence Agent]
    B --> C[Financial Analysis]
    B --> D[Operational Metrics]
    B --> E[Customer Analytics]

    C --> F[Revenue Health]
    C --> G[Cash Flow Analysis]
    D --> H[Efficiency Scores]
    E --> I[Risk Assessment]

    F --> J[Business Intelligence Report]
    G --> J
    H --> J
    I --> J

    J --> K[Performance Insights]

    style B fill:#c8e6c9
    style J fill:#e8f5e8
```

### Strategy Agent - Pattern Recognition

```mermaid
graph LR
    A[Intelligence Output] --> B[Strategy Agent]
    B --> C[Pattern Detection]
    B --> D[Risk Analysis]
    B --> E[Opportunity Identification]

    C --> F[Business Model Patterns]
    D --> G[Strategic Risks]
    E --> H[Growth Opportunities]

    F --> I[Strategic Insights Report]
    G --> I
    H --> I

    I --> J[Strategic Intelligence]

    style B fill:#ffecb3
    style I fill:#e8f5e8
```

### Decision Agent - Strategic Synthesis

```mermaid
graph LR
    A[All Agent Outputs] --> B[Decision Agent]
    B --> C[Priority Analysis]
    B --> D[Impact Assessment]
    B --> E[Resource Planning]

    C --> F[Immediate Actions]
    D --> G[Strategic Initiatives]
    E --> H[Implementation Plan]

    F --> I[Decision Framework]
    G --> I
    H --> I

    I --> J[Actionable Decisions]

    style B fill:#ffcdd2
    style I fill:#e8f5e8
```

### Visualization Agent - Interactive Intelligence

```mermaid
graph LR
    A[Decision Framework] --> B[Visualization Agent]
    B --> C[Chart Generation]
    B --> D[Dashboard Assembly]
    B --> E[Report Creation]

    C --> F[Financial Charts]
    D --> G[Executive Dashboard]
    E --> H[Analysis Reports]

    F --> I[Interactive Intelligence]
    G --> I
    H --> I

    I --> J[Business Intelligence UI]

    style B fill:#e1bee7
    style I fill:#e8f5e8
```

## 📊 Data Flow Architecture

### Multi-Source Data Integration

```mermaid
graph TD
    A[Oracle Database] --> E[Data Integration Layer]
    B[CRM Systems] --> E
    C[Financial APIs] --> E
    D[External Data] --> E

    E --> F[Unified Data Model]
    F --> G[Discovery Agent]
    F --> H[Intelligence Agent]
    F --> I[Strategy Agent]

    G --> J[Agent Results Store]
    H --> J
    I --> J

    J --> K[Decision Agent]
    K --> L[Executive Summary]
    K --> M[Interactive Dashboard]
    K --> N[Strategic Actions]

    style E fill:#e3f2fd
    style F fill:#f1f8e9
    style J fill:#fce4ec
    style L fill:#fff3e0
    style M fill:#e8f5e8
    style N fill:#f3e5f5
```

## 🔄 CrewAI Migration Architecture

### Current MVP vs Target CrewAI

```mermaid
graph TD
    subgraph "Current MVP Architecture"
        A1[Python Orchestrator] --> B1[Sequential Agents]
        B1 --> C1[Mock Data Processing]
        C1 --> D1[Streamlit Dashboard]
    end

    subgraph "Target CrewAI Architecture"
        A2[CrewAI Crew Manager] --> B2[Intelligent Agent Coordination]
        B2 --> C2[Real-time Data Processing]
        C2 --> D2[Advanced Visualizations]
        B2 --> E2[Memory & Learning]
        B2 --> F2[Dynamic Task Creation]
    end

    A1 -.->|Migration Path| A2
    B1 -.->|Enhanced Coordination| B2
    C1 -.->|Live Data Integration| C2
    D1 -.->|AI-Enhanced UI| D2

    style A1 fill:#ffeb3b
    style A2 fill:#4caf50
    style B1 fill:#ff9800
    style B2 fill:#2196f3
```

## 🎯 Business Intelligence Flow

### From Data to Decisions

```mermaid
graph LR
    A[Raw Business Data] --> B[Discovery & Cataloging]
    B --> C[Intelligence Analysis]
    C --> D[Strategic Pattern Recognition]
    D --> E[Decision Synthesis]
    E --> F[Executive Actions]

    G[Performance Monitoring] --> B
    F --> H[Implementation]
    H --> I[Results Measurement]
    I --> G

    J[Continuous Learning] --> C
    I --> J

    style A fill:#e3f2fd
    style F fill:#e8f5e8
    style H fill:#fff3e0
    style I fill:#f3e5f5
    style J fill:#fce4ec
```

## 🚀 Deployment Architecture

### Production Scaling

```mermaid
graph TD
    A[Load Balancer] --> B[API Gateway]
    B --> C[Agent Orchestrator Cluster]

    C --> D[Discovery Agent Pool]
    C --> E[Intelligence Agent Pool]
    C --> F[Strategy Agent Pool]
    C --> G[Decision Agent Pool]

    H[Data Lake] --> D
    H --> E
    H --> F

    I[Vector Database] --> E
    I --> F
    I --> G

    J[Redis Cache] --> C
    K[PostgreSQL] --> C

    D --> L[Results Store]
    E --> L
    F --> L
    G --> L

    L --> M[Dashboard Service]
    L --> N[API Endpoints]
    L --> O[Report Generator]

    style C fill:#e1f5fe
    style H fill:#f1f8e9
    style I fill:#fce4ec
    style L fill:#e8f5e8
```

---

These diagrams illustrate the complete architecture from individual agent logic through enterprise deployment scenarios, showing how the Decisioning Agentic Flow scales from MVP to production-ready business intelligence platform.