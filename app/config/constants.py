from app.instructions.instructions_manager import InstructionsManager

instructions_manager = InstructionsManager()

AGENT_MASTER_DESCRIPTION = """Analyste de données BigQuery - Expert en interrogation et analyse de grands ensembles de données."""
AGENT_MASTER_INSTRUCTION = instructions_manager.get_instructions("master_v1")
