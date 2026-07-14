"""
Pandas Getting Started
W3Schools: https://www.w3schools.com/python/pandas_getting_started.asp

First steps with Pandas: creating Series and DataFrames from various sources.
"""
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Example 1: Creating a Series from a list
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: Creating a Series")
print("=" * 60)

temperatures = [72.5, 68.0, 75.3, 71.8, 69.2]
temp_series = pd.Series(temperatures)
print("Temperature Series:")
print(temp_series)
print()

# With labels
days = pd.Series(
    [72.5, 68.0, 75.3, 71.8, 69.2],
    index=["Mon", "Tue", "Wed", "Thu", "Fri"],
    name="Temp (°F)"
)
print("Labeled Series:")
print(days)
print()
print(f"Wednesday temperature: {days['Wed']}")
print()

# ---------------------------------------------------------------------------
# Example 2: Creating a DataFrame from a dictionary
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: DataFrame from Dictionary")
print("=" * 60)

employees = {
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Department": ["Engineering", "Marketing", "Engineering", "Sales"],
    "Salary": [95000, 72000, 102000, 68000],
    "Years": [5, 3, 8, 2],
}
df = pd.DataFrame(employees)
print(df)
print()

# ---------------------------------------------------------------------------
# Example 3: Creating a DataFrame from a list of lists
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: DataFrame from List of Lists")
print("=" * 60)

rows = [
    ["Apple", "Fruit", 1.20],
    ["Carrot", "Vegetable", 0.80],
    ["Bread", "Grain", 2.50],
    ["Milk", "Dairy", 3.00],
    ["Chicken", "Protein", 5.99],
]
shopping = pd.DataFrame(
    rows,
    columns=["Item", "Category", "Price"]
)
print(shopping)
print()

# ---------------------------------------------------------------------------
# Example 4: Creating a DataFrame from a NumPy array
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: DataFrame from NumPy Array")
print("=" * 60)

np.random.seed(42)
data = np.random.randint(1, 100, size=(5, 4))
df_rand = pd.DataFrame(
    data,
    columns=["A", "B", "C", "D"],
    index=["row1", "row2", "row3", "row4", "row5"]
)
print("Random DataFrame:")
print(df_rand)
print()

# ---------------------------------------------------------------------------
# Example 5: Quick inspection methods
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 5: Inspecting Your DataFrame")
print("=" * 60)

print("Shape:", df.shape)         # (rows, cols)
print("Columns:", list(df.columns))
print("Index:", list(df.index))
print()

print("First 2 rows (head):")
print(df.head(2))
print()

print("Info:")
df.info()
print()

print("Describe (numeric stats):")
print(df.describe())
print()

print("Value counts for Department:")
print(df["Department"].value_counts())
print()

# ---------------------------------------------------------------------------
# Example 6: Saving and loading
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 6: Save to CSV and Read Back")
print("=" * 60)

import os
import tempfile

csv_path = os.path.join(tempfile.gettempdir(), "pandas_ex02_demo.csv")

df.to_csv(csv_path, index=False)
print(f"Saved DataFrame to: {csv_path}")

df_loaded = pd.read_csv(csv_path)
print("Loaded back:")
print(df_loaded)
print()

# Clean up
os.remove(csv_path)
print("Temp file removed.")
print()
print("Done!")
