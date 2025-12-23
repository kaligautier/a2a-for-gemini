"""
Agent Registry - Central registry for all agents.

This module provides a dictionary mapping agent names to their instances,
making it easy to discover and access all available agents programmatically.
"""

from typing import Dict
from google.adk.agents import LlmAgent

# Import all agents
from app.components.agents.master_agent.agent import root_agent as master_agent
from app.components.agents.google_search_agent.agent import root_agent as google_search_agent
from app.components.agents.agent_with_bq_toolbox.agent import root_agent as agent_bq_with_mcp_toolbox
from app.components.agents.agent_with_native_bq.agent import root_agent as agent_with_native_bq
from app.components.agents.agent_with_pg.agent import root_agent as agent_with_pg
from app.components.agents.agent_with_tools.agent import root_agent as agent_with_tools
from app.components.agents.agent_with_vertex_ai_search.agent import root_agent as agent_with_vertex_ai_search
from app.components.agents.agent_with_vertex_rag.agent import root_agent as agent_with_vertex_rag
from app.components.agents.parralel_agent.agent import root_agent as parallel_agent
from app.components.agents.seq_and_loop_agent.agent import root_agent as seq_and_loop_agent


# Agent registry: maps agent names to agent instances
AGENTS_REGISTRY: Dict[str, LlmAgent] = {
    # Master orchestrator
    "master_agent": master_agent,

    # Specialized agents
    "google_search_agent": google_search_agent,
    "agent_bq_with_mcp_toolbox": agent_bq_with_mcp_toolbox,
    "agent_with_native_bq": agent_with_native_bq,
    "agent_with_pg": agent_with_pg,
    "agent_with_tools": agent_with_tools,
    "agent_with_vertex_ai_search": agent_with_vertex_ai_search,
    "agent_with_vertex_rag": agent_with_vertex_rag,

    # Workflow agents
    "parallel_agent": parallel_agent,
    "seq_and_loop_agent": seq_and_loop_agent,
}


def get_all_agents() -> Dict[str, LlmAgent]:
    """
    Get all registered agents.

    Returns:
        Dictionary mapping agent names to agent instances
    """
    return AGENTS_REGISTRY


def get_agent(agent_name: str) -> LlmAgent:
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
