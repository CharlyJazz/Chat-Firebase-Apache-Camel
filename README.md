# Realtime Chat using Apache Camel, Cassandra and Firestore

Chat system architecture leveraging Apache Camel's aggregation pattern. This architecture incorporates a mechanism to buffer incoming messages for a specific timeout duration, measured in seconds. Subsequently, the system aggregates these buffered messages based on their unique chat IDs. The purpose of this aggregation step is to optimize Firestore usage by reducing the number of write operations. The aggregated message data is then efficiently dispatched to Firestore, with the primary goal of minimizing Firestore billing costs.

The chat pagination utilize Cassandra instead of Firestore. This strategic decision serves a dual purpose:

- It alleviates the load on Firestore's read operations
- Harnesses the inherent advantages of Cassandra for optimizing the partitioning using the `chat_id` as the partition key.

[![Demo Video](https://github.com/CharlyJazz/Chat-Firebase-Apache-Camel/assets/12489333/79618746-367e-474c-bc16-07b2da7693dc)](https://user-images.githubusercontent.com/12489333/273462854-31d8e470-4169-4ac7-a397-327987f885f3.mov)


The next content of this paper explain the sistem using a Architectural Map Features approach.

## Problem

Create a chat that makes spam difficult, optimizes availability, and manages reading and writing operations in Firestore to reduce expenses.

## The Features are:

1. Create User
2. Login
3. Get the list of users
4. User send messages to other user
5. Create a new chat room between to users: The user A will find the user B and start a chat.
6. User get realtime message updating

## Mapping Features to Architectural Components

- Feature Mapping 1: The users management and authentication (features 1, 2 and 3) will be handle by a microservice called **Auth Microservice**
  - The microservice will have a store.
  - The microservice will use JWT for the Authentication.
- Feature Mapping 2. Chat creation and Message creation/retrieving (features 4 and 5) will be handle by a microservice called **Chat Microservice**
  - The microservice will have a store.
- Feature Mapping 3. **Chat Microservice** will take care of sending the messages to a queue proccesing in other to satisfy the feature 6

## Realtime solution to satisfy feature 6

Instead of using Firestore or another cloud-based solution for a complete chat solution, we are going to use Firestore only to update the UI with the `aggregated news messages`.

The `aggregated news messages` refers to a set of messages sent by a user. Instead of displaying each message one by one, there will be a server that will group all the related messages sent by a user into a list. This list will then be retrieved for the chat..

![Architecture diagram](https://user-images.githubusercontent.com/12489333/166072172-482250b2-93f7-4787-9652-3826054cc817.png)

This is how it looks like in Firestore:

![Firestore Image of the messages](https://user-images.githubusercontent.com/12489333/269821581-987ba838-92c0-493a-bc08-5352205597cf.png)

## Architectural Components to explicit implementation details

- The auth and chat microservices will be written in Python using FastAPI.
- The message aggregating process will be handled by Apache Camel using SpringBoot on Java.
- User databases will be Postgres.
- Chat database will be Cassandra to create a fast partition for each chat and fast pagination based on Time UUID.
- The `aggregated news messages` will be saved into Firestore and only will retrieve for realtime
- Chat messages queue processing will be handle by Kafka using a Python Kafka Consumer.
- Auth validation in Python microservices will be handled by a Python shared library called `auth-validator`

## Chat messages pagination and retrieving of the first page

The Chat will send a HTTP request to the Chat Microserver `/chat/<id>?time=<time-uuid>&quantity` to retrieve a set of messages

- Query parameter **quatity** will be a integer to know the max size of messages to get
- Query parameter **time** will be the UUID time of the last message that the chat have to get messages before that time
- Both query parameter are optional. When there are not quantity you get 10. When there are not time you get the latest messages.

## Development Enviroment Details

- We going to use [tilt](https://tilt.dev/) in order to run the infraestructure on Kubernetes for development purposes.
- There is a Docker Compose for development purposes.
- For Python you need Pipenv and version 3.9.7
- For Java you need:

```
java 17.0.2 2022-01-18 LTS
Java(TM) SE Runtime Environment (build 17.0.2+8-LTS-86)
Java HotSpot(TM) 64-Bit Server VM (build 17.0.2+8-LTS-86, mixed mode, sharing)
```

## Best current way to run the project:

```bash
docker-compose rm -svf && docker-compose up
```

It should create 9 containers:

```
1.)
chat-firebase-apache-camel_zookeeper_1
2.)
chat-firebase-apache-camel_cassandra_1
3.)
chat-firebase-apache-camel_auth_db_1
4.)
chat-firebase-apache-camel_kafka_1
5.)
chat-firebase-apache-camel_consumer_1
6.)
chat-firebase-apache-camel_auth_microservice_1
7.)
chat-firebase-apache-camel_apache_camel_microservices_1
8.)
chat-firebase-apache-camel_chat_microservices_1
9.)
chat-firebase-apache-camel_frontend-web
```

Then you can open `http://localhost:3000/` and start using the chat.

## Run tests in Apache Camel

```bash
mvn test -X
```

## How to run the microservices manually?

- Chat Microservice:

```bash
cd chat-microservice && pipenv run server
```

- Auth Microservice:

```bash
cd auth-microservice && pipenv run server
```

- You will need Maven to run the Apache Camel Spring Boot server

```bash
cd apache-camel-service-bus && mvn package && mvn spring-boot:run
```

## Docker Development Worflow

### Main command to run docker-compose

```bash
docker-compose rm -svf && docker-compose up
```

### Migrate using Alembic in the Auth Microservice

In order to use the auth microservice you must migrate using alembic to create the user table. Access to the container and run:

```bash
pipenv shell
alembic upgrade head
```

It should print something like:

```bash
dict_keys(['user'])
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> fe1a63894533, create user table
INFO  [alembic.runtime.migration] Running upgrade fe1a63894533 -> d3c6204b9f3c, username unique
```

### Run Kafka CLI:

Create a topic:

```bash
docker exec -it CONTAINER_ID kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3 --topic charlytest
```

List of topics:

```bash
docker exec -it CONTAINER_ID kafka-topics.sh --bootstrap-server localhost:9092 --list
```

Get topics information

```bash
docker exec -it CONTAINER_ID kafka-topics.sh --bootstrap-server localhost:9092 --describe
```

Console Producer using key and acks

In this case 12345 is the key and hello de message content (Useful to put all the messages in the same partition using the user_id)

```bash
docker exec -it CONTAINER_ID kafka-console-producer.sh  --bootstrap-server localhost:9092 --topic charlytest --producer-property acks=all --property parse.key=true --property key.separator=:

>> 12345:hello
```

### Access to Cassandra:

```bash
docker exec -it CONTAINER_ID cqlsh
```

### Get the network information

```bash
docker network ls | grep "camel"
```

### Firebase integration for Firestore.

You need to download the `service_account_key.json ` from your Firebase project add it to the `aggregated-messages-consumer` folder.

Also you need to update the .env file in the `frontend-dev` folder to looks like:

```bash
# MICROSERVICES
NEXT_PUBLIC_AUTH_MICROSERVICE = 'http://0.0.0.0:8000'
NEXT_PUBLIC_CHAT_MICROSERVICE = 'http://0.0.0.0:9000'
# FIREBASE
NEXT_PUBLIC_API_KEY="..."
NEXT_PUBLIC_AUTH_DOMAIN="..."
NEXT_PUBLIC_PROJECT_ID="..."
NEXT_PUBLIC_STORAGE_BUCKET="..."
NEXT_PUBLIC_MESSAGING_SENDER_ID="..."
NEXT_PUBLIC_APP_ID="..."
```

---

### License

Apache License 2.0
