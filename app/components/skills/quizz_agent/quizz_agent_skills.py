"""Skills for the Quizz Agent."""

from a2a.types import AgentSkill

generic_quizz_skill = AgentSkill(
    id="generic_quizz_request",
    name="Gérer les demandes de quiz",
    description=(
        "Traite toute demande concernant les quiz interactifs : création à partir d'un sujet, "
        "analyse de difficulté, génération de variations, et explication des réponses. "
        "Formulez votre demande en langage naturel."
    ),
    tags=["Quiz", "Formation", "Évaluation", "Pédagogie", "Générique"],
    examples=[
        "Crée un quiz de 5 questions sur l'histoire de l'art",
        "Analyse la difficulté de ce quiz pour des étudiants de première année",
        "Génère 2 autres versions de ce test sur la biologie",
        "Explique-moi les réponses du quiz précédent",
    ],
    inputSchema={
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "Votre demande complète en langage naturel concernant le quiz."
            }
        },
        "required": ["prompt"]
    },
    outputSchema={
        "type": "object",
        "properties": {
            "response": {
                "type": "string",
                "description": "La réponse de l'agent, pouvant contenir le quiz, l'analyse ou les explications demandées."
            }
        }
    }
)

QUIZZ_AGENT_SKILLS = [generic_quizz_skill]
