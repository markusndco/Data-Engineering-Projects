"""
Copies curated parquet data from S3 to Redshift internal tables.
"""
import os
import psycopg2

REDSHIFT_DSN = os.getenv("REDSHIFT_DSN", "dbname=dev user=awsuser password=*** host=redshift port=5439")
S3_PATH = os.getenv("S3_PATH", "s3://your-bucket/curated/kpi_by_day/")
IAM_ROLE = os.getenv("IAM_ROLE", "arn:aws:iam::123456789012:role/RedshiftCopyRole")

DDL = """
CREATE SCHEMA IF NOT EXISTS curated;
CREATE TABLE IF NOT EXISTS curated_kpi_by_day (
  day DATE,
  region VARCHAR(16),
  unique_users BIGINT,
  events BIGINT,
  avg_rt_ms DOUBLE PRECISION
);
"""

COPY = f"""
COPY curated_kpi_by_day
FROM '{S3_PATH}'
IAM_ROLE '{IAM_ROLE}'
FORMAT AS PARQUET;
"""

def main():
    conn = psycopg2.connect(REDSHIFT_DSN)
    conn.autocommit = True
    cur = conn.cursor()
    for stmt in filter(None, DDL.split(";")):
        s = stmt.strip()
        if s: cur.execute(s + ";")
    cur.execute(COPY)
    cur.close(); conn.close()
    print("[OK] Redshift load complete")

if __name__ == "__main__":
    main()
