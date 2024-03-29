import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.chat import ChatSentREST, ChatCreatedResponse
from app.schemas.message import GetMessageValidator, MessageSchema
from app.core.config import settings
from app.models.chat import Chat
from app.models.chat_messages import ChatMessages
from ..deps import (
    get_token_data,
    get_current_user_id
)


router = APIRouter(tags=["Chat"])

@router.post(
    "/chat/", 
    response_model=ChatCreatedResponse, 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_token_data)]
)
async def create_chat(
    chat: ChatSentREST, 
    current_user_id = Depends(get_current_user_id)
):
    """
    Create a chat between users using this endpoint.
    Validate if current user id in user_id
    This endpoint is not validating if the users id already exists.
    This endpoint does not have way to get the users name.
    - **users_id**: List of users ID
    """
    if str(current_user_id) not in chat.users_id:
        raise HTTPException(
            status_code=401, detail='User is not authorized to do this action'
        )
    user_1_id, user_2_id = chat.users_id
    if Chat.users_id_belongs_to_chat(None, user_1_id, user_2_id):
        raise HTTPException(
            status_code=422, detail='There is a chat for this users'
        )
    user_1_name, user_2_name = chat.users_name
    new_chat = Chat.create(
        chat_id = str(uuid.uuid4()),
        users_id = [user_1_id, user_2_id],
        users_name = [user_1_name, user_2_name]
    )
    return new_chat

@router.get(
    "/chat/", 
    response_model=list[ChatCreatedResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_data)]
)
async def get_user_chats(current_user_id = Depends(get_current_user_id)):
    """
    Get all chat that belongs to the authenticated user
    """
    results = Chat.objects().filter(users_id__contains=str(current_user_id)).allow_filtering()
    return list(results)

@router.get(
    "/chat/{chat_id}/messages/", 
    response_model=list[MessageSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_data)]
)
async def get_messages(chat_message: GetMessageValidator = Depends()):
    """
    Get chat messages between users using this endpoint.
    - **chat_id**: ID of the chat between users
    - **time**: get the chat messages sorted by the time
    - **quantity**: limit of the messages that you will receive
    """
    if chat_message.chat_id_validator(chat_message.chat_id):
        raise HTTPException(
            status_code=404, detail=settings.GET_MESSAGES_CHAT_ID_ERROR
        )
    if chat_message.chat_time_validator(chat_message.chat_id, chat_message.get_time(chat_message.chat_id, chat_message.time)):
        raise HTTPException(
            status_code=404, detail=settings.GET_MESSAGES_TIME_ERROR
        )
    if chat_message.quantity_validator(chat_message.quantity):
        raise HTTPException(
            status_code=422, detail=settings.GET_MESSAGES_QUANTITY_ERROR
        )

    if chat_message.time == None:
        return list(
            ChatMessages
                .objects(chat_id=chat_message.chat_id)
                .limit(chat_message.quantity)
            )
    else:
        return list(
            ChatMessages
                .objects(chat_id=chat_message.chat_id)
                .filter(time__lt=chat_message.time)
                .limit(chat_message.quantity)
            )
