"""Resume business logic."""

import os
from sqlalchemy.orm import Session
from sqlalchemy import select

from models.resume import Resume


def save_resume(
    db: Session,
    user_id: int,
    filename: str,
    file_path: str,
    extracted_text: str | None,
) -> Resume:
    """Save resume metadata to the database."""
    resume = Resume(
        user_id=user_id,
        filename=filename,
        file_path=file_path,
        extracted_text=extracted_text,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume


def get_resume_by_user(db: Session, user_id: int) -> Resume | None:
    """Get the latest resume for a user."""
    statement = (
        select(Resume)
        .where(Resume.user_id == user_id)
        .order_by(Resume.created_at.desc())
    )
    return db.scalar(statement)


def delete_resume(db: Session, resume: Resume) -> None:
    """Delete resume from DB and disk."""
    # File bhi disk se hatao
    if os.path.exists(resume.file_path):
        os.remove(resume.file_path)

    db.delete(resume)
    db.commit()
