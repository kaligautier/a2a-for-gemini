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

# Permission to write to Artifact Registry
resource "google_project_iam_member" "cloudbuild_artifactregistry_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
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
