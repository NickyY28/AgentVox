import uvicorn
from fastapi import FastAPI
from core.config import settings
from core.constants import HEALTH_PATH
from core.database import Base, engine

from api import api_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        description=("AgentVox backend API"),
        version="0.1.0",
        debug=settings.debug,
    )

    Base.metadata.create_all(bind=engine)

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.get(HEALTH_PATH, tags=["health"])
    async def health_check() -> dict[str, str]:
        """Liveness probe for orchestrators and load balancers."""
        return {"status": "ok", "service": settings.app_name}

    @app.get("/", tags=["root"])
    async def root() -> dict[str, str]:
        """API root welcome payload."""
        return {"message": f"Welcome to {settings.app_name} API"}

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
