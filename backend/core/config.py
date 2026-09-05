"""Application settings loaded from environment variables / ``.env``."""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed runtime configuration for the AgentVox API."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    APP_NAME: str = "AgentVox"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS
    CORS_ORIGINS: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000", "http://localhost:8000"]
    )

    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str = "change-me-to-a-long-random-secret"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    # cookies
    COOKIE_DOMAIN: str | None = None
    COOKIE_HTTPONLY: bool = True
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: str = "lax"
    COOKIE_EXP: int = 30  # in minutes

    # Paths / logging
    UPLOAD_DIR: str = "uploads"
    LOG_DIR: str = "logs"
    LOG_LEVEL: str = "INFO"

    # LLM
    LLM_ENABLED: bool = False
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_API_KEY: str | None = None
    LLM_BASE_URL: str | None = None

    # Embeddings
    EMBEDDING_ENABLED: bool = False
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_API_KEY: str | None = None
    EMBEDDING_BASE_URL: str | None = None
    EMBEDDING_DIMENSIONS: int = 1536

    # RAG
    RAG_ENABLED: bool = False
    RAG_TOP_K: int = 5
    RAG_CHUNK_SIZE: int = 1000
    RAG_CHUNK_OVERLAP: int = 200

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: object) -> object:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
