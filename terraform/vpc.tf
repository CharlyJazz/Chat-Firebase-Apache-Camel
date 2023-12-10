# https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/using_gke_with_terraform
# https://cloud.google.com/kubernetes-engine/docs/how-to/deploying-gateways

# Important:
# The Gateway API is supported on VPC-native clusters only.
# I needs a proxy-only subnet

# VPC main for GLE Cluster
resource "google_compute_network" "vpc" {
  name                    = "${var.project_id}-vpc"
  auto_create_subnetworks = false
}

# Subnet config for VPC-native in GKE Cluster
resource "google_compute_subnetwork" "subnet" {
  name          = "${var.project_id}-subnet"
  region        = var.region
  ip_cidr_range = "10.2.0.0/16"
  network       = google_compute_network.vpc.id
  secondary_ip_range {
    range_name    = "services-range"
    ip_cidr_range = "192.168.1.0/24"
  }

  secondary_ip_range {
    range_name    = "pod-ranges"
    ip_cidr_range = "192.168.64.0/22"
  }
}

# Proxy-Only Subnet
resource "google_compute_subnetwork" "managed_proxy_subnet" {
  role          = "ACTIVE"
  purpose       = "REGIONAL_MANAGED_PROXY"
  name          = var.managed_proxy_subnet
  region        = var.region
  network       = google_compute_network.vpc.name
  ip_cidr_range = "10.0.32.0/20"

  depends_on = [google_compute_network.vpc]
}

# Verify your proxy-only subnet
# gcloud compute networks subnets describe my-gke-proxy-subnet --region=us-central1
