📊 Big Data Log Analytics Pipeline  

## 📖 Overview  
This project demonstrates a **big data ETL pipeline** for processing and analyzing application logs at scale. Raw logs are ingested into an HDFS-style partitioned structure, processed with **PySpark**, stored as curated Parquet, loaded into **Amazon Redshift**, and queried using **Hive** for insights.  

---

## 🎯 Objectives  
- ⚡ Ingest raw CSV logs into partitioned HDFS-like structure  
- 🛠 Process logs with PySpark to compute KPIs (users, events, latency)  
- 📂 Store curated data in Parquet format for efficient querying  
- 🗄 Load curated datasets into Amazon Redshift for analytics  
- 🔍 Define Hive external tables for querying Parquet data  
- 📊 Enable log-based metrics for operational insights  

---

## 🏗 Architecture  
- **Ingestion**: Python pipeline partitions raw logs by date and hour:contentReference[oaicite:0]{index=0}  
- **Processing**: PySpark cleans, aggregates, and writes curated Parquet KPIs:contentReference[oaicite:1]{index=1}  
- **Storage**: Parquet files stored in curated zone  
- **Warehouse**: Redshift loader copies curated data into analytics tables:contentReference[oaicite:2]{index=2}  
- **Query Layer**: Hive external tables enable BI/SQL access:contentReference[oaicite:3]{index=3}  

---

## 🌟 Features  
- Automated ingestion with partitioning  
- Spark-based data cleaning, validation, and aggregation  
- Storage optimization with Parquet  
- Redshift integration for analytical queries  
- Hive queries for ad-hoc analytics  
- End-to-end pipeline simulation of big data stack  

---

## 🛠 Tech Stack  
- **Ingestion:** Python (CSV → partitioned HDFS style)  
- **Processing:** Apache Spark (PySpark)  
- **Storage:** Parquet files (curated zone)  
- **Warehouse:** Amazon Redshift  
- **Query Layer:** Apache Hive  

---

## 📂 Repository Structure  
.
```
├── README.md # Project overview
├── ingestion_pipeline.py # Ingest raw CSV logs into partitioned folders
├── spark_processing.py # PySpark job for cleaning & aggregations
├── redshift_loader.py # Load curated data from S3 → Redshift
├── hive_queries.sql # Hive DDL & sample queries
├── data/
│ └── sample_logs.csv # Example raw logs for pipeline demo
```

---

## 🚀 Getting Started  
1. 📥 Place raw logs into `data/sample_logs.csv`  
2. 🌀 Run `ingestion_pipeline.py` to create partitioned raw data  
3. 🔥 Run `spark_processing.py` to generate curated Parquet outputs  
4. 🗄 Use `redshift_loader.py` to load curated data into Redshift  
5. 🔍 Execute `hive_queries.sql` to query curated Parquet tables  

---

## 🔍 Use Cases  
- Application log analytics  
- Monitoring latency, errors, and usage patterns  
- Building KPI dashboards from log events  
- Demonstrating big data ETL workflows  

---

## 📜 License  
This project is provided for **educational and demonstration purposes**. Adapt for production with proper security, scalability, and compliance measures.  
