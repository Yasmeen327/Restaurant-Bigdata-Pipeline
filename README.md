# Egyptian Restaurant Data Platform  
## End-to-End Medallion Architecture on Databricks (11.1M+ Records | 2020–2025)

> A production-grade analytics system simulating a multi-branch restaurant chain in Egypt.  
> Built entirely on **Databricks** (Spark + Delta Lake), orchestrated with **Apache Airflow**, and delivered through **Power BI**.

This is my Big Data project for the ITI Power BI Development Track – built to demonstrate enterprise-ready data engineering skills.

---

## Dashboard Previews

| Page | Preview |
|------|---------|
| Executive Overview | `assets/overview.png` |
| Profit Analysis | `assets/profit-analysis.png` |
| Customer Insights | `assets/customer-insights.png` |
| What-If Simulator | `assets/what-if-simulator.png` |

---

## Why This Project Matters

This isn't just a dashboard. It's a complete data platform that:

- Processes 11.1 million raw records from 9 disparate files (7 CSV + 2 JSON)
- Runs a Medallion Architecture (Bronze → Silver → Gold) entirely on Databricks
- Uses PySpark for distributed data transformation
- Stores everything in Delta Lake for ACID compliance and time travel
- Orchestrates daily runs with Apache Airflow
- Delivers 4 interactive Power BI pages with profit modeling, what-if simulation, and customer retention analysis

---

## Databricks – The Heart of the Pipeline

### Why Databricks?

| Feature | How I Used It |
|---------|----------------|
| Unified workspace | All notebooks (Bronze, Silver, Gold) in one place |
| Delta Lake | ACID transactions, schema enforcement, time travel |
| PySpark | Distributed processing of 11M rows |
| Auto-loader | Incremental ingestion from cloud storage |
| SQL Analytics | Quick validation queries after each layer |

### Databricks Notebooks

**01_bronze_layer.ipynb**
- Input: 7 CSV + 2 JSON files
- Operations: unionByName, schema unification, Delta write
- Output: `bronze_restaurant` (11,110,000 rows)

**02_silver_layer.ipynb**
- Input: `bronze_restaurant`
- Operations: Deduplication (2M rows removed), price filter (51K rows removed), profit modeling (3 cost drivers), feature engineering (`time_of_day`, `is_weekend`, `year`, `quarter`)
- Output: `silver_restaurant` (2,497,678 rows)

**03_gold_layer.ipynb**
- Input: `silver_restaurant`
- Operations: Create star schema (1 fact table + 6 dimension tables), enforce relationships
- Output: `gold_fact_orders` + 6 dimension tables

### Databricks SQL Examples

```sql
-- Bronze: Unified ingestion
CREATE OR REPLACE TABLE bronze_restaurant
USING DELTA
AS SELECT * FROM csv.`/path/restaurants`
UNION ALL
SELECT * FROM json.`/path/orders`;

-- Silver: Deduplication using ROW_NUMBER
CREATE OR REPLACE TABLE silver_restaurant AS
SELECT * FROM (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY order_date) as row_num
    FROM bronze_restaurant
) WHERE row_num = 1;

-- Silver: Add profit column
CREATE OR REPLACE TABLE silver_restaurant_with_profit AS
SELECT *,
    total_amount - 
    (total_amount * 0.30) - 
    CASE WHEN order_type = 'Delivery' THEN 15 ELSE 0 END - 
    CASE WHEN payment_method = 'Card' THEN total_amount * 0.015 ELSE 0 END AS profit
FROM silver_restaurant;


Complete Architecture
Below is the end-to-end data flow from raw sources to the final Power BI dashboard, including orchestration via Apache Airflow.

flowchart TD
    CSV[7 CSV Files]
    JSON[2 JSON Files]
    
    BRONZE[Bronze Layer<br/>11,110,000 rows<br/>Delta Table]
    SILVER[Silver Layer<br/>Cleaning + Profit Model<br/>2,497,678 rows]
    GOLD[Gold Layer<br/>Star Schema<br/>Fact + 6 Dimensions]
    
    DAG[Airflow DAG<br/>Daily at 2 AM]
    
    DASH[Power BI Dashboard<br/>4 Pages]

    CSV --> BRONZE
    JSON --> BRONZE
    BRONZE --> SILVER
    SILVER --> GOLD
    GOLD --> DASH

    DAG -.-> BRONZE
    DAG -.-> SILVER
    DAG -.-> GOLD
Airflow DAG – Production Orchestration
File: restaurant_pipeline_dag.py

Workflow Tasks (in order):

start_task

ingest_bronze – load 9 files to Delta table

clean_silver – dedupe, filter, profit calc

build_gold – star schema (fact + dims)

data_quality – validate row counts and nulls

notify_success – Slack webhook alert

end_task

Configuration	Value
Schedule	0 2 * * * (daily 2 AM)
Retries	3 attempts with 5-minute delay
Timeout	60 minutes
Alerting	Slack webhook (success/failure)








Profit Modeling (Silver Layer)
Since actual cost data wasn't available, I built a deterministic financial model directly in PySpark:

Cost Driver	Assumption	Annual Impact
Food cost	30 percent of revenue	~196M EGP
Delivery cost	15 EGP per delivery order	~11M EGP
Card processing fee	1.5 percent of card transactions	~2.95M EGP
Result: Average profit margin = 65.34 percent

Power BI Dashboard – 4 Pages
Page 1: Executive Overview
KPI cards: Revenue (654.5M), Profit (444M), Margin (65.34%), Orders (2.5M), Rating (3.70)

Revenue trend by year (2020 to 2025)

Revenue by branch (Cairo highest)

Top 5 items by revenue

Payment method distribution

Data quality snapshot showing 8.6M rows removed

Page 2: Profit Analysis
Branch Performance Table:

Branch	Revenue	Net Profit	Margin	Status
Cairo	229M	155M	70%	Strong
Giza	131M	89M	69%	Strong
Alexandria	131M	89M	68%	Average
Mansoura	65M	44M	67%	Average
Tanta	65M	44M	66%	Average
Assiut	33M	22M	64%	At Risk
Actionable Insights:

Assiut margin is 64 percent, 6 points below Cairo. High delivery mix at 42 percent is eroding profit. Push weekend dine-in promotions.

Grills deliver 68 percent margin. Increasing menu share by 5 percent could add about 7M EGP to annual profit.

Card payments cost 1.5 percent. Shifting card users to Wallet saves about 1.4M EGP per year.

Page 3: Customer Insights
Key Metrics:

Total Customers: 200,000

Active Customers: 175,000

Churn Rate: 12.6 percent

Avg Orders per Customer: 12.49

CLV by Branch (Customer Lifetime Value):

Cairo: 1,159 EGP

Alexandria: 714 EGP

Giza: 714 EGP

Tanta: 458 EGP

Mansoura: 458 EGP

Assiut: 351 EGP

Customer Segmentation:

New customers (1 order): 0.4 percent

Regular customers (2 to 5 orders): 1.5 percent

Loyal customers (6+ orders): 98.1 percent

Business Recommendations:

Cairo customers have 3.2 times higher lifetime value than Assiut. Investigate frequency versus order value.

98 percent of customers are loyal. Launch a VIP referral program.

Churn rate at 12.6 percent. Target at-risk branches with win-back offers.

Page 4: What-If Simulator
Parameter	Default	Business Impact
Delivery Order Percent Increase	+13%	Each 1% adds about 417 orders per month
Cash to Digital Payment Shift	+15%	Saves 1.5 percent per transaction
Average Discount Reduction	-2%	Current discount is 3.6 percent
Menu Price Increase	+5%	Each 1% adds about 6.5M revenue
Combined Impact:

Revenue Impact: +49M EGP annually

Profit Impact: +31.9M EGP annually

New Profit Margin: 66.0 percent (vs 65.3 percent)

Data Quality Results
Stage	Records
Raw ingestion (Bronze)	11,110,000
After duplicate removal	9,110,000
After price filter	9,058,558
After joins (Gold)	2,497,678
Quality Gates Enforced:

Duplicate detection using ROW_NUMBER window function

Price validation removing negative or zero values

Schema enforcement across all 9 sources

Referential integrity between fact and dimension tables

Tech Stack
Layer	Technology
Data Lake	Delta Lake (Databricks)
Processing	Apache Spark (PySpark)
Orchestration	Apache Airflow
BI and Analytics	Power BI
Languages	Python, SQL, DAX
Version Control	GitHub
Repository Structure
text
Egyptian-Restaurant-Platform/
├── assets/
│   ├── overview.png
│   ├── profit-analysis.png
│   ├── customer-insights.png
│   └── what-if-simulator.png
├── notebooks/
│   ├── 01_bronze_layer.ipynb
│   ├── 02_silver_layer.ipynb
│   └── 03_gold_layer.ipynb
├── airflow/
│   └── restaurant_pipeline_dag.py
├── powerbi/
│   └── restaurant_dashboard.pbix
├── README.md
└── requirements.txt
How to Reproduce
Databricks Setup
Import 3 notebooks into Databricks workspace

Mount source files (CSV and JSON) to DBFS

Run bronze, then silver, then gold sequentially

Export Gold tables as Parquet

Airflow Deployment
Copy DAG to Airflow dags folder

Configure Slack webhook for alerts

Start scheduler and trigger DAG

Power BI
Open .pbix file

Connect to exported Gold tables

Publish to Power BI Service

Data Engineering Highlights
Capability	Implementation
Scalability	PySpark distributed processing for 11M rows
Idempotency	Delta Lake overwrite-safe operations
Data Quality	Deduplication, null handling, referential integrity
Orchestration	Airflow DAG with retries and Slack alerts
Star Schema	Fact table plus 6 dimensions
Profit Modeling	3 cost drivers embedded in PySpark
Simulation Layer	Power BI what-if parameters
Business KPIs
Metric	Value
Total Revenue	654.5M EGP
Total Profit	444.0M EGP
Average Profit Margin	65.34 percent
Average Order Value	262 EGP
Average Rating	3.70 out of 5
Total Clean Orders	2,497,678
Date Range	2020 to 2025
Branches	6
Author
Yasmeen El Shamy
GitHub: Yasmeen327

License
MIT License – free for educational and professional use with attribution.









