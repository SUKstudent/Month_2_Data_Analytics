import pandas as pd
customers = pd.read_csv("/olist_customers_dataset.csv")
orders = pd.read_csv("/olist_orders_dataset.csv")
order_items = pd.read_csv("/olist_order_items_dataset.csv")
payments = pd.read_csv("/olist_order_payments_dataset.csv")
products = pd.read_csv("/olist_products_dataset.csv")
reviews = pd.read_csv("/olist_order_reviews_dataset.csv")
sellers = pd.read_csv("/olist_sellers_dataset.csv")
geolocation = pd.read_csv("/olist_geolocation_dataset.csv")
list1=[customers,order_items,orders,payments,sellers,reviews,products,geolocation]
for i in list1:
  print(i.head())
  print(i.shape)
  print(i.duplicated())
  i.info()
  print(i.isnull().sum())
# Check order status distribution
print("Order Status Distribution:")
print(orders['order_status'].value_counts())
# Keep only delivered orders
orders = orders[orders['order_status'] == 'delivered']
# Handle missing values in Orders
orders = orders.dropna(subset=[
    'order_approved_at',
    'order_delivered_customer_date'
])
# Handle missing values in Order Items
order_items = order_items.dropna()
# Handle missing values in Products
products['product_category_name'] = products['product_category_name'].fillna('Unknown')
products['product_name_lenght'] = products['product_name_lenght'].fillna(0)
products['product_description_lenght'] = products['product_description_lenght'].fillna(0)
products['product_photos_qty'] = products['product_photos_qty'].fillna(0)
products = products.dropna(subset=[
    'product_weight_g',
    'product_length_cm',
    'product_height_cm',
    'product_width_cm'
])
# Verify missing values after cleaning
print("\nOrders Missing Values:")
print(orders.isnull().sum())
print("\nOrder Items Missing Values:")
print(order_items.isnull().sum())
print("\nProducts Missing Values:")
print(products.isnull().sum())
# Check final dataset shapes
print("\nFinal Dataset Shapes:")
print("Orders:", orders.shape)
print("Order Items:", order_items.shape)
print("Products:", products.shape)

# Convert purchase timestamp into datetime
orders['order_purchase_timestamp'] = pd.to_datetime(
    orders['order_purchase_timestamp']
)
# Extract Purchase Month
orders['OrderMonth'] = orders['order_purchase_timestamp'].dt.to_period('M')
# Verify
print(orders[['order_purchase_timestamp', 'OrderMonth']].head())
print(orders.dtypes)
# Save cleaned datasets
orders.to_csv("orders_cleaned.csv", index=False)
order_items.to_csv("order_items_cleaned.csv", index=False)
products.to_csv("products_cleaned.csv", index=False)
print("Cleaned datasets saved successfully!")
# Merge Orders and Customers
cohort_df = pd.merge(
    orders,
    customers,
    on='customer_id',
    how='left'
)

# Merge Payments
cohort_df = pd.merge(
    cohort_df,
    payments,
    on='order_id',
    how='left'
)
# Verify merged dataset
print(cohort_df.head())
print(cohort_df.shape)
print(cohort_df.info())
# Calculate first purchase month of each customer
cohort_df['CohortMonth'] = (
    cohort_df.groupby('customer_unique_id')['order_purchase_timestamp']
             .transform('min')
             .dt.to_period('M')
)
# Verify
print(
    cohort_df[['customer_unique_id',
               'order_purchase_timestamp',
               'CohortMonth']].head()
)
# Save dataset
cohort_df.to_csv("cohort_dataset.csv", index=False)
