# History:

### General:

- minikube start --cpus 4 --memory 4000
- minikube tunnel (Open tunnel for loadbalancer services)
- kubectl rollout restart deployment frontend-web-deployment
- kubectl rollout restart deployment aggregated-messages-consumer
- kubectl rollout restart deployment kafka-broker
- kubectl rollout restart deployment chat-microservice

### Auth Microservice Folder:

- docker build -t charlyjazz/auth-microservice:latest .
- docker push charlyjazz/auth-microservice:latest
- kubectl apply -f auth-microservice/k8s

### Chat Microservice Folder: (TO DO)

- docker build -t charlyjazz/chat-microservice:latest .
- docker push charlyjazz/chat-microservice:latest
- kubectl apply -f chat-microservice/k8s
- kubectl exec -it chat-db-5645dbf764-x8kw2 -- /bin/bash (To verify `SELECT release_version FROM system.local;`)
- `CREATE KEYSPACE chat_messages WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};`

### Kafka Folder

- To test the connection:
- `k exec -it kafka-broker-6d896685cd-t9p48 -- /bin/sh`
- Create a topic to test
- `kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic testtopic`
- Verify is a topic is getting messages
- `kafka-console-consumer --bootstrap-server localhost:9092 --topic chat_messages from-beginning`

### Aggregated Messages Consumer

- docker build -t charlyjazz/amc:latest .
- docker push charlyjazz/amc:latest
- kubectl create secret generic firebase-secret --from-file=service_account_key.json=./service_account_key.json

### Apache Camel Service Bus

- docker build -t charlyjazz/apache-camel-microservice:latest .
- docker push charlyjazz/apache-camel-microservice:latest

### Front-End Web

- docker build -t charlyjazz/frontend-web:latest .
- docker push charlyjazz/frontend-web:latest
- kubectl create secret generic frontend-secrets --from-env-file=.env
