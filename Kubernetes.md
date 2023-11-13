# History:

### General:

- minikube tunnel (Open tunnel for loadbalancer services)

### Auth Microservice Folder:

- docker build -t charlyjazz/auth-microservice:latest .
- docker push charlyjazz/auth-microservice:latest
- kubectl appply -f auth-microservice/k8s

### Chat Microservice Folder: (TO DO)

- docker build -t charlyjazz/<>-microservice:latest .
- docker push charlyjazz/<>-microservice:latest
- kubectl appply -f <>-microservice/k8s
