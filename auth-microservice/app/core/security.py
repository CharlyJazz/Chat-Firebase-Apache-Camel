from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.users import User

from sqlalchemy import select

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(user: User) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
        {"exp": expire, "user_id": str(user.id)},
        key=settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM,
    )


def is_valid_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def authenticate(
    session: AsyncSession, username: str, password: str
) -> Optional[User]:
    result = await session.execute(
        select(User).filter(User.username==username)
    )
    user = result.scalars().first()
    if user is not None and is_valid_password(password, user.hashed_password):
        return user
    return None
