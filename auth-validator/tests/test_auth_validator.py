from src.auth_validator import AuthValidator, TokenPayload
from jose import jwt
from datetime import datetime, timedelta

import pytest
import fastapi

SECRET_KEY = '1234567890'
ALGORITHM = 'HS256'

def test_auth_validator():
  token = jwt.encode(
      {
        "exp": datetime.utcnow() + timedelta(minutes=30), 
        "user_id": "1"
      },
      key=SECRET_KEY,
      algorithm=ALGORITHM
  )
  validator = AuthValidator(SECRET_KEY, ALGORITHM)
  
  with pytest.raises(fastapi.exceptions.HTTPException):
      validator.get_token_data('PEPE PERINOLO')
  
  token_result = validator.get_token_data(token)
  
  assert token_result.user_id == 1
