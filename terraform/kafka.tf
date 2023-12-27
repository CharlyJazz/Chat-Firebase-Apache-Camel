data "kubectl_filename_list" "manifests" {
  pattern = "../kafka/k8s/*.yaml"
}

resource "kubectl_manifest" "kafka_and_zookeeper" {
  count     = length(data.kubectl_filename_list.manifests.matches)
  yaml_body = file(element(data.kubectl_filename_list.manifests.matches, count.index))

  depends_on = [
    google_container_cluster.primary,
    google_compute_network.vpc,
    google_compute_subnetwork.subnet,
    google_compute_subnetwork.managed_proxy_subnet,
  ]
}
