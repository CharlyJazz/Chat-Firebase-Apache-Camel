terraform {
  backend "gcs" {
    bucket = "state-bucket-tfstate-chat1"
    prefix = "terraform/state"
    # credentials = "/Users/carlosazuaje/.config/gcloud/application_default_credentials.json"
    # impersonate_service_account = "terraform-admin@chat1-405416.iam.gserviceaccount.com"
  }
}
