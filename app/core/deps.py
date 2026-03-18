# deps.py
from __future__ import annotations

from typing import Generator

from sqlalchemy.orm import Session

from app.core.config import get_settings, Settings
from app.core.database import SessionLocal
from app.core.security import require_api_key as _require_api_key

_settings = get_settings()

def settings() -> Settings:
    return _settings

def require_api_key() -> None:
    # FastAPI will inject header into require_api_key via dependency call signature, but we keep it explicit:
    _require_api_key(_settings)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
