"""Cookie utilities."""

from fastapi import Response

from core.config import settings


def set_cookie(
    response: Response,
    key: str,
    value: str,
    max_age: int = settings.COOKIE_EXP * 60,
) -> None:
    """Set a cookie in the response."""

    response.set_cookie(
        key=key,
        value=value,
        httponly=settings.COOKIE_HTTPONLY,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=max_age,
        path="/",
        domain=settings.COOKIE_DOMAIN,
    )


def clear_cookie(
    response: Response,
    key: str,
) -> None:
    """Clear a cookie from the response."""

    response.delete_cookie(
        key=key,
        httponly=settings.COOKIE_HTTPONLY,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        path="/",
        domain=settings.COOKIE_DOMAIN,
    )
