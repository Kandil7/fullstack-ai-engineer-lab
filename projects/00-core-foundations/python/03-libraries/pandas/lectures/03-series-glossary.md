# Glossary 03: Series Deep Dive

## Quick Reference

| Term | Definition | Example |
|---|---|---|
| Series | 1D labeled array | `pd.Series([1, 2, 3])` |
| Index | Labels for each element | `s.index` |
| Values | Raw data as NumPy array | `s.values` |
| dtype | Data type of elements | `s.dtype` |
| loc | Label-based indexing | `s.loc["a"]` |
| iloc | Position-based indexing | `s.iloc[0]` |
| Boolean Indexing | Filter by condition | `s[s > 5]` |
| Vectorized Operation | Element-wise operation | `s * 2` |
| Alignment | Index-based matching in operations | `s1 + s2` |
| apply() | Apply function to each element | `s.apply(func)` |
| map() | Map values using dict/Series | `s.map(dict)` |
| rolling() | Rolling window calculations | `s.rolling(3).mean()` |

---

## Alphabetical Definitions

### A

**Alignment**
Pandas aligns values by index when performing operations between Series. Missing indices produce NaN.

```python
s1 = pd.Series([1, 2], index=["a", "b"])
s2 = pd.Series([10, 20], index=["b", "c"])
result = s1 + s2
# a     NaN
# b    12.0
# c     NaN
```

**Aggregation**
Reducing a Series to a single summary value (sum, mean, etc.).

```python
s.sum()    # 360
s.mean()   # 72.0
```

### B

**Boolean Indexing**
Filtering a Series using a boolean mask (True/False values).

```python
s = pd.Series([10, 20, 30, 40])
print(s[s > 20])
# 2    30
# 3    40
```

### D

**Dropna**
Removes missing values (NaN) from a Series.

```python
s = pd.Series([1, np.nan, 3])
print(s.dropna())
# 0    1.0
# 2    3.0
```

**Dtype**
The data type of each element in the Series (int64, float64, object, etc.).

```python
print(s.dtype)  # int64
```

### F

**Fillna**
Replaces missing values with a specified value or strategy.

```python
s = pd.Series([1, np.nan, 3])
print(s.fillna(0))
# 0    1.0
# 1    0.0
# 2    3.0
```

### I

**Index**
Row labels for each element in a Series.

```python
s = pd.Series([1, 2, 3], index=["a", "b", "c"])
print(s.index)
# Index(['a', 'b', 'c'], dtype='object')
```

**Iloc**
Position-based indexing — selects by integer position (0-indexed).

```python
s = pd.Series([10, 20, 30])
print(s.iloc[1])  # 20
```

### L

**Loc**
Label-based indexing — selects by index label.

```python
s = pd.Series([10, 20, 30], index=["a", "b", "c"])
print(s.loc["b"])  # 20
```

### M

**Map**
Maps values using a dictionary or Series.

```python
s = pd.Series(["a", "b", "c"])
mapping = {"a": 1, "b": 2, "c": 3}
print(s.map(mapping))
# 0    1
# 1    2
# 2    3
```

**Missing Value (NaN)**
Not a Number — represents absent data in Pandas.

```python
import numpy as np
s = pd.Series([1, np.nan, 3])
```

### R

**Rank**
Assigns ranks to values (1 = smallest).

```python
s = pd.Series([72, 68, 75])
print(s.rank())
# 0    2.0
# 1    1.0
# 2    3.0
```

**Rolling**
Calculates rolling window statistics (moving average, etc.).

```python
s = pd.Series([1, 2, 3, 4, 5])
print(s.rolling(window=3).mean())
# 0    NaN
# 1    NaN
# 2    2.0
# 3    3.0
# 4    4.0
```

### S

**Sort Values**
Sorts a Series by its values.

```python
s = pd.Series([3, 1, 2])
print(s.sort_values())
# 1    1
# 2    2
# 0    3
```

**Sort Index**
Sorts a Series by its index labels.

```python
s = pd.Series([10, 20, 30], index=["c", "a", "b"])
print(s.sort_index())
# a    20
# b    30
# c    10
```

### V

**Values**
Returns the raw data as a NumPy array.

```python
s = pd.Series([1, 2, 3])
print(s.values)  # [1 2 3]
```

**Vectorized Operation**
Applies an operation to all elements at once without Python loops.

```python
s = pd.Series([1, 2, 3])
print(s * 2)
# 0    2
# 1    4
# 2    6
```

---

## Code Examples

### Example 1: Series Indexing

```python
import pandas as pd

s = pd.Series(
    [72, 68, 75, 80, 65],
    index=["Mon", "Tue", "Wed", "Thu", "Fri"]
)

# Label-based
print(s.loc["Wed"])           # 75
print(s.loc["Mon":"Wed"])     # Slice

# Position-based
print(s.iloc[0])              # 72
print(s.iloc[1:3])            # Slice

# Boolean
print(s[s > 70])
```

### Example 2: Missing Data

```python
import pandas as pd
import numpy as np

s = pd.Series([1, 2, np.nan, 4, np.nan, 6])

print(s.isnull().sum())    # 2
print(s.dropna())          # Remove NaN
print(s.fillna(0))         # Replace with 0
print(s.fillna(s.mean()))  # Replace with mean
```

### Example 3: Aggregation

```python
import pandas as pd

s = pd.Series([72, 68, 75, 80, 65])

print(s.sum())     # 360
print(s.mean())    # 72.0
print(s.std())     # 5.52
print(s.min())     # 65
print(s.max())     # 80
print(s.median())  # 72.0
print(s.count())   # 5
```

---

## Related Terms

| Term | Related To | Relationship |
|---|---|---|
| loc | Series | Label-based indexing |
| iloc | Series | Position-based indexing |
| Boolean Indexing | Series | Filter by condition |
| NaN | Missing Data | Representation of missing values |
| dropna | Series | Remove missing values |
| fillna | Series | Fill missing values |
| apply | Series | Transform each element |
| map | Series | Map values to new values |
| rolling | Series | Window calculations |
| sort_values | Series | Sort by values |

---

## Key Methods Reference

```
Series Indexing:
  s.loc[label]       -> Label-based
  s.iloc[pos]        -> Position-based
  s[condition]       -> Boolean indexing

Missing Data:
  s.isnull()         -> Boolean mask
  s.notnull()        -> Boolean mask
  s.dropna()         -> Remove NaN
  s.fillna(value)    -> Replace NaN

Sorting:
  s.sort_values()    -> Sort by values
  s.sort_index()     -> Sort by index

Aggregation:
  s.sum()            -> Sum
  s.mean()           -> Mean
  s.std()            -> Standard deviation
  s.min()            -> Minimum
  s.max()            -> Maximum
  s.count()          -> Count non-null
  s.nunique()        -> Count unique values

Transformation:
  s.apply(func)      -> Apply function
  s.map(dict)        -> Map values
  s.rolling(n)       -> Rolling window
```

---

## Self-Test Questions

1. What is the difference between `.loc` and `.iloc`?
2. How do you fill missing values with the mean?
3. What happens when you add two Series with different indices?
4. How do you apply a custom function to every element?
5. What is the difference between `.apply()` and `.map()`?
