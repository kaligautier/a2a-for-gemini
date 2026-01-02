"""
Skills configuration for A2A agents.

This module provides helper functions to retrieve skills for each agent.
Skills are defined in their respective agent's skills module under
`app/components/skills/<agent_name>/skills.py`.
"""

from a2a.types import AgentSkill

from app.components.skills.quizz_agent.quizz_agent_skills import QUIZZ_AGENT_SKILLS
from app.components.skills.training_script_agent.training_script_agent_skills import (
    TRAINING_SCRIPT_AGENT_SKILLS,
)


def get_skills_for_agent(agent_name: str) -> list[AgentSkill]:
    """
    Get the list of skills for a specific agent.

    Args:
        agent_name: Name of the agent

    Returns:
        List of AgentSkill objects for that agent

    Raises:
        ValueError: If agent_name is not recognized
    """
    skills_map = {
        "quizz_agent": QUIZZ_AGENT_SKILLS,
        "training_script_agent": TRAINING_SCRIPT_AGENT_SKILLS,
    }

    if agent_name not in skills_map:
        available = ", ".join(skills_map.keys())
        raise ValueError(
            f"Unknown agent '{agent_name}'. Available agents: {available}"
        )

    return skills_map[agent_name]


def get_all_skills() -> dict[str, list[AgentSkill]]:
    """
    Get all skills for all agents.

    Returns:
        Dictionary mapping agent names to their skills
    """
    return {
        "quizz_agent": QUIZZ_AGENT_SKILLS,
        "training_script_agent": TRAINING_SCRIPT_AGENT_SKILLS,
    }
