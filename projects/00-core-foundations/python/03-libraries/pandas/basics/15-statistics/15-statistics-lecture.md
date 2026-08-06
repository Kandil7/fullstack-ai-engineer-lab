# Lecture 15: Statistics in Pandas

## Learning Objectives

By the end of this lecture, you will be able to:
- Calculate and interpret measures of central tendency
- Compute measures of spread and variability
- Use `describe()` for quick statistical summaries
- Calculate percentiles and quantiles
- Perform grouped statistical analysis
- Understand skewness and kurtosis
- Apply statistical functions to rolling windows

---

## 1. Why Statistics in Pandas?

Statistics transforms raw numbers into actionable insights. Before building models or creating charts, you must understand your data numerically:

- **What is typical?** (central tendency)
- **How spread out is it?** (variability)
- **Are there unusual values?** (distribution shape)
- **How do groups compare?** (grouped statistics)

Pandas provides built-in statistical methods that work directly on DataFrames.

---

## 2. Central Tendency

### 2.1 Mean (Average)

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'department': ['Sales', 'Sales', 'Engineering', 'Engineering', 'HR', 'HR'],
    'salary': [55000, 62000, 95000, 105000, 58000, 61000],
    'bonus': [5000, 6000, 12000, 15000, 4000, 4500]
})

# Column mean
print(f"Average salary: ${df['salary'].mean():,.2f}")
# Average salary: $72,666.67

# Mean of all numeric columns
print(df.mean(numeric_only=True))
```

### 2.2 Median (Middle Value)

```python
# Median — resistant to outliers
print(f"Median salary: ${df['salary'].median():,.2f}")
# Median salary: $59,500.00

# Why median matters — with an outlier
df_with_outlier = df.copy()
df_with_outlier.loc[5, 'salary'] = 500000
print(f"Mean with outlier:   ${df_with_outlier['salary'].mean():,.2f}")
print(f"Median with outlier: ${df_with_outlier['salary'].median():,.2f}")
# Mean with outlier:   $130,333.33
# Median with outlier: $59,500.00
```

### 2.3 Mode (Most Frequent)

```python
scores = pd.Series([85, 90, 90, 95, 85, 85, 100, 90])
print(f"Mode: {scores.mode().tolist()}")
# Mode: [85, 90] — can be multiple values
```

---

## 3. Measures of Spread

### 3.1 Standard Deviation

```python
# How much values deviate from the mean
print(f"Std dev of salary: ${df['salary'].std():,.2f}")
# Std dev of salary: $22,228.11

# Population std dev (ddof=0)
print(f"Population std: ${df['salary'].std(ddof=0):,.2f}")
```

### 3.2 Variance

```python
# Square of standard deviation
print(f"Variance: {df['salary'].var():,.2f}")
```

### 3.3 Range and IQR

```python
# Range
salary_range = df['salary'].max() - df['salary'].min()
print(f"Salary range: ${salary_range:,.2f}")

# Interquartile Range (IQR)
Q1 = df['salary'].quantile(0.25)
Q3 = df['salary'].quantile(0.75)
IQR = Q3 - Q1
print(f"IQR: ${IQR:,.2f}")
print(f"25th percentile: ${Q1:,.2f}")
print(f"75th percentile: ${Q3:,.2f}")
```

### 3.4 Coefficient of Variation

```python
# Normalized measure of spread (std / mean)
cv = df['salary'].std() / df['salary'].mean()
print(f"Coefficient of variation: {cv:.2%}")
```

---

## 4. The describe() Method

```python
# Comprehensive summary
print(df[['salary', 'bonus']].describe())

# Output:
#              salary         bonus
# count      6.000000      6.000000
# mean   72666.666667   7750.000000
# std    22228.113330   4378.926695
# min    55000.000000   4000.000000
# 25%    58750.000000   4375.000000
# 50%    59500.000000   5500.000000
# 75%    71250.000000  10500.000000
# max   105000.000000  15000.000000

# With percentiles
print(df['salary'].describe(percentiles=[.1, .25, .5, .75, .9, .95, .99]))
```

---

## 5. Percentiles and Quantiles

```python
# Specific percentiles
print(f"5th percentile:   ${df['salary'].quantile(0.05):,.2f}")
print(f"95th percentile:  ${df['salary'].quantile(0.95):,.2f}")
print(f"99th percentile:  ${df['salary'].quantile(0.99):,.2f}")

# Multiple quantiles at once
quantiles = df['salary'].quantile([0.1, 0.25, 0.5, 0.75, 0.9])
print(quantiles)
```

---

## 6. Skewness and Kurtosis

```python
# Skewness: asymmetry of distribution
# Positive = right tail, Negative = left tail, 0 = symmetric
print(f"Skewness: {df['salary'].skew():.2f}")

# Kurtosis: tail heaviness
# > 0 = heavy tails, < 0 = light tails, 0 = normal-like
print(f"Kurtosis: {df['salary'].kurtosis():.2f}")
```

---

## 7. Grouped Statistics

### 7.1 Basic GroupBy Statistics

```python
# Statistics per department
dept_stats = df.groupby('department')['salary'].agg([
    'count', 'mean', 'median', 'std', 'min', 'max'
])
print(dept_stats)

# Output:
#              count          mean   median           std     min     max
# department
# Engineering      2  100000.00000  100000   7071.06781   95000  105000
# HR               2   59500.00000   59500    2121.32034   58000   61000
# Sales            2   58500.00000   58500    4949.74747   55000   62000
```

### 7.2 Multiple Aggregations

```python
# Different aggregations per column
result = df.groupby('department').agg({
    'salary': ['mean', 'std', 'min', 'max'],
    'bonus': ['mean', 'sum', 'count']
})
print(result)
```

### 7.3 Named Aggregations (Pandas 0.25+)

```python
result = df.groupby('department').agg(
    avg_salary=('salary', 'mean'),
    salary_range=('salary', lambda x: x.max() - x.min()),
    total_bonus=('bonus', 'sum'),
    headcount=('salary', 'count')
).reset_index()
print(result)
```

### 7.4 Statistical Functions on Groups

```python
# Which department has highest salary variance?
print(df.groupby('department')['salary'].var())

# Which department has highest bonus-to-salary ratio?
df['bonus_ratio'] = df['bonus'] / df['salary']
print(df.groupby('department')['bonus_ratio'].mean())
```

---

## 8. Correlation Basics

```python
# Correlation matrix
corr_matrix = df[['salary', 'bonus']].corr()
print(corr_matrix)

# Correlation of one column with all others
print(df.corr(numeric_only=True)['salary'])

# Spearman correlation (rank-based)
print(df[['salary', 'bonus']].corr(method='spearman'))
```

---

## 9. Expanding Window Statistics

```python
# Cumulative statistics
df_timeseries = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=10),
    'sales': [100, 120, 115, 130, 125, 140, 135, 150, 145, 160]
})

# Expanding mean (cumulative average)
df_timeseries['expanding_mean'] = df_timeseries['sales'].expanding().mean()

# Expanding std
df_timeseries['expanding_std'] = df_timeseries['sales'].expanding().std()

# Rolling statistics
df_timeseries['rolling_3d_mean'] = df_timeseries['sales'].rolling(3).mean()
df_timeseries['rolling_5d_max'] = df_timeseries['sales'].rolling(5).max()
```

---

## 10. Common Statistical Functions Reference

| Function | Description | Sensitive to Outliers? |
|----------|-------------|----------------------|
| `mean()` | Arithmetic average | Yes |
| `median()` | Middle value | No |
| `mode()` | Most frequent value | No |
| `std()` | Standard deviation | Yes |
| `var()` | Variance | Yes |
| `min()` / `max()` | Extremes | Yes |
| `quantile(q)` | q-th percentile | No |
| `skew()` | Distribution asymmetry | Yes |
| `kurt()` | Tail heaviness | Yes |
| `sem()` | Standard error of mean | Yes |
| `mad()` | Mean absolute deviation | Yes |

---

## 11. Common Mistakes

1. **Using mean for skewed data** — If data is heavily skewed, median is more representative.
2. **Ignoring NaN behavior** — Most functions skip NaN by default. Use `skipna=False` to count them.
3. **Population vs. sample** — `std()` uses `ddof=1` (sample). Use `std(ddof=0)` for population.
4. **Correlation ≠ causation** — A high correlation does not imply one variable causes the other.
5. **Aggregating without groupby** — `df.mean()` collapses everything. Use `groupby()` first when comparing groups.

---

## 12. Best Practices

1. **Always check `describe()` first** — It reveals distribution shape, outliers, and missing data.
2. **Compare mean vs. median** — A large gap suggests skewness or outliers.
3. **Use named aggregations** — `agg(name=('col', 'func'))` produces clearer output.
4. **Visualize distributions** — Histograms complement numerical statistics.
5. **Report sample sizes** — A mean of 3 data points is less reliable than one from 3000.

---

## 13. Exercises

### Exercise 1: Salary Analysis
Calculate mean, median, std, and IQR for salaries by department. Which department has the most equal pay?

### Exercise 2: Rolling Statistics
Given daily stock prices, compute 7-day and 30-day rolling means and standard deviations.

### Exercise 3: Statistical Summary
Write a function `column_summary(df)` that returns a DataFrame with count, mean, std, min, Q1, median, Q3, max, skewness, and kurtosis for each numeric column.

---

## 14. Summary

| Concept | Method | Interpretation |
|---------|--------|---------------|
| Central tendency | `mean()`, `median()`, `mode()` | What's typical |
| Spread | `std()`, `var()`, `quantile()` | How variable |
| Shape | `skew()`, `kurtosis()` | Distribution form |
| Comparison | `groupby().agg()` | Group differences |
| Cumulative | `expanding()`, `rolling()` | Trends over time |

**Key takeaway**: Statistics gives you the numbers; interpretation gives you the meaning. Always ask "what does this number tell me about my data?" before moving to visualization.

---

*Next: [16 – Scatter Plot](16-scatter-plot-lecture.md)*
