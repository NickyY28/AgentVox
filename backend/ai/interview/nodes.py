"""LangGraph nodes for the AgentVox interview engine."""

from ai.interview.state import InterviewState
from ai.llm import get_llm
from schemas.interview import NextAction, ResponseAnalysis


def load_context(state: InterviewState) -> InterviewState:
    """Validate and initialize interview context."""

    competencies = state.get("competencies", [])
    if not competencies:
        raise ValueError("At least one competency is required.")

    state.setdefault("conversation_history", [])
    state.setdefault("current_competency_index", 0)
    state.setdefault("interview_complete", False)

    return state


def select_competency(state: InterviewState) -> InterviewState:
    """Select the competency currently being evaluated."""

    competencies = state.get("competencies", [])
    index = state.get("current_competency_index", 0)

    if index >= len(competencies):
        state["current_competency"] = None
        state["interview_complete"] = True

        return state

    competency = competencies[index]

    if isinstance(competency, dict):
        state["current_competency"] = competency.get("name")
    else:
        state["current_competency"] = str(competency)

    return state


def plan_interview(state: InterviewState) -> InterviewState:
    """Create an initial interview plan from context."""

    resume_context = state.get("resume_context", {})
    job_context = state.get("job_context",    {})
    competencies = state.get("competencies", [])

    prompt = f"""
        You are an expert technical interviewer.

        Create an interview strategy using the following context.

        Candidate resume:
        {resume_context}

        Target job:
        {job_context}

        Competencies:
        {competencies}

        The interview should:
        - evaluate the listed competencies,
        - use the candidate's actual experience,
        - prefer practical questions,
        - avoid irrelevant questions,
        - progressively collect evidence.

        Do not generate interview questions yet.
        Return a concise strategy.
    """

    response = get_llm().invoke(prompt)

    state["reasoning"] = {"interview_plan": response.content}

    return state


def generate_question(state: InterviewState) -> InterviewState:
    """Generate the next interview question."""

    competency = state.get("current_competency")

    if not competency:
        raise ValueError("No current competency selected.")

    resume_context = state.get("resume_context", {})
    job_context = state.get("job_context", {})
    history = state.get("conversation_history", [])
    follow_up_context = state.get("follow_up_context")

    if follow_up_context:
        question_instruction = f"""
            This is a targeted follow-up.

            The previous response requires more evidence.

            Reason:
            {follow_up_context}

            Ask ONE focused follow-up question.
            Do not repeat the previous question.
        """
    else:
        question_instruction = """
            Ask ONE strong question for the competency.
            Prefer a practical, experience-based question.
        """

        prompt = f"""
            You are conducting a professional technical interview.

            Current competency:
            {competency}

            Candidate resume:
            {resume_context}

            Target job:
            {job_context}

            Conversation history:
            {history}

            {question_instruction}

            Rules:
            - Ask exactly one question.
            - Do not provide an answer.
            - Do not ask multiple questions.
            - Keep it conversational.
            - Do not evaluate the candidate in the question.
        """

    response = get_llm().invoke(prompt)
    question = response.content.strip()
    state["current_question"] = question
    state["conversation_history"].append(
        {
            "role": "assistant",
            "content": question,
            "type": "question",
            "competency": competency,
        }
    )

    state["follow_up_context"] = None

    return state


def analyze_response(state: InterviewState) -> InterviewState:
    """Analyze the candidate's answer."""

    answer = state.get("candidate_answer")

    if not answer or not answer.strip():
        raise ValueError("Candidate answer cannot be empty.")

    competency = state.get("current_competency")

    question = state.get("current_question")

    prompt = f"""
        You are an expert technical interviewer.

        Analyze the candidate's answer against
        the current competency.

        Competency:
        {competency}

        Question:
        {question}

        Candidate answer:
        {answer}

        Evaluate:

        1. Claims made by the candidate.
        2. Evidence supporting each claim.
        3. Reasoning quality.
        4. Strengths.
        5. Weaknesses.
        6. Whether enough evidence exists to evaluate
           the competency.

        Important rules:

        - Never invent evidence.
        - Only use information explicitly provided
          by the candidate.
        - Clearly separate claims and evidence.
        - If evidence is missing, mark it as missing.
        - Do not judge accent, appearance, personality,
          filler words, or body language.
    """

    llm = get_llm().with_structured_output(ResponseAnalysis)

    analysis = llm.invoke(prompt)

    state["claims"] = [
        claim.model_dump()
        for claim in analysis.claims
    ]

    state["evidence"] = [
        {
            "claim": claim.claim,
            "evidence": claim.evidence,
        }
        for claim in analysis.claims
        if claim.evidence
    ]

    state["reasoning"] = {
        "summary": analysis.summary,
        "quality": analysis.reasoning_quality,
        "strengths": analysis.strengths,
        "weaknesses": analysis.weaknesses,
        "evidence_sufficiency": (
            analysis.evidence_sufficiency
        ),
    }

    state["confidence"] = analysis.confidence

    state["conversation_history"].append(
        {
            "role": "user",
            "content": answer,
            "type": "answer",
            "competency": competency,
        }
    )

    return state


def decide_next_action(state: InterviewState) -> InterviewState:
    """Decide the next step in the interview."""

    competencies = state.get(
        "competencies",
        [],
    )

    current_index = state.get(
        "current_competency_index",
        0,
    )

    analysis = state.get(
        "reasoning",
        {},
    )

    confidence = state.get(
        "confidence",
        0.0,
    )

    is_last_competency = (
        current_index >= len(competencies) - 1
    )

    prompt = f"""
        You are an adaptive technical interviewer.
        
        Current competency:
        {state.get("current_competency")}
        
        Response analysis:
        {analysis}
        
        Confidence:
        {confidence}
        
        Is this the final competency?
        {is_last_competency}
        
        Choose exactly one:
        
        follow_up
        - Important evidence is missing or unclear.
        
        next_competency
        - Current competency has enough evidence.
        
        complete
        - Current competency is evaluated and
          there are no competencies remaining.
        
        Rules:
        - Do not ask follow-ups without a reason.
        - Missing important evidence should trigger
          a follow-up.
        - Do not invent evidence.
    """

    llm = get_llm().with_structured_output(NextAction)
    decision = llm.invoke(prompt)
    action = decision.action

    # Safety rule:
    # Do not finish while competencies remain.
    if (
        action == "complete"
        and not is_last_competency
    ):
        action = "next_competency"

    state["next_action"] = action

    if action == "follow_up":
        state["follow_up_context"] = (
            decision.reason
        )

    return state


def prepare_next_competency(state: InterviewState) -> InterviewState:
    """Move to the next competency."""

    state["current_competency_index"] = (
        state.get("current_competency_index", 0) + 1)
    state["follow_up_context"] = None
    state["current_question"] = None
    state["candidate_answer"] = None

    return state


def complete_interview(state: InterviewState) -> InterviewState:
    """Mark the interview as completed."""

    state["interview_complete"] = True
    state["current_question"] = None

    return state


async def retrieve_relevant_context(state: dict) -> dict:
    """Retrieve resume/JD context relevant to current question."""

    from ai.rag.service import RAGService

    # db should be injected through runtime/config
    db = state.get("_db")

    if db is None:
        return {
            "retrieved_context": ""
        }

    rag = RAGService(db)

    question = state.get(
        "current_question",
        "",
    )

    context = await rag.retrieve_context(
        query=question,
        limit=5,
        resume_id=state.get("resume_id"),
        job_context_id=state.get(
            "job_context_id"
        ),
    )

    return {
        "retrieved_context": context
    }
