# Glossary 15: Statistics

## Quick Reference

| Method / Function | Purpose | Returns |
|-------------------|---------|---------|
| `df.mean()` | Arithmetic average | Scalar or Series |
| `df.median()` | Middle value | Scalar or Series |
| `df.mode()` | Most frequent value | Series |
| `df.std()` | Standard deviation (sample) | Scalar or Series |
| `df.var()` | Variance | Scalar or Series |
| `df.min()` / `df.max()` | Minimum / Maximum | Scalar or Series |
| `df.quantile(q)` | q-th percentile | Scalar or Series |
| `df.describe()` | Full statistical summary | DataFrame |
| `df.skew()` | Distribution skewness | Scalar or Series |
| `df.kurtosis()` | Distribution kurtosis | Scalar or Series |
| `df.sem()` | Standard error of mean | Scalar or Series |
| `df.corr()` | Correlation matrix | DataFrame |
| `df.cov()` | Covariance matrix | DataFrame |
| `df.groupby().agg()` | Group-level statistics | DataFrame |
| `df.expanding()` | Expanding window | Expanding object |
| `df.rolling(n)` | Rolling window | Rolling object |

---

## Alphabetical Definitions

### C

**Coefficient of Variation (CV)**
Normalized measure of spread: `std / mean`. Useful for comparing variability across datasets with different scales.
```python
cv = df['salary'].std() / df['salary'].mean()
```

**count()**
Returns the number of non-null values. Essential for understanding sample size behind statistics.
```python
df['score'].count()  # Excludes NaN
```

**corr()**
Computes pairwise correlation between numeric columns. Default is Pearson. Also supports Spearman and Kendall.
```python
df[['price', 'quantity', 'revenue']].corr()
df[['x', 'y']].corr(method='spearman')
```

**cov()**
Computes covariance between columns. Positive covariance means variables move together.
```python
df[['salary', 'bonus']].cov()
```

### D

**describe()**
Generates count, mean, std, min, 25%, 50%, 75%, max for numeric columns. Add `include='all'` for object columns too.
```python
df.describe()
df.describe(percentiles=[.05, .25, .5, .75, .95])
df.describe(include='all')
```

### E

**expanding()**
Creates an expanding (cumulative) window starting from the beginning. Unlike rolling, it grows with each observation.
```python
df['cumulative_mean'] = df['sales'].expanding().mean()
df['cumulative_std'] = df['sales'].expanding().std()
```

### K

**Kurtosis**
Measure of distribution tail heaviness relative to normal distribution. `kurtosis() = 0` is normal-like. Positive = heavy tails (more outliers). Negative = light tails.
```python
df['price'].kurtosis()
```

### M

**mean()**
Arithmetic average: sum of values divided by count. Sensitive to outliers.
```python
df['salary'].mean()  # sum / count
```

**median()**
Middle value when sorted. Robust to outliers. For even counts, returns the average of two middle values.
```python
df['salary'].median()
```

**mode()**
Most frequently occurring value. Can return multiple values if there are ties.
```python
df['color'].mode()  # Returns Series
df['color'].mode()[0]  # First mode
```

**mad()**
Mean absolute deviation from the mean. Robust alternative to standard deviation.
```python
df['salary'].mad()
```

### P

**percentile / quantile**
Value below which a given percentage of observations fall. `quantile(0.25)` = 25th percentile = Q1.
```python
df['salary'].quantile(0.25)  # 25th percentile
df['salary'].quantile(0.5)   # Same as median
df['salary'].quantile(0.75)  # 75th percentile = Q3
```

### Q

**Q1, Q2, Q3**
First quartile (25th percentile), second quartile (50th = median), third quartile (75th percentile). IQR = Q3 - Q1.
```python
Q1 = df['salary'].quantile(0.25)
Q3 = df['salary'].quantile(0.75)
IQR = Q3 - Q1
```

### R

**Range**
Difference between maximum and minimum values. Sensitive to outliers.
```python
salary_range = df['salary'].max() - df['salary'].min()
```

**rolling()**
Provides rolling window calculations. Requires `window` size. Does not include partial windows by default.
```python
df['ma_7'] = df['sales'].rolling(window=7).mean()
df['rolling_std'] = df['sales'].rolling(window=10).std()
```

### S

**sem()**
Standard error of the mean: `std / sqrt(n)`. Measures precision of the mean estimate.
```python
df['salary'].sem()
```

**Skewness**
Asymmetry of distribution. Positive = right tail longer. Negative = left tail longer. Zero = symmetric.
```python
df['income'].skew()  # Right-skewed income distributions are common
```

**std()**
Standard deviation. Uses `ddof=1` (sample) by default. Use `ddof=0` for population.
```python
df['salary'].std()      # Sample std (ddof=1)
df['salary'].std(ddof=0)  # Population std
```

### V

**var()**
Variance: square of standard deviation. Same `ddof` behavior as `std()`.
```python
df['salary'].var()       # Sample variance
df['salary'].var(ddof=0) # Population variance
```

---

## Code Examples

### Example 1: Complete Statistical Profile

```python
import pandas as pd
import numpy as np

def statistical_profile(df):
    """Generate a comprehensive statistical profile for all numeric columns."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    stats = pd.DataFrame(index=numeric_cols)

    for col in numeric_cols:
        s = df[col].dropna()
        stats.loc[col, 'count'] = s.count()
        stats.loc[col, 'mean'] = s.mean()
        stats.loc[col, 'median'] = s.median()
        stats.loc[col, 'std'] = s.std()
        stats.loc[col, 'min'] = s.min()
        stats.loc[col, 'Q1'] = s.quantile(0.25)
        stats.loc[col, 'Q3'] = s.quantile(0.75)
        stats.loc[col, 'max'] = s.max()
        stats.loc[col, 'IQR'] = s.quantile(0.75) - s.quantile(0.25)
        stats.loc[col, 'skewness'] = s.skew()
        stats.loc[col, 'kurtosis'] = s.kurtosis()
        stats.loc[col, 'CV'] = s.std() / s.mean() if s.mean() != 0 else np.nan

    return stats.round(3)

# Usage
profile = statistical_profile(df)
print(profile)
```

### Example 2: Group Comparison

```python
import seaborn as sns

df = sns.load_dataset('titanic')

# Compare survival statistics by class
result = df.groupby('class').agg(
    survival_rate=('survived', 'mean'),
    avg_fare=('fare', 'mean'),
    median_fare=('fare', 'median'),
    fare_std=('fare', 'std'),
    count=('survived', 'count'),
    min_age=('age', 'min'),
    max_age=('age', 'max')
).round(3)

print(result)
```

### Example 3: Rolling Window Analysis

```python
# Simulated daily stock data
np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=90)
prices = pd.Series(np.cumsum(np.random.randn(90) * 2) + 100, index=dates)

analysis = pd.DataFrame({
    'price': prices,
    'daily_return': prices.pct_change(),
    'ma_7': prices.rolling(7).mean(),
    'ma_30': prices.rolling(30).mean(),
    'volatility_7d': prices.pct_change().rolling(7).std(),
    'volatility_30d': prices.pct_change().rolling(30).std(),
    'cumulative_return': (1 + prices.pct_change()).cumprod() - 1
})

print(analysis.tail(10))
```

---

## Related Terms

| Term | Related To | Connection |
|------|-----------|------------|
| `mean()` vs `median()` | Skewness | Large gap indicates skew |
| `std()` vs `var()` | Spread | Variance = std² |
| `ddof` | `std()`, `var()` | 0=population, 1=sample |
| `quantile()` | `describe()` | Q1/Q2/Q3 are quantiles |
| `skew()` | `kurtosis()` | Both describe shape |
| `rolling()` | `expanding()` | Fixed vs growing window |
| `corr()` | `cov()` | Correlation is normalized covariance |

---

*See also: [Lecture 15](15-statistics-lecture.md) | [Lecture 23 – Correlation](23-corr-lecture.md)*
