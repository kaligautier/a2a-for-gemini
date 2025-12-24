"""
Agents package - Exposes all available agents.

This module centralizes access to all agents in the application:
- Quizz Agent: Generates quizzes and educational content
- Training Script Agent: Creates comprehensive training scripts
"""

from app.components.agents.quizz_agent.agent import (
    root_agent as quizz_agent,
)
from app.components.agents.training_script_agent.agent import (
    root_agent as training_script_agent,
)

__all__ = [
    "quizz_agent",
    "training_script_agent",
]
