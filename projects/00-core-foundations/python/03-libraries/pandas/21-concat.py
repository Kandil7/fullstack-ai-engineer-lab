"""
Concatenating DataFrames
W3Schools: https://www.w3schools.com/python/pandas_dataframe_concat.asp

concat() stacks DataFrames vertically (rows) or horizontally (columns).
Unlike merge(), it doesn't require common columns.
"""
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

df1 = pd.DataFrame({
    "Name": ["Alice", "Bob"],
    "Score": [85, 92],
    "Grade": ["A", "A+"],
})

df2 = pd.DataFrame({
    "Name": ["Charlie", "Diana"],
    "Score": [78, 88],
    "Grade": ["B+", "A-"],
})

df3 = pd.DataFrame({
    "Name": ["Eve", "Frank"],
    "Score": [95, 70],
    "Grade": ["A+", "B"],
})

print("df1:")
print(df1)
print()

print("df2:")
print(df2)
print()

print("df3:")
print(df3)
print()

# ---------------------------------------------------------------------------
# Example 1: Vertical concatenation (default axis=0)
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: Vertical Concatenation (axis=0)")
print("=" * 60)

vertical = pd.concat([df1, df2, df3], ignore_index=True)
print("Stacked vertically:")
print(vertical)
print()

# ---------------------------------------------------------------------------
# Example 2: Horizontal concatenation (axis=1)
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: Horizontal Concatenation (axis=1)")
print("=" * 60)

df_left = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Score": [85, 92, 78],
})

df_right = pd.DataFrame({
    "Grade": ["A", "A+", "B+"],
    "Passed": [True, True, False],
})

horizontal = pd.concat([df_left, df_right], axis=1)
print("Stacked horizontally:")
print(horizontal)
print()

# ---------------------------------------------------------------------------
# Example 3: Concat with different columns (outer join)
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: Concat with Different Columns")
print("=" * 60)

df_a = pd.DataFrame({
    "Name": ["Alice", "Bob"],
    "Score": [85, 92],
})

df_b = pd.DataFrame({
    "Name": ["Charlie", "Diana"],
    "Grade": ["B+", "A-"],
    "Bonus": [5, 10],
})

outer_concat = pd.concat([df_a, df_b], ignore_index=True)
print("Outer concat (union of columns):")
print(outer_concat)
print()

# Inner concat (only common columns)
inner_concat = pd.concat([df_a, df_b], ignore_index=True, join="inner")
print("Inner concat (intersection of columns):")
print(inner_concat)
print()

# ---------------------------------------------------------------------------
# Example 4: Concat with keys (hierarchical index)
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: Concat with Keys")
print("=" * 60)

keyed = pd.concat(
    [df1, df2, df3],
    keys=["Group1", "Group2", "Group3"],
    ignore_index=False,
)
print("With hierarchical keys:")
print(keyed)
print()

# Reset to flat index
print("Reset index:")
print(keyed.reset_index())
print()

# ---------------------------------------------------------------------------
# Example 5: Practical example – combining monthly data
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 5: Combining Monthly Sales Data")
print("=" * 60)

monthly_data = []
for month in range(1, 4):
    temp = pd.DataFrame({
        "Month": [f"2024-{month:02d}"] * 5,
        "Product": ["A", "B", "C", "D", "E"],
        "Sales": np.random.randint(100, 500, 5),
    })
    monthly_data.append(temp)

quarterly = pd.concat(monthly_data, ignore_index=True)
print("Quarterly sales data:")
print(quarterly)
print()

# Aggregate by product
summary = quarterly.groupby("Product")["Sales"].sum().reset_index()
summary.columns = ["Product", "Total_Sales"]
print("Total sales by product:")
print(summary)
print()

# Pivot table
pivot = quarterly.pivot_table(values="Sales", index="Product", columns="Month", aggfunc="sum")
print("Pivot table:")
print(pivot)
print()

print("Done!")
