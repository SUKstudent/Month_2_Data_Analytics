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


# Total Customers
total_customers = customer_summary["customer_unique_id"].nunique()

# Total Orders
total_orders = customer_summary["total_orders"].sum()
# Purchase Frequency
purchase_frequency = total_orders / total_customers
# Add Purchase Frequency
customer_summary["purchase_frequency"] = purchase_frequency
# Repeat Customers
repeat_customers = customer_summary[
    customer_summary["total_orders"] > 1
]
# One-Time Customers
one_time_customers = customer_summary[
    customer_summary["total_orders"] == 1
]
# Customer Statistics
print(f"Purchase Frequency : {purchase_frequency:.2f}")
print(f"Repeat Customers : {len(repeat_customers)}")
print(f"One-Time Customers : {len(one_time_customers)}")
