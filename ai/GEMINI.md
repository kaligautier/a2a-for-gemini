# a2a-for-gemini / porte-folio-manager

## Project Overview

This project is a FastAPI-based platform for deploying and managing Generative AI agents using Google Cloud's Vertex AI and the Google Agent Development Kit (ADK). It includes a complete CI/CD pipeline and Infrastructure as Code (IaC) setup using Terraform.

The application serves as a template and runtime for "Agent-to-Agent" (A2A) interactions, supporting various capabilities including RAG (Retrieval Augmented Generation), BigQuery integration, and external tool usage via the Model Context Protocol (MCP).

## Tech Stack

*   **Language:** Python 3.10+
*   **Web Framework:** FastAPI
*   **Package Manager:** `uv`
*   **Infrastructure:** Terraform
*   **Cloud Provider:** Google Cloud Platform (GCP)
*   **AI/ML:** Google Vertex AI (Gemini Models), LangChain (via ADK integration)

## Directory Structure

```text
├── app/
│   ├── components/
│   │   ├── agents/      # Agent implementations (logic, prompts)
│   │   ├── tools/       # Custom tools and MCP integrations
│   │   └── plugins/     # Plugins for extending functionality
│   ├── config/          # Configuration settings (Pydantic based)
│   ├── instructions/    # Jinja2 templates for system instructions
│   ├── services/        # Business logic services
│   ├── utils/           # Shared utilities (logging, error handling)
│   ├── main.py          # Application entry point
│   └── application.py   # App factory
├── iac/                 # Terraform Infrastructure as Code
│   ├── init/            # Initialization scripts
│   └── ...              # .tf files
├── cloudbuild.yaml      # Google Cloud Build configuration
└── pyproject.toml       # Project dependencies and metadata
```

## Setup & Installation

### Prerequisites

*   **Python 3.10+**
*   **uv** (Python package manager): [Installation Guide](https://github.com/astral-sh/uv)
*   **Google Cloud SDK (`gcloud`)**: Authenticated with your GCP project.
*   **Terraform**: For infrastructure deployment.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd a2a-for-gemini
    ```

2.  **Install dependencies:**
    This project uses `uv` for dependency management.
    ```bash
    uv sync
    ```

3.  **Environment Configuration:**
    Create a `.env` file in the root directory. The configuration is managed by `app/config/settings.py`. Key variables include:

    ```ini
    GOOGLE_CLOUD_PROJECT=your-project-id
    GOOGLE_CLOUD_LOCATION=europe-west1
    MODEL=gemini-2.5-flash
    # See app/config/settings.py for all available options
    ```

## Running the Application

To start the local development server with hot reload:

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.
API Documentation (Swagger UI) is available at `http://localhost:8000/docs`.

## Infrastructure Deployment

The project uses Terraform to provision necessary GCP resources.

1.  **Initialize Infrastructure:**
    The initialization script creates the Terraform state bucket.
    ```bash
    cd iac/init
    chmod +x init.sh
    ./init.sh <PROJECT_ID>
    ```

2.  **Deploy with Terraform:**
    ```bash
    cd iac
    terraform init -backend-config=init/backend.tfvars
    terraform plan -var project_id=<PROJECT_ID>
    terraform apply -var project_id=<PROJECT_ID>
    ```

## Development Conventions

*   **Code Style:** The project enforces code quality using `ruff` and `mypy`.
    *   Linting: `uv run ruff check .`
    *   Type Checking: `uv run mypy .`
*   **Agents:** New agents should be added to `app/components/agents/` and registered in `app/components/agents/registry.py`.
*   **Dependencies:** Manage dependencies using `pyproject.toml`. Run `uv sync` after making changes.
