# # """Agora RTC token generation service."""

# # from datetime import datetime, timezone

# # from agora_token_builder import RtcTokenBuilder
# # from core.config import settings


# # class AgoraService:
# #     """Service responsible for generating Agora RTC tokens."""

# #     @staticmethod
# #     def generate_rtc_token(channel_name: str, uid: int, expire_seconds: int | None = None) -> str:

# #         if not settings.AGORA_APP_ID:

# #             raise ValueError("AGORA_APP_ID is not configured.")

# #         if not settings.AGORA_APP_CERTIFICATE:

# #             raise ValueError("AGORA_APP_CERTIFICATE is not configured.")

# #         expire_seconds = (
# #             expire_seconds or settings.AGORA_TOKEN_EXPIRE_SECONDS
# #         )

# #         current_timestamp = int(
# #             datetime.now(timezone.utc).timestamp()
# #         )

# #         privilege_expired_ts = (
# #             current_timestamp + expire_seconds
# #         )

# #         token = RtcTokenBuilder.buildTokenWithUid(
# #             settings.AGORA_APP_ID,
# #             settings.AGORA_APP_CERTIFICATE,
# #             channel_name,
# #             uid,
# #             1,  # Publisher
# #             privilege_expired_ts,
# #         )

# #         return token


# # agora_service = AgoraService()


# """Agora RTC token generation service."""

# from __future__ import annotations

# from agora_token_builder import Role_Publisher, RtcTokenBuilder
# from core.config import settings


# class AgoraService:
#     """Generate Agora RTC tokens."""

#     def generate_rtc_token(self, channel_name: str, uid: int) -> str:
#         if not settings.AGORA_APP_ID:
#             raise ValueError("AGORA_APP_ID is not configured.")

#         if not settings.AGORA_APP_CERTIFICATE:
#             raise ValueError("AGORA_APP_CERTIFICATE is not configured.")

#         if uid <= 0:
#             raise ValueError("Agora UID must be greater than 0.")

#         token = RtcTokenBuilder.build_token_with_uid(
#             settings.AGORA_APP_ID,
#             settings.AGORA_APP_CERTIFICATE,
#             channel_name,
#             uid,
#             Role_Publisher,
#             settings.AGORA_TOKEN_EXPIRE_SECONDS,
#             settings.AGORA_TOKEN_EXPIRE_SECONDS,
#         )

#         return token


# agora_service = AgoraService()


"""Agora RTC token generation service."""

from agora_token_builder import RtcTokenBuilder
from core.config import settings


class AgoraService:
    """Service for generating Agora RTC tokens."""

    def generate_rtc_token(
        self,
        channel_name: str,
        uid: int,
    ) -> str:
        if not settings.AGORA_APP_ID:
            raise ValueError("AGORA_APP_ID is not configured.")

        if not settings.AGORA_APP_CERTIFICATE:
            raise ValueError("AGORA_APP_CERTIFICATE is not configured.")

        if uid <= 0:
            raise ValueError("Agora UID must be greater than 0.")

        expiration = settings.AGORA_TOKEN_EXPIRE_SECONDS

        token = RtcTokenBuilder.buildTokenWithUid(
            settings.AGORA_APP_ID,
            settings.AGORA_APP_CERTIFICATE,
            channel_name,
            uid,
            1,  # Role_Publisher
            expiration,
        )

        return token


agora_service = AgoraService()
