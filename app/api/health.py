from fastapi import APIRouter
from app.core.logging import logger

router = APIRouter()

@router.get("/health")
def health():
    logger.info("Health endpoint called...")

    return {
        "status": "healthy"
        }