"""
Pandas Indexing & Selection: loc, iloc, boolean indexing
=========================================================

This module covers all methods for selecting and filtering data in pandas.
"""

import pandas as pd
import numpy as np

# Create sample data
np.random.seed(42)
df = pd.DataFrame({
    'id': range(1, 21),
    'name': [f'Employee_{i}' for i in range(1, 21)],
    'age': np.random.randint(22, 60, 20),
    'salary': np.random.randint(50000, 150000, 20),
    'department': np.random.choice(['Eng', 'Sales', 'HR', 'Marketing'], 20),
    'years_exp': np.random.randint(1, 20, 20),
    'is_remote': np.random.choice([True, False], 20),
    'bonus': np.random.randint(0, 20000, 20)
}, index=list('abcdefghijklmnopqrst'))  # Custom string index

print("Sample DataFrame:")
print(df)
print(f"\nIndex: {df.index.tolist()}")
print(f"Columns: {df.columns.tolist()}")
print()

# =============================================================================
# 1. LOC - LABEL-BASED INDEXING
# =============================================================================

print("=" * 60)
print("1. LOC - LABEL-BASED INDEXING")
print("=" * 60)

# Select row by label
print("df.loc['e'] (single row as Series):")
print(df.loc['e'])
print()

# Select multiple rows by label
print("df.loc[['a', 'e', 'j']] (multiple rows):")
print(df.loc[['a', 'e', 'j']])
print()

# Slice with labels (INCLUSIVE on both ends!)
print("df.loc['c':'h'] (inclusive slice):")
print(df.loc['c':'h'])
print()

# Select columns by label
print("df.loc[:, 'name'] (single column):")
print(df.loc[:, 'name'])
print()

print("df.loc[:, ['name', 'salary', 'department']] (multiple columns):")
print(df.loc[:, ['name', 'salary', 'department']])
print()

# Select rows AND columns
print("df.loc['c':'h', ['name', 'salary']] (rows + cols):")
print(df.loc['c':'h', ['name', 'salary']])
print()

# Boolean array with loc
print("df.loc[df['salary'] > 100000, ['name', 'salary']] (filter + select):")
print(df.loc[df['salary'] > 100000, ['name', 'salary']])
print()

# =============================================================================
# 2. ILOC - POSITION-BASED INDEXING
# =============================================================================

print("=" * 60)
print("2. ILOC - POSITION-BASED INDEXING")
print("=" * 60)

# Select row by integer position
print("df.iloc[0] (first row):")
print(df.iloc[0])
print()

print("df.iloc[-1] (last row):")
print(df.iloc[-1])
print()

# Multiple rows by position
print("df.iloc[[0, 4, 9]] (rows 0, 4, 9):")
print(df.iloc[[0, 4, 9]])
print()

# Slice by position (EXCLUSIVE end!)
print("df.iloc[2:6] (rows 2,3,4,5):")
print(df.iloc[2:6])
print()

# Select columns by position
print("df.iloc[:, 1] (2nd column - name):")
print(df.iloc[:, 1])
print()

print("df.iloc[:, [1, 3]] (columns at pos 1, 3):")
print(df.iloc[:, [1, 3]])
print()

# Rows AND columns by position
print("df.iloc[2:6, 1:4] (rows 2-5, cols 1-3):")
print(df.iloc[2:6, 1:4])
print()

# =============================================================================
# 3. DIRECT INDEXING (BRACKETS)
# =============================================================================

print("=" * 60)
print("3. DIRECT INDEXING []")
print("=" * 60)

# Single column -> Series
print("df['name'] (Series):")
print(type(df['name']))
print(df['name'].head())
print()

# Multiple columns -> DataFrame
print("df[['name', 'salary']] (DataFrame):")
print(type(df[['name', 'salary']]))
print(df[['name', 'salary']].head())
print()

# Row slice (by position!)
print("df[2:5] (rows 2,3,4 by POSITION):")
print(df[2:5])
print()

# =============================================================================
# 4. BOOLEAN INDEXING (MASKING)
# =============================================================================

print("=" * 60)
print("4. BOOLEAN INDEXING")
print("=" * 60)

# Simple condition
high_salary = df['salary'] > 100000
print("df['salary'] > 100000:")
print(high_salary.head(10))
print()

print("df[high_salary]:")
print(df[high_salary])
print()

# Multiple conditions (use &, |, ~ with parentheses!)
print("df[(df['salary'] > 100000) & (df['department'] == 'Eng')]:")
print(df[(df['salary'] > 100000) & (df['department'] == 'Eng')])
print()

print("df[(df['age'] > 40) | (df['years_exp'] > 15)]:")
print(df[(df['age'] > 40) | (df['years_exp'] > 15)])
print()

print("df[~(df['department'] == 'HR')] (NOT HR):")
print(df[~(df['department'] == 'HR')].head())
print()

# isin
print("df[df['department'].isin(['Eng', 'Sales'])]:")
print(df[df['department'].isin(['Eng', 'Sales'])])
print()

# between
print("df[df['salary'].between(80000, 120000)]:")
print(df[df['salary'].between(80000, 120000)])
print()

# =============================================================================
# 5. QUERY METHOD (SQL-LIKE)
# =============================================================================

print("=" * 60)
print("5. QUERY METHOD")
print("=" * 60)

print("df.query('salary > 100000 and department == \"Eng\"'):")
print(df.query('salary > 100000 and department == "Eng"'))
print()

# Use @ to reference variables
threshold = 100000
dept = 'Eng'
print(f"df.query('salary > @threshold and department == @dept'):")
print(df.query('salary > @threshold and department == @dept'))
print()

# =============================================================================
# 6. WHERE & MASK
# =============================================================================

print("=" * 60)
print("6. WHERE & MASK")
print("=" * 60)

# where - keep where True, NaN where False
print("df.where(df['salary'] > 100000):")
print(df.where(df['salary'] > 100000).head(10))
print()

# mask - opposite of where
print("df.mask(df['salary'] > 100000):")
print(df.mask(df['salary'] > 100000).head(10))
print()

# =============================================================================
# 7. LOOKUP BY INDEX/VALUES (DEPRECATED/REPLACED)
# =============================================================================

print("=" * 60)
print("7. AT & IAT (FAST SCALAR ACCESS)")
print("=" * 60)

# at - label-based scalar access
print(f"df.at['e', 'salary']: {df.at['e', 'salary']}")

# iat - position-based scalar access
print(f"df.iat[4, 3]: {df.iat[4, 3]}")  # row 4, col 3 (salary)

# =============================================================================
# 8. COMMON PITFALLS
# =============================================================================

print("=" * 60)
print("8. COMMON PITFALLS")
print("=" * 60)

# Chained indexing warning
# BAD: df['salary'][df['age'] > 40]  # May raise SettingWithCopyWarning
# GOOD: df.loc[df['age'] > 40, 'salary']

# Slice with loc is INCLUSIVE
# df.loc['a':'c'] includes 'c'
# df.iloc[0:3] excludes position 3

# Setting with enlargement
# NOTE: the list must match the FULL column count (8 cols), or pandas raises
# "cannot set a row with mismatched columns"
df.loc['z'] = [21, 'Zoe', 28, 95000, 'Eng', 5, True, 5000]
print("After df.loc['z'] = [...]:")
print(df.tail(3))

print("\n" + "=" * 60)
print("END OF INDEXING & SELECTION")
print("=" * 60)