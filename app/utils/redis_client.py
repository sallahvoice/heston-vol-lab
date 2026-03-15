import os
import redis
from dotenv import load_dotenv
from fastapi import FastApi, Request
from app.core.logger import get_logger

load_dotenv()
app = FastApi()
logger = get_logger(__file__)

try:
    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", "6379")),
        db=int(os.getenv("REDIS_DB", "0")),
        password=os.getenv("REDIS_PASSWORD", "None")
    )
    redis_client.ping()
    logger.info("Redis connection established")

except redis.exception.ConnectionError as e:
    logger.error("Redis connection failed: %s", e)
    redis_client = None


@app.post("/expire_cache/")
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


@app.get("/health/")
def health():
    redis_status = "connect" if redis_client else "disconnected"
    return {"status": "health", "message": redis_status}