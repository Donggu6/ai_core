# app/services/llm_groq.py
import os

import requests  # pip install requests

from .base import LlmClient


class GroqClient(LlmClient):
    def __init__(self, model: str = "llama-3.1-8b-instant"):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = model
        # Groq는 OpenAI 호환 chat completions 엔드포인트를 사용
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

    def generate(self, prompt: str, **kwargs) -> str:
        if not self.api_key:
            return "[AI ERROR] GROQ_API_KEY not configured"

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

        resp = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
