"""
Utility to generate agent.json cards for all registered agents.

This module provides functions to automatically generate agent cards
at application startup with dynamic URLs based on the deployment environment.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any

from app.config.settings import settings

logger = logging.getLogger(__name__)


def get_agent_directory(agent_name: str) -> Path | None:
    """
    Get the directory path for an agent by name.

    Returns None if directory not found.
    """
    agents_dir = Path(settings.AGENT_DIR)

    possible_names = [
        agent_name,
        f"{agent_name}_agent",
    ]

    for name in possible_names:
        agent_dir = agents_dir / name
        if agent_dir.exists():
            return agent_dir

    return None


def get_agent_description(agent_name: str, agent_instance: Any) -> str:
    """
    Extract description from agent instance or module docstring.

    Priority:
    1. agent_instance.description attribute
    2. First line of agent module's docstring
    3. Default fallback description
    """
    if hasattr(agent_instance, 'description') and agent_instance.description:
        return agent_instance.description

    try:
        import importlib
        module_name = f"app.components.agents.{agent_name}.agent"
        if not module_name.endswith('_agent.agent'):
            try:
                module = importlib.import_module(module_name)
            except ModuleNotFoundError:
                module_name = f"app.components.agents.{agent_name}_agent.agent"
                module = importlib.import_module(module_name)
        else:
            module = importlib.import_module(module_name)

        if module.__doc__:
            lines = [line.strip() for line in module.__doc__.strip().split('\n') if line.strip()]
            if lines:
                return lines[0]
    except Exception as e:
        logger.debug(f"Could not extract description from module docstring for {agent_name}: {e}")

    return f"{agent_name} agent"


def generate_agent_card(agent_name: str, agent_instance: Any) -> bool:
    """
    Generate agent.json file for a specific agent.

    Returns True if successful, False otherwise.
    """
    service_url = settings.get_agent_url(agent_name)

    if service_url.startswith("http://localhost"):
        k_service = os.getenv("K_SERVICE")
        if k_service:
            region = settings.GOOGLE_CLOUD_LOCATION
            service_url = f"https://{k_service}-HASH-{region}.a.run.app"

    description = get_agent_description(agent_name, agent_instance)

    agent_card = {
        "name": agent_name,
        "url": service_url,
        "description": description,
        "version": "1.0.0",
        "capabilities": {},
        "skills": [],
        "defaultInputModes": ["text/plain"],
        "defaultOutputModes": ["text/plain"],
        "supportsAuthenticatedExtendedCard": False,
    }

    agent_dir = get_agent_directory(agent_name)
    if not agent_dir:
        logger.warning(f"Could not find directory for agent '{agent_name}', skipping card generation")
        return False

    agent_json_path = agent_dir / "agent.json"

    try:
        with open(agent_json_path, "w") as f:
            json.dump(agent_card, f, indent=2)

        logger.info(f"✓ Generated {agent_json_path.relative_to(Path.cwd())}")
        return True
    except Exception as e:
        logger.error(f"Failed to write {agent_json_path}: {e}")
        return False


def generate_all_agent_cards() -> None:
    """Generate agent.json files for all registered agents."""

    from app.components.agents.registry import get_all_agents

    agents = get_all_agents()

    logger.info("Generating agent cards with custom URLs...")

    success_count = 0
    for agent_name, agent_instance in agents.items():
        agent_url = settings.get_agent_url(agent_name)
        logger.info(f"  • {agent_name}: {agent_url}")
        if generate_agent_card(agent_name, agent_instance):
            success_count += 1

    logger.info(f"✓ Generated {success_count}/{len(agents)} agent cards successfully")
