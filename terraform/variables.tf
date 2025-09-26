# Variables for Oracle Cloud Infrastructure Deployment
# Decisioning Agentic Flow

# Required Variables

variable "tenancy_ocid" {
  description = "OCID of the tenancy (root compartment)"
  type        = string
  validation {
    condition     = can(regex("^ocid1\\.tenancy\\.", var.tenancy_ocid))
    error_message = "The tenancy_ocid must be a valid OCI tenancy OCID starting with 'ocid1.tenancy.'."
  }
}

variable "compartment_ocid" {
  description = "OCID of the parent compartment where resources will be created"
  type        = string
  validation {
    condition     = can(regex("^ocid1\\.(compartment|tenancy)\\.", var.compartment_ocid))
    error_message = "The compartment_ocid must be a valid OCI compartment OCID."
  }
}

variable "region" {
  description = "OCI region where resources will be deployed"
  type        = string
  default     = "us-ashburn-1"
  validation {
    condition = contains([
      "us-ashburn-1", "us-phoenix-1", "us-sanjose-1",
      "ca-toronto-1", "ca-montreal-1",
      "eu-frankfurt-1", "eu-zurich-1", "eu-amsterdam-1", "uk-london-1",
      "ap-mumbai-1", "ap-seoul-1", "ap-sydney-1", "ap-tokyo-1", "ap-singapore-1",
      "sa-saopaulo-1",
      "me-jeddah-1", "me-dubai-1",
      "af-johannesburg-1"
    ], var.region)
    error_message = "Region must be a valid OCI region identifier."
  }
}

# Database Configuration

variable "db_admin_password" {
  description = "Admin password for Autonomous Database (minimum 12 characters, must include uppercase, lowercase, numeric, and special characters)"
  type        = string
  sensitive   = true
  validation {
    condition     = length(var.db_admin_password) >= 12
    error_message = "Database admin password must be at least 12 characters long."
  }
}

# Environment Configuration

variable "environment" {
  description = "Environment name (dev, test, stage, prod)"
  type        = string
  default     = "dev"
  validation {
    condition     = contains(["dev", "test", "stage", "prod"], var.environment)
    error_message = "Environment must be one of: dev, test, stage, prod."
  }
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "decisioning-agentic-flow"
  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.project_name))
    error_message = "Project name must contain only lowercase letters, numbers, and hyphens."
  }
}

# Network Configuration

variable "vcn_cidr_block" {
  description = "CIDR block for the Virtual Cloud Network"
  type        = string
  default     = "10.0.0.0/16"
  validation {
    condition     = can(cidrhost(var.vcn_cidr_block, 0))
    error_message = "VCN CIDR block must be a valid IPv4 CIDR notation."
  }
}

variable "public_subnet_cidr" {
  description = "CIDR block for the public subnet"
  type        = string
  default     = "10.0.1.0/24"
  validation {
    condition     = can(cidrhost(var.public_subnet_cidr, 0))
    error_message = "Public subnet CIDR block must be a valid IPv4 CIDR notation."
  }
}

variable "functions_subnet_cidr" {
  description = "CIDR block for the functions subnet"
  type        = string
  default     = "10.0.2.0/24"
  validation {
    condition     = can(cidrhost(var.functions_subnet_cidr, 0))
    error_message = "Functions subnet CIDR block must be a valid IPv4 CIDR notation."
  }
}

variable "database_subnet_cidr" {
  description = "CIDR block for the database subnet"
  type        = string
  default     = "10.0.3.0/24"
  validation {
    condition     = can(cidrhost(var.database_subnet_cidr, 0))
    error_message = "Database subnet CIDR block must be a valid IPv4 CIDR notation."
  }
}

# Database Configuration

variable "db_cpu_core_count" {
  description = "Number of CPU cores for the Autonomous Database"
  type        = number
  default     = 1
  validation {
    condition     = var.db_cpu_core_count >= 1 && var.db_cpu_core_count <= 128
    error_message = "CPU core count must be between 1 and 128."
  }
}

variable "db_data_storage_size_in_tbs" {
  description = "Data storage size in terabytes for the Autonomous Database"
  type        = number
  default     = 1
  validation {
    condition     = var.db_data_storage_size_in_tbs >= 1 && var.db_data_storage_size_in_tbs <= 128
    error_message = "Data storage size must be between 1 and 128 TB."
  }
}

variable "db_auto_scaling_enabled" {
  description = "Enable auto scaling for the Autonomous Database"
  type        = bool
  default     = true
}

variable "db_is_serverless" {
  description = "Configure Autonomous Database as serverless"
  type        = bool
  default     = true
}

variable "db_license_model" {
  description = "License model for Autonomous Database (LICENSE_INCLUDED or BRING_YOUR_OWN_LICENSE)"
  type        = string
  default     = "LICENSE_INCLUDED"
  validation {
    condition     = contains(["LICENSE_INCLUDED", "BRING_YOUR_OWN_LICENSE"], var.db_license_model)
    error_message = "License model must be either LICENSE_INCLUDED or BRING_YOUR_OWN_LICENSE."
  }
}

# Functions Configuration

variable "functions_timeout_in_seconds" {
  description = "Timeout in seconds for function execution"
  type        = number
  default     = 300
  validation {
    condition     = var.functions_timeout_in_seconds >= 30 && var.functions_timeout_in_seconds <= 3600
    error_message = "Function timeout must be between 30 and 3600 seconds."
  }
}

variable "functions_memory_in_mbs" {
  description = "Memory allocation in MB for functions"
  type        = number
  default     = 512
  validation {
    condition     = contains([128, 256, 512, 1024, 2048, 3008], var.functions_memory_in_mbs)
    error_message = "Function memory must be one of: 128, 256, 512, 1024, 2048, 3008 MB."
  }
}

# API Gateway Configuration

variable "api_gateway_endpoint_type" {
  description = "API Gateway endpoint type (PUBLIC or PRIVATE)"
  type        = string
  default     = "PUBLIC"
  validation {
    condition     = contains(["PUBLIC", "PRIVATE"], var.api_gateway_endpoint_type)
    error_message = "API Gateway endpoint type must be either PUBLIC or PRIVATE."
  }
}

# Object Storage Configuration

variable "enable_object_versioning" {
  description = "Enable versioning for object storage buckets"
  type        = bool
  default     = true
}

variable "object_storage_tier" {
  description = "Default storage tier for object storage buckets"
  type        = string
  default     = "Standard"
  validation {
    condition     = contains(["Standard", "InfrequentAccess", "Archive"], var.object_storage_tier)
    error_message = "Storage tier must be one of: Standard, InfrequentAccess, Archive."
  }
}

variable "results_retention_days" {
  description = "Number of days to retain analysis results"
  type        = number
  default     = 365
  validation {
    condition     = var.results_retention_days >= 30 && var.results_retention_days <= 3650
    error_message = "Results retention must be between 30 and 3650 days."
  }
}

# Security Configuration

variable "enable_vault_encryption" {
  description = "Enable vault-based encryption for sensitive resources"
  type        = bool
  default     = true
}

variable "vault_type" {
  description = "Type of vault (DEFAULT or VIRTUAL_PRIVATE)"
  type        = string
  default     = "DEFAULT"
  validation {
    condition     = contains(["DEFAULT", "VIRTUAL_PRIVATE"], var.vault_type)
    error_message = "Vault type must be either DEFAULT or VIRTUAL_PRIVATE."
  }
}

variable "enable_mtls" {
  description = "Enable mutual TLS for database connections"
  type        = bool
  default     = true
}

# Monitoring Configuration

variable "enable_monitoring" {
  description = "Enable monitoring and alerting"
  type        = bool
  default     = true
}

variable "enable_logging" {
  description = "Enable centralized logging"
  type        = bool
  default     = true
}

variable "log_retention_days" {
  description = "Number of days to retain logs"
  type        = number
  default     = 30
  validation {
    condition     = var.log_retention_days >= 7 && var.log_retention_days <= 3653
    error_message = "Log retention must be between 7 and 3653 days."
  }
}

# Analytics Cloud Configuration (Optional)

variable "enable_analytics_cloud" {
  description = "Deploy Oracle Analytics Cloud instance"
  type        = bool
  default     = false
}

variable "analytics_capacity_value" {
  description = "OCPU capacity for Analytics Cloud (only if enabled)"
  type        = number
  default     = 1
  validation {
    condition     = var.analytics_capacity_value >= 1 && var.analytics_capacity_value <= 52
    error_message = "Analytics Cloud capacity must be between 1 and 52 OCPUs."
  }
}

variable "analytics_license_type" {
  description = "License type for Analytics Cloud"
  type        = string
  default     = "LICENSE_INCLUDED"
  validation {
    condition     = contains(["LICENSE_INCLUDED", "BRING_YOUR_OWN_LICENSE"], var.analytics_license_type)
    error_message = "Analytics license type must be either LICENSE_INCLUDED or BRING_YOUR_OWN_LICENSE."
  }
}

# Backup and Disaster Recovery

variable "enable_cross_region_backup" {
  description = "Enable cross-region backup for disaster recovery"
  type        = bool
  default     = false
}

variable "backup_retention_days" {
  description = "Number of days to retain database backups"
  type        = number
  default     = 7
  validation {
    condition     = var.backup_retention_days >= 1 && var.backup_retention_days <= 35
    error_message = "Backup retention must be between 1 and 35 days."
  }
}

# Cost Management

variable "enable_auto_scaling" {
  description = "Enable auto-scaling for cost optimization"
  type        = bool
  default     = true
}

variable "budget_amount" {
  description = "Monthly budget amount in USD for cost alerts"
  type        = number
  default     = 100
  validation {
    condition     = var.budget_amount >= 1
    error_message = "Budget amount must be greater than 0."
  }
}

# Tags

variable "additional_tags" {
  description = "Additional tags to apply to all resources"
  type        = map(string)
  default     = {}
}

variable "cost_center" {
  description = "Cost center for billing allocation"
  type        = string
  default     = ""
}

variable "owner_email" {
  description = "Email of the resource owner"
  type        = string
  default     = ""
  validation {
    condition     = var.owner_email == "" || can(regex("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$", var.owner_email))
    error_message = "Owner email must be a valid email address or empty string."
  }
}

# Feature Flags

variable "enable_gen_ai_agents" {
  description = "Enable Gen AI Agents service (when available)"
  type        = bool
  default     = false
}

variable "enable_apex_application" {
  description = "Deploy APEX application for dashboard"
  type        = bool
  default     = true
}

variable "enable_streaming" {
  description = "Enable streaming service for real-time processing"
  type        = bool
  default     = false
}

# Local values for computed configurations
locals {
  # Merge default and additional tags
  all_tags = merge(
    {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
      CreatedOn   = timestamp()
    },
    var.cost_center != "" ? { CostCenter = var.cost_center } : {},
    var.owner_email != "" ? { Owner = var.owner_email } : {},
    var.additional_tags
  )

  # Compute resource names
  resource_prefix = "${var.project_name}-${var.environment}"

  # Network configuration validation
  subnet_cidrs = [
    var.public_subnet_cidr,
    var.functions_subnet_cidr,
    var.database_subnet_cidr
  ]

  # Validate that subnets are within VCN CIDR
  validate_subnets = [
    for cidr in local.subnet_cidrs :
    cidr if can(cidrnetmask("${cidrhost(var.vcn_cidr_block, 0)}/${split("/", var.vcn_cidr_block)[1]}"))
  ]
}