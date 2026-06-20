from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import logger
from app.api.router import router

logger.info("Starting Application...")

app = FastAPI(
    title = settings.APP_NAME,
    version = settings.APP_VERSION
)

@app.get("/")
def root():
    logger.info("Root endpoint called.")

    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }

app.include_router(router)