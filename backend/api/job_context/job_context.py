"""Job Context API routes."""

from api.auth.auth_dependencies import get_current_user
from core.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from models.user import User
from sqlalchemy.orm import Session

from .job_context_schemas import (
    JobContextCreate,
    JobContextResponse,
    JobContextUpdate,
)
from .job_context_service import (
    create_job_context,
    delete_job_context,
    get_job_context,
    update_job_context,
)

job_context = APIRouter(
    prefix="/job-context",
    tags=["Job Context"],
)


@job_context.post(
    "",
    response_model=JobContextResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job_context_endpoint(
    payload: JobContextCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JobContextResponse:
    """Create a job context for the current user."""

    existing_context = get_job_context(
        db=db,
        user_id=current_user.id,
    )

    if existing_context:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Job context already exists.",
        )

    return create_job_context(
        db=db,
        user_id=current_user.id,
        target_role=payload.target_role,
        company_name=payload.company_name,
        job_description=payload.job_description,
    )


@job_context.get(
    "/me",
    response_model=JobContextResponse,
)
def get_my_job_context(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JobContextResponse:
    """Get the current user's job context."""

    job_context = get_job_context(
        db=db,
        user_id=current_user.id,
    )

    if not job_context:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job context not found.",
        )

    return job_context


@job_context.put(
    "/me",
    response_model=JobContextResponse,
)
def update_my_job_context(
    payload: JobContextUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JobContextResponse:
    """Update the current user's job context."""

    job_context = get_job_context(
        db=db,
        user_id=current_user.id,
    )

    if not job_context:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job context not found.",
        )

    return update_job_context(
        db=db,
        job_context=job_context,
        target_role=payload.target_role,
        company_name=payload.company_name,
        job_description=payload.job_description,
    )


@job_context.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_my_job_context(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete the current user's job context."""

    job_context = get_job_context(
        db=db,
        user_id=current_user.id,
    )

    if not job_context:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job context not found.",
        )

    delete_job_context(
        db=db,
        job_context=job_context,
    )
