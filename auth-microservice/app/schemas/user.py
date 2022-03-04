from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str = None


class UserCreate(BaseModel):
    username: str = None
    password: str = None
