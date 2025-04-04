data "azurerm_client_config" "current" {}

data "azurerm_subscription" "primary" {}

data "azurerm_resource_group" "rg" {
  name = "rg-${var.project_id}-${var.env}-eau-001"
}

resource "azurerm_storage_account" "sa" {
  name                     = "st${var.project_id}${var.env}eau001"
  resource_group_name      = data.azurerm_resource_group.rg.name
  location                 = data.azurerm_resource_group.rg.location
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
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location
  os_type             = var.asp_os_type
  sku_name            = var.asp_sku_name
}

resource "azurerm_container_app_environment" "containerenv" {
  name                = "cae-${var.project_id}-${var.env}-eau-001"
  location            = data.azurerm_resource_group.rg.location
  resource_group_name = data.azurerm_resource_group.rg.name
}


