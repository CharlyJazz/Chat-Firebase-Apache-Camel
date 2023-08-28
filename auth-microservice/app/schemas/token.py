from typing import Literal, Optional

from pydantic import BaseModel


class AuthenticationSuccessResponse(BaseModel):
    access_token: str
    token_type: Literal["Bearer"]
    id: str
    username: str