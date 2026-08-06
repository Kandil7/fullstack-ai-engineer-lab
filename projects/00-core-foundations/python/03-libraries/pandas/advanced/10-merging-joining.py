"""
Pandas Merging & Joining: merge, join, concat, combine_first
=============================================================

Combining DataFrames using SQL-style joins and other methods.
"""

import pandas as pd
import numpy as np

np.random.seed(42)

# =============================================================================
# 1. CREATE SAMPLE DATA
# =============================================================================

print("=" * 60)
print("1. SAMPLE DATASETS")
print("=" * 60)

# Employees
employees = pd.DataFrame({
    'emp_id': [1, 2, 3, 4, 5, 6],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank'],
    'dept_id': [10, 20, 10, 30, 20, 40],
    'salary': [75000, 82000, 90000, 65000, 88000, 72000],
    'hire_date': pd.to_datetime(['2020-01-15', '2019-03-22', '2021-07-10', '2022-02-01', '2018-11-30', '2023-05-15'])
})
print("Employees:")
print(employees)
print()

# Departments
departments = pd.DataFrame({
    'dept_id': [10, 20, 30, 50],
    'dept_name': ['Engineering', 'Sales', 'Marketing', 'Finance'],
    'location': ['NYC', 'SF', 'LA', 'Chicago'],
    'budget': [1000000, 500000, 300000, 800000]
})
print("Departments:")
print(departments)
print()

# Projects
projects = pd.DataFrame({
    'project_id': [100, 101, 102, 103],
    'project_name': ['Website Redesign', 'Mobile App', 'Data Pipeline', 'API Gateway'],
    'emp_id': [1, 3, 2, 5],  # Lead engineer
    'budget': [50000, 75000, 100000, 60000]
})
print("Projects:")
print(projects)
print()

# Performance reviews
reviews = pd.DataFrame({
    'emp_id': [1, 2, 3, 4, 5, 6],
    'review_year': [2023, 2023, 2023, 2023, 2023, 2023],
    'score': [4.2, 3.8, 4.5, 3.9, 4.3, 4.0],
    'promoted': [True, False, True, False, True, False]
})
print("Performance Reviews:")
print(reviews)
print()

# =============================================================================
# 2. MERGE - SQL-STYLE JOINS
# =============================================================================

print("=" * 60)
print("2. MERGE - SQL-STYLE JOINS")
print("=" * 60)

# Inner join (default)
inner = pd.merge(employees, departments, on='dept_id', how='inner')
print("INNER JOIN (employees x departments):")
print(inner[['name', 'dept_name', 'location']])
print()

# Left join
left = pd.merge(employees, departments, on='dept_id', how='left')
print("LEFT JOIN (all employees, dept info if exists):")
print(left[['name', 'dept_name', 'location']])
print()

# Right join
right = pd.merge(employees, departments, on='dept_id', how='right')
print("RIGHT JOIN (all departments, employee info if exists):")
print(right[['name', 'dept_name', 'location']])
print()

# Outer join
outer = pd.merge(employees, departments, on='dept_id', how='outer')
print("OUTER JOIN (all records from both):")
print(outer[['name', 'dept_name', 'location']])
print()

# Merge on different column names
emp_proj = pd.merge(employees, projects, left_on='emp_id', right_on='emp_id', how='left')
print("Merge employees with projects (different key names):")
print(emp_proj[['name', 'project_name', 'project_id']])
print()

# Multiple merge keys
# Create data with composite keys
df1 = pd.DataFrame({
    'year': [2022, 2022, 2023, 2023],
    'quarter': [1, 2, 1, 2],
    'region': ['North', 'North', 'South', 'South'],
    'sales': [100, 150, 200, 250]
})
df2 = pd.DataFrame({
    'year': [2022, 2022, 2023, 2023],
    'quarter': [1, 2, 1, 2],
    'region': ['North', 'North', 'South', 'South'],
    'target': [120, 160, 180, 280]
})
merged_multi = pd.merge(df1, df2, on=['year', 'quarter', 'region'])
print("Merge on multiple keys:")
print(merged_multi)
print()

# Merge with suffixes
emp_reviews = pd.merge(employees, reviews, on='emp_id', how='left', suffixes=('_emp', '_review'))
print("Merge with suffixes:")
print(emp_reviews[['name', 'score', 'promoted']])
print()

# =============================================================================
# 3. JOIN - INDEX-BASED
# =============================================================================

print("=" * 60)
print("3. JOIN - INDEX-BASED")
print("=" * 60)

# Set index
emp_indexed = employees.set_index('emp_id')
dept_indexed = departments.set_index('dept_id')

# Join on index
joined = emp_indexed.join(dept_indexed, on='dept_id', how='left', lsuffix='_emp', rsuffix='_dept')
print("Join on index (employees indexed by emp_id):")
print(joined[['name', 'dept_name', 'location']])
print()

# Join multiple
# NOTE: .join([df1, df2]) does NOT support suffixes ("Suffixes not supported when
# joining multiple DataFrames"), so chain pairwise joins and rename first to avoid
# the 'budget' column collision
projects_indexed = projects.set_index('emp_id').rename(columns={'budget': 'project_budget'})
joined_multi = (emp_indexed
    .join(dept_indexed, how='left', rsuffix='_dept')
    .join(projects_indexed, how='left', rsuffix='_proj'))
print("Join multiple DataFrames:")
print(joined_multi[['name', 'dept_name', 'project_name', 'project_budget']])
print()

# =============================================================================
# 4. CONCAT - STACKING
# =============================================================================

print("=" * 60)
print("4. CONCAT - STACKING DATAFRAMES")
print("=" * 60)

# Vertical concat (stack rows)
df_2022 = pd.DataFrame({'month': [1, 2, 3], 'sales': [100, 120, 110], 'year': 2022})
df_2023 = pd.DataFrame({'month': [1, 2, 3], 'sales': [130, 140, 135], 'year': 2023})
df_2024 = pd.DataFrame({'month': [1, 2, 3], 'sales': [150, 160, 155], 'year': 2024})

concat_vert = pd.concat([df_2022, df_2023, df_2024], ignore_index=True)
print("Vertical concat (ignore_index=True):")
print(concat_vert)
print()

# With keys (creates MultiIndex)
concat_keys = pd.concat([df_2022, df_2023, df_2024], keys=['2022', '2023', '2024'], names=['year'])
print("Concat with keys:")
print(concat_keys)
print()

# Horizontal concat (stack columns)
df_a = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
df_b = pd.DataFrame({'C': [7, 8, 9], 'D': [10, 11, 12]})
concat_horiz = pd.concat([df_a, df_b], axis=1)
print("Horizontal concat (axis=1):")
print(concat_horiz)
print()

# Concat with different columns (outer join)
df_diff1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df_diff2 = pd.DataFrame({'B': [5, 6], 'C': [7, 8]})
concat_outer = pd.concat([df_diff1, df_diff2], ignore_index=True, sort=False)
print("Concat different columns (outer):")
print(concat_outer)
print()

# Inner join concat
concat_inner = pd.concat([df_diff1, df_diff2], join='inner')
print("Concat inner join (common columns only):")
print(concat_inner)
print()

# =============================================================================
# 5. COMBINE_FIRST & UPDATE
# =============================================================================

print("=" * 60)
print("5. COMBINE_FIRST & UPDATE")
print("=" * 60)

# combine_first - fill missing from another DataFrame
df_main = pd.DataFrame({
    'A': [1, np.nan, 3],
    'B': [np.nan, 5, np.nan],
    'C': [7, 8, 9]
})
df_fill = pd.DataFrame({
    'A': [10, 20, 30],
    'B': [40, 50, 60],
    'D': [70, 80, 90]
})

combined = df_main.combine_first(df_fill)
print("combine_first (fill NaN from df_fill):")
print(combined)
print()

# update - modify in place
df_update = df_main.copy()
df_update.update(df_fill)
print("update (in-place modification):")
print(df_update)
print()

# =============================================================================
# 6. MERGE ASOF - NEAREST MATCH
# =============================================================================

print("=" * 60)
print("6. MERGE_ASOF - NEAREST MATCH (TIME SERIES)")
print("=" * 60)

# Stock prices
prices = pd.DataFrame({
    'time': pd.date_range('2023-01-01 09:30', periods=10, freq='5min'),
    'price': [100, 101, 100.5, 102, 101.5, 103, 102.5, 104, 103.5, 105]
})
# Trades
trades = pd.DataFrame({
    'time': pd.to_datetime(['2023-01-01 09:31', '2023-01-01 09:36', '2023-01-01 09:42']),
    'quantity': [100, 200, 150],
    'side': ['buy', 'sell', 'buy']
})

print("Prices:")
print(prices)
print("\nTrades:")
print(trades)

# merge_asof - backward (nearest prior)
trades_with_price = pd.merge_asof(trades, prices, on='time', direction='backward')
print("\nmerge_asof (direction='backward' - nearest prior price):")
print(trades_with_price)
print()

# forward
trades_forward = pd.merge_asof(trades, prices, on='time', direction='forward')
print("merge_asof (direction='forward' - nearest future price):")
print(trades_forward)
print()

# nearest
trades_nearest = pd.merge_asof(trades, prices, on='time', direction='nearest')
print("merge_asof (direction='nearest' - closest price):")
print(trades_nearest)
print()

# =============================================================================
# 7. PRACTICAL PATTERNS
# =============================================================================

print("=" * 60)
print("7. PRACTICAL PATTERNS")
print("=" * 60)

# Pattern 1: Slowly Changing Dimensions (SCD Type 2)
print("Pattern 1: SCD Type 2 - Historical tracking")
# Current state
current = pd.DataFrame({
    'customer_id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'email': ['alice@old.com', 'bob@email.com', 'charlie@email.com'],
    'tier': ['Gold', 'Silver', 'Bronze'],
    'valid_from': pd.to_datetime(['2023-01-01', '2023-01-01', '2023-01-01']),
    'valid_to': pd.NaT,
    'is_current': [True, True, True]
})
# New state
new = pd.DataFrame({
    'customer_id': [1, 4],
    'name': ['Alice', 'David'],
    'email': ['alice@new.com', 'david@email.com'],
    'tier': ['Platinum', 'Bronze']
})
new['valid_from'] = pd.Timestamp('2023-06-01')
new['valid_to'] = pd.NaT
new['is_current'] = True

# Expire old record for customer 1
current.loc[current['customer_id'] == 1, ['valid_to', 'is_current']] = [pd.Timestamp('2023-05-31'), False]
scd = pd.concat([current, new], ignore_index=True)
print("SCD Type 2 result:")
print(scd)
print()

# Pattern 2: Fuzzy merge (approximate string matching)
print("Pattern 2: Fuzzy matching concept")
from difflib import get_close_matches

df_customers = pd.DataFrame({'customer_name': ['Alice Smith', 'Bob Johnson', 'Charlie Brown']})
df_orders = pd.DataFrame({'customer_name': ['A. Smith', 'Robert Johnson', 'C. Brown']})

def fuzzy_merge(df1, df2, key1, key2, threshold=0.6):
    matches = []
    for val in df1[key1]:
        close = get_close_matches(val, df2[key2].tolist(), n=1, cutoff=threshold)
        matches.append(close[0] if close else None)
    df1['matched'] = matches
    return pd.merge(df1, df2, left_on='matched', right_on=key2, how='left')

fuzzy_result = fuzzy_merge(df_customers.copy(), df_orders.copy(), 'customer_name', 'customer_name')
print("Fuzzy merge result:")
print(fuzzy_result[['customer_name_x', 'customer_name_y']])
print()

# Pattern 3: Self-join (hierarchical data)
print("Pattern 3: Self-join for hierarchy")
org = pd.DataFrame({
    'emp_id': [1, 2, 3, 4, 5],
    'name': ['CEO', 'CTO', 'CFO', 'VP Eng', 'VP Sales'],
    'manager_id': [None, 1, 1, 2, 2]
})
org_self = pd.merge(org, org, left_on='manager_id', right_on='emp_id', how='left', 
                    suffixes=('', '_mgr'))
print("Org chart with manager names:")
print(org_self[['name', 'name_mgr']])
print()

# Pattern 4: Merge with indicator
print("Pattern 4: Merge with indicator")
merge_with_indicator = pd.merge(employees, departments, on='dept_id', how='outer', indicator=True)
print("Merge indicator:")
print(merge_with_indicator[['name', 'dept_name', '_merge']])
print()

# =============================================================================
# 8. PERFORMANCE TIPS
# =============================================================================

print("=" * 60)
print("8. PERFORMANCE TIPS")
print("=" * 60)

# 1. Use appropriate join type (inner < left < outer)
# 2. Merge on indexed columns when possible
# 3. Use categorical for string join keys
# 4. Avoid merging on multiple columns if possible
# 5. Use merge_asof for time series

import time

# Create larger DataFrames
n = 100000
df_large1 = pd.DataFrame({
    'key': np.random.randint(0, 10000, n),
    'value1': np.random.randn(n)
})
df_large2 = pd.DataFrame({
    'key': np.random.randint(0, 10000, n),
    'value2': np.random.randn(n)
})

# Time merge
start = time.time()
result = pd.merge(df_large1, df_large2, on='key', how='inner')
print(f"Merge 100k rows: {time.time() - start:.4f}s")

# With categorical
df_large1_cat = df_large1.copy()
df_large2_cat = df_large2.copy()
df_large1_cat['key'] = df_large1_cat['key'].astype('category')
df_large2_cat['key'] = df_large2_cat['key'].astype('category')

start = time.time()
result_cat = pd.merge(df_large1_cat, df_large2_cat, on='key', how='inner')
print(f"Merge 100k rows (categorical): {time.time() - start:.4f}s")

print("\n" + "=" * 60)
print("END OF MERGING & JOINING")
print("=" * 60)