"""
Loading Data into Pandas
W3Schools: https://www.w3schools.com/python/pandas_csv.asp

Pandas can read data from many formats: CSV, JSON, Excel, SQL, and more.
This script demonstrates loading and saving data.
"""
import pandas as pd
import numpy as np
import os
import tempfile

# We'll use a temp directory for demo files
TMPDIR = tempfile.gettempdir()


def save_demo_csv(path: str) -> None:
    """Create a sample CSV file for demonstration."""
    df = pd.DataFrame({
        "Name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
        "Age": [25, 30, 35, 28, 22],
        "City": ["New York", "London", "Paris", "Tokyo", "Sydney"],
        "Salary": [70000, 80000, 95000, 75000, 65000],
    })
    df.to_csv(path, index=False)
    print(f"Created demo CSV: {path}")
    print()


# ---------------------------------------------------------------------------
# Example 1: Reading a CSV file
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: Read CSV")
print("=" * 60)

csv_path = os.path.join(TMPDIR, "pandas_ex05_data.csv")
save_demo_csv(csv_path)

df = pd.read_csv(csv_path)
print("Loaded DataFrame:")
print(df)
print(f"Shape: {df.shape}")
print()

# ---------------------------------------------------------------------------
# Example 2: CSV options and parameters
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: CSV Reading Options")
print("=" * 60)

# Read with different options
df_limited = pd.read_csv(csv_path, nrows=3)  # Only first 3 rows
print("First 3 rows (nrows=3):")
print(df_limited)
print()

# Read only specific columns
df_cols = pd.read_csv(csv_path, usecols=["Name", "Salary"])
print("Only Name and Salary:")
print(df_cols)
print()

# Set index column
df_idx = pd.read_csv(csv_path, index_col="Name")
print("Indexed by Name:")
print(df_idx)
print()

# ---------------------------------------------------------------------------
# Example 3: Saving data to CSV
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: Save to CSV")
print("=" * 60)

products = pd.DataFrame({
    "Product": ["Widget", "Gadget", "Doohickey"],
    "Price": [9.99, 24.99, 14.99],
    "In Stock": [True, False, True],
})

# Save with default settings
out_path = os.path.join(TMPDIR, "pandas_ex05_products.csv")
products.to_csv(out_path, index=False)
print(f"Saved to: {out_path}")

# Verify by reading back
df_verify = pd.read_csv(out_path)
print("Read back:")
print(df_verify)
print()

# ---------------------------------------------------------------------------
# Example 4: Reading CSV with errors
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: Handling Read Errors")
print("=" * 60)

# Handle missing values
messy_csv = os.path.join(TMPDIR, "pandas_ex05_messy.csv")
pd.DataFrame({
    "A": [1, 2, None, 4],
    "B": ["x", None, "z", "w"],
}).to_csv(messy_csv, index=False)

df_messy = pd.read_csv(messy_csv)
print("CSV with missing values:")
print(df_messy)
print()

print("Fill NaN with defaults:")
print(df_messy.fillna({"A": 0, "B": "unknown"}))
print()

# ---------------------------------------------------------------------------
# Example 5: Other file formats
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 5: Other Formats (JSON, Excel concepts)")
print("=" * 60)

# Save as JSON
json_path = os.path.join(TMPDIR, "pandas_ex05_data.json")
df.to_json(json_path, orient="records", indent=2)
print(f"Saved as JSON: {json_path}")

df_json = pd.read_json(json_path)
print("Loaded from JSON:")
print(df_json)
print()

# Note: For Excel (.xlsx), you would use:
#   df.to_excel("output.xlsx", index=False)
#   df = pd.read_excel("input.xlsx")
# Requires: pip install openpyxl

# Save as Parquet (if pyarrow is installed)
try:
    parquet_path = os.path.join(TMPDIR, "pandas_ex05_data.parquet")
    df.to_parquet(parquet_path, index=False)
    df_pq = pd.read_parquet(parquet_path)
    print("Parquet round-trip successful!")
    print(df_pq.head(2))
    print()
except ImportError:
    print("Parquet requires pyarrow – skipping.")
    print()

# Clean up temp files
for f in [csv_path, out_path, messy_csv, json_path]:
    if os.path.exists(f):
        os.remove(f)
print("Temp files cleaned up.")
print("Done!")
