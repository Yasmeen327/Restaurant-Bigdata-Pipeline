# Databricks notebook source
csv_df = spark.table("restaurant_orders_csv")
json_df = spark.table("restaurant_orders_json")

bronze_df = csv_df.unionByName(json_df)

bronze_df.write.format("delta").mode("overwrite").saveAsTable("bronze_orders")
print(f"Bronze: {bronze_df.count()} rows")


# COMMAND ----------

from pyspark.sql import functions as F

df = spark.table("bronze_orders")

print("=== SHAPE ===")
print(f"Rows: {df.count()}, Columns: {len(df.columns)}")

print("\n=== NULL COUNTS ===")
df.select([F.count(F.when(F.col(c).isNull(), c)).alias(c) for c in df.columns]).show()

print("\n=== DUPLICATE ORDER IDs ===")
from pyspark.sql.functions import count
dup_count = df.groupBy("order_id").count().filter("count > 1").count()
print(f"Duplicate order_ids: {dup_count}")

print("\n=== DATE RANGE ===")
df.selectExpr("min(order_date)", "max(order_date)").show()

print("\n=== NEGATIVE OR ZERO AMOUNTS ===")
print(f"Zero/negative total_amount: {df.filter(F.col('total_amount') <= 0).count()}")
print(f"Zero/negative price: {df.filter(F.col('price') <= 0).count()}")
print(f"Zero/negative quantity: {df.filter(F.col('quantity') <= 0).count()}")

print("\n=== DISCOUNT RANGE ===")
df.selectExpr("min(discount)", "max(discount)", "avg(discount)").show()

print("\n=== RATING RANGE ===")
df.selectExpr("min(rating)", "max(rating)").show()
df.groupBy("rating").count().orderBy("rating").show()

print("\n=== BRANCH VALUES ===")
df.groupBy("branch").count().orderBy("branch").show()

print("\n=== ORDER TYPE VALUES ===")
df.groupBy("order_type").count().show()

print("\n=== PAYMENT METHOD VALUES ===")
df.groupBy("payment_method").count().show()

print("\n=== HOUR RANGE ===")
df.selectExpr("min(hour)", "max(hour)").show()
df.filter(F.col("hour") < 0).count()
df.filter(F.col("hour") > 23).count()

# COMMAND ----------

from pyspark.sql import functions as F

df = spark.table("bronze_orders")

silver_df = (
    df
    # ── TYPE CASTING ──────────────────────────────────────────
    .withColumn("order_date",    F.to_date("order_date", "yyyy-MM-dd"))
    .withColumn("hour",          F.col("hour").cast("integer"))
    .withColumn("price",         F.col("price").cast("double"))
    .withColumn("quantity",      F.col("quantity").cast("integer"))
    .withColumn("discount",      F.col("discount").cast("double"))
    .withColumn("total_amount",  F.col("total_amount").cast("double"))
    .withColumn("rating",        F.col("rating").cast("integer"))
    .withColumn("is_weekend",    F.col("is_weekend").cast("integer"))
    .withColumn("customer_id",   F.col("customer_id").cast("string"))
    .withColumn("order_id",      F.col("order_id").cast("string"))

    # ── REMOVE BAD RECORDS ────────────────────────────────────
    # Drop zero or negative amounts and prices
    .filter(F.col("total_amount") > 0)
    .filter(F.col("price") > 0)

    # ── DEDUPLICATE ───────────────────────────────────────────
    # Keep the first occurrence of each order_id
    .dropDuplicates(["order_id"])

    # ── STANDARDIZE TEXT ──────────────────────────────────────
    .withColumn("order_type",      F.initcap(F.trim("order_type")))
    .withColumn("payment_method",  F.initcap(F.trim("payment_method")))
    .withColumn("branch",          F.trim("branch"))
    .withColumn("category",        F.trim("category"))
    .withColumn("item_name",       F.trim("item_name"))

    # ── DATE FEATURES ─────────────────────────────────────────
    .withColumn("year",         F.year("order_date"))
    .withColumn("month",        F.month("order_date"))
    .withColumn("month_name",   F.date_format("order_date", "MMMM"))
    .withColumn("day_of_week",  F.dayofweek("order_date"))
    .withColumn("quarter",      F.quarter("order_date"))

    # ── TIME BUCKET ───────────────────────────────────────────
    .withColumn("time_of_day",
        F.when(F.col("hour") < 12, "Morning")
         .when(F.col("hour") < 17, "Afternoon")
         .when(F.col("hour") < 21, "Evening")
         .otherwise("Night"))

    # ── PROFIT ENGINEERING ────────────────────────────────────
    # Assumption 1: Food cost = 30% of revenue (industry standard)
    # Assumption 2: Delivery cost = 15 EGP flat per delivery order
    # Assumption 3: Card processing fee = 1.5% of total amount
    .withColumn("food_cost",
        F.round(F.col("total_amount") * 0.30, 2))
    .withColumn("delivery_cost",
        F.when(F.col("order_type") == "Delivery", 15.0).otherwise(0.0))
    .withColumn("payment_cost",
        F.when(F.col("payment_method") == "Card",
               F.round(F.col("total_amount") * 0.015, 2))
         .otherwise(0.0))
    .withColumn("total_cost",
        F.round(F.col("food_cost") + F.col("delivery_cost") + F.col("payment_cost"), 2))
    .withColumn("profit",
        F.round(F.col("total_amount") - F.col("total_cost"), 2))
    .withColumn("profit_margin",
        F.round((F.col("profit") / F.col("total_amount")) * 100, 2))
)

silver_df.write.format("delta").mode("overwrite").saveAsTable("silver_orders")

print(f"Bronze rows:         {df.count():,}")
print(f"After removing bad:  {df.filter(F.col('total_amount') > 0).filter(F.col('price') > 0).count():,}")
print(f"Silver (deduped):    {silver_df.count():,}")
print(f"Rows removed:        {df.count() - silver_df.count():,}")

# COMMAND ----------

# ── FACT TABLE ────────────────────────────────────────────────
fact_orders = spark.table("silver_orders").select(
    "order_id", "order_date", "customer_id", "branch",
    "category", "item_name", "payment_method", "order_type",
    "price", "quantity", "discount", "total_amount",
    "food_cost", "delivery_cost", "payment_cost", "total_cost",
    "profit", "profit_margin", "rating", "is_weekend",
    "hour", "time_of_day", "year", "month", "month_name",
    "quarter", "day_of_week"
)
fact_orders.write.format("delta").mode("overwrite").saveAsTable("gold_fact_orders")
print(f"✅ gold_fact_orders: {fact_orders.count():,} rows")

# ── DIM: Date ─────────────────────────────────────────────────
dim_date = spark.table("silver_orders").select(
    "order_date", "year", "month", "month_name",
    "quarter", "day_of_week", "is_weekend"
).dropDuplicates(["order_date"]).orderBy("order_date")
dim_date.write.format("delta").mode("overwrite").saveAsTable("gold_dim_date")
print(f"✅ gold_dim_date: {dim_date.count():,} rows")

# ── DIM: Branch ───────────────────────────────────────────────
dim_branch = spark.table("silver_orders").select(
    "branch"
).dropDuplicates(["branch"]).orderBy("branch")
dim_branch.write.format("delta").mode("overwrite").saveAsTable("gold_dim_branch")
print(f"✅ gold_dim_branch: {dim_branch.count():,} rows")

# ── DIM: Category ─────────────────────────────────────────────
dim_category = spark.table("silver_orders").select(
    "category", "item_name"
).dropDuplicates(["category", "item_name"]).orderBy("category")
dim_category.write.format("delta").mode("overwrite").saveAsTable("gold_dim_category")
print(f"✅ gold_dim_category: {dim_category.count():,} rows")

# ── DIM: Payment ──────────────────────────────────────────────
dim_payment = spark.table("silver_orders").select(
    "payment_method"
).dropDuplicates(["payment_method"])
dim_payment.write.format("delta").mode("overwrite").saveAsTable("gold_dim_payment")
print(f" gold_dim_payment: {dim_payment.count():,} rows")

# ── DIM: Customer ─────────────────────────────────────────────
dim_customer = spark.table("silver_orders").select(
    "customer_id"
).dropDuplicates(["customer_id"])
dim_customer.write.format("delta").mode("overwrite").saveAsTable("gold_dim_customer")
print(f" gold_dim_customer: {dim_customer.count():,} rows")

# ── DIM: Time ─────────────────────────────────────────────────
dim_time = spark.table("silver_orders").select(
    "hour", "time_of_day"
).dropDuplicates(["hour"]).orderBy("hour")
dim_time.write.format("delta").mode("overwrite").saveAsTable("gold_dim_time")
print(f" gold_dim_time: {dim_time.count():,} rows")

print("\n Gold layer complete!")

# COMMAND ----------

spark.sql("""
    SELECT
        COUNT(*)                            AS total_orders,
        ROUND(SUM(total_amount), 0)         AS total_revenue,
        ROUND(SUM(profit), 0)              AS total_profit,
        ROUND(AVG(profit_margin), 2)       AS avg_profit_margin,
        ROUND(AVG(total_amount), 2)        AS avg_order_value,
        ROUND(AVG(rating), 2)              AS avg_rating,
        MIN(order_date)                    AS from_date,
        MAX(order_date)                    AS to_date
    FROM gold_fact_orders
""").show()

# COMMAND ----------

spark.table("gold_fact_orders") \
    .coalesce(1) \
    .write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv("/Volumes/workspace/default/csv_uploads/gold_fact_orders_export")

print(" Done! CSV exported to /Volumes/workspace/default/csv_uploads/gold_fact_orders_export")