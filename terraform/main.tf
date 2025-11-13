# Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "rg-scalable-etl"
  location = "centralus"
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


# Azure SQL Server
resource "azurerm_mssql_server" "sql_server" {
  name                         = "scalableetl-sqlserver"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  version                      = "12.0"
  administrator_login          = "etladmin"
  administrator_login_password = var.sql_admin_password
}

# Azure SQL Database
resource "azurerm_mssql_database" "sql_db" {
  name                = "scalableetl-db"
  server_id           = azurerm_mssql_server.sql_server.id
  sku_name            = "Basic"
  max_size_gb         = 2
  zone_redundant      = false
}
