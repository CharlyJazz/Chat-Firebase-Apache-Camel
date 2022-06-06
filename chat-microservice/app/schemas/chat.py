from pydantic import BaseModel, Field
from uuid import UUID

class ChatSentREST(BaseModel):
    users_id: str[]
    
    class Config:
        schema_extra = {
            "example": {
                "users_id": [1, 2]
            }
        }

class ChatCreatedResponse(BaseModel):
    chat_id: UUID
    users_id: str = Field(..., min_items=2, max_items=2)
    # TODO: Validate users_id unique values
    class Config:
        schema_extra = {
            "example": {
                "chat_id": "808a156a-672d-4604-ab3d-355bc3445e2e",
                "users_id": ['1', '2']
            }
        }
