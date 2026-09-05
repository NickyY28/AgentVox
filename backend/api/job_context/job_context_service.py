"""Business logic for Job Context."""

from models.job_context import JobContext
from sqlalchemy import select
from sqlalchemy.orm import Session


def create_job_context(
    db: Session,
    user_id: int,
    target_role: str,
    company_name: str | None,
    job_description: str,
) -> JobContext:
    """Create a new job context for a user."""

    job_context = JobContext(
        user_id=user_id,
        target_role=target_role,
        company_name=company_name,
        job_description=job_description,
    )

    db.add(job_context)
    db.commit()
    db.refresh(job_context)

    return job_context


def get_job_context(
    db: Session,
    user_id: int,
) -> JobContext | None:
    """Get the user's job context."""

    statement = (
        select(JobContext)
        .where(JobContext.user_id == user_id)
        .order_by(JobContext.created_at.desc())
    )

    return db.scalars(statement).first()


def update_job_context(
    db: Session,
    job_context: JobContext,
    target_role: str | None = None,
    company_name: str | None = None,
    job_description: str | None = None,
) -> JobContext:
    """Update an existing job context."""

    if target_role is not None:
        job_context.target_role = target_role

    if company_name is not None:
        job_context.company_name = company_name

    if job_description is not None:
        job_context.job_description = job_description

    db.commit()
    db.refresh(job_context)

    return job_context


def delete_job_context(
    db: Session,
    job_context: JobContext,
) -> None:
    """Delete an existing job context."""

    db.delete(job_context)
    db.commit()
