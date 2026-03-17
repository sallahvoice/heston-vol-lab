from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter()

@router.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "alive",
        "timestamp": datetime.now(timezone.utc).isoformat()
        }