variable "project_id" {
  type        = string
  description = "GCP project identifier"
}

variable "region" {
  type        = string
  description = "GCP region"
  default     = "europe-west1"
}

variable "location" {
  type        = string
  description = "GCP location for multi-regional resources"
  default     = "EU"
}

variable "service_name" {
  type        = string
  description = "Cloud Run service name"
  default     = "a2a-for-gemini"
}

variable "image" {
  type        = string
  description = "Docker image for the Cloud Run service"
}

variable "alert_email" {
  type        = string
  description = "Email address for monitoring alerts"
  default     = "admin@chronodrive.com"
}
