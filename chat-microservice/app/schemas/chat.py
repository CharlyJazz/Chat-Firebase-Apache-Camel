from pydantic import BaseModel, Field, validator
from typing import List
from uuid import UUID

class ChatSentREST(BaseModel):
    users_id: List[str]
    users_name: List[str]
        
    @validator('users_id')
    def users_id_uniques(cls, v):
        assert len(set(v)) == len(v), 'must be uniques values'
        return v

    @validator('users_id')
    def users_id_length(cls, v):
        assert len(v) == 2, 'must has two values'
        return v

    @validator('users_name')
    def users_name_uniques(cls, v):
        assert len(set(v)) == len(v), 'must be uniques values'
        return v

    @validator('users_name')
    def users_name_length(cls, v):
        assert len(v) == 2, 'must has two values'
        return v


    class Config:
        schema_extra = {
            "example": {
                "users_id": [1, 2],
                "users_name": ['Bart', 'Pepe']
            }
        }

class ChatCreatedResponse(BaseModel):
    chat_id: UUID
    users_id: List[str]
    users_name: List[str]

    class Config:
        schema_extra = {
            "example": {
                "chat_id": "808a156a-672d-4604-ab3d-355bc3445e2e",
                "users_id": ['1', '2'],
                "users_name": ["Pepe", "Foo"]
            }
        }
