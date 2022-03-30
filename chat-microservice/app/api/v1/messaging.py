import json

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from cassandra import WriteFailure

from app.schemas.message import MessageSentREST, MessageCreatedResponse
from app.core.config import settings
from ..deps import (
    get_kafka_producer,
    get_chat_message_model
)


router = APIRouter(tags=["Messaging"])

@router.post(
    "/messaging/", 
    response_model=MessageCreatedResponse, 
    status_code=status.HTTP_201_CREATED
)
async def create_message(
    message: MessageSentREST, 
    kafka_producer = Depends(get_kafka_producer),
    chat_message_model = Depends(get_chat_message_model),
):
    """
    The user send a message using this endpoint
    Save the message in cassandra in async way
    Send the message to the kafka topic to use in apache camel
    Message ID and the timestamp automatically created

    - **body**: Message text
    - **from_user**: ID of the user that wrote it
    - **to_user**: ID of the user that need the message back
    """
    await kafka_producer.send_and_wait("chat_messages", message.json().encode('utf-8'))
    try:
        record_created = get_chat_message_model().create(**message.__dict__)
        return MessageCreatedResponse(**dict(record_created))
    except BaseException:
        raise HTTPException(
            status_code=400, detail=settings.CASSANDRA_MESSAGE_CREATION_ERROR
        )

