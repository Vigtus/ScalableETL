##############################################
# main.tf – główny plik infrastruktury
##############################################

##############################################
# Resource Group
##############################################

resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

##############################################
# Azure Storage Account
##############################################

resource "azurerm_storage_account" "storage" {
  name                     = "scalableetlstorage"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  https_traffic_only_enabled = true
  min_tls_version            = "TLS1_2"

  blob_properties {
    versioning_enabled = false
  }

    lifecycle {
    prevent_destroy = true
  }
}


##############################################
# Event Grid
##############################################

resource "azurerm_eventgrid_system_topic" "etl_topic" {
  name                   = "etl-event-topic"
  resource_group_name    = azurerm_resource_group.rg.name
  location               = azurerm_resource_group.rg.location
  source_arm_resource_id = azurerm_storage_account.storage.id
  topic_type             = "Microsoft.Storage.StorageAccounts"
}

/*
resource "azurerm_eventgrid_system_topic_event_subscription" "etl_subscription" {
  name                  = "etl-event-subscription"
  resource_group_name   = azurerm_resource_group.rg.name
  system_topic          = azurerm_eventgrid_system_topic.etl_topic.name
  event_delivery_schema = "EventGridSchema"

  included_event_types = [
    "Microsoft.Storage.BlobCreated"
  ]

  webhook_endpoint {
    url = "https://airflow-api.azurecontainerapps.io/api/v1/dags/etl_pipeline/dagRuns"
  }

}
*/


##############################################
# AKS – Azure Kubernetes Service
##############################################

resource "azurerm_kubernetes_cluster" "aks_cluster" {
  name                = "etl-aks-cluster"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "etl-aks"

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_B4ms"
  }

  identity {
    type = "SystemAssigned"
  }

  tags = {
    environment = "dev"
    project     = "ScalableETL"
  }
}

