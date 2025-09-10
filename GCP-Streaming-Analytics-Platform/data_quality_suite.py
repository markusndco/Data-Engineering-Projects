"""
Great Expectations Suite for Streaming Analytics
- Builds suites for bronze/silver/gold
- Runs hourly checkpoints
"""
import os, json
from datetime import datetime
import great_expectations as ge
from great_expectations.data_context import DataContext
from great_expectations.checkpoint import SimpleCheckpoint
ROOT = os.getenv("GE_ROOT_DIR","/dbfs/great_expectations")
BRONZE = os.getenv("BRONZE_TABLE","analytics_raw.events_bronze")
SILVER = os.getenv("SILVER_TABLE","analytics.events_silver")
GOLD   = os.getenv("GOLD_TABLE","analytics.events_gold")

def ctx():
    os.makedirs(ROOT, exist_ok=True)
    return DataContext(context_root_dir=ROOT)

def suite(context, name, cols):
    try:
        s = context.get_expectation_suite(name)
    except Exception:
        s = context.create_expectation_suite(name)
    for c in cols:
        s.add_expectation("expect_column_to_exist", kwargs={"column": c})
        s.add_expectation("expect_column_values_to_not_be_null", kwargs={"column": c, "mostly": 0.99})
    if "event_id" in cols:
        s.add_expectation("expect_column_values_to_be_unique", kwargs={"column":"event_id"})
    s.add_expectation("expect_table_row_count_to_be_between", kwargs={"min_value":1,"max_value":100000000})
    context.save_expectation_suite(s, suite_name=name)
    return s

def run_chk(context, suite_name, table):
    chk = SimpleCheckpoint(
        name=f"chk_{suite_name}",
        data_context=context,
        validations=[{
            "batch_request": {
                "datasource_name": "spark_datasource",
                "data_connector_name": "default_runtime_data_connector_name",
                "data_asset_name": table,
                "runtime_parameters": {"query": f"SELECT * FROM {table} WHERE event_ts >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)"},
                "batch_identifiers": {"default_identifier_name": datetime.utcnow().isoformat()},
            },
            "expectation_suite_name": suite_name,
        }]
    )
    res = chk.run()
    return res.to_json_dict()

def main():
    c = ctx()
    bronze_cols = ["event_id","event_ts","user_id","session_id","event_type","page","product_id","price","currency","country","device","referrer","is_bot","dwell_time_ms","latency_ms","status","ab_variant","campaign"]
    silver_cols = bronze_cols + ["category","revenue_usd"]
    gold_cols   = ["minute","country","device","ab_variant","campaign","category","gmv","errors","events","unique_users","avg_dwell_ms"]
    suite(c, "bronze_suite", bronze_cols)
    suite(c, "silver_suite", silver_cols)
    suite(c, "gold_suite",   gold_cols)
    out = Path(ROOT) / "validation_results"; out.mkdir(parents=True, exist_ok=True)

    for (n, t) in [("bronze_suite",BRONZE),("silver_suite",SILVER),("gold_suite",GOLD)]:
        jr = run_chk(c, n, t)
        (out / f"{n}_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.json").write_text(json.dumps(jr, indent=2))

if __name__ == "__main__":
    from pathlib import Path
    main()

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