# Chat App

Chat Message Architecture Solution that **do not** save each message inside Firestore

## Problem

We need a Chat App between two users but dont want save all the message in Firestore. Also we do not want read firestore to retrieve the messages and pagiante it.

## The Features are:

1. Create User
2. Login
3. Get the list of users
4. User send messages to other user 
5. Create a new chat room between to users: The user A will find the user B and start a chat.
6. User get realtime message updating

## Mapping Features to Architectural Components

- M1. The users management and authentication (features 1, 2 and 3) will be handle by a microservice called "Auth Microservice"
  - The microservice will have a store.
  - The microservice will use JWT for the Authentication
- M2. Chat creation and Message creation/retrieving (features 4 and 5) will be handle by a microservice called "Chat Microservice"
  - The microservice will have a store.
- M3. **Chat Microservice** will take care of sending the messages to a queue proccesing in other to satisfy the feature 6

## Realtime solution to satisfy feature 6

Instead of use Firestore or another cloud based solution for a full chat solution we going to use Firestore only to show the news messages aggregated.

A "new message aggregated" is a set of messages sent by a user, instead of show each message one by one there 
will be a server that going to group all the related messages sent by a user to a chat in a list. And that list will be retrieve to the chat.
This solution will be 

![Architecture diagram](https://user-images.githubusercontent.com/12489333/166072172-482250b2-93f7-4787-9652-3826054cc817.png)

**Advantages of this approach?**

None, I mean this is only for learn purposes and Apache Camel and microservices. 
I couldn't think of any other use for apache camel, the only use was to add chat messages

## Architectural Components to explicit implementation details

- The two microservices will be written in Python using FastAPI
- The message aggregating process will be handle by Apache Camel
- User databases will be Postgres
- Chat database will be Cassandra to create a fast partition for each chat
- "New Messages Aggregated" will be save into Firestore and only will retrieve for realtime
- Chat messages queue processing will be handle by Kafka
- Auth validation in microservices will be handle by a python shared library `auth-validator`

## Chat messages pagination and retrieving of the first page

The Chat will send a HTTP request to the Chat Microserver `/chat/<id>?time=<time-uuid>&quantity` to retrieve a set of messages

- Query parameter **quatity** will be a integer to know the max size of messages to get
- Query parameter **time** will be the UUID time of the last message that the chat have to get messages before that time
- Both query parameter are optional. When there are not quantity you get 10. When there are not time you get the latest messages.

## Development Enviroment Details

- We going to use [tilt](https://tilt.dev/) in order to run the infraestructure and Kubernetes obviously
- Also there are a Docker Compose file with Postgres, Kafka, Zookeeper and Cassandra.
- For Python you need Pipenv and version 3.9.7
- For Java you need:

```
java 17.0.2 2022-01-18 LTS
Java(TM) SE Runtime Environment (build 17.0.2+8-LTS-86)
Java HotSpot(TM) 64-Bit Server VM (build 17.0.2+8-LTS-86, mixed mode, sharing)
```


## Docker Development Worflow

### Kick off all the containers

```bash
docker-compose rm -svf && docker-compose up
```

### Run Kafka CLI:

Create a topic:
``` bash
docker exec -it CONTAINER_ID kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3 --topic charlytest
```

List of topics:
``` bash
docker exec -it CONTAINER_ID kafka-topics.sh --bootstrap-server localhost:9092 --list
```

Get topics information
``` bash
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
