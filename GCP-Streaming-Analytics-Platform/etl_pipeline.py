"""
Databricks Streaming ETL — GCP Edition
======================================
- Ingests events from GCS (Auto Loader)
- Writes bronze/silver/gold to BigQuery
"""
import os
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import col, from_json, to_timestamp, date_format, sha2, concat_ws, when, expr, regexp_extract, coalesce, lit
class Config:
    project_id = os.getenv("GCP_PROJECT", "demo-project")
    raw_bucket = os.getenv("RAW_BUCKET", "gcs-raw-events")
    ckpt_bucket = os.getenv("CKPT_BUCKET", "gcs-stream-checkpoints")
    bronze_bq = os.getenv("BRONZE_BQ", "analytics_raw.events_bronze")
    silver_bq = os.getenv("SILVER_BQ", "analytics.events_silver")
    gold_bq   = os.getenv("GOLD_BQ", "analytics.events_gold")
    ckpt_path = os.getenv("CKPT_PATH", f"gs://gcs-stream-checkpoints/etl")
    autoloader_path = os.getenv("AUTOLOADER_PATH", f"gs://gcs-raw-events/landing/")
    trigger_seconds = int(os.getenv("TRIGGER_SECONDS", "60"))
from pyspark.sql.functions import *
event_schema = StructType([
    StructField("event_id", StringType()),
    StructField("ts", StringType()),
    StructField("user_id", StringType()),
    StructField("session_id", StringType()),
    StructField("event_type", StringType()),
    StructField("page", StringType()),
    StructField("product_id", StringType()),
    StructField("price", DoubleType()),
    StructField("currency", StringType()),
    StructField("country", StringType()),
    StructField("device", StringType()),
    StructField("referrer", StringType()),
    StructField("is_bot", BooleanType()),
    StructField("dwell_time_ms", IntegerType()),
    StructField("latency_ms", IntegerType()),
    StructField("status", StringType()),
    StructField("ab_variant", StringType()),
    StructField("campaign", StringType()),
    StructField("event_source", StringType())
])
def spark():
    return (SparkSession.builder
            .appName("StreamingAnalytics_ETL")
            .config("spark.sql.session.timeZone","UTC")
            .config("spark.sql.shuffle.partitions","400")
            .config("spark.databricks.cloudFiles.format","json")
            .getOrCreate())

def read_autoloader(sp: SparkSession) -> DataFrame:
    return (sp.readStream.format("cloudFiles")
            .option("cloudFiles.format","json")
            .option("cloudFiles.inferColumnTypes","false")
            .option("cloudFiles.schemaLocation", f"{Config.ckpt_path}/schema")
            .load(Config.autoloader_path))

def parse(df: DataFrame) -> DataFrame:
    p = (df.selectExpr("CAST(_rescued_data AS STRING) AS payload")
           .withColumn("j", from_json(col("payload"), event_schema))
           .select("j.*")
           .withColumn("event_ts", to_timestamp(col("ts")))
           .withColumn("dt", date_format(col("event_ts"), "yyyy-MM-dd"))
           .withColumn("hr", date_format(col("event_ts"), "HH")))
    return p

def cleanse(df: DataFrame) -> DataFrame:
    return (df
            .withColumn("price", coalesce(col("price"), lit(0.0)))
            .withColumn("dwell_time_ms", coalesce(col("dwell_time_ms"), lit(0)))
            .withColumn("latency_ms", coalesce(col("latency_ms"), lit(0)))
            .withColumn("is_bot", coalesce(col("is_bot"), lit(False)))
            .withColumn("status", coalesce(col("status"), lit("ok"))))

def dedup(df: DataFrame) -> DataFrame:
    return (df.withWatermark("event_ts","30 minutes").dropDuplicates(["event_id"]))

def features(df: DataFrame) -> DataFrame:
    return (df
            .withColumn("is_purchase", (col("event_type")=="purchase").cast("boolean"))
            .withColumn("revenue_usd", when(col("currency")=="USD", col("price")).otherwise(col("price")))
            .withColumn("category", regexp_extract(col("page"), r"/category/([A-Za-z0-9_-]+)", 1))
            .withColumn("minute", date_format(col("event_ts"), "yyyy-MM-dd HH:mm"))
            .withColumn("key", sha2(concat_ws("|","user_id","session_id","event_type","event_ts"),256)))

def write_bronze(df: DataFrame):
    return (df.writeStream.format("bigquery")
            .option("table", Config.bronze_bq)
            .option("checkpointLocation", f"{Config.ckpt_path}/bronze")
            .option("temporaryGcsBucket", Config.ckpt_bucket)
            .outputMode("append")
            .trigger(processingTime=f"{Config.trigger_seconds} seconds")
            .start())

def write_silver(df: DataFrame):
    return (df.writeStream.format("bigquery")
            .option("table", Config.silver_bq)
            .option("checkpointLocation", f"{Config.ckpt_path}/silver")
            .option("temporaryGcsBucket", Config.ckpt_bucket)
            .outputMode("append")
            .trigger(processingTime=f"{Config.trigger_seconds} seconds")
            .start())

def write_gold(df: DataFrame):
    return (df.writeStream.format("bigquery")
            .option("table", Config.gold_bq)
            .option("checkpointLocation", f"{Config.ckpt_path}/gold")
            .option("temporaryGcsBucket", Config.ckpt_bucket)
            .outputMode("complete")
            .trigger(processingTime=f"{Config.trigger_seconds} seconds")
            .start())

def aggregate_gold(df: DataFrame) -> DataFrame:
    return (df.groupBy("minute","country","device","ab_variant","campaign","category")
            .agg(expr("SUM(CASE WHEN is_purchase THEN price ELSE 0 END)").alias("gmv"),
                 expr("SUM(CASE WHEN status!='ok' THEN 1 ELSE 0 END)").alias("errors"),
                 expr("COUNT(*)").alias("events"),
                 expr("COUNT(DISTINCT user_id)").alias("unique_users"),
                 expr("AVG(dwell_time_ms)").alias("avg_dwell_ms")))

def main():
    sp = spark()
    raw = read_autoloader(sp)
    p = parse(raw)
    c = cleanse(p)
    d = dedup(c)
    f = features(d)
    bq1 = write_bronze(f)
    bq2 = write_silver(f)
    g = aggregate_gold(f)
    bq3 = write_gold(g)
    sp.streams.awaitAnyTermination()

if __name__ == "__main__":
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
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.
# TIP: Test UDFs thoroughly and avoid Python UDFs where possible.

# ----------------------------
# Appendix Notes
# These notes serve as embedded runbooks and operational context.
# ----------------------------
# TIP: Tune shuffle partitions based on input size and cluster cores.
# TIP: Use checkpointing + exactly-once sinks where available.
# TIP: Validate schema changes via canary pipelines.
# TIP: Push row-level quality metrics to monitoring.
# TIP: Prefer partition pruning and columnar formats for cost control.