# Identity and Access Management Configuration
# Decisioning Agentic Flow - OCI IAM Security

# Dynamic Groups for Service-to-Service Authentication

# Dynamic Group for Functions
resource "oci_identity_dynamic_group" "decisioning_functions" {
  compartment_id = var.tenancy_ocid
  name           = "${local.project_name}-functions-dg"
  description    = "Dynamic group for decisioning agent functions"
  matching_rule  = "ALL {resource.type = 'fnfunc', resource.compartment.id = '${oci_identity_compartment.decisioning_compartment.id}'}"

  freeform_tags = local.common_tags
}

# Dynamic Group for API Gateway
resource "oci_identity_dynamic_group" "decisioning_apigateway" {
  compartment_id = var.tenancy_ocid
  name           = "${local.project_name}-apigateway-dg"
  description    = "Dynamic group for API Gateway"
  matching_rule  = "ALL {resource.type = 'ApiGateway', resource.compartment.id = '${oci_identity_compartment.decisioning_compartment.id}'}"

  freeform_tags = local.common_tags
}

# Dynamic Group for Analytics Cloud (if needed)
resource "oci_identity_dynamic_group" "decisioning_analytics" {
  compartment_id = var.tenancy_ocid
  name           = "${local.project_name}-analytics-dg"
  description    = "Dynamic group for Analytics Cloud instances"
  matching_rule  = "ALL {resource.type = 'analyticsinstance', resource.compartment.id = '${oci_identity_compartment.decisioning_compartment.id}'}"

  freeform_tags = local.common_tags
}

# Policies for Functions
resource "oci_identity_policy" "decisioning_functions_policy" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id
  name           = "${local.project_name}-functions-policy"
  description    = "Policy for decisioning agent functions"

  statements = [
    # Database access
    "Allow dynamic-group ${oci_identity_dynamic_group.decisioning_functions.name} to use autonomous-databases in compartment id ${oci_identity_compartment.decisioning_compartment.id}",

    # Object Storage access
    "Allow dynamic-group ${oci_identity_dynamic_group.decisioning_functions.name} to manage objects in compartment id ${oci_identity_compartment.decisioning_compartment.id} where target.bucket.name='${oci_objectstorage_bucket.decisioning_artifacts.name}'",
    "Allow dynamic-group ${oci_identity_dynamic_group.decisioning_functions.name} to manage objects in compartment id ${oci_identity_compartment.decisioning_compartment.id} where target.bucket.name='${oci_objectstorage_bucket.decisioning_results.name}'",

    # Vault and Key Management
    "Allow dynamic-group ${oci_identity_dynamic_group.decisioning_functions.name} to use vaults in compartment id ${oci_identity_compartment.decisioning_compartment.id}",
    "Allow dynamic-group ${oci_identity_dynamic_group.decisioning_functions.name} to use keys in compartment id ${oci_identity_compartment.decisioning_compartment.id}",

    # Logging
    "Allow dynamic-group ${oci_identity_dynamic_group.decisioning_functions.name} to use log-groups in compartment id ${oci_identity_compartment.decisioning_compartment.id}",
    "Allow dynamic-group ${oci_identity_dynamic_group.decisioning_functions.name} to use log-content in compartment id ${oci_identity_compartment.decisioning_compartment.id}",

    # Monitoring and Metrics
    "Allow dynamic-group ${oci_identity_dynamic_group.decisioning_functions.name} to use metrics in compartment id ${oci_identity_compartment.decisioning_compartment.id}",
    "Allow dynamic-group ${oci_identity_dynamic_group.decisioning_functions.name} to manage management-agents in compartment id ${oci_identity_compartment.decisioning_compartment.id}",

    # Network access for private subnets
    "Allow dynamic-group ${oci_identity_dynamic_group.decisioning_functions.name} to use virtual-network-family in compartment id ${oci_identity_compartment.decisioning_compartment.id}",

    # Analytics Cloud integration (if used)
    "Allow dynamic-group ${oci_identity_dynamic_group.decisioning_functions.name} to use analytics-clouds in compartment id ${oci_identity_compartment.decisioning_compartment.id}"
  ]

  freeform_tags = local.common_tags
}

# Policy for API Gateway
resource "oci_identity_policy" "decisioning_apigateway_policy" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id
  name           = "${local.project_name}-apigateway-policy"
  description    = "Policy for API Gateway to invoke functions"

  statements = [
    # Function invocation
    "Allow dynamic-group ${oci_identity_dynamic_group.decisioning_apigateway.name} to use functions-family in compartment id ${oci_identity_compartment.decisioning_compartment.id}",

    # Logging for API Gateway
    "Allow dynamic-group ${oci_identity_dynamic_group.decisioning_apigateway.name} to use log-groups in compartment id ${oci_identity_compartment.decisioning_compartment.id}",
    "Allow dynamic-group ${oci_identity_dynamic_group.decisioning_apigateway.name} to manage log-content in compartment id ${oci_identity_compartment.decisioning_compartment.id}",

    # Network access
    "Allow dynamic-group ${oci_identity_dynamic_group.decisioning_apigateway.name} to use virtual-network-family in compartment id ${oci_identity_compartment.decisioning_compartment.id}"
  ]

  freeform_tags = local.common_tags
}

# Policy for Analytics Cloud (if needed)
resource "oci_identity_policy" "decisioning_analytics_policy" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id
  name           = "${local.project_name}-analytics-policy"
  description    = "Policy for Analytics Cloud to access data sources"

  statements = [
    # Database access for Analytics Cloud
    "Allow dynamic-group ${oci_identity_dynamic_group.decisioning_analytics.name} to use autonomous-databases in compartment id ${oci_identity_compartment.decisioning_compartment.id}",

    # Object Storage access for data files
    "Allow dynamic-group ${oci_identity_dynamic_group.decisioning_analytics.name} to read objects in compartment id ${oci_identity_compartment.decisioning_compartment.id} where target.bucket.name='${oci_objectstorage_bucket.decisioning_results.name}'",

    # Network access
    "Allow dynamic-group ${oci_identity_dynamic_group.decisioning_analytics.name} to use virtual-network-family in compartment id ${oci_identity_compartment.decisioning_compartment.id}"
  ]

  freeform_tags = local.common_tags
}

# User Groups for Human Access

# Group for Decisioning Administrators
resource "oci_identity_group" "decisioning_admins" {
  compartment_id = var.tenancy_ocid
  name           = "${local.project_name}-admins"
  description    = "Administrators for Decisioning Agentic Flow"

  freeform_tags = local.common_tags
}

# Group for Decisioning Users (Business Users)
resource "oci_identity_group" "decisioning_users" {
  compartment_id = var.tenancy_ocid
  name           = "${local.project_name}-users"
  description    = "Business users for Decisioning Agentic Flow dashboards"

  freeform_tags = local.common_tags
}

# Group for Decisioning Developers
resource "oci_identity_group" "decisioning_developers" {
  compartment_id = var.tenancy_ocid
  name           = "${local.project_name}-developers"
  description    = "Developers for Decisioning Agentic Flow"

  freeform_tags = local.common_tags
}

# Policy for Administrators
resource "oci_identity_policy" "decisioning_admin_policy" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id
  name           = "${local.project_name}-admin-policy"
  description    = "Full administrative access to decisioning resources"

  statements = [
    # Full access to all resources in the compartment
    "Allow group ${oci_identity_group.decisioning_admins.name} to manage all-resources in compartment id ${oci_identity_compartment.decisioning_compartment.id}",

    # Access to manage dynamic groups and policies
    "Allow group ${oci_identity_group.decisioning_admins.name} to manage dynamic-groups in tenancy where target.group.name =~ '${local.project_name}-*'",
    "Allow group ${oci_identity_group.decisioning_admins.name} to manage policies in compartment id ${oci_identity_compartment.decisioning_compartment.id}",

    # Network administration
    "Allow group ${oci_identity_group.decisioning_admins.name} to manage virtual-network-family in compartment id ${oci_identity_compartment.decisioning_compartment.id}",

    # Monitoring and observability
    "Allow group ${oci_identity_group.decisioning_admins.name} to manage alarms in compartment id ${oci_identity_compartment.decisioning_compartment.id}",
    "Allow group ${oci_identity_group.decisioning_admins.name} to manage metrics in compartment id ${oci_identity_compartment.decisioning_compartment.id}",
    "Allow group ${oci_identity_group.decisioning_admins.name} to read announcements in tenancy"
  ]

  freeform_tags = local.common_tags
}

# Policy for Business Users
resource "oci_identity_policy" "decisioning_users_policy" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id
  name           = "${local.project_name}-users-policy"
  description    = "Read-only access to dashboards and results for business users"

  statements = [
    # Read access to analysis results
    "Allow group ${oci_identity_group.decisioning_users.name} to read objects in compartment id ${oci_identity_compartment.decisioning_compartment.id} where target.bucket.name='${oci_objectstorage_bucket.decisioning_results.name}'",

    # Access to Analytics Cloud dashboards
    "Allow group ${oci_identity_group.decisioning_users.name} to use analytics-clouds in compartment id ${oci_identity_compartment.decisioning_compartment.id}",

    # API Gateway access for dashboard data
    "Allow group ${oci_identity_group.decisioning_users.name} to use api-gateway-family in compartment id ${oci_identity_compartment.decisioning_compartment.id}",

    # Basic monitoring access
    "Allow group ${oci_identity_group.decisioning_users.name} to read metrics in compartment id ${oci_identity_compartment.decisioning_compartment.id}",

    # APEX application access (if used)
    "Allow group ${oci_identity_group.decisioning_users.name} to use autonomous-databases in compartment id ${oci_identity_compartment.decisioning_compartment.id}"
  ]

  freeform_tags = local.common_tags
}

# Policy for Developers
resource "oci_identity_policy" "decisioning_developers_policy" {
  compartment_id = oci_identity_compartment.decisioning_compartment.id
  name           = "${local.project_name}-developers-policy"
  description    = "Development access to functions and debugging resources"

  statements = [
    # Functions development access
    "Allow group ${oci_identity_group.decisioning_developers.name} to manage functions-family in compartment id ${oci_identity_compartment.decisioning_compartment.id}",

    # Object storage for artifacts and testing
    "Allow group ${oci_identity_group.decisioning_developers.name} to manage objects in compartment id ${oci_identity_compartment.decisioning_compartment.id}",

    # Database access for testing
    "Allow group ${oci_identity_group.decisioning_developers.name} to use autonomous-databases in compartment id ${oci_identity_compartment.decisioning_compartment.id}",

    # API Gateway management
    "Allow group ${oci_identity_group.decisioning_developers.name} to manage api-gateway-family in compartment id ${oci_identity_compartment.decisioning_compartment.id}",

    # Logging and debugging
    "Allow group ${oci_identity_group.decisioning_developers.name} to manage log-groups in compartment id ${oci_identity_compartment.decisioning_compartment.id}",
    "Allow group ${oci_identity_group.decisioning_developers.name} to manage log-content in compartment id ${oci_identity_compartment.decisioning_compartment.id}",

    # Monitoring for debugging
    "Allow group ${oci_identity_group.decisioning_developers.name} to read metrics in compartment id ${oci_identity_compartment.decisioning_compartment.id}",
    "Allow group ${oci_identity_group.decisioning_developers.name} to manage alarms in compartment id ${oci_identity_compartment.decisioning_compartment.id}",

    # Resource inspection
    "Allow group ${oci_identity_group.decisioning_developers.name} to inspect all-resources in compartment id ${oci_identity_compartment.decisioning_compartment.id}"
  ]

  freeform_tags = local.common_tags
}

# Output the group and dynamic group information
output "functions_dynamic_group_id" {
  description = "OCID of the functions dynamic group"
  value       = oci_identity_dynamic_group.decisioning_functions.id
}

output "apigateway_dynamic_group_id" {
  description = "OCID of the API Gateway dynamic group"
  value       = oci_identity_dynamic_group.decisioning_apigateway.id
}

output "analytics_dynamic_group_id" {
  description = "OCID of the Analytics dynamic group"
  value       = oci_identity_dynamic_group.decisioning_analytics.id
}

output "admin_group_id" {
  description = "OCID of the administrators group"
  value       = oci_identity_group.decisioning_admins.id
}

output "users_group_id" {
  description = "OCID of the business users group"
  value       = oci_identity_group.decisioning_users.id
}

output "developers_group_id" {
  description = "OCID of the developers group"
  value       = oci_identity_group.decisioning_developers.id
}