from fastapi import APIRouter
from app.api.v1.endpoints.health import health

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"]) #will include other endpoints