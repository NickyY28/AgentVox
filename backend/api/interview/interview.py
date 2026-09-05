"""Interview API endpoints."""

from ai.interview.graph import interview_graph
from fastapi import APIRouter, HTTPException

from api.interview.interview_schemas import AnswerRequest, StartInterviewRequest

interview = APIRouter(prefix="/interview", tags=["Interview"])


# Temporary development-only session store.
# This will be replaced by PostgreSQL persistence.
_interview_sessions: dict[int, dict] = {}

_session_counter = 0


@interview.post("/start")
def start_interview(data: StartInterviewRequest):
    """Start a new interview session."""

    global _session_counter

    _session_counter += 1

    interview_id = _session_counter

    initial_state = {
        "user_id": 0,
        "interview_id": interview_id,
        "resume_context": data.resume_context,
        "job_context": data.job_context,
        "competencies": data.competencies,
        "current_competency_index": 0,
        "conversation_history": [],
        "interview_complete": False,
    }

    try:
        result = interview_graph.invoke(
            initial_state,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to start interview.",
        ) from exc

    _interview_sessions[interview_id] = result

    return {
        "interview_id": interview_id,
        "question": result.get(
            "current_question",
        ),
        "competency": result.get(
            "current_competency",
        ),
        "completed": result.get(
            "interview_complete",
            False,
        ),
    }


@interview.post("/{interview_id}/answer")
def submit_answer(interview_id: int, data: AnswerRequest):
    """Submit a candidate answer."""

    state = _interview_sessions.get(
        interview_id,
    )

    if state is None:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found.",
        )

    if state.get("interview_complete"):
        raise HTTPException(
            status_code=400,
            detail="Interview is already complete.",
        )

    state["candidate_answer"] = data.answer

    try:
        result = interview_graph.invoke(
            state,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to process answer.",
        ) from exc

    _interview_sessions[interview_id] = result

    return {
        "interview_id": interview_id,
        "question": result.get(
            "current_question",
        ),
        "competency": result.get(
            "current_competency",
        ),
        "next_action": result.get(
            "next_action",
        ),
        "confidence": result.get(
            "confidence",
        ),
        "reasoning": result.get(
            "reasoning",
        ),
        "claims": result.get(
            "claims",
            [],
        ),
        "evidence": result.get(
            "evidence",
            [],
        ),
        "completed": result.get(
            "interview_complete",
            False,
        ),
    }
