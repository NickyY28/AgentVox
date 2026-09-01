"""Authentication API routes."""

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from utils.cookies import set_cookie, clear_cookie

from api.auth.auth_dependencies import get_current_user
from api.auth.auth_schemas import (
    LoginRequest,
    SignupRequest,
    TokenResponse,
    UserResponse,

)
from api.auth.auth_service import (
    authenticate_user,
    create_user,
    get_user_by_email,
)
from core.database import get_db
from core.security import create_access_token
from models.user import User
from core.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def signup(
    data: SignupRequest,
    db: Session = Depends(get_db),
) -> User:
    """Register a new user."""

    existing_user = get_user_by_email(db, data.email)

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        )

    return create_user(
        db=db,
        email=data.email,
        password=data.password,
        full_name=data.full_name,
    )


@router.post(
    "/login",

    response_model=TokenResponse,
)
def login(
    data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Authenticate a user and return an access token."""

    user = authenticate_user(
        db=db,
        email=data.email,
        password=data.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        subject=str(user.id),
    )

    set_cookie(
        response=response,
        key="access_token",
        value=access_token,

    )

    return TokenResponse(
        access_token=access_token,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
) -> User:
    """Return the currently authenticated user."""

    return current_user


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
def logout(response: Response) -> None:
    """Log out the current user by clearing the access token cookie."""

    clear_cookie(
        response=response,
        key="access_token",
    )
