# Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "rg-scalable-etl"
  location = "westeurope"
}

# Storage Account
resource "azurerm_storage_account" "storage" {
  name                     = "scalableetlstorage"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"
}

# Blob Container (na dane wejściowe)
resource "azurerm_storage_container" "input_data" {
  name                  = "input-data"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}