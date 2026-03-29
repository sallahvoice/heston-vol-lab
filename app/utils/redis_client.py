import hashlib
import json
import os
from typing import Any

import redis
from dotenv import load_dotenv

from app.core.logger import get_logger

load_dotenv()
logger = get_logger(__name__)


def _build_client() -> redis.Redis | None:
    try:
        client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            db=int(os.getenv("REDIS_DB", "0")),
            password=os.getenv("REDIS_PASSWORD", None)
        )
        client.ping()
        logger.info("Redis connection established")

    except redis.exceptions.RedisError as e:
        logger.error("Redis connection failed: %s", e)
        return None

redis_client = _build_client()


def build_cache_key(namespace: str, payload: dict[str, Any]) -> str:
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    return f"{namespace}:{digest}"


def get_json(key: str) -> dict[str, Any] | None:
    if redis_client is none:
        return None
    try:
        raw = redis_client.get(key)
        if raw is None:
            return None
        return json.loads(raw)
    except (redis.exceptions.RedisError, json.JSONDecodeError) as e:
        logger.warning("Redis GET failed for key %s: %s", key, e)
        return None


def set_json(key: str, value: dict[str, Any], ttl_seconds: int = 300) -> None:
    if redis_client is None:
        return
    try:
        redis_client.setex(key, ttl_seconds, json.dumps(value, default=str))
    except redis.exceptions.RedisError as e:
        logger.warning("Redis SET failed for key %s: %s", key, e)