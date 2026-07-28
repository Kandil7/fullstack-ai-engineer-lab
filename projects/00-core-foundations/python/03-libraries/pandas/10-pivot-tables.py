"""
Pandas Pivot Tables: pivot_table, crosstab, melt, pivot
========================================================

Reshaping data from long to wide format and vice versa.
"""

import pandas as pd
import numpy as np

np.random.seed(42)

# Create sample sales data
dates = pd.date_range('2023-01-01', periods=200, freq='D')
df = pd.DataFrame({
    'date': np.random.choice(dates, 200),
    'region': np.random.choice(['North', 'South', 'East', 'West'], 200),
    'product': np.random.choice(['Widget A', 'Widget B', 'Gadget X', 'Gadget Y'], 200),
    'sales_rep': np.random.choice(['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'], 200),
    'quantity': np.random.randint(1, 50, 200),
    'unit_price': np.random.choice([10.0, 25.0, 50.0, 75.0, 100.0], 200),
})
df['revenue'] = df['quantity'] * df['unit_price']
df['month'] = df['date'].dt.month
df['quarter'] = df['date'].dt.quarter

print("Sample Sales Data:")
print(df.head(10))
print(f"Shape: {df.shape}")
print()

# =============================================================================
# 1. PIVOT_TABLE
# =============================================================================

print("=" * 60)
print("1. PIVOT_TABLE")
print("=" * 60)

# Basic pivot table
pivot1 = pd.pivot_table(df, values='revenue', index='region', columns='product', aggfunc='sum')
print("Revenue by Region x Product:")
print(pivot1.round(2))
print()

# Multiple values
pivot2 = pd.pivot_table(df, 
                        values=['revenue', 'quantity'], 
                        index='region', 
                        columns='product', 
                        aggfunc={'revenue': 'sum', 'quantity': 'mean'})
print("Revenue (sum) and Quantity (mean) by Region x Product:")
print(pivot2.round(2))
print()

# Multiple index/columns
pivot3 = pd.pivot_table(df,
                        values='revenue',
                        index=['region', 'sales_rep'],
                        columns='product',
                        aggfunc='sum',
                        fill_value=0)
print("Revenue by Region+Sales Rep x Product:")
print(pivot3.round(2).head(10))
print()

# With margins (subtotals/grand total)
pivot4 = pd.pivot_table(df,
                        values='revenue',
                        index='region',
                        columns='product',
                        aggfunc='sum',
                        margins=True,
                        margins_name='Total')
print("With margins (subtotals):")
print(pivot4.round(2))
print()

# Multiple aggregation functions
pivot5 = pd.pivot_table(df,
                        values='revenue',
                        index='region',
                        columns='product',
                        aggfunc=['sum', 'mean', 'count'],
                        fill_value=0)
print("Multiple aggfuncs (sum, mean, count):")
print(pivot5.round(2))
print()

# =============================================================================
# 2. CROSSTAB
# =============================================================================

print("=" * 60)
print("2. CROSSTAB (CONTINGENCY TABLES)")
print("=" * 60)

# Basic crosstab - frequency count
ct1 = pd.crosstab(df['region'], df['product'])
print("Frequency count: Region x Product:")
print(ct1)
print()

# Crosstab with values and aggfunc
ct2 = pd.crosstab(df['region'], df['product'], values=df['revenue'], aggfunc='sum')
print("Sum of revenue: Region x Product:")
print(ct2.round(2))
print()

# Normalize (proportions)
ct3 = pd.crosstab(df['region'], df['product'], normalize='index')
print("Row proportions (normalize='index'):")
print(ct3.round(3))
print()

ct4 = pd.crosstab(df['region'], df['product'], normalize='columns')
print("Column proportions (normalize='columns'):")
print(ct4.round(3))
print()

ct5 = pd.crosstab(df['region'], df['product'], normalize='all')
print("Overall proportions (normalize='all'):")
print(ct5.round(3))
print()

# Multiple row/column variables
ct6 = pd.crosstab([df['region'], df['sales_rep']], df['product'], margins=True)
print("Multi-index crosstab:")
print(ct6)
print()

# =============================================================================
# 3. MELT (WIDE TO LONG)
# =============================================================================

print("=" * 60)
print("3. MELT - WIDE TO LONG")
print("=" * 60)

# Create wide format data
wide_df = pd.DataFrame({
    'employee': ['Alice', 'Bob', 'Charlie'],
    'jan_sales': [1000, 1500, 1200],
    'feb_sales': [1100, 1600, 1300],
    'mar_sales': [1200, 1700, 1400],
    'jan_target': [900, 1400, 1100],
    'feb_target': [1000, 1500, 1200],
    'mar_target': [1100, 1600, 1300],
})
print("Wide format:")
print(wide_df)
print()

# Melt all value columns
melted = pd.melt(wide_df, 
                 id_vars=['employee'], 
                 var_name='metric_month', 
                 value_name='value')
print("Melted (all value cols):")
print(melted.head(12))
print()

# Melt with specific value columns
melted2 = pd.melt(wide_df,
                  id_vars=['employee'],
                  value_vars=['jan_sales', 'feb_sales', 'mar_sales'],
                  var_name='month',
                  value_name='sales')
print("Melted (only sales):")
print(melted2)
print()

# Split metric and month
melted2['metric'] = melted2['month'].str.split('_').str[0]
melted2['month'] = melted2['month'].str.split('_').str[1]
print("Split metric and month:")
print(melted2)
print()

# =============================================================================
# 4. PIVOT (SIMPLE RESHAPING)
# =============================================================================

print("=" * 60)
print("4. PIVOT (SIMPLE RESHAPING)")
print("=" * 60)

# Pivot requires unique index/column combinations
df_unique = df.drop_duplicates(subset=['region', 'product', 'month']).head(20)
print("Unique subset for pivot:")
print(df_unique[['region', 'product', 'month', 'revenue']].head(10))
print()

pivot_simple = df_unique.pivot(index='region', columns='product', values='revenue')
print("Simple pivot:")
print(pivot_simple.round(2))
print()

# Pivot with multiple index
df_unique2 = df.drop_duplicates(subset=['region', 'sales_rep', 'product']).head(20)
pivot_multi = df_unique2.pivot(index=['region', 'sales_rep'], columns='product', values='revenue')
print("Pivot with multi-index:")
print(pivot_multi.round(2).head(10))
print()

# =============================================================================
# 5. STACK / UNSTACK
# =============================================================================

print("=" * 60)
print("5. STACK / UNSTACK")
print("=" * 60)

# Start with pivot table result
pivot_result = pd.pivot_table(df,
                              values='revenue',
                              index=['region', 'sales_rep'],
                              columns='product',
                              aggfunc='sum',
                              fill_value=0)
print("Pivot table result:")
print(pivot_result.round(2))
print()

# Stack - columns to index
stacked = pivot_result.stack()
print("Stacked (columns -> index):")
print(stacked.head(12))
print(f"Type: {type(stacked)}")
print()

# Unstack - index to columns
unstacked = stacked.unstack()
print("Unstacked (back to wide):")
print(unstacked.round(2))
print()

# Unstack specific level
unstacked_level = stacked.unstack(level=0)  # unstack region
print("Unstack level=0 (region):")
print(unstacked_level.round(2))
print()

# =============================================================================
# 6. WIDE TO LONG WITH WIDE_TO_LONG
# =============================================================================

print("=" * 60)
print("6. WIDE_TO_LONG")
print("=" * 60)

# Create wide data with numbered columns
wide_numbered = pd.DataFrame({
    'id': [1, 2, 3],
    'X_1': [10, 20, 30],
    'X_2': [11, 21, 31],
    'X_3': [12, 22, 32],
    'Y_1': [100, 200, 300],
    'Y_2': [110, 210, 310],
    'Y_3': [120, 220, 320],
})
print("Wide with numbered cols:")
print(wide_numbered)
print()

# wide_to_long
long_numbered = pd.wide_to_long(wide_numbered, 
                                 stubnames=['X', 'Y'], 
                                 i='id', 
                                 j='time')
print("wide_to_long result:")
print(long_numbered.reset_index())
print()

# =============================================================================
# 7. PRACTICAL EXAMPLES
# =============================================================================

print("=" * 60)
print("7. PRACTICAL EXAMPLES")
print("=" * 60)

# Example 1: Sales dashboard summary
print("Example 1: Sales Dashboard")
dashboard = pd.pivot_table(df,
                          values=['revenue', 'quantity'],
                          index='region',
                          columns='product',
                          aggfunc={'revenue': 'sum', 'quantity': 'sum'},
                          margins=True,
                          margins_name='Total')
print(dashboard.round(2))
print()

# Example 2: Monthly trend by product
monthly_trend = pd.pivot_table(df,
                              values='revenue',
                              index='month',
                              columns='product',
                              aggfunc='sum',
                              fill_value=0)
print("Monthly revenue trend by product:")
print(monthly_trend.round(2))
print()

# Example 3: Rep performance matrix
rep_perf = pd.crosstab(df['sales_rep'], df['product'], 
                       values=df['revenue'], aggfunc='sum', margins=True)
print("Sales Rep x Product performance:")
print(rep_perf.round(2))
print()

# Example 4: Cohort analysis prep
# Create cohort data
cohort_data = pd.DataFrame({
    'customer_id': range(1, 101),
    'signup_month': np.random.choice(pd.date_range('2023-01', '2023-06', freq='MS'), 100),
    'month_1_revenue': np.random.exponential(50, 100).round(2),
    'month_2_revenue': np.random.exponential(40, 100).round(2),
    'month_3_revenue': np.random.exponential(30, 100).round(2),
})
cohort_data['signup_month'] = cohort_data['signup_month'].dt.to_period('M')

# Melt for cohort analysis
cohort_long = pd.melt(cohort_data,
                      id_vars=['customer_id', 'signup_month'],
                      value_vars=['month_1_revenue', 'month_2_revenue', 'month_3_revenue'],
                      var_name='period',
                      value_name='revenue')
cohort_long['period_num'] = cohort_long['period'].str.extract(r'(\d+)').astype(int)

cohort_pivot = pd.pivot_table(cohort_long,
                             values='revenue',
                             index='signup_month',
                             columns='period_num',
                             aggfunc='mean')
print("Cohort analysis (avg revenue by signup month and period):")
print(cohort_pivot.round(2))
print()

# Example 4: Cohort analysis with pivot
# Create cohort data
np.random.seed(42)
cohort_data = pd.DataFrame({
    'customer_id': range(1, 101),
    'signup_month': pd.date_range('2023-01', '2023-06', freq='MS').repeat(17)[:100],
    'month_1_revenue': np.random.exponential(50, 100).round(2),
    'month_2_revenue': np.random.exponential(40, 100).round(2),
    'month_3_revenue': np.random.exponential(30, 100).round(2),
})
cohort_data['signup_month'] = cohort_data['signup_month'].dt.to_period('M')

# Melt for cohort analysis
cohort_long = pd.melt(cohort_data,
                      id_vars=['customer_id', 'signup_month'],
                      value_vars=['month_1_revenue', 'month_2_revenue', 'month_3_revenue'],
                      var_name='period',
                      value_name='revenue')
cohort_long['period_num'] = cohort_long['period'].str.extract(r'(\d+)').astype(int)

cohort_pivot = pd.pivot_table(cohort_long,
                             values='revenue',
                             index='signup_month',
                             columns='period_num',
                             aggfunc='mean')
print("Cohort analysis (avg revenue by signup month and period):")
print(cohort_pivot.round(2))
print()

# Example 5: Feature engineering from pivot
# Create customer-product matrix
customer_product = pd.crosstab(df['sales_rep'], df['product'], 
                               values=df['revenue'], aggfunc='sum', fill_value=0)
print("Customer-Product matrix (for ML features):")
print(customer_product.round(2))
print()

# =============================================================================
# 8. SUMMARY: WHEN TO USE WHAT
# =============================================================================

print("=" * 60)
print("8. SUMMARY: WHEN TO USE WHAT")
print("=" * 60)

summary = """
| Function        | Use Case                                    | Input Shape | Output Shape |
|-----------------|---------------------------------------------|-------------|--------------|
| pivot_table     | Aggregation with multiple groupings         | Long        | Wide         |
| crosstab        | Frequency counts, contingency tables        | Long        | Wide         |
| melt            | Wide to long (tidy data)                    | Wide        | Long         |
| pivot           | Simple reshape (no aggregation)             | Long        | Wide         |
| stack/unstack   | Move between hierarchical index/columns     | Wide/Long   | Long/Wide    |
| wide_to_long    | Numbered column patterns (X_1, X_2, ...)    | Wide        | Long         |

Key Principles:
- Long format = "tidy data" (one row per observation)
- Wide format = human-readable, good for reporting
- pivot_table/crosstab: aggregate + reshape in one step
- melt: essential for plotting (seaborn, ggplot), ML feature prep
"""
print(summary)

print("=" * 60)
print("END OF PIVOT TABLES")
print("=" * 60)