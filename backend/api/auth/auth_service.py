"""Authentication business logic."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.security import hash_password, verify_password
from models.user import User


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    """Find a user by email address."""
    statement = select(User).where(User.email == email)
    return db.scalar(statement)


def create_user(
    db: Session,
    email: str,
    password: str,
    full_name: str | None = None,
) -> User:
    """Create a new user."""

    user = User(
        email=email,
        password_hash=hash_password(password),
        full_name=full_name,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:
    """Authenticate a user using email and password."""

    user = get_user_by_email(db, email)

    if user is None:
        return None

    if not user.is_active:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user
