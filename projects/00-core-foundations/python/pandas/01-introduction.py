"""
Pandas Introduction
W3Schools: https://www.w3schools.com/python/pandas_intro.asp

Pandas is a Python library used for working with data sets.
It has functions for analyzing, cleaning, exploring, and manipulating data.
"""
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Example 1: What is Pandas?
# Pandas is short for "Panel Data" and is a powerful open-source Python library
# used for data manipulation and analysis.
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: What is Pandas?")
print("=" * 60)

# Series – a one-dimensional labeled array
mylist = [1, 2, 3, 4, 5]
myseries = pd.Series(mylist)
print("Series from list:")
print(myseries)
print()

# DataFrame – a two-dimensional labeled data structure
mydict = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "London", "Paris"],
}
mydf = pd.DataFrame(mydict)
print("DataFrame from dict:")
print(mydf)
print()

# ---------------------------------------------------------------------------
# Example 2: Pandas Series
# A Pandas Series is like a column in a table. It is a one-dimensional array
# holding data of any type.
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: Pandas Series")
print("=" * 60)

# Simple Series
s = pd.Series([10, 20, 30, 40, 50])
print("Simple Series:")
print(s)
print()

# Series with custom index
s_named = pd.Series(
    [100, 200, 300],
    index=["a", "b", "c"],
    name="Values"
)
print("Series with custom index:")
print(s_named)
print()

# Access elements
print("Access by label: s_named['b'] =", s_named["b"])
print("Access by position: s_named.iloc[0] =", s_named.iloc[0])
print()

# ---------------------------------------------------------------------------
# Example 3: Pandas DataFrame
# A Pandas DataFrame is like a spreadsheet or SQL table – a 2D labeled data
# structure with columns of potentially different types.
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: Pandas DataFrame")
print("=" * 60)

data = {
    "Product": ["Laptop", "Phone", "Tablet", "Monitor"],
    "Price": [999, 699, 449, 299],
    "Quantity": [10, 25, 40, 15],
    "In_Stock": [True, False, True, True],
}
df = pd.DataFrame(data)

print("Full DataFrame:")
print(df)
print()

print("Column 'Product':")
print(df["Product"])
print()

print("DataFrame shape:", df.shape)
print("DataFrame dtypes:")
print(df.dtypes)
print()

# ---------------------------------------------------------------------------
# Example 4: Pandas vs Other Tools
# Why Pandas?
#   - Handles missing data (NaN)
#   - Automatic data alignment by labels
#   - Powerful groupby operations
#   - Built-in visualization
#   - Easy to read/write many file formats (CSV, JSON, SQL, Excel)
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: Pandas Key Capabilities")
print("=" * 60)

# Missing data handling
df_with_nan = pd.DataFrame({
    "A": [1, 2, np.nan, 4],
    "B": [np.nan, 2, 3, 4],
})
print("DataFrame with NaN:")
print(df_with_nan)
print()

print("Drop rows with NaN:")
print(df_with_nan.dropna())
print()

print("Fill NaN with 0:")
print(df_with_nan.fillna(0))
print()

# Data alignment
s1 = pd.Series([1, 2, 3], index=["a", "b", "c"])
s2 = pd.Series([10, 20, 30], index=["b", "c", "d"])
print("Automatic alignment (s1 + s2):")
print(s1 + s2)  # aligned by index; missing values become NaN
print()

# ---------------------------------------------------------------------------
# Example 5: Getting Started – Install and Import
# To use Pandas you need to install it:
#   pip install pandas
# Then import it (commonly aliased as pd):
#   import pandas as pd
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 5: Quick Start – Version Check")
print("=" * 60)

print(f"Pandas version: {pd.__version__}")
print(f"NumPy version: {np.__version__}")
print()

# A quick "hello world" with Pandas
hello = pd.DataFrame({
    "greeting": ["Hello", "Bonjour", "Hola", "Ciao"],
    "language": ["English", "French", "Spanish", "Italian"],
})
print(hello)
print()
print("Done! You are ready to learn Pandas.")
