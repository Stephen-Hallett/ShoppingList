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

resource "azurerm_storage_table" "users" {
  name                 = "users"
  storage_account_name = azurerm_storage_account.sa.name
}

resource "azurerm_storage_table" "items" {
  name                 = "items"
  storage_account_name = azurerm_storage_account.sa.name
}

resource "azurerm_storage_table" "lists" {
  name                 = "lists"
  storage_account_name = azurerm_storage_account.sa.name
}

resource "azurerm_storage_table" "logs" {
  name                 = "logs"
  storage_account_name = azurerm_storage_account.sa.name
}

resource "azurerm_container_app_environment" "cae" {
  name                = "cae-${var.project_id}-${var.env}-eau-001"
  location            = data.azurerm_resource_group.rg.location
  resource_group_name = data.azurerm_resource_group.rg.name
}

resource "azurerm_container_app" "backend" {
  name                         = "ca-${var.project_id}-${var.env}-eau-backend"
  container_app_environment_id = azurerm_container_app_environment.cae.id
  resource_group_name          = data.azurerm_resource_group.rg.name
  revision_mode                = "Single"

  secret {
    name  = "ghcr-token"
    value = var.ghcr-token
  }

  ingress {
    external_enabled           = false
    allow_insecure_connections = false
    target_port                = 8000
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    container {
      name   = "backend"
      image  = "ghcr.io/stephen-hallett/backend:latest"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "TABLE_CONNECTION"
        value = azurerm_storage_account.sa.primary_connection_string
      }

      env {
        name  = "HASH_KEY"
        value = var.hash_key
      }
    }
  }

  registry {
    server               = "ghcr.io"
    username             = "stephen-hallett"
    password_secret_name = "ghcr-token"
  }
}

resource "azurerm_container_app" "frontend" {
  depends_on                   = [azurerm_container_app.backend]
  name                         = "ca-${var.project_id}-${var.env}-eau-frontend"
  container_app_environment_id = azurerm_container_app_environment.cae.id
  resource_group_name          = data.azurerm_resource_group.rg.name
  revision_mode                = "Single"

  secret {
    name  = "ghcr-token"
    value = var.ghcr-token
  }


  ingress {
    external_enabled = true
    target_port      = 6969
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }


  template {
    container {
      name   = "frontend"
      image  = "ghcr.io/stephen-hallett/frontend:latest"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "BACKEND_ENDPOINT"
        value = "https://${azurerm_container_app.backend.name}.internal.${azurerm_container_app_environment.cae.default_domain}"
      }

      env {
        name  = "HASH_KEY"
        value = var.hash_key
      }
    }
  }

  registry {
    server               = "ghcr.io"
    username             = "stephen-hallett"
    password_secret_name = "ghcr-token"
  }
}

resource "azurerm_storage_share" "weaviate_data" {
  name               = "weaviatedata"
  storage_account_id = azurerm_storage_account.sa.id
  quota              = 5 # in GB — increase as needed
  enabled_protocol   = "SMB"
}


resource "azurerm_container_app" "weaviate" {
  name                         = "ca-${var.project_id}-${var.env}-eau-weaviate"
  container_app_environment_id = azurerm_container_app_environment.cae.id
  resource_group_name          = data.azurerm_resource_group.rg.name
  revision_mode                = "Single"

  ingress {
    external_enabled           = false
    allow_insecure_connections = false
    target_port                = 8080
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    container {
      name   = "weaviate"
      image  = "semitechnologies/weaviate:latest"
      cpu    = 0.5
      memory = "1.0Gi"

      env {
        name  = "QUERY_DEFAULTS_LIMIT"
        value = "25"
      }

      env {
        name  = "AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED"
        value = "true"
      }

      env {
        name  = "PERSISTENCE_DATA_PATH"
        value = "/var/lib/weaviate"
      }

      env {
        name  = "ENABLE_MODULES"
        value = ""
      }

      env {
        name  = "DEFAULT_VECTORIZER_MODULE"
        value = "none"
      }

      volume_mounts {
        name = "weaviate-volume"
        path = "/var/lib/weaviate"
      }
    }

    volume {
      name = "weaviate-volume"

      storage_name = azurerm_storage_share.weaviate_data.name
      storage_type = "AzureFile"
    }
  }
}
