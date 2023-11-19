# kubectl create secret generic firebase-secret -from-file=service_account_key.json=./firestore_service_account.json
# Needed by the consumer server
resource "kubernetes_secret" "firebase_secret" {
  metadata {
    name = "firebase-secret"
  }

  data = {
    "service_account_key.json" = file("${path.module}/firestore_service_account.json")
  }
}

# kubectl create secret generic frontend-secrets --from-env-file=.env
# Needed by the front end
# I don't know how to translate it to terraform...
