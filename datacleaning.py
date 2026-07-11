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
