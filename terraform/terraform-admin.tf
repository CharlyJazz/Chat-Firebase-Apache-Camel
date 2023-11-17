data "google_service_account" "target_service_account" {
  account_id = "terraform-admin"
  project    = var.project_id
}

output "target_service_account_email" {
  value = data.google_service_account.target_service_account.email
}

resource "google_service_account" "impersonating_service_account" {
  account_id   = "impersonator-account"
  display_name = "Impersonating Service Account"
}

resource "google_project_iam_member" "impersonator_permissions" {
  project = var.project_id
  role    = "roles/iam.serviceAccountTokenCreator"
  member  = "serviceAccount:${google_service_account.impersonating_service_account.email}"
  condition {
    title       = "impersonation"
    description = "Allows impersonation of the target service account"
    expression  = "resource.name == 'projects/-/serviceAccounts/${data.google_service_account.target_service_account.email}'"
  }
}

resource "google_project_iam_member" "storage_admin_permission" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${data.google_service_account.target_service_account.email}"
}

# Still needs some other permissions to use this in bucket state config
# "message": "Permission 'iam.serviceAccounts.getAccessToken' denied on resource (or it may not exist).",
