# IAM permissions for Cloud Build service account
# This service account needs permissions to manage IAM and deploy Cloud Run

# Permission to manage IAM bindings
resource "google_project_iam_member" "cloudbuild_iam_admin" {
  project = var.project_id
  role    = "roles/resourcemanager.projectIamAdmin"
  member  = "serviceAccount:build-learning-path-sa@${var.project_id}.iam.gserviceaccount.com"
}

# Permission to act as service accounts (required for Cloud Run deployment)
resource "google_project_iam_member" "cloudbuild_service_account_user" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:build-learning-path-sa@${var.project_id}.iam.gserviceaccount.com"
}

# Permission to manage Cloud Run services
resource "google_project_iam_member" "cloudbuild_run_admin" {
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:build-learning-path-sa@${var.project_id}.iam.gserviceaccount.com"
}

# Permission to access secrets (for Cloud Run environment variables)
resource "google_project_iam_member" "cloudbuild_secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:build-learning-path-sa@${var.project_id}.iam.gserviceaccount.com"
}

# Permission to manage secrets (to create them if they don't exist)
resource "google_project_iam_member" "cloudbuild_secret_admin" {
  project = var.project_id
  role    = "roles/secretmanager.admin"
  member  = "serviceAccount:build-learning-path-sa@${var.project_id}.iam.gserviceaccount.com"
}

# Permission to manage Artifact Registry
resource "google_project_iam_member" "cloudbuild_artifactregistry_admin" {
  project = var.project_id
  role    = "roles/artifactregistry.admin"
  member  = "serviceAccount:build-learning-path-sa@${var.project_id}.iam.gserviceaccount.com"
}

# Permissions for logging
resource "google_project_iam_member" "cloudbuild_logging_bucket_writer" {
  project = var.project_id
  role    = "roles/logging.bucketWriter"
  member  = "serviceAccount:build-learning-path-sa@${var.project_id}.iam.gserviceaccount.com"
}

resource "google_project_iam_member" "cloudbuild_logging_log_writer" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:build-learning-path-sa@${var.project_id}.iam.gserviceaccount.com"
}

resource "google_project_iam_member" "cloudbuild_logging_viewer" {
  project = var.project_id
  role    = "roles/logging.viewer"
  member  = "serviceAccount:build-learning-path-sa@${var.project_id}.iam.gserviceaccount.com"
}

# Permission to manage Cloud Storage
resource "google_project_iam_member" "cloudbuild_storage_admin" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:build-learning-path-sa@${var.project_id}.iam.gserviceaccount.com"
}

# IAM permissions for Cloud Run service account to access secrets
resource "google_secret_manager_secret_iam_member" "agent_engine_id_secret_accessor" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.agent_engine_id_secret.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}

# Permission to manage AI Platform resources
resource "google_project_iam_member" "cloudbuild_aiplatform_admin" {
  project = var.project_id
  role    = "roles/aiplatform.admin"
  member  = "serviceAccount:build-learning-path-sa@${var.project_id}.iam.gserviceaccount.com"
}

# Custom role for creating Reasoning Engines
resource "google_project_iam_custom_role" "reasoning_engine_creator" {
  project     = var.project_id
  role_id     = "reasoningEngineCreator"
  title       = "Reasoning Engine Creator"
  description = "Custom role to allow creation of Vertex AI Reasoning Engines"
  permissions = ["aiplatform.reasoningEngines.create"]

  depends_on = [
    google_project_iam_member.cloudbuild_iam_role_admin
  ]
}

resource "google_project_iam_member" "cloudbuild_reasoning_engine_creator" {
  project = var.project_id
  role    = google_project_iam_custom_role.reasoning_engine_creator.id
  member  = "serviceAccount:build-learning-path-sa@${var.project_id}.iam.gserviceaccount.com"
}

# Permission to manage custom IAM roles
resource "google_project_iam_member" "cloudbuild_iam_role_admin" {
  project = var.project_id
  role    = "roles/iam.roleAdmin"
  member  = "serviceAccount:build-learning-path-sa@${var.project_id}.iam.gserviceaccount.com"
}