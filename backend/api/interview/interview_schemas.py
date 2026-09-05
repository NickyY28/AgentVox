"""API request and response schemas for interviews."""

from pydantic import BaseModel, Field


class StartInterviewRequest(BaseModel):
    """Request to start an interview."""

    resume_context: dict = Field(
        default_factory=dict,
    )

    job_context: dict = Field(
        default_factory=dict,
    )

    competencies: list[dict]


class AnswerRequest(BaseModel):
    """Candidate answer submission."""

    answer: str = Field(
        min_length=1,
        max_length=10000,
    )
