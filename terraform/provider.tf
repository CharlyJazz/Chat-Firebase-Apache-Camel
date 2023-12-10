provider "google" {
  project = var.project_id
  region  = var.region
}


provider "kubectl" {
  load_config_file = true
}

provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = var.gke_config_context
}
