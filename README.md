# a2a-for-gemini
A2A pour Chronodrive Gemini Entreprise

Les objectifs du projet sont de déployer un agent en A2A avec Terraform et toute la pipeline CI/CD.

Ce projet expose plusieurs agents à travers le protocole A2A. Les agents sont connectés à Gemini Entreprise via Vertex AI et utilisent des bases vectorielles RAG managées.

## Agents Disponibles

L'application propose 2 agents :

### 1. **quizz_agent**
Agent spécialisé dans la création de quiz interactifs basés sur des documents fournis par l'utilisateur.

- **Endpoint**: `http://localhost:8085/a2a/quizz_agent`
- **Agent Card**: `http://localhost:8085/a2a/quizz_agent/.well-known/agent-card.json`

### 2. **training_script_agent**
Agent spécialisé dans la création de scripts de formation pédagogiques et structurés.

- **Endpoint**: `http://localhost:8085/a2a/training_script_agent`
- **Agent Card**: `http://localhost:8085/a2a/training_script_agent/.well-known/agent-card.json`

## Infrastructure

```
Github Repository → Cloud Build → Artifact Registry → Cloud Run
```

## Installation et Démarrage

### Synchroniser les dépendances

```bash
uv sync
```

### Lancer l'application ADK en local

```bash
uv run uvicorn app.main:app --reload --port 8085
```

Une fois démarré, vous pouvez accéder à :
- **Web UI**: `http://localhost:8085/web`
- **Documentation API**: `http://localhost:8085/docs`
- **Health Check**: `http://localhost:8085/health`

# Guide d'utilisation A2A

## Format de requête JSON-RPC

### Champs obligatoires

Toute requête JSON-RPC A2A doit contenir :
- **`id`** : Identifiant unique de la requête (nombre ou chaîne)
- **`messageId`** : Identifiant unique du message dans `params.message`

### Méthode principale: `message/send`

Envoie un message à l'agent et attend la réponse complète.

### Exemples avec curl

#### Exemple 1 : Agent Quizz

```bash
curl -X POST http://localhost:8085/a2a/quizz_agent \
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
            "text": "Crée un quiz sur la sécurité informatique"
          }
        ]
      }
    },
    "id": 1
  }'
```

#### Exemple 2 : Agent Training Script

```bash
curl -X POST http://localhost:8085/a2a/training_script_agent \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "message/send",
    "params": {
      "message": {
        "messageId": "msg-002",
        "role": "user",
        "parts": [
          {
            "text": "il y a quoi dans la charte formateur en interne"
          }
        ]
      }
    },
    "id": 2
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

## Consommer un agent distant via A2A

### Exemple : Utiliser un agent distant dans un autre agent

```python
from google.adk.agents import LlmAgent
from google.adk.agents.remote import RemoteA2aAgent
from app.config.settings import settings

# Créer une référence vers un agent distant
quizz_agent_remote = RemoteA2aAgent(
    name="quizz_agent",
    description="Agent spécialisé dans la création de quiz interactifs",
    agent_card=(
        f"{settings.get_agent_url('quizz_agent')}/a2a/quizz_agent/.well-known/agent-card.json"
    ),
)

# L'utiliser comme sous-agent
root_agent = LlmAgent(
    name="orchestrator",
    sub_agents=[quizz_agent_remote],
    # ...
)
```

### Configuration des URLs personnalisées

Vous pouvez définir des URLs personnalisées pour chaque agent via les variables d'environnement :

```bash
# URL de base (par défaut)
A2A_BASE_URL=http://localhost:8085

# URLs spécifiques par agent (optionnel)
A2A_AGENT_QUIZZ_AGENT_URL=https://quizz.example.com
A2A_AGENT_TRAINING_SCRIPT_AGENT_URL=https://training.example.com
```

## Configuration du projet

### Variables d'environnement principales

Créez un fichier `.env` à la racine du projet :

```bash
# Application
APP_NAME=a2a-for-gemini
LOG_LEVEL=INFO

# Google Cloud
GOOGLE_CLOUD_PROJECT=votre-projet-gcp
GOOGLE_CLOUD_LOCATION=europe-west1
GOOGLE_GENAI_USE_VERTEXAI=true

# Modèle AI
MODEL=gemini-1.5-flash-001

# A2A
A2A_BASE_URL=http://localhost:8085

# RAG Corpus
RAG_CORPUS_ID=projects/PROJECT_ID/locations/LOCATION/ragCorpora/CORPUS_ID

# Sessions managées (optionnel)
USE_AGENT_ENGINE_SESSIONS=false
# AGENT_ENGINE_ID=projects/PROJECT_ID/locations/LOCATION/reasoningEngines/ENGINE_ID

# Télémétrie (optionnel)
GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY=false
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=false
```

## Architecture du projet

```
app/
├── components/
│   ├── agents/           # Définition des agents
│   │   ├── quizz_agent/
│   │   │   ├── agent.py
│   │   │   └── .adk/
│   │   ├── training_script_agent/
│   │   │   ├── agent.py
│   │   │   └── .adk/
│   │   └── registry.py   # Registre central des agents
│   ├── tools/            # Outils personnalisés
│   │   └── custom/
│   │       └── vertex_ai_rag_retrieval_tool.py
│   └── callbacks/        # Callbacks pour logging et monitoring
├── config/
│   ├── settings.py       # Configuration centralisée
│   └── constants.py      # Constantes et instructions
├── instructions/         # Templates d'instructions
├── utils/               # Utilitaires
└── main.py              # Point d'entrée FastAPI
```

## Fonctionnalités

- **Multi-agents** : Support de plusieurs agents spécialisés
- **Protocole A2A** : Exposition complète via JSON-RPC 2.0
- **RAG** : Intégration avec Vertex AI RAG pour les bases vectorielles
- **Sessions managées** : Support optionnel des sessions via Agent Engine
- **Télémétrie** : OpenTelemetry pour monitoring et traces
- **Web UI** : Interface web pour tester les agents
- **API Documentation** : Swagger/OpenAPI automatique
- **Health Check** : Endpoint pour monitoring
- **CI/CD** : Pipeline complète avec Cloud Build
