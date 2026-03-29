import redis
from fastapi import APIRouter, Request, Depends

from app.core.logger import get_logger
from app.utils.redis_client import get_redis_client


router = APIRouter(prefix="/redis", tags=["redis"])
logger = get_logger(__name__)


@router.post("/cache/expire")
async def expire_cache(
    request: Request,
    redis_client = Depends(get_redis_client)):
    try:
        data = await request.json()
        cache_key = data.get("cache_key")

        if not cache_key:
            return {"status": "info", "message": "no cache_key provided"}
        result = redis_client.delete(cache_key)
        
        if result:
            logger.info("cache key '%s' expired successfully", cache_key)
            return {
                "status": "success",
                "message": f"successfully delete cache key: {cache_key}"
            }
        
        return {
            "status": "warning",
            "message": f"failed to delete cache key: {cache_key}"
        }
    except redis.RedisError as e:
        logger.exception("cache expiry error: %s", e)
        return {"status": "error", "message": f"cache expiry failed {str(e)}"}


@router.get("/health/")
def health(redis_client = Depends(get_redis_client)):
    try:
        redis_client.ping()
        return {"status": "health", "message": "connected"}
    except redis.RedisError:
        return {"status": "error", "message": "disconnected"}