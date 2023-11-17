data "kubectl_filename_list" "manifests" {
  pattern = "../kafka/k8s/*.yaml"
}

resource "kubectl_manifest" "kafka_and_zookeeper" {
  count     = length(data.kubectl_filename_list.manifests.matches)
  yaml_body = file(element(data.kubectl_filename_list.manifests.matches, count.index))
}
