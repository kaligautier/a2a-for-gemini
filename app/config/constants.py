from app.instructions.instructions_manager import InstructionsManager

instructions_manager = InstructionsManager()

AGENT_QUIZZ_DESCRIPTION = """Agent spécialisé dans la création de quiz interactifs basés sur des documents fournis par l'utilisateur."""
AGENT_QUIZZ_INSTRUCTION = instructions_manager.get_instructions("quizz_v1")

AGENT_TRAINING_SCRIPT_DESCRIPTION = """Agent spécialisé dans la création de scripts de formation pédagogiques et structurés."""
AGENT_TRAINING_SCRIPT_INSTRUCTION = instructions_manager.get_instructions("training_script_v1")