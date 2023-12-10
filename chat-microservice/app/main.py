from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router
from app.core.config import settings
from app.core.kafka import kafka_producer
from app.core.middlewares import request_middleware
from app.core.cassandra import cassandra_connect, cassandra_shutdown

async def startup_event():
    if not settings.TESTING_MODE:
        await kafka_producer.start()
    cassandra_connect()


async def shutdown_event():
    if not settings.TESTING_MODE:
        await kafka_producer.stop()
    cassandra_shutdown()


def create_application() -> FastAPI:
    application = FastAPI(title=settings.PROJECT_NAME)
    # origins = [ "http://localhost:3000", "http://34.69.26.50:3000" ]
    origins = [ "*" ]
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    application.include_router(router)
    application.add_event_handler("startup", startup_event)
    application.add_event_handler("shutdown", shutdown_event)
    application.middleware("http")(request_middleware)
    return application

app = create_application()
