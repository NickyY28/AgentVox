"""FastAPI dependencies for authenticated users."""

import jwt

from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from core.config import settings
from core.database import get_db
from core.security import decode_access_token
from models.user import User


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
    access_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> User:
    """Resolve the authenticated user from a bearer token or cookie."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = None

    # Prefer Authorization: Bearer <token>
    if credentials is not None:
        token = credentials.credentials

    # Fall back to access_token cookie
    elif access_token is not None:
        token = access_token

    if token is None:
        raise credentials_exception

    try:
        payload = decode_access_token(token)
        subject = payload.get("sub")

        if not subject:
            raise credentials_exception

        user_id = int(subject)

    except (ValueError, TypeError, jwt.InvalidTokenError):
        raise credentials_exception

    user = db.get(User, user_id)

    if user is None or not user.is_active:
        raise credentials_exception

    return user
