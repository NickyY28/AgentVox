"""Pydantic schemas for Job Context APIs."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class JobContextCreate(BaseModel):
    """Payload for creating a job context."""

    target_role: str = Field(
        ...,
        min_length=2,
        max_length=255,
    )

    company_name: str | None = Field(
        default=None,
        max_length=255,
    )

    job_description: str = Field(
        ...,
        min_length=10,
    )


class JobContextUpdate(BaseModel):
    """Payload for updating a job context."""

    target_role: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    company_name: str | None = Field(
        default=None,
        max_length=255,
    )

    job_description: str | None = Field(
        default=None,
        min_length=10,
    )


class JobContextResponse(BaseModel):
    """Job context response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    target_role: str
    company_name: str | None
    job_description: str
    created_at: datetime
    updated_at: datetime
