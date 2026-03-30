import os
import hmac
from fastapi import Header, HTTPException, status
from app.core.config import settings

API_KEY_HEADER = "X-API-Key"

def validate_api_key(x_api_key: str | None = Header(default=None)) -> str:
    """
    Validate API key with constant-time comparison.

    - dev: no API_KEY → skip validation
    - prod: no API_KEY → crash
    """

    configured_key = settings.api_key
    expected_api_key = configured_key.get_secret_value() if configured_key else None
    environment = settings.environment

    if not expected_api_key:
        if environment == "prod":
            raise RuntimeError("API_KEY not set")
        return "ok"

    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Missing {API_KEY_HEADER} header",
        )

    if not hmac.compare_digest(x_api_key, expected_api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid {API_KEY_HEADER} header"
        )

    return "ok"