resource "google_storage_bucket" "default" {
  # Only comment the count attribute if
  # you did not create the bucket manually in GCP
  # In that case you should comment the backend config
  # for the first apply
  count         = 0
  name          = "state-bucket-tfstate-chat1"
  force_destroy = false
  location      = "US"
  storage_class = "STANDARD"

  versioning {
    enabled = true
  }
}
