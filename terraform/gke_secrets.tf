resource "kubernetes_secret" "firebase_secret" {
  metadata {
    name = "firebase-secret"
  }

  data = {
    "service_account_key.json" = file("${path.module}/firestore_service_account.json")
  }
}

resource "kubernetes_secret" "frontend_secrets" {
  metadata {
    name = "frontend-secrets"
  }

  data = {
    "file.txt" = file("${path.module}/env.prod")
  }
}
