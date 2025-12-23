import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from google.genai import types

from app.utils.error import ConfigurationError


class Settings(BaseSettings):
    """
    Application settings with environment variable support.
    Configuration is loaded from:
    1. Environment variables
    2. .env file (in non-Docker environments)
    3. Default values defined below
    All settings are type-safe and validated by Pydantic.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

    if not os.getenv("DOCKER_ENV"):
        load_dotenv(find_dotenv(".env"))

    APP_NAME: str = Field(
        default="ADK_Agent_Template",
        description="Application name displayed in API documentation",
    )

    APP_DESCRIPTION: str = Field(
        default="Production-ready ADK agent template with best practices",
        description="Application description for API documentation",
    )

    APP_VERSION: str = Field(
        default="0.1.0",
        description="Application version",
    )

    PROJECT_NAME: str = Field(
        default="adk-agent-template",
        description="Project identifier used in paths and naming",
    )

    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )

    AGENT_NAME: str = Field(
        default="template_agent",
        description="Primary agent name",
    )

    @property
    def RETRY_CONFIG(self) -> types.HttpRetryOptions:
        """Get the HTTP retry configuration."""
        return types.HttpRetryOptions(
            attempts=5,
            exp_base=7,
            initial_delay=1,
            http_status_codes=[429, 500, 503, 504],
        )

    MODEL: str = Field(
        default="gemini-2.5-flash",
        description="AI model to use for the agent",
    )

    @property
    def AGENT_DIR(self) -> str:
        """Get the absolute path to the agents directory."""
        return str(Path(__file__).parent.parent / "components" / "agents")

    @property
    def INSTRUCTIONS_DIR(self) -> str:
        """Get the absolute path to the instructions templates directory."""
        return str(Path(__file__).parent.parent / "instructions" / "templates")

    GOOGLE_GENAI_USE_VERTEXAI: bool = Field(
        default=True,
        description="Enable Vertex AI for Google Generative AI (required)",
    )

    GOOGLE_CLOUD_PROJECT: str = Field(
        default="lil-onboard-gcp",
        description="GCP project ID (required)",
    )

    GOOGLE_CLOUD_LOCATION: str = Field(
        default="europe-west1",
        description="GCP region (e.g., us-central1, europe-west1)",
    )
    
    AGENT_ENGINE_ID: str = Field(
        default="",
        description=(
            "Vertex AI Agent Engine (Reasoning Engine) ID for managed sessions. "
            "Format: projects/PROJECT_ID/locations/LOCATION/reasoningEngines/ENGINE_ID"
        ),
    )
    USE_AGENT_ENGINE_SESSIONS: bool = Field(
        default=False,
        description="Enable Vertex AI Agent Engine Sessions (fully managed on GCP)",
    )

try:
    settings = Settings()
except ValidationError as e:
    raise ConfigurationError(
        message="Configuration validation failed",
        details={"pydantic_errors": e.errors()},
    ) from e