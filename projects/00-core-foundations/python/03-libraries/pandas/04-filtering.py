"""
Pandas Filtering: Advanced Query Techniques
============================================

Covers query(), complex boolean logic, string filtering, and performance tips.
"""

import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    'id': range(1, 101),
    'name': [f'User_{i}' for i in range(1, 101)],
    'age': np.random.randint(18, 70, 100),
    'salary': np.random.randint(30000, 200000, 100),
    'department': np.random.choice(['Eng', 'Sales', 'HR', 'Marketing', 'Finance', 'Ops'], 100),
    'city': np.random.choice(['NYC', 'SF', 'LA', 'Chicago', 'Austin', 'Seattle', 'Boston'], 100),
    'join_date': pd.date_range('2020-01-01', periods=100, freq='W'),
    'is_manager': np.random.choice([True, False], 100, p=[0.15, 0.85]),
    'performance_score': np.random.uniform(1.0, 5.0, 100).round(2),
    'skills': [','.join(np.random.choice(['Python', 'SQL', 'Java', 'AWS', 'Docker', 'K8s', 'React', 'ML'], 
                                           np.random.randint(1, 5), replace=False)) 
               for _ in range(100)]
})

print("DataFrame shape:", df.shape)
print(df.head())
print()

# =============================================================================
# 1. QUERY METHOD - SQL-LIKE SYNTAX
# =============================================================================

print("=" * 60)
print("1. QUERY METHOD")
print("=" * 60)

# Basic query
result = df.query('salary > 100000')
print(f"df.query('salary > 100000'): {len(result)} rows")
print(result.head())
print()

# Multiple conditions
result = df.query('salary > 100000 and department == "Eng"')
print(f"df.query('salary > 100000 and department == \"Eng\"'): {len(result)} rows")
print()

# Using variables with @
dept = 'Eng'
min_sal = 100000
result = df.query('salary > @min_sal and department == @dept')
print(f"Using @variables: {len(result)} rows")
print()

# String methods in query
result = df.query('city.str.startswith("S")')  # SF, Seattle
print(f"df.query('city.str.startswith(\"S\")'): {len(result)} rows")
print()

result = df.query('name.str.contains("User_1")')  # regex
print(f"df.query('name.str.contains(\"User_1\")'): {len(result)} rows")
print()

# In operator
result = df.query('department in ["Eng", "Sales", "Marketing"]')
print(f"df.query('department in [\"Eng\", \"Sales\", \"Marketing\"]'): {len(result)} rows")
print()

# Not in
result = df.query('department not in ["HR", "Finance"]')
print(f"df.query('department not in [\"HR\", \"Finance\"]'): {len(result)} rows")
print()

# Between
result = df.query('salary.between(80000, 120000)')
print(f"df.query('salary.between(80000, 120000)'): {len(result)} rows")
print()

# =============================================================================
# 2. BOOLEAN INDEXING WITH COMPLEX CONDITIONS
# =============================================================================

print("=" * 60)
print("2. COMPLEX BOOLEAN INDEXING")
print("=" * 60)

# Multiple conditions with &, |, ~
mask = (
    (df['salary'] > 100000) & 
    (df['department'].isin(['Eng', 'Sales'])) & 
    (df['age'] < 40) & 
    (~df['is_manager'])
)
result = df[mask]
print(f"Complex mask (salary>100k, Eng/Sales, age<40, not manager): {len(result)} rows")
print()

# Using eval for complex expressions (can be faster for large DataFrames)
result = df.eval('salary > 100000 and department in ["Eng", "Sales"] and age < 40 and not is_manager')
print(f"df.eval(...): {result.sum()} rows")
print()

# =============================================================================
# 3. STRING FILTERING
# =============================================================================

print("=" * 60)
print("3. STRING FILTERING (.str accessor)")
print("=" * 60)

# Contains (case insensitive)
result = df[df['city'].str.contains('s', case=False)]
print(f"Cities containing 's': {len(result)} rows")
print(result[['name', 'city']].head())
print()

# Startswith / Endswith
result = df[df['name'].str.startswith('User_1')]  # User_1, User_10-19
print(f"Names starting with 'User_1': {len(result)} rows")
print()

# Match regex
result = df[df['skills'].str.contains(r'\bPython\b')]  # word boundary
print(f"Has Python skill: {len(result)} rows")
print()

# Extract with regex
df['first_skill'] = df['skills'].str.extract(r'^([^,]+)')
print("Extracted first skill:")
print(df[['name', 'skills', 'first_skill']].head())
print()

# Split and expand
skills_expanded = df['skills'].str.split(',', expand=True)
skills_expanded.columns = [f'skill_{i+1}' for i in range(skills_expanded.shape[1])]
print("Split skills into columns:")
print(skills_expanded.head())
print()

# =============================================================================
# 4. DATETIME FILTERING
# =============================================================================

print("=" * 60)
print("4. DATETIME FILTERING")
print("=" * 60)

# Ensure datetime
df['join_date'] = pd.to_datetime(df['join_date'])

# Year, month, day accessors
result = df[df['join_date'].dt.year == 2020]
print(f"Joined in 2020: {len(result)} rows")
print()

result = df[df['join_date'].dt.month.isin([1, 2, 3])]  # Q1
print(f"Joined in Q1: {len(result)} rows")
print()

# Date range
start = '2020-06-01'
end = '2020-12-31'
result = df[df['join_date'].between(start, end)]
print(f"Joined between {start} and {end}: {len(result)} rows")
print()

# Relative dates (last N days)
cutoff = df['join_date'].max() - pd.Timedelta(days=90)
result = df[df['join_date'] >= cutoff]
print(f"Joined in last 90 days: {len(result)} rows")
print()

# =============================================================================
# 5. FILTERING WITH NAN VALUES
# =============================================================================

print("=" * 60)
print("5. HANDLING NaN IN FILTERS")
print("=" * 60)

# Add some NaN values
df_nan = df.copy()
df_nan.loc[0:5, 'performance_score'] = np.nan
df_nan.loc[10:12, 'city'] = np.nan

print("Rows with NaN in performance_score:")
print(df_nan[df_nan['performance_score'].isna()][['name', 'performance_score']])
print()

print("Rows WITHOUT NaN in performance_score:")
print(df_nan[df_nan['performance_score'].notna()].head())
print()

# Fillna then filter
result = df_nan.fillna({'performance_score': 0}).query('performance_score > 3')
print(f"After fillna(0), score > 3: {len(result)} rows")
print()

# Dropna then filter
result = df_nan.dropna(subset=['performance_score']).query('performance_score > 3')
print(f"After dropna, score > 3: {len(result)} rows")
print()

# =============================================================================
# 6. PERFORMANCE TIPS
# =============================================================================

print("=" * 60)
print("6. PERFORMANCE TIPS")
print("=" * 60)

import time

# Create larger DataFrame for timing
large_df = pd.DataFrame({
    'a': np.random.randn(1_000_000),
    'b': np.random.randn(1_000_000),
    'c': np.random.choice(['X', 'Y', 'Z'], 1_000_000),
    'd': np.random.randint(0, 100, 1_000_000)
})

# Method 1: Boolean indexing
start = time.time()
result1 = large_df[(large_df['a'] > 0) & (large_df['c'] == 'X')]
time1 = time.time() - start
print(f"Boolean indexing: {time1:.4f}s, {len(result1)} rows")

# Method 2: Query
start = time.time()
result2 = large_df.query('a > 0 and c == "X"')
time2 = time.time() - start
print(f"Query: {time2:.4f}s, {len(result2)} rows")

# Method 3: eval
start = time.time()
mask = large_df.eval('a > 0 and c == "X"')
result3 = large_df[mask]
time3 = time.time() - start
print(f"Eval + indexing: {time3:.4f}s, {len(result3)} rows")

# Method 4: NumPy where (fastest for simple conditions)
start = time.time()
mask = (large_df['a'].values > 0) & (large_df['c'].values == 'X')
result4 = large_df[mask]
time4 = time.time() - start
print(f"NumPy arrays: {time4:.4f}s, {len(result4)} rows")

print("\nNote: query/eval can be faster for complex expressions on large DataFrames")
print("due to optimized parsing and reduced intermediate copies.")

print("\n" + "=" * 60)
print("END OF FILTERING")
print("=" * 60)