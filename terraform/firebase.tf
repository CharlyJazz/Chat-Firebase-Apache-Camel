resource "google_project_service" "firestore" {
  project = var.project_id
  service = "firestore.googleapis.com"
}

resource "google_firestore_database" "database" {
  project     = var.project_id
  name        = "(default)"        # Default is (default)
  location_id = "nam5"             # us-central1
  type        = "FIRESTORE_NATIVE" # https://cloud.google.com/datastore/docs/firestore-or-datastore

  depends_on = [google_project_service.firestore]
}

resource "google_service_account" "firestore_service_account" {
  project      = var.project_id
  account_id   = "firestore-service-account"
  display_name = "Firestore Service Account"
}

resource "google_project_iam_member" "firestore_role" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.firestore_service_account.email}"
}

resource "google_service_account_key" "firestore_service_account_key" {
  service_account_id = google_service_account.firestore_service_account.name
  public_key_type    = "TYPE_X509_PEM_FILE"
}


resource "local_file" "firestore_service_acount_chat_messages" {
  filename = "./firestore_service_acount_chat_messages.json"
  content  = base64decode(google_service_account_key.firestore_service_account_key.private_key)
}
