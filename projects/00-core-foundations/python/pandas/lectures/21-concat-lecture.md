# Lecture 21: Concat in Pandas

## Learning Objectives

By the end of this lecture, you will be able to:
- Concatenate DataFrames vertically (rows) and horizontally (columns)
- Handle index alignment and duplicates
- Use `ignore_index` to reindex
- Concatenate with different column sets
- Merge multiple DataFrames in a loop
- Choose between concat and merge

---

## 1. What is Concat?

Concat (concatenation) stacks DataFrames together. Unlike merge (which joins on keys), concat simply appends DataFrames along an axis. Think of it as gluing tables together.

---

## 2. Basic Vertical Concatenation

```python
import pandas as pd
import numpy as np

# Monthly sales data
jan = pd.DataFrame({
    'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
    'product': ['A', 'B', 'A'],
    'sales': [100, 150, 120]
})

feb = pd.DataFrame({
    'date': ['2024-02-01', '2024-02-02', '2024-02-03'],
    'product': ['B', 'A', 'C'],
    'sales': [200, 180, 90]
})

mar = pd.DataFrame({
    'date': ['2024-03-01', '2024-03-02'],
    'product': ['A', 'B'],
    'sales': [210, 170]
})

# Stack vertically (along rows)
quarter = pd.concat([jan, feb, mar], ignore_index=True)
print(quarter)
#          date product  sales
# 0  2024-01-01       A    100
# 1  2024-01-02       B    150
# 2  2024-01-03       A    120
# 3  2024-02-01       B    200
# 4  2024-02-02       A    180
# 5  2024-02-03       C     90
# 6  2024-03-01       A    210
# 7  2024-03-02       B    170
```

---

## 3. Horizontal Concatenation

```python
# Side by side (along columns)
df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
df2 = pd.DataFrame({'C': [7, 8, 9], 'D': [10, 11, 12]})

horizontal = pd.concat([df1, df2], axis=1)
print(horizontal)
#    A  B   C   D
# 0  1  4   7  10
# 1  2  5   8  11
# 2  3  6   9  12
```

---

## 4. Key Parameters

### 4.1 ignore_index

```python
# Without ignore_index — preserves original indices
result = pd.concat([df1, df2])
print(result.index)
# Int64Index([0, 1, 2, 0, 1, 2])  # Duplicate indices!

# With ignore_index — creates clean sequential index
result = pd.concat([df1, df2], ignore_index=True)
print(result.index)
# RangeIndex(start=0, stop=6, step=1)
```

### 4.2 axis Parameter

```python
# axis=0: Stack vertically (default)
pd.concat([df1, df2], axis=0)

# axis=1: Stack horizontally
pd.concat([df1, df2], axis=1)
```

### 4.3 join Parameter

```python
# join='outer' (default): Keep all columns, fill NaN where missing
df3 = pd.DataFrame({'A': [1, 2], 'B': [3, 4], 'E': [5, 6]})
df4 = pd.DataFrame({'A': [7, 8], 'C': [9, 10]})

result = pd.concat([df3, df4], join='outer')
print(result)
#     A    B    C    E
# 0  1.0  3.0  NaN  5.0
# 1  2.0  4.0  NaN  6.0
# 2  7.0  NaN  9.0  NaN
# 3  8.0  NaN  10.0 NaN

# join='inner': Only keep common columns
result = pd.concat([df3, df4], join='inner')
print(result)
#    A
# 0  1
# 1  2
# 2  7
# 3  8
```

---

## 5. Concatenating Many DataFrames

### 5.1 Loop Concatenation

```python
# Read and concatenate multiple CSV files
import glob

files = glob.glob('data/sales_*.monthly_*.csv')
all_data = []

for file in files:
    df = pd.read_csv(file)
    all_data.append(df)

combined = pd.concat(all_data, ignore_index=True)
```

### 5.2 Dictionary of DataFrames

```python
data = {
    'January': jan,
    'February': feb,
    'March': mar
}

# Concat with keys to identify source
quarter = pd.concat(data, names=['month', 'quarter_index'])
print(quarter.head())
#                  date product  sales
# month    quarter_index
# January  0     2024-01-01       A    100
#          1     2024-01-02       B    150
#          2     2024-01-03       A    120
```

---

## 6. Handling Misaligned Columns

```python
df_a = pd.DataFrame({'A': [1, 2], 'B': [3, 4], 'C': [5, 6]})
df_b = pd.DataFrame({'B': [7, 8], 'C': [9, 10], 'D': [11, 12]})

# Outer concat (all columns)
result = pd.concat([df_a, df_b], ignore_index=True)
print(result)
#     A  B   C     D
# 0  1.0  3   5   NaN
# 1  2.0  4   6   NaN
# 2  NaN  7   9  11.0
# 3  NaN  8  10  12.0

# Inner concat (common columns only)
result = pd.concat([df_a, df_b], join='inner', ignore_index=True)
print(result)
#    B   C
# 0  3   5
# 1  4   6
# 2  7   9
# 3  8  10
```

---

## 7. Concat vs Merge

| Feature | concat | merge |
|---------|--------|-------|
| Purpose | Stack/append DataFrames | Join on shared keys |
| Axis | Rows or columns | Always joins on keys |
| Key matching | No | Yes |
| Use case | Same structure tables | Related tables |

```python
# concat: Same structure, just stack
pd.concat([df1, df2, df3], ignore_index=True)

# merge: Different structure, join on keys
pd.merge(df_customers, df_orders, on='customer_id')
```

---

## 8. Common Mistakes

1. **Forgetting `ignore_index=True`** — Duplicate indices cause problems later.
2. **Not checking columns** — Different columns produce NaN. Use `join='inner'` if you want only common columns.
3. **Concatenating in a loop without collecting** — Always append to a list, then concat once.
4. **Mixing up axis** — `axis=0` stacks rows; `axis=1` stacks columns.

---

## 9. Best Practices

1. **Collect in a list, concat once** — Much faster than repeated concat.
2. **Always use `ignore_index=True`** unless you need multi-level indexing.
3. **Check shapes before concat** — Verify each DataFrame has expected columns.
4. **Use `keys=` parameter** — Creates a MultiIndex identifying source DataFrames.

---

## 10. Exercises

### Exercise 1: Monthly Files
Concatenate 12 monthly CSV files into a single yearly DataFrame with a `month` column.

### Exercise 2: Missing Columns
Concatenate two DataFrames with different columns using both `join='outer'` and `join='inner'`. What's the difference?

### Exercise 3: Multi-Index
Use the `keys` parameter to concatenate three DataFrames and create a MultiIndex. Reset the index and examine the structure.

---

## 11. Summary

| Parameter | Purpose | Default |
|-----------|---------|---------|
| `axis=0` | Stack vertically (rows) | Default |
| `axis=1` | Stack horizontally (columns) | — |
| `ignore_index` | Reset index to 0,1,2... | False |
| `join='outer'` | Keep all columns | Default |
| `join='inner'` | Keep only common columns | — |
| `keys` | Create MultiIndex source labels | None |

**Key takeaway**: Concat is for stacking DataFrames with the same structure. Merge is for joining related DataFrames on shared keys. Know which one to use.

---

*Next: [22 – GroupBy](22-groupby-lecture.md)*
