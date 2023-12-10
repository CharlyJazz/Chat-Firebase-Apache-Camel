terraform {
  backend "gcs" {
    bucket = "state-bucket-tfstate-chat3"
    prefix = "terraform/state"
  }
}
