# Import Required Libraries day 15
import pandas as pd
import numpy as np
# Load Datasets
orders = pd.read_csv("/content/orders_cleaned.csv")
customers = pd.read_csv("/content/olist_customers_dataset.csv")
order_items = pd.read_csv("/content/order_items_cleaned.csv")
# Merge Orders with Customers
orders_customers = pd.merge(
    orders,
    customers,
    on="customer_id",
    how="left"
)
# Merge with Order Items
orders_complete = pd.merge(
    orders_customers,
    order_items,
    on="order_id",
    how="left"
)
# Customer Purchase Summary
customer_summary = (
    orders_complete
    .groupby("customer_unique_id")
    .agg(
        total_orders=("order_id", "nunique"),
        total_revenue=("price", "sum")
    )
    .reset_index()
)
# Average Order Value (AOV)
customer_summary["average_order_value"] = (
    customer_summary["total_revenue"] /
    customer_summary["total_orders"]
)
# Preview Dataset
customer_summary.head()
# Dataset Information
customer_summary.info()
