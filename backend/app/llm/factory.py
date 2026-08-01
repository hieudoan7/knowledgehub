from functools import lru_cache

from app.llm.base import LLMService
from app.llm.ollama import OllamaService


@lru_cache(maxsize=1)
def get_llm_service() -> LLMService:
    """Return the configured LLM."""

    return OllamaService()
