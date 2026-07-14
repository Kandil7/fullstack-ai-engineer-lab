"""
Pandas Statistics
W3Schools: https://www.w3schools.com/python/pandas_stat.asp

Pandas provides many built-in statistical functions for data analysis.
"""
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

np.random.seed(42)
n = 100

df = pd.DataFrame({
    "age": np.random.randint(18, 65, n),
    "income": np.random.normal(55000, 15000, n).round(2),
    "score": np.random.uniform(0, 100, n).round(1),
    "department": np.random.choice(["Engineering", "Marketing", "Sales", "HR"], n),
})

print("Sample DataFrame (first 5 rows):")
print(df.head())
print(f"Shape: {df.shape}")
print()

# ---------------------------------------------------------------------------
# Example 1: Basic aggregations
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: Basic Aggregations")
print("=" * 60)

print(f"Mean income:   ${df['income'].mean():,.2f}")
print(f"Median income: ${df['income'].median():,.2f}")
print(f"Std income:    ${df['income'].std():,.2f}")
print(f"Min income:    ${df['income'].min():,.2f}")
print(f"Max income:    ${df['income'].max():,.2f}")
print(f"Sum of ages:   {df['age'].sum()}")
print()

# ---------------------------------------------------------------------------
# Example 2: describe() – full summary statistics
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: describe()")
print("=" * 60)

print("Numeric columns:")
print(df.describe().round(2))
print()

# Specific percentiles
print("Custom percentiles:")
print(df["income"].describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9]).round(2))
print()

# ---------------------------------------------------------------------------
# Example 3: Aggregation by group
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: Aggregation by Group")
print("=" * 60)

# Mean by department
dept_stats = df.groupby("department")[["income", "score"]].mean().round(2)
print("Mean income and score by department:")
print(dept_stats)
print()

# Multiple aggregations
dept_agg = df.groupby("department").agg(
    count=("age", "size"),
    avg_age=("age", "mean"),
    avg_income=("income", "mean"),
    max_score=("score", "max"),
).round(2)
print("Multiple aggregations by department:")
print(dept_agg)
print()

# ---------------------------------------------------------------------------
# Example 4: Correlation
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: Correlation")
print("=" * 60)

numeric_cols = df[["age", "income", "score"]]
corr = numeric_cols.corr().round(3)
print("Correlation matrix:")
print(corr)
print()

# Correlation of income with other columns
print("Income correlations:")
print(df.corr(numeric_only=True)["income"].round(3))
print()

# ---------------------------------------------------------------------------
# Example 5: Rolling and cumulative statistics
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 5: Rolling and Cumulative Statistics")
print("=" * 60)

# Create a time series
dates = pd.date_range("2024-01-01", periods=20, freq="D")
ts = pd.DataFrame({
    "date": dates,
    "value": np.cumsum(np.random.randn(20)) + 100,
})
ts = ts.set_index("date")

print("Daily values:")
print(ts.head(10))
print()

# Rolling mean (7-day)
ts["rolling_7d"] = ts["value"].rolling(window=7).mean().round(2)
print("7-day rolling mean:")
print(ts[["value", "rolling_7d"]].dropna())
print()

# Cumulative sum
ts["cumulative"] = ts["value"].cumsum().round(2)
print("Cumulative sum:")
print(ts[["value", "cumulative"]].tail(5))
print()

# Percentage change
ts["pct_change"] = ts["value"].pct_change().round(4)
print("Percentage change:")
print(ts[["value", "pct_change"]].head(10))
print()

print("Done!")
