import uvicorn
from api import api_router
from core.config import settings
from core.constants import HEALTH_PATH
from core.database import Base, engine
from fastapi import FastAPI


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        description=("AgentVox backend API"),
        version="0.1.0",
        debug=settings.DEBUG,
    )

    Base.metadata.create_all(bind=engine)

    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    @app.get(HEALTH_PATH, tags=["health"])
    async def health_check() -> dict[str, str]:
        """Liveness probe for orchestrators and load balancers."""
        return {"status": "ok", "service": settings.APP_NAME}

    @app.get("/", tags=["root"])
    async def root() -> dict[str, str]:
        """API root welcome payload."""
        return {"message": f"Welcome to {settings.APP_NAME} API"}

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
