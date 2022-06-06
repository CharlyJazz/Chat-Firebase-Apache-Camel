import json

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.schemas.chat import ChatSentREST, ChatCreatedResponse
from app.core.config import settings
from app.models.chat import Chat
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
    Create a chat between users using this endpoint

    - **users_id**: List of users ID
    """

    # TODO
    # Query user 1
    # Return error if user does not exist
    # user_1_id = 
    # user_1_name = 

    # TODO
    # Query user 2
    # Return error if user does not exist
    # user_2_id =
    # user_2_name =

    # TODO: Validate there is not already a chat with the two users
    
    # TODO: Try Catch and raise error

    new_chat = Chat.create(
        chat_id = str(uuid.uuid4()),
        users_id = [user_1_id, user_2_id],
        users_name = [user_1_name, user_2_name]
    )

    #  TODO: Return JSON
