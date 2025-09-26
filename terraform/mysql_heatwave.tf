# MySQL HeatWave Configuration for Decisioning Agentic Flow
# High-performance analytics and ML-native data platform

# Variables for MySQL HeatWave
variable "mysql_admin_username" {
  description = "MySQL administrator username"
  type        = string
  default     = "admin"
  validation {
    condition     = length(var.mysql_admin_username) >= 1 && length(var.mysql_admin_username) <= 16
    error_message = "MySQL admin username must be between 1 and 16 characters."
  }
}

variable "mysql_admin_password" {
  description = "MySQL administrator password (minimum 8 characters, include uppercase, lowercase, numeric, and special characters)"
  type        = string
  sensitive   = true
  validation {
    condition     = length(var.mysql_admin_password) >= 8
    error_message = "MySQL admin password must be at least 8 characters long."
  }
}

variable "mysql_shape_name" {
  description = "MySQL DB System compute shape"
  type        = string
  default     = "MySQL.HeatWave.VM.Standard.E3"
  validation {
    condition = contains([
      "MySQL.HeatWave.VM.Standard.E3",
      "MySQL.VM.Standard.E3.1.8GB",
      "MySQL.VM.Standard.E3.1.16GB",
      "MySQL.VM.Standard.E3.2.32GB",
      "MySQL.VM.Standard.E3.4.64GB",
      "MySQL.VM.Standard.E3.8.128GB"
    ], var.mysql_shape_name)
    error_message = "MySQL shape must be a valid MySQL DB System shape."
  }
}

variable "enable_heatwave_cluster" {
  description = "Enable HeatWave analytics cluster"
  type        = bool
  default     = true
}

variable "heatwave_cluster_size" {
  description = "Number of HeatWave analytics nodes (1-64)"
  type        = number
  default     = 2
  validation {
    condition     = var.heatwave_cluster_size >= 1 && var.heatwave_cluster_size <= 64
    error_message = "HeatWave cluster size must be between 1 and 64 nodes."
  }
}

variable "heatwave_shape_name" {
  description = "HeatWave analytics cluster node shape"
  type        = string
  default     = "MySQL.HeatWave.VM.Standard.E3"
  validation {
    condition = contains([
      "MySQL.HeatWave.VM.Standard.E3",
      "MySQL.HeatWave.BM.Standard3.64"
    ], var.heatwave_shape_name)
    error_message = "HeatWave shape must be a valid HeatWave node shape."
  }
}

variable "mysql_data_storage_size_in_gbs" {
  description = "Data storage size in GB for MySQL DB System"
  type        = number
  default     = 50
  validation {
    condition     = var.mysql_data_storage_size_in_gbs >= 50 && var.mysql_data_storage_size_in_gbs <= 65536
    error_message = "MySQL data storage size must be between 50 and 65536 GB."
  }
}

variable "mysql_port" {
  description = "MySQL port number"
  type        = number
  default     = 3306
  validation {
    condition     = var.mysql_port >= 1024 && var.mysql_port <= 65535
    error_message = "MySQL port must be between 1024 and 65535."
  }
}

variable "mysql_backup_retention_days" {
  description = "Number of days to retain MySQL backups"
  type        = number
  default     = 7
  validation {
    condition     = var.mysql_backup_retention_days >= 1 && var.mysql_backup_retention_days <= 35
    error_message = "MySQL backup retention must be between 1 and 35 days."
  }
}

variable "enable_mysql_high_availability" {
  description = "Enable high availability for MySQL (recommended for production)"
  type        = bool
  default     = false
}

variable "mysql_maintenance_window_start_time" {
  description = "Maintenance window start time (format: ddd HH:mm)"
  type        = string
  default     = "SUN 04:00"
  validation {
    condition     = can(regex("^(MON|TUE|WED|THU|FRI|SAT|SUN) ([0-1][0-9]|2[0-3]):[0-5][0-9]$", var.mysql_maintenance_window_start_time))
    error_message = "Maintenance window must be in format 'DDD HH:mm' (e.g., 'SUN 04:00')."
  }
}

# Network Security Group for MySQL HeatWave
resource "oci_core_network_security_group" "mysql_heatwave_nsg" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id
  vcn_id         = oci_core_vcn.decisioning_vcn.id
  display_name   = "${local.project_name}-mysql-heatwave-nsg"

  freeform_tags = local.common_tags
}

# MySQL HeatWave NSG Rules
resource "oci_core_network_security_group_security_rule" "mysql_ingress_3306" {
  network_security_group_id = oci_core_network_security_group.mysql_heatwave_nsg.id
  direction                 = "INGRESS"
  protocol                  = "6"
  source                    = "10.0.0.0/16"
  source_type               = "CIDR_BLOCK"
  description               = "Allow MySQL connections from VCN"

  tcp_options {
    destination_port_range {
      min = var.mysql_port
      max = var.mysql_port
    }
  }
}

resource "oci_core_network_security_group_security_rule" "mysql_ingress_33060" {
  network_security_group_id = oci_core_network_security_group.mysql_heatwave_nsg.id
  direction                 = "INGRESS"
  protocol                  = "6"
  source                    = "10.0.0.0/16"
  source_type               = "CIDR_BLOCK"
  description               = "Allow MySQL X Protocol connections from VCN"

  tcp_options {
    destination_port_range {
      min = 33060
      max = 33060
    }
  }
}

resource "oci_core_network_security_group_security_rule" "mysql_egress" {
  network_security_group_id = oci_core_network_security_group.mysql_heatwave_nsg.id
  direction                 = "EGRESS"
  protocol                  = "all"
  destination               = "0.0.0.0/0"
  destination_type          = "CIDR_BLOCK"
  description               = "Allow all outbound traffic"
}

# MySQL HeatWave Database System
resource "oci_mysql_mysql_db_system" "decisioning_heatwave" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id

  # Authentication
  admin_password = var.mysql_admin_password
  admin_username = var.mysql_admin_username

  # Placement
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
  shape_name         = var.mysql_shape_name
  subnet_id          = oci_core_subnet.database_subnet.id

  # Basic configuration
  display_name = "${local.project_name}-heatwave-db"
  description  = "MySQL HeatWave for Decisioning Agentic Flow analytics"

  # Storage
  data_storage_size_in_gb = var.mysql_data_storage_size_in_gbs

  # High availability (for production)
  is_highly_available = var.enable_mysql_high_availability

  # Port configuration
  port    = var.mysql_port
  port_x  = 33060

  # MySQL Configuration
  mysql_version = "8.0.35"

  configuration_id = oci_mysql_mysql_configuration.decisioning_mysql_config.id

  # Backup policy
  backup_policy {
    is_enabled        = true
    retention_in_days = var.mysql_backup_retention_days
    window_start_time = "03:00"

    # Point-in-time recovery
    pitr_policy {
      is_enabled = true
    }
  }

  # Maintenance window
  maintenance {
    window_start_time = var.mysql_maintenance_window_start_time
  }

  # Security
  is_secure_transport_required = true

  # Network security
  hostname_label = "decisioning-heatwave"

  freeform_tags = merge(local.common_tags, {
    "DatabaseType" = "MySQL HeatWave"
    "Purpose"      = "Analytics and ML"
  })

  lifecycle {
    ignore_changes = [
      # Ignore changes to admin_password to prevent accidental updates
      admin_password,
    ]
  }
}

# MySQL Configuration for optimal HeatWave performance
resource "oci_mysql_mysql_configuration" "decisioning_mysql_config" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id

  display_name = "${local.project_name}-mysql-config"
  description  = "Optimized MySQL configuration for HeatWave analytics"

  shape_name = var.mysql_shape_name

  # Configuration variables optimized for analytics workloads
  variables {
    # InnoDB settings for analytics
    innodb_buffer_pool_size                = "75%"
    innodb_buffer_pool_instances           = "8"
    innodb_log_file_size                   = "512M"
    innodb_flush_log_at_trx_commit        = "2"

    # Query optimization
    max_connections                        = "1000"
    query_cache_type                       = "OFF"
    query_cache_size                       = "0"

    # HeatWave specific settings
    secondary_engine_cost_threshold        = "100000"
    use_secondary_engine                   = "ON"

    # Performance schema for monitoring
    performance_schema                     = "ON"
    performance_schema_max_table_instances = "12500"

    # Logging
    slow_query_log                        = "ON"
    long_query_time                       = "2"
    log_queries_not_using_indexes         = "ON"

    # Security
    sql_mode = "STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO"
  }

  freeform_tags = local.common_tags
}

# HeatWave Analytics Cluster
resource "oci_mysql_analytics_cluster" "decisioning_analytics" {
  count = var.enable_heatwave_cluster ? 1 : 0

  db_system_id = oci_mysql_mysql_db_system.decisioning_heatwave.id

  cluster_size = var.heatwave_cluster_size
  shape_name   = var.heatwave_shape_name

  freeform_tags = merge(local.common_tags, {
    "Component" = "HeatWave Analytics"
    "Purpose"   = "In-Memory Analytics"
  })

  # Wait for DB system to be active
  depends_on = [oci_mysql_mysql_db_system.decisioning_heatwave]
}

# Create database user for agents
resource "null_resource" "mysql_setup" {
  depends_on = [oci_mysql_mysql_db_system.decisioning_heatwave]

  provisioner "local-exec" {
    command = <<-EOT
      # Wait for MySQL to be ready
      sleep 30

      # Create setup script
      cat > mysql_setup.sql << 'EOF'
-- Create database for decisioning
CREATE DATABASE IF NOT EXISTS decisioning_heatwave;

-- Create user for agents
CREATE USER IF NOT EXISTS 'decisioning_agent'@'%' IDENTIFIED BY '${var.mysql_admin_password}';

-- Grant privileges
GRANT ALL PRIVILEGES ON decisioning_heatwave.* TO 'decisioning_agent'@'%';

-- Grant HeatWave specific privileges
GRANT SECONDARY_ENGINE_USER ON *.* TO 'decisioning_agent'@'%';

-- Flush privileges
FLUSH PRIVILEGES;

-- Use the decisioning database
USE decisioning_heatwave;

-- Create optimized tables for analytics
CREATE TABLE IF NOT EXISTS projects (
    project_id VARCHAR(50) PRIMARY KEY,
    project_name VARCHAR(200) NOT NULL,
    project_type VARCHAR(50),
    start_date DATE,
    end_date DATE,
    budget_amount DECIMAL(15,2),
    actual_cost DECIMAL(15,2),
    status VARCHAR(20),
    customer_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_analytics_date (start_date, status),
    INDEX idx_analytics_customer (customer_id, project_type),
    INDEX idx_analytics_budget (budget_amount, actual_cost)
) ENGINE=InnoDB;

-- Create financial metrics table
CREATE TABLE IF NOT EXISTS financial_metrics (
    metric_id VARCHAR(50) PRIMARY KEY,
    project_id VARCHAR(50),
    metric_type VARCHAR(50),
    metric_value DECIMAL(15,2),
    metric_date DATE,
    currency_code VARCHAR(3) DEFAULT 'USD',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    INDEX idx_analytics_metrics (metric_date, metric_type, project_id),
    INDEX idx_analytics_value (metric_type, metric_value)
) ENGINE=InnoDB;

-- Create customer analytics table
CREATE TABLE IF NOT EXISTS customer_analytics (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(200),
    industry VARCHAR(100),
    annual_revenue DECIMAL(15,2),
    credit_rating VARCHAR(10),
    payment_terms INT,
    average_payment_days DECIMAL(5,1),
    total_projects INT DEFAULT 0,
    total_revenue DECIMAL(15,2) DEFAULT 0,
    risk_score DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_analytics_industry (industry, credit_rating),
    INDEX idx_analytics_revenue (annual_revenue, risk_score)
) ENGINE=InnoDB;

-- Create business events table for real-time processing
CREATE TABLE IF NOT EXISTS business_events (
    event_id VARCHAR(50) PRIMARY KEY,
    event_type VARCHAR(50),
    entity_type VARCHAR(50),
    entity_id VARCHAR(50),
    event_data JSON,
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE,

    INDEX idx_events_time (event_timestamp, event_type, processed),
    INDEX idx_events_entity (entity_type, entity_id)
) ENGINE=InnoDB;

-- Create agent results table
CREATE TABLE IF NOT EXISTS agent_results (
    result_id VARCHAR(50) PRIMARY KEY,
    agent_name VARCHAR(50) NOT NULL,
    execution_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL,
    execution_time DECIMAL(10,3),
    confidence_score DECIMAL(3,2),
    insights JSON,
    recommendations JSON,
    raw_data JSON,

    INDEX idx_results_agent (agent_name, execution_timestamp),
    INDEX idx_results_status (status, execution_timestamp)
) ENGINE=InnoDB;

-- Enable HeatWave for analytics tables
ALTER TABLE projects SECONDARY_ENGINE=RAPID;
ALTER TABLE financial_metrics SECONDARY_ENGINE=RAPID;
ALTER TABLE customer_analytics SECONDARY_ENGINE=RAPID;
ALTER TABLE business_events SECONDARY_ENGINE=RAPID;
ALTER TABLE agent_results SECONDARY_ENGINE=RAPID;

-- Load data into HeatWave
ALTER TABLE projects SECONDARY_LOAD;
ALTER TABLE financial_metrics SECONDARY_LOAD;
ALTER TABLE customer_analytics SECONDARY_LOAD;
ALTER TABLE business_events SECONDARY_LOAD;
ALTER TABLE agent_results SECONDARY_LOAD;
EOF

      echo "MySQL setup script created successfully"
    EOT
  }

  triggers = {
    db_system_id = oci_mysql_mysql_db_system.decisioning_heatwave.id
  }
}

# Outputs for MySQL HeatWave
output "mysql_heatwave_id" {
  description = "OCID of the MySQL HeatWave DB System"
  value       = oci_mysql_mysql_db_system.decisioning_heatwave.id
}

output "mysql_heatwave_hostname" {
  description = "Hostname of the MySQL HeatWave DB System"
  value       = oci_mysql_mysql_db_system.decisioning_heatwave.hostname_label
}

output "mysql_heatwave_fqdn" {
  description = "Fully qualified domain name of the MySQL HeatWave DB System"
  value       = "${oci_mysql_mysql_db_system.decisioning_heatwave.hostname_label}.${oci_core_subnet.database_subnet.dns_label}.${oci_core_vcn.decisioning_vcn.dns_label}.oraclevcn.com"
}

output "mysql_heatwave_port" {
  description = "Port number for MySQL connections"
  value       = oci_mysql_mysql_db_system.decisioning_heatwave.port
}

output "mysql_heatwave_port_x" {
  description = "Port number for MySQL X Protocol connections"
  value       = oci_mysql_mysql_db_system.decisioning_heatwave.port_x
}

output "heatwave_analytics_cluster_id" {
  description = "OCID of the HeatWave Analytics Cluster"
  value       = var.enable_heatwave_cluster ? oci_mysql_analytics_cluster.decisioning_analytics[0].id : null
}

output "heatwave_cluster_size" {
  description = "Number of nodes in the HeatWave Analytics Cluster"
  value       = var.enable_heatwave_cluster ? var.heatwave_cluster_size : 0
}

output "mysql_connection_string" {
  description = "MySQL connection string for applications"
  value = "mysql://${var.mysql_admin_username}@${oci_mysql_mysql_db_system.decisioning_heatwave.hostname_label}.${oci_core_subnet.database_subnet.dns_label}.${oci_core_vcn.decisioning_vcn.dns_label}.oraclevcn.com:${oci_mysql_mysql_db_system.decisioning_heatwave.port}/decisioning_heatwave"
  sensitive = true
}

# Data source for MySQL shapes (for reference)
data "oci_mysql_shapes" "mysql_shapes" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id

  filter {
    name   = "name"
    values = ["MySQL.HeatWave.VM.Standard.E3"]
  }
}

# Local values for HeatWave configuration
locals {
  mysql_heatwave_config = {
    host     = "${oci_mysql_mysql_db_system.decisioning_heatwave.hostname_label}.${oci_core_subnet.database_subnet.dns_label}.${oci_core_vcn.decisioning_vcn.dns_label}.oraclevcn.com"
    port     = oci_mysql_mysql_db_system.decisioning_heatwave.port
    database = "decisioning_heatwave"
    username = "decisioning_agent"
    heatwave_enabled = var.enable_heatwave_cluster
    cluster_size     = var.heatwave_cluster_size
  }
}