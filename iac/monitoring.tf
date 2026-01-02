# Monitoring and alerting for A2A agents

# Notification channel for alerts
resource "google_monitoring_notification_channel" "email" {
  display_name = "A2A Agents Email Alerts"
  type         = "email"
  project      = var.project_id

  labels = {
    email_address = var.alert_email
  }

  enabled = true
}

# Alert: High request count (potential abuse)
resource "google_monitoring_alert_policy" "high_request_count" {
  display_name = "A2A Agents - High Request Count"
  project      = var.project_id
  combiner     = "OR"

  conditions {
    display_name = "Request count exceeds 100 req/min"

    condition_threshold {
      filter          = "resource.type=\"cloud_run_revision\" AND resource.labels.service_name=\"${var.service_name}\" AND metric.type=\"run.googleapis.com/request_count\""
      duration        = "60s"
      comparison      = "COMPARISON_GT"
      threshold_value = 100

      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_RATE"
      }
    }
  }

  documentation {
    content   = "Le service A2A reçoit plus de 100 requêtes par minute. Vérifiez s'il y a un abus ou une attaque en cours."
    mime_type = "text/markdown"
  }

  notification_channels = [
    google_monitoring_notification_channel.email.name
  ]

  alert_strategy {
    auto_close = "1800s"  # Auto-close après 30 minutes
  }
}

# Alert: High error rate
resource "google_monitoring_alert_policy" "high_error_rate" {
  display_name = "A2A Agents - High Error Rate"
  project      = var.project_id
  combiner     = "OR"

  conditions {
    display_name = "Error rate exceeds 10%"

    condition_threshold {
      filter          = "resource.type=\"cloud_run_revision\" AND resource.labels.service_name=\"${var.service_name}\" AND metric.type=\"run.googleapis.com/request_count\" AND metric.labels.response_code_class=\"5xx\""
      duration        = "120s"
      comparison      = "COMPARISON_GT"
      threshold_value = 10

      aggregations {
        alignment_period     = "60s"
        per_series_aligner   = "ALIGN_RATE"
        cross_series_reducer = "REDUCE_SUM"
      }
    }
  }

  documentation {
    content   = "Le service A2A rencontre un taux d'erreur élevé (>10%). Vérifiez les logs Cloud Run pour diagnostiquer."
    mime_type = "text/markdown"
  }

  notification_channels = [
    google_monitoring_notification_channel.email.name
  ]
}

# Alert: High memory usage
resource "google_monitoring_alert_policy" "high_memory_usage" {
  display_name = "A2A Agents - High Memory Usage"
  project      = var.project_id
  combiner     = "OR"

  conditions {
    display_name = "Memory usage exceeds 80%"

    condition_threshold {
      filter          = "resource.type=\"cloud_run_revision\" AND resource.labels.service_name=\"${var.service_name}\" AND metric.type=\"run.googleapis.com/container/memory/utilizations\""
      duration        = "300s"
      comparison      = "COMPARISON_GT"
      threshold_value = 0.8

      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_MEAN"
      }
    }
  }

  documentation {
    content   = "L'utilisation mémoire dépasse 80%. Considérez augmenter les limites ou optimiser le code."
    mime_type = "text/markdown"
  }

  notification_channels = [
    google_monitoring_notification_channel.email.name
  ]
}

# Budget alert (requires billing account ID)
# Uncomment and configure if you want budget alerts
# resource "google_billing_budget" "a2a_budget" {
#   billing_account = var.billing_account
#   display_name    = "A2A Agents Monthly Budget"
#
#   budget_filter {
#     projects = ["projects/${var.project_id}"]
#     services = [
#       "services/E5F0-23E1-8F93",  # Cloud Run
#       "services/8800-0AE7-E10F"   # Vertex AI
#     ]
#   }
#
#   amount {
#     specified_amount {
#       currency_code = "EUR"
#       units         = "100"  # Budget mensuel : 100€
#     }
#   }
#
#   threshold_rules {
#     threshold_percent = 0.5  # Alerte à 50%
#   }
#
#   threshold_rules {
#     threshold_percent = 0.9  # Alerte à 90%
#   }
#
#   threshold_rules {
#     threshold_percent = 1.0  # Alerte à 100%
#   }
#
#   all_updates_rule {
#     monitoring_notification_channels = [
#       google_monitoring_notification_channel.email.id
#     ]
#   }
# }

# Dashboard for monitoring
resource "google_monitoring_dashboard" "a2a_dashboard" {
  dashboard_json = jsonencode({
    displayName = "A2A Agents Monitoring"
    mosaicLayout = {
      columns = 12
      tiles = [
        {
          width  = 6
          height = 4
          widget = {
            title = "Request Count"
            xyChart = {
              dataSets = [{
                timeSeriesQuery = {
                  timeSeriesFilter = {
                    filter = "resource.type=\"cloud_run_revision\" AND resource.labels.service_name=\"${var.service_name}\" AND metric.type=\"run.googleapis.com/request_count\""
                    aggregation = {
                      alignmentPeriod  = "60s"
                      perSeriesAligner = "ALIGN_RATE"
                    }
                  }
                }
              }]
            }
          }
        },
        {
          xPos   = 6
          width  = 6
          height = 4
          widget = {
            title = "Response Latency"
            xyChart = {
              dataSets = [{
                timeSeriesQuery = {
                  timeSeriesFilter = {
                    filter = "resource.type=\"cloud_run_revision\" AND resource.labels.service_name=\"${var.service_name}\" AND metric.type=\"run.googleapis.com/request_latencies\""
                    aggregation = {
                      alignmentPeriod  = "60s"
                      perSeriesAligner = "ALIGN_DELTA"
                    }
                  }
                }
              }]
            }
          }
        },
        {
          yPos   = 4
          width  = 6
          height = 4
          widget = {
            title = "Error Rate (5xx)"
            xyChart = {
              dataSets = [{
                timeSeriesQuery = {
                  timeSeriesFilter = {
                    filter = "resource.type=\"cloud_run_revision\" AND resource.labels.service_name=\"${var.service_name}\" AND metric.type=\"run.googleapis.com/request_count\" AND metric.labels.response_code_class=\"5xx\""
                    aggregation = {
                      alignmentPeriod  = "60s"
                      perSeriesAligner = "ALIGN_RATE"
                    }
                  }
                }
              }]
            }
          }
        },
        {
          xPos   = 6
          yPos   = 4
          width  = 6
          height = 4
          widget = {
            title = "Instance Count"
            xyChart = {
              dataSets = [{
                timeSeriesQuery = {
                  timeSeriesFilter = {
                    filter = "resource.type=\"cloud_run_revision\" AND resource.labels.service_name=\"${var.service_name}\" AND metric.type=\"run.googleapis.com/container/instance_count\""
                    aggregation = {
                      alignmentPeriod  = "60s"
                      perSeriesAligner = "ALIGN_MEAN"
                    }
                  }
                }
              }]
            }
          }
        }
      ]
    }
  })
}

output "monitoring_dashboard_url" {
  description = "URL of the monitoring dashboard"
  value       = "https://console.cloud.google.com/monitoring/dashboards/custom/${google_monitoring_dashboard.a2a_dashboard.id}?project=${var.project_id}"
}
