from fastapi import APIRouter

from api.auth import auth
from api.job_context import job_context
from api.resume import router as resume_router

api_router = APIRouter()

api_router.include_router(auth)
api_router.include_router(resume_router)
api_router.include_router(job_context)

__all__ = ["api_router"]
