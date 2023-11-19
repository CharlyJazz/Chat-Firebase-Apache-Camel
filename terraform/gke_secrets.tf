resource "kubernetes_secret" "firebase_secret" {
  metadata {
    name = "firebase-secret"
  }

  data = {
    "service_account_key.json" = file("${path.module}/firestore_service_account.json")
  }
}

# I don't know how to do kubectl create secret generic frontend-secrets --from-env-file=.env
