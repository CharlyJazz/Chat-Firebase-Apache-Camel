import os

from typing import Any, Optional
from pydantic import BaseSettings, SecretStr, validator


class Settings(BaseSettings):
    TESTING_MODE: bool = os.getenv("TESTING_MODE", 0)
    PROJECT_NAME: str
    SECRET_KEY: SecretStr
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    CASSANDRA_KEYSPACE: str
    CASSANDRA_PROTOCOL_VERSION: int
    CASSANDRA_CLUSTER_ADDRESS: str
    CASSANDRA_MESSAGE_CREATION_ERROR: Optional[str] = None
    CASSANDRA_MESSAGE_CREATION_UNAUTHORIZED: Optional[str] = None
    KAFKA_BOOTSTRAP_SERVER: str
    CASSANDRA_KEYSPACE_TESTING: str = 'python_test_environment'

    class Config:
        # Relative to main.py
        env_file = "../.env"

    @validator("CASSANDRA_MESSAGE_CREATION_ERROR", pre=True)
    def validate_cassandra_message_creation_error(cls, v: Optional[str], values: dict[str, Any]) -> str:
        if isinstance(v, str):
            return v

        return f"\
Error creating the message in cassandra cluster \
{values.get('CASSANDRA_CLUSTER_ADDRESS')} \
at keyspace {values.get('CASSANDRA_KEYSPACE')}"

    @validator("CASSANDRA_MESSAGE_CREATION_UNAUTHORIZED", pre=True)
    def validate_cassandra_message_creation_unauthorized(cls, v: Optional[str], values: dict[str, Any]) -> str:
        if isinstance(v, str):
            return v

        return f"\
Unauthorized action in cassandra cluster \
{values.get('CASSANDRA_CLUSTER_ADDRESS')} \
at keyspace {values.get('CASSANDRA_KEYSPACE')}"


settings = Settings()
