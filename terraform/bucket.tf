resource "google_storage_bucket" "default" {
  name          = "state-bucket-tfstate-chat1"
  force_destroy = false
  location      = "US"
  storage_class = "STANDARD"

  versioning {
    enabled = true
  }
}
