# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an A2A (Agent-to-Agent) protocol implementation for Gemini using Google ADK (Agent Development Kit). The project demonstrates deployment of multi-agent systems to Google Cloud Platform (GCP) with a complete CI/CD pipeline using Terraform and Cloud Build.

The pipeline: GitHub Repository → Cloud Build → Artifact Registry → Cloud Run

## Development Commands

### Environment Setup
```bash
# Install dependencies
uv sync

# Run the development server (default port 8085)
uv run uvicorn app.main:app --reload --port 8085
```

### Testing & Linting
```bash
# Run tests
uv run pytest

# Run linting
uv run ruff check .

# Run type checking
uv run mypy .

# Run spell checking
uv run codespell
```

### Docker
```bash
# Build Docker image locally
docker build -t a2a-for-gemini .

# Run Docker container
docker run -p 8080:8080 a2a-for-gemini
```

## Architecture

### Application Structure

The application follows a clean component-based architecture:

- **`app/application.py`**: FastAPI application factory. Creates the app using Google ADK's `get_fast_api_app()`, which automatically sets up routes for all agents in the agents directory. Can optionally use Vertex AI Agent Engine for managed sessions via `session_service_uri`.

- **`app/main.py`**: Entry point that instantiates the FastAPI app.

- **`app/config/settings.py`**: Centralized configuration using Pydantic settings. All environment variables are typed and validated. Key configs include:
  - GCP project settings (PROJECT, LOCATION)
  - Agent configuration (MODEL, AGENT_DIR)
  - A2A protocol settings (BASE_URL, AGENT_NAME)
  - Optional Agent Engine Sessions support

- **`app/components/agents/`**: All agent implementations. Each agent is automatically discovered by ADK via the registry.
  - `registry.py`: Central registry mapping agent names to instances
  - Each agent subdirectory contains its implementation

- **`app/instructions/`**: Jinja2 templates for agent instructions with frontmatter support via `InstructionsManager`

- **`app/components/callbacks/`**: ADK callbacks for logging and telemetry:
  - `before_agent.py`: Log when agents start
  - `after_agent.py`: Log when agents complete
  - `tool_callbacks.py`: Log tool invocations

- **`app/components/tools/`**: Custom tools for agents

### Multi-Agent Pattern Example

The `seq_and_loop_agent` demonstrates Google ADK's composition patterns:

- **SequentialAgent**: Executes sub-agents in sequence
- **LoopAgent**: Iteratively executes sub-agents until exit condition or max iterations
- **State Management**: Agents communicate via shared state using `output_key`
- **Exit Strategy**: Tools can break loops by calling specialized functions

Example flow:
1. InitialWriterAgent → writes draft (output_key="current_story")
2. LoopAgent (StoryRefinementLoop) begins:
   - CriticAgent → evaluates (output_key="critique")
   - RefinerAgent → improves or calls exit_loop() tool
3. Loop continues until approval or max_iterations reached

### CI/CD Pipeline (Cloud Build)

The `cloudbuild.yaml` defines a multi-stage pipeline:

1. **project-init**: Creates GCS bucket for Terraform state if needed
2. **create-ar-repo**: Creates Artifact Registry repository
3. **docker-build**: Builds container image
4. **docker-push**: Pushes to Artifact Registry
5. **terraform-init**: Initializes Terraform with backend config
6. **terraform-plan**: Plans infrastructure changes with image tag
7. **terraform-apply**: Applies changes to deploy to Cloud Run

All steps use `waitFor` to enforce proper ordering and parallelization.

### Infrastructure (Terraform)

Located in `iac/`:

- **backend.tf**: Remote state in GCS bucket
- **variables.tf**: Input variables (project_id, region, service_name, image)
- **cloud_run.tf**: Cloud Run service configuration
- **secrets.tf**: Secret Manager integration (API keys, credentials)
- **iam.tf**: IAM policies and service accounts

The Terraform expects the Docker image URL to be passed as a variable during apply.

### A2A Protocol

Agents are exposed via A2A protocol using Google ADK's `to_a2a()` utility. The root agent becomes accessible as an A2A endpoint, allowing agent-to-agent communication.

Configuration in `settings.py`:
- `A2A_BASE_URL`: Public URL where agent is accessible
- `A2A_AGENT_NAME`: Which agent to expose (must exist in registry)

## Key Concepts

### Agent Discovery
ADK automatically discovers agents by scanning the directory specified in `settings.AGENT_DIR` (app/components/agents). The registry in `app/components/agents/registry.py` maps agent names to instances for programmatic access.

### Configuration Loading
Settings use Pydantic for validation and support:
1. Environment variables (highest priority)
2. .env file (development)
3. Default values (fallback)

In Docker, `.env` loading is skipped (DOCKER_ENV flag).

### Logging
Structured logging is configured in `app/utils/logger.py` with callbacks providing trace context for agent execution flow.

### Instructions Templates
Use `InstructionsManager.get_instructions(template, **kwargs)` to load Jinja2 templates from `app/instructions/templates/`. Templates support frontmatter metadata and variable interpolation.

## GCP Environment

Default configuration:
- Project: `lil-onboard-gcp`
- Region: `europe-west1`
- Service: `a2a-for-gemini`

Update these in `app/config/settings.py` or via environment variables for your GCP project.
