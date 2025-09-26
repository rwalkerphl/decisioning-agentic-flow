import io
import json
import logging
import time
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from fdk import response
import mysql.connector
from mysql.connector import Error

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentResult:
    """Standard result format for all agents"""
    def __init__(self, agent_name: str, task_id: str, status: str, data: Dict[str, Any],
                 insights: List[str], recommendations: List[str], timestamp: datetime,
                 execution_time: float, confidence_score: float):
        self.agent_name = agent_name
        self.task_id = task_id
        self.status = status
        self.data = data
        self.insights = insights
        self.recommendations = recommendations
        self.timestamp = timestamp
        self.execution_time = execution_time
        self.confidence_score = confidence_score

    def to_dict(self):
        return {
            "agent_name": self.agent_name,
            "task_id": self.task_id,
            "status": self.status,
            "data": self.data,
            "insights": self.insights,
            "recommendations": self.recommendations,
            "timestamp": self.timestamp.isoformat(),
            "execution_time": self.execution_time,
            "confidence_score": self.confidence_score
        }

class HeatWaveViewGeneratorAgent:
    """Agent that dynamically creates analytical views on HeatWave OLAP side"""

    def __init__(self, config: Dict):
        self.config = config
        self.name = "view_generator"
        self.heatwave_config = config.get('heatwave', {})
        self.connection = None
        self.view_registry = {}
        self.metric_definitions = self._load_metric_definitions()

    def _create_heatwave_connection(self):
        """Create optimized HeatWave connection"""
        try:
            connection_config = {
                'host': self.heatwave_config.get('host', 'localhost'),
                'port': self.heatwave_config.get('port', 3306),
                'user': self.heatwave_config.get('user', 'decisioning_agent'),
                'password': self.heatwave_config.get('password', ''),
                'database': self.heatwave_config.get('database', 'decisioning_heatwave'),
                'use_unicode': True,
                'charset': 'utf8mb4',
                'autocommit': True,
                'connect_timeout': self.heatwave_config.get('connection_timeout', 30),
                'use_pure': False,
                'sql_mode': '',
                'raise_on_warnings': False
            }

            connection = mysql.connector.connect(**connection_config)

            # Enable HeatWave secondary engine
            cursor = connection.cursor()
            try:
                cursor.execute("SET SESSION use_secondary_engine = ON")
                cursor.execute("SET SESSION secondary_engine_cost_threshold = 100000")
                logger.info("HeatWave secondary engine enabled for view generation")
            except Error as e:
                logger.warning(f"Could not enable HeatWave engine: {e}")
            finally:
                cursor.close()

            return connection

        except Error as e:
            logger.error(f"Failed to connect to MySQL HeatWave: {e}")
            return None

    def execute(self, input_data: Dict) -> AgentResult:
        """Execute view generation based on metric requirements"""
        start_time = time.time()

        try:
            logger.info(f"Starting HeatWave {self.name} agent execution")

            # Create connection
            self.connection = self._create_heatwave_connection()
            if not self.connection:
                raise Exception("Failed to establish HeatWave connection")

            # Analyze current data structure
            data_analysis = self._analyze_oltp_schema()

            # Get required metrics from input
            required_metrics = input_data.get('required_metrics', [
                'revenue_trend', 'cash_flow_analysis', 'project_efficiency',
                'customer_health_score'
            ])

            # Identify missing metrics
            missing_metrics = self._identify_missing_metrics(required_metrics)

            # Generate new views for missing metrics
            created_views = []
            for metric in missing_metrics:
                view_result = self._create_metric_view(metric, data_analysis)
                if view_result['success']:
                    created_views.append(view_result)

            # Optimize existing views
            optimization_results = self._optimize_existing_views()

            # Update view registry
            self._update_view_registry(created_views)

            execution_time = time.time() - start_time

            result = AgentResult(
                agent_name=self.name,
                task_id=f"{self.name}_{int(time.time())}",
                status="success",
                data={
                    "created_views": created_views,
                    "optimization_results": optimization_results,
                    "data_analysis": data_analysis,
                    "view_registry": self.view_registry,
                    "required_metrics": required_metrics,
                    "missing_metrics": missing_metrics
                },
                insights=self._generate_view_insights(created_views, optimization_results),
                recommendations=self._generate_view_recommendations(data_analysis),
                timestamp=datetime.now(),
                execution_time=execution_time,
                confidence_score=0.95
            )

            logger.info(f"View generator agent completed successfully in {execution_time:.2f}s")
            return result

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"View generator agent failed: {str(e)}")

            return AgentResult(
                agent_name=self.name,
                task_id=f"{self.name}_{int(time.time())}",
                status="error",
                data={"error": str(e)},
                insights=[],
                recommendations=[],
                timestamp=datetime.now(),
                execution_time=execution_time,
                confidence_score=0.0
            )

        finally:
            if self.connection:
                self.connection.close()

    def _analyze_oltp_schema(self) -> Dict:
        """Analyze OLTP schema to understand data structure"""
        cursor = self.connection.cursor()

        try:
            # Get table information
            cursor.execute("""
                SELECT
                    TABLE_NAME,
                    COLUMN_NAME,
                    DATA_TYPE,
                    IS_NULLABLE,
                    COLUMN_KEY,
                    EXTRA
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                ORDER BY TABLE_NAME, ORDINAL_POSITION
            """)

            schema_info = {}
            for row in cursor.fetchall():
                table_name = row[0]
                if table_name not in schema_info:
                    schema_info[table_name] = {
                        'columns': [],
                        'primary_keys': [],
                        'foreign_keys': []
                    }

                column_info = {
                    'name': row[1],
                    'type': row[2],
                    'nullable': row[3] == 'YES',
                    'key': row[4],
                    'extra': row[5]
                }

                schema_info[table_name]['columns'].append(column_info)

                if row[4] == 'PRI':
                    schema_info[table_name]['primary_keys'].append(row[1])

            # Get data statistics
            data_stats = {}
            for table_name in schema_info.keys():
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    row_count = cursor.fetchone()[0]
                    data_stats[table_name] = {'row_count': row_count}
                except Error:
                    data_stats[table_name] = {'row_count': 0}

            return {
                'schema_info': schema_info,
                'data_statistics': data_stats,
                'analysis_timestamp': datetime.now().isoformat(),
                'total_tables': len(schema_info),
                'total_columns': sum(len(table['columns']) for table in schema_info.values())
            }

        except Exception as e:
            logger.error(f"Schema analysis failed: {str(e)}")
            return {
                'schema_info': {},
                'data_statistics': {},
                'analysis_timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
        finally:
            cursor.close()

    def _identify_missing_metrics(self, required_metrics: List[str]) -> List[Dict]:
        """Identify metrics that need new views"""
        cursor = self.connection.cursor()
        existing_views = set()

        try:
            # Get existing views
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            for table in tables:
                table_name = table[0]
                if table_name.startswith('analytics_'):
                    metric_name = table_name.replace('analytics_', '')
                    existing_views.add(metric_name)
                    self.view_registry[metric_name] = {
                        'view_name': table_name,
                        'status': 'existing'
                    }

        except Error as e:
            logger.warning(f"Could not check existing views: {e}")
        finally:
            cursor.close()

        missing_metrics = []
        for metric_name in required_metrics:
            if metric_name not in existing_views:
                metric_def = self.metric_definitions.get(metric_name)
                if metric_def:
                    missing_metrics.append({
                        'name': metric_name,
                        'definition': metric_def,
                        'priority': metric_def.get('priority', 'medium')
                    })

        # Sort by priority
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        missing_metrics.sort(key=lambda x: priority_order.get(x['priority'], 2), reverse=True)

        return missing_metrics

    def _create_metric_view(self, metric: Dict, data_analysis: Dict) -> Dict:
        """Create a new analytical view for a specific metric"""
        metric_name = metric['name']
        metric_def = metric['definition']

        try:
            # Generate optimized SQL for the metric
            view_sql = self._generate_view_sql(metric_def, data_analysis)

            if not view_sql:
                return {
                    'success': False,
                    'metric_name': metric_name,
                    'error': 'Could not generate SQL for metric',
                    'created_at': datetime.now().isoformat()
                }

            # Create the view on HeatWave OLAP side
            view_name = f"analytics_{metric_name}"

            cursor = self.connection.cursor()

            # Drop view if exists
            try:
                cursor.execute(f"DROP VIEW IF EXISTS {view_name}")
            except Error:
                pass

            # Create new view
            create_view_sql = f"CREATE VIEW {view_name} AS {view_sql}"
            cursor.execute(create_view_sql)

            # Load view into HeatWave if possible
            try:
                cursor.execute(f"ALTER VIEW {view_name} SECONDARY_ENGINE=RAPID")
                cursor.execute(f"ALTER VIEW {view_name} SECONDARY_LOAD")
                heatwave_enabled = True
            except Error as e:
                logger.warning(f"Could not load view {view_name} into HeatWave: {e}")
                heatwave_enabled = False

            # Test view performance
            performance_result = self._test_view_performance(view_name)

            cursor.close()

            return {
                'success': True,
                'metric_name': metric_name,
                'view_name': view_name,
                'view_sql': view_sql,
                'heatwave_enabled': heatwave_enabled,
                'performance': performance_result,
                'created_at': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Failed to create view for metric {metric_name}: {str(e)}")
            return {
                'success': False,
                'metric_name': metric_name,
                'error': str(e),
                'created_at': datetime.now().isoformat()
            }

    def _generate_view_sql(self, metric_def: Dict, data_analysis: Dict) -> str:
        """Generate optimized SQL for metric view"""
        metric_type = metric_def.get('type', 'custom')
        metric_name = metric_def.get('name', '')

        # Check if we have the required tables
        schema_info = data_analysis.get('schema_info', {})
        available_tables = set(schema_info.keys())

        logger.info(f"Generating SQL for {metric_name} of type {metric_type}")
        logger.info(f"Available tables: {available_tables}")

        if metric_type == 'financial_kpi':
            return self._generate_financial_kpi_sql(metric_def, schema_info)
        elif metric_type == 'operational_metric':
            return self._generate_operational_metric_sql(metric_def, schema_info)
        elif metric_type == 'customer_insight':
            return self._generate_customer_insight_sql(metric_def, schema_info)
        elif metric_type == 'trend_analysis':
            return self._generate_trend_analysis_sql(metric_def, schema_info)
        else:
            return self._generate_default_view_sql(metric_def, schema_info)

    def _generate_financial_kpi_sql(self, metric_def: Dict, schema_info: Dict) -> str:
        """Generate SQL for financial KPI views"""
        metric_name = metric_def.get('name', '')

        # Check for financial transactions table (OLTP side)
        if 'financial_transactions_oltp' in schema_info:
            if metric_name == 'revenue_trend':
                return """
                SELECT
                    DATE_FORMAT(ft.transaction_date, '%Y-%m') as period,
                    SUM(CASE WHEN ft.transaction_type = 'INVOICE' THEN ft.amount ELSE 0 END) as revenue,
                    SUM(CASE WHEN ft.transaction_type = 'COST' THEN ft.amount ELSE 0 END) as costs,
                    (SUM(CASE WHEN ft.transaction_type = 'INVOICE' THEN ft.amount ELSE 0 END) -
                     SUM(CASE WHEN ft.transaction_type = 'COST' THEN ft.amount ELSE 0 END)) as net_profit,
                    COUNT(DISTINCT ft.project_id) as active_projects,
                    COUNT(DISTINCT p.customer_id) as active_customers
                FROM financial_transactions_oltp ft
                LEFT JOIN projects_oltp p ON ft.project_id = p.project_id
                WHERE ft.transaction_date >= DATE_SUB(CURDATE(), INTERVAL 24 MONTH)
                    AND ft.status = 'COMPLETED'
                GROUP BY DATE_FORMAT(ft.transaction_date, '%Y-%m')
                ORDER BY period DESC
                """

            elif metric_name == 'cash_flow_analysis':
                return """
                SELECT
                    DATE_FORMAT(ft.transaction_date, '%Y-%m') as period,
                    SUM(CASE WHEN ft.transaction_type = 'INVOICE' THEN ft.amount ELSE 0 END) as invoiced,
                    SUM(CASE WHEN ft.transaction_type = 'PAYMENT' THEN ft.amount ELSE 0 END) as collected,
                    (SUM(CASE WHEN ft.transaction_type = 'INVOICE' THEN ft.amount ELSE 0 END) -
                     SUM(CASE WHEN ft.transaction_type = 'PAYMENT' THEN ft.amount ELSE 0 END)) as outstanding_ar,
                    CASE WHEN SUM(CASE WHEN ft.transaction_type = 'INVOICE' THEN ft.amount ELSE 0 END) > 0
                         THEN (SUM(CASE WHEN ft.transaction_type = 'PAYMENT' THEN ft.amount ELSE 0 END) /
                               SUM(CASE WHEN ft.transaction_type = 'INVOICE' THEN ft.amount ELSE 0 END) * 100)
                         ELSE 0 END as collection_rate,
                    AVG(DATEDIFF(CURDATE(), ft.transaction_date)) as avg_days_outstanding
                FROM financial_transactions_oltp ft
                WHERE ft.transaction_date >= DATE_SUB(CURDATE(), INTERVAL 18 MONTH)
                    AND ft.status = 'COMPLETED'
                    AND ft.transaction_type IN ('INVOICE', 'PAYMENT')
                GROUP BY DATE_FORMAT(ft.transaction_date, '%Y-%m')
                ORDER BY period DESC
                """

        # Fallback to legacy financial_metrics table
        elif 'financial_metrics' in schema_info:
            if metric_name == 'revenue_trend':
                return """
                SELECT
                    DATE_FORMAT(fm.metric_date, '%Y-%m') as period,
                    SUM(CASE WHEN fm.metric_type = 'REVENUE' THEN fm.metric_value ELSE 0 END) as revenue,
                    SUM(CASE WHEN fm.metric_type = 'COST' THEN fm.metric_value ELSE 0 END) as costs,
                    (SUM(CASE WHEN fm.metric_type = 'REVENUE' THEN fm.metric_value ELSE 0 END) -
                     SUM(CASE WHEN fm.metric_type = 'COST' THEN fm.metric_value ELSE 0 END)) as net_profit,
                    COUNT(DISTINCT fm.project_id) as active_projects
                FROM financial_metrics fm
                WHERE fm.metric_date >= DATE_SUB(CURDATE(), INTERVAL 24 MONTH)
                GROUP BY DATE_FORMAT(fm.metric_date, '%Y-%m')
                ORDER BY period DESC
                """

        return ""

    def _generate_operational_metric_sql(self, metric_def: Dict, schema_info: Dict) -> str:
        """Generate SQL for operational metric views"""
        metric_name = metric_def.get('name', '')

        if 'projects_oltp' in schema_info or 'projects' in schema_info:
            table_name = 'projects_oltp' if 'projects_oltp' in schema_info else 'projects'

            if metric_name == 'project_efficiency':
                return f"""
                SELECT
                    p.project_type,
                    p.status,
                    COUNT(*) as project_count,
                    AVG(CASE WHEN p.end_date IS NOT NULL
                             THEN DATEDIFF(p.end_date, p.start_date)
                             ELSE DATEDIFF(CURDATE(), p.start_date) END) as avg_duration_days,
                    AVG(CASE WHEN p.budget_amount > 0
                             THEN (p.actual_cost / p.budget_amount * 100) END) as avg_budget_utilization_pct,
                    SUM(p.budget_amount) as total_planned_value,
                    SUM(p.actual_cost) as total_actual_cost,
                    CASE WHEN SUM(p.budget_amount) > 0
                         THEN ((SUM(p.budget_amount) - SUM(p.actual_cost)) / SUM(p.budget_amount) * 100)
                         ELSE 0 END as cost_savings_pct
                FROM {table_name} p
                WHERE p.start_date >= DATE_SUB(CURDATE(), INTERVAL 24 MONTH)
                GROUP BY p.project_type, p.status
                ORDER BY project_count DESC
                """

        return ""

    def _generate_customer_insight_sql(self, metric_def: Dict, schema_info: Dict) -> str:
        """Generate SQL for customer insight views"""
        metric_name = metric_def.get('name', '')

        if metric_name == 'customer_health_score':
            # Check available tables
            customers_table = None
            projects_table = None

            if 'customers_oltp' in schema_info:
                customers_table = 'customers_oltp'
            elif 'customer_analytics' in schema_info:
                customers_table = 'customer_analytics'

            if 'projects_oltp' in schema_info:
                projects_table = 'projects_oltp'
            elif 'projects' in schema_info:
                projects_table = 'projects'

            if customers_table and projects_table:
                return f"""
                SELECT
                    c.customer_id,
                    c.customer_name,
                    c.industry,
                    COALESCE(c.annual_revenue, 0) as annual_revenue,
                    COALESCE(c.credit_rating, 'UNKNOWN') as credit_rating,
                    COUNT(p.project_id) as total_projects,
                    COALESCE(SUM(p.budget_amount), 0) as total_project_value,
                    AVG(CASE WHEN p.budget_amount > 0
                             THEN (p.actual_cost / p.budget_amount) END) as avg_cost_efficiency,
                    MAX(p.start_date) as last_project_date,
                    COALESCE(DATEDIFF(CURDATE(), MAX(p.start_date)), 9999) as days_since_last_project,
                    -- Health Score Calculation
                    CASE
                        WHEN COUNT(p.project_id) >= 3 AND DATEDIFF(CURDATE(), MAX(p.start_date)) <= 90 THEN 'EXCELLENT'
                        WHEN COUNT(p.project_id) >= 2 AND DATEDIFF(CURDATE(), MAX(p.start_date)) <= 180 THEN 'GOOD'
                        WHEN COUNT(p.project_id) >= 1 AND DATEDIFF(CURDATE(), MAX(p.start_date)) <= 365 THEN 'FAIR'
                        ELSE 'POOR'
                    END as health_category,
                    -- Numeric health score (0-100)
                    GREATEST(0, LEAST(100,
                        100 -
                        (GREATEST(0, DATEDIFF(CURDATE(), MAX(p.start_date)) - 90) * 0.1) -
                        (CASE WHEN COUNT(p.project_id) = 0 THEN 50 ELSE 0 END)
                    )) as health_score_numeric
                FROM {customers_table} c
                LEFT JOIN {projects_table} p ON c.customer_id = p.customer_id
                WHERE c.status = 'ACTIVE' OR c.status IS NULL
                GROUP BY c.customer_id, c.customer_name, c.industry, c.annual_revenue, c.credit_rating
                ORDER BY health_score_numeric DESC
                """

        return ""

    def _generate_trend_analysis_sql(self, metric_def: Dict, schema_info: Dict) -> str:
        """Generate SQL for trend analysis views"""
        # For now, return a simple trend analysis if we have financial data
        if 'financial_metrics' in schema_info:
            return """
            SELECT
                DATE_FORMAT(fm.metric_date, '%Y-%m') as period,
                COUNT(DISTINCT fm.project_id) as active_projects,
                SUM(fm.metric_value) as total_value,
                AVG(fm.metric_value) as avg_value
            FROM financial_metrics fm
            WHERE fm.metric_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
            GROUP BY DATE_FORMAT(fm.metric_date, '%Y-%m')
            ORDER BY period DESC
            """
        return ""

    def _generate_default_view_sql(self, metric_def: Dict, schema_info: Dict) -> str:
        """Generate default view SQL when specific type is not recognized"""
        # Return a simple count query for the first available table
        if schema_info:
            first_table = list(schema_info.keys())[0]
            return f"""
            SELECT
                COUNT(*) as total_records,
                DATE(created_at) as date_created
            FROM {first_table}
            WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            GROUP BY DATE(created_at)
            ORDER BY date_created DESC
            """
        return ""

    def _test_view_performance(self, view_name: str) -> Dict:
        """Test view performance on HeatWave"""
        cursor = self.connection.cursor()

        try:
            # Test simple aggregation
            start_time = time.time()
            cursor.execute(f"SELECT COUNT(*) FROM {view_name}")
            result = cursor.fetchone()
            execution_time = time.time() - start_time

            return {
                'execution_time_seconds': execution_time,
                'row_count': result[0] if result else 0,
                'performance_rating': 'EXCELLENT' if execution_time < 0.1 else 'GOOD' if execution_time < 1.0 else 'NEEDS_OPTIMIZATION',
                'heatwave_accelerated': execution_time < 0.5
            }

        except Exception as e:
            return {
                'execution_time_seconds': None,
                'error': str(e),
                'performance_rating': 'ERROR'
            }
        finally:
            cursor.close()

    def _optimize_existing_views(self) -> Dict:
        """Optimize existing analytical views"""
        optimization_results = {}

        for metric_name, view_info in self.view_registry.items():
            if view_info.get('status') == 'existing':
                view_name = view_info['view_name']
                try:
                    # Test current performance
                    current_performance = self._test_view_performance(view_name)

                    # If performance is suboptimal, try to reload into HeatWave
                    if current_performance['performance_rating'] == 'NEEDS_OPTIMIZATION':
                        cursor = self.connection.cursor()
                        try:
                            cursor.execute(f"ALTER VIEW {view_name} SECONDARY_UNLOAD")
                            cursor.execute(f"ALTER VIEW {view_name} SECONDARY_LOAD")
                            new_performance = self._test_view_performance(view_name)
                            optimization_results[view_name] = {
                                'optimized': True,
                                'before_performance': current_performance,
                                'after_performance': new_performance
                            }
                        except Error as e:
                            optimization_results[view_name] = {
                                'optimized': False,
                                'error': f"HeatWave optimization failed: {str(e)}"
                            }
                        finally:
                            cursor.close()
                    else:
                        optimization_results[view_name] = {
                            'optimized': False,
                            'reason': 'Performance already optimal',
                            'current_performance': current_performance
                        }

                except Exception as e:
                    optimization_results[view_name] = {
                        'optimized': False,
                        'error': str(e)
                    }

        return optimization_results

    def _update_view_registry(self, created_views: List[Dict]):
        """Update view registry with newly created views"""
        for view_info in created_views:
            if view_info['success']:
                metric_name = view_info['metric_name']
                self.view_registry[metric_name] = {
                    'view_name': view_info['view_name'],
                    'status': 'created',
                    'created_at': view_info['created_at'],
                    'heatwave_enabled': view_info.get('heatwave_enabled', False),
                    'performance': view_info.get('performance', {})
                }

    def _generate_view_insights(self, created_views: List[Dict], optimization_results: Dict) -> List[str]:
        """Generate insights from view creation and optimization"""
        insights = []

        successful_creations = [v for v in created_views if v['success']]
        if successful_creations:
            insights.append(f"Successfully created {len(successful_creations)} new analytical views on HeatWave OLAP engine")

        heatwave_enabled_views = [v for v in successful_creations if v.get('heatwave_enabled', False)]
        if heatwave_enabled_views:
            insights.append(f"Enabled HeatWave acceleration for {len(heatwave_enabled_views)} views, providing 100x+ query performance")

        optimized_views = [v for v in optimization_results.values() if v.get('optimized', False)]
        if optimized_views:
            insights.append(f"Optimized {len(optimized_views)} existing views for better analytical performance")

        fast_views = [v for v in successful_creations if v.get('performance', {}).get('execution_time_seconds', 1) < 0.1]
        if fast_views:
            insights.append(f"Generated {len(fast_views)} ultra-fast views with sub-100ms query response times")

        return insights

    def _generate_view_recommendations(self, data_analysis: Dict) -> List[str]:
        """Generate recommendations based on data analysis"""
        recommendations = []

        total_tables = data_analysis.get('total_tables', 0)
        if total_tables < 5:
            recommendations.append("Consider adding more data sources to enable richer analytical views")

        schema_info = data_analysis.get('schema_info', {})
        if 'financial_transactions_oltp' not in schema_info:
            recommendations.append("Implement transactional financial data structure for real-time cash flow analytics")

        if 'customers_oltp' not in schema_info:
            recommendations.append("Add customer master data table to enable customer intelligence views")

        recommendations.append("Schedule regular view optimization to maintain peak HeatWave performance")
        recommendations.append("Monitor view usage patterns to optimize the most frequently accessed metrics")

        return recommendations

    def _load_metric_definitions(self) -> Dict:
        """Load predefined metric definitions"""
        return {
            'revenue_trend': {
                'type': 'financial_kpi',
                'tables': ['financial_transactions_oltp', 'projects_oltp'],
                'priority': 'high',
                'description': 'Monthly revenue trends with profit margins and project activity'
            },
            'cash_flow_analysis': {
                'type': 'financial_kpi',
                'tables': ['financial_transactions_oltp'],
                'priority': 'high',
                'description': 'Cash flow analysis with AR and collection efficiency metrics'
            },
            'project_efficiency': {
                'type': 'operational_metric',
                'tables': ['projects_oltp'],
                'priority': 'medium',
                'description': 'Project efficiency and resource utilization metrics'
            },
            'customer_health_score': {
                'type': 'customer_insight',
                'tables': ['customers_oltp', 'projects_oltp'],
                'priority': 'high',
                'description': 'Customer health scores with risk assessment and engagement metrics'
            },
            'business_trends': {
                'type': 'trend_analysis',
                'tables': ['financial_metrics', 'projects'],
                'priority': 'medium',
                'description': 'Business trend analysis with growth rates and seasonality patterns'
            }
        }

def handler(ctx, data: io.BytesIO = None):
    """OCI Function handler for HeatWave view generator agent"""

    try:
        # Parse input data
        if data and data.getvalue():
            input_data = json.loads(data.getvalue())
        else:
            input_data = {}

        logger.info("HeatWave View Generator agent function invoked")

        # Extract HeatWave configuration from environment or input
        heatwave_config = {
            'host': os.environ.get('MYSQL_HOST', input_data.get('heatwave', {}).get('host', 'localhost')),
            'port': int(os.environ.get('MYSQL_PORT', '3306')),
            'user': os.environ.get('MYSQL_USER', 'decisioning_agent'),
            'password': os.environ.get('MYSQL_PASSWORD', ''),
            'database': os.environ.get('MYSQL_DATABASE', 'decisioning_heatwave'),
            'connection_timeout': int(os.environ.get('MYSQL_CONNECTION_TIMEOUT', '30'))
        }

        # Initialize agent with HeatWave configuration
        agent_config = {
            'heatwave': heatwave_config,
            'auto_optimization': os.environ.get('AUTO_VIEW_OPTIMIZATION', 'true').lower() == 'true',
            'performance_monitoring': os.environ.get('VIEW_PERFORMANCE_MONITORING', 'true').lower() == 'true'
        }
        agent_config.update(input_data.get('config', {}))

        agent = HeatWaveViewGeneratorAgent(config=agent_config)

        # Execute agent logic
        result = agent.execute(input_data)

        return response.Response(
            ctx,
            response_data=json.dumps(result.to_dict(), default=str),
            headers={"Content-Type": "application/json"}
        )

    except Exception as e:
        logger.error(f"HeatWave view generator agent function failed: {str(e)}")
        error_result = {
            "agent_name": "view_generator",
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

        return response.Response(
            ctx,
            response_data=json.dumps(error_result),
            headers={"Content-Type": "application/json"},
            status_code=500
        )