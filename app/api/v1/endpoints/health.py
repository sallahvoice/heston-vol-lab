from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
def health() -> dict[str, str]:
    return {
        "status": "alive",
        "timestamp": datetime.now(timezone.utc).isoformat()
        }