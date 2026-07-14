# Glossary 14: Adding New Columns

## Quick Reference

| Method / Function | Purpose | Returns |
|-------------------|---------|---------|
| `df['col'] = value` | Create column via assignment | DataFrame |
| `df.assign(**kwargs)` | Create columns (chainable) | New DataFrame |
| `np.where(cond, x, y)` | Binary conditional column | Array |
| `np.select(conds, choices)` | Multi-condition column | Array |
| `pd.cut(x, bins, labels)` | Bin into equal-width groups | Categorical Series |
| `pd.qcut(x, q, labels)` | Bin into equal-frequency groups | Categorical Series |
| `df.apply(func, axis)` | Apply function row/col-wise | Series/DataFrame |
| `df.cumsum()` | Cumulative sum | Series |
| `df.rolling(n).mean()` | Rolling window average | Series |
| `df.pct_change()` | Percentage change | Series |
| `df.rank()` | Rank values | Series |
| `df[col].dt.*` | Datetime component access | Series |

---

## Alphabetical Definitions

### A

**assign()**
Returns a new DataFrame with added (or replaced) columns. Ideal for method chaining because it doesn't modify the original.
```python
result = df.assign(
    profit=lambda x: x['revenue'] - x['cost'],
    margin=lambda x: x['profit'] / x['revenue']
)
```

**apply()**
Applies a function along rows (`axis=1`) or columns (`axis=0`). Useful for complex logic but slower than vectorized operations.
```python
df['label'] = df.apply(lambda row: 'High' if row['score'] > 80 else 'Low', axis=1)
```

**astype()**
Changes the dtype of a column. Useful after creating a derived column that should be a specific type.
```python
df['is_active'] = df['status'].astype(bool)
```

### C

**Conditional Column**
A column whose values depend on conditions applied to other columns. Created with `np.where()`, `np.select()`, or boolean indexing.
```python
df['grade'] = np.where(df['score'] >= 90, 'A',
               np.where(df['score'] >= 80, 'B', 'C'))
```

**cumsum()**
Returns the cumulative sum along a axis. Useful for running totals.
```python
df['cumulative_sales'] = df['daily_sales'].cumsum()
```

**cummax() / cummin()**
Returns the cumulative maximum or minimum.
```python
df['running_high'] = df['price'].cummax()
```

### D

**dt Accessor**
Provides datetime properties and methods for Series with datetime dtype.
```python
df['month'] = df['date'].dt.month
df['day_name'] = df['date'].dt.day_name()
df['quarter'] = df['date'].dt.quarter
```

**Day-of-Week Numbering**
Monday=0 through Sunday=6. Used for weekend detection: `df['date'].dt.dayofweek >= 5`.

### I

**ISO Calendar Week**
Week number according to ISO 8601. Accessed via `df['date'].dt.isocalendar().week`.

### L

**Lambda Function**
Anonymous inline function used with `apply()` or `assign()`. Convenient for simple one-off operations.
```python
df.assign(new_col=lambda x: x['a'] + x['b'])
```

### N

**np.where()**
Vectorized conditional assignment. Returns value x where condition is True, value y where False.
```python
df['status'] = np.where(df['balance'] > 0, 'active', 'inactive')
```

**np.select()**
Multi-condition vectorized assignment. Takes a list of conditions and choices, with an optional default.
```python
conditions = [df['score'] >= 90, df['score'] >= 80]
choices = ['A', 'B']
df['grade'] = np.select(conditions, choices, default='C')
```

### P

**pct_change()**
Calculates the percentage change between the current and prior element. Returns NaN for the first row.
```python
df['growth'] = df['revenue'].pct_change()
```

**pd.cut()**
Bins continuous data into equal-width intervals. Labels can be assigned to each bin.
```python
df['age_group'] = pd.cut(df['age'], bins=[0,18,35,60,100],
                          labels=['Minor','Young','Middle','Senior'])
```

**pd.qcut()**
Bins continuous data into equal-frequency intervals (quantiles). Each bin has roughly the same number of observations.
```python
df['income_quartile'] = pd.qcut(df['income'], q=4, labels=['Q1','Q2','Q3','Q4'])
```

### R

**rank()**
Assigns ranks to values. `ascending=False` gives highest value rank 1.
```python
df['sales_rank'] = df['sales'].rank(ascending=False, method='min')
```

**rolling()**
Provides rolling window calculations. Must specify `window` size.
```python
df['ma_7'] = df['sales'].rolling(window=7).mean()
df['ma_30'] = df['sales'].rolling(window=30).mean()
```

### S

**str Accessor**
Provides string manipulation methods for Series with object dtype.
```python
df['domain'] = df['email'].str.split('@').str[1]
df['initial'] = df['name'].str[0]
```

### T

**to_period()**
Converts datetime to a Period (e.g., monthly period). Useful for grouping by time periods.
```python
df['month_period'] = df['date'].dt.to_period('M')
```

---

## Code Examples

### Example 1: Feature Engineering Pipeline

```python
import pandas as pd
import numpy as np

df = pd.read_csv('transactions.csv')
df['date'] = pd.to_datetime(df['date'])

# Create multiple derived columns at once
df = df.assign(
    # Revenue features
    profit=lambda x: x['revenue'] - x['cost'],
    margin_pct=lambda x: ((x['profit'] / x['revenue']) * 100).round(2),
    revenue_log=lambda x: np.log1p(x['revenue']),

    # Date features
    year=lambda x: x['date'].dt.year,
    month=lambda x: x['date'].dt.month,
    quarter=lambda x: x['date'].dt.quarter,
    is_weekend=lambda x: x['date'].dt.dayofweek >= 5,

    # Categorical bins
    revenue_tier=lambda x: pd.cut(
        x['revenue'],
        bins=[0, 1000, 5000, 10000, float('inf')],
        labels=['Small', 'Medium', 'Large', 'Enterprise']
    ),

    # Conditional flags
    is_high_margin=lambda x: x['margin_pct'] > 30,
    is_large=lambda x: x['revenue'] > 5000
)

print(df[['revenue', 'profit', 'margin_pct', 'revenue_tier', 'is_high_margin']])
```

### Example 2: String Feature Extraction

```python
df = pd.DataFrame({
    'url': [
        'https://shop.com/products/electronics/phone-123',
        'https://shop.com/products/clothing/shirt-456',
        'https://shop.com/products/electronics/laptop-789'
    ]
})

df = df.assign(
    domain=lambda x: x['url'].str.extract(r'//([^/]+)'),
    category=lambda x: x['url'].str.extract(r'/products/([^/]+)'),
    product_id=lambda x: x['url'].str.extract(r'-(\d+)$'),
    domain_length=lambda x: x['domain'].str.len(),
    is_electronics=lambda x: x['category'] == 'electronics'
)

print(df[['domain', 'category', 'product_id', 'is_electronics']])
```

### Example 3: Rolling Features

```python
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=30),
    'sales': np.random.randint(50, 200, 30)
})

df = df.assign(
    rolling_3d_avg=lambda x: x['sales'].rolling(3).mean(),
    rolling_7d_avg=lambda x: x['sales'].rolling(7).mean(),
    rolling_3d_std=lambda x: x['sales'].rolling(3).std(),
    cumulative=lambda x: x['sales'].cumsum(),
    pct_change=lambda x: x['sales'].pct_change(),
    is_above_avg=lambda x: x['sales'] > x['sales'].expanding().mean()
)

print(df[['date', 'sales', 'rolling_7d_avg', 'cumulative']].tail(10))
```

---

## Related Terms

| Term | Related To | Connection |
|------|-----------|------------|
| `np.where()` | `np.select()` | Single vs. multi-condition |
| `pd.cut()` | `pd.qcut()` | Equal-width vs. equal-frequency bins |
| `assign()` | `df['col'] = val` | Chainable vs. in-place creation |
| `.dt` accessor | `to_datetime()` | Datetime extraction after conversion |
| `.str` accessor | `str.strip()`, `str.split()` | String manipulation |
| `apply()` | Vectorized ops | Flexible but slower alternative |
| `rolling()` | `expanding()` | Window vs. cumulative calculations |

---

*See also: [Lecture 14](14-data-new-column-lecture.md) | [Lecture 15 – Statistics](15-statistics-lecture.md)*
