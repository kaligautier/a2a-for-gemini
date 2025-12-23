# Google Cloud Secret Manager secrets
# These secrets are required by the Cloud Run service

resource "google_secret_manager_secret" "google_cloud_location" {
  secret_id = "GOOGLE_CLOUD_LOCATION"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "google_cloud_project" {
  secret_id = "GOOGLE_CLOUD_PROJECT"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "model" {
  secret_id = "MODEL"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "app_name" {
  secret_id = "APP_NAME"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "app_description" {
  secret_id = "APP_DESCRIPTION"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "app_version" {
  secret_id = "APP_VERSION"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "project_name" {
  secret_id = "PROJECT_NAME"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "log_level" {
  secret_id = "LOG_LEVEL"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "agent_name" {
  secret_id = "AGENT_NAME"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "google_genai_use_vertexai" {
  secret_id = "GOOGLE_GENAI_USE_VERTEXAI"

  replication {
    auto {}
  }
}

# Secret versions with initial values
resource "google_secret_manager_secret_version" "google_cloud_location" {
  secret      = google_secret_manager_secret.google_cloud_location.id
  secret_data = var.region
}

resource "google_secret_manager_secret_version" "google_cloud_project" {
  secret      = google_secret_manager_secret.google_cloud_project.id
  secret_data = var.project_id
}

resource "google_secret_manager_secret_version" "model" {
  secret      = google_secret_manager_secret.model.id
  secret_data = "gemini-2.0-flash-exp"
}

resource "google_secret_manager_secret_version" "app_name" {
  secret      = google_secret_manager_secret.app_name.id
  secret_data = var.service_name
}

resource "google_secret_manager_secret_version" "app_description" {
  secret      = google_secret_manager_secret.app_description.id
  secret_data = "A2A for Gemini - Agent to Agent communication"
}

resource "google_secret_manager_secret_version" "app_version" {
  secret      = google_secret_manager_secret.app_version.id
  secret_data = "1.0.0"
}

resource "google_secret_manager_secret_version" "project_name" {
  secret      = google_secret_manager_secret.project_name.id
  secret_data = var.service_name
}

resource "google_secret_manager_secret_version" "log_level" {
  secret      = google_secret_manager_secret.log_level.id
  secret_data = "INFO"
}

resource "google_secret_manager_secret_version" "agent_name" {
  secret      = google_secret_manager_secret.agent_name.id
  secret_data = "a2a-gemini-agent"
}

resource "google_secret_manager_secret_version" "google_genai_use_vertexai" {
  secret      = google_secret_manager_secret.google_genai_use_vertexai.id
  secret_data = "true"
}

# Grant Cloud Run service account access to secrets
resource "google_secret_manager_secret_iam_member" "cloud_run_secret_access" {
  for_each = toset([
    "GOOGLE_CLOUD_LOCATION",
    "GOOGLE_CLOUD_PROJECT",
    "MODEL",
    "APP_NAME",
    "APP_DESCRIPTION",
    "APP_VERSION",
    "PROJECT_NAME",
    "LOG_LEVEL",
    "AGENT_NAME",
    "GOOGLE_GENAI_USE_VERTEXAI",
  ])

  secret_id = each.value
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"

  depends_on = [
    google_secret_manager_secret.google_cloud_location,
    google_secret_manager_secret.google_cloud_project,
    google_secret_manager_secret.model,
    google_secret_manager_secret.app_name,
    google_secret_manager_secret.app_description,
    google_secret_manager_secret.app_version,
    google_secret_manager_secret.project_name,
    google_secret_manager_secret.log_level,
    google_secret_manager_secret.agent_name,
    google_secret_manager_secret.google_genai_use_vertexai,
  ]
}
