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

### Use kubectl provider

- https://registry.terraform.io/providers/gavinbunney/kubectl/latest/docs/data-sources/kubectl_filename_list#matches

### Save State in GCP Storage (TODO)

- gcloud services enable storage.googleapis.com
- I created a role for my user with all the storage permissions needed
- gcloud iam service-accounts create terraform-admin \
   --description="Service account for Terraform administration" \
   --display-name="Terraform Admin" \
   --project=chat1-405416
- gcloud auth application-default login --project chat1-405416 - https://fabianlee.org/2023/06/11/terraform-fixing-error-querying-cloud-storage-failed-storage-bucket-doesnt-exist/

### Create Github Action Pipeline for auth-microservice (TODO)
