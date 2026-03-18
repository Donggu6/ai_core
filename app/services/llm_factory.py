import os
from app.services.llm.base import LlmClient
from app.services.llm.openai_client import OpenAiClient
from app.services.llm.localai_client import LocalAiClient
from app.services.llm.groq_client import GroqClient
from app.services.llm.grok_client import GrokClient

def get_llm_client() -> LlmClient:
    provider = os.getenv("AI_PROVIDER", "local").lower()

    if provider == "openai":
        return OpenAiClient(model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))
    if provider == "groq":
        return GroqClient(model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"))
    if provider == "grok":
        return GrokClient(model=os.getenv("GROK_MODEL", "grok-code-fast-1"))
    return LocalAiClient(model=os.getenv("LOCALAI_MODEL", "local-llama"))
