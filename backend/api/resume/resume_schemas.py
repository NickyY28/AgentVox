"""Pydantic schemas for resume endpoints."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ResumeResponse(BaseModel):
    """What we return to the client after upload or fetch."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    extracted_text: str | None
    created_at: datetime
