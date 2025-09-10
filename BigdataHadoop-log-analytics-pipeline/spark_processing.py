"""
PySpark Processing Job (Batch)
- Reads partitioned raw CSVs (stand-in for HDFS/S3)
- Cleans + aggregates metrics (sessions/events/errors/latency)
- Writes curated parquet to local path (simulate S3)
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, date_format, to_timestamp, countDistinct, count, avg

RAW = "out_raw"
CURATED = "curated"

spark = (SparkSession.builder
         .appName("BigDataSparkProcessing")
         .config("spark.sql.sources.partitionOverwriteMode","dynamic")
         .getOrCreate())

df = (spark.read
      .option("header", True)
      .csv(f"{RAW}/**/*.csv"))

df2 = (df
       .withColumn("event_ts", to_timestamp(col("event_time")))
       .withColumn("is_error", (col("status_code") >= 400).cast("boolean"))
       .withColumn("day", date_format(col("event_ts"), "yyyy-MM-dd"))
       .withColumn("response_time_ms", col("response_time_ms").cast("int"))
       .withColumn("bytes", col("bytes").cast("int"))
       .dropna(subset=["event_ts"]))

agg = (df2.groupBy("day","region")
       .agg(countDistinct("user_id").alias("unique_users"),
            count("*").alias("events"),
            avg("response_time_ms").alias("avg_rt_ms")))

(agg.write
 .mode("overwrite")
 .partitionBy("day")
 .parquet(f"{CURATED}/kpi_by_day"))

spark.stop()
