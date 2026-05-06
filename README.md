🍽️ Egyptian Restaurant Data Platform
End-to-End Medallion Architecture on Databricks (11.1M+ Records | 2020–2025)

Production-grade analytics system simulating a multi-branch restaurant chain in Egypt.
Built using Databricks (Spark + Delta Lake), orchestrated via Apache Airflow, and modeled for Power BI-driven business intelligence.

📌 Executive Summary

This project implements a scalable end-to-end data platform processing 11.1M+ transactional records across 6 restaurant branches in Egypt, transforming raw operational data into a structured analytics warehouse.

It enables executive reporting, profitability tracking, customer behavior analysis, and scenario-based decision modeling.

Key outcomes
11.1M raw records → 2.49M analytics-ready records
444M EGP modeled profit
65.34% average profit margin
Fully automated daily pipeline via Airflow
Star schema optimized for BI workloads
Power BI semantic model with interactive simulation layer
🧱 System Architecture
High-Level Data Flow
🧱 Medallion Architecture
🔵 Bronze Layer — Raw Ingestion

This layer preserves raw source fidelity for traceability and reprocessing.

9 heterogeneous data sources (CSV + JSON)
Unified using unionByName
Stored in Delta Lake format
No transformations applied

Output:

bronze_restaurant
11,110,000 records
🟡 Silver Layer — Data Cleaning & Feature Engineering

This layer ensures data quality and introduces analytical readiness.

Data Cleaning
Removed ~2M duplicate order_id records
Filtered 51,442 invalid price records
Standardized schema across all sources
Feature Engineering
time_of_day segmentation
year / quarter extraction
weekend flag
profit estimation model

Output:

2,497,678 clean records
🟢 Gold Layer — Analytics Warehouse (Star Schema)

This layer is optimized for BI performance and reporting.

Fact Table
gold_fact_orders (2.49M records)
Dimension Tables
date
branch
category
customer
payment
time
Design Principles
Fully denormalized for analytics performance
BI-optimized joins
Partition-friendly structure for scalability
⚙️ Orchestration Layer (Apache Airflow)
DAG: restaurant_medallion_pipeline

The pipeline runs as a production-style scheduled workflow.

Execution Flow

start → ingest_bronze → clean_silver → build_gold → data_quality → notify_success → end

Configuration
Schedule: daily (02:00 AM)
Retries: 3 (5-minute delay)
Timeout: 60 minutes
Slack notifications for success/failure
Reliability Design
Idempotent pipeline execution
Safe re-runs without duplication
Data validation before publishing Gold layer
💰 Profit Modeling Layer

Since real cost data was unavailable, a deterministic financial model was implemented using industry benchmarks for quick-service restaurants.

Assumptions
Food cost: 30% of revenue
Delivery cost: 15 EGP per order
Card processing fee: 1.5% per transaction
Result
Average profit margin: 65.34%
Fully reproducible logic embedded in Silver layer transformations
📊 Business Intelligence Layer (Power BI)

The BI layer is designed as a multi-page analytical system supporting executive and operational decision-making.

Executive Overview
Revenue & profit KPIs
Sales trends (2020–2025)
Top product categories
Payment method distribution
Data quality monitoring
Profitability Analysis
Branch-level performance comparison
Margin segmentation (high / medium / low)
Operational insights:
underperforming branch detection
category-level optimization opportunities
Customer Analytics
Customer Lifetime Value (CLV)
Churn rate: 12.6%
Segmentation: new / regular / loyal customers
Retention analysis by branch
Scenario Simulation Engine

What-if analysis system built using parameterized models:

Delivery mix changes
Discount strategy impact
Price adjustments
Digital payment adoption
Business impact simulation
+49M EGP revenue potential
+31.9M EGP profit uplift
Margin improvement: 65.3% → 66.0%
🧪 Data Quality Framework
Stage	Records
Raw ingestion	11,110,000
After deduplication	9,110,000
After cleaning	2,497,678
Gold layer	2,497,678
Controls implemented
Duplicate transaction detection
Null handling strategy
Schema enforcement across layers
Referential integrity validation in Gold layer
🛠️ Technology Stack
Layer	Technology
Storage	Delta Lake
Processing	Apache Spark (PySpark)
Orchestration	Apache Airflow
Visualization	Power BI
Version Control	GitHub
Languages	Python, SQL, DAX
📁 Repository Structure
Egyptian-Restaurant-Platform/
│
├── notebooks/
│   ├── 01_bronze_layer.ipynb
│   ├── 02_silver_layer.ipynb
│   └── 03_gold_layer.ipynb
│
├── airflow/
│   └── restaurant_medallion_dag.py
│
├── powerbi/
│   └── restaurant_dashboard.pbix
│
├── docs/
│   └── architecture.png
│
├── README.md
└── requirements.txt
🚀 Reproducibility
Databricks
Execute Bronze → Silver → Gold notebooks sequentially
Export Gold tables for BI consumption
Airflow
Deploy DAG in Airflow scheduler
Enable monitoring and alerts
Power BI
Connect to Gold layer tables
Define relationships
Publish semantic model
🧠 Engineering Highlights
End-to-end Medallion architecture implementation
Large-scale Spark processing (11M+ records)
Production-style Airflow orchestration
Star schema optimized for BI performance
Data quality gating before publishing
Scenario-based financial simulation layer
👤 Author

Yasmeen Elshamy
ITI – Power BI Development Track
Focus: Data Engineering, Analytics Systems, BI Architecture

GitHub: @Yasmeen327

📜 License

MIT License — for educational and professional use with attribution.








































































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

