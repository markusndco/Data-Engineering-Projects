-- Hive DDL for curated tables
CREATE DATABASE IF NOT EXISTS bigdata_curated;

CREATE EXTERNAL TABLE IF NOT EXISTS bigdata_curated.kpi_by_day (
  region STRING,
  unique_users BIGINT,
  events BIGINT,
  avg_rt_ms DOUBLE
)
PARTITIONED BY (day STRING)
STORED AS PARQUET
LOCATION 's3://your-bucket/curated/kpi_by_day';

MSCK REPAIR TABLE bigdata_curated.kpi_by_day;

-- Example query
SELECT day, region, events, avg_rt_ms
FROM bigdata_curated.kpi_by_day
ORDER BY day, region;
