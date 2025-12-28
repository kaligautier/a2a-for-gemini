resource "google_vertex_ai_reasoning_engine" "agent_engine" {
  project      = var.project_id
  region       = var.region
  display_name = "Demo Agent Engine (Terraform)"
  description  = "Agent Engine for Session and Memory"
}

resource "google_secret_manager_secret" "agent_engine_id_secret" {
  project   = var.project_id
  secret_id = "AGENT_ENGINE_ID"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "agent_engine_id_secret_version" {
  secret      = google_secret_manager_secret.agent_engine_id_secret.id
  secret_data = google_vertex_ai_reasoning_engine.agent_engine.name
}