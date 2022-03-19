### Deps

`pipenv install`

`pipenv shell`

### Migrations

Load env variables

`export $(cat .env | xargs)`

`alembic revision --autogenerate -m "<DESCRIPTION>"`

`alembic upgrade head`


### Re run containers

`docker-compose up --force-recreate`


### Run server

`uvicorn app.main:app --host 0.0.0.0 --port 80  --reload`


### Run tests

`pytest app/tests --disable-warnings -rP`


## Access to postgres in development

Let imagine `ec4942c811fe` is the container ID (`docker ps` will show you what is the id)

`docker exec -ti ec4942c811fe psql -U auth_microservice`
