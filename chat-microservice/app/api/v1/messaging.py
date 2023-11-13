import json

from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from app.schemas.message import MessageSentREST, MessageSchema
from app.core.config import settings
from app.models.chat_messages import ChatMessages
from app.models.chat import Chat
from ..deps import (
    # get_kafka_producer,
    get_token_data,
    get_current_user_id,
    get_logging_event
)


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)

router = APIRouter(tags=["Messaging"])

@router.post(
    "/messaging/",
    response_model=MessageSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_token_data)]
)
async def create_message(
    message: MessageSentREST,
    # kafka_producer = Depends(get_kafka_producer),
    current_user_id = Depends(get_current_user_id),
    Logging = Depends(get_logging_event)
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
    try:
        record_created = ChatMessages.create(**message.__dict__)
        schema = MessageSchema(**dict(record_created))
        json_dump = json.dumps(dict(schema), cls=UUIDEncoder).encode('utf-8')
        Logging.info('Message created {}'.format(json_dump))
        # await kafka_producer.send_and_wait("chat_messages", json_dump)
        return schema
    except BaseException as e:
        Logging.error(f"An error occurred: {str(e)}")  # Log the error message
        raise HTTPException(
            status_code=400, detail=settings.CASSANDRA_MESSAGE_CREATION_ERROR
        )
