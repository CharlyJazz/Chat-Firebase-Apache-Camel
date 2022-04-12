from typing import Any, Optional

from pydantic import BaseSettings, SecretStr, validator


class Settings(BaseSettings):
    PROJECT_NAME: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PORT: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_URI: Optional[str] = None
    FIRST_USER_USERNAME: str
    FIRST_USER_PASSWORD: SecretStr
    SECRET_KEY: SecretStr
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    # DELETE THIS AFTER IMPLEMENT AUTH VALIDATOR LIBRARY
    GET_TOKEN_DATA_403: str = 'Could not validate credentials'
    GET_CURRENT_USER_404: str = 'User not found'
    OAUTH2_NOT_AUTHENTICATED: str = 'Not authenticated'

    @validator("POSTGRES_URI", pre=True)
    def validate_postgres_conn(cls, v: Optional[str], values: dict[str, Any]) -> str:
        if isinstance(v, str):
            return v
        password: SecretStr = values.get("POSTGRES_PASSWORD", SecretStr(""))
        return "{scheme}://{user}:{password}@{host}:{port}/{db}".format(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=password.get_secret_value(),
            host=values.get("POSTGRES_HOST"),
            db=values.get("POSTGRES_DB"),
            port=values.get("POSTGRES_PORT")
        )

    class Config:
        # Relative to main.py
        env_file = "../.env"


settings = Settings()
