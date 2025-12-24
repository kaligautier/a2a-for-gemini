# a2a-for-gemini
A2a for Chronodrive Gemini Entreprise

Les objectifs du projet sont de déployer un agent en a2a avec du terraform et toute la pipeline de ci/cd.

Je veux exposer plusieurs agents à travers le protocol a2a. 

Les agents sont connectés à Gemini Entreprise.

L'application propose 2 agents : 

1. Agent pour la génération de quizz basé sur une base vactoriel managé.
2. Génaration de script pour créer des formations en interne basé sur une base vactoriel managé.

# Infrastructure

Github reposotory -> Cloud Build -> Artifac Registry -> Cloud Run 

Pour lancer le projet il faut : 

`un sync`

Pour lancer ADK :

`uv run uvicorn app.main:app --reload --port 8085`


# Guide d'utilisation A2A

## Endpoint A2A

**URL de base en local **: `http://localhost:8085/a2a/seq_and_loop_agent`

**Agent Card**: `http://localhost:8085/a2a/seq_and_loop_agent/.well-known/agent-card.json`

## Format de requête JSON-RPC

### Méthode principale: `message/send`

Envoie un message à l'agent et attend la réponse complète.

### Exemple avec curl

```bash
curl -X POST http://localhost:8085/a2a/seq_and_loop_agent \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "message/send",
    "params": {
      "message": {
        "messageId": "msg-001",
        "role": "user",
        "parts": [
          {
            "text": "Écris une histoire sur un robot"
          }
        ]
      }
    },
    "id": 1
  }'
```

## Méthodes A2A disponibles

Le protocole A2A d'ADK supporte les méthodes suivantes:

### Messages
- **`message/send`** - Envoyer un message et attendre le résultat final
- **`message/stream`** - Envoyer un message et recevoir des événements en streaming

### Gestion des tâches
- **`tasks/get`** - Récupérer une tâche par ID
- **`tasks/cancel`** - Annuler une tâche en cours
- **`tasks/resubscribe`** - Se reconnecter au flux d'événements d'une tâche en streaming

### Configuration des notifications
- **`tasks/pushNotificationConfig/get`** - Obtenir la config de notification d'une tâche
- **`tasks/pushNotificationConfig/set`** - Définir la config de notification
- **`tasks/pushNotificationConfig/list`** - Lister les configs de notification
- **`tasks/pushNotificationConfig/delete`** - Supprimer une config de notification

### Carte étendue
- **`agent/authenticatedExtendedCard`** - Obtenir la carte agent étendue authentifiée

## Structure de la réponse

```json
{
  "id": 1,
  "jsonrpc": "2.0",
  "result": {
    "artifacts": [
      {
        "artifactId": "...",
        "parts": [
          {
            "kind": "text",
            "text": "L'histoire générée par l'agent"
          }
        ]
      }
    ],
    "contextId": "...",
    "history": [
      // Historique complet de l'exécution de l'agent
    ],
    "id": "...",
    "kind": "task",
    "metadata": {
      "adk_app_name": "seq_and_loop_agent",
      "adk_usage_metadata": {
        "totalTokenCount": 1686,
        // ...
      }
    },
    "status": {
      "state": "completed",
      "timestamp": "..."
    }
  }
}
```

Exemple pour pouvoir consommer un agent distant via a2a

```
prime_agent = RemoteA2aAgent(
    name="prime_agent",
    description="Agent for story refinement using sequential and loop patterns with iterative critique and improvement",
    agent_card=(
        f"{settings.A2A_BASE_URL}/.well-known/agent-card.json"
    ),
)

root_agent = LlmAgent(
    sub_agents=[prime_agent],
)
```