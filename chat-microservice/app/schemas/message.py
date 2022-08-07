from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

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
