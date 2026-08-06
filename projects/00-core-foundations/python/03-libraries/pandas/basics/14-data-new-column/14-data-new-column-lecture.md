# Lecture 14: Adding New Columns in Pandas

## Learning Objectives

By the end of this lecture, you will be able to:
- Create new columns from existing data
- Use conditional logic to create categorical columns
- Apply functions row-wise and element-wise
- Derive date/time components
- Use `assign()` for method chaining
- Create columns with `np.select()` for complex conditions
- Avoid common pitfalls with chained assignment

---

## 1. Why Add New Columns?

Raw data often lacks the fields needed for analysis. You may need:
- **Derived metrics**: profit margin from revenue and cost
- **Categorical bins**: age groups from raw ages
- **Flags**: boolean indicators for conditions
- **Time components**: year, month, day from a datetime
- **Normalized values**: per-capita rates, percentages

Adding columns is one of the most common Pandas operations.

---

## 2. Basic Column Creation

### 2.1 Direct Assignment

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'product': ['A', 'B', 'C', 'D'],
    'revenue': [1000, 2500, 800, 3200],
    'cost': [600, 1800, 500, 2100]
})

# Simple arithmetic
df['profit'] = df['revenue'] - df['cost']
df['profit_margin'] = (df['profit'] / df['revenue'] * 100).round(2)

print(df)
#   product  revenue  cost  profit  profit_margin
# 0       A     1000   600     400          40.0
# 1       B     2500  1800     700          28.0
# 2       C      800   500     300          37.5
# 3       D     3200  2100    1100          34.4
```

### 2.2 Constant Value

```python
df['currency'] = 'USD'
df['tax_rate'] = 0.08
df['processed'] = False
```

---

## 3. Conditional Columns

### 3.1 Using np.where()

```python
# Binary condition
df['is_profitable'] = np.where(df['profit'] > 0, 'Yes', 'No')

# With numeric default
df['bonus'] = np.where(df['revenue'] > 2000, df['revenue'] * 0.05, 0)
```

### 3.2 Using np.select() for Multiple Conditions

```python
conditions = [
    df['profit_margin'] >= 40,
    df['profit_margin'] >= 30,
    df['profit_margin'] >= 20,
]
choices = ['Excellent', 'Good', 'Average']

df['performance'] = np.select(conditions, choices, default='Poor')
```

### 3.3 Using pd.cut() for Binning

```python
# Equal-width bins
df['revenue_tier'] = pd.cut(
    df['revenue'],
    bins=[0, 1000, 2000, 3000, float('inf')],
    labels=['Low', 'Medium', 'High', 'Premium']
)

# Custom bins with specific edges
df['profit_category'] = pd.cut(
    df['profit'],
    bins=[-float('inf'), 0, 500, 1000, float('inf')],
    labels=['Loss', 'Low', 'Medium', 'High']
)
```

### 3.4 Using pd.qcut() for Quantile Bins

```python
# Divide into equal-frequency groups
df['revenue_quartile'] = pd.qcut(
    df['revenue'],
    q=4,
    labels=['Q1', 'Q2', 'Q3', 'Q4']
)
```

---

## 4. Applying Functions

### 4.1 Element-wise with apply()

```python
# Apply a function to each element
df['profit_label'] = df['profit'].apply(
    lambda x: 'High' if x > 800 else 'Medium' if x > 300 else 'Low'
)

# Apply to each row
df['summary'] = df.apply(
    lambda row: f"{row['product']}: ${row['profit']:,} ({row['profit_margin']}%)",
    axis=1
)
```

### 4.2 Vectorized Operations (Preferred)

```python
# Faster than apply() for simple operations
df['revenue_per_cost'] = df['revenue'] / df['cost']
df['double_revenue'] = df['revenue'] * 2
df['revenue_log'] = np.log1p(df['revenue'])  # log(1+x) for safety
```

### 4.3 Using np.vectorize()

```python
def classify_product(margin):
    if margin >= 40:
        return 'Star'
    elif margin >= 30:
        return 'Cash Cow'
    elif margin >= 20:
        return 'Question Mark'
    else:
        return 'Dog'

# Vectorize for efficiency on large datasets
classify_vec = np.vectorize(classify_product)
df['boston_matrix'] = classify_vec(df['profit_margin'])
```

---

## 5. Date/Time Derived Columns

```python
df = pd.DataFrame({
    'date': pd.to_datetime(['2024-01-15', '2024-06-20', '2024-12-31']),
    'amount': [100, 250, 180]
})

# Extract components
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['day_of_week'] = df['date'].dt.day_name()
df['quarter'] = df['date'].dt.quarter
df['is_weekend'] = df['date'].dt.dayofweek >= 5
df['week_number'] = df['date'].dt.isocalendar().week

# Date arithmetic
df['days_from_start'] = (df['date'] - df['date'].min()).dt.days
df['month_year'] = df['date'].dt.to_period('M')
```

---

## 6. String-Derived Columns

```python
df = pd.DataFrame({
    'full_name': ['Alice Smith', 'Bob Johnson', 'Charlie Brown'],
    'email': ['alice@example.com', 'bob@test.org', 'charlie@demo.net']
})

# Split strings
df['first_name'] = df['full_name'].str.split().str[0]
df['last_name'] = df['full_name'].str.split().str[-1]

# Extract patterns
df['domain'] = df['email'].str.extract(r'@(.+)')
df['username'] = df['email'].str.split('@').str[0]

# Length and character operations
df['name_length'] = df['full_name'].str.len()
df['initials'] = df['full_name'].str[0]
```

---

## 7. Using assign() for Method Chaining

```python
# assign() returns a new DataFrame — great for chaining
result = (df
    .assign(
        profit=lambda x: x['revenue'] - x['cost'],
        margin=lambda x: (x['profit'] / x['revenue'] * 100).round(2),
        tier=lambda x: pd.cut(x['margin'], bins=[0, 25, 35, 100], labels=['Low', 'Mid', 'High']),
        is_high=lambda x: x['margin'] > 35
    )
    .query('is_high == True')
)
```

---

## 8. Cumulative and Rolling Columns

```python
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=5),
    'sales': [100, 150, 120, 180, 160]
})

# Cumulative sum
df['cumulative_sales'] = df['sales'].cumsum()

# Cumulative max
df['running_max'] = df['sales'].cummax()

# Rolling average (3-day window)
df['rolling_avg_3d'] = df['sales'].rolling(window=3).mean()

# Percentage change
df['pct_change'] = df['sales'].pct_change()

# Rank
df['sales_rank'] = df['sales'].rank(ascending=False)
```

---

## 9. Common Mistakes

1. **Chained assignment warning** — `df['new_col'] = ...` on a slice may trigger `SettingWithCopyWarning`. Use `.loc[]` or `assign()`.
2. **Using apply() when vectorized works** — `apply()` is slow on large DataFrames. Prefer vectorized operations.
3. **Modifying during iteration** — Never loop over rows to create columns. Vectorize instead.
4. **Forgetting NaN propagation** — Operations on NaN produce NaN. Handle missing values before deriving columns.
5. **Setting wrong index alignment** — When adding from another Series, ensure indices match or use `.values`.

---

## 10. Best Practices

1. **Prefer vectorized operations** over `apply()` — they are 10-100x faster.
2. **Use `assign()` for chaining** — keeps transformations clean and readable.
3. **Name columns clearly** — `profit_margin_pct` is better than `pm`.
4. **Add columns in logical groups** — derive all date components together.
5. **Check dtypes after creation** — new columns may not have expected types.
6. **Use `pd.cut()` and `pd.qcut()`** instead of manual if/else chains for binning.

---

## 11. Exercises

### Exercise 1: Profit Analysis
Given this DataFrame, add columns for: profit, profit_margin, and a "performance" label (Excellent/Good/Average/Poor).
```python
df = pd.DataFrame({
    'product': ['A', 'B', 'C', 'D', 'E'],
    'revenue': [5000, 3200, 1800, 4500, 2100],
    'cost': [3000, 2800, 1200, 2700, 1900]
})
```

### Exercise 2: Date Features
Create a DataFrame with a `datetime` column and derive: year, month, quarter, day_name, is_weekend, and days_since_start.

### Exercise 3: Conditional Logic
Given a student grades DataFrame, create columns for letter grade (A/B/C/D/F) and pass/fail status using `np.select()`.

---

## 12. Summary

| Method | Use Case | Performance |
|--------|----------|-------------|
| Direct assignment | Simple arithmetic | Fast |
| `np.where()` | Binary conditions | Fast |
| `np.select()` | Multiple conditions | Fast |
| `pd.cut()` | Binning into categories | Fast |
| `pd.qcut()` | Quantile-based bins | Fast |
| `.apply()` | Complex row-wise logic | Slow |
| `assign()` | Method chaining | Fast |

**Key takeaway**: Adding derived columns transforms raw data into analysis-ready features. Always prefer vectorized operations over row-wise apply for performance.

---

*Next: [15 – Statistics](15-statistics-lecture.md)*
