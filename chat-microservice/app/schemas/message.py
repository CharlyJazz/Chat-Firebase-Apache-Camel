from pydantic import BaseModel, validator
from datetime import datetime
from app.core.config import settings
from typing import Optional
from uuid import UUID
from app.models.chat_messages import ChatMessages

class MessageSentREST(BaseModel):
    body: str
    from_user: str
    to_user: str
    chat_id: str
    
    class Config:
        schema_extra = {
            "example": {
                "body": "Hello bro!",
                "from_user": "1",
                "to_user": "2",
                "chat_id": "808a156a-672d-4604-ab3d-355bc3445e2e"
            }
        }

class GetMessageValidator(BaseModel):
    chat_id: UUID
    quantity: Optional[int] = 5
    time: Optional[UUID] = None

    @validator('quantity')
    def set_quantity(cls, quantity):
        return quantity or 5
    
    @staticmethod
    def get_time(chat_id, time):
        if time == None:
            return str(ChatMessages.objects(chat_id=chat_id).first()["time"])
        return time

    @staticmethod
    def chat_id_validator(chat_id) -> bool:
        return len(ChatMessages.objects(chat_id=chat_id)) == 0

    @staticmethod
    def quantity_validator(quantity) -> bool:
        return quantity <= 0 or quantity > settings.MAX_MESSAGES_QUANTITY_PAGINATION

    @staticmethod
    def chat_time_validator(chat_id, time) -> bool:
        if time == None:
            return False
        return len(ChatMessages.objects(chat_id=chat_id).filter(time=time)) == 0

class MessageCreatedResponse(BaseModel):
    message_id: UUID
    from_user: str
    to_user: str
    body: str
    chat_id: UUID
    time: UUID

    class Config:
        schema_extra = {
            "example": {
                "message_id": "808a156a-672d-4604-ab3d-355bc3445e2e",
                "from_user": "1",
                "to_user": "1",
                "body": "Hello bro!",
                "chat_id": "808a156a-672d-4604-ab3d-355bc3445e2e",
                "time": "935b7ae6-afc1-11ec-b85d-b29c4ace6a4c"
            }
        }
