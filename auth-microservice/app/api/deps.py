from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.users import User
from app.schemas.token import TokenPayload

oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


async def get_session():
    async with SessionLocal() as session:
        yield session


def get_token_data(token: str = Depends(oauth2)) -> TokenPayload:
    try:
        secret_key = settings.SECRET_KEY.get_secret_value()
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return token_data


async def get_current_user(
    token: str = Depends(get_token_data),
    session: AsyncSession = Depends(get_session),
):
    user = await User.get(session, id=token.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user
