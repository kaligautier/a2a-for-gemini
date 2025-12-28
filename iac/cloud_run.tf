data "google_project" "project" {
}

resource "google_cloud_run_v2_service" "default" {
  name     = var.service_name
  location = var.region

  # Depend on secrets being set up first
  depends_on = [
    google_secret_manager_secret_version.google_cloud_location,
    google_secret_manager_secret_version.google_cloud_project,
    google_secret_manager_secret_version.model,
    google_secret_manager_secret_version.app_name,
    google_secret_manager_secret_version.app_description,
    google_secret_manager_secret_version.app_version,
    google_secret_manager_secret_version.project_name,
    google_secret_manager_secret_version.log_level,
    google_secret_manager_secret_version.agent_name,
    google_secret_manager_secret_version.google_genai_use_vertexai,
    google_secret_manager_secret_version.rag_corpus_id,
    google_secret_manager_secret_version.a2a_base_url,
    google_secret_manager_secret_version.a2a_agent_quizz_agent_url,
    google_secret_manager_secret_version.a2a_agent_training_script_agent_url,
    google_secret_manager_secret_version.agent_engine_id_secret_version,
  ]

  template {
    scaling {
      min_instance_count = 0
      max_instance_count = 1
    }
    containers {
      image = var.image
      
      env {
        name = "GOOGLE_CLOUD_LOCATION"
        value_source {
          secret_key_ref {
            secret  = "GOOGLE_CLOUD_LOCATION"
            version = "latest"
          }
        }
      }
      env {
        name = "GOOGLE_CLOUD_PROJECT"
        value_source {
          secret_key_ref {
            secret  = "GOOGLE_CLOUD_PROJECT"
            version = "latest"
          }
        }
      }
      env {
        name = "MODEL"
        value_source {
          secret_key_ref {
            secret  = "MODEL"
            version = "latest"
          }
        }
      }  
      env {
        name = "APP_NAME"
        value_source {
          secret_key_ref {
            secret  = "APP_NAME"
            version = "latest"
          }
        }
      }
      env {
        name = "APP_DESCRIPTION"
        value_source {
          secret_key_ref {
            secret  = "APP_DESCRIPTION"
            version = "latest"
          }
        }
      }
      env {
        name = "APP_VERSION"
        value_source {
          secret_key_ref {
            secret  = "APP_VERSION"
            version = "latest"
          }
        }
      }
      env {
        name = "PROJECT_NAME"
        value_source {
          secret_key_ref {
            secret  = "PROJECT_NAME"
            version = "latest"
          }
        }
      }
      env {
        name = "LOG_LEVEL"
        value_source {
          secret_key_ref {
            secret  = "LOG_LEVEL"
            version = "latest"
          }
        }
      }
      env {
        name = "AGENT_NAME"
        value_source {
          secret_key_ref {
            secret  = "AGENT_NAME"
            version = "latest"
          }
        }
      }
      env {
        name = "GOOGLE_GENAI_USE_VERTEXAI"
        value_source {
          secret_key_ref {
            secret  = "GOOGLE_GENAI_USE_VERTEXAI"
            version = "latest"
          }
        }
      }
      env {
        name = "RAG_CORPUS_ID"
        value_source {
          secret_key_ref {
            secret  = "RAG_CORPUS_ID"
            version = "latest"
          }
        }
      }
      env {
        name = "A2A_BASE_URL"
        value_source {
          secret_key_ref {
            secret  = "A2A_BASE_URL"
            version = "latest"
          }
        }
      }
      env {
        name = "A2A_AGENT_QUIZZ_AGENT_URL"
        value_source {
          secret_key_ref {
            secret  = "A2A_AGENT_QUIZZ_AGENT_URL"
            version = "latest"
          }
        }
      }
      env {
        name = "A2A_AGENT_TRAINING_SCRIPT_AGENT_URL"
        value_source {
          secret_key_ref {
            secret  = "A2A_AGENT_TRAINING_SCRIPT_AGENT_URL"
            version = "latest"
          }
        }
      }
      env {
        name = "AGENT_ENGINE_ID"
        value_source {
          secret_key_ref {
            secret  = "AGENT_ENGINE_ID"
            version = "latest"
          }
        }
      }
    }
  }
}

# Output the service URL for reference
output "service_url" {
  description = "URL of the deployed Cloud Run service"
  value       = google_cloud_run_v2_service.default.uri
}

output "a2a_quizz_agent_url" {
  description = "A2A endpoint for the quizz agent"
  value       = "${google_cloud_run_v2_service.default.uri}/a2a/quizz_agent"
}

output "a2a_training_script_agent_url" {
  description = "A2A endpoint for the training script agent"
  value       = "${google_cloud_run_v2_service.default.uri}/a2a/training_script_agent"
}

output "project_id" {
  description = "GCP Project ID"
  value       = data.google_project.project.project_id
}

