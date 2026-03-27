import os
import hmac
from fastapi import Header, HTTPException, status

API_KEY_HEADER = "X-API-Key"

def validate_api_key(x_api_key: str | None = Header(default=None)) -> str:
    """Validate API key with constant-time comparison."""

    expected_api_key = os.getenv("API_KEY")

    if not expected_api_key:
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