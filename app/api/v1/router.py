from fastapi import APIRouter
from app.api.v1.endpoints import health
from app.api.v1.endpoints.simulation import router as simulation_router

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"]) #will include other endpoints
api_router.include_router(simulation_router)