from pydantic import BaseModel
from datetime import datetime

class MessageSentREST(BaseModel):
    body: str
    created_at: datetime
    from_user: str
    to_user: str
    
    class Config:
      schema_extra = {
          "example": {
              "body": "Hello bro!",
              "created_at": "2020-03-20T14:28:23.382748",
              "from_user": "1",
              "to_user": "2"
          }
      }
