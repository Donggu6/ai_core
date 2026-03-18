# app/core/config.py

import os
from dataclasses import dataclass
from dotenv import load_dotenv


def _load_env():
    # project root = .../ai-engine-platform
    here = os.path.abspath(os.path.dirname(__file__))

    # .../app/core -> .../app -> .../ai-engine -> platform root
    platform_root = os.path.abspath(os.path.join(here, "..", "..", ".."))

    env_path = os.path.join(platform_root, ".env")
    load_dotenv(env_path)


@dataclass(frozen=True)
class Settings:
    db_url: str
    api_key: str | None
    model_path: str
    default_platform: str

    grok_api_key: str | None
    grok_base_url: str
    grok_model: str


def get_settings() -> Settings:
    _load_env()

    db_url = os.getenv("AI_DB_URL") or os.getenv(
        "DB_URL",
        "postgresql+psycopg2://postgres:ai23@localhost:5432/ai_assistant",
    )

    api_key = os.getenv("AI_ENGINE_API_KEY")

    default_platform = os.getenv("AI_PLATFORM_DEFAULT", "sourcing")

    here = os.path.abspath(os.path.dirname(__file__))

    model_path = os.path.abspath(
        os.path.join(here, "..", "assets", "model.pkl")
    )

    grok_api_key = os.getenv("GROK_API_KEY")

    grok_base_url = os.getenv(
        "GROK_BASE_URL",
        "https://api.x.ai/v1"
    )

    grok_model = os.getenv(
        "GROK_MODEL",
        "grok-code-fast-1"
    )

    return Settings(
        db_url=db_url,
        api_key=api_key,
        model_path=model_path,
        default_platform=default_platform,
        grok_api_key=grok_api_key,
        grok_base_url=grok_base_url,
        grok_model=grok_model,
    )