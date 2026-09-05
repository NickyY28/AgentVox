"""AI-powered job description analysis."""

from ai.llm import get_llm
from pydantic import BaseModel, Field


class JobAnalysis(BaseModel):
    """Structured job description analysis result."""

    role: str = Field(
        description="The primary job role."
    )

    required_skills: list[str] = Field(
        description="Skills explicitly required for the role."
    )

    preferred_skills: list[str] = Field(
        description="Skills listed as preferred or desirable."
    )

    responsibilities: list[str] = Field(
        description="Major responsibilities of the role."
    )

    qualifications: list[str] = Field(
        description="Required education, experience, or qualifications."
    )


def analyze_job_description(
    job_description: str,
) -> JobAnalysis:
    """Analyze a job description using the configured LLM."""

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        JobAnalysis
    )

    prompt = f"""
        Analyze the following job description.

        Extract only information explicitly supported by the job description.

        Identify:
        - primary role
        - required skills
        - preferred skills
        - major responsibilities
        - qualifications

        Do not invent requirements.

        Job Description:
        ---
        {job_description}
        ---
    """

    return structured_llm.invoke(prompt)
