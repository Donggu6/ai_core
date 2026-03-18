# app/services/llm_openai.py
import os
from openai import OpenAI
from .base import LlmClient

class OpenAiClient(LlmClient):
    def __init__(self, model: str = "gpt-4.1-mini"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
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
