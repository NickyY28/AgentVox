from fastapi import APIRouter

from api.agora import agora
from api.auth import auth
from api.interview import interview
from api.job_context import job_context
from api.resume import router as resume_router

api_router = APIRouter()

api_router.include_router(auth)
api_router.include_router(resume_router)
api_router.include_router(job_context)
api_router.include_router(interview)
api_router.include_router(agora, prefix="/agora", tags=["Agora"])

__all__ = ["api_router"]
