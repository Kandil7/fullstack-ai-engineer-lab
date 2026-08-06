"""
Adding a New Column
W3Schools: https://www.w3schools.com/python/pandas_dataframe_add_column.asp

There are several ways to add a new column to a DataFrame.
"""
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

df = pd.DataFrame({
    "Product": ["Laptop", "Phone", "Tablet", "Monitor", "Keyboard"],
    "Price": [999.99, 699.99, 449.99, 299.99, 129.99],
    "Quantity": [10, 25, 40, 15, 50],
    "Category": ["Electronics", "Electronics", "Electronics", "Peripherals", "Peripherals"],
})

print("Original DataFrame:")
print(df)
print()

# ---------------------------------------------------------------------------
# Example 1: Simple column assignment
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: Simple Assignment")
print("=" * 60)

# Add a column with a constant value
df["In_Stock"] = True
print("Added 'In_Stock' column:")
print(df)
print()

# ---------------------------------------------------------------------------
# Example 2: Column from computation
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: Column from Computation")
print("=" * 60)

df["Revenue"] = df["Price"] * df["Quantity"]
df["Tax"] = (df["Revenue"] * 0.08).round(2)
df["Total"] = (df["Revenue"] + df["Tax"]).round(2)
print("Added computed columns:")
print(df[["Product", "Revenue", "Tax", "Total"]])
print()

# ---------------------------------------------------------------------------
# Example 3: Column using apply()
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: Column using apply()")
print("=" * 60)

def price_tier(price):
    """Assign a tier based on price."""
    if price >= 800:
        return "Premium"
    elif price >= 400:
        return "Mid-Range"
    else:
        return "Budget"

df["Tier"] = df["Price"].apply(price_tier)
print("Added 'Tier' column via apply():")
print(df[["Product", "Price", "Tier"]])
print()

# ---------------------------------------------------------------------------
# Example 4: Column with np.where()
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: np.where() for Conditional Column")
print("=" * 60)

df["Volume_Label"] = np.where(
    df["Quantity"] >= 30,
    "High",
    np.where(df["Quantity"] >= 20, "Medium", "Low")
)
print("Volume labels:")
print(df[["Product", "Quantity", "Volume_Label"]])
print()

# ---------------------------------------------------------------------------
# Example 5: insert() – add column at specific position
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 5: insert() at Specific Position")
print("=" * 60)

# Insert at position 1 (second column)
df.insert(1, "SKU", ["LP-001", "PH-002", "TB-003", "MN-004", "KB-005"])
print("Inserted 'SKU' at position 1:")
print(df[["Product", "SKU", "Price"]])
print()

# ---------------------------------------------------------------------------
# Example 6: Assign() method (chainable)
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 6: assign() Method (Chainable)")
print("=" * 60)

df_assigned = (
    df[["Product", "Price", "Quantity"]]
    .assign(
        Discount=lambda x: x["Price"] * 0.10,
        Final_Price=lambda x: x["Price"] * 0.90,
    )
)
print("Using assign() (chainable, non-mutating):")
print(df_assigned)
print()

print("Done!")
