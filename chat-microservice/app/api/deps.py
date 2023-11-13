from fastapi import Depends

# from app.core.kafka import kafka_producer
from app.core.config import settings
from app.core.logging import Logging

from auth_validator import AuthValidator

validator = AuthValidator(settings.SECRET_KEY.get_secret_value(), settings.ALGORITHM)

get_token_data = validator.get_token_data

"""
Kafka Producer instance as dependency in order to easy mock it
"""
def get_kafka_producer():
    return None
    # return kafka_producer

"""
Tiny helper to retrieve the user id from then JWT token
"""
async def get_current_user_id(token = Depends(get_token_data)) -> str:
    return token.user_id

"""
Logging to handle start events that are outside from uvicorn request middleware
"""
def get_logging_event():
    return Logging