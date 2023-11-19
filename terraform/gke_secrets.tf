resource "kubernetes_secret" "firebase_secret" {
  metadata {
    name = "firebase-secret"
  }

  data = {
    "service_account_key.json" = file("${path.module}/firestore_service_account.json")
  }
}

# resource "kubernetes_secret" "frontend_secrets" {
#   metadata {
#     name = "frontend-secrets"
#   }

#   data = {
#     for k, v in tomap({ for s in split("\n", trimspace(file("${path.module}/.env"))) : split("=", s)[0] => split("=", s)[1] }) : k => v
#   }
# }
