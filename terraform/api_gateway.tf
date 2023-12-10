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

data "kubectl_filename_list" "api_gateway_manifests" {
  pattern = "../api-gateway/*.yaml"
}

resource "kubectl_manifest" "api_gateway" {
  count     = length(data.kubectl_filename_list.api_gateway_manifests.matches)
  yaml_body = file(element(data.kubectl_filename_list.api_gateway_manifests.matches, count.index))

  depends_on = [
    google_container_cluster.primary,
    google_compute_network.vpc,
    google_compute_subnetwork.subnet,
    google_compute_subnetwork.managed_proxy_subnet,
  ]
}
