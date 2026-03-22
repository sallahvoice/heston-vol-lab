from fastapi import APIRouter, Request

router = APIRouter(prefix="/redis", tags=["redis"])


@router.post("/cache/expire")
async def expire_cache(request: Request):
    try:
        data = await request.json()
        cache_key = data.get("cache_key")
        if not cache_key:
            return {"status": "info", "message": "no cache_key provided"}
        if not redis_client:
            return {"status": "info", "message": "Redis client not available"}
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
def health():
    redis_status = "connect" if redis_client else "disconnected"
    return {"status": "health", "message": redis_status}