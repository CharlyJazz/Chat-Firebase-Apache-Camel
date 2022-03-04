from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..deps import (
    get_current_user,
    get_session,
    get_token_data,
)
from app.core.security import get_password_hash
from app.models.users import User as UserModel
from app.schemas.user import User as UserSchema
from app.schemas.user import UserCreate as UserCreateSchema


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserSchema], dependencies=[Depends(get_token_data)])
async def get_users(session: AsyncSession = Depends(get_session)):
    """
    Retrieve users.
    """
    result = await session.execute(select(UserModel))
    return result.scalars().all()


@router.post("/", response_model=UserSchema)
async def create_user(data: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    """
    Create User.
    """
    user = UserModel(
        username=data.username, 
        hashed_password=get_password_hash(data.password)
    )
    try:
        session.add(user)
        await session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=409, detail="User with this username already exits"
    )
    return {
        "id": user.id,
        "username": user.username
    }
