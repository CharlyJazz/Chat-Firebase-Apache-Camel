from arq import create_pool
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router
from app.core.config import settings


def create_application() -> FastAPI:
    application = FastAPI(title=settings.PROJECT_NAME)
    origins = [ "http://localhost:3000", "http://34.69.26.50:3000" ]
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    application.include_router(router)
    return application


app = create_application()
