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

# Total Customers day 16
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

# Estimated CLTV day 17
customer_summary["estimated_cltv"] = (
    customer_summary["average_order_value"] *
    customer_summary["purchase_frequency"]
)
# Customer Ranking
customer_summary["cltv_rank"] = (
    customer_summary["estimated_cltv"]
    .rank(ascending=False)
)
customer_summary.head()

"""**Day 18 – Customer Segmentation**"""
# Calculate Quantiles Once
q25 = customer_summary["estimated_cltv"].quantile(0.25)
q50 = customer_summary["estimated_cltv"].quantile(0.50)
q75 = customer_summary["estimated_cltv"].quantile(0.75)
# Customer Segmentation
def segment(cltv):
    if cltv >= q75:
        return "Premium"
    elif cltv >= q50:
        return "High"
    elif cltv >= q25:
        return "Medium"
    else:
        return "Low"
customer_summary["segment"] = customer_summary["estimated_cltv"].apply(segment)
customer_summary["segment"].value_counts()

"""**Day 19 – Business Insights**"""
# Top Customers
top_customers = customer_summary.nlargest(
    10,
    "estimated_cltv"
)
# Bottom Customers
bottom_customers = customer_summary.nsmallest(
    10,
    "estimated_cltv"
)
# Summary Statistics
average_cltv = customer_summary["estimated_cltv"].mean()
median_cltv = customer_summary["estimated_cltv"].median()
highest_cltv = customer_summary["estimated_cltv"].max()
lowest_cltv = customer_summary["estimated_cltv"].min()
# Segment Summary
segment_summary = (
    customer_summary
    .groupby("segment")["estimated_cltv"]
    .mean()
)
print(segment_summary)

"""**Day 20 – Finalize & Export Dataset**"""
# Dataset Validation
customer_summary.info()
customer_summary.describe()
customer_summary.isnull().sum()
customer_summary.duplicated().sum()
# Export Dataset
customer_summary.to_csv(
    "cltv_dataset.csv",
    index=False
)
print("Dataset Exported Successfully!")

"""**Day 21 – Validation & Documentation**"""
# Final Verification
print(customer_summary.shape)
print(customer_summary.columns)
print(customer_summary.dtypes)
customer_summary.describe()
customer_summary.head()
print("Week 3 Completed Successfully!")
