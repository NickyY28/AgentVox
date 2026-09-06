

"""Agora RTC token generation service."""

from datetime import datetime, timezone

from agora_token_builder import RtcTokenBuilder
from core.config import settings


class AgoraService:
    """Service for generating Agora RTC tokens."""

    def generate_rtc_token(self, channel_name: str, uid: int) -> str:
        if not settings.AGORA_APP_ID:
            raise ValueError("AGORA_APP_ID is not configured.")

        if not settings.AGORA_APP_CERTIFICATE:
            raise ValueError("AGORA_APP_CERTIFICATE is not configured.")

        if uid <= 0:
            raise ValueError("Agora UID must be greater than 0.")

        # AGORA_TOKEN_EXPIRE_SECONDS is a duration,
        # while buildTokenWithUid expects an absolute Unix timestamp.
        current_timestamp = int(datetime.now(timezone.utc).timestamp())

        privilege_expired_ts = (
            current_timestamp + settings.AGORA_TOKEN_EXPIRE_SECONDS
        )

        token = RtcTokenBuilder.buildTokenWithUid(
            settings.AGORA_APP_ID,
            settings.AGORA_APP_CERTIFICATE,
            channel_name,
            uid,
            1,  # Publisher
            privilege_expired_ts,
        )

        return token


agora_service = AgoraService()
