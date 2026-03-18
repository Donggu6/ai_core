# health.py
from fastapi import APIRouter
from ..core.config import get_settings

router = APIRouter(tags=["Health"])
_settings = get_settings()

@router.get("/")
def root():
    return {"status": "ok", "service": "ai-engine"}

@router.get("/health")
def health():
    return {"status": "UP", "db": "configured", "api_key_required": bool(_settings.api_key)}
