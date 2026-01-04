"""FastAPI application factory."""

import json
import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from google.adk.cli.fast_api import get_fast_api_app

from app.config.settings import settings
from app.utils.agent_card_generator import generate_all_agent_cards

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""

    try:
        generate_all_agent_cards()
    except Exception as e:
        logger.error(f"FATAL: Failed to generate agent cards on startup: {e}", exc_info=True)
        # Re-raise the exception to prevent the app from starting in a broken state
        raise

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

    # Remove ADK's default agent-card route and replace with our own
    # to include inputSchema and outputSchema which the A2A SDK doesn't support
    routes_to_remove = []
    for route in app.router.routes:
        if hasattr(route, 'path') and route.path == "/a2a/quizz_agent/.well-known/agent-card.json":
            routes_to_remove.append(route)
    
    for route in routes_to_remove:
        app.router.routes.remove(route)
        logger.info(f"Removed ADK default route: {route.path}")

    @app.get("/a2a/quizz_agent/.well-known/agent-card.json", tags=["A2A"], summary="Quizz Agent Card Override")
    async def quizz_agent_card_override() -> JSONResponse:
        """
        Override the ADK-generated agent card to include inputSchema and outputSchema.
        The A2A SDK's AgentSkill model doesn't support these fields, so we serve
        the agent.json file directly.
        """
        agent_json_path = Path(settings.AGENT_DIR) / "quizz_agent" / "agent.json"
        
        try:
            with open(agent_json_path, "r", encoding="utf-8") as f:
                agent_card_data = json.load(f)
            return JSONResponse(content=agent_card_data, status_code=200)
        except Exception as e:
            logger.error(f"Failed to load agent card from {agent_json_path}: {e}")
            return JSONResponse(
                content={"error": "Agent card not found"},
                status_code=404
            )

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
