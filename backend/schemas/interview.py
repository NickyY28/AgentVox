"""Pydantic schemas for interview intelligence."""

from typing import Literal

from pydantic import BaseModel, Field


class Claim(BaseModel):
    """A claim extracted from a candidate response."""
    claim: str
    evidence: str | None = None


class ResponseAnalysis(BaseModel):
    """Structured analysis of a candidate response."""
    summary: str
    claims: list[Claim] = Field(default_factory=list)
    reasoning_quality: str
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    evidence_sufficiency: Literal["sufficient", "insufficient", "unclear"]
    confidence: float = Field(ge=0.0, le=1.0)


class NextAction(BaseModel):
    """Decision produced by the adaptive interviewer."""
    action: Literal["follow_up", "next_competency", "complete"]
    reason: str
