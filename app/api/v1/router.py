from fastapi import APIRouter

from app.api.v1.endpoints.redis import router as redis_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.simulation import router as simulation_router
from app.api.v1.endpoints.pricing import router as pricing_router
from app.api.v1.endpoints.calibration import router as calibration_router

api_router = APIRouter()

api_router.include_router(redis_router)
api_router.include_router(health_router)
api_router.include_router(simulation_router)
api_router.include_router(pricing_router)
api_router.include_router(calibration_router)
