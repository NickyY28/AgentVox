"""Service layer for adaptive AgentVox interviews."""

from __future__ import annotations

from ai.interview.graph import interview_graph
from sqlalchemy.orm import Session


class InterviewService:
    """Run adaptive interview turns."""

    def __init__(self, db: Session) -> None:
        self.db = db

    async def start(
        self,
        *,
        user_id: int,
        interview_id: int,
        resume_id: int | None,
        job_context_id: int | None,
        resume_context: str,
        job_context: str,
        competencies: list[dict],
    ) -> dict:
        """Start an interview."""

        state = {
            "user_id": user_id,
            "interview_id": interview_id,
            "resume_id": resume_id,
            "job_context_id": job_context_id,
            "resume_context": resume_context,
            "job_context": job_context,
            "competencies": competencies,
            "conversation_history": [],
            "current_question": "",
            "candidate_answer": "",
            "claims": [],
            "evidence": [],
            "reasoning": "",
            "confidence": 0.0,
            "evidence_sufficient": False,
            "follow_up_count": 0,
            "max_follow_ups": 2,
            "current_competency_index": 0,
            "next_action": "generate_question",
            "completed": False,
        }

        result = await interview_graph.ainvoke(
            state
        )

        return result

    async def answer(
        self,
        state: dict,
        answer: str,
    ) -> dict:
        """Process one candidate answer."""

        state["candidate_answer"] = answer

        state["next_action"] = "record_answer"

        result = await interview_graph.ainvoke(
            state
        )

        return result
