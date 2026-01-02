"""Skills for the Training Script Agent."""

from a2a.types import AgentSkill

generic_training_script_skill = AgentSkill(
    id="generic_training_script_request",
    name="Gérer les demandes de scripts de formation",
    description=(
        "Traite toute demande concernant les scripts de formation : création sur un sujet, "
        "adaptation de niveau, structuration d'agenda, génération d'exercices, "
        "extraction d'objectifs, et création d'évaluations. "
        "Formulez votre demande en langage naturel."
    ),
    tags=["Formation", "Script", "Pédagogie", "Apprentissage", "Générique"],
    examples=[
        "Crée un script de formation d'une heure sur les bases de Python",
        "Adapte cette formation pour un public de managers",
        "Génère des exercices pratiques pour cette session sur Docker",
        "Quels sont les objectifs pédagogiques de ce document ?",
    ],
    inputSchema={
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "Votre demande complète en langage naturel concernant le script de formation."
            }
        },
        "required": ["prompt"]
    },
    outputSchema={
        "type": "object",
        "properties": {
            "response": {
                "type": "string",
                "description": "La réponse de l'agent, pouvant contenir le script, l'analyse ou les éléments de formation demandés."
            }
        }
    }
)


TRAINING_SCRIPT_AGENT_SKILLS = [generic_training_script_skill]
