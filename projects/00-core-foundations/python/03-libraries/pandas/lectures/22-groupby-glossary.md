# Glossary 22: GroupBy

## Quick Reference

| Method / Function | Purpose | Returns |
|-------------------|---------|---------|
| `df.groupby('col')` | Split DataFrame by key | GroupBy object |
| `.agg()` | Aggregate with functions | DataFrame |
| `.transform()` | Broadcast group result back | Series/DataFrame |
| `.filter()` | Keep groups passing condition | DataFrame |
| `.apply()` | Apply custom function | DataFrame |
| `.sum()` / `.mean()` | Sum / mean per group | Series |
| `.count()` | Count non-null per group | Series |
| `.first()` / `.last()` | First/last value per group | DataFrame |
| `.size()` | Total size per group (incl. NaN) | Series |
| `.nunique()` | Unique count per group | Series |
| `.get_group()` | Get one group as DataFrame | DataFrame |

---

## Alphabetical Definitions

### A

**agg() / aggregate()**
Applies one or more aggregation functions to each group. Supports named aggregations.
```python
df.groupby('dept').agg(
    avg_salary=('salary', 'mean'),
    count=('salary', 'count')
)
```

**apply()**
Applies a custom function to each group. More flexible but slower than `agg()`.
```python
df.groupby('dept').apply(lambda x: x.nlargest(2, 'salary'))
```

### G

**get_group()**
Retrieves a single group as a DataFrame by key value.
```python
sales_team = df.groupby('department').get_group('Sales')
```

### I

**Iterating Over Groups**
Use `for name, group in df.groupby('col'):` to loop through groups. Useful for custom processing.
```python
for dept, group in df.groupby('department'):
    print(f"{dept}: {len(group)} employees")
```

### N

**nunique()**
Counts the number of unique values within each group.
```python
df.groupby('department')['employee'].nunique()
```

### R

**rank()**
Assigns ranks within each group. Useful for finding top performers per category.
```python
df['rank'] = df.groupby('department')['salary'].rank(ascending=False)
```

### S

**size()**
Returns the total size of each group (including NaN values). Unlike `count()`, which excludes NaN.
```python
df.groupby('department').size()
```

**split-apply-combine**
The three-step GroupBy pattern: split data by key, apply function to each group, combine results.
```
Split → Apply → Combine
DataFrame → Groups → Functions → Result
```

### T

**transform()**
Applies a function to each group and broadcasts the result back to the original DataFrame shape. Preserves index alignment.
```python
df['dept_avg'] = df.groupby('dept')['salary'].transform('mean')
df['dept_rank'] = df.groupby('dept')['salary'].rank()
```

---

## Code Examples

### Example 1: Named Aggregations

```python
import pandas as pd

df = pd.DataFrame({
    'store': ['A', 'A', 'B', 'B', 'A', 'B'],
    'product': ['X', 'Y', 'X', 'Y', 'X', 'Y'],
    'revenue': [1000, 1500, 800, 1200, 1100, 1400],
    'quantity': [10, 15, 8, 12, 11, 14]
})

# Multiple aggregations per column
result = df.groupby('store').agg(
    total_revenue=('revenue', 'sum'),
    avg_revenue=('revenue', 'mean'),
    total_units=('quantity', 'sum'),
    num_products=('product', 'nunique'),
    avg_price=('revenue', lambda x: (x / df.loc[x.index, 'quantity']).mean())
).reset_index()

print(result)
```

### Example 2: Transform for Features

```python
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    'department': np.random.choice(['Sales', 'Eng', 'HR'], 100),
    'salary': np.random.randint(40000, 120000, 100)
})

# Add group-level features
df = df.assign(
    dept_mean=df.groupby('department')['salary'].transform('mean'),
    dept_std=df.groupby('department')['salary'].transform('std'),
    dept_min=df.groupby('department')['salary'].transform('min'),
    dept_max=df.groupby('department')['salary'].transform('max'),
    salary_zscore=lambda x: (x['salary'] - x['dept_mean']) / x['dept_std'],
    rank_in_dept=df.groupby('department')['salary'].rank(ascending=False),
    pct_of_dept_total=lambda x: x['salary'] / x.groupby('department')['salary'].transform('sum') * 100
)

print(df.head(10))
```

### Example 3: Filter and Transform

```python
# Filter: keep departments with avg salary > 60000
filtered = df.groupby('department').filter(lambda g: g['salary'].mean() > 60000)

# Then transform on filtered data
filtered['adjusted_salary'] = filtered.groupby('department')['salary'].transform(
    lambda x: x - x.mean() + 70000  # Normalize to 70k baseline
)

print(f"Original: {len(df)} rows, Filtered: {len(filtered)} rows")
```

---

## Related Terms

| Term | Related To | Connection |
|------|-----------|------------|
| `agg()` | `transform()` | Aggregate vs broadcast |
| `transform()` | `rank()`, `mean()` | Add group stats to original |
| `filter()` | Boolean indexing | Keep/drop groups |
| `apply()` | Custom functions | Flexible but slower |
| `groupby` + `merge()` | Alternative | Can achieve same result |
| `pivot_table()` | Aggregation | Reshape + aggregate |

---

*See also: [Lecture 22](22-groupby-lecture.md) | [Lecture 15 – Statistics](15-statistics-lecture.md)*
