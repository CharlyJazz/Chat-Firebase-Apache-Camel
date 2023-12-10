import asyncio
import socket

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", status_code=200)
async def health():
    return Response(status_code=200)
