# Databricks notebook source
spark.table("gold_dim_branch") \
    .coalesce(1) \
    .write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv("/Volumes/workspace/default/csv_uploads/gold_dim_branch_export")
print(" branch done")

# COMMAND ----------

spark.table("gold_dim_category") \
    .coalesce(1) \
    .write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv("/Volumes/workspace/default/csv_uploads/gold_dim_category_export")
print("category done")

# COMMAND ----------

spark.table("gold_dim_payment") \
    .coalesce(1) \
    .write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv("/Volumes/workspace/default/csv_uploads/gold_dim_payment_export")
print("payment done")

# COMMAND ----------

spark.table("gold_dim_customer") \
    .coalesce(1) \
    .write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv("/Volumes/workspace/default/csv_uploads/gold_dim_customer_export")
print("customer done")

# COMMAND ----------

spark.table("gold_dim_time") \
    .coalesce(1) \
    .write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv("/Volumes/workspace/default/csv_uploads/gold_dim_time_export")
print("time done")