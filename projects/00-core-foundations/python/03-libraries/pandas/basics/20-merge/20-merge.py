"""
Merge DataFrames
W3Schools: https://www.w3schools.com/python/pandas_dataframe_merge.asp

Merge combines DataFrames based on common columns or indices, similar
to SQL JOIN operations.
"""
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

employees = pd.DataFrame({
    "emp_id": [1, 2, 3, 4, 5],
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "dept_id": [101, 102, 101, 103, 102],
})

departments = pd.DataFrame({
    "dept_id": [101, 102, 103, 104],
    "dept_name": ["Engineering", "Marketing", "Sales", "HR"],
    "budget": [500000, 300000, 400000, 200000],
})

salaries = pd.DataFrame({
    "emp_id": [1, 2, 3, 6],
    "salary": [95000, 80000, 102000, 75000],
})

print("Employees:")
print(employees)
print()

print("Departments:")
print(departments)
print()

print("Salaries:")
print(salaries)
print()

# ---------------------------------------------------------------------------
# Example 1: Inner merge (default)
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: Inner Merge")
print("=" * 60)

inner = pd.merge(employees, departments, on="dept_id", how="inner")
print("Inner merge (employees + departments):")
print(inner)
print()
# Only rows with matching dept_id in both DataFrames
# Diana's dept 103 and HR (104) don't appear because HR has no employees

# ---------------------------------------------------------------------------
# Example 2: Left merge
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: Left Merge")
print("=" * 60)

left = pd.merge(employees, departments, on="dept_id", how="left")
print("Left merge (keep all employees):")
print(left)
print()
# All employees are kept; HR (dept 104) is excluded

# ---------------------------------------------------------------------------
# Example 3: Right merge
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: Right Merge")
print("=" * 60)

right = pd.merge(employees, departments, on="dept_id", how="right")
print("Right merge (keep all departments):")
print(right)
print()
# All departments are kept; HR shows NaN for missing employees

# ---------------------------------------------------------------------------
# Example 4: Outer merge
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: Outer Merge (Full Join)")
print("=" * 60)

outer = pd.merge(employees, departments, on="dept_id", how="outer")
print("Outer merge (keep everything):")
print(outer)
print()

# ---------------------------------------------------------------------------
# Example 5: Merge on different column names
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 5: Merge on Different Column Names")
print("=" * 60)

left_df = pd.DataFrame({
    "id": [1, 2, 3],
    "value": ["a", "b", "c"],
})
right_df = pd.DataFrame({
    "identifier": [2, 3, 4],
    "score": [10, 20, 30],
})

merged = pd.merge(left_df, right_df, left_on="id", right_on="identifier", how="inner")
print("Merge with different column names:")
print(merged)
print()

# ---------------------------------------------------------------------------
# Example 6: Merge with index
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 6: Merge on Index")
print("=" * 60)

df_a = pd.DataFrame({
    "A": [1, 2, 3],
    "B": ["x", "y", "z"],
}, index=["k1", "k2", "k3"])

df_b = pd.DataFrame({
    "C": [10, 20, 30],
    "D": ["a", "b", "c"],
}, index=["k2", "k3", "k4"])

merged_idx = pd.merge(df_a, df_b, left_index=True, right_index=True, how="outer")
print("Merge on index (outer):")
print(merged_idx)
print()

# ---------------------------------------------------------------------------
# Example 7: Merge employees + departments + salaries (multi-table)
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 7: Multi-Table Merge Chain")
print("=" * 60)

# Chain multiple merges
full = (
    employees
    .merge(departments, on="dept_id", how="left")
    .merge(salaries, on="emp_id", how="left")
)
print("Full employee info:")
print(full)
print()

# Check for employees without salary info
missing_salary = full[full["salary"].isna()]
if len(missing_salary) > 0:
    print("Employees without salary info:")
    print(missing_salary[["name", "dept_name"]])
    print()

print("Done!")
