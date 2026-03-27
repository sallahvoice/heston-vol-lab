import os

from fastapi import Header, HTTPException, status

API_KEY_HEADER = "X-API-Key"

def validate_api_key(x_api_key: str | None = Header(default=None)) -> str:
    """Validate API key when API_KEY is configured in env
    if API_KEY is not set this dependency becomes a a no-op to avoid local dev blocking
    """

    expected_api_key = os.getenv("API_KEY")
    if not expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Missing {API_KEY_HEADER}  header"
        )

    if x_api_key !=expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid {API_KEY_HEADER} header",
        )

    return "ok"