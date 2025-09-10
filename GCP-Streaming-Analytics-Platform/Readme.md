📊 GCP Streaming Analytics Platform  

## 📖 Overview  
This project implements a **streaming analytics platform on Google Cloud Platform (GCP)**. It ingests clickstream-like events, processes them with Databricks Structured Streaming, validates data with Great Expectations, and persists bronze/silver/gold layers in **BigQuery**. Infrastructure is provisioned via **Terraform**, monitoring is handled with Python alerting, and insights are surfaced through **Looker dashboards**.  

---

## 🎯 Objectives  
- ⚡ Ingest raw events from GCS into Databricks using Auto Loader  
- 🛠 Transform events through **bronze → silver → gold** layers in BigQuery  
- ✅ Apply hourly **data quality validations** with Great Expectations  
- 🖥 Provision infrastructure with Terraform for repeatability  
- 📊 Deliver real-time insights with Looker dashboards  
- 🔔 Trigger monitoring alerts for anomalies or schema issues  

---

## 🏗 Architecture  
- **Ingestion**: Raw event data lands in **Google Cloud Storage**  
- **ETL**: Databricks Structured Streaming parses, cleanses, deduplicates, and aggregates into bronze, silver, and gold BigQuery tables:contentReference[oaicite:0]{index=0}  
- **Data Quality**: Great Expectations validates bronze/silver/gold layers hourly:contentReference[oaicite:1]{index=1}  
- **Storage**: BigQuery serves as the analytical warehouse  
- **Monitoring**: Python-based alerting monitors data quality & anomalies  
- **Dashboards**: Looker visualizes KPIs from gold tables  
- **Infra**: Terraform defines GCP resources (buckets, datasets, IAM)  

---

## 🌟 Features  
- Scalable ingestion with Databricks Auto Loader  
- Exactly-once guarantees with checkpoints  
- Tiered data modeling: bronze → silver → gold  
- Automated Great Expectations data validation  
- Infrastructure-as-code with Terraform  
- Real-time alerting with Python monitoring scripts  
- Interactive Looker dashboards  

---

## 🛠 Tech Stack  
- **Compute & ETL**: Databricks, PySpark  
- **Storage & Warehouse**: Google Cloud Storage, BigQuery  
- **Data Quality**: Great Expectations  
- **Infra**: Terraform  
- **Monitoring**: Python (custom alerts)  
- **Visualization**: Looker  

---

## 📂 Repository Structure 
``` 
├── README.md # Project overview
├── etl_pipeline.py # Databricks streaming ETL (bronze/silver/gold)
├── data_quality_suite.py # Great Expectations validation suite
├── monitoring_alerts.py # Monitoring and alerting script
├── gcp_infra.tf # Terraform config for GCP infra
├── looker_dashboard.json # Looker dashboard definition
├── data/
│ └── event_stream_sample_small.csv # Sample event data
```

---

## 🚀 Getting Started  
1. 🖥 Provision GCP resources with Terraform (`gcp_infra.tf`)  
2. ⚡ Deploy ETL to Databricks (`etl_pipeline.py`) to process events into BigQuery  
3. ✅ Run data validations with Great Expectations (`data_quality_suite.py`)  
4. 🔔 Configure monitoring (`monitoring_alerts.py`) for anomalies  
5. 📊 Import Looker dashboard (`looker_dashboard.json`) for analytics  

---

## 🔍 Use Cases  
- Real-time **event stream analytics**  
- **Data quality monitoring** in streaming pipelines  
- **Product analytics** dashboards (sessions, revenue, anomalies)  
- Scalable, cloud-native ETL architecture  

---

## 📜 License  
This project is provided for **educational and demonstration purposes**. Please review compliance and cost considerations before production deployment.  
