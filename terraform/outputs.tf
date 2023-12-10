variable "project_id" {
  description = "project id"
}

variable "region" {
  description = "region"
}

variable "gke_config_context" {
  description = "GKE Cluster name. Set it right after first terraform apply."
}

variable "managed_proxy_subnet" {
  description = "Name fo the proxy subnet for the api gateway"
}

output "region" {
  value       = var.region
  description = "GCloud Region"
}

output "project_id" {
  value       = var.project_id
  description = "GCloud Project ID"
}

output "kubernetes_cluster_name" {
  value       = google_container_cluster.primary.name
  description = "GKE Cluster Name"
}

output "kubernetes_cluster_host" {
  value       = google_container_cluster.primary.endpoint
  description = "GKE Cluster Host"
}
