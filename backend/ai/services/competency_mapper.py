"""AI-powered competency mapping."""

from ai.llm import get_llm
from pydantic import BaseModel, Field


class Competency(BaseModel):
    """A competency to evaluate during the interview."""

    name: str = Field(
        description="Name of the competency."
    )

    description: str = Field(
        description="What the competency represents."
    )

    importance: str = Field(
        description="Importance level: high, medium, or low."
    )


class CompetencyMapping(BaseModel):
    """Competencies derived from resume and job requirements."""

    competencies: list[Competency]


def map_competencies(
    resume_analysis: str,
    job_analysis: str,
) -> CompetencyMapping:
    """Map candidate and job information into interview competencies."""

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        CompetencyMapping
    )

    prompt = f"""
        You are designing a competency-based technical interview.

        Use the candidate resume analysis and job description analysis below.

        Identify the most relevant competencies that should be evaluated
        during the interview.

        Prioritize competencies that:
        1. Are important for the target role.
        2. Can be evaluated from candidate responses.
        3. Connect the candidate's background with the job requirements.

        Do not invent candidate experience.
        Do not claim that the candidate possesses a skill merely because
        the job description requires it.

        Candidate Resume Analysis:
        ---
        {resume_analysis}
        ---

        Job Description Analysis:
        ---
        {job_analysis}
        ---
    """

    return structured_llm.invoke(prompt)
