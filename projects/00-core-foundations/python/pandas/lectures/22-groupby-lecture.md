# Lecture 22: GroupBy in Pandas

## Learning Objectives

By the end of this lecture, you will be able to:
- Split data into groups using `groupby()`
- Apply aggregate functions (sum, mean, count, etc.)
- Use named aggregations for complex summaries
- Apply transform and filter operations
- Chain groupby with other Pandas operations
- Handle multi-level grouping
- Understand the split-apply-combine pattern

---

## 1. The Split-Apply-Combine Pattern

GroupBy follows three steps:
1. **Split** — Divide data into groups based on a key
2. **Apply** — Apply a function to each group
3. **Combine** — Merge results back together

```
DataFrame → Split by key → Apply function → Combined result
┌──────┬───────┐     ┌──────┐  ┌──────┐
│ A  10│ B  20 │ →   │ A:10 │→ │ A:15 │
│ A  20│ B  30 │     │ A:20 │  │ B:25 │
│ A  15│ B  25 │     │ B:20 │  └──────┘
└──────┴───────┘     │ B:30 │
                    │ B:25 │
                    └──────┘
```

---

## 2. Basic GroupBy

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'department': ['Sales', 'Sales', 'Engineering', 'Engineering', 'HR', 'HR', 'Sales', 'Engineering'],
    'employee': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry'],
    'salary': [55000, 62000, 95000, 105000, 58000, 61000, 58000, 98000],
    'bonus': [5000, 6000, 12000, 15000, 4000, 4500, 5500, 13000]
})

# Simple aggregation
dept_mean = df.groupby('department')['salary'].mean()
print(dept_mean)
# department
# Engineering    99333.333333
# HR             59500.000000
# Sales          58333.333333
```

---

## 3. Common Aggregation Functions

```python
# Single function
print(df.groupby('department')['salary'].sum())
print(df.groupby('department')['salary'].mean())
print(df.groupby('department')['salary'].std())
print(df.groupby('department')['salary'].count())

# Multiple functions
print(df.groupby('department')['salary'].agg(['count', 'mean', 'min', 'max']))
#              count          mean    min     max
# department
# Engineering      3  99333.333333  95000  105000
# HR               2  59500.000000  58000   61000
# Sales            3  58333.333333  55000   62000
```

---

## 4. Named Aggregations

```python
# Different aggregations per column
result = df.groupby('department').agg(
    headcount=('employee', 'count'),
    avg_salary=('salary', 'mean'),
    total_bonus=('bonus', 'sum'),
    salary_range=('salary', lambda x: x.max() - x.min()),
    avg_bonus_ratio=('bonus', lambda x: (x / df.loc[x.index, 'salary']).mean())
).reset_index()

print(result)
#     department  headcount    avg_salary  total_bonus  salary_range  avg_bonus_ratio
# 0  Engineering          3  99333.333333        40000         10000         0.131579
# 1           HR          2  59500.000000         8500          3000         0.073077
# 2        Sales          3  58333.333333        16500          7000         0.090278
```

---

## 5. Multiple GroupBy Keys

```python
df_multi = pd.DataFrame({
    'region': ['North', 'North', 'South', 'South', 'North', 'South', 'North', 'South'],
    'department': ['Sales', 'Sales', 'Sales', 'Sales', 'Eng', 'Eng', 'Eng', 'Eng'],
    'revenue': [10000, 12000, 8000, 9500, 25000, 22000, 28000, 20000]
})

# Group by multiple columns
result = df_multi.groupby(['region', 'department'])['revenue'].sum()
print(result)
# region  department
# North   Eng           53000
#         Sales         22000
# South   Eng           42000
#         Sales         17500

# Reset index for flat DataFrame
result = result.reset_index()
print(result)
```

---

## 6. Transform

```python
# Transform applies a function and returns same-sized result
# Useful for adding group-level statistics back to original data

df['dept_avg_salary'] = df.groupby('department')['salary'].transform('mean')
df['salary_vs_dept_avg'] = df['salary'] - df['dept_avg_salary']
df['salary_rank_in_dept'] = df.groupby('department')['salary'].rank(ascending=False)

print(df[['employee', 'department', 'salary', 'dept_avg_salary', 'salary_rank_in_dept']])
#   employee   department  salary  dept_avg_salary  salary_rank_in_dept
# 0    Alice        Sales   55000     58333.333333                  3.0
# 1      Bob        Sales   62000     58333.333333                  1.0
# 2  Charlie  Engineering   95000     99333.333333                  3.0
# 3    Diana  Engineering  105000     99333.333333                  1.0
# 4      Eve           HR   58000     59500.000000                  2.0
# 5    Frank           HR   61000     59500.000000                  1.0
# 6    Grace        Sales   58000     58333.333333                  2.0
# 7    Henry  Engineering   98000     99333.333333                  2.0
```

---

## 7. Filter

```python
# Keep only groups that pass a condition
# Filter departments where average salary > 60000
high_salary_depts = df.groupby('department').filter(
    lambda x: x['salary'].mean() > 60000
)
print(high_salary_depts)
#   department employee  salary  bonus
# 2  Engineering  Charlie   95000  12000
# 3  Engineering    Diana  105000  15000
# 7  Engineering    Henry   98000  13000
```

---

## 8. Apply

```python
# Apply custom function to each group
def top_performer(group):
    return group.nlargest(1, 'salary')[['employee', 'salary']]

top_per_dept = df.groupby('department').apply(top_perductor)
print(top_per_dept)
```

---

## 9. Iterating Over Groups

```python
for name, group in df.groupby('department'):
    print(f"\n--- {name} ({len(group)} employees) ---")
    print(f"  Avg salary: ${group['salary'].mean():,.0f}")
    print(f"  Top earner: {group.nlargest(1, 'salary')['employee'].values[0]}")
```

---

## 10. Common Mistakes

1. **Forgetting `reset_index()`** — GroupBy results have MultiIndex. Reset for flat DataFrame.
2. **Using `apply()` when `agg()` works** — `agg()` is faster and more readable.
3. **Modifying group in iteration** — GroupBy returns views. Use `.copy()` if modifying.
4. **Not specifying column before aggregation** — `df.groupby('dept').mean()` aggregates ALL numeric columns.

---

## 11. Best Practices

1. **Use named aggregations** — `agg(name=('col', 'func'))` produces readable output.
2. **Prefer `agg()` over `apply()`** — `agg()` is vectorized and faster.
3. **Use `transform()` to add group stats** — Preserves original DataFrame shape.
4. **Chain operations** — `df.groupby('dept').agg(...).reset_index().sort_values(...)`

---

## 12. Exercises

### Exercise 1: Sales Summary
Given sales data with `region`, `product`, and `revenue`, create a summary showing total revenue per region and per product.

### Exercise 2: Top Performers
Use `groupby()` and `transform()` to add a column showing each employee's rank within their department.

### Exercise 3: Filter Groups
Filter to keep only departments with more than 3 employees and average salary above $60,000.

---

## 13. Summary

| Method | Purpose | Returns |
|--------|---------|---------|
| `groupby().agg()` | Aggregate groups | DataFrame |
| `groupby().transform()` | Add group stats to original | Series/DataFrame |
| `groupby().filter()` | Keep groups passing condition | DataFrame |
| `groupby().apply()` | Custom function per group | DataFrame |
| `groupby().count()` | Count per group | Series |
| `groupby().sum()` | Sum per group | Series |

**Key takeaway**: GroupBy is the most powerful operation in Pandas for data analysis. Master split-apply-combine and you can answer almost any question about your data.

---

*Next: [23 – Correlation](23-corr-lecture.md)*
