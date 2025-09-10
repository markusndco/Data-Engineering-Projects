"""
Monitoring & Alerts — Pub/Sub + BigQuery
"""
import os, json, traceback
from datetime import datetime, timezone
from typing import Dict, Any
from google.cloud import pubsub_v1, bigquery
PROJECT = os.getenv("GCP_PROJECT","demo-project")
DATASET = os.getenv("INCIDENT_DATASET","ops")
TABLE   = os.getenv("INCIDENT_TABLE","pipeline_incidents")
TOPIC   = os.getenv("ALERTS_TOPIC","projects/demo-project/topics/pipeline-alerts")
publisher = pubsub_v1.PublisherClient()
bq = bigquery.Client(project=PROJECT)

def classify(p: Dict[str, Any]) -> Dict[str, Any]:
    sev, reason = "INFO","ok"
    if p.get("failed_records_ratio",0)>0.02: sev,reason = "HIGH","failed_records_ratio>2%"
    elif p.get("lag_seconds",0)>600: sev,reason = "MEDIUM","streaming_lag>10min"
    elif p.get("dq_failures",0)>0: sev,reason = "MEDIUM","data_quality_failures>0"
    return {"severity":sev,"reason":reason}

def record(row: Dict[str, Any]):
    table = f"{PROJECT}.{DATASET}.{TABLE}"
    row["ingested_at"] = datetime.now(timezone.utc).isoformat()
    errs = bq.insert_rows_json(table, [row])
    if errs: print(f"[WARN] BQ insert errors: {errs}")

def alert(msg: Dict[str, Any]):
    publisher.publish(TOPIC, data=json.dumps(msg).encode("utf-8"))

def handler(event, context=None):
    try:
        payload = json.loads((event.get("data") or b"{}").decode("utf-8"))
        c = classify(payload); out = {**payload, **c}
        record(out)
        if c["severity"] in ("HIGH","MEDIUM"): alert(out)
        return {"status":"ok","incident":out}
    except Exception as e:
        traceback.print_exc()
        return {"status":"error","error":str(e)}

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