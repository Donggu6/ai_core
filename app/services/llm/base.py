# app/services/llm_base.py
from abc import ABC, abstractmethod
from typing import Any, Dict

class LlmClient(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs: Any) -> str:
        ...
