### History

# General

- Install gcloud and login
- https://github.com/hashicorp/learn-terraform-provision-gke-cluster
- https://developer.hashicorp.com/terraform/tutorials/kubernetes/gke
- Set quota `gcloud auth application-default set-quota-project chat2-405718`
- terraform init - Save variables
- terraform apply - Create resources in GCP
- Super importante correr esto diario gcloud config set project chat2-405718
- gcloud container clusters get-credentials chat2-405718-gke --region us-central1 - kubectl context

### Configure kubectl

- gcloud container clusters get-credentials $(terraform output -raw kubernetes_cluster_name) --region $(terraform output -raw region)
- https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke

#### Plugins

- brew install kube-ps1

### Use kubectl provider

- https://registry.terraform.io/providers/gavinbunney/kubectl/latest/docs/data-sources/kubectl_filename_list#matches

### Create Github Action Pipeline for auth-microservice

- gcloud iam service-accounts create github-action
  gcloud projects add-iam-policy-binding chat1-405416 \
   --member=serviceAccount:github-action@chat1-405416.iam.gserviceaccount.com \
   --role=roles/container.admin
  gcloud projects add-iam-policy-binding chat1-405416 \
   --member=serviceAccount:github-action@chat1-405416.iam.gserviceaccount.com \
   --role=roles/storage.admin
  gcloud projects add-iam-policy-binding chat1-405416 \
   --member=serviceAccount:github-action@chat1-405416.iam.gserviceaccount.com \
   --role=roles/container.clusterViewer

- I used this action: https://github.com/simenandre/setup-gke-gcloud-auth-plugin/blob/main/action.yml
- kubectl create secret generic frontend-secrets --from-env-file=terraform/env.prod
