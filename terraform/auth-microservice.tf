data "kubectl_filename_list" "manifests" {
  pattern = "../auth-microservice/k8s/*.yaml"
}

resource "kubectl_manifest" "auth_microservice" {
  count     = length(data.kubectl_filename_list.manifests.matches)
  yaml_body = file(element(data.kubectl_filename_list.manifests.matches, count.index))
}
