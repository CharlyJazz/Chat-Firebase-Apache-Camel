from typing import Any, Dict, Optional

from pydantic import BaseSettings, SecretStr, validator


class Settings(BaseSettings):
    PROJECT_NAME: str
    SECRET_KEY: SecretStr
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str

    # TODO: Add here all the KAFKA ENV VARIABLES

    class Config:
        # Relative to main.py
        env_file = "../.env"


settings = Settings()
