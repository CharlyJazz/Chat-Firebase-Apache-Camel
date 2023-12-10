
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
