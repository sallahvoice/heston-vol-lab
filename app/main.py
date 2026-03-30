from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logger import get_logger
from app.core.exceptions import (
    FellerConditionViolation,
    InvalidParameterError,
    ModelConvergenceError
)

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

async def http_exception_handler(request: Request, e: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=e.status_code,
        content={
            "code": "http_error",
            "detail": e.detail,
            "request_path": request.url.path,
            "timestamp": datetime.now(timezone.utc),
        },
    )

async def domain_exception_handler(request: Request, e: Exception) -> JSONResponse:
    logger.warning("domain error at %s: %s", request.url.path, e)
    return JSONResponse(
        status_code=422,
        content = {
            "code": "validation_error",
            "detail": str(e),
            "request_path": request.url.path,
            "timestamp": datetime.now(timezone.utc),
            },
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, e: Exception) -> JSONResponse:
    logger.exception("unhandled error at %s: %s", request.url.path, e)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error",
            "request_path": request.url.path,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(ValueError, domain_exception_handler)
app.add_exception_handler(FellerConditionViolation, domain_exception_handler)
app.add_exception_handler(InvalidParameterError, domain_exception_handler)
app.add_exception_handler(ModelConvergenceError, domain_exception_handler)