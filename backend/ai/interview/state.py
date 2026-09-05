"""State definition for the AgentVox interview graph."""

from typing import TypedDict


class InterviewState(TypedDict, total=False):
    """State carried through the interview workflow."""

    # Identity
    user_id: int
    interview_id: int

    # Context
    resume_context: dict
    job_context: dict
    competencies: list[dict]

    # Interview progress
    current_competency_index: int
    current_competency: str | None

    # Conversation
    conversation_history: list[dict]
    current_question: str | None
    candidate_answer: str | None

    # Response analysis
    claims: list[dict]
    evidence: list[dict]
    reasoning: dict
    confidence: float | None

    # Adaptive control
    next_action: str | None
    follow_up_context: str | None

    # Interview status
    interview_complete: bool
