from typing import Any, Dict, Optional

from pydantic import BaseSettings, SecretStr, validator


class Settings(BaseSettings):
    PROJECT_NAME: str
    SECRET_KEY: SecretStr
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    CASSANDRA_KEYSPACE: str
    CASSANDRA_PROTOCOL_VERSION: int
    CASSANDRA_CLUSTER_ADDRESS: str
    CASSANDRA_MESSAGE_CREATION_ERROR: Optional[str] = None
    KAFKA_BOOTSTRAP_SERVER: str

    @validator("CASSANDRA_MESSAGE_CREATION_ERROR", pre=True)
    def validate_cassandra_message_creationg(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if isinstance(v, str):
            return v

        return f"\
Error creating the message in cassandra cluster \
{values.get('CASSANDRA_CLUSTER_ADDRESS')} \
at keyspace {values.get('CASSANDRA_KEYSPACE')}"

    class Config:
        # Relative to main.py
        env_file = "../.env"


settings = Settings()
