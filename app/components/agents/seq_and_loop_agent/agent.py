"""
Story Refinement Pipeline - LoopAgent Pattern Example.

Ce fichier démontre l'utilisation de LoopAgent et SequentialAgent pour créer un pipeline
de raffinement itératif d'histoires avec critique et amélioration.

## Architecture Multi-Agents

**Pipeline global (SequentialAgent):**
1. InitialWriterAgent → Écrit le premier draft
2. StoryRefinementLoop → Boucle de raffinement (LoopAgent)

**Boucle de raffinement (LoopAgent):**
1. CriticAgent → Évalue l'histoire et fournit une critique
2. RefinerAgent → Améliore l'histoire OU appelle exit_loop() si approuvée

## Pattern LoopAgent

Le LoopAgent exécute ses sub-agents en boucle jusqu'à ce que:
- Un agent appelle un outil qui break la boucle (exit_loop())
- Le nombre max d'itérations est atteint (max_iterations)

## Flux de données (output_key)

Les agents communiquent via le state partagé avec output_key:
- InitialWriterAgent: output_key="current_story" → Crée l'histoire initiale
- CriticAgent: output_key="critique" → Génère la critique
- RefinerAgent: output_key="current_story" → Met à jour l'histoire raffinée

Dans les instructions, utilisez {current_story} et {critique} pour accéder au state.

## Exit Loop Strategy

Le RefinerAgent a un outil exit_loop() qui permet de sortir de la boucle:
- Si critique == "APPROVED" → Appelle exit_loop() → Break la boucle
- Sinon → Rafine l'histoire → Continue la boucle (prochain tour: CriticAgent)
"""

import logging

from google.adk.agents import LlmAgent
from google.adk.agents.loop_agent import LoopAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.tools.function_tool import FunctionTool

from app.components.callbacks.after_agent import log_agent_end
from app.components.callbacks.before_agent import log_agent_start
from app.components.callbacks.tool_callbacks import log_after_tool, log_before_tool
from app.config.settings import settings

logger = logging.getLogger(__name__)

def exit_loop():
    """
    Appeler cette fonction UNIQUEMENT quand la critique est 'APPROVED'.
    Indique que l'histoire est terminée et qu'aucune autre modification n'est nécessaire.
    """
    return {"status": "approved", "message": "Histoire approuvée. Sortie de la boucle de raffinement."}

initial_writer_agent = LlmAgent(
    name="InitialWriterAgent",
    model=settings.MODEL,
    instruction="""En te basant sur la demande de l'utilisateur, écris le premier draft d'une courte histoire (environ 100-150 mots).
    Retourne uniquement le texte de l'histoire, sans introduction ni explication.""",
    output_key="current_story",
    before_agent_callback=log_agent_start,
    after_agent_callback=log_agent_end,
    before_tool_callback=log_before_tool,
    after_tool_callback=log_after_tool,
)

refiner_agent = LlmAgent(
    name="RefinerAgent",
    model=settings.MODEL,
    instruction="""Tu es un raffineur d'histoires. Tu as accès au draft de l'histoire et à la critique.

    Draft de l'histoire: {current_story}
    Critique: {critique}

    Ta tâche est d'analyser la critique.
    - SI la critique est EXACTEMENT "APPROVED", tu DOIS appeler la fonction `exit_loop` et rien d'autre.
    - SINON, réécris l'histoire pour incorporer pleinement les feedbacks de la critique.""",
    output_key="current_story", 
    tools=[
        FunctionTool(exit_loop)
    ],
    before_agent_callback=log_agent_start,
    after_agent_callback=log_agent_end,
    before_tool_callback=log_before_tool,
    after_tool_callback=log_after_tool,
)

critic_agent = LlmAgent(
    name="CriticAgent",
    model=settings.MODEL,
    instruction="""Tu es un critique d'histoires constructif. Évalue l'histoire fournie ci-dessous.
    Histoire: {current_story}

    Évalue l'intrigue, les personnages et le rythme de l'histoire.
    - Si l'histoire est bien écrite et complète, tu DOIS répondre avec la phrase exacte: "APPROVED"
    - Sinon, fournis 2-3 suggestions spécifiques et actionnables pour l'améliorer.""",
    output_key="critique",  # Stocke le feedback dans le state
    before_agent_callback=log_agent_start,
    after_agent_callback=log_agent_end,
    before_tool_callback=log_before_tool,
    after_tool_callback=log_after_tool,
)

story_refinement_loop = LoopAgent(
    name="StoryRefinementLoop",
    sub_agents=[critic_agent, refiner_agent],
    max_iterations=2,
)

root_agent = SequentialAgent(
    name="StoryPipeline",
    sub_agents=[initial_writer_agent, story_refinement_loop],
)



