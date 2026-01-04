"""Skills for the Quizz Agent."""

chat_interaction_skill = {
    "id": "chat_interaction",
    "name": "Discussion Expert",
    "description": "Canal principal. Envoyez votre message complet ici pour interagir avec l'agent (quiz ou questions).",
    "tags": ["Quiz", "Formation", "RAG", "Chat"],
    "examples": [
        "Crée un quiz de 5 questions sur l'histoire de l'art",
        "Analyse la difficulté de ce quiz pour des étudiants de première année",
        "Génère 2 autres versions de ce test sur la biologie",
        "Explique-moi les réponses du quiz précédent",
    ],
}

QUIZZ_AGENT_SKILLS = [chat_interaction_skill]
