### Deps

`pipenv install`

`pipenv shell`


### Re run containers

`docker-compose up --force-recreate`


### Run server

`uvicorn app.main:app --host 0.0.0.0 --port 80  --reload`


### Run tests

`pytest app/tests --disable-warnings -rP`


## Access to cassandra in development

`docker exec -it book-cassandra cqlsh`


## Ideas

- https://stackoverflow.com/questions/24176883/cassandra-schema-for-a-chat-application
