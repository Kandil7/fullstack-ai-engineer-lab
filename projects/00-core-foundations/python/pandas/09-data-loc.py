"""
Data Selection with loc[]
W3Schools: https://www.w3schools.com/python/pandas_dataframe_loc.asp

loc[] is label-based data selection. Unlike iloc[], which uses integer
positions, loc[] uses the index labels.
"""
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Sample data with named index
# ---------------------------------------------------------------------------

df = pd.DataFrame({
    "Product": ["Laptop", "Phone", "Tablet", "Monitor", "Keyboard"],
    "Price": [999, 699, 449, 299, 129],
    "Quantity": [10, 25, 40, 15, 50],
    "Category": ["Electronics", "Electronics", "Electronics", "Peripherals", "Peripherals"],
}, index=["P001", "P002", "P003", "P004", "P005"])

print("Product DataFrame:")
print(df)
print()

# ---------------------------------------------------------------------------
# Example 1: Basic loc[] access
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: Basic loc[] Access")
print("=" * 60)

# Single row by label
print("Row P002:")
print(df.loc["P002"])
print(f"Type: {type(df.loc['P002']).__name__}")
print()

# Single value
print("Price of P003:", df.loc["P003", "Price"])
print()

# ---------------------------------------------------------------------------
# Example 2: Selecting rows and columns
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: Rows and Columns with loc[]")
print("=" * 60)

# Multiple rows, all columns
print("Rows P001, P003, P005:")
print(df.loc[["P001", "P003", "P005"]])
print()

# Multiple rows, specific columns
print("Product and Price for P001-P003:")
print(df.loc["P001":"P003", ["Product", "Price"]])
print()

# All rows, specific column
print("All Categories:")
print(df.loc[:, "Category"])
print()

# ---------------------------------------------------------------------------
# Example 3: Conditional selection with loc[]
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: Conditional Selection")
print("=" * 60)

# Boolean mask
mask = df["Price"] > 500
print("Products costing more than $500:")
print(df.loc[mask])
print()

# Multiple conditions
mask2 = (df["Category"] == "Electronics") & (df["Quantity"] >= 25)
print("Electronics with Quantity >= 25:")
print(df.loc[mask2])
print()

# Assigning values with loc
df_copy = df.copy()
df_copy.loc[df_copy["Price"] > 500, "Expensive"] = True
df_copy.loc[df_copy["Price"] <= 500, "Expensive"] = False
print("DataFrame with Expensive flag:")
print(df_copy)
print()

# ---------------------------------------------------------------------------
# Example 4: Setting values with loc[]
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: Setting Values with loc[]")
print("=" * 60)

df_mod = df.copy()

# Set a single value
df_mod.loc["P001", "Price"] = 899
print("Changed P001 price to 899:")
print(df_mod.loc["P001"])
print()

# Set multiple values
df_mod.loc["P003":"P005", "Quantity"] = 0
print("Zeroed out quantities for P003-P005:")
print(df_mod[["Product", "Quantity"]])
print()

# ---------------------------------------------------------------------------
# Example 5: loc[] with datetime index
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 5: loc[] with Datetime Index")
print("=" * 60)

dates = pd.date_range("2024-01-01", periods=7, freq="D")
ts_df = pd.DataFrame({
    "Temperature": [32, 35, 28, 30, 38, 40, 36],
    "Humidity": [65, 70, 80, 75, 60, 55, 62],
}, index=dates)

print("Daily Weather:")
print(ts_df)
print()

# Select by date range
print("Jan 3 to Jan 5:")
print(ts_df.loc["2024-01-03":"2024-01-05"])
print()

# Select by partial string
print("Jan 1 entries:")
print(ts_df.loc["2024-01"])
print()

print("Done!")
