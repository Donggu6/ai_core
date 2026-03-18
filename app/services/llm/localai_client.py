# app/services/llm_localai.py
import os
from openai import OpenAI
from .base import LlmClient

class LocalAiClient(LlmClient):
    def __init__(self, model: str = "local-llama"):
        self.client = OpenAI(
            api_key=os.getenv("LOCALAI_API_KEY", "dummy"),
            base_url=os.getenv("LOCALAI_BASE_URL", "http://localhost:3000/v1"),
        )
        self.model = model

    def generate(self, prompt: str, **kwargs) -> str:
        res = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an ecommerce AI consultant."},
                {"role": "user", "content": prompt},
            ],
            temperature=kwargs.get("temperature", 0.6),
        )
        return res.choices[0].message.content or ""
