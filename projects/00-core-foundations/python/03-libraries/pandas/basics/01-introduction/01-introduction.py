"""
Pandas Introduction: Series & DataFrame Creation
=================================================

This module covers the fundamentals of creating pandas Series and DataFrames
from various data sources.
"""

import pandas as pd
import numpy as np

# =============================================================================
# 1. CREATING SERIES
# =============================================================================

print("=" * 60)
print("1. CREATING SERIES")
print("=" * 60)

# From a list
s1 = pd.Series([1, 3, 5, np.nan, 6, 8])
print("From list:")
print(s1)
print(f"Index: {s1.index.tolist()}")
print(f"Values: {s1.values}")
print(f"Type: {type(s1)}")
print()

# From a dictionary (keys become index)
s2 = pd.Series({'a': 1, 'b': 2, 'c': 3})
print("From dict:")
print(s2)
print()

# From scalar (broadcast to index)
s3 = pd.Series(5, index=[0, 1, 2, 3])
print("From scalar with index:")
print(s3)
print()

# With custom index
s4 = pd.Series([10, 20, 30], index=['x', 'y', 'z'])
print("With custom index:")
print(s4)
print(f"Access by label: s4['y'] = {s4['y']}")
print(f"Access by position: s4[1] = {s4[1]}")
print()

# =============================================================================
# 2. CREATING DATAFRAMES
# =============================================================================

print("=" * 60)
print("2. CREATING DATAFRAMES")
print("=" * 60)

# From dict of lists/arrays (columns)
df1 = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'age': [25, 30, 35, 28],
    'city': ['NYC', 'LA', 'Chicago', 'Houston'],
    'salary': [70000, 80000, 90000, 75000]
})
print("From dict of lists:")
print(df1)
print(f"Shape: {df1.shape}")
print(f"Columns: {df1.columns.tolist()}")
print(f"Dtypes:\n{df1.dtypes}")
print()

# From list of dicts (rows)
df2 = pd.DataFrame([
    {'name': 'Alice', 'age': 25, 'city': 'NYC'},
    {'name': 'Bob', 'age': 30, 'city': 'LA'},
    {'name': 'Charlie', 'age': 35, 'city': 'Chicago'},
])
print("From list of dicts:")
print(df2)
print()

# From 2D numpy array
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
df3 = pd.DataFrame(arr, columns=['A', 'B', 'C'], index=['x', 'y', 'z'])
print("From numpy array:")
print(df3)
print()

# From Series (each becomes a column)
s_a = pd.Series([1, 2, 3], name='A')
s_b = pd.Series([4, 5, 6], name='B')
df4 = pd.DataFrame({'A': s_a, 'B': s_b})
print("From Series:")
print(df4)
print()

# =============================================================================
# 3. READING FROM FILES (COMMON FORMATS)
# =============================================================================

print("=" * 60)
print("3. READING FROM FILES (examples)")
print("=" * 60)

# CSV
# df_csv = pd.read_csv('data.csv')

# JSON
# df_json = pd.read_json('data.json')

# Excel
# df_excel = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# Parquet (efficient columnar format)
# df_parquet = pd.read_parquet('data.parquet')

# SQL
# df_sql = pd.read_sql('SELECT * FROM users', connection)

print("""
Common read functions:
  pd.read_csv('file.csv')
  pd.read_json('file.json')
  pd.read_excel('file.xlsx')
  pd.read_parquet('file.parquet')
  pd.read_sql(query, connection)
  pd.read_html(url)          # HTML tables
  pd.read_clipboard()        # From clipboard
""")

# =============================================================================
# 4. BASIC INSPECTION
# =============================================================================

print("=" * 60)
print("4. BASIC INSPECTION")
print("=" * 60)

print("df1.head():")
print(df1.head())
print()

print("df1.tail(2):")
print(df1.tail(2))
print()

print("df1.info():")
df1.info()
print()

print("df1.describe():")
print(df1.describe())
print()

print("df1.describe(include='all'):")
print(df1.describe(include='all'))
print()

# =============================================================================
# 5. SERIES VS DATAFRAME OPERATIONS
# =============================================================================

print("=" * 60)
print("5. SERIES VS DATAFRAME")
print("=" * 60)

# Series is 1D, DataFrame is 2D
print(f"Series ndim: {s1.ndim}")
print(f"DataFrame ndim: {df1.ndim}")
print()

# Series has name, DataFrame has columns
print(f"Series name: {s1.name}")
s1.name = 'my_series'
print(f"After naming: {s1.name}")
print()

# DataFrame columns can be accessed as Series
print("df1['age'] is a Series:")
print(type(df1['age']))
print(df1['age'])
print()

# Multiple columns -> DataFrame
print("df1[['name', 'age']] is a DataFrame:")
print(type(df1[['name', 'age']]))
print(df1[['name', 'age']])

print("\n" + "=" * 60)
print("END OF INTRODUCTION")
print("=" * 60)