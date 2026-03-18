# ✅ 새 파일: app/services/llm_grok.py

import os
import requests
from app.core.config import get_settings
from .base import LlmClient

class GrokClient(LlmClient):

    def __init__(self, model: str | None = None):
        settings = get_settings()
        self.api_key = settings.grok_api_key or os.getenv("GROK_API_KEY")
        self.base_url = (settings.grok_base_url or os.getenv("GROK_BASE_URL", "https://api.x.ai/v1")).rstrip("/")
        self.model = model or settings.grok_model or os.getenv("GROK_MODEL", "grok-code-fast-1")

    def generate(self, prompt: str, **kwargs) -> str:
        if not self.api_key:
            return "[AI ERROR] GROK_API_KEY not configured"

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an ecommerce AI consultant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": kwargs.get("temperature", 0.6),
        }

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        except requests.HTTPError as e:
            print("[GROK ERROR]", resp.status_code, resp.text)
            raise