data "azurerm_client_config" "current" {}

data "azurerm_subscription" "primary" {}

data "azurerm_resource_group" "rg" {
  name     = "rg-${var.project_id}-${var.env}-eau-001"
  location = "australiaeast"
}

resource "azurerm_storage_account" "sa" {
  name                     = "st${var.project_id}${var.env}eau001"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_table" "items" {
  name                 = "items"
  storage_account_name = azurerm_storage_account.sa.name
}

resource "azurerm_storage_table" "lists" {
  name                 = "lists"
  storage_account_name = azurerm_storage_account.sa.name
}

resource "azurerm_service_plan" "asp" {
  name                = "asp-${var.project_id}-${var.env}-eau-001"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = var.asp_os_type
  sku_name            = var.asp_sku_name
}

# Create the web app, pass in the App Service Plan ID
# resource "azurerm_linux_web_app" "webapp" {
#   name                = var.app_name
#   location            = azurerm_resource_group.rg.location
#   resource_group_name = azurerm_resource_group.rg.name
#   service_plan_id     = azurerm_service_plan.asp.id
#   https_only          = true
#   site_config {

#   }
# }

# resource "azurerm_role_assignment" "table-contrib" {
#   scope                = azurerm_storage_account.sa.id
#   role_definition_name = "Storage Table Data Contributor"
#   principal_id         = var.user_object_id
# }
