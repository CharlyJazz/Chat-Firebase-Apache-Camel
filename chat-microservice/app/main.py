from arq import create_pool
from fastapi import FastAPI

from app.api import router
from app.core.config import settings
from app.core.kafka import kafka_producer
from app.core.cassandra import cassandra_connect, cassandra_shutdown

async def startup_event():
    await kafka_producer.start()
    cassandra_connect()


async def shutdown_event():
    await kafka_producer.stop()
    cassandra_shutdown()


def create_application() -> FastAPI:
    application = FastAPI(title=settings.PROJECT_NAME)
    application.include_router(router)
    application.add_event_handler("startup", startup_event)
    application.add_event_handler("shutdown", shutdown_event)
    return application


app = create_application()
