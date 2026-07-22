#Week2
# Find first purchase month for each customer day 8
cohort = orders.groupby('customer_id')['OrderMonth'].min().reset_index()
# Rename column
cohort.rename(columns={'OrderMonth': 'CohortMonth'}, inplace=True)
# Merge with orders dataset
orders = orders.merge(cohort, on='customer_id')
# Verify
print(orders[['customer_id', 'OrderMonth', 'CohortMonth']].head())

# Calculate year and month difference day 9
year_diff = orders['OrderMonth'].dt.year - orders['CohortMonth'].dt.year
month_diff = orders['OrderMonth'].dt.month - orders['CohortMonth'].dt.month
# Create Cohort Index
orders['CohortIndex'] = year_diff * 12 + month_diff + 1
# Verify
print(orders[['customer_id','OrderMonth','CohortMonth','CohortIndex']].head())

# Count unique customers day 10
cohort_data = orders.groupby(
    ['CohortMonth', 'CohortIndex']
)['customer_id'].nunique().reset_index()

# Create retention matrix
retention_matrix = cohort_data.pivot_table(
    index='CohortMonth',
    columns='CohortIndex',
    values='customer_id'
)
# Verify
print(retention_matrix)

# First month's customers day 11
cohort_size = retention_matrix.iloc[:, 0]
# Calculate retention percentage
retention_percentage = retention_matrix.divide(cohort_size, axis=0) * 100
# Round values
retention_percentage = retention_percentage.round(2)
# Verify
print(retention_percentage)

# Replace missing values day 12
retention_percentage = retention_percentage.fillna(0)
# Verify
print(retention_percentage)

# Average retention by cohort
print("Average Retention by Cohort")
print(retention_percentage.mean(axis=1))

# Average retention by month
print("\nAverage Retention by Month")
print(retention_percentage.mean())
