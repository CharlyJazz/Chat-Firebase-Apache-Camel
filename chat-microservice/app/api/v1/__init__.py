from fastapi import APIRouter

from app.api.v1.messaging import router as messaging_router
from app.api.v1.chat import router as chat_router


router = APIRouter(prefix="/v1")
router.include_router(messaging_router)
router.include_router(chat_router)
