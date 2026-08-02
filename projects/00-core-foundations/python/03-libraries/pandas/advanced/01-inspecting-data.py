"""
Pandas Data Inspection: head, info, describe, dtypes
=====================================================

This module covers essential methods for inspecting and understanding your data.
"""

import pandas as pd
import numpy as np

# Create sample data
np.random.seed(42)
df = pd.DataFrame({
    'id': range(1, 101),
    'name': [f'User_{i}' for i in range(1, 101)],
    'age': np.random.randint(18, 80, 100),
    'salary': np.random.normal(75000, 20000, 100).astype(int),
    'department': np.random.choice(['Engineering', 'Sales', 'Marketing', 'HR', 'Finance'], 100),
    'join_date': pd.date_range('2020-01-01', periods=100, freq='D'),
    'is_manager': np.random.choice([True, False], 100, p=[0.1, 0.9]),
    'performance_score': np.random.uniform(1, 5, 100).round(2),
    'bonus': np.where(np.random.random(100) > 0.7, np.random.randint(1000, 10000, 100), 0),
    'notes': np.random.choice(['', 'Top performer', 'Needs improvement', 'On leave'], 100, p=[0.7, 0.1, 0.1, 0.1])
})

# Introduce some missing values
df.loc[5:10, 'salary'] = np.nan
df.loc[15:20, 'performance_score'] = np.nan
df.loc[30, 'department'] = np.nan

print("=" * 60)
print("1. HEAD & TAIL")
print("=" * 60)

print("df.head() - First 5 rows:")
print(df.head())
print()

print("df.head(10) - First 10 rows:")
print(df.head(10))
print()

print("df.tail(3) - Last 3 rows:")
print(df.tail(3))
print()

print("=" * 60)
print("2. INFO - CONCISE SUMMARY")
print("=" * 60)

print("df.info():")
df.info()
print()

print("df.info(verbose=True, show_counts=True):")
df.info(verbose=True, show_counts=True)
print()

print("=" * 60)
print("3. DESCRIBE - STATISTICAL SUMMARY")
print("=" * 60)

print("df.describe() - Numeric columns only:")
print(df.describe())
print()

print("df.describe(include='all') - All columns:")
print(df.describe(include='all'))
print()

print("df.describe(include=[np.number]) - Only numeric:")
print(df.describe(include=[np.number]))
print()

print("df.describe(include=['object', 'bool']) - Categorical:")
print(df.describe(include=['object', 'bool']))
print()

# Percentiles
print("df.describe(percentiles=[0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]):")
print(df.describe(percentiles=[0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]))
print()

print("=" * 60)
print("4. DTYPES & MEMORY USAGE")
print("=" * 60)

print("df.dtypes:")
print(df.dtypes)
print()

print("df.memory_usage(deep=True):")
print(df.memory_usage(deep=True))
print()

print(f"Total memory: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
print()

print("=" * 60)
print("5. SHAPE, SIZE, NDIM")
print("=" * 60)

print(f"df.shape: {df.shape} (rows, columns)")
print(f"df.size: {df.size} (total elements)")
print(f"df.ndim: {df.ndim} (dimensions)")
print(f"len(df): {len(df)} (rows)")
print()

print("=" * 60)
print("6. COLUMNS & INDEX")
print("=" * 60)

print(f"df.columns: {df.columns.tolist()}")
print(f"df.index: {df.index.tolist()[:5]}... (first 5)")
print(f"df.columns.dtype: {df.columns.dtype}")
print(f"df.index.dtype: {df.index.dtype}")
print()

# Rename columns
df_renamed = df.rename(columns={'name': 'employee_name', 'salary': 'annual_salary'})
print("After rename:")
print(df_renamed.columns.tolist())
print()

# Set index
df_indexed = df.set_index('id')
print("After set_index('id'):")
print(df_indexed.head())
print(f"New index name: {df_indexed.index.name}")
print()

# Reset index
df_reset = df_indexed.reset_index()
print("After reset_index():")
print(df_reset.head())
print()

print("=" * 60)
print("7. UNIQUE VALUES & VALUE COUNTS")
print("=" * 60)

print("df['department'].unique():")
print(df['department'].unique())
print()

print("df['department'].nunique():", df['department'].nunique())
print()

print("df['department'].value_counts():")
print(df['department'].value_counts())
print()

print("df['department'].value_counts(normalize=True):")
print(df['department'].value_counts(normalize=True))
print()

print("df['is_manager'].value_counts():")
print(df['is_manager'].value_counts())
print()

print("=" * 60)
print("8. MISSING VALUES")
print("=" * 60)

print("df.isna().sum():")
print(df.isna().sum())
print()

print("df.isna().mean() * 100 (percent missing):")
print((df.isna().mean() * 100).round(2))
print()

print("df.notna().sum():")
print(df.notna().sum())
print()

# Rows with any missing
missing_rows = df[df.isna().any(axis=1)]
print(f"Rows with any missing: {len(missing_rows)}")
print(missing_rows[['id', 'salary', 'performance_score', 'department']])
print()

print("=" * 60)
print("9. SAMPLE & RANDOM ROWS")
print("=" * 60)

print("df.sample(5):")
print(df.sample(5))
print()

print("df.sample(frac=0.1, random_state=42):")
print(df.sample(frac=0.1, random_state=42))
print()

print("=" * 60)
print("10. QUICK CORRELATION (numeric only)")
print("=" * 60)

print("df.select_dtypes(include=[np.number]).corr():")
print(df.select_dtypes(include=[np.number]).corr().round(2))

print("\n" + "=" * 60)
print("END OF INSPECTION")
print("=" * 60)