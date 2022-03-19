from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from kafka import KafkaProducer

from app.schemas.message import MessageSentREST
from ..deps import (
    get_kafka_producer
)

import json

router = APIRouter(tags=["Messaging"])

@router.post("/messaging/")
async def create_message(
    message: MessageSentREST, 
    kafka_producer = Depends(get_kafka_producer)
):
    """
    The user send a message using this endpoint
    Save the message in cassandra in async way
    Send the message to the kafka topic to use in apache camel
    
    - **body**: Message text
    - **created_at**: Time when the message was wrote
    - **from_user**: ID of the user that wrote it
    - **to_user**: ID of the user that need the message back
    """
    # TODO: Save message in cassandra async
    await kafka_producer.send_and_wait("chat_messages", message.json().encode('utf-8'))
    return {"succes": "always"}
