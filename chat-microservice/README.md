### Deps

`pipenv install`

`pipenv shell`

### Re run containers

`docker-compose rm -svf && docker-compose up`

### Run server

- `pipenv run server`
- `uvicorn app.main:app --host 0.0.0.0 --port 80  --reload`

### Run tests

Cassandra Tests

`pipenv run db-test`

Server Tests

`export TESTING_MODE=1 && pipenv run api-test`

Run a specific test case

`export TESTING_MODE=1 && pytest app/tests/api --disable-warnings -rP -k test_no_allow_create_chat_message_if_to_user_not_match`

- Do not user UID as user ids for creating JWT. It will raise 403. Also users id are integers because the database is Postgres

## Access to cassandra in development

`docker exec -it book-cassandra cqlsh`

## Ideas

- https://stackoverflow.com/questions/24176883/cassandra-schema-for-a-chat-application

## GKE Tests

- 1,
