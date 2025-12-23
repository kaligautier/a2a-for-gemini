
resource "google_project_iam_member" "cloudbuild_artifactregistry_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${data.google_project.project.number}@cloudbuild.gserviceaccount.com"
}

# Grant service account user role to the default compute service account
# This allows Cloud Run to use the compute service account
resource "google_project_iam_member" "compute_service_account_user" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:build-learning-path-sa@${var.project_id}.iam.gserviceaccount.com"
}

data "google_project" "project" {
}

resource "google_cloud_run_v2_service" "default" {
  name     = var.service_name
  location = var.region

  # Depend on IAM permissions and secrets being set up first
  depends_on = [
    google_project_iam_member.cloudbuild_artifactregistry_writer,
    google_project_iam_member.compute_service_account_user,
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
    }
  }
}
