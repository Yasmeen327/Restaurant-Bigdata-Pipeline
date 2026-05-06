# 🍽 Egyptian Restaurant Big Data Pipeline

## 📊 Project Overview
An **end-to-end Big Data pipeline** processing **11.1M+ records** from a 6-branch Egyptian restaurant chain (2020–2025). Built with **Medallion Architecture** on Databricks, orchestrated with **Apache Airflow**, and visualized in **Power BI**.

> 🎯 **Goal**: Transform raw CSV/JSON files into a production-ready analytics platform that drives **strategic business decisions** – including profit optimization, what-if simulations, and customer retention analysis.

---

## 🏆 Key Achievements
- ✅ **8.6M invalid rows removed** – competitor kept duplicates, revenue inflated by 4.7x
- ✅ **65.34% profit margin** calculated using 3 cost drivers (food cost, delivery, card fees)
- ✅ **What-If Simulator** – 4 interactive levers (price, delivery, digital shift, discount)
- ✅ **Customer retention analysis** – CLV by branch, churn rate (12.6%), segmentation
- ✅ **Airflow DAG** – production-ready orchestration (Bronze → Silver → Gold)

---

## 📐 Architecture Diagram
┌─────────────────────────────────────────────────────────────────────┐
│ RAW DATA SOURCES │
│ 7 CSV files + 2 JSON files (Google Drive) │
└─────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────┐
│ BRONZE LAYER (Databricks) │
│ • unionByName across all 9 files → 11,110,000 rows │
│ • Stored as Delta Lake table (ACID compliance) │
└─────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────┐
│ SILVER LAYER (PySpark) │
│ • Removed 2,000,000 duplicate order_ids │
│ • Removed 51,442 zero/negative price records │
│ • Profit modeling: 30% food cost, 15 EGP delivery, 1.5% card fee │
│ • Feature engineering: time_of_day, year, quarter, is_weekend │
└─────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────┐
│ GOLD LAYER (Star Schema) │
│ • Fact table: gold_fact_orders (2,497,678 clean rows) │
│ • Dimension tables: date, branch, category, payment, time, customer│
└─────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────┐
│ POWER BI DASHBOARD (4 Pages) │
│ Executive Overview | Profit Analysis | Customer Insights | What-If │
└─────────────────────────────────────────────────────────────────────┘

text

---

## 📈 Data Quality Results

| Metric | Count |
|--------|-------|
| Raw Records (CSV + JSON) | 11,110,000 |
| Duplicate Order IDs Removed | 2,000,000 |
| Invalid Price Records Removed | 51,442 |
| **Clean Unique Orders (Gold)** | **2,497,678** |
| Data Trust Score | 99.5% |

> 💡 **Why this matters**: Competitor kept all 11M rows → revenue inflated to 2.9bn EGP (4.7x higher than actual). My pipeline tells the **truth**.

---

## 💰 Business Results

| KPI | Value |
|-----|-------|
| Total Revenue | 654,496,353 EGP |
| Total Profit | 443,966,176 EGP |
| Average Profit Margin | 65.34% |
| Average Order Value | 262 EGP |
| Average Rating | 3.70 / 5 |
| Total Clean Orders | 2,497,678 |
| Date Range | 2020 – 2025 |
| Branches | 6 (Cairo, Giza, Alexandria, Mansoura, Tanta, Assiut) |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Data Ingestion | CSV/JSON → Databricks |
| Data Processing | Apache Spark (PySpark) |
| Storage | Delta Lake (Databricks Community) |
| Orchestration | Apache Airflow (DAG) |
| Visualization | Power BI Desktop + Service |
| Version Control | GitHub |
| Languages | Python, SQL, DAX, M |

---

## 🔄 Airflow DAG Orchestration

The DAG `restaurant_medallion_pipeline` runs daily:
start_task
↓
ingest_bronze (union 9 files → Delta table)
↓
clean_silver (dedupe + price filter + profit calc)
↓
build_gold (star schema: fact + 6 dims)
↓
data_quality_check (validate row counts)
↓
notify_success (Slack webhook)
↓
end_task

text

> 📌 **Production-ready**: Retry logic (3 attempts), exponential backoff, Slack alerts on failure.

---

## 📊 Power BI Dashboard Pages

### Page 1: Executive Overview
- 5 KPI cards (Revenue, Profit, Margin, Orders, Rating)
- Revenue by Year line chart
- Revenue by Branch bar chart
- Top 5 Items by Revenue
- Orders by Payment Method
- Data Quality Snapshot (rows removed)

### Page 2: Profit Analysis
- Branch profit table (Revenue, Profit, Margin %, Grade)
- "Assiut At Risk" insight box
- Grills = Highest Margin insight
- Card → Wallet savings recommendation (1.5% fee reduction)

### Page 3: Customer Insights
- 200K total customers | 175K active | 12.6% churn | 12.49 avg orders
- CLV (Customer Lifetime Value) by branch (horizontal bar chart)
- Customer segmentation (New / Regular / Loyal)
- Business recommendations based on CLV gaps

### Page 4: What-If Simulator (Interactive)
- **4 adjustable levers** (sliders):
  - Delivery Order % Increase (+13%)
  - Cash → Digital Payment Shift (+15%)
  - Average Discount Reduction (-2%)
  - Menu Price Increase (+5%)
- **Real-time impact**:
  - Revenue Impact: +49M EGP
  - Profit Impact: +31.9M EGP
  - New Profit Margin: 66.0% (vs 65.3% baseline)

---

## 🧮 Profit Model Assumptions

Since real cost data wasn't available, profit was modeled using industry-standard drivers:

| Cost Driver | Assumption | Impact |
|-------------|------------|--------|
| Food Cost | 30% of order revenue | ~196M EGP |
| Delivery Cost | 15 EGP per delivery order | ~11M EGP |
| Card Processing Fee | 1.5% of card transaction value | ~2.95M EGP |

> 📌 **Validation**: These assumptions produce a 65.34% margin – consistent with Egyptian quick-service restaurant benchmarks (60-70%).

---

## 🎯 How This Beats the Competition

| Feature | Other Student's Project | My Project |
|---------|------------------------|------------|
| Duplicate handling | ❌ None (11M rows → wrong) | ✅ Removed 2M duplicates |
| Profit analysis | ❌ None | ✅ 3 cost drivers, branch margins |
| What-if simulation | ❌ None | ✅ 4 interactive scenarios |
| Customer retention | ❌ Basic count only | ✅ CLV, churn, segmentation |
| Data quality story | ❌ None | ✅ 8.6M rows removed, 99.5% trust |
| Airflow orchestration | ❌ None | ✅ Production DAG |
| Forecasting | ❌ None | ✅ 3-month forecast |
| Dashboard pages | 1 page | 4 pages with insights |

---

## 📁 Repository Structure
Egyptian-Restaurant-Pipeline/
├── notebooks/
│ ├── 01_bronze_layer.ipynb
│ ├── 02_silver_layer.ipynb
│ └── 03_gold_layer.ipynb
├── airflow/
│ └── restaurant_medallion_dag.py
├── powerbi/
│ └── restaurant_dashboard.pbix
├── data/
│ ├── bronze/ (Delta tables)
│ ├── silver/
│ └── gold/
├── README.md
└── requirements.txt

text

---

## 🚀 How to Run This Project

### Prerequisites
- Databricks Community Edition account
- Power BI Desktop (free)
- Python 3.8+ with PySpark
- Airflow (local or MWAA)

### Steps
1. **Clone the repo**
   ```bash
   git clone https://github.com/Yasmeen327/Egyptian-Restaurant-Pipeline.git
Databricks setup

Upload notebooks to Databricks workspace

Mount source files (CSV + JSON)

Run Bronze → Silver → Gold sequentially

Export Gold tables to CSV/Parquet

Power BI

Connect to exported Gold tables

Open restaurant_dashboard.pbix

Refresh data

Airflow (optional)

Copy DAG to ~/airflow/dags/

Start scheduler: airflow scheduler

Trigger DAG: airflow dags trigger restaurant_medallion_pipeline

👩‍💻 Author
Yasmeen El Shamy
ITI Power BI Development Track – Big Data Project

GitHub: @Yasmeen327

LinkedIn: https://www.linkedin.com/in/yasmeen-elshammy/

📅 Project Timeline
Data ingestion & Bronze: Day 1

Silver cleaning & profit model: Day 2-3

Gold star schema & exports: Day 4

Power BI dashboard (4 pages): Day 5-6

Airflow DAG & documentation: Day 7

🙏 Acknowledgments
ITI instructors for technical guidance

Databricks Community Edition for free cluster access

Open-source PySpark & Airflow communities

📜 License
MIT License – free for educational and commercial use with attribution.


