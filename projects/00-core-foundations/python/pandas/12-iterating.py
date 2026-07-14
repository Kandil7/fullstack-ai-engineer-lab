"""
Iterating over a DataFrame
W3Schools: https://www.w3schools.com/python/pandas_dataframe_iterrows.asp

Pandas provides several ways to iterate over a DataFrame. While vectorized
operations are preferred, iteration is sometimes necessary.
"""
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

df = pd.DataFrame({
    "Product": ["Laptop", "Phone", "Tablet", "Monitor", "Keyboard"],
    "Price": [999, 699, 449, 299, 129],
    "Quantity": [10, 25, 40, 15, 50],
})

print("Original DataFrame:")
print(df)
print()

# ---------------------------------------------------------------------------
# Example 1: iterrows() – iterate over rows
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: iterrows()")
print("=" * 60)

print("Iterating with iterrows():")
for index, row in df.iterrows():
    total = row["Price"] * row["Quantity"]
    print(f"  {row['Product']:12s} – Total Value: ${total:>8,}")
print()

# ---------------------------------------------------------------------------
# Example 2: itertuples() – faster than iterrows()
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: itertuples() (faster)")
print("=" * 60)

print("Iterating with itertuples():")
for row in df.itertuples(index=False):
    total = row.Price * row.Quantity
    print(f"  {row.Product:12s} – ${total:>8,}")
print()

# Access by attribute (not dict-like)
print("First row via itertuples:")
first = next(df.itertuples(index=False))
print(f"  Product: {first.Product}, Price: ${first.Price}")
print()

# ---------------------------------------------------------------------------
# Example 3: iteritems() – iterate over columns (deprecated in favor of items())
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: items() – iterate over columns")
print("=" * 60)

print("Column names and their sums:")
for col_name, col_data in df.items():
    if col_data.dtype in [np.int64, np.float64]:
        print(f"  {col_name}: sum={col_data.sum()}, mean={col_data.mean():.1f}")
    else:
        print(f"  {col_name}: {len(col_data)} values")
print()

# ---------------------------------------------------------------------------
# Example 4: Apply a function row-wise
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: apply() – Row-wise Function")
print("=" * 60)

def categorize_price(row):
    """Categorize product by price."""
    if row["Price"] >= 800:
        return "Premium"
    elif row["Price"] >= 400:
        return "Mid-range"
    else:
        return "Budget"

df["Category"] = df.apply(categorize_price, axis=1)
print("DataFrame with categories:")
print(df)
print()

# ---------------------------------------------------------------------------
# Example 5: Vectorized operations (preferred over iteration)
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 5: Vectorized Operations (Preferred)")
print("=" * 60)

# Instead of iterating, use vectorized operations
df["Revenue"] = df["Price"] * df["Quantity"]
df["Tax"] = df["Revenue"] * 0.08
df["Total"] = df["Revenue"] + df["Tax"]

print("DataFrame with computed columns (vectorized):")
print(df)
print()

# np.vectorize for custom functions
def format_currency(val):
    """Format a number as currency string."""
    return f"${val:,.2f}"

# Apply formatting (for display only)
print("Formatted Revenue:")
for val in df["Revenue"]:
    print(f"  {format_currency(val)}")
print()

print("Done!")
