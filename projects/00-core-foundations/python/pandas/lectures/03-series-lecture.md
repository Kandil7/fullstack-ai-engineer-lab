# Lecture 03: Series Deep Dive

## 🎯 Learning Objectives

By the end of this lecture, you will be able to:

- Create Series from various data sources
- Use label-based and position-based indexing
- Perform vectorized operations on Series
- Apply methods for data cleaning and transformation
- Understand alignment behavior in Pandas

---

## 📖 1. What is a Series?

A Series is a one-dimensional labeled array capable of holding any data type. It is the building block of DataFrames — every column in a DataFrame is a Series.

```python
import pandas as pd

s = pd.Series([10, 20, 30, 40, 50])
print(s)
# 0    10
# 1    20
# 2    30
# 3    40
# 4    50
# dtype: int64
```

### Components of a Series

| Component | Description | Access |
|---|---|---|
| Values | The actual data (NumPy array) | `s.values` |
| Index | Row labels | `s.index` |
| Name | Optional name for the Series | `s.name` |
| Dtype | Data type of values | `s.dtype` |

---

## 📖 2. Creating a Series

### From a List

```python
import pandas as pd

s = pd.Series([72, 68, 75, 80, 65])
print(s)
# 0    72
# 1    68
# 2    75
# 3    80
# 4    65
# dtype: int64
```

### From a Dictionary

```python
import pandas as pd

population = pd.Series({
    "Tokyo": 13960000,
    "Delhi": 11030000,
    "Shanghai": 24870000,
    "Sao Paulo": 12330000
})
print(population)
# Tokyo       13960000
# Delhi       11030000
# Shanghai    24870000
# Sao Paulo   12330000
# dtype: int64
```

### From a NumPy Array

```python
import numpy as np
import pandas as pd

arr = np.array([1.5, 2.7, 3.9, 4.1])
s = pd.Series(arr, dtype="float32")
print(s.dtype)  # float32
```

### With Custom Index and Name

```python
import pandas as pd

temps = pd.Series(
    [72, 68, 75, 80, 65],
    index=["Mon", "Tue", "Wed", "Thu", "Fri"],
    name="Temperature"
)
print(temps.name)  # Temperature
```

---

## 📖 3. Indexing a Series

### Label-Based Indexing (loc)

```python
import pandas as pd

s = pd.Series(
    [72, 68, 75, 80, 65],
    index=["Mon", "Tue", "Wed", "Thu", "Fri"]
)

# Single label
print(s.loc["Wed"])  # 75

# Multiple labels
print(s.loc[["Mon", "Fri"]])
# Mon    72
# Fri    65

# Slice with labels (inclusive end)
print(s.loc["Mon":"Wed"])
# Mon    72
# Tue    68
# Wed    75
```

### Position-Based Indexing (iloc)

```python
import pandas as pd

s = pd.Series([72, 68, 75, 80, 65])

# Single position
print(s.iloc[0])  # 72

# Multiple positions
print(s.iloc[[0, 2, 4]])
# 0    72
# 2    75
# 4    65

# Slice (exclusive end)
print(s.iloc[1:3])
# 1    68
# 2    75
```

### Boolean Indexing

```python
import pandas as pd

s = pd.Series([72, 68, 75, 80, 65])

# Filter
hot_days = s[s > 70]
print(hot_days)
# 0    72
# 2    75
# 3    80

# Multiple conditions
filtered = s[(s >= 68) & (s <= 75)]
print(filtered)
# 0    72
# 1    68
# 2    75
```

---

## 📖 4. Vectorized Operations

### Arithmetic Operations

```python
import pandas as pd

s1 = pd.Series([1, 2, 3, 4])
s2 = pd.Series([10, 20, 30, 40])

# Element-wise operations
print(s1 + s2)    # Addition
print(s1 * s2)    # Multiplication
print(s2 - s1)    # Subtraction
print(s2 / s1)    # Division

# With scalar
print(s1 * 10)
# 0    10
# 1    20
# 2    30
# 3    40
```

### Comparison Operations

```python
import pandas as pd

s = pd.Series([72, 68, 75, 80, 65])

print(s > 70)     # Boolean Series
print(s >= 70)    # Boolean Series
print(s == 75)    # Boolean Series
print(s != 72)    # Boolean Series
```

### Mathematical Functions

```python
import pandas as pd
import numpy as np

s = pd.Series([1, 4, 9, 16, 25])

print(np.sqrt(s))      # Square root
print(np.log(s))       # Natural log
print(np.exp(s))       # Exponential
print(s.sum())         # Sum
print(s.mean())        # Mean
print(s.std())         # Standard deviation
print(s.min())         # Minimum
print(s.max())         # Maximum
```

---

## 📖 5. Useful Methods

### Handling Missing Data

```python
import pandas as pd
import numpy as np

s = pd.Series([1, 2, np.nan, 4, np.nan, 6])

print(s.isnull())          # Boolean mask of nulls
# 0    False
# 1    False
# 2     True
# 3    False
# 4     True
# 5    False

print(s.dropna())          # Remove nulls
# 0    1.0
# 1    2.0
# 3    4.0
# 5    6.0

print(s.fillna(0))         # Fill nulls with 0
# 0    1.0
# 1    2.0
# 2    0.0
# 3    4.0
# 4    0.0
# 5    6.0

print(s.fillna(s.mean()))  # Fill with mean
```

### Sorting

```python
import pandas as pd

s = pd.Series(
    [72, 68, 75, 80, 65],
    index=["Mon", "Tue", "Wed", "Thu", "Fri"]
)

print(s.sort_values())         # Sort by values
print(s.sort_values(ascending=False))  # Descending
print(s.sort_index())          # Sort by index
print(s.rank())                # Rank values
```

### Aggregation

```python
import pandas as pd

s = pd.Series([72, 68, 75, 80, 65])

print(s.sum())        # 360
print(s.mean())       # 72.0
print(s.median())     # 72.0
print(s.std())        # 5.52
print(s.min())        # 65
print(s.max())        # 80
print(s.count())      # 5
print(s.nunique())    # 5
print(s.unique())     # [72 68 75 80 65]
```

### String Operations

```python
import pandas as pd

s = pd.Series(["Alice", "Bob", "Charlie", "Diana"])

print(s.str.lower())
print(s.str.upper())
print(s.str.len())
print(s.str.contains("li"))
print(s.str.replace("a", "@"))
```

---

## 📖 6. Alignment Behavior

Pandas aligns values by index when performing operations between Series.

```python
import pandas as pd

s1 = pd.Series([1, 2, 3], index=["a", "b", "c"])
s2 = pd.Series([10, 20, 30], index=["b", "c", "d"])

# Alignment by index
result = s1 + s2
print(result)
# a     NaN
# b    22.0
# c    33.0
# d     NaN
# dtype: float64
```

### Filling Missing Values

```python
result = s1.add(s2, fill_value=0)
print(result)
# a     1.0
# b    22.0
# c    33.0
# d    30.0
# dtype: float64
```

---

## 📖 7. Applying Functions

### Using `.apply()`

```python
import pandas as pd

s = pd.Series([1, 4, 9, 16, 25])

print(s.apply(lambda x: x ** 2))
# 0     1
# 1    16
# 2    81
# 3   256
# 4   625
```

### Using `.map()`

```python
import pandas as pd

s = pd.Series(["a", "b", "c", "a"])

mapping = {"a": "Alpha", "b": "Beta", "c": "Gamma"}
print(s.map(mapping))
# 0    Alpha
# 1     Beta
# 2    Gamma
# 3    Alpha
```

---

## 📖 8. Real-World Example

```python
import pandas as pd

# Monthly sales data
sales = pd.Series(
    [45000, 52000, 38000, 61000, 55000, 48000,
     67000, 72000, 58000, 63000, 71000, 85000],
    index=pd.date_range("2024-01", periods=12, freq="MS"),
    name="Monthly Sales"
)

# Summary statistics
print("Total Sales:", sales.sum())
print("Average Sales:", sales.mean())
print("Best Month:", sales.idxmax())
print("Worst Month:", sales.idxmin())

# Growth rate
print("Growth Rate:")
print(sales.pct_change().dropna())

# Rolling average (3-month)
print("3-Month Rolling Average:")
print(sales.rolling(window=3).mean())
```

---

## ❌ 9. Common Mistakes

### Mistake 1: Using `[]` for Label-Based Indexing with Non-Integer Labels

```python
import pandas as pd

s = pd.Series([10, 20, 30], index=["a", "b", "c"])

# This may not work as expected
# print(s["a"])  # Works, but ambiguous with integer index

# Always use .loc for label-based
print(s.loc["a"])
```

### Mistake 2: Forgetting Alignment

```python
import pandas as pd

s1 = pd.Series([1, 2, 3], index=["a", "b", "c"])
s2 = pd.Series([10, 20], index=["a", "b"])

# Result has NaN for missing index
result = s1 + s2
# c is NaN because it's only in s1
```

### Mistake 3: Modifying a View

```python
import pandas as pd

s = pd.Series([1, 2, 3, 4, 5])

# This may raise a warning
# s[s > 2] = 99

# Use .loc instead
s.loc[s > 2] = 99
```

---

## ✅ 10. Best Practices

1. **Use `.loc` and `.iloc`** — avoid ambiguous indexing with `[]`
2. **Check alignment** — when combining Series, verify index alignment
3. **Use `.fillna()` before operations** — prevent NaN propagation
4. **Name your Series** — helps with debugging and output readability
5. **Use vectorized operations** — avoid Python loops
6. **Leverage `.apply()` for complex logic** — when vectorization isn't possible
7. **Use `.rolling()` for time series** — moving averages, windows

---

## 🏋️ 11. Exercises

### Exercise 1: Series Creation

```python
import pandas as pd

# TODO: Create a Series of temperatures for a week
# Use days as index: Mon-Sun
# Include at least one missing value (np.nan)

# TODO: Print the Series
# TODO: Print the mean temperature (ignoring NaN)
# TODO: Print the hottest and coldest days
```

### Exercise 2: Filtering and Transformation

```python
import pandas as pd
import numpy as np

s = pd.Series([15, 22, np.nan, 35, 28, 42, 19, np.nan, 31])

# TODO: Count the number of missing values
# TODO: Fill missing values with the mean
# TODO: Filter values greater than 25
# TODO: Calculate the percentage of values above 25
```

### Exercise 3: String Operations

```python
import pandas as pd

s = pd.Series(["  Alice Smith  ", "BOB JONES", "charlie brown", "Diana Prince"])

# TODO: Strip whitespace, lowercase all, and count characters
# TODO: Extract the first name (before the space)
# TODO: Replace spaces with underscores
```

---

## 📝 12. Summary

| Concept | What You Learned |
|---|---|
| Series Components | Values, index, name, dtype |
| Creation | From lists, dicts, arrays |
| Indexing | `.loc` (labels), `.iloc` (positions), boolean |
| Operations | Arithmetic, comparison, math functions |
| Methods | `dropna()`, `fillna()`, `sort_values()`, `apply()` |
| Alignment | Index-based alignment in operations |
| Aggregation | `sum()`, `mean()`, `std()`, `min()`, `max()` |

### Next Lecture

In [Lecture 04: DataFrames Deep Dive](./04-dataframes-lecture.md), we will explore DataFrames in depth — row/column operations, transformation, and advanced indexing.

---

## 📚 Further Reading

- [Pandas Series Documentation](https://pandas.pydata.org/docs/reference/series.html)
- [Pandas User Guide: Series](https://pandas.pydata.org/docs/user_guide/basics.html)
- [Pandas Comparison with SQL](https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sql.html)
