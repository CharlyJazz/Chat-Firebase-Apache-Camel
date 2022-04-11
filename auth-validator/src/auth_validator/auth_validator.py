from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError, BaseModel

from jose import jwt

MESSAGE_GET_TOKEN_DATA_403 = 'Could not validate credentials'

class TokenPayload(BaseModel):
    user_id: int

class AuthValidator:
  def __init__(self, secret_key, algorithms):
    self.secret_key = secret_key
    self.algorithms = algorithms
  
  def get_token_data(
      self, 
      token: str = Depends(
        OAuth2PasswordBearer(tokenUrl="/api/v1/login")
      )
    ) -> TokenPayload:
    try:
        payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithms])
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(status_code=403, detail=MESSAGE_GET_TOKEN_DATA_403)
    return token_data
