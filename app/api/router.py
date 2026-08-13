from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.document import router as document_router
from app.api.upload import router as upload_router
from app.api.query import router as query_router

router = APIRouter()

router.include_router(
    health_router
)

router.include_router(
    document_router
)

router.include_router(
    upload_router
)

router.include_router(
    query_router
)