"""
Pandas Series
W3Schools: https://www.w3schools.com/python/pandas_series.asp

A Pandas Series is a one-dimensional labeled array capable of holding any
data type (integers, strings, floats, Python objects, etc.).
"""
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Example 1: Basic Series creation
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: Basic Series")
print("=" * 60)

# From a list
s1 = pd.Series([10, 20, 30, 40, 50])
print("Series from list:")
print(s1)
print(f"dtype: {s1.dtype}")
print()

# From a NumPy array
arr = np.array([1.5, 2.7, 3.9, 4.1, 5.3])
s2 = pd.Series(arr)
print("Series from NumPy array:")
print(s2)
print()

# ---------------------------------------------------------------------------
# Example 2: Series with custom labels (index)
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: Custom Index Labels")
print("=" * 60)

scores = pd.Series(
    [88, 92, 76, 95, 84],
    index=["Alice", "Bob", "Charlie", "Diana", "Eve"],
    name="Test Scores"
)
print("Student scores:")
print(scores)
print()

# Access by label
print(f"Bob's score: {scores['Bob']}")
print(f"Diana's score: {scores.loc['Diana']}")
print()

# Access by position
print(f"First student's score (iloc[0]): {scores.iloc[0]}")
print()

# Slicing by label (inclusive on both ends)
print("Alice to Charlie:")
print(scores["Alice":"Charlie"])
print()

# Slicing by position (exclusive end)
print("Positions 1 to 3:")
print(scores.iloc[1:4])
print()

# ---------------------------------------------------------------------------
# Example 3: Series operations
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: Series Operations")
print("=" * 60)

temps = pd.Series(
    [72.5, 68.0, 75.3, 71.8, 69.2],
    index=["Mon", "Tue", "Wed", "Thu", "Fri"]
)
print("Weekly temperatures:")
print(temps)
print()

# Scalar operations
temps_celsius = (temps - 32) * 5 / 9
print("Celsius conversion:")
print(temps_celsius.round(2))
print()

# Boolean indexing
hot_days = temps[temps > 70]
print("Days above 70°F:")
print(hot_days)
print()

# Aggregations
print(f"Mean: {temps.mean():.1f}")
print(f"Max: {temps.max()}")
print(f"Min: {temps.min()}")
print(f"Std: {temps.std():.2f}")
print()

# ---------------------------------------------------------------------------
# Example 4: Series from dictionary
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: Series from Dictionary")
print("=" * 60)

population = {
    "Tokyo": 13960000,
    "Delhi": 11030000,
    "Shanghai": 24870000,
    "Sao Paulo": 12330000,
    "Mumbai": 12440000,
}
pop_series = pd.Series(population, name="Population")
print("City populations:")
print(pop_series)
print()

print(f"Shanghai population: {pop_series['Shanghai']:,}")
print()

# Cities above 12 million
big_cities = pop_series[pop_series > 12000000]
print("Cities with population > 12M:")
print(big_cities)
print()

# ---------------------------------------------------------------------------
# Example 5: Useful Series methods
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 5: Series Methods")
print("=" * 60)

data = pd.Series([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
print("Original Series:")
print(data)
print()

print("value_counts():")
print(data.value_counts())
print()

print("sorted (ascending):")
print(data.sort_values().reset_index(drop=True))
print()

print("unique values:", data.unique())
print("nunique:", data.nunique())
print()

# has NaN
s_nan = pd.Series([1, 2, np.nan, 4, np.nan])
print("Series with NaN:")
print(s_nan)
print(f"hasnans: {s_nan.hasnans}")
print(f"count (non-null): {s_nan.count()}")
print()

print("Done!")
