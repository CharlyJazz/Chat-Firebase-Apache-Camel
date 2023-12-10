resource "google_service_account" "github_action" {
  account_id   = "github-action"
  display_name = "GitHub Action Service Account"
}

resource "google_project_iam_binding" "container_admin" {
  project = var.project_id
  role    = "roles/container.admin"

  members = [
    "serviceAccount:${google_service_account.github_action.email}",
  ]

  depends_on = [google_service_account.github_action]
}

resource "google_project_iam_binding" "storage_admin" {
  project = var.project_id
  role    = "roles/storage.admin"

  members = [
    "serviceAccount:${google_service_account.github_action.email}",
  ]
  depends_on = [google_service_account.github_action]
}

resource "google_project_iam_binding" "cluster_viewer" {
  project = var.project_id
  role    = "roles/container.clusterViewer"

  members = [
    "serviceAccount:${google_service_account.github_action.email}",
  ]

  depends_on = [google_service_account.github_action]
}
