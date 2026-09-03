from fastapi import APIRouter
from api.resume import router as resume_router
from api.auth import router as auth_router


api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(resume_router)

__all__ = ["api_router"]
