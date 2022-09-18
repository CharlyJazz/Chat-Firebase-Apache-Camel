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
    CASSANDRA_MESSAGE_GET_MESSAGES_ERROR: Optional[str] = None
    GET_MESSAGES_QUANTITY_ERROR: Optional[str] = None
    GET_MESSAGES_TIME_ERROR: Optional[str] = None
    GET_MESSAGES_CHAT_ID_ERROR: Optional[str] = None
    KAFKA_BOOTSTRAP_SERVER: str
    CASSANDRA_KEYSPACE_TESTING: str = 'python_test_environment'
    MAX_MESSAGES_QUANTITY_PAGINATION = 20

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

    @validator("GET_MESSAGES_QUANTITY_ERROR", pre=True)
    def validate_get_messages_quantity(cls, v: Optional[str], values: dict[str, Any]) -> str:
        if isinstance(v, str):
            return v
        return 'quantity param must be greater than 0 and lower or equals than 20'

    @validator("GET_MESSAGES_TIME_ERROR", pre=True)
    def validate_get_messages_time(cls, v: Optional[str], values: dict[str, Any]) -> str:
        if isinstance(v, str):
            return v
        return 'there are not pages for the given time'
    
    @validator("GET_MESSAGES_CHAT_ID_ERROR", pre=True)
    def validate_get_messages_chat_id(cls, v: Optional[str], values: dict[str, Any]) -> str:
        if isinstance(v, str):
            return v
        return 'chat ID is not found'

    @validator("CASSANDRA_MESSAGE_CREATION_UNAUTHORIZED", pre=True)
    def validate_cassandra_message_creation_unauthorized(cls, v: Optional[str], values: dict[str, Any]) -> str:
        if isinstance(v, str):
            return v

        return f"\
Unauthorized action in cassandra cluster \
{values.get('CASSANDRA_CLUSTER_ADDRESS')} \
at keyspace {values.get('CASSANDRA_KEYSPACE')}"

    @validator("CASSANDRA_MESSAGE_GET_MESSAGES_ERROR", pre=True)
    def validate_cassandra_get_messages_unauthorized(cls, v: Optional[str], values: dict[str, Any]) -> str:
        if isinstance(v, str):
            return v

        return f"\
Unauthorized action in cassandra cluster \
{values.get('CASSANDRA_MESSAGE_GET_MESSAGES_ERROR')} \
at keyspace {values.get('CASSANDRA_KEYSPACE')}"


settings = Settings()
