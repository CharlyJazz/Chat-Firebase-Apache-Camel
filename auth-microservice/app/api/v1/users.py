from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

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

@router.get("/{user_id}", response_model=UserSchema, dependencies=[Depends(get_token_data)])
async def get_user(
        user_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: UserSchema = Depends(get_current_user)
    ):
    """
    Retrieve a user by id.
    """
    result = await session.get(UserModel, user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@router.post("/", response_model=UserSchema)
async def create_user(
        data: UserCreateSchema, 
        session: AsyncSession = Depends(get_session), 
        status_code=status.HTTP_201_CREATED
    ):
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
    return UserSchema(id=user.id, username=user.username)
