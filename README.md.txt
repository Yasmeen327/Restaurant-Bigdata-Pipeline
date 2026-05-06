# 🍽 Egyptian Restaurant Big Data Pipeline

## Overview
End-to-end Big Data pipeline processing **11M+ records** from a multi-branch Egyptian restaurant chain using **Databricks**, **PySpark**, **Apache Airflow**, and **Power BI**.

## Architecture
Raw Data (11.1M records)
7 CSV + 2 JSON files
↓
┌─────────────────┐
│   BRONZE LAYER  │  → Unified raw Delta table (11.1M rows)
│   (Databricks)  │  → unionByName across all 9 source files
└─────────────────┘
↓
┌─────────────────┐
│   SILVER LAYER  │  → Cleaned & engineered (2.49M rows)
│   (PySpark)     │  → Removed 2M duplicates + 51K bad records
│                 │  → Profit modeling (3 cost drivers)
└─────────────────┘
↓
┌─────────────────┐
│   GOLD LAYER    │  → Star Schema ready for analytics
│   (Delta Lake)  │  → 1 Fact table + 6 Dimension tables
└─────────────────┘
↓
┌─────────────────┐
│    POWER BI     │  → 4-page Executive Dashboard
│   Dashboard     │  → Profit Analysis + What-If Simulator
└─────────────────┘

## Data Quality Results
| Metric | Value |
|--------|-------|
| Raw Records | 11,110,000 |
| Duplicate Order IDs Removed | 2,000,000 |
| Invalid Price Records Removed | 51,442 |
| Clean Unique Orders | 2,497,678 |
| Null Values Found | 0 |

## Business Results
| KPI | Value |
|-----|-------|
| Total Revenue | 654.5M EGP |
| Total Profit | 443.97M EGP |
| Avg Profit Margin | 65.34% |
| Avg Order Value | 262 EGP |
| Avg Rating | 3.70 / 5 |
| Date Range | 2020 – 2025 |

## Tech Stack
| Tool | Purpose |
|------|---------|
| Databricks (Community Edition) | Data processing & Delta Lake storage |
| Apache Spark / PySpark | Large-scale data transformation |
| Delta Lake | ACID-compliant storage layer |
| Apache Airflow | Pipeline orchestration & scheduling |
| Power BI | Business intelligence dashboard |
| Python | DAG development & data engineering |

## Profit Model Assumptions
Since cost data was not available in the dataset, profit was modeled using industry-standard assumptions:

| Cost Driver | Assumption |
|-------------|------------|
| Food Cost | 30% of order revenue |
| Delivery Cost | 15 EGP flat per delivery order |
| Card Processing Fee | 1.5% of order value for card payments |

## Dashboard Pages
1. **Executive Overview** — Revenue, Profit, Orders, Rating KPIs + trends
2. **Profit Analysis** — Branch profit table, category margins, business insights
3. **Customer Insights** — CLV, churn rate, customer trends
4. **What-If Simulator** — Scenario analysis with 4 interactive parameters

## Author
**Yasmeen El Shamy**
ITI Power BI Development Track — Big Data Project
GitHub: [@Yasmeen327](https://github.com/Yasmeen327)

