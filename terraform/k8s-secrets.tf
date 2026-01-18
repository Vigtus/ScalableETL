resource "kubernetes_namespace" "airflow" {
  metadata {
    name = "airflow"
  }
}
resource "kubernetes_secret" "azure_storage" {
  metadata {
    name      = "azure-storage-secret"
    namespace = kubernetes_namespace.airflow.metadata[0].name
  }

  data = {
    AZURE_STORAGE_ACCOUNT = azurerm_storage_account.storage.name
    AZURE_STORAGE_KEY     = azurerm_storage_account.storage.primary_access_key
  }

  type = "Opaque"
}
