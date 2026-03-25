from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("Starting %s in %s", settings.app_name, settings.environment)
    yield
    logger.info("Shutting down %s", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)
app.include_router(api_router, prefix="/api/v1")

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("unhandled error at %s: %s", request.url.path, exc)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )