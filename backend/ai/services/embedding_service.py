"""Embedding service for AgentVox RAG."""

from functools import lru_cache

from core.config import settings
from langchain_openai import OpenAIEmbeddings


@lru_cache
def get_embeddings() -> OpenAIEmbeddings:
    """Create and cache the configured embedding model."""

    if not settings.EMBEDDING_ENABLED:
        raise RuntimeError("Embedding integration is disabled.")

    if not settings.EMBEDDING_API_KEY:
        raise RuntimeError(
            "EMBEDDING_API_KEY is not configured."
        )

    return OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        api_key=settings.EMBEDDING_API_KEY,
        base_url=settings.EMBEDDING_BASE_URL,
    )


def embed_text(text: str) -> list[float]:
    """Generate an embedding for a single text."""

    if not text.strip():
        raise ValueError("Cannot embed empty text.")

    return get_embeddings().embed_query(text)
