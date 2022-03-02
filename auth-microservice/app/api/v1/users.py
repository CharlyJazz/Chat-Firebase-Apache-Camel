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
from app.models.users import User

router = APIRouter(prefix="/users", tags=["Users"])
