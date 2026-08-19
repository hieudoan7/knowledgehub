from functools import lru_cache

from app.core.config import settings
from app.llm.base import LLMService
from app.llm.ollama import OllamaService
from app.llm.bedrock import BedrockService


@lru_cache(maxsize=1)
def get_llm_service() -> LLMService:
    """Return the configured LLM service."""

    provider = settings.LLM_PROVIDER.lower()

    if provider == "ollama":
        return OllamaService()
    
    if provider == "bedrock":
        return BedrockService()

    raise ValueError(
        f"Unsupported LLM provider: {settings.LLM_PROVIDER}"
    )