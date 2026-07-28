"""
Pandas MultiIndex: Hierarchical indexing, xs, swaplevel
========================================================

Advanced indexing with multiple levels for complex data structures.
"""

import pandas as pd
import numpy as np

np.random.seed(42)

# =============================================================================
# 1. CREATING MULTIINDEX
# =============================================================================

print("=" * 60)
print("1. CREATING MULTIINDEX")
print("=" * 60)

# From arrays
arrays = [
    ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C'],
    ['X', 'Y', 'Z', 'X', 'Y', 'Z', 'X', 'Y', 'Z']
]
index = pd.MultiIndex.from_arrays(arrays, names=['first', 'second'])
s = pd.Series(np.random.randn(9), index=index)
print("From arrays:")
print(s)
print()

# From tuples
tuples = [('A', 'X'), ('A', 'Y'), ('B', 'X'), ('B', 'Y')]
index2 = pd.MultiIndex.from_tuples(tuples, names=['letter', 'symbol'])
s2 = pd.Series([1, 2, 3, 4], index=index2)
print("From tuples:")
print(s2)
print()

# From product (cartesian product)
index3 = pd.MultiIndex.from_product([
    ['A', 'B', 'C'],
    ['X', 'Y'],
    [1, 2]
], names=['letter', 'symbol', 'number'])
s3 = pd.Series(range(len(index3)), index=index3)
print("From product:")
print(s3)
print()

# From DataFrame
df = pd.DataFrame({
    'region': ['North', 'North', 'South', 'South'],
    'product': ['A', 'B', 'A', 'B'],
    'sales': [100, 200, 150, 250]
})
df_multi = df.set_index(['region', 'product'])
print("From DataFrame set_index:")
print(df_multi)
print()

# =============================================================================
# 2. ACCESSING MULTIINDEX DATA
# =============================================================================

print("=" * 60)
print("2. ACCESSING MULTIINDEX DATA")
print("=" * 60)

# Create sample DataFrame
idx = pd.MultiIndex.from_product([
    ['2023', '2024'],
    ['Q1', 'Q2', 'Q3', 'Q4'],
    ['North', 'South', 'East', 'West']
], names=['year', 'quarter', 'region'])

df_multi = pd.DataFrame({
    'sales': np.random.randint(1000, 10000, len(idx)),
    'units': np.random.randint(10, 100, len(idx)),
    'profit': np.random.randint(100, 1000, len(idx))
}, index=idx)

print("Sample DataFrame shape:", df_multi.shape)
print(df_multi.head(12))
print()

# Select by level
print("df_multi.loc['2023'] (all 2023):")
print(df_multi.loc['2023'].head())
print()

print("df_multi.loc[('2023', 'Q1')] (2023 Q1):")
print(df_multi.loc[('2023', 'Q1')])
print()

print("df_multi.loc[('2023', 'Q1', 'North')] (specific):")
print(df_multi.loc[('2023', 'Q1', 'North')])
print()

# Slice with slice()
print("df_multi.loc[('2023', 'Q1'):('2023', 'Q2')] (slice):")
print(df_multi.loc[('2023', 'Q1'):('2023', 'Q2')].head(8))
print()

# Cross-section (xs) - select at specific level
print("df_multi.xs('2023', level='year') (cross-section):")
print(df_multi.xs('2023', level='year').head())
print()

print("df_multi.xs('North', level='region') (by region):")
print(df_multi.xs('North', level='region').head())
print()

# Multiple xs
print("df_multi.xs([('2023', 'Q1'), ('2024', 'Q2')], level=('year', 'quarter')):")
print(df_multi.xs([('2023', 'Q1'), ('2024', 'Q2')], level=('year', 'quarter')))
print()

# =============================================================================
# 3. INDEX OPERATIONS
# =============================================================================

print("=" * 60)
print("3. INDEX OPERATIONS")
print("=" * 60)

# Swap levels
print("swaplevel(0, 1):")
swapped = df_multi.swaplevel('year', 'quarter')
print(swapped.head(8))
print()

# Sort index (required for some operations after swap)
print("sort_index():")
sorted_df = swapped.sort_index()
print(sorted_df.head(8))
print()

# Reorder levels
print("reorder_levels(['region', 'year', 'quarter']):")
reordered = df_multi.reorder_levels(['region', 'year', 'quarter'])
print(reordered.head(8))
print()

# Reset index (to columns)
print("reset_index():")
reset = df_multi.reset_index()
print(reset.head())
print(f"Columns: {reset.columns.tolist()}")
print()

# =============================================================================
# 4. GROUPBY WITH MULTIINDEX
# =============================================================================

print("=" * 60)
print("4. GROUPBY WITH MULTIINDEX")
print("=" * 60)

# Group by level
print("groupby(level='year').sum():")
print(df_multi.groupby(level='year').sum())
print()

print("groupby(level=['year', 'quarter']).mean():")
print(df_multi.groupby(level=['year', 'quarter']).mean().head(8))
print()

# Groupby on column with MultiIndex
df_reset = df_multi.reset_index()
print("groupby(['year', 'region']).agg({'sales': ['sum', 'mean']}):")
print(df_reset.groupby(['year', 'region']).agg({'sales': ['sum', 'mean']}).head(8))
print()

# =============================================================================
# 5. PIVOT TABLES & MULTIINDEX
# =============================================================================

print("=" * 60)
print("5. PIVOT TABLES & MULTIINDEX")
print("=" * 60)

# Create data for pivot
sales_data = pd.DataFrame({
    'year': np.random.choice([2022, 2023, 2024], 500),
    'quarter': np.random.choice(['Q1', 'Q2', 'Q3', 'Q4'], 500),
    'region': np.random.choice(['North', 'South', 'East', 'West'], 500),
    'product': np.random.choice(['A', 'B', 'C'], 500),
    'sales': np.random.randint(100, 5000, 500),
    'units': np.random.randint(1, 50, 500)
})

# Pivot table creates MultiIndex columns
pivot = pd.pivot_table(sales_data,
                       values=['sales', 'units'],
                       index=['year', 'quarter'],
                       columns=['region', 'product'],
                       aggfunc={'sales': 'sum', 'units': 'mean'},
                       fill_value=0)

print("Pivot table with MultiIndex columns:")
print(pivot.head())
print(f"\nColumn levels: {pivot.columns.names}")
print(f"Index levels: {pivot.index.names}")
print()

# Stack/unstack
print("stack() - columns to index:")
stacked = pivot.stack(level='product')
print(stacked.head(10))
print()

print("unstack() - index to columns:")
unstacked = stacked.unstack(level='product')
print(unstacked.head())
print()

# =============================================================================
# 6. ADVANCED SLICING
# =============================================================================

print("=" * 60)
print("6. ADVANCED SLICING WITH IndexSlice")
print("=" * 60)

idx = pd.IndexSlice

# Select specific combinations
print("idx['2023', 'Q1', 'North']:")
print(df_multi.loc[idx['2023', 'Q1', 'North'], :])
print()

print("idx['2023', :, 'North'] (all quarters for 2023 North):")
print(df_multi.loc[idx['2023', :, 'North'], :].head(8))
print()

print("idx[:, 'Q1', :] (Q1 across all years/regions):")
print(df_multi.loc[idx[:, 'Q1', :], :].head(8))
print()

print("idx['2023':'2024', 'Q1':'Q2', ['North', 'South']] (complex slice):")
print(df_multi.loc[idx['2023':'2024', 'Q1':'Q2', ['North', 'South']], :].head(12))
print()

# Column selection with IndexSlice
print("idx[:, ['sales', 'profit']] (select columns):")
print(df_multi.loc[idx[:, :], idx[:, ['sales', 'profit']]].head(8))
print()

# =============================================================================
# 7. MULTIINDEX IN AGGREGATIONS
# =============================================================================

print("=" * 60)
print("7. MULTIINDEX IN AGGREGATIONS")
print("=" * 60)

# Named aggregation creates MultiIndex columns
result = sales_data.groupby(['year', 'quarter']).agg(
    total_sales=('sales', 'sum'),
    avg_sales=('sales', 'mean'),
    total_units=('units', 'sum'),
    avg_units=('units', 'mean'),
    transaction_count=('sales', 'count')
).round(2)

print("Named aggregation with MultiIndex columns:")
print(result)
print(f"\nColumns: {result.columns.tolist()}")
print()

# Flatten MultiIndex columns
result_flat = result.copy()
result_flat.columns = [f"{col[0]}_{col[1]}" for col in result_flat.columns]
print("Flattened columns:")
print(result_flat.head())
print()

# =============================================================================
# 8. PERFORMANCE CONSIDERATIONS
# =============================================================================

print("=" * 60)
print("8. PERFORMANCE CONSIDERATIONS")
print("=" * 60)

import time

# Large MultiIndex DataFrame
n = 100000
large_idx = pd.MultiIndex.from_product([
    range(100),  # 100 groups
    range(10),   # 10 subgroups
    range(100)   # 100 items each
], names=['group', 'subgroup', 'item'])

large_df = pd.DataFrame({
    'value': np.random.randn(n),
    'category': np.random.choice(['A', 'B', 'C'], n)
}, index=large_idx[:n])

print(f"Large MultiIndex DataFrame: {large_df.shape}")

# Time indexing operations
start = time.time()
result1 = large_df.loc[0]  # First level
time1 = time.time() - start

start = time.time()
result2 = large_df.xs(0, level='group')  # Cross-section
time2 = time.time() - start

start = time.time()
result3 = large_df.loc[idx[0, :, 50], :]  # IndexSlice
time3 = time.time() - start

print(f"loc[0]: {time1:.4f}s")
print(f"xs(0, level='group'): {time2:.4f}s")
print(f"IndexSlice[0, :, 50]: {time3:.4f}s")
print()

# Sorting matters!
unsorted = large_df.sample(frac=1)  # Shuffle
start = time.time()
unsorted.loc[0]
time_unsorted = time.time() - start

sorted_df = large_df.sort_index()
start = time.time()
sorted_df.loc[0]
time_sorted = time.time() - start

print(f"Unsorted loc[0]: {time_unsorted:.4f}s")
print(f"Sorted loc[0]: {time_sorted:.4f}s")
print(f"Sorting speedup: {time_unsorted/time_sorted:.1f}x")
print()

# Memory
print(f"MultiIndex memory: {large_df.index.memory_usage(deep=True) / 1024:.1f} KB")
print(f"DataFrame memory: {large_df.memory_usage(deep=True).sum() / 1024:.1f} KB")

print("\n" + "=" * 60)
print("END OF MULTIINDEX")
print("=" * 60)