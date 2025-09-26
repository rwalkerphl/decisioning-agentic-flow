# Oracle Cloud Infrastructure Terraform Configuration
# Decisioning Agentic Flow - Production Deployment

terraform {
  required_version = ">= 1.0"
  required_providers {
    oci = {
      source  = "oracle/oci"
      version = ">= 4.120.0"
    }
  }
}

# Variables
variable "tenancy_ocid" {
  description = "OCID of the tenancy"
  type        = string
}

variable "compartment_ocid" {
  description = "OCID of the compartment"
  type        = string
}

variable "region" {
  description = "OCI region"
  type        = string
  default     = "us-ashburn-1"
}

variable "db_admin_password" {
  description = "Admin password for Autonomous Database"
  type        = string
  sensitive   = true
}

variable "environment" {
  description = "Environment name (dev/test/prod)"
  type        = string
  default     = "prod"
}

# Provider configuration
provider "oci" {
  tenancy_ocid = var.tenancy_ocid
  region       = var.region
}

# Data sources
data "oci_identity_availability_domains" "ads" {
  compartment_id = var.tenancy_ocid
}

data "oci_objectstorage_namespace" "namespace" {
  compartment_id = var.compartment_ocid
}

# Local values
locals {
  project_name = "decisioning-agentic-flow"
  common_tags = {
    Project     = local.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
    CreatedOn   = timestamp()
  }
}

# Compartment for decisioning agents
resource "oci_identity_compartment" "decisioning_compartment" {
  compartment_id = var.compartment_ocid
  description    = "Compartment for Decisioning Agentic Flow Resources"
  name           = "${local.project_name}-${var.environment}"

  freeform_tags = local.common_tags
}

# Virtual Cloud Network
resource "oci_core_vcn" "decisioning_vcn" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id
  cidr_blocks    = ["10.0.0.0/16"]
  display_name   = "${local.project_name}-vcn"
  dns_label      = "decisionvcn"

  freeform_tags = local.common_tags
}

# Internet Gateway
resource "oci_core_internet_gateway" "decisioning_igw" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id
  vcn_id         = oci_core_vcn.decisioning_vcn.id
  display_name   = "${local.project_name}-igw"
  enabled        = true

  freeform_tags = local.common_tags
}

# NAT Gateway for private subnets
resource "oci_core_nat_gateway" "decisioning_nat" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id
  vcn_id         = oci_core_vcn.decisioning_vcn.id
  display_name   = "${local.project_name}-nat"

  freeform_tags = local.common_tags
}

# Service Gateway for Oracle services
resource "oci_core_service_gateway" "decisioning_sg" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id
  vcn_id         = oci_core_vcn.decisioning_vcn.id
  display_name   = "${local.project_name}-sg"

  services {
    service_id = data.oci_core_services.all_services.services[0].id
  }

  freeform_tags = local.common_tags
}

data "oci_core_services" "all_services" {
  filter {
    name   = "name"
    values = ["All .* Services In Oracle Services Network"]
    regex  = true
  }
}

# Route Table for Public Subnet
resource "oci_core_route_table" "public_route_table" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id
  vcn_id         = oci_core_vcn.decisioning_vcn.id
  display_name   = "${local.project_name}-public-rt"

  route_rules {
    destination       = "0.0.0.0/0"
    network_entity_id = oci_core_internet_gateway.decisioning_igw.id
    description       = "Default route to Internet Gateway"
  }

  freeform_tags = local.common_tags
}

# Route Table for Private Subnets
resource "oci_core_route_table" "private_route_table" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id
  vcn_id         = oci_core_vcn.decisioning_vcn.id
  display_name   = "${local.project_name}-private-rt"

  route_rules {
    destination       = "0.0.0.0/0"
    network_entity_id = oci_core_nat_gateway.decisioning_nat.id
    description       = "Default route to NAT Gateway"
  }

  route_rules {
    destination       = data.oci_core_services.all_services.services[0].cidr_block
    network_entity_id = oci_core_service_gateway.decisioning_sg.id
    description       = "Route to Oracle Services"
  }

  freeform_tags = local.common_tags
}

# Security List for Public Subnet
resource "oci_core_security_list" "public_security_list" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id
  vcn_id         = oci_core_vcn.decisioning_vcn.id
  display_name   = "${local.project_name}-public-sl"

  # Ingress Rules
  ingress_security_rules {
    protocol    = "6" # TCP
    source      = "0.0.0.0/0"
    description = "Allow HTTPS traffic"

    tcp_options {
      min = 443
      max = 443
    }
  }

  ingress_security_rules {
    protocol    = "6" # TCP
    source      = "0.0.0.0/0"
    description = "Allow HTTP traffic"

    tcp_options {
      min = 80
      max = 80
    }
  }

  # Egress Rules
  egress_security_rules {
    protocol    = "all"
    destination = "0.0.0.0/0"
    description = "Allow all outbound traffic"
  }

  freeform_tags = local.common_tags
}

# Security List for Private Subnets
resource "oci_core_security_list" "private_security_list" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id
  vcn_id         = oci_core_vcn.decisioning_vcn.id
  display_name   = "${local.project_name}-private-sl"

  # Ingress Rules - Allow traffic from VCN
  ingress_security_rules {
    protocol    = "all"
    source      = "10.0.0.0/16"
    description = "Allow all traffic from VCN"
  }

  # Egress Rules
  egress_security_rules {
    protocol    = "all"
    destination = "0.0.0.0/0"
    description = "Allow all outbound traffic"
  }

  freeform_tags = local.common_tags
}

# Public Subnet for API Gateway
resource "oci_core_subnet" "public_subnet" {
  compartment_id             = oci_identity_compartment.decisioning_compartment.id
  vcn_id                     = oci_core_vcn.decisioning_vcn.id
  cidr_block                 = "10.0.1.0/24"
  display_name               = "${local.project_name}-public-subnet"
  dns_label                  = "publicsub"
  availability_domain        = data.oci_identity_availability_domains.ads.availability_domains[0].name

  route_table_id             = oci_core_route_table.public_route_table.id
  security_list_ids          = [oci_core_security_list.public_security_list.id]
  prohibit_public_ip_on_vnic = false

  freeform_tags = local.common_tags
}

# Private Subnet for Functions
resource "oci_core_subnet" "functions_subnet" {
  compartment_id             = oci_identity_compartment.decisioning_compartment.id
  vcn_id                     = oci_core_vcn.decisioning_vcn.id
  cidr_block                 = "10.0.2.0/24"
  display_name               = "${local.project_name}-functions-subnet"
  dns_label                  = "functsub"
  availability_domain        = data.oci_identity_availability_domains.ads.availability_domains[0].name

  route_table_id             = oci_core_route_table.private_route_table.id
  security_list_ids          = [oci_core_security_list.private_security_list.id]
  prohibit_public_ip_on_vnic = true

  freeform_tags = local.common_tags
}

# Private Subnet for Database
resource "oci_core_subnet" "database_subnet" {
  compartment_id             = oci_identity_compartment.decisioning_compartment.id
  vcn_id                     = oci_core_vcn.decisioning_vcn.id
  cidr_block                 = "10.0.3.0/24"
  display_name               = "${local.project_name}-database-subnet"
  dns_label                  = "dbsub"
  availability_domain        = data.oci_identity_availability_domains.ads.availability_domains[1].name

  route_table_id             = oci_core_route_table.private_route_table.id
  security_list_ids          = [oci_core_security_list.private_security_list.id]
  prohibit_public_ip_on_vnic = true

  freeform_tags = local.common_tags
}

# Autonomous Database
resource "oci_database_autonomous_database" "decisioning_db" {
  compartment_id           = oci_identity_compartment.decisioning_compartment.id
  cpu_core_count          = 1
  data_storage_size_in_tbs = 1
  db_name                 = "DECISIONDB"
  display_name            = "${local.project_name}-adb"
  admin_password          = var.db_admin_password

  # Serverless configuration for cost optimization
  is_auto_scaling_enabled = true
  is_serverless           = true

  # Security configuration
  subnet_id                        = oci_core_subnet.database_subnet.id
  nsg_ids                         = [oci_core_network_security_group.database_nsg.id]
  is_mtls_connection_required     = true

  # Backup configuration
  is_auto_scaling_for_storage_enabled = true

  freeform_tags = local.common_tags
}

# Network Security Group for Database
resource "oci_core_network_security_group" "database_nsg" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id
  vcn_id         = oci_core_vcn.decisioning_vcn.id
  display_name   = "${local.project_name}-db-nsg"

  freeform_tags = local.common_tags
}

# Database NSG Rules
resource "oci_core_network_security_group_security_rule" "db_ingress_1521" {
  network_security_group_id = oci_core_network_security_group.database_nsg.id
  direction                 = "INGRESS"
  protocol                  = "6"
  source                    = "10.0.0.0/16"
  description               = "Allow Oracle DB connections from VCN"

  tcp_options {
    destination_port_range {
      min = 1521
      max = 1521
    }
  }
}

# Object Storage Bucket for artifacts
resource "oci_objectstorage_bucket" "decisioning_artifacts" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id
  name           = "${local.project_name}-artifacts"
  namespace      = data.oci_objectstorage_namespace.namespace.namespace

  # Security configuration
  public_access_type = "NoPublicAccess"
  versioning         = "Enabled"

  # Storage tier for cost optimization
  storage_tier = "Standard"

  freeform_tags = local.common_tags
}

# Object Storage Bucket for results
resource "oci_objectstorage_bucket" "decisioning_results" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id
  name           = "${local.project_name}-results"
  namespace      = data.oci_objectstorage_namespace.namespace.namespace

  # Security configuration
  public_access_type = "NoPublicAccess"
  versioning         = "Enabled"

  # Lifecycle policy for cost management
  retention_rules {
    display_name = "Delete after 1 year"
    duration {
      time_amount = 365
      time_unit   = "DAYS"
    }
  }

  freeform_tags = local.common_tags
}

# Functions Application
resource "oci_functions_application" "decisioning_app" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id
  display_name   = "${local.project_name}-app"
  subnet_ids     = [oci_core_subnet.functions_subnet.id]

  # Configuration for the application
  config = {
    "DB_CONNECTION_STRING" = oci_database_autonomous_database.decisioning_db.connection_strings[0].high
    "STORAGE_NAMESPACE"    = data.oci_objectstorage_namespace.namespace.namespace
    "ARTIFACTS_BUCKET"     = oci_objectstorage_bucket.decisioning_artifacts.name
    "RESULTS_BUCKET"       = oci_objectstorage_bucket.decisioning_results.name
  }

  freeform_tags = local.common_tags
}

# API Gateway
resource "oci_apigateway_gateway" "decisioning_gateway" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id
  endpoint_type  = "PUBLIC"
  display_name   = "${local.project_name}-gateway"
  subnet_id      = oci_core_subnet.public_subnet.id

  freeform_tags = local.common_tags
}

# Vault for Key Management
resource "oci_kms_vault" "decisioning_vault" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id
  display_name   = "${local.project_name}-vault"
  vault_type     = "DEFAULT"

  freeform_tags = local.common_tags
}

# Master Encryption Key
resource "oci_kms_key" "decisioning_key" {
  compartment_id      = oci_identity_compartment.decisioning_compartment.id
  display_name        = "${local.project_name}-master-key"
  management_endpoint = oci_kms_vault.decisioning_vault.management_endpoint

  key_shape {
    algorithm = "AES"
    length    = 256
  }

  freeform_tags = local.common_tags
}

# Outputs
output "compartment_id" {
  description = "OCID of the decisioning compartment"
  value       = oci_identity_compartment.decisioning_compartment.id
}

output "vcn_id" {
  description = "OCID of the VCN"
  value       = oci_core_vcn.decisioning_vcn.id
}

output "database_connection_string" {
  description = "Database connection string"
  value       = oci_database_autonomous_database.decisioning_db.connection_strings[0].high
  sensitive   = true
}

output "api_gateway_hostname" {
  description = "API Gateway hostname"
  value       = oci_apigateway_gateway.decisioning_gateway.hostname
}

output "functions_app_id" {
  description = "Functions application OCID"
  value       = oci_functions_application.decisioning_app.id
}

output "artifacts_bucket" {
  description = "Artifacts bucket name"
  value       = oci_objectstorage_bucket.decisioning_artifacts.name
}

output "results_bucket" {
  description = "Results bucket name"
  value       = oci_objectstorage_bucket.decisioning_results.name
}

output "vault_id" {
  description = "Vault OCID"
  value       = oci_kms_vault.decisioning_vault.id
}

output "master_key_id" {
  description = "Master encryption key OCID"
  value       = oci_kms_key.decisioning_key.id
}