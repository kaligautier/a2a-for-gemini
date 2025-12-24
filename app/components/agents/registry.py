"""
Agent Registry - Central registry for all agents.

This module provides a dictionary mapping agent names to their instances,
making it easy to discover and access all available agents programmatically.
"""

from typing import Dict

from google.adk.agents import Agent

from app.components.agents.quizz_agent.agent import (
    root_agent as quizz_agent,
)
from app.components.agents.training_script_agent.agent import (
    root_agent as training_script_agent,
)

AGENTS_REGISTRY: dict[str, Agent] = {
    "quizz_agent": quizz_agent,
    "training_script_agent": training_script_agent,
}


def get_all_agents() -> Dict[str, Agent]:
    """
    Get all registered agents.

    Returns:
        Dictionary mapping agent names to agent instances
    """
    return AGENTS_REGISTRY


def get_agent(agent_name: str) -> Agent:
    """
    Get a specific agent by name.

    Args:
        agent_name: Name of the agent to retrieve

    Returns:
        The requested agent instance

    Raises:
        KeyError: If agent name is not found in registry
    """
    if agent_name not in AGENTS_REGISTRY:
        available = ", ".join(AGENTS_REGISTRY.keys())
        raise KeyError(
            f"Agent '{agent_name}' not found. Available agents: {available}"
        )
    return AGENTS_REGISTRY[agent_name]


def list_agent_names() -> list[str]:
    """
    Get a list of all registered agent names.

    Returns:
        List of agent names
    """
    return list(AGENTS_REGISTRY.keys())
