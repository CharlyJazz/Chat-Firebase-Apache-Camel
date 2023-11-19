import asyncio
import socket

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response
from sqlalchemy.sql import text

from app.api.deps import get_session

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", status_code=200)
async def health(session: AsyncSession = Depends(get_session)):
    try:
        await asyncio.wait_for(session.execute(text("SELECT 1")), timeout=1)
    except (asyncio.TimeoutError, socket.gaierror):
        return Response(status_code=503)
    return Response(status_code=200)
