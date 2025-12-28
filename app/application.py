"""FastAPI application factory."""

import logging


from fastapi import FastAPI
from fastapi.responses import JSONResponse
from google.adk.cli.fast_api import get_fast_api_app

from app.config.settings import settings
from app.utils.agent_card_generator import generate_all_agent_cards

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""

    generate_all_agent_cards()

    session_service_uri = None
    if settings.USE_AGENT_ENGINE_SESSIONS:
        if not settings.AGENT_ENGINE_ID:
            raise ValueError(
                "AGENT_ENGINE_ID must be set when USE_AGENT_ENGINE_SESSIONS is True."
            )
        APP_ID = settings.AGENT_ENGINE_ID.split('/')[-1]
        session_service_uri = f"agentengine://{APP_ID}"
        logger.info(f"Using Vertex AI Agent Engine Sessions: {APP_ID}")
    else:
        logger.info("Using InMemorySessionService (sessions not persisted)")

    app: FastAPI = get_fast_api_app(
        agents_dir=settings.AGENT_DIR,
        web=True,  # Enable web UI
        a2a=True,  # Enable A2A protocol support
        session_service_uri=session_service_uri,
    )

    app.title = settings.APP_NAME
    app.description = settings.APP_DESCRIPTION
    app.version = settings.APP_VERSION

    @app.get("/health", tags=["Health"], summary="Health Check")
    async def health_check() -> JSONResponse:
        """
        Health check endpoint for monitoring systems.

        Returns:
            JSONResponse: A simple JSON response with status "ok"
        """
        return JSONResponse(
            content={
                "status": "ok",
                "app": settings.APP_NAME,
                "version": settings.APP_VERSION,
            },
            status_code=200,
        )

    logger.info(
        f"FastAPI application created: {settings.APP_NAME} v{settings.APP_VERSION}"
    )
    logger.info(f"Agent directory: {settings.AGENT_DIR}")
    logger.info("Web UI enabled: True")

    return app
