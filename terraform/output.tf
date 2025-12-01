##############################################
# OUTPUTS
##############################################

# Zwraca ID i nazwę system topic (zamiast endpoint)
output "eventgrid_system_topic_id" {
  value = azurerm_eventgrid_system_topic.etl_topic.id
}

output "eventgrid_system_topic_name" {
  value = azurerm_eventgrid_system_topic.etl_topic.name
}

output "aks_cluster_name" {
  description = "Nazwa klastra AKS"
  value       = azurerm_kubernetes_cluster.aks_cluster.name
}

output "resource_group_name" {
  description = "Nazwa grupy zasobów"
  value       = azurerm_resource_group.rg.name
}