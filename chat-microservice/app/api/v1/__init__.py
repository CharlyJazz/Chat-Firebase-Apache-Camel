from fastapi import APIRouter

from app.api.v1.messaging import router as messaging_router

router = APIRouter(prefix="/v1")
router.include_router(messaging_router)
