# 🍽️ Egyptian Restaurant Data Platform  ## End-to-End Medallion Architecture on Databricks (11.1M+ Records | 2020–2025)> A production-grade analytics system simulating a multi-branch restaurant chain in Egypt.  > Built using **Databricks (Apache Spark + Delta Lake)**, orchestrated with **Apache Airflow**, and delivered through **Power BI**.This project was developed as part of the ITI Power BI Development Track and is designed to demonstrate **end-to-end data engineering and analytics capabilities** in a realistic business scenario.---# 📊 Dashboard Previews## Executive Overview![Executive Overview](assets/overview.png)## Profit Analysis![Profit Analysis](assets/profit-analysis.png)## Customer Insights![Customer Insights](assets/customer-insights.png)## What-If Simulator![What If Simulator](assets/what-if-simulator.png)---# 🚀 Project OverviewThis project implements a complete data platform that:- Processes **11.1M+ raw records** from 9 heterogeneous data sources (7 CSV + 2 JSON)- Applies **Medallion Architecture (Bronze → Silver → Gold)** for structured data transformation- Uses **PySpark** for scalable distributed processing- Stores data in **Delta Lake** with ACID guarantees and time travel support- Orchestrates workflows using **Apache Airflow**- Delivers **interactive dashboards in Power BI** with advanced analytics and simulation---# 🧱 System Architecture## High-Level Data Flow```mermaidflowchart TD    %% Data Sources    CSV[CSV Files (7)] --> INGEST    JSON[JSON Files (2)] --> INGEST    %% Ingestion    INGEST[Databricks Ingestion Layer] --> BRONZE    %% Medallion Layers    BRONZE[Bronze Layer<br>Raw Delta Table<br>11.1M rows] --> SILVER    SILVER[Silver Layer<br>Cleaning + Feature Engineering<br>2.49M rows] --> GOLD    GOLD[Gold Layer<br>Star Schema<br>Fact + 6 Dimensions] --> BI    %% Orchestration    AIRFLOW[Airflow DAG<br>Daily 2 AM] -.-> INGEST    AIRFLOW -.-> BRONZE    AIRFLOW -.-> SILVER    AIRFLOW -.-> GOLD    %% Consumption    BI[Power BI Dashboard<br>4 Pages]

Architecture Explanation
The system follows a layered Medallion Architecture:


Raw data is ingested from CSV and JSON sources into Databricks


The Bronze layer stores raw, unprocessed data in Delta format


The Silver layer applies data cleaning, deduplication, and feature engineering


The Gold layer structures the data into a star schema optimized for analytics


Apache Airflow orchestrates the pipeline with scheduled execution


Power BI consumes the Gold layer to deliver business insights


This design ensures:


Scalability using distributed Spark processing


Reliability through idempotent transformations


Performance via BI-optimized schema design



🧊 Databricks Implementation
Notebooks Overview
01_bronze_layer.ipynb


Ingest 7 CSV and 2 JSON files


Schema alignment using unionByName


Store as Delta table


Output:
bronze_restaurant — 11,110,000 rows

02_silver_layer.ipynb


Deduplication (~2M rows removed)


Remove invalid price records (51K rows)


Feature engineering:


time_of_day


year, quarter


is_weekend




Profit modeling


Output:
silver_restaurant — 2,497,678 rows

03_gold_layer.ipynb


Star schema modeling:


Fact table: gold_fact_orders


6 dimension tables




Relationship enforcement


Optimized for Power BI



Example SQL Transformation
SELECT * FROM (    SELECT *,           ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY order_date) AS rn    FROM bronze_restaurant)WHERE rn = 1;

⚙️ Apache Airflow Orchestration
DAG: restaurant_pipeline_dag.py
Pipeline Flow
start → ingest_bronze → clean_silver → build_gold → data_quality → notify → end
Configuration
SettingValueScheduleDaily at 02:00 AMRetries3Delay5 minutesTimeout60 minutesAlertsSlack
Design Considerations


Idempotent pipeline execution


Safe reprocessing


Automated monitoring and alerting



💰 Profit Modeling
Due to lack of cost data, a deterministic model was applied:
Cost DriverAssumptionFood Cost30% of revenueDelivery Cost15 EGP per orderCard Fee1.5% per transaction
Result:
Average profit margin = 65.34%

📊 Power BI Dashboard
Page 1 — Executive Overview


Revenue: 654.5M EGP


Profit: 444M EGP


Margin: 65.34%


Orders: 2.5M


Revenue trends and top categories



Page 2 — Profit Analysis


Branch performance comparison


Margin segmentation


Insights:


Assiut underperforming (64%)


Grill category highest margin (68%)





Page 3 — Customer Insights


Customers: 200K


Churn: 12.6%


Customer Lifetime Value (CLV)


Segmentation: New / Regular / Loyal



Page 4 — What-If Simulator


Delivery ratio changes


Pricing adjustments


Discount optimization


Impact:


+49M EGP revenue


+31.9M EGP profit


Margin improved to 66.0%



🧪 Data Quality
StageRecordsRaw (Bronze)11,110,000After Deduplication9,110,000Final (Gold)2,497,678
Quality Controls


Deduplication using window functions


Price validation


Schema enforcement


Referential integrity



🛠️ Tech Stack
LayerTechnologyStorageDelta LakeProcessingApache Spark (PySpark)OrchestrationApache AirflowBIPower BILanguagesPython, SQL, DAX

📁 Repository Structure
Egyptian-Restaurant-Platform/├── assets/│   ├── overview.png│   ├── profit-analysis.png│   ├── customer-insights.png│   └── what-if-simulator.png├── notebooks/│   ├── 01_bronze_layer.ipynb│   ├── 02_silver_layer.ipynb│   └── 03_gold_layer.ipynb├── airflow/│   └── restaurant_pipeline_dag.py├── powerbi/│   └── restaurant_dashboard.pbix├── README.md└── requirements.txt

🚀 How to Run
Databricks


Run Bronze → Silver → Gold notebooks sequentially


Airflow


Deploy DAG and start scheduler


Power BI


Connect to Gold tables and refresh dataset



🧠 Engineering Highlights


End-to-end Medallion Architecture


Large-scale Spark processing (11M+ records)


Production-style orchestration with Airflow


Star schema optimized for BI


Embedded financial modeling


Interactive simulation layer



👤 Author
Yasmeen El Shamy
ITI – Power BI Development Track
GitHub: @Yasmeen327

📜 License
MIT License
