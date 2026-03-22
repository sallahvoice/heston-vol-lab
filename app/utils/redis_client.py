import os
import redis
from dotenv import load_dotenv
from app.core.logger import get_logger

load_dotenv()
logger = get_logger(__file__)

try:
    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", "6379")),
        db=int(os.getenv("REDIS_DB", "0")),
        password=os.getenv("REDIS_PASSWORD", None)
    )
    redis_client.ping()
    logger.info("Redis connection established")

except redis.exceptions.ConnectionError as e:
    logger.error("Redis connection failed: %s", e)
    redis_client = None