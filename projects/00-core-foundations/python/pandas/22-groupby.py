"""
GroupBy
W3Schools: https://www.w3schools.com/python/pandas_dataframe_groupby.asp

GroupBy splits data into groups, applies a function independently to each
group, and combines the results. This is one of Pandas' most powerful features.
"""
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

np.random.seed(42)
df = pd.DataFrame({
    "Department": np.random.choice(["Engineering", "Marketing", "Sales", "HR"], 50),
    "Employee": [f"Emp_{i}" for i in range(1, 51)],
    "Salary": np.random.randint(50000, 120000, 50),
    "Years": np.random.randint(1, 15, 50),
    "Performance": np.random.randint(60, 100, 50),
})

print("Sample DataFrame (first 10 rows):")
print(df.head(10))
print(f"Shape: {df.shape}")
print()

# ---------------------------------------------------------------------------
# Example 1: Basic GroupBy – single aggregation
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: Basic GroupBy – Mean")
print("=" * 60)

mean_salary = df.groupby("Department")["Salary"].mean()
print("Mean salary by department:")
print(mean_salary.round(0))
print()

# ---------------------------------------------------------------------------
# Example 2: Multiple aggregations
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: Multiple Aggregations with agg()")
print("=" * 60)

dept_stats = df.groupby("Department").agg(
    count=("Employee", "size"),
    avg_salary=("Salary", "mean"),
    max_salary=("Salary", "max"),
    avg_years=("Years", "mean"),
    avg_performance=("Performance", "mean"),
).round(0)

print("Department statistics:")
print(dept_stats)
print()

# ---------------------------------------------------------------------------
# Example 3: Multiple columns groupby
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: GroupBy Multiple Columns")
print("=" * 60)

# Create a seniority column
df["Seniority"] = df["Years"].apply(
    lambda y: "Senior" if y >= 5 else "Junior"
)

grouped = df.groupby(["Department", "Seniority"]).agg(
    count=("Employee", "size"),
    avg_salary=("Salary", "mean"),
).round(0)

print("By Department and Seniority:")
print(grouped)
print()

# Unstack for pivot-like view
print("Unstacked view:")
print(grouped.unstack())
print()

# ---------------------------------------------------------------------------
# Example 4: Custom aggregation functions
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: Custom Aggregation Functions")
print("=" * 60)

def salary_range(s):
    """Calculate the range of salaries."""
    return s.max() - s.min()

custom_stats = df.groupby("Department").agg(
    count=("Salary", "size"),
    mean=("Salary", "mean"),
    median=("Salary", "median"),
    std=("Salary", "std"),
    salary_range=("Salary", salary_range),
    pct_high_performer=("Performance", lambda x: (x >= 90).mean() * 100),
).round(0)

print("Custom aggregations by department:")
print(custom_stats)
print()

# ---------------------------------------------------------------------------
# Example 5: Transform and filter
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 5: Transform and Filter")
print("=" * 60)

# Transform: add department mean salary as a new column
df["Dept_Avg_Salary"] = df.groupby("Department")["Salary"].transform("mean")
df["Above_Avg"] = df["Salary"] > df["Dept_Avg_Salary"]

print("With department average comparison:")
print(df[["Employee", "Department", "Salary", "Dept_Avg_Salary", "Above_Avg"]].head(10))
print()

# Filter: keep only departments with average salary > 75000
filtered = df.groupby("Department").filter(lambda x: x["Salary"].mean() > 75000)
print(f"Departments with avg salary > 75k: {filtered['Department'].unique()}")
print(f"Filtered rows: {len(filtered)}")
print()

# ---------------------------------------------------------------------------
# Example 6: GetGroup
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 6: get_group()")
print("=" * 60)

eng_group = df.groupby("Department").get_group("Engineering")
print("Engineering department:")
print(eng_group[["Employee", "Salary", "Years"]].head())
print()

print("Done!")
