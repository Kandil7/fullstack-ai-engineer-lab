# Glossary 21: Concat

## Quick Reference

| Method / Function | Purpose | Returns |
|-------------------|---------|---------|
| `pd.concat()` | Stack/append DataFrames | DataFrame |
| `axis=0` | Stack vertically (rows) | — |
| `axis=1` | Stack horizontally (columns) | — |
| `ignore_index` | Reset index | bool |
| `join='outer'` | Keep all columns (fill NaN) | — |
| `join='inner'` | Keep only common columns | — |
| `keys` | Add MultiIndex source labels | list |
| `names` | Name MultiIndex levels | list |
| `sort` | Sort columns if axis=1 | bool |

---

## Alphabetical Definitions

### A

**axis**
Determines concatenation direction. `axis=0` stacks rows vertically. `axis=1` stacks columns horizontally.
```python
pd.concat([df1, df2], axis=0)  # Vertical (default)
pd.concat([df1, df2], axis=1)  # Horizontal
```

### C

**Concatenation**
Joining two or more DataFrames by stacking them along an axis. Unlike merge, concat doesn't use key-based matching.
```python
pd.concat([df1, df2, df3], ignore_index=True)
```

### I

**ignore_index**
When True, discards original indices and creates a new sequential RangeIndex. Prevents duplicate index issues.
```python
pd.concat([df1, df2], ignore_index=True)
# Index: 0, 1, 2, 3, 4, 5 (not 0, 1, 2, 0, 1, 2)
```

### J

**join**
Controls how columns are handled. `'outer'` (default) keeps all columns, filling NaN where missing. `'inner'` keeps only common columns.
```python
pd.concat([df1, df2], join='outer')  # All columns
pd.concat([df1, df2], join='inner')  # Common columns only
```

### K

**keys**
Adds a level to the MultiIndex identifying which DataFrame each row came from. Useful for tracking source data.
```python
result = pd.concat([df1, df2], keys=['source_a', 'source_b'])
print(result.index)
# MultiIndex([('source_a', 0), ('source_a', 1), ('source_b', 0), ...])
```

### M

**MultiIndex**
Hierarchical index created by the `keys` parameter. Levels represent source DataFrame labels and original row indices.
```python
result = pd.concat(data_dict, names=['source', 'row_id'])
result.reset_index()  # Convert to flat DataFrame
```

### N

**names**
Names the levels of the MultiIndex created by `keys`. Improves readability.
```python
pd.concat(data, keys=['Jan', 'Feb', 'Mar'], names=['month', 'idx'])
```

### S

**sort**
When concatenating horizontally (`axis=1`), sorts the resulting columns alphabetically. Default is True.
```python
pd.concat([df1, df2], axis=1, sort=False)  # Preserve column order
```

---

## Code Examples

### Example 1: Batch File Concatenation

```python
import pandas as pd
import glob

# Find all CSV files
files = glob.glob('data/*.csv')
print(f"Found {len(files)} files")

# Efficient batch concat
dfs = []
for file in files:
    df = pd.read_csv(file)
    df['source_file'] = file  # Track origin
    dfs.append(df)

# Single concat operation (fast)
combined = pd.concat(dfs, ignore_index=True)
print(f"Combined shape: {combined.shape}")
```

### Example 2: Column Alignment

```python
df_a = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df_b = pd.DataFrame({'B': [5, 6], 'C': [7, 8]})

# Outer: All columns
outer = pd.concat([df_a, df_b], join='outer', ignore_index=True)
print("Outer join:")
print(outer)
#     A  B    C
# 0  1.0  3  NaN
# 1  2.0  4  NaN
# 2  NaN  5  7.0
# 3  NaN  6  8.0

# Inner: Common columns only
inner = pd.concat([df_a, df_b], join='inner', ignore_index=True)
print("\nInner join:")
print(inner)
#    B
# 0  3
# 1  4
# 2  5
# 3  6
```

### Example 3: Multi-Index Tracking

```python
quarterly = {
    'Q1': pd.DataFrame({'sales': [100, 120, 110]}),
    'Q2': pd.DataFrame({'sales': [130, 140, 125]}),
    'Q3': pd.DataFrame({'sales': [150, 145, 160]}),
    'Q4': pd.DataFrame({'sales': [170, 180, 175]})
}

result = pd.concat(quarterly, names=['quarter', 'month_idx'])
print(result)

# Reset to flat DataFrame
result = result.reset_index()
print(result)
#   quarter  level_1  sales
# 0      Q1        0    100
# 1      Q1        1    120
# 2      Q1        2    110
# 3      Q2        0    130
# ...
```

---

## Related Terms

| Term | Related To | Connection |
|------|-----------|------------|
| `axis` | `concat()` | Direction: rows (0) or columns (1) |
| `ignore_index` | `reset_index()` | Both reset to sequential index |
| `join` | SQL JOIN concept | Outer = UNION, Inner = INTERSECT |
| `keys` | `MultiIndex` | Source tracking |
| `merge()` | `concat()` | Key-based vs stack-based combining |
| `append()` | `concat()` | Deprecated; use concat instead |

---

*See also: [Lecture 21](21-concat-lecture.md) | [Lecture 20 – Merge](20-merge-lecture.md)*
