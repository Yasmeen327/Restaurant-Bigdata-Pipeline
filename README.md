# 🍽️ Egyptian Restaurant Data Platform  
## End-to-End Medallion Architecture on Databricks (11.1M+ Records | 2020–2025)

> **A production-grade analytics system** simulating a multi-branch restaurant chain in Egypt.  
> Built entirely on **Databricks** (Spark + Delta Lake), orchestrated with **Apache Airflow**, and delivered through **Power BI**.

📌 **This is my Big Data project for the ITI Power BI Development Track – built to demonstrate enterprise-ready data engineering skills.**

---

## 📸 Dashboard Previews

| Page | Preview |
|------|---------|
| Executive Overview | ![Overview](assets/overview.png) |
| Profit Analysis | ![Profit Analysis](assets/profit-analysis.png) |
| Customer Insights | ![Customer Insights](assets/customer-insights.png) |
| What-If Simulator | ![What-If Simulator](assets/what-if-simulator.png) |

---

## 🎯 Why This Project Matters

This isn't just a dashboard. It's a **complete data platform** that:

- Processes **11.1M+ raw records** from 9 disparate files (CSV + JSON)
- Runs a **Medallion Architecture** (Bronze → Silver → Gold) entirely on Databricks
- Uses **PySpark** for distributed data transformation
- Stores everything in **Delta Lake** for ACID compliance and time travel
- Orchestrates daily runs with **Apache Airflow**
- Delivers **4 interactive Power BI pages** with profit modeling, what-if simulation, and customer retention analysis

> 💡 **My instructor loves Databricks. So I built the entire pipeline there – from raw ingestion to star schema.**

---

## 🧱 Databricks – The Heart of the Pipeline

### Why Databricks?

| Feature | How I Used It |
|---------|----------------|
| **Unified workspace** | All notebooks (Bronze, Silver, Gold) in one place |
| **Delta Lake** | ACID transactions, schema enforcement, time travel |
| **PySpark** | Distributed processing of 11M+ rows |
| **Auto-loader** | Incremental ingestion from cloud storage |
| **SQL Analytics** | Quick validation queries after each layer |
| **Cluster management** | Optimized for community edition (single node) |

### Databricks Notebooks (3)

```mermaid
flowchart LR
    N1[01_bronze_layer.ipynb] --> N2[02_silver_layer.ipynb]
    N2 --> N3[03_gold_layer.ipynb]
Notebook	Input	Operations	Output	Rows
01_bronze_layer	7 CSV + 2 JSON	unionByName, schema unification, Delta write	bronze_restaurant	11,110,000
02_silver_layer	bronze_restaurant	Deduplication (2M rows), price filter (51K rows), profit modeling (3 cost drivers), feature engineering (time_of_day, is_weekend, year, quarter)	silver_restaurant	2,497,678
03_gold_layer	silver_restaurant	Create star schema: 1 fact table + 6 dimension tables, enforce relationships, validate referential integrity	gold_fact_orders + dim_date, dim_branch, dim_category, dim_customer, dim_payment, dim_time	2,497,678
Databricks – Beautiful Features I Used
sql
-- Bronze: Unified ingestion
CREATE OR REPLACE TABLE bronze_restaurant
USING DELTA
AS SELECT * FROM csv.`/path/restaurants`
UNION ALL
SELECT * FROM json.`/path/orders`;

-- Silver: Deduplication with window
DELETE FROM silver_restaurant
WHERE order_id IN (
    SELECT order_id FROM (
        SELECT order_id, ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY order_date) as rn
        FROM bronze_restaurant
    ) WHERE rn > 1
);

-- Silver: Profit modeling
ALTER TABLE silver_restaurant ADD COLUMNS (
    profit DECIMAL(12,2) GENERATED ALWAYS AS (
        total_amount - 
        (total_amount * 0.30) - 
        (CASE WHEN order_type = 'Delivery' THEN 15 ELSE 0 END) - 
        (CASE WHEN payment_method = 'Card' THEN total_amount * 0.015 ELSE 0 END)
    )
);

-- Gold: Star schema with foreign keys
CREATE TABLE gold_fact_orders AS
SELECT 
    o.order_id,
    d.date_key,
    b.branch_key,
    c.category_key,
    p.payment_key,
    o.customer_id,
    t.time_key,
    o.total_amount,
    o.profit
FROM silver_restaurant o
LEFT JOIN dim_date d ON o.order_date = d.date
LEFT JOIN dim_branch b ON o.branch = b.branch_name
LEFT JOIN dim_category c ON o.category = c.category_name
LEFT JOIN dim_payment p ON o.payment_method = p.method;
📐 Complete Architecture

flowchart TD
    subgraph SOURCES[Raw Data Sources]
        CSV[7 CSV Files]
        JSON[2 JSON Files]
    end

    subgraph DATABRICKS[Databricks Platform]
        direction TB
        BRONZE[🔵 Bronze Layer<br>11,110,000 rows<br>Delta Table]
        SILVER[🟡 Silver Layer<br>Cleaning + Profit Model<br>2,497,678 rows]
        GOLD[🟢 Gold Layer<br>Star Schema<br>Fact + 6 Dimensions]
    end

    subgraph AIRFLOW[Apache Airflow]
        DAG[restaurant_medallion_pipeline<br>Daily @ 2 AM]
    end

    subgraph POWERBI[Power BI]
        DASH[4-Page Dashboard<br>Executive • Profit • Customers • What-If]
    end

    CSV --> BRONZE
    JSON --> BRONZE
    BRONZE --> SILVER
    SILVER --> GOLD
    GOLD --> DASH

    DAG -.-> BRONZE
    DAG -.-> SILVER
    DAG -.-> GOLD










⚙️ Airflow DAG – Production Orchestration
Located in: restaurant_pipeline_dag.py

text
┌──────────────┐
│   start_task │
└──────┬───────┘
       ▼
┌──────────────┐
│ ingest_bronze│  ← Load 9 files → Delta table
└──────┬───────┘
       ▼
┌──────────────┐
│ clean_silver │  ← Dedupe, filter, profit calc
└──────┬───────┘
       ▼
┌──────────────┐
│  build_gold  │  ← Star schema (fact + dims)
└──────┬───────┘
       ▼
┌──────────────┐
│ data_quality │  ← Validate row counts & nulls
└──────┬───────┘
       ▼
┌──────────────┐
│notify_success│  ← Slack webhook alert
└──────┬───────┘
       ▼
┌──────────────┐
│   end_task   │
└──────────────┘
Configuration	Value
Schedule	0 2 * * * (daily 2 AM)
Retries	3 attempts (5-minute delay)
Timeout	60 minutes
Alerting	Slack webhook (success/failure)
Catchup	False
💰 Profit Modeling (Silver Layer)
Since actual cost data wasn't available, I built a deterministic financial model directly in PySpark:

Cost Driver	Assumption	Annual Impact
Food cost	30% of revenue	~196M EGP
Delivery cost	15 EGP per delivery order	~11M EGP
Card processing fee	1.5% of card transactions	~2.95M EGP
Result: Average profit margin = 65.34% (consistent with Egyptian QSR benchmarks)

📊 Power BI Dashboard – 4 Pages
Page 1: Executive Overview
KPI cards: Revenue (654.5M), Profit (444M), Margin (65.34%), Orders (2.5M), Rating (3.70)

Revenue trend by year (2020–2025)

Revenue by branch (Cairo #1)

Top 5 items by revenue

Payment method distribution

Data quality snapshot – 8.6M rows removed, 99.5% trust score

Page 2: Profit Analysis
Branch performance table with margin grading

Actionable insights: Assiut improvement, grill margin opportunity, card→wallet savings

Conditional formatting (green/gold/red based on margin)

Page 3: Customer Insights
200K total customers, 175K active, 12.6% churn

CLV (Customer Lifetime Value) by branch (bar chart)

Customer segmentation (New / Regular / Loyal)

Business recommendations for low-CLV branches

Page 4: What-If Simulator
4 interactive parameters (delivery %, digital shift, discount reduction, price increase)

Live updates to revenue impact (+49M), profit impact (+31.9M), new margin (66.0%)

Same-page simulation – no need to switch tabs

📈 Data Quality Results
Stage	Records
Raw ingestion (Bronze)	11,110,000
After duplicate removal	9,110,000
After price filter	9,058,558
After joins (Gold)	2,497,678
Quality gates enforced:

Duplicate detection (ROW_NUMBER() window)

Price validation (negative/zero removal)

Schema enforcement across all 9 sources

Referential integrity (fact → dim keys)

Null handling (explicit defaults)

🛠️ Complete Tech Stack
Layer	Technology	Why
Data Lake	Delta Lake (Databricks)	ACID, time travel, schema enforcement
Processing	Apache Spark (PySpark)	Distributed 11M+ row processing
Orchestration	Apache Airflow	Production scheduling, retries, alerts
BI & Analytics	Power BI	Interactive dashboards, what-if parameters
Languages	Python, SQL, DAX	End-to-end control
Version Control	GitHub	Portfolio-ready
📁 Repository Structure
text
Egyptian-Restaurant-Platform/
│
├── assets/                      # Dashboard screenshots
│   ├── overview.png
│   ├── profit-analysis.png
│   ├── customer-insights.png
│   └── what-if-simulator.png
│
├── notebooks/                   # Databricks notebooks
│   ├── 01_bronze_layer.ipynb
│   ├── 02_silver_layer.ipynb
│   └── 03_gold_layer.ipynb
│
├── airflow/
│   └── restaurant_pipeline_dag.py
│
├── powerbi/
│   └── restaurant_dashboard.pbix
│
├── README.md
└── requirements.txt
🚀 How to Reproduce (Data Engineering Focus)
1. Databricks Setup
Import 3 notebooks into Databricks workspace

Mount source files (CSV + JSON) to DBFS

Run 01_bronze_layer → 02_silver_layer → 03_gold_layer

Verify row counts at each stage

Export Gold tables as Parquet

2. Airflow Deployment
Copy restaurant_pipeline_dag.py to ~/airflow/dags/

Configure Slack webhook for alerts

Start scheduler: airflow scheduler

Trigger DAG: airflow dags trigger restaurant_medallion_pipeline

3. Power BI
Open restaurant_dashboard.pbix

Connect to exported Gold tables

Publish to Power BI Service

🧠 Data Engineering Highlights
Capability	Implementation
Scalability	PySpark distributed processing (11M+ rows)
Idempotency	Delta Lake MERGE / overwrite-safe operations
Data Quality	Deduplication, null handling, referential integrity
Orchestration	Airflow DAG with retries and Slack alerts
Immutability	Bronze → Silver → Gold with time travel
Star Schema	Fact + 6 dimensions for BI optimization
Profit Modeling	3 cost drivers embedded in PySpark
Simulation Layer	Power BI what-if parameters
📊 Business KPIs (Final)
Metric	Value
Total Revenue	654.5M EGP
Total Profit	444.0M EGP
Average Profit Margin	65.34%
Average Order Value	262 EGP
Average Rating	3.70 / 5
Total Clean Orders	2,497,678
Date Range	2020 – 2025
Branches	6 (Cairo, Giza, Alexandria, Mansoura, Tanta, Assiut)
👩‍💻 Author
Yasmeen El Shamy
ITI – Power BI Development Track
Big Data Project – Job Portfolio

GitHub: @Yasmeen327

Focus: Data Engineering, Analytics Systems, BI Architecture

📌 This project is my ticket to a data engineering or BI role. Every line of code, every visual, and every insight was built with production standards in mind.

📜 License
MIT License – free for educational and professional use with attribution.



