"""
Dropping Data
W3Schools: https://www.w3schools.com/python/pandas_dataframe_drop.asp

The drop() method removes specified rows or columns from a DataFrame.
"""
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "Age": [25, 30, 35, 28, 22],
    "Department": ["Engineering", "Marketing", "Engineering", "Sales", "Marketing"],
    "Salary": [70000, 80000, 95000, 75000, 65000],
    "Temp_Col1": [1, 2, 3, 4, 5],
    "Temp_Col2": [10, 20, 30, 40, 50],
}, index=["e1", "e2", "e3", "e4", "e5"])

print("Original DataFrame:")
print(df)
print()

# ---------------------------------------------------------------------------
# Example 1: Drop columns
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: Drop Columns")
print("=" * 60)

# Drop a single column
df1 = df.drop(columns=["Temp_Col1"])
print("Dropped Temp_Col1:")
print(df1.head(3))
print()

# Drop multiple columns
df2 = df.drop(columns=["Temp_Col1", "Temp_Col2"])
print("Dropped both temp columns:")
print(df2)
print()

# Using axis parameter
df3 = df.drop("Temp_Col2", axis=1)
print("Using axis=1 to drop Temp_Col2:")
print(df3.head(3))
print()

# ---------------------------------------------------------------------------
# Example 2: Drop rows by label
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: Drop Rows by Label")
print("=" * 60)

# Drop single row
df4 = df.drop("e3")
print("Dropped row e3:")
print(df4)
print()

# Drop multiple rows
df5 = df.drop(["e1", "e5"])
print("Dropped rows e1 and e5:")
print(df5)
print()

# ---------------------------------------------------------------------------
# Example 3: Drop rows by position (with iloc)
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: Drop Rows by Position")
print("=" * 60)

# drop() uses labels, so to drop by position you can use iloc
df6 = df.drop(df.index[[0, 2, 4]])
print("Dropped rows at positions 0, 2, 4:")
print(df6)
print()

# Alternative: keep certain rows
keep_indices = [1, 3]
df7 = df.iloc[keep_indices]
print(f"Kept only rows at positions {keep_indices}:")
print(df7)
print()

# ---------------------------------------------------------------------------
# Example 4: Drop duplicates
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: Drop Duplicates")
print("=" * 60)

df_dup = pd.DataFrame({
    "Name": ["Alice", "Bob", "Alice", "Charlie", "Bob"],
    "Department": ["Engineering", "Marketing", "Engineering", "Sales", "Marketing"],
    "Salary": [70000, 80000, 70000, 95000, 80000],
})
print("DataFrame with duplicates:")
print(df_dup)
print()

# Drop exact duplicates
df_no_dup = df_dup.drop_duplicates()
print("After drop_duplicates():")
print(df_no_dup)
print()

# Drop based on specific columns
df_no_name_dup = df_dup.drop_duplicates(subset=["Name"], keep="first")
print("First occurrence per Name:")
print(df_no_name_dup)
print()

# ---------------------------------------------------------------------------
# Example 5: Drop rows with NaN
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 5: Drop Missing Values")
print("=" * 60)

df_nan = pd.DataFrame({
    "A": [1, 2, np.nan, 4, 5],
    "B": [np.nan, 2, 3, np.nan, 5],
    "C": ["x", "y", "z", "w", "v"],
})
print("DataFrame with NaN:")
print(df_nan)
print()

# Drop rows with any NaN
print("dropna (any):")
print(df_nan.dropna())
print()

# Drop rows where all values are NaN (none qualify here)
print("dropna (how='all'):")
print(df_nan.dropna(how="all"))
print()

# Drop columns with NaN
print("dropna on columns (axis=1):")
print(df_nan.dropna(axis=1))
print()

# Drop based on threshold
print("dropna with thresh=2 (at least 2 non-null):")
print(df_nan.dropna(thresh=2))
print()

print("Done!")
