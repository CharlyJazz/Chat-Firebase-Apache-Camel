terraform {
  backend "gcs" {
    bucket = "state-bucket-tfstate-chat1"
    prefix = "terraform/state"
  }
}
