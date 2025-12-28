
import logging

from google.adk.agents import LlmAgent

from app.components.callbacks.after_agent import log_agent_end
from app.components.callbacks.before_agent import log_agent_start
from app.components.callbacks.tool_callbacks import log_after_tool, log_before_tool
from app.components.tools.custom.vertex_ai_rag_retrieval_tool import (
    vertex_ai_rag_retrieval_tool,
)
from app.config.constants import AGENT_QUIZZ_DESCRIPTION, AGENT_QUIZZ_INSTRUCTION
from app.config.settings import settings

logger = logging.getLogger(__name__)

root_agent = LlmAgent(
    name="quizz_agent",
    model=settings.MODEL,
    description=AGENT_QUIZZ_DESCRIPTION,
    instruction=AGENT_QUIZZ_INSTRUCTION,
    tools=[
        vertex_ai_rag_retrieval_tool
    ],
    before_agent_callback=log_agent_start,
    after_agent_callback=log_agent_end,
    before_tool_callback=log_before_tool,
    after_tool_callback=log_after_tool
)
