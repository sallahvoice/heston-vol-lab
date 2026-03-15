from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="simulation", tags=["simulation"])

@router.get("/health")
def health():
    return {
        "status": "alive",
        "timestamp": datetime.utcnow()
        }