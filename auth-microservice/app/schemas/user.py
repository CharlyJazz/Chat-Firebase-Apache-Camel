from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str = None

    # PR To fastapi to add this like to the async sql alchemy example 
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str = None
    password: str = None
