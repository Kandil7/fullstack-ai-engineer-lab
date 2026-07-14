# Glossary 12: Iterating

## Quick Reference

| Term | Definition | Example |
|---|---|---|
| iterrows | Iterate over rows (index, Series) | `for i, row in df.iterrows()` |
| itertuples | Iterate over rows (named tuples) | `for row in df.itertuples()` |
| apply | Apply function to rows/columns | `df.apply(func, axis=1)` |
| map | Map values using dict/function | `df["col"].map(dict)` |
| map (DataFrame) | Apply function element-wise | `df.map(func)` |
| Vectorized | Element-wise operation without loops | `df["A"] + df["B"]` |
| axis | 0=rows, 1=columns | `df.apply(func, axis=1)` |
| Lambda | Anonymous function | `lambda x: x * 2` |

---

## Alphabetical Definitions

### A

**Apply**
Applies a function along rows or columns of a DataFrame.

```python
# Column-wise (default)
df.apply(lambda x: x.max())

# Row-wise
df.apply(lambda x: x.sum(), axis=1)
```

### I

**Iterrows**
Iterates over DataFrame rows as (index, Series) pairs. Slow for large DataFrames.

```python
for index, row in df.iterrows():
    print(index, row["Name"])
```

**Itertuples**
Iterates over DataFrame rows as named tuples. Faster than iterrows().

```python
for row in df.itertuples():
    print(row.Name, row.Age)
```

### L

**Lambda**
An anonymous function defined inline.

```python
df["A"].apply(lambda x: x ** 2)
df.apply(lambda x: x.max() - x.min(), axis=1)
```

### M

**Map**
Maps values using a dictionary or function.

```python
# With dictionary
df["col"].map({"a": 1, "b": 2})

# With function
df["col"].map(lambda x: x.upper())

# DataFrame map (element-wise)
df.map(lambda x: x ** 2)
```

### V

**Vectorized**
Operations applied to entire arrays at once without explicit loops. Much faster than iteration.

```python
df["C"] = df["A"] + df["B"]          # Vectorized
df["D"] = np.sqrt(df["A"])           # Vectorized
df["E"] = np.where(df["A"] > 5, "High", "Low")  # Vectorized
```

---

## Code Examples

### Example 1: Iteration Methods

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [28, 35, 42]
})

# iterrows
for index, row in df.iterrows():
    print(f"{row['Name']}: {row['Age']}")

# itertuples
for row in df.itertuples():
    print(f"{row.Name}: {row.Age}")
```

### Example 2: apply()

```python
import pandas as pd

df = pd.DataFrame({
    "A": [1, 2, 3],
    "B": [4, 5, 6]
})

# Column-wise
print(df.apply(lambda x: x.sum()))

# Row-wise
print(df.apply(lambda x: x.sum(), axis=1))

# Custom function
def range_func(x):
    return x.max() - x.min()

print(df.apply(range_func))
```

### Example 3: map()

```python
import pandas as pd

df = pd.DataFrame({
    "Grade": ["A", "B", "C", "A"]
})

# Map with dictionary
grade_map = {"A": 4, "B": 3, "C": 2, "D": 1}
df["GPA"] = df["Grade"].map(grade_map)

# Map with function
df["Grade_Lower"] = df["Grade"].map(lambda x: x.lower())
```

---

## Related Terms

| Term | Related To | Relationship |
|---|---|---|
| iterrows | DataFrame | Row iteration |
| itertuples | DataFrame | Row iteration (faster) |
| apply | DataFrame | Function application |
| map | Series/DataFrame | Value mapping |
| vectorized | Operations | Fast element-wise ops |
| axis | apply | Direction (rows/columns) |

---

## Performance Comparison

```
Fastest:
  Vectorized operations      (df["A"] + df["B"])
  Numpy functions            (np.sqrt(df["A"]))
  map() with dictionary      (df["col"].map(dict))

Medium:
  apply() with function      (df.apply(func))
  map() with lambda          (df["col"].map(lambda))

Slowest:
  itertuples()               (for row in df.itertuples())
  iterrows()                 (for i, row in df.iterrows())
  Python loops               (for i in range(len(df)))
```

---

## Axis Reference

```
axis=0 or axis="index":
  - Operates along rows (column-wise)
  - df.apply(func, axis=0) applies func to each column

axis=1 or axis="columns":
  - Operates along columns (row-wise)
  - df.apply(func, axis=1) applies func to each row
```

---

## Self-Test Questions

1. What is the difference between `iterrows()` and `itertuples()`?
2. How do you apply a function to each row?
3. When should you use vectorized operations instead of iteration?
4. What does `axis=1` mean in `apply()`?
5. How do you map values using a dictionary?
