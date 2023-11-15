#!/bin/bash

# Exit script on any error
set -e

# List of directories containing Kubernetes configurations
declare -a k8s_dirs=(
    "kafka/k8s"
    "chat-microservice/k8s"
    "apache-camel-service-bus/k8s"
    "auth-microservice/k8s"
    "aggregated-messages-consumer/k8s"
    "frontend-web/k8s"
)

kubectl create secret generic firebase-secret --from-file=service_account_key.json=./aggregated-messages-consumer/service_account_key.json
kubectl create secret generic frontend-secrets --from-env-file=.env

# Function to apply Kubernetes configurations
apply_configs() {
    for dir in "${k8s_dirs[@]}"
    do
        echo "Applying Kubernetes configurations in $dir"
        kubectl apply -f $dir
    done
}

# Execute the function
apply_configs

echo "Kubernetes configurations applied successfully."
