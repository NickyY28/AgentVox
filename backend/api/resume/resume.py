"""Resume API routes."""

import os
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from api.auth.auth_dependencies import get_current_user
from api.resume.resume_schemas import ResumeResponse
from api.resume.resume_service import save_resume, get_resume_by_user, delete_resume
from core.config import settings
from core.constants import ALLOWED_RESUME_EXTENSIONS, UPLOAD_MAX_SIZE_MB
from core.database import get_db
from models.user import User
from utils.file_parser import parse_resume

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/upload", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ResumeResponse:
    """Upload and parse a resume."""

    # 1. Extension validate karo
    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_RESUME_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {ALLOWED_RESUME_EXTENSIONS}",
        )

    # 2. File bytes pado
    file_bytes = await file.read()

    # 3. Size validate karo
    if len(file_bytes) > UPLOAD_MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size: {UPLOAD_MAX_SIZE_MB}MB",
        )

    # 4. Disk pe save karo
    upload_dir = Path(settings.UPLOAD_DIR) / str(current_user.id)
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / file.filename
    file_path.write_bytes(file_bytes)

    # 5. Text extract karo
    extracted_text = parse_resume(file.filename, file_bytes)

    # 6. DB me save karo
    resume = save_resume(
        db=db,
        user_id=current_user.id,
        filename=file.filename,
        file_path=str(file_path),
        extracted_text=extracted_text,
    )

    return resume


@router.get("/me", response_model=ResumeResponse)
def get_my_resume(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ResumeResponse:
    """Get current user's resume."""
    resume = get_resume_by_user(db, current_user.id)
    if resume is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No resume found")
    return resume


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_resume(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """Delete current user's resume."""
    resume = get_resume_by_user(db, current_user.id)
    if resume is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No resume found")
    delete_resume(db, resume)
