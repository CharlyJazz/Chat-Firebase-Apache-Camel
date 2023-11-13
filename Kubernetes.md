# History:

### General:

- minikube tunnel (Open tunnel for loadbalancer services)

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
