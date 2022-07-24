import json

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.schemas.message import MessageSentREST, MessageCreatedResponse
from app.core.config import settings
from app.models.chat_messages import ChatMessages
from app.models.chat import Chat
from ..deps import (
    get_kafka_producer,
    get_token_data,
    get_current_user_id
)


router = APIRouter(tags=["Messaging"])

@router.post(
    "/messaging/", 
    response_model=MessageCreatedResponse, 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_token_data)]
)
async def create_message(
    message: MessageSentREST, 
    kafka_producer = Depends(get_kafka_producer),
    current_user_id = Depends(get_current_user_id)
):
    """
    The user send a message using this endpoint
    Save the message in cassandra in async way (TODO async)
    Send the message to the kafka topic to use it in apache camel in async way (TODO async)
    Message ID and the timestamp automatically created

    - **chat_id**: ID of the chat
    - **body**: Message text
    - **from_user**: ID of the user that wrote it
    - **to_user**: ID of the user that need the message back
    """
    if str(current_user_id) != str(message.from_user):
        raise HTTPException(
            status_code=401, detail=settings.CASSANDRA_MESSAGE_CREATION_UNAUTHORIZED
        )
    if not Chat.users_id_belongs_to_chat(message.chat_id, message.from_user, message.to_user):
        raise HTTPException(
            status_code=401, detail=settings.CASSANDRA_MESSAGE_CREATION_UNAUTHORIZED
        )
    await kafka_producer.send_and_wait("chat_messages", message.json().encode('utf-8'))
    try:
        record_created = ChatMessages.create(**message.__dict__)
        return MessageCreatedResponse(**dict(record_created))
    except BaseException:
        raise HTTPException(
            status_code=400, detail=settings.CASSANDRA_MESSAGE_CREATION_ERROR
        )


@router.get(
    "/messaging/", 
    status_code=status.HTTP_200_OK,
)
async def get_messages():
    pass
