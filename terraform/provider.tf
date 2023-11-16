provider "google" {
  project = var.project_id
  region  = var.region
}


provider "kubectl" {
  load_config_file = true
}
