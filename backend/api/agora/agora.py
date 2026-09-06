"""Agora voice API."""

from core.config import settings
from fastapi import APIRouter, HTTPException, status
from services.agora_service import agora_service

from api.agora.agora_schemas import (
    AgoraTokenRequest,
    AgoraTokenResponse,
)

agora = APIRouter()


@agora.post("/token", response_model=AgoraTokenResponse)
async def generate_agora_token(
    payload: AgoraTokenRequest,
):
    """Generate an Agora RTC token."""

    if not settings.AGORA_APP_ID:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Agora is not configured.",
        )

    try:
        token = agora_service.generate_rtc_token(
            channel_name=payload.channel_name,
            uid=payload.uid,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    return AgoraTokenResponse(
        token=token,
        app_id=settings.AGORA_APP_ID,
        channel_name=payload.channel_name,
        uid=payload.uid,
        expires_in=settings.AGORA_TOKEN_EXPIRE_SECONDS,
    )
