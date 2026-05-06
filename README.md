```markdown
# 🍽 Egyptian Restaurant Big Data Pipeline
### End-to-end Big Data Engineering Project | Databricks · PySpark · Airflow · Delta Lake · Power BI

---

## 🎯 Project Overview

A production-grade **Big Data pipeline** that ingests, cleans, transforms, and serves **11 million+ records** from a multi-branch Egyptian restaurant chain. Built using the **Medallion Architecture** on **Databricks**, orchestrated with **Apache Airflow**, and visualized in **Power BI**.

This project demonstrates real-world data engineering skills including large-scale data processing, pipeline orchestration, data quality management, star schema modeling, and business intelligence delivery.

---

## 🏗 Architecture

```mermaid
flowchart TD
    A[7 CSV + 2 JSON files] --> B[Bronze Layer]
    B --> C[Silver Layer]
    C --> D[Gold Layer]
    D --> E[Power BI Dashboard]
    F[Airflow DAG] -.-> B
    F -.-> C
    F -.-> D
```
---

**Layer Details**

| Layer  | Operation | Rows |
|--------|----------|------|
| Bronze | unionByName across 9 files | 11,110,000 |
| Silver | Deduplication (2M), price filter (51K), feature engineering | 2,497,678 |
| Gold   | Star schema: fact_orders + 6 dimensions | 2,497,678 |

📊 Data Quality Results

Metric Value
Raw Records Ingested 11,110,000
Duplicate Order IDs Removed 2,000,000
Invalid Price Records Removed 51,442
Null Values Found 0
Clean Unique Orders 2,497,678

Key insight: The raw dataset contained duplicate records that inflated order counts by 4x. Proper deduplication reduced 11.1M records to 2.49M clean, trustworthy orders — a critical data engineering decision that ensures accurate reporting.

---

💰 Business Results

KPI Value
Total Revenue 654.5M EGP
Total Profit 443.97M EGP
Avg Profit Margin 65.34%
Avg Order Value 262 EGP
Avg Rating 3.70 / 5
Unique Customers 200,000
Date Range Jan 2020 – Dec 2025
Branches 6 Egyptian cities

---

🔧 Tech Stack

Technology Purpose
Apache Spark / PySpark Large-scale data transformation (11M+ records)
Databricks Unified analytics platform & notebook environment
Delta Lake ACID-compliant storage with time travel
Apache Airflow Pipeline orchestration & daily scheduling
Power BI Business intelligence & executive dashboard
Python DAG development, data engineering logic
SQL Data validation and quality checks

---

🔄 Airflow DAG

The DAG restaurant_medallion_pipeline runs on a daily schedule and orchestrates the full pipeline:

```
start
  └─► ingest_bronze      (Unify 7 CSV + 2 JSON → Bronze Delta table)
        └─► clean_silver  (Clean, dedupe, engineer features → Silver)
              └─► build_gold  (Star schema → Gold layer)
                    └─► data_quality_check  (Validate row counts, nulls, margins)
                          └─► notify_success  (Log pipeline summary)
                                └─► end
```

Quality checks in the DAG:

· Row count validation (expected: ~2.49M)
· Null value assertion across all columns
· Duplicate check on order IDs
· Profit margin sanity check (expected: 60–75%)

---

💡 Profit Model

Since cost data was not available in the raw dataset, profit was modeled using industry-standard assumptions:

Cost Driver Assumption Rationale
Food Cost 30% of order revenue Industry standard F&B cost ratio
Delivery Cost 15 EGP flat per delivery order Fixed logistics cost per order
Card Processing Fee 1.5% of order value Standard merchant processing rate

Formula:

```
Profit = Revenue − Food Cost − Delivery Cost − Payment Cost
Profit Margin = (Profit / Revenue) × 100
```

---

📈 Branch Performance

Branch Revenue Net Profit Margin Status
القاهرة 229M EGP 155M EGP 70% ✅ Strong
الجيزة 131M EGP 89M EGP 69% ✅ Strong
الإسكندرية 131M EGP 89M EGP 68% ✅ Strong
المنصورة 65M EGP 44M EGP 67% ⚠️ Average
طنطا 65M EGP 44M EGP 66% ⚠️ Average
أسيوط 33M EGP 22M EGP 64% 🔴 At Risk

---

📊 Power BI Dashboard Pages

Page 1 — Executive Overview

KPI cards (Revenue, Profit, Orders, AOV, Rating), revenue trend by year, branch performance bar chart, payment method and order type distribution, top items by revenue.

Page 2 — Profit Analysis

Branch profit table with performance grades, profit by category, cost breakdown (food/delivery/payment), and 3 actionable business insights.

Page 3 — Customer Insights

Total vs active customers, churn rate, customer lifetime value (CLV) by branch, customer trend over time.

Page 4 — What-If Simulator

4 interactive parameters:

· Delivery Order % Increase
· Cash → Digital Payment Shift
· Average Discount Reduction
· Menu Price Increase

Live impact cards showing Revenue Impact, Profit Impact, and New Profit Margin as parameters change.

---

📁 Repository Structure

```
Restaurant-Bigdata-Pipeline/
│
├── dags/
│   └── restaurant_pipeline_dag.py    # Airflow DAG (full pipeline orchestration)
│
├── notebooks/
│   ├── 01_bronze_ingestion.py        # Bronze layer: raw data unification
│   ├── 02_silver_cleaning.py         # Silver layer: cleaning & feature engineering
│   └── 03_gold_star_schema.py        # Gold layer: star schema construction
│
├── dashboard/
│   └── restaurant_dashboard.pbix     # Power BI dashboard file
│
├── docs/
│   └── architecture_diagram.png      # Pipeline architecture diagram
│
└── README.md
```

---

🚀 How to Run

Prerequisites

· Databricks Community Edition account
· Apache Airflow installed (Ubuntu/Linux recommended)
· Power BI Desktop

Steps

1. Upload data to Databricks

```
Upload CSV and JSON files to Databricks FileStore
Run: SHOW TABLES to verify tables are created
```

2. Run notebooks in order

```
01_bronze_ingestion.py  →  Creates bronze_orders
02_silver_cleaning.py   →  Creates silver_orders
03_gold_star_schema.py  →  Creates gold_fact_orders + 6 dimensions
```

3. Deploy Airflow DAG

```bash
cp dags/restaurant_pipeline_dag.py $AIRFLOW_HOME/dags/
airflow dags trigger restaurant_medallion_pipeline
```

4. Connect Power BI

```
Export Gold tables as CSV from Databricks
Load into Power BI Desktop
Relationships already configured in star schema
```

---

👩‍💻 Author

Yasmeen El Shamy
ITI Power BI Development Track — Big Data Engineering Project
GitHub: @Yasmeen327

---

📌 Key Learnings

· Medallion Architecture is essential for large-scale data quality management
· Deduplication at scale requires careful key identification — order_id was the correct grain
· Profit modeling with assumed costs is a valid analytical technique when cost data is unavailable — the key is transparency about assumptions
· Pipeline orchestration with Airflow transforms a notebook exercise into a production system
· Star schema design decisions directly impact Power BI performance and DAX complexity

```
``
