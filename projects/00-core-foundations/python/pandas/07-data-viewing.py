"""
Viewing Data
W3Schools: https://www.w3schools.com/python/pandas_viewing_data.asp

Pandas provides many methods to inspect and view your data quickly.
"""
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Create sample DataFrame
# ---------------------------------------------------------------------------

np.random.seed(42)
df = pd.DataFrame({
    "Name": [
        "Alice", "Bob", "Charlie", "Diana", "Eve",
        "Frank", "Grace", "Heidi", "Ivan", "Judy",
    ],
    "Department": [
        "Engineering", "Marketing", "Engineering", "Sales", "Engineering",
        "Marketing", "Sales", "Engineering", "Marketing", "Sales",
    ],
    "Age": [25, 30, 35, 28, 22, 40, 33, 29, 45, 31],
    "Salary": [
        70000, 80000, 95000, 75000, 65000,
        88000, 72000, 91000, 85000, 68000,
    ],
    "Performance": np.random.randint(60, 100, 10),
})

print("Full DataFrame:")
print(df)
print()

# ---------------------------------------------------------------------------
# Example 1: head() and tail()
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: head() and tail()")
print("=" * 60)

print("head(3) – first 3 rows:")
print(df.head(3))
print()

print("tail(3) – last 3 rows:")
print(df.tail(3))
print()

# ---------------------------------------------------------------------------
# Example 2: info() and describe()
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: info() and describe()")
print("=" * 60)

print("DataFrame Info:")
df.info()
print()

print("Numeric Statistics:")
print(df.describe())
print()

print("All Columns Statistics (including non-numeric):")
print(df.describe(include="all"))
print()

# ---------------------------------------------------------------------------
# Example 3: Shape, columns, and dtypes
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: Shape, Columns, Dtypes")
print("=" * 60)

print(f"Shape (rows, cols): {df.shape}")
print(f"Number of rows: {len(df)}")
print(f"Number of columns: {df.shape[1]}")
print(f"Column names: {list(df.columns)}")
print(f"Data types:\n{df.dtypes}")
print()

# ---------------------------------------------------------------------------
# Example 4: select_dtypes
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: Selecting by Data Type")
print("=" * 60)

print("Numeric columns only:")
numeric_df = df.select_dtypes(include=[np.number])
print(numeric_df.head())
print()

print("Object (string) columns only:")
str_df = df.select_dtypes(include=["object"])
print(str_df.head())
print()

# ---------------------------------------------------------------------------
# Example 5: nunique, value_counts, sample
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 5: Unique Values and Sampling")
print("=" * 60)

print(f"Unique departments: {df['Department'].nunique()}")
print(f"Department value counts:")
print(df["Department"].value_counts())
print()

print("Random sample of 3 rows:")
print(df.sample(3, random_state=1))
print()

print("Unique ages sorted:")
print(sorted(df["Age"].unique()))
print()

print("Done!")
