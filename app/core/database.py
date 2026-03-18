from __future__ import annotations

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import get_settings

Base = declarative_base()

def make_engine(db_url: str):
    return create_engine(db_url, pool_pre_ping=True)

def make_session_local(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

_settings = get_settings()
engine = make_engine(_settings.db_url)
SessionLocal = make_session_local(engine)

def init_db() -> None:
    env = os.getenv("APP_ENV", "dev")

    # register models
    from app.domain.entities.analysis_report import AnalysisReport  # noqa
    from app.domain.entities.predict_result import PredictResult  # noqa
    from app.domain.entities.ai_result import AiAnalysisResult  # noqa

    if env == "dev":
        Base.metadata.create_all(bind=engine)
        print("[DB] Auto create (dev)")
    else:
        print("[DB] Skip init (prod)")
