provider "google" {
  project = var.project_id
  region  = var.region
}


provider "kubectl" {
  load_config_file = true
}

provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "gke_chat1-405416_us-central1_chat1-405416-gke"
}
