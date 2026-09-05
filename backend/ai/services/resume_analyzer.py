"""AI-powered resume analysis."""

from ai.llm import get_llm
from pydantic import BaseModel, Field


class ResumeAnalysis(BaseModel):
    """Structured resume analysis result."""

    summary: str = Field(
        description="A concise professional summary of the candidate."
    )

    skills: list[str] = Field(
        description="Technical and professional skills identified from the resume."
    )

    experience: list[str] = Field(
        description="Important work experience, internships, or projects."
    )

    education: list[str] = Field(
        description="Relevant educational qualifications."
    )

    achievements: list[str] = Field(
        description="Notable achievements, certifications, or accomplishments."
    )


def analyze_resume(resume_text: str) -> ResumeAnalysis:
    """Analyze resume text using the configured LLM."""

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        ResumeAnalysis
    )

    prompt = f"""
        Analyze the following candidate resume.

        Extract only information supported by the resume.

        Identify:
        - professional summary
        - technical and professional skills
        - work experience, internships, and projects
        - education
        - achievements and certifications

        Do not invent information.

        Resume:
        ---
        {resume_text}
        ---
    """

    return structured_llm.invoke(prompt)
