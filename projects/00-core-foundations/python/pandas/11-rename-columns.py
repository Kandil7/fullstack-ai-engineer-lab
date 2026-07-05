"""
Renaming Columns
W3Schools: https://www.w3schools.com/python/pandas_dataframe_rename.asp

Learn to rename DataFrame columns using rename(), direct assignment,
and other techniques.
"""
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

df = pd.DataFrame({
    "First Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Last Name": ["Smith", "Jones", "Brown", "Wilson"],
    "Age In Years": [25, 30, 35, 28],
    "Annual Salary ($)": [70000, 80000, 95000, 75000],
    "Department Name": ["Engineering", "Marketing", "Engineering", "Sales"],
})

print("Original DataFrame:")
print(df)
print(f"Columns: {list(df.columns)}")
print()

# ---------------------------------------------------------------------------
# Example 1: Rename columns with rename()
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: rename() with a Dictionary")
print("=" * 60)

df_renamed = df.rename(columns={
    "First Name": "first_name",
    "Last Name": "last_name",
    "Age In Years": "age",
    "Annual Salary ($)": "salary",
    "Department Name": "department",
})
print("Renamed columns:")
print(df_renamed)
print(f"Columns: {list(df_renamed.columns)}")
print()

# ---------------------------------------------------------------------------
# Example 2: Rename with a function
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: Rename with a Lambda Function")
print("=" * 60)

# Convert all column names to lowercase and replace spaces with underscores
df_clean = df.rename(columns=lambda c: c.lower().replace(" ", "_").replace("($)", "").strip("_"))
print("Cleaned column names:")
print(df_clean.head(2))
print(f"Columns: {list(df_clean.columns)}")
print()

# ---------------------------------------------------------------------------
# Example 3: Direct column assignment
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: Direct Column Rename via Assignment")
print("=" * 60)

df_direct = df.copy()
df_direct.columns = [
    "first_name",
    "last_name",
    "age",
    "salary",
    "department",
]
print("Directly assigned column names:")
print(df_direct.head(2))
print(f"Columns: {list(df_direct.columns)}")
print()

# ---------------------------------------------------------------------------
# Example 4: Adding prefixes and suffixes
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: add_prefix() and add_suffix()")
print("=" * 60)

df_small = df[["Age In Years", "Annual Salary ($)"]].copy()

# Add prefix
df_prefixed = df_small.add_prefix("emp_")
print("With prefix 'emp_':")
print(df_prefixed.head(2))
print()

# Add suffix
df_suffixed = df_small.add_suffix("_2024")
print("With suffix '_2024':")
print(df_suffixed.head(2))
print()

# ---------------------------------------------------------------------------
# Example 5: Using set_axis() and str methods
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 5: More Column Transformation Techniques")
print("=" * 60)

# Using str accessor to transform column names
df_transformed = df.copy()
df_transformed.columns = df_transformed.columns.str.lower()
df_transformed.columns = df_transformed.columns.str.replace(" ", "_")
df_transformed.columns = df_transformed.columns.str.replace("($)", "", regex=False)
df_transformed.columns = df_transformed.columns.str.strip("_")

print("Transformed columns:")
print(df_transformed.head(2))
print(f"Columns: {list(df_transformed.columns)}")
print()

# Using set_axis with a list
df_set = df.copy()
df_set = df_set.set_axis(
    ["fname", "lname", "age", "salary", "dept"],
    axis=1
)
print("Using set_axis():")
print(df_set.head(2))
print()

print("Done!")
