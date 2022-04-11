from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.users import User

from auth_validator import AuthValidator

validator = AuthValidator(settings.SECRET_KEY.get_secret_value(), settings.ALGORITHM)

get_token_data = validator.get_token_data

async def get_session():
    async with SessionLocal() as session:
        yield session

async def get_current_user(
    token: str = Depends(get_token_data),
    session: AsyncSession = Depends(get_session),
):
    user = await session.get(User, token.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=settings.GET_CURRENT_USER_404)
    return user
