"""
Selecting Data
W3Schools: https://www.w3schools.com/python/pandas_dataframe_loc.asp

Learn to select specific rows and columns from a DataFrame.
"""
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "Department": ["Engineering", "Marketing", "Engineering", "Sales", "Marketing"],
    "Age": [25, 30, 35, 28, 22],
    "Salary": [70000, 80000, 95000, 75000, 65000],
    "Rating": [4.5, 3.8, 4.9, 4.2, 3.5],
}, index=["emp1", "emp2", "emp3", "emp4", "emp5"])

print("Original DataFrame:")
print(df)
print()

# ---------------------------------------------------------------------------
# Example 1: Selecting columns
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: Selecting Columns")
print("=" * 60)

# Single column -> Series
print("Single column (Salary):")
print(df["Salary"])
print(f"Type: {type(df['Salary']).__name__}")
print()

# Multiple columns -> DataFrame
print("Multiple columns:")
print(df[["Name", "Salary"]])
print()

# ---------------------------------------------------------------------------
# Example 2: Selecting rows with [] slicing
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: Row Slicing with []")
print("=" * 60)

# Slice by position (like Python list slicing)
print("First 3 rows:")
print(df[:3])
print()

print("Last 2 rows:")
print(df[-2:])
print()

# ---------------------------------------------------------------------------
# Example 3: loc[] – label-based selection
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: loc[] – Label-Based Selection")
print("=" * 60)

# Single row by label
print("Row 'emp2':")
print(df.loc["emp2"])
print()

# Multiple rows
print("Rows 'emp1' to 'emp3':")
print(df.loc["emp1":"emp3"])
print()

# Row and column
print("Salary of emp4:", df.loc["emp4", "Salary"])
print()

# Multiple rows and columns
print("Name and Rating for emp1, emp3, emp5:")
print(df.loc[["emp1", "emp3", "emp5"], ["Name", "Rating"]])
print()

# Conditional selection with loc
print("Employees with Salary > 70000:")
print(df.loc[df["Salary"] > 70000])
print()

# ---------------------------------------------------------------------------
# Example 4: iloc[] – integer position-based selection
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: iloc[] – Position-Based Selection")
print("=" * 60)

# Single row by position
print("Row at index 2:")
print(df.iloc[2])
print()

# Multiple rows
print("Rows 0 and 1:")
print(df.iloc[[0, 1]])
print()

# Row and column by position
print("Element at row 1, column 3:", df.iloc[1, 3])
print()

# Slice rows and columns
print("Rows 1:4, Columns 0:2:")
print(df.iloc[1:4, 0:2])
print()

# ---------------------------------------------------------------------------
# Example 5: Boolean indexing
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 5: Boolean Indexing")
print("=" * 60)

# Single condition
mask = df["Department"] == "Engineering"
print("Engineering employees:")
print(df[mask])
print()

# Multiple conditions (AND)
mask2 = (df["Department"] == "Marketing") & (df["Age"] < 28)
print("Marketing employees under 28:")
print(df[mask2])
print()

# Multiple conditions (OR)
mask3 = (df["Rating"] >= 4.5) | (df["Salary"] > 90000)
print("Rating >= 4.5 OR Salary > 90k:")
print(df[mask3])
print()

# isin()
print("Engineering or Sales:")
print(df[df["Department"].isin(["Engineering", "Sales"])])
print()

print("Done!")
