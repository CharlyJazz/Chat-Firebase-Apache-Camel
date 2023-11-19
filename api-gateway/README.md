# API Gateway for Auth and Chat Microservices

Resource: https://cloud.google.com/kubernetes-engine/docs/how-to/deploying-gateways

## Standard Config

To enable the Gateway API on a existing VPC-native GKE cluster, use the following:

- gcloud container clusters update chat1-405416-gke \
  --gateway-api=standard \
  --location=us-central1

- Confirm gcloud container clusters describe chat1-405416-gke \
   --location=us-central1 \
   --format json

- Shoud contains

```json
"networkConfig": {
  ...
  "gatewayApiConfig": {
    "channel": "CHANNEL_STANDARD"
  },
  ...
},
```

- kubectl get gatewayclass should return the GatewayClass

Configure a proxy-only subnet
You must configure a proxy-only subnet before you create a Gateway that uses an internal Application Load Balancer. Each region of a VPC in which you use internal Application Load Balancers must have a proxy-only subnet. This subnet provides internal IP addresses to the load balancer proxies.

Create a proxy-only subnet:

- gcloud compute networks subnets create proxy-only-subnet-api-gateway \
   --purpose=REGIONAL_MANAGED_PROXY \
   --role=ACTIVE \
   --region=us-central1 \
   --network=chat1-405416-vpc \
   --range=10.129.0.0/23

```log
NAME                           REGION       NETWORK           RANGE          STACK_TYPE  IPV6_ACCESS_TYPE  INTERNAL_IPV6_PREFIX  EXTERNAL_IPV6_PREFIX
proxy-only-subnet-api-gateway  us-central1  chat1-405416-vpc  10.129.0.0/23
```

Apply gateway

```bash
kubectl apply -f api-gateway/gateway.yaml
```

Apply Auth http route

```bash
kubectl apply -f api-gateway/auth-http-route.yaml
```

kubectl describe gateways global-external-managed-chat-api-gateway

kubectl describe healthcheckpolicy auth-healthcheck

kubectl describe httproute auth-http-route
