# Terraform — GCP Streaming Analytics Platform
terraform {
  required_version = ">= 1.6.0"
  required_providers { google = { source = "hashicorp/google", version = "~> 5.0" } }
}
provider "google" { project = var.project_id  region = var.region }
variable "project_id" { type = string }
variable "region"     { type = string  default = "us-central1" }
variable "location"   { type = string  default = "US" }
resource "google_storage_bucket" "raw" {
  name          = "${var.project_id}-raw-events"
  location      = var.location
  force_destroy = true
  versioning { enabled = true }
  lifecycle_rule { action { type = "SetStorageClass" storage_class = "NEARLINE" } condition { age = 30 } }
}
resource "google_storage_bucket" "ckpt" {
  name          = "${var.project_id}-stream-ckpt"
  location      = var.location
  force_destroy = true
  versioning { enabled = true }
}
resource "google_pubsub_topic" "events" { name = "engagement-events" }
resource "google_pubsub_subscription" "events_sub" {
  name  = "engagement-events-sub"
  topic = google_pubsub_topic.events.name
  ack_deadline_seconds = 30
  message_retention_duration = "1200s"
}
resource "google_bigquery_dataset" "analytics" { dataset_id = "analytics" location = var.location delete_contents_on_destroy = true }
resource "google_bigquery_dataset" "analytics_raw" { dataset_id = "analytics_raw" location = var.location delete_contents_on_destroy = true }
resource "google_bigquery_dataset" "ops" { dataset_id = "ops" location = var.location delete_contents_on_destroy = true }
# tables (bronze/silver/gold/incidents) omitted for brevity in this header; see full module in repo.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------