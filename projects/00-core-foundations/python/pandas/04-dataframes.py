"""
Pandas DataFrames
W3Schools: https://www.w3schools.com/python/pandas_dataframes.asp

A DataFrame is a 2-dimensional labeled data structure with columns of
potentially different types. Think of it as a spreadsheet, SQL table,
or a dict of Series objects.
"""
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Example 1: Creating a DataFrame
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: Creating a DataFrame")
print("=" * 60)

# From a dictionary of lists
data = {
    "Name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "Age": [25, 30, 35, 28, 22],
    "City": ["New York", "London", "Paris", "Tokyo", "Sydney"],
    "Salary": [70000, 80000, 95000, 75000, 65000],
}
df = pd.DataFrame(data)
print("Employee DataFrame:")
print(df)
print()

# ---------------------------------------------------------------------------
# Example 2: Accessing columns
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: Accessing Columns")
print("=" * 60)

# Single column – returns a Series
print("Name column:")
print(df["Name"])
print(f"Type: {type(df['Name']).__name__}")
print()

# Multiple columns – returns a DataFrame
print("Name and Salary:")
print(df[["Name", "Salary"]])
print()

# Dot notation (works when column name is a valid Python identifier)
print("Age via dot notation:")
print(df.Age)
print()

# ---------------------------------------------------------------------------
# Example 3: Adding and removing columns
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: Adding and Removing Columns")
print("=" * 60)

# Add a new column
df["Bonus"] = df["Salary"] * 0.10
print("DataFrame with Bonus column:")
print(df)
print()

# Add column from computation
df["Age_Group"] = df["Age"].apply(lambda a: "Senior" if a >= 30 else "Junior")
print("DataFrame with Age_Group:")
print(df[["Name", "Age", "Age_Group"]])
print()

# Remove a column
df_dropped = df.drop(columns=["Bonus", "Age_Group"])
print("After dropping Bonus and Age_Group:")
print(df_dropped)
print()

# ---------------------------------------------------------------------------
# Example 4: DataFrame from list of dictionaries
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: From List of Dictionaries")
print("=" * 60)

books = [
    {"title": "1984", "author": "Orwell", "year": 1949, "rating": 4.7},
    {"title": "Dune", "author": "Herbert", "year": 1965, "rating": 4.5},
    {"title": "Neuromancer", "author": "Gibson", "year": 1984, "rating": 4.2},
    {"title": "Foundation", "author": "Asimov", "year": 1951, "rating": 4.6},
]
books_df = pd.DataFrame(books)
print("Sci-Fi Books:")
print(books_df)
print()

# ---------------------------------------------------------------------------
# Example 5: DataFrame inspection
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 5: DataFrame Inspection")
print("=" * 60)

# Create a bigger DataFrame
np.random.seed(0)
big_df = pd.DataFrame({
    "id": range(1, 101),
    "value": np.random.randn(100).round(2),
    "category": np.random.choice(["A", "B", "C"], 100),
})

print(f"Shape: {big_df.shape}")
print(f"Size: {big_df.size}")
print(f"Columns: {list(big_df.columns)}")
print(f"Dtypes:\n{big_df.dtypes}")
print()

print("Head (3):")
print(big_df.head(3))
print()

print("Tail (3):")
print(big_df.tail(3))
print()

print("Describe:")
print(big_df.describe())
print()

print("Category counts:")
print(big_df["category"].value_counts())
print()

print("Done!")
