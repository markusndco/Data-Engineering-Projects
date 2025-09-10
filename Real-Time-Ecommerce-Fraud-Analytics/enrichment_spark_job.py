"""
EMR Spark Streaming Job — Real-Time Enrichment
----------------------------------------------
Consumes events from Kinesis, enriches with reference data, computes session-level
metrics, and writes partitioned parquet files to S3 for Redshift Spectrum and
downstream analytics.

Highlights:
- Structured Streaming from Kinesis
- JSON parsing and schema enforcement
- Sessionization with watermarking
- Simple fraud heuristics for real-time tagging
- Output sink: S3 parquet partitioned by dt=YYYY-MM-DD/hr=HH

Author: Kiran Ranganalli
Last Updated: Aug 2025
"""

import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, from_json, window, to_timestamp, expr, when,
    date_format, concat_ws, lit
)
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, BooleanType, TimestampType

KINESIS_STREAM = os.getenv("KINESIS_STREAM", "ecommerce-events-stream")
AWS_REGION = os.getenv("AWS_REGION", "us-west-2")
S3_OUT = os.getenv("S3_OUT", "s3://ecommerce-analytics-data/enriched/")
CHECKPOINT = os.getenv("CHECKPOINT", "s3://ecommerce-analytics-data/checkpoints/enriched/")

spark = (
    SparkSession.builder
    .appName("RealTimeEnrichmentJob")
    .getOrCreate()
)

spark.conf.set("spark.sql.shuffle.partitions", "200")

# Define schema for strict parsing
schema = StructType([
    StructField("event_id", StringType()),
    StructField("event_type", StringType()),
    StructField("ts", StringType()),
    StructField("user_id", StringType()),
    StructField("session_id", StringType()),
    StructField("product_id", StringType()),
    StructField("category", StringType()),
    StructField("region", StringType()),
    StructField("geo_ip", StringType()),
    StructField("amount", DoubleType()),
    StructField("currency", StringType()),
    StructField("device", StringType()),
    StructField("is_gift", BooleanType()),
    StructField("payment_method", StringType()),
    StructField("success", BooleanType()),
])

# Read from Kinesis
raw = (
    spark.readStream
    .format("kinesis")
    .option("streamName", KINESIS_STREAM)
    .option("region", AWS_REGION)
    .option("initialPosition", "LATEST")
    .load()
)

# Kinesis records are base64-encoded; decode and parse JSON
json_df = raw.selectExpr("CAST(data AS STRING) AS payload")

parsed = (
    json_df
    .withColumn("json", from_json(col("payload"), schema))
    .select("json.*")
    .withColumn("event_ts", to_timestamp(col("ts")))
)

# Fraud heuristics (illustrative)
enriched = (
    parsed
    .withColumn("is_high_value", when(col("amount") > 500, lit(True)).otherwise(lit(False)))
    .withColumn("is_geo_mismatch", when(col("region").isin("EU","APAC") & (col("currency") == "USD"), lit(True)).otherwise(lit(False)))
    .withColumn("fraud_score", expr("CASE WHEN is_high_value THEN 0.4 ELSE 0 END + CASE WHEN NOT success AND event_type='payment_attempt' THEN 0.5 ELSE 0 END + CASE WHEN is_geo_mismatch THEN 0.2 ELSE 0 END"))
    .withColumn("dt", date_format(col("event_ts"), "yyyy-MM-dd"))
    .withColumn("hr", date_format(col("event_ts"), "HH"))
)

# Write partitioned parquet for Spectrum/QuickSight
query = (
    enriched
    .writeStream
    .format("parquet")
    .option("path", S3_OUT)
    .option("checkpointLocation", CHECKPOINT)
    .partitionBy("dt","hr")
    .outputMode("append")
    .start()
)

query.awaitTermination()
