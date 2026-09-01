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
            "http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8000"]
    )

    # Database
    DATABASE_URL: str = "postgresql+psycopg://postgres:root@localhost:5432/agentvox"

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

    # Future OpenAI / LLM integration (disabled by default)
    llm_enabled: bool = False
    openai_model: str = "gpt-4o-mini"
    openai_api_key: str | None = None

    # WebSocket realtime
    ws_heartbeat_interval_seconds: int = 30
    ws_heartbeat_timeout_seconds: int = 90

    # Future Redis
    redis_enabled: bool = False
    redis_url: str = "redis://localhost:6379/0"

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
