from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from app.api.deps import get_session

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/", status_code=200)
async def health(session: AsyncSession = Depends(get_session)):
    return Response(status_code=200)
