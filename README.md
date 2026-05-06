# 🍽️ Egyptian Restaurant Data Platform  
## End-to-End Medallion Architecture on Databricks (11.1M+ Records | 2020–2025)

> Production-grade analytics system simulating a multi-branch restaurant chain in Egypt.  
Built using Databricks (Spark + Delta Lake), orchestrated via Apache Airflow, and modeled for Power BI-driven business intelligence.

---

## 📌 Executive Summary

This project implements a scalable end-to-end data platform processing **11.1M+ transactional records** across 6 restaurant branches in Egypt, transforming raw operational data into a structured analytics warehouse.

It supports executive reporting, profitability tracking, customer segmentation, and scenario-based decision modeling.

### Key Outcomes
- 11.1M raw records → **2.49M analytics-ready records**
- **444M EGP** modeled profit
- **65.34%** average profit margin
- Fully automated daily pipeline via **Airflow**
- Star schema optimized for BI workloads
- Power BI semantic model with **simulation layer**

---

## 🧱 System Architecture

### High-Level Data Flow

```mermaid
flowchart TD
    A[Raw Data Sources - CSV + JSON] --> B[Ingestion Layer - Databricks / Fivetran]
    B --> C[Bronze Layer - Raw Delta Tables]
    C --> D[Silver Layer - Cleaned + Enriched Data]
    D --> E[Gold Layer - Star Schema Warehouse]
    E --> F[Power BI Semantic Layer]

    G[Airflow Orchestration] --> C
    G --> D
    G --> E
```




































































⏱️ Airflow DAG – Production Orchestration
restaurant_medallion_pipeline runs daily at 2 AM with retries and Slack alerts.

text
          ┌──────────────┐
          │   start_task │
          └──────┬───────┘
                 │
                 ▼
          ┌──────────────┐
          │ ingest_bronze│  ← Load 9 files → Delta table
          └──────┬───────┘
                 │
                 ▼
          ┌──────────────┐
          │ clean_silver │  ← Dedupe, filter, profit calc
          └──────┬───────┘
                 │
                 ▼
          ┌──────────────┐
          │  build_gold  │  ← Star schema (fact + dims)
          └──────┬───────┘
                 │
                 ▼
          ┌──────────────┐
          │ data_quality │  ← Validate row counts & nulls
          └──────┬───────┘
                 │
                 ▼
          ┌──────────────┐
          │notify_success│  ← Slack webhook alert
          └──────┬───────┘
                 │
                 ▼
          ┌──────────────┐
          │   end_task   │
          └──────────────┘
Configuration

Schedule: 0 2 * * *

Retries: 3 (delay 5 min)

Timeout: 60 min

Alert: Slack (success/failure)

💰 Profit Model Assumptions
Since actual cost data was unavailable, profit was estimated using industry‑standard drivers for Egyptian quick‑service restaurants:

Cost Driver	Assumption
Food cost	30% of order revenue
Delivery cost	15 EGP per delivery order
Card processing fee	1.5% of card transaction value
Resulting average profit margin: 65.34%

📈 Data Quality & Processing
Step	Records
Raw ingested	11,110,000
Duplicate order_id removed	2,000,000
Invalid price rows removed	51,442
Final clean orders (Gold)	2,497,678
All null values handled, schemas unified, data types enforced.

💼 Business KPIs
Metric	Value
Total Revenue	654.5M EGP
Total Profit	444.0M EGP
Average Profit Margin	65.34%
Average Order Value	262 EGP
Average Rating	3.70 / 5
Clean Orders	2,497,678
Date Range	2020 – 2025
Branches	6 (Cairo, Giza, Alexandria, Mansoura, Tanta, Assiut)
📊 Power BI Dashboard (4 Pages)
Page	Content
1. Executive Overview	KPI cards, revenue trend, top items, payment methods, data quality snapshot
2. Profit Analysis	Branch performance table, margin grading, actionable insights (e.g., Assiut improvement, grill margin opportunity)
3. Customer Insights	Customer lifetime value (CLV) by branch, churn rate (12.6%), segmentation (New/Regular/Loyal), business recommendations
4. What-If Simulator	Four interactive sliders (delivery %, digital shift, discount reduction, price increase). Real‑time impact on revenue (+49M EGP), profit (+31.9M EGP), and margin (66.0% vs 65.3% baseline)
🛠️ Tech Stack
Layer	Technology
Data Ingestion	CSV/JSON → Databricks
Data Processing	Apache Spark (PySpark)
Storage	Delta Lake (Databricks Community)
Orchestration	Apache Airflow (DAG)
Visualization	Power BI Desktop + Service
Version Control	GitHub
Languages	Python, SQL, DAX
📁 Repository Structure
text
Egyptian-Restaurant-Pipeline/
├── notebooks/
│   ├── 01_bronze_layer.ipynb
│   ├── 02_silver_layer.ipynb
│   └── 03_gold_layer.ipynb
├── airflow/
│   └── restaurant_medallion_dag.py
├── powerbi/
│   └── restaurant_dashboard.pbix
├── README.md
└── requirements.txt
🚀 How to Reproduce
Databricks
Import notebooks → run Bronze → Silver → Gold sequentially.

Export Gold tables as CSV/Parquet.

Power BI
Open .pbix file → connect to exported tables → refresh.

Airflow (optional)
Copy DAG to ~/airflow/dags/ → start scheduler → trigger DAG.

👩‍💻 Author
Yasmeen El Shamy
ITI Power BI Development Track – Big Data Project
GitHub: @Yasmeen327

📜 License
MIT License – free for educational and professional use with attribution.

