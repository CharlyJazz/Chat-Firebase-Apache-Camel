### History

# General

- Install gcloud and login
- https://github.com/hashicorp/learn-terraform-provision-gke-cluster
- https://developer.hashicorp.com/terraform/tutorials/kubernetes/gke
- Set quota `gcloud auth application-default set-quota-project apache-camel-chat-development`
- terraform init - Save variables
- terraform apply - Create resources in GCP

### Configure kubectl

- gcloud container clusters get-credentials $(terraform output -raw kubernetes_cluster_name) --region $(terraform output -raw region)
- https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke

#### Plugins

- brew install kube-ps1
