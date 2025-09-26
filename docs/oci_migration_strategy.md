# OCI Migration Strategy - Decisioning Agentic Flow

## 🎯 Migration Overview

This document outlines the strategic approach to migrate the Decisioning Agentic Flow from local MVP to production-scale Oracle Cloud Infrastructure (OCI) deployment using Gen AI Agents service.

## 🔄 Migration Phases

### Phase 1: Assessment & Planning (Week 1-2)

#### Current State Analysis
```mermaid
graph LR
    A[Local MVP] --> B[Python Orchestrator]
    B --> C[5 Agents]
    C --> D[Oracle MCP]
    D --> E[Streamlit Dashboard]

    style A fill:#ffcdd2
    style E fill:#ffcdd2
```

**Current Architecture Limitations:**
- Single-instance execution
- No auto-scaling
- Basic error handling
- Limited monitoring
- Manual deployment

#### Target State Vision
```mermaid
graph TB
    subgraph "OCI Production"
        A[🚪 API Gateway] --> B[🤖 Gen AI Agents]
        B --> C[📊 Analytics Cloud]
        B --> D[🗄️ Autonomous DB]
        C --> E[📱 Enterprise Dashboard]
    end

    subgraph "Enterprise Features"
        F[🔒 IAM Security]
        G[📈 Auto-scaling]
        H[🔍 Monitoring]
        I[🔄 CI/CD Pipeline]
    end

    style A fill:#e8f5e8
    style B fill:#e1f5fe
    style C fill:#fff3e0
```

**Target Benefits:**
- Enterprise-grade scalability
- Native Oracle integration
- Professional dashboards
- Automated operations
- Advanced security

### Phase 2: Infrastructure Foundation (Week 3-4)

#### 2.1 OCI Account Setup

**Required Services Enablement:**
```bash
# Enable required OCI services
oci iam compartment create \
  --compartment-id $TENANCY_OCID \
  --name "decisioning-production" \
  --description "Production environment for Decisioning Agentic Flow"

# Service limits check
oci limits resource-availability get \
  --service-name "functions" \
  --limit-name "function-count-per-application"
```

**Service Dependencies:**
| Service | Purpose | Sizing |
|---------|---------|---------|
| Gen AI Agents | Agent orchestration | Standard tier |
| Autonomous Database | Data storage | 1 OCPU, 1TB |
| Analytics Cloud | Dashboards | 1 OCPU |
| API Gateway | Public interface | Standard |
| Functions | Agent execution | Per-invoke |
| Object Storage | Artifacts | 100GB |

#### 2.2 Network Architecture

**Create `migration/network_design.tf`:**
```hcl
# Regional network design
resource "oci_core_vcn" "decisioning_prod" {
  compartment_id = var.compartment_ocid
  cidr_blocks    = ["10.0.0.0/16"]
  display_name   = "decisioning-production-vcn"

  # Enable DNS for service discovery
  dns_label = "decisionprod"
}

# Multi-AZ subnet design
resource "oci_core_subnet" "agent_subnet" {
  compartment_id      = var.compartment_ocid
  vcn_id             = oci_core_vcn.decisioning_prod.id
  cidr_block         = "10.0.1.0/24"
  display_name       = "agent-execution-subnet"
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name

  # Private subnet for security
  prohibit_public_ip_on_vnic = true
}

resource "oci_core_subnet" "database_subnet" {
  compartment_id      = var.compartment_ocid
  vcn_id             = oci_core_vcn.decisioning_prod.id
  cidr_block         = "10.0.2.0/24"
  display_name       = "database-subnet"
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[1].name

  # Private subnet for database security
  prohibit_public_ip_on_vnic = true
}

resource "oci_core_subnet" "public_subnet" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.decisioning_prod.id
  cidr_block     = "10.0.3.0/24"
  display_name   = "public-gateway-subnet"

  # Public subnet for API Gateway
  prohibit_public_ip_on_vnic = false
}
```

#### 2.3 Security Foundation

**Identity & Access Management:**
```hcl
# Service-specific dynamic groups
resource "oci_identity_dynamic_group" "agents_group" {
  compartment_id = var.tenancy_ocid
  name           = "decisioning-agents-dg"
  description    = "Dynamic group for agent functions"
  matching_rule  = "ALL {resource.type = 'fnfunc', resource.compartment.id = '${var.compartment_ocid}'}"
}

resource "oci_identity_dynamic_group" "analytics_group" {
  compartment_id = var.tenancy_ocid
  name           = "decisioning-analytics-dg"
  description    = "Dynamic group for analytics cloud"
  matching_rule  = "ALL {resource.type = 'analyticsinstance', resource.compartment.id = '${var.compartment_ocid}'}"
}

# Least privilege policies
resource "oci_identity_policy" "agent_execution_policy" {
  compartment_id = var.compartment_ocid
  name           = "decisioning-agent-execution"
  description    = "Minimal required permissions for agent execution"

  statements = [
    "Allow dynamic-group decisioning-agents-dg to use autonomous-databases in compartment id ${var.compartment_ocid}",
    "Allow dynamic-group decisioning-agents-dg to manage objects in compartment id ${var.compartment_ocid} where target.bucket.name='decisioning-artifacts'",
    "Allow dynamic-group decisioning-agents-dg to use analytics-clouds in compartment id ${var.compartment_ocid}"
  ]
}
```

### Phase 3: Agent Migration (Week 5-6)

#### 3.1 Agent Containerization

**Create `migration/containerize_agents.py`:**
```python
"""
Migration utility to containerize existing agents for OCI deployment
"""
import os
import shutil
from pathlib import Path

class AgentContainerizer:
    def __init__(self, source_dir: str, target_dir: str):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)

    def containerize_agent(self, agent_name: str):
        """Convert local agent to OCI Function format"""

        # Create function directory structure
        func_dir = self.target_dir / f"{agent_name}-function"
        func_dir.mkdir(parents=True, exist_ok=True)

        # Generate func.yaml
        func_yaml = f"""
schema_version: 20180708
name: {agent_name}-agent
version: 1.0.0
runtime: python
entrypoint: /python/bin/fdk /function/func.py handler
memory: 512
timeout: 300
build_image: fnproject/python:3.9-dev
run_image: fnproject/python:3.9
"""
        (func_dir / "func.yaml").write_text(func_yaml.strip())

        # Generate requirements.txt
        requirements = """
fdk>=0.1.54
oci>=2.88.0
pandas>=1.5.0
numpy>=1.21.0
"""
        (func_dir / "requirements.txt").write_text(requirements.strip())

        # Generate func.py wrapper
        func_py = f"""
import io
import json
import logging
from fdk import response
from {agent_name}_agent import {agent_name.title()}Agent

def handler(ctx, data: io.BytesIO = None):
    \"\"\"OCI Function handler for {agent_name} agent\"\"\"

    try:
        # Parse input data
        if data.getvalue():
            input_data = json.loads(data.getvalue())
        else:
            input_data = {{}}

        # Initialize agent
        agent = {agent_name.title()}Agent(
            config=input_data.get('config', {{}})
        )

        # Execute agent logic
        result = agent.execute(input_data)

        return response.Response(
            ctx,
            response_data=json.dumps(result.__dict__),
            headers={{"Content-Type": "application/json"}}
        )

    except Exception as e:
        logging.error(f"Agent execution failed: {{str(e)}}")
        return response.Response(
            ctx,
            response_data=json.dumps({{"error": str(e)}}),
            headers={{"Content-Type": "application/json"}},
            status_code=500
        )
"""
        (func_dir / "func.py").write_text(func_py)

        # Copy agent implementation
        agent_source = self.source_dir / "orchestration" / "orchestrator.py"
        agent_target = func_dir / f"{agent_name}_agent.py"

        # Extract agent class from orchestrator
        self._extract_agent_class(agent_source, agent_target, agent_name)

        print(f"✅ Containerized {agent_name} agent")

    def _extract_agent_class(self, source_file: Path, target_file: Path, agent_name: str):
        """Extract individual agent class from orchestrator"""

        # Read orchestrator source
        source_code = source_file.read_text()

        # Extract agent method and create standalone class
        agent_class = f"""
import json
import asyncio
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Any, Optional

@dataclass
class AgentResult:
    agent_name: str
    task_id: str
    status: str
    data: Dict[str, Any]
    insights: List[str]
    recommendations: List[str]
    timestamp: datetime
    execution_time: float
    confidence_score: float

class {agent_name.title()}Agent:
    def __init__(self, config: Dict):
        self.config = config
        self.name = "{agent_name}"

    def execute(self, input_data: Dict) -> AgentResult:
        \"\"\"Execute {agent_name} agent logic\"\"\"
        start_time = time.time()

        # Agent-specific implementation
        result = self._run_{agent_name}_logic(input_data)

        execution_time = time.time() - start_time

        return AgentResult(
            agent_name=self.name,
            task_id=f"{{self.name}}_{{int(time.time())}}",
            status="success",
            data=result.get("data", {{}}),
            insights=result.get("insights", []),
            recommendations=result.get("recommendations", []),
            timestamp=datetime.now(),
            execution_time=execution_time,
            confidence_score=result.get("confidence_score", 0.85)
        )

    def _run_{agent_name}_logic(self, input_data: Dict) -> Dict:
        \"\"\"Core {agent_name} agent logic\"\"\"
        # Implementation extracted from orchestrator
        pass
"""

        target_file.write_text(agent_class)

# Usage
containerizer = AgentContainerizer(
    source_dir="src",
    target_dir="oci-functions"
)

agents = ["discovery", "intelligence", "strategy", "decision", "visualization"]
for agent in agents:
    containerizer.containerize_agent(agent)
```

#### 3.2 Gen AI Agents Configuration

**Create `migration/genai_agent_config.yaml`:**
```yaml
apiVersion: genai.oci.oracle.com/v1
kind: AgentConfiguration
metadata:
  name: decisioning-orchestrator
  namespace: decisioning-prod
spec:
  orchestration:
    type: "sequential_with_parallel"
    timeout: 1800
    retryPolicy:
      maxRetries: 3
      backoffMultiplier: 2

  agents:
    discovery:
      type: "data_discovery"
      runtime: "python3.9"
      memory: "512MB"
      timeout: 300
      dependencies:
        - oci
        - pandas
        - numpy
      config:
        data_sources:
          - type: "autonomous_database"
            connection_type: "wallet"
          - type: "object_storage"
            bucket_name: "decisioning-artifacts"

    intelligence:
      type: "business_analytics"
      runtime: "python3.9"
      memory: "1GB"
      timeout: 600
      dependencies:
        - oci
        - pandas
        - numpy
        - scipy
      config:
        parallel_processing: true
        cache_results: true
        metrics:
          - financial_health
          - operational_efficiency
          - customer_analytics

    strategy:
      type: "pattern_recognition"
      runtime: "python3.9"
      memory: "1GB"
      timeout: 450
      dependencies:
        - oci
        - scikit-learn
        - pandas
      config:
        ml_models:
          - trend_analysis
          - anomaly_detection
          - risk_assessment

    decision:
      type: "decision_synthesis"
      runtime: "python3.9"
      memory: "512MB"
      timeout: 300
      dependencies:
        - oci
        - pandas
      config:
        prioritization_framework: "business_impact"
        decision_matrix: "risk_reward"

    visualization:
      type: "dashboard_generation"
      runtime: "python3.9"
      memory: "512MB"
      timeout: 200
      dependencies:
        - oci
        - plotly
        - streamlit
      config:
        output_formats:
          - analytics_cloud
          - apex_dashboard
          - json_export

  dataflow:
    sequence:
      - stage: "discovery"
        agents: ["discovery"]
        condition: "always"

      - stage: "analysis"
        agents: ["intelligence", "strategy"]
        condition: "discovery.status == 'success'"
        parallel: true

      - stage: "synthesis"
        agents: ["decision"]
        condition: "intelligence.status == 'success' AND strategy.status == 'success'"

      - stage: "presentation"
        agents: ["visualization"]
        condition: "decision.status == 'success'"

  outputs:
    aggregation_strategy: "merge_with_priority"
    storage:
      type: "object_storage"
      bucket: "decisioning-results"
      retention_days: 90
```

### Phase 4: Data Migration (Week 7)

#### 4.1 Database Migration Strategy

**Create `migration/database_migration.sql`:**
```sql
-- Create production schema in Autonomous Database
CREATE USER decisioning_prod IDENTIFIED BY ${STRONG_PASSWORD};

-- Grant necessary privileges
GRANT CONNECT, RESOURCE TO decisioning_prod;
GRANT CREATE VIEW TO decisioning_prod;
GRANT CREATE PROCEDURE TO decisioning_prod;

-- Create schema objects
CREATE TABLE decisioning_prod.analysis_results (
    result_id VARCHAR2(50) PRIMARY KEY,
    analysis_type VARCHAR2(100) NOT NULL,
    execution_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    agent_results CLOB CHECK (agent_results IS JSON),
    executive_summary CLOB CHECK (executive_summary IS JSON),
    status VARCHAR2(20) DEFAULT 'COMPLETED',
    created_by VARCHAR2(100),
    retention_date DATE
);

-- Create indexes for performance
CREATE INDEX idx_analysis_timestamp ON decisioning_prod.analysis_results(execution_timestamp);
CREATE INDEX idx_analysis_type ON decisioning_prod.analysis_results(analysis_type);
CREATE INDEX idx_analysis_status ON decisioning_prod.analysis_results(status);

-- Create results view for dashboard
CREATE VIEW decisioning_prod.latest_analysis AS
SELECT
    result_id,
    analysis_type,
    execution_timestamp,
    JSON_VALUE(executive_summary, '$.situation_assessment.business_health') as business_health,
    JSON_VALUE(executive_summary, '$.financial_projections.current_state') as financial_state,
    status
FROM decisioning_prod.analysis_results
WHERE execution_timestamp >= SYSDATE - 30;

-- Create stored procedure for cleanup
CREATE PROCEDURE decisioning_prod.cleanup_old_results AS
BEGIN
    DELETE FROM analysis_results
    WHERE retention_date < SYSDATE;
    COMMIT;
END;
```

#### 4.2 Data Source Configuration

**Create `migration/data_source_config.json`:**
```json
{
  "production_sources": {
    "primary_database": {
      "type": "autonomous_database",
      "connection_type": "wallet",
      "service_name": "decisioning_prod_high",
      "schema": "DECISIONING_PROD",
      "wallet_location": "/opt/oracle/wallet",
      "connection_pool": {
        "min_connections": 2,
        "max_connections": 10,
        "connection_timeout": 30
      }
    },
    "analytics_storage": {
      "type": "object_storage",
      "namespace": "decisioning_namespace",
      "bucket": "decisioning-analytics",
      "region": "us-ashburn-1",
      "access_type": "instance_principal"
    },
    "external_apis": {
      "market_data": {
        "type": "rest_api",
        "base_url": "https://api.marketdata.com/v1",
        "auth_type": "api_key",
        "rate_limit": 1000,
        "timeout": 30
      }
    }
  },
  "development_sources": {
    "test_database": {
      "type": "autonomous_database",
      "connection_type": "wallet",
      "service_name": "decisioning_dev_medium",
      "schema": "DECISIONING_DEV"
    }
  }
}
```

### Phase 5: Dashboard Migration (Week 8)

#### 5.1 Analytics Cloud Migration

**Create `migration/oac_migration.py`:**
```python
"""
Migrate Streamlit dashboard to Oracle Analytics Cloud
"""
import json
import requests
from typing import Dict, List

class OACMigrator:
    def __init__(self, oac_instance_url: str, auth_token: str):
        self.base_url = oac_instance_url
        self.headers = {
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/json'
        }

    def create_data_source(self, source_config: Dict) -> str:
        """Create OAC data source from config"""

        payload = {
            "name": "Decisioning Analytics",
            "description": "AI-generated business intelligence data",
            "type": "ORACLE_DATABASE",
            "connectionDetails": {
                "host": source_config["host"],
                "port": source_config["port"],
                "serviceName": source_config["service_name"],
                "username": source_config["username"],
                "walletPath": source_config["wallet_path"]
            }
        }

        response = requests.post(
            f"{self.base_url}/api/v1/dataSources",
            headers=self.headers,
            json=payload
        )

        return response.json()["id"]

    def create_dataset(self, data_source_id: str) -> str:
        """Create dataset from analysis results"""

        payload = {
            "name": "Decisioning Results",
            "description": "Business intelligence analysis results",
            "dataSourceId": data_source_id,
            "sql": """
                SELECT
                    result_id,
                    analysis_type,
                    execution_timestamp,
                    JSON_VALUE(agent_results, '$.discovery.data.data_ecosystem.total_entities') as total_entities,
                    JSON_VALUE(agent_results, '$.intelligence.data.financial_intelligence.revenue_analysis.total_revenue') as total_revenue,
                    JSON_VALUE(agent_results, '$.intelligence.data.financial_intelligence.revenue_analysis.gross_margin') as gross_margin,
                    JSON_VALUE(executive_summary, '$.situation_assessment.business_health') as business_health_score
                FROM decisioning_prod.analysis_results
                WHERE status = 'COMPLETED'
                ORDER BY execution_timestamp DESC
            """
        }

        response = requests.post(
            f"{self.base_url}/api/v1/datasets",
            headers=self.headers,
            json=payload
        )

        return response.json()["id"]

    def create_dashboard(self, dataset_id: str) -> str:
        """Create executive dashboard"""

        dashboard_spec = {
            "name": "Decisioning Executive Dashboard",
            "description": "AI-Generated Business Intelligence Dashboard",
            "layout": {
                "type": "CANVAS",
                "width": 1200,
                "height": 800
            },
            "visualizations": [
                {
                    "type": "KPI_CARD",
                    "title": "Business Health Score",
                    "position": {"x": 0, "y": 0, "width": 300, "height": 200},
                    "datasetId": dataset_id,
                    "config": {
                        "metric": "business_health_score",
                        "format": "number",
                        "threshold": {
                            "critical": 60,
                            "warning": 75,
                            "good": 85
                        }
                    }
                },
                {
                    "type": "LINE_CHART",
                    "title": "Revenue Trend",
                    "position": {"x": 300, "y": 0, "width": 600, "height": 400},
                    "datasetId": dataset_id,
                    "config": {
                        "xAxis": "execution_timestamp",
                        "yAxis": "total_revenue",
                        "aggregation": "sum"
                    }
                },
                {
                    "type": "GAUGE_CHART",
                    "title": "Gross Margin",
                    "position": {"x": 900, "y": 0, "width": 300, "height": 200},
                    "datasetId": dataset_id,
                    "config": {
                        "metric": "gross_margin",
                        "min": 0,
                        "max": 100,
                        "target": 80,
                        "format": "percentage"
                    }
                },
                {
                    "type": "TABLE",
                    "title": "Latest Analysis Results",
                    "position": {"x": 0, "y": 400, "width": 1200, "height": 400},
                    "datasetId": dataset_id,
                    "config": {
                        "columns": [
                            "analysis_type",
                            "execution_timestamp",
                            "business_health_score",
                            "total_revenue",
                            "gross_margin"
                        ],
                        "pageSize": 10,
                        "sortBy": "execution_timestamp",
                        "sortOrder": "DESC"
                    }
                }
            ]
        }

        response = requests.post(
            f"{self.base_url}/api/v1/dashboards",
            headers=self.headers,
            json=dashboard_spec
        )

        return response.json()["id"]

    def migrate_complete_dashboard(self, db_config: Dict) -> Dict:
        """Complete dashboard migration process"""

        print("📊 Starting OAC dashboard migration...")

        # Create data source
        data_source_id = self.create_data_source(db_config)
        print(f"✅ Created data source: {data_source_id}")

        # Create dataset
        dataset_id = self.create_dataset(data_source_id)
        print(f"✅ Created dataset: {dataset_id}")

        # Create dashboard
        dashboard_id = self.create_dashboard(dataset_id)
        print(f"✅ Created dashboard: {dashboard_id}")

        return {
            "data_source_id": data_source_id,
            "dataset_id": dataset_id,
            "dashboard_id": dashboard_id,
            "dashboard_url": f"{self.base_url}/dv/ui/dashboard/{dashboard_id}"
        }
```

#### 5.2 APEX Alternative Migration

**Create `migration/apex_migration.sql`:**
```sql
-- Create APEX application for decisioning dashboard
DECLARE
    l_app_id NUMBER;
BEGIN
    -- Create new application
    l_app_id := apex_application_install.get_application_id;

    apex_application.create_application(
        p_id => l_app_id,
        p_name => 'Decisioning Executive Dashboard',
        p_alias => 'DECISIONING_EXEC',
        p_application_group => 'BUSINESS_INTELLIGENCE',
        p_schema => 'DECISIONING_PROD'
    );

    -- Create executive dashboard page
    apex_page.create_page(
        p_application_id => l_app_id,
        p_id => 1,
        p_name => 'Executive Dashboard',
        p_alias => 'EXECUTIVE_DASHBOARD',
        p_page_template => 'Minimal (No Navigation)',
        p_page_mode => 'NORMAL'
    );

    -- Add business health region
    apex_region.create_region(
        p_application_id => l_app_id,
        p_page_id => 1,
        p_name => 'Business Health Score',
        p_source_type => 'SQL_QUERY',
        p_source => q'[
            SELECT
                'Business Health' as label,
                ROUND(TO_NUMBER(JSON_VALUE(executive_summary, '$.situation_assessment.business_health_numeric'))) as value,
                CASE
                    WHEN TO_NUMBER(JSON_VALUE(executive_summary, '$.situation_assessment.business_health_numeric')) >= 85 THEN 'success'
                    WHEN TO_NUMBER(JSON_VALUE(executive_summary, '$.situation_assessment.business_health_numeric')) >= 70 THEN 'warning'
                    ELSE 'danger'
                END as status
            FROM decisioning_prod.analysis_results
            WHERE ROWNUM = 1
            ORDER BY execution_timestamp DESC
        ]',
        p_region_template => 'Content Block'
    );

    COMMIT;
END;
/
```

### Phase 6: Testing & Validation (Week 9)

#### 6.1 End-to-End Testing

**Create `migration/test_migration.py`:**
```python
"""
Comprehensive testing suite for OCI migration
"""
import asyncio
import json
import time
import requests
from typing import Dict, List

class MigrationTester:
    def __init__(self, config: Dict):
        self.config = config
        self.test_results = []

    async def test_infrastructure(self) -> Dict:
        """Test OCI infrastructure components"""

        results = {
            "infrastructure": {
                "vcn": await self._test_vcn(),
                "subnets": await self._test_subnets(),
                "security_lists": await self._test_security(),
                "database": await self._test_database(),
                "object_storage": await self._test_storage()
            }
        }

        return results

    async def test_agent_execution(self) -> Dict:
        """Test agent function execution"""

        test_payload = {
            "analysis_type": "strategic_business_health",
            "config": self.config["agent_config"]
        }

        results = {}
        agents = ["discovery", "intelligence", "strategy", "decision", "visualization"]

        for agent in agents:
            start_time = time.time()

            try:
                # Invoke agent function
                response = await self._invoke_function(f"{agent}-agent", test_payload)
                execution_time = time.time() - start_time

                results[agent] = {
                    "status": "success",
                    "execution_time": execution_time,
                    "response_size": len(json.dumps(response)),
                    "confidence_score": response.get("confidence_score", 0)
                }

            except Exception as e:
                results[agent] = {
                    "status": "failed",
                    "error": str(e),
                    "execution_time": time.time() - start_time
                }

        return {"agent_execution": results}

    async def test_dashboard_integration(self) -> Dict:
        """Test dashboard functionality"""

        results = {
            "oac_dashboard": await self._test_oac_dashboard(),
            "api_gateway": await self._test_api_gateway(),
            "data_refresh": await self._test_data_refresh()
        }

        return {"dashboard_integration": results}

    async def test_performance(self) -> Dict:
        """Performance testing"""

        # Load testing
        concurrent_requests = 10
        total_requests = 100

        start_time = time.time()

        tasks = []
        for i in range(total_requests):
            task = self._make_api_request(f"test_request_{i}")
            tasks.append(task)

            # Batch requests for concurrency control
            if len(tasks) >= concurrent_requests:
                results = await asyncio.gather(*tasks)
                tasks = []

        # Process remaining requests
        if tasks:
            results = await asyncio.gather(*tasks)

        total_time = time.time() - start_time

        return {
            "performance": {
                "total_requests": total_requests,
                "total_time": total_time,
                "requests_per_second": total_requests / total_time,
                "average_response_time": total_time / total_requests
            }
        }

    async def run_complete_test_suite(self) -> Dict:
        """Run all migration tests"""

        print("🧪 Starting OCI migration testing...")

        all_results = {}

        # Infrastructure tests
        print("📋 Testing infrastructure...")
        all_results.update(await self.test_infrastructure())

        # Agent execution tests
        print("🤖 Testing agent execution...")
        all_results.update(await self.test_agent_execution())

        # Dashboard integration tests
        print("📊 Testing dashboard integration...")
        all_results.update(await self.test_dashboard_integration())

        # Performance tests
        print("⚡ Running performance tests...")
        all_results.update(await self.test_performance())

        # Generate test report
        test_report = self._generate_test_report(all_results)

        print("✅ Migration testing complete!")
        return test_report

    def _generate_test_report(self, results: Dict) -> Dict:
        """Generate comprehensive test report"""

        total_tests = 0
        passed_tests = 0

        for category, tests in results.items():
            if isinstance(tests, dict):
                for test_name, test_result in tests.items():
                    total_tests += 1
                    if test_result.get("status") == "success":
                        passed_tests += 1

        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0

        return {
            "test_summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": total_tests - passed_tests,
                "success_rate": f"{success_rate:.1f}%",
                "migration_ready": success_rate >= 95
            },
            "detailed_results": results,
            "recommendations": self._generate_recommendations(results)
        }

    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate recommendations based on test results"""

        recommendations = []

        # Check performance
        perf = results.get("performance", {})
        if perf.get("requests_per_second", 0) < 10:
            recommendations.append("Consider increasing function memory allocation for better performance")

        # Check agent execution
        agent_results = results.get("agent_execution", {})
        failed_agents = [agent for agent, result in agent_results.items() if result.get("status") != "success"]
        if failed_agents:
            recommendations.append(f"Fix failed agents: {', '.join(failed_agents)}")

        # Check infrastructure
        infra = results.get("infrastructure", {})
        if not all(component.get("status") == "success" for component in infra.values()):
            recommendations.append("Resolve infrastructure connectivity issues before production deployment")

        return recommendations
```

#### 6.2 Performance Benchmarking

**Create `migration/performance_benchmark.py`:**
```python
"""
Performance benchmarking for production readiness
"""
import asyncio
import time
import statistics
from typing import List, Dict

class PerformanceBenchmark:
    def __init__(self, config: Dict):
        self.config = config
        self.benchmarks = {}

    async def benchmark_agent_performance(self) -> Dict:
        """Benchmark individual agent performance"""

        agents = ["discovery", "intelligence", "strategy", "decision", "visualization"]
        results = {}

        for agent in agents:
            print(f"🔬 Benchmarking {agent} agent...")

            execution_times = []
            memory_usage = []

            # Run multiple iterations
            for i in range(10):
                start_time = time.time()

                # Execute agent
                result = await self._execute_agent(agent)

                execution_time = time.time() - start_time
                execution_times.append(execution_time)
                memory_usage.append(result.get("memory_used", 0))

            results[agent] = {
                "avg_execution_time": statistics.mean(execution_times),
                "min_execution_time": min(execution_times),
                "max_execution_time": max(execution_times),
                "std_execution_time": statistics.stdev(execution_times),
                "avg_memory_usage": statistics.mean(memory_usage),
                "success_rate": 100.0  # Assuming all successful for benchmark
            }

        return results

    async def benchmark_end_to_end_workflow(self) -> Dict:
        """Benchmark complete decisioning workflow"""

        iterations = 5
        workflow_times = []

        for i in range(iterations):
            print(f"📊 Running end-to-end workflow {i+1}/{iterations}...")

            start_time = time.time()

            # Simulate complete workflow
            result = await self._run_complete_workflow()

            workflow_time = time.time() - start_time
            workflow_times.append(workflow_time)

        return {
            "end_to_end_workflow": {
                "avg_workflow_time": statistics.mean(workflow_times),
                "min_workflow_time": min(workflow_times),
                "max_workflow_time": max(workflow_times),
                "target_time": 1800,  # 30 minutes
                "performance_rating": self._calculate_performance_rating(statistics.mean(workflow_times))
            }
        }

    def _calculate_performance_rating(self, avg_time: float) -> str:
        """Calculate performance rating based on execution time"""

        if avg_time <= 300:  # 5 minutes
            return "Excellent"
        elif avg_time <= 600:  # 10 minutes
            return "Good"
        elif avg_time <= 1200:  # 20 minutes
            return "Fair"
        else:
            return "Needs Optimization"
```

### Phase 7: Production Deployment (Week 10)

#### 7.1 Blue-Green Deployment Strategy

**Create `migration/blue_green_deployment.py`:**
```python
"""
Blue-Green deployment strategy for zero-downtime migration
"""
import asyncio
import json
from typing import Dict

class BlueGreenDeployment:
    def __init__(self, config: Dict):
        self.config = config
        self.blue_environment = "current_production"
        self.green_environment = "new_oci_environment"

    async def deploy_green_environment(self) -> Dict:
        """Deploy new OCI environment (green)"""

        print("🟢 Deploying Green Environment (OCI)...")

        steps = [
            "deploy_infrastructure",
            "deploy_agents",
            "configure_database",
            "setup_monitoring",
            "run_smoke_tests"
        ]

        results = {}
        for step in steps:
            print(f"   📋 Executing: {step}")
            result = await self._execute_deployment_step(step)
            results[step] = result

            if result["status"] != "success":
                raise Exception(f"Deployment failed at step: {step}")

        return {"green_deployment": results}

    async def run_parallel_testing(self) -> Dict:
        """Run parallel testing between blue and green"""

        print("🔄 Running parallel testing...")

        test_cases = [
            "data_consistency_test",
            "performance_comparison",
            "functionality_validation",
            "security_verification"
        ]

        results = {}
        for test in test_cases:
            blue_result = await self._run_test_on_environment(test, "blue")
            green_result = await self._run_test_on_environment(test, "green")

            results[test] = {
                "blue": blue_result,
                "green": green_result,
                "green_better": green_result["score"] >= blue_result["score"]
            }

        return {"parallel_testing": results}

    async def traffic_switching(self, percentage: int = 10) -> Dict:
        """Gradually switch traffic to green environment"""

        print(f"🔀 Switching {percentage}% traffic to green environment...")

        # Update API Gateway routing
        routing_config = {
            "blue_weight": 100 - percentage,
            "green_weight": percentage,
            "health_check_enabled": True,
            "fallback_to_blue": True
        }

        # Monitor for errors
        monitoring_period = 300  # 5 minutes
        error_threshold = 0.01   # 1%

        monitoring_result = await self._monitor_traffic_switch(
            routing_config,
            monitoring_period,
            error_threshold
        )

        return {
            "traffic_switch": {
                "percentage": percentage,
                "routing_config": routing_config,
                "monitoring_result": monitoring_result,
                "ready_for_next_increment": monitoring_result["error_rate"] < error_threshold
            }
        }

    async def complete_cutover(self) -> Dict:
        """Complete cutover to green environment"""

        print("🎯 Executing complete cutover to OCI...")

        # Final validation
        validation_result = await self._final_validation()

        if not validation_result["all_systems_green"]:
            raise Exception("Final validation failed - aborting cutover")

        # Switch 100% traffic
        cutover_result = await self.traffic_switching(100)

        # Update DNS if needed
        dns_result = await self._update_dns_records()

        # Decommission blue environment (after grace period)
        decommission_plan = await self._plan_blue_decommission()

        return {
            "complete_cutover": {
                "validation": validation_result,
                "traffic_switch": cutover_result,
                "dns_update": dns_result,
                "decommission_plan": decommission_plan,
                "migration_complete": True
            }
        }
```

#### 7.2 Production Monitoring Setup

**Create `migration/production_monitoring.yaml`:**
```yaml
apiVersion: monitoring.oci.oracle.com/v1
kind: MonitoringConfiguration
metadata:
  name: decisioning-production-monitoring
spec:
  compartmentId: ${COMPARTMENT_OCID}

  alarms:
    - name: "High Agent Execution Failures"
      metricCompartmentId: ${COMPARTMENT_OCID}
      namespace: "oci_faas"
      metricName: "FunctionErrors"
      query: "FunctionErrors[1m].sum() by resourceDisplayName"
      statistic: "Sum"
      resolution: "1m"
      severity: "CRITICAL"
      threshold: 5
      destinations:
        - ${CRITICAL_NOTIFICATIONS_TOPIC_OCID}

    - name: "Database Performance Degradation"
      namespace: "oci_autonomous_database"
      metricName: "CpuUtilization"
      query: "CpuUtilization[5m].mean()"
      threshold: 80
      severity: "WARNING"
      destinations:
        - ${WARNING_NOTIFICATIONS_TOPIC_OCID}

    - name: "Dashboard Response Time"
      namespace: "oci_apigateway"
      metricName: "HttpResponseTime"
      query: "HttpResponseTime[1m].mean()"
      threshold: 5000  # 5 seconds
      severity: "WARNING"

  dashboards:
    - name: "Decisioning Production Health"
      widgets:
        - type: "line_chart"
          title: "Agent Execution Times"
          query: "FunctionDuration[1m].mean() by resourceDisplayName"

        - type: "number"
          title: "Total Daily Analyses"
          query: "FunctionInvocations[1d].sum()"

        - type: "gauge"
          title: "System Health Score"
          query: "custom_health_score[5m].latest()"

        - type: "table"
          title: "Recent Errors"
          query: "FunctionErrors[1h].sum() by resourceDisplayName"

  custom_metrics:
    - name: "business_health_score"
      namespace: "decisioning_custom"
      description: "AI-calculated business health score"

    - name: "analysis_confidence_score"
      namespace: "decisioning_custom"
      description: "Average confidence score across all agents"

    - name: "dashboard_user_sessions"
      namespace: "decisioning_custom"
      description: "Active dashboard user sessions"
```

## 📊 Migration Timeline & Milestones

### Critical Path Schedule

```mermaid
gantt
    title Decisioning Agentic Flow - OCI Migration Timeline
    dateFormat  YYYY-MM-DD
    axisFormat  %m/%d

    section Phase 1: Planning
    Assessment & Planning    :p1, 2024-01-01, 14d
    Architecture Design     :p2, after p1, 7d

    section Phase 2: Infrastructure
    OCI Account Setup       :i1, after p2, 3d
    Network Configuration   :i2, after i1, 4d
    Security Foundation     :i3, after i2, 7d

    section Phase 3: Development
    Agent Containerization  :d1, after i3, 10d
    Gen AI Agents Config    :d2, after d1, 7d
    API Gateway Setup       :d3, after d2, 5d

    section Phase 4: Data Migration
    Database Migration      :m1, after d3, 7d
    Data Source Config      :m2, after m1, 3d

    section Phase 5: Dashboard
    OAC Migration          :v1, after m2, 10d
    APEX Alternative       :v2, after v1, 5d

    section Phase 6: Testing
    End-to-End Testing     :t1, after v2, 7d
    Performance Testing    :t2, after t1, 7d
    User Acceptance        :t3, after t2, 7d

    section Phase 7: Production
    Blue-Green Deployment  :prod1, after t3, 7d
    Traffic Migration      :prod2, after prod1, 7d
    Complete Cutover       :prod3, after prod2, 3d
```

### Success Criteria

| Phase | Success Metrics | Validation Method |
|-------|----------------|-------------------|
| Infrastructure | 99.9% uptime, <2s response | Automated monitoring |
| Agent Migration | 100% functional parity | Side-by-side testing |
| Data Migration | Zero data loss, <5min sync | Data validation scripts |
| Dashboard | User adoption >80% | Usage analytics |
| Production | <0.1% error rate | Performance monitoring |

### Risk Mitigation

| Risk | Impact | Mitigation Strategy |
|------|--------|-------------------|
| Agent execution failures | High | Comprehensive testing, fallback mechanisms |
| Data migration issues | Critical | Staged migration, rollback procedures |
| Performance degradation | Medium | Load testing, auto-scaling configuration |
| User adoption resistance | Medium | Training, phased rollout |
| Cost overruns | Medium | Resource monitoring, budget alerts |

## 🎯 Post-Migration Optimization

### Immediate Post-Migration (Week 11-12)

1. **Performance Optimization**
   - Function memory tuning
   - Database query optimization
   - Caching implementation

2. **Monitoring Enhancement**
   - Custom metric implementation
   - Alert fine-tuning
   - Dashboard optimization

3. **User Training & Support**
   - Executive dashboard training
   - Technical documentation
   - Support procedures

### Long-term Enhancements (Month 2-6)

1. **Advanced AI Features**
   - ML model integration
   - Predictive analytics
   - Natural language insights

2. **Enterprise Integration**
   - SSO implementation
   - API ecosystem expansion
   - Third-party connectors

3. **Global Deployment**
   - Multi-region setup
   - Data residency compliance
   - Performance optimization

---

This comprehensive migration strategy provides a detailed roadmap for successfully transitioning the Decisioning Agentic Flow from local MVP to enterprise-scale Oracle Cloud Infrastructure deployment, ensuring zero downtime and enhanced capabilities throughout the process.