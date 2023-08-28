from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.core.security import authenticate, create_access_token
from app.schemas.token import AuthenticationSuccessResponse

from typing import Annotated

from typing import Annotated

router = APIRouter(tags=["Login"])


@router.post("/login/", response_model=AuthenticationSuccessResponse)
async def login(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session),
):  
    user = await authenticate(session, username=data.username, password=data.password)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {
        "access_token": create_access_token(user), 
        "token_type": "Bearer",
        "id": str(user.id),
        "username": str(user.username),
    }
