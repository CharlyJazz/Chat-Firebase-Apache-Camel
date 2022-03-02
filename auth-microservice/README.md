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

`pytest app/tests --disable-warnings`
