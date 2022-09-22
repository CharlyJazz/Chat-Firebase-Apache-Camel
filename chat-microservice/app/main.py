from fastapi import FastAPI, Request
from starlette.concurrency import iterate_in_threadpool
import json

from app.api import router
from app.core.config import settings
from app.core.kafka import kafka_producer
from app.core.logging import Logging
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
    application.include_router(router)
    application.add_event_handler("startup", startup_event)
    application.add_event_handler("shutdown", shutdown_event)
    return application


app = create_application()

@app.middleware("http")
async def request_middleware(request: Request, call_next):
    Logging.info(f"Request started at {request.url.path}")
    response = await call_next(request)
    response_body = [chunk async for chunk in response.body_iterator]
    response.body_iterator = iterate_in_threadpool(iter(response_body))
    if response.status_code >= 400:
        Logging.error(f"{response.status_code} {json.loads(response_body[0].decode())['detail']} at {request.url.path}")
    else:
        Logging.info(f"{response.status_code} Request OK at {request.url.path}")
    Logging.info(f"Request ended at {request.url.path}")
    return response