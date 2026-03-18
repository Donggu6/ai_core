# app/main.py

import os
from dotenv import load_dotenv

from fastapi import FastAPI

from app.core.database import init_db

from app.api.health import router as health_router
from app.api.predict import router as predict_router
from app.api.analyze import router as analyze_router
from app.api.coach import router as coach_router


load_dotenv()

app = FastAPI(
    title="AI Logic Engine",
    version="1.2.0",
    description="Platform-in-platform AI Engine"
)


@app.on_event("startup")
def startup():

    required = ["AI_DB_URL"]

    provider = os.getenv("AI_PROVIDER", "local").lower()

    provider_keys = {
        "openai": "OPENAI_API_KEY",
        "grok": "GROK_API_KEY",
        "groq": "GROQ_API_KEY",
    }

    if provider in provider_keys:
        required.append(provider_keys[provider])

    missing = [k for k in required if not os.getenv(k)]

    if missing:
        raise RuntimeError(f"[ENV ERROR] Missing: {missing}")

    print(f"[ENV] Loaded OK — provider={provider}")

    init_db()

    print("[DB] Initialized")


app.include_router(health_router, tags=["Health"])
app.include_router(predict_router, tags=["Predict"])
app.include_router(analyze_router, tags=["Analyze"])
app.include_router(coach_router, tags=["Coach"])