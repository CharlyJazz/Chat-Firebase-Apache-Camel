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

output "firestore_service_account_json" {
  value = jsonencode({
    type                        = "service_account",
    project_id                  = var.project_id,
    private_key_id              = google_service_account_key.firestore_service_account_key.name,
    private_key                 = base64decode(google_service_account_key.firestore_service_account_key.private_key),
    client_email                = google_service_account.firestore_service_account.email,
    client_id                   = google_service_account.firestore_service_account.name,
    auth_uri                    = "https://accounts.google.com/o/oauth2/auth",
    token_uri                   = "https://oauth2.googleapis.com/token",
    auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs",
    client_x509_cert_url        = "https://www.googleapis.com/robot/v1/metadata/x509/${google_service_account.firestore_service_account.email}"
  })
  sensitive = true
}

