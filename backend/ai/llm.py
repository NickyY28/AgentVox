"""Centralized LLM configuration for AgentVox."""

from functools import lru_cache

from core.config import settings
from langchain_openai import ChatOpenAI


@lru_cache
def get_llm() -> ChatOpenAI:
    """Create and cache the configured LLM."""

    if not settings.LLM_ENABLED:
        raise RuntimeError("LLM integration is disabled.")

    if not settings.LLM_API_KEY:
        raise RuntimeError("LLM_API_KEY is not configured.")

    return ChatOpenAI(
        model=settings.LLM_MODEL,
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_BASE_URL,
        temperature=0,
    )
