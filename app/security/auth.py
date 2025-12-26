# app/security/auth.py
from fastapi import Header, HTTPException
from app.core.config import get_settings

def require_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")):
    settings = get_settings()

    if not settings.API_KEY:
        raise HTTPException(status_code=500, detail="API_KEY not configured")

    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return True