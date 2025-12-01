variable "resource_group_name" {
  type        = string
  description = "Nazwa grupy zasobów"
}


variable "location" {
  type        = string
  default     = "centralus"
  description = "Region Azure"
}


variable "blob_storage_id" {
  type        = string
  description = "ID konta Storage z Blobami"
}


variable "airflow_webhook_url" {
  type        = string
  description = "Adres endpointu webhooka Airflow"
}