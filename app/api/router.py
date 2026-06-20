from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.document import router as document_router

router = APIRouter()

router.include_router(
    health_router,
    tags=["Health"]
)

router.include_router(
    document_router,
    tags=["Documents"]
)