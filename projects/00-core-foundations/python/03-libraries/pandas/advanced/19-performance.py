"""
Pandas Performance: Optimization, memory, best practices
=========================================================

Techniques for writing fast, memory-efficient pandas code.
"""

import pandas as pd
import numpy as np
import time
import sys
import io

np.random.seed(42)

# =============================================================================
# 1. MEMORY OPTIMIZATION
# =============================================================================

print("=" * 60)
print("1. MEMORY OPTIMIZATION")
print("=" * 60)

# Create a sample DataFrame
df = pd.DataFrame({
    'id': range(100000),
    'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], 100000),
    'subcategory': np.random.choice(['X', 'Y', 'Z'], 100000),
    'value1': np.random.randn(100000),
    'value2': np.random.randn(100000),
    'value3': np.random.randint(0, 1000, 100000),
    'flag': np.random.choice([True, False], 100000),
    'date': pd.date_range('2020-01-01', periods=100000, freq='min')
})

print("Original memory usage:")
print(df.memory_usage(deep=True))
print(f"Total: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
print()

# Optimize function
def optimize_dtypes(df):
    """Optimize DataFrame dtypes for memory efficiency."""
    df_opt = df.copy()
    
    for col in df_opt.columns:
        col_type = df_opt[col].dtype
        
        # Object -> Category (if low cardinality)
        if col_type == 'object':
            unique_ratio = df_opt[col].nunique() / len(df_opt[col])
            if unique_ratio < 0.5:
                df_opt[col] = df_opt[col].astype('category')
        
        # Int64 -> smaller int
        elif col_type == 'int64':
            col_min = df_opt[col].min()
            col_max = df_opt[col].max()
            if col_min >= 0:
                if col_max < 255:
                    df_opt[col] = df_opt[col].astype('uint8')
                elif col_max < 65535:
                    df_opt[col] = df_opt[col].astype('uint16')
                elif col_max < 4294967295:
                    df_opt[col] = df_opt[col].astype('uint32')
            else:
                if col_min > -128 and col_max < 127:
                    df_opt[col] = df_opt[col].astype('int8')
                elif col_min > -32768 and col_max < 32767:
                    df_opt[col] = df_opt[col].astype('int16')
                elif col_min > -2147483648 and col_max < 2147483647:
                    df_opt[col] = df_opt[col].astype('int32')
        
        # Float64 -> Float32
        elif col_type == 'float64':
            df_opt[col] = df_opt[col].astype('float32')
        
        # Bool -> uint8
        elif col_type == 'bool':
            df_opt[col] = df_opt[col].astype('uint8')
    
    return df_opt

df_opt = optimize_dtypes(df)

print("Optimized memory usage:")
print(df_opt.memory_usage(deep=True))
print(f"Total: {df_opt.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
print()

print("Dtype comparison:")
for col in df.columns:
    print(f"  {col}: {df[col].dtype} -> {df_opt[col].dtype}")
print()

# =============================================================================
# 2. VECTORIZATION VS APPLY
# =============================================================================

print("=" * 60)
print("2. VECTORIZATION VS APPLY")
print("=" * 60)

# Create test data
perf_df = pd.DataFrame({
    'A': np.random.randn(100000),
    'B': np.random.randn(100000),
    'C': np.random.randn(100000)
})

# Method 1: apply (slow)
start = time.time()
result_apply = perf_df.apply(lambda row: row['A'] + row['B'] * row['C'], axis=1)
time_apply = time.time() - start

# Method 2: vectorized (fast)
start = time.time()
result_vec = perf_df['A'] + perf_df['B'] * perf_df['C']
time_vec = time.time() - start

# Method 3: eval (fast for complex expressions)
start = time.time()
result_eval = perf_df.eval('A + B * C')
time_eval = time.time() - start

print(f"apply(axis=1):     {time_apply:.4f}s")
print(f"Vectorized:        {time_vec:.4f}s")
print(f"eval():            {time_eval:.4f}s")
print(f"Speedup (apply/vec): {time_apply/time_vec:.1f}x")
print()

# String operations
str_df = pd.DataFrame({'text': ['hello world'] * 100000})

start = time.time()
str_df['text'].apply(lambda x: x.upper())
time_apply_str = time.time() - start

start = time.time()
str_df['text'].str.upper()
time_vec_str = time.time() - start

print(f"String apply:   {time_apply_str:.4f}s")
print(f"String .str:    {time_vec_str:.4f}s")
print(f"Speedup: {time_apply_str/time_vec_str:.1f}x")
print()

# =============================================================================
# 3. QUERY & EVAL
# =============================================================================

print("=" * 60)
print("3. QUERY & EVAL")
print("=" * 60)

# Large DataFrame
big_df = pd.DataFrame({
    'A': np.random.randn(1000000),
    'B': np.random.randn(1000000),
    'C': np.random.randn(1000000),
    'category': np.random.choice(['X', 'Y', 'Z', 'W'], 1000000)
})

# Boolean indexing
start = time.time()
mask = (big_df['A'] > 0) & (big_df['B'] < 0) & (big_df['category'].isin(['X', 'Y']))
result_bool = big_df[mask]
time_bool = time.time() - start

# Query
start = time.time()
result_query = big_df.query('A > 0 and B < 0 and category in ["X", "Y"]')
time_query = time.time() - start

print(f"Boolean indexing: {time_bool:.4f}s")
print(f"Query:            {time_query:.4f}s")
print(f"Results match: {len(result_bool) == len(result_query)}")
print()

# Eval for new columns
start = time.time()
big_df['D'] = big_df['A'] + big_df['B'] * big_df['C']
time_direct = time.time() - start

start = time.time()
big_df.eval('D = A + B * C', inplace=True)
time_eval = time.time() - start

print(f"Direct assignment: {time_direct:.4f}s")
print(f"Eval:              {time_eval:.4f}s")
print()

# =============================================================================
# 4. GROUPBY PERFORMANCE
# =============================================================================

print("=" * 60)
print("4. GROUPBY PERFORMANCE")
print("=" * 60)

# Use categorical for groupby keys
grp_df = pd.DataFrame({
    'group': np.random.choice(['A', 'B', 'C', 'D', 'E'], 1000000),
    'value': np.random.randn(1000000)
})

# String groupby
start = time.time()
grp_df.groupby('group')['value'].sum()
time_str = time.time() - start

# Categorical groupby
grp_df_cat = grp_df.copy()
grp_df_cat['group'] = grp_df_cat['group'].astype('category')
start = time.time()
grp_df_cat.groupby('group')['value'].sum()
time_cat = time.time() - start

print(f"String groupby:    {time_str:.4f}s")
print(f"Categorical groupby: {time_cat:.4f}s")
print(f"Speedup: {time_str/time_cat:.1f}x")
print()

# Avoid apply in groupby
grp_df2 = pd.DataFrame({
    'group': np.random.choice(['A', 'B', 'C'], 100000),
    'value1': np.random.randn(100000),
    'value2': np.random.randn(100000)
})

# Slow: apply
start = time.time()
grp_df2.groupby('group').apply(lambda x: x['value1'].sum() / x['value2'].sum())
time_apply = time.time() - start

# Fast: vectorized
start = time.time()
grp_df2.groupby('group')['value1'].sum() / grp_df2.groupby('group')['value2'].sum()
time_vec = time.time() - start

print(f"Groupby apply:     {time_apply:.4f}s")
print(f"Groupby vectorized: {time_vec:.4f}s")
print(f"Speedup: {time_apply/time_vec:.1f}x")
print()

# =============================================================================
# 5. MERGE PERFORMANCE
# =============================================================================

print("=" * 60)
print("5. MERGE PERFORMANCE")
print("=" * 60)

left = pd.DataFrame({
    'key': np.random.randint(0, 10000, 50000),
    'val1': np.random.randn(50000)
})

right = pd.DataFrame({
    'key': np.random.randint(0, 10000, 50000),
    'val2': np.random.randn(50000)
})

# Sort keys first
left_sorted = left.sort_values('key')
right_sorted = right.sort_values('key')

start = time.time()
pd.merge(left, right, on='key')
time_unsorted = time.time() - start

start = time.time()
pd.merge(left_sorted, right_sorted, on='key')
time_sorted = time.time() - start

print(f"Unsorted merge: {time_unsorted:.4f}s")
print(f"Sorted merge:   {time_sorted:.4f}s")
print()

# Categorical keys
left_cat = left.copy()
right_cat = right.copy()
left_cat['key'] = left_cat['key'].astype('category')
right_cat['key'] = right_cat['key'].astype('category')

start = time.time()
pd.merge(left_cat, right_cat, on='key')
time_cat = time.time() - start

print(f"Categorical merge: {time_cat:.4f}s")
print()

# =============================================================================
# 6. CHUNKED PROCESSING
# =============================================================================

print("=" * 60)
print("6. CHUNKED PROCESSING FOR LARGE FILES")
print("=" * 60)

# Create a large CSV in memory
large_csv_data = io.StringIO()
pd.DataFrame({
    'id': range(1000000),
    'value': np.random.randn(1000000),
    'category': np.random.choice(['A', 'B', 'C'], 1000000)
}).to_csv(large_csv_data, index=False)
large_csv_data.seek(0)

# Process in chunks
chunk_size = 100000
results = []

start = time.time()
for chunk in pd.read_csv(large_csv_data, chunksize=chunk_size):
    # Process each chunk
    chunk_result = chunk.groupby('category')['value'].agg(['sum', 'mean', 'count'])
    results.append(chunk_result)

# Combine results
final_result = pd.concat(results).groupby(level=0).sum()
time_chunked = time.time() - start

print(f"Chunked processing (1M rows, {chunk_size} chunks): {time_chunked:.4f}s")
print(f"Result:\n{final_result}")
print()

# =============================================================================
# 7. BEST PRACTICES SUMMARY
# =============================================================================

print("=" * 60)
print("7. PERFORMANCE BEST PRACTICES")
print("=" * 60)

practices = """
1. USE VECTORIZED OPERATIONS
   [OK] df['A'] + df['B']
   [X] df.apply(lambda x: x['A'] + x['B'], axis=1)

2. USE .STR, .DT ACCESSORS
   [OK] df['text'].str.upper()
   [X] df['text'].apply(str.upper)

3. USE QUERY/EVAL FOR COMPLEX FILTERS
   [OK] df.query('A > 0 and B < 10')
   [X] df[(df['A'] > 0) & (df['B'] < 10)]

4. OPTIMIZE DTYPES
   [OK] category for low-cardinality strings
   [OK] int32/float32 when precision allows
   [OK] uint8 for boolean flags

5. USE CATEGORICAL FOR GROUPBY/MERGE KEYS
   [OK] df['key'] = df['key'].astype('category')

6. AVOID CHAINED INDEXING
   [OK] df.loc[mask, 'col']
   [X] df[mask]['col']

7. SORT BEFORE MERGE/GROUPBY ON INDEX
   [OK] df.sort_index().loc[key]

8. USE CHUNKED READING FOR LARGE FILES
   [OK] pd.read_csv('big.csv', chunksize=100000)

9. USE EVAL FOR COMPLEX EXPRESSIONS
   [OK] df.eval('D = A + B * C')

10. AVOID ITERATING ROWS
    [X] for idx, row in df.iterrows()
    [OK] df.apply() or vectorized
"""

print(practices)

# =============================================================================
# 8. PROFILING TOOLS
# =============================================================================

print("=" * 60)
print("8. PROFILING TOOLS")
print("=" * 60)

profiler_info = """
# Line-by-line profiling
pip install line_profiler
# @profile decorator on functions

# Memory profiling
pip install memory_profiler
# @profile decorator

# Pandas profiling
pip install pandas-profiling
# df.profile_report()

# Built-in
df.memory_usage(deep=True)
df.info(memory_usage='deep')

# Time operations
import time
start = time.time()
# operation
print(f"Time: {time.time() - start:.4f}s")

# IPython magic
%timeit df.groupby('key')['value'].sum()
%memit df = pd.read_csv('large.csv')
"""

print(profiler_info)

print("\n" + "=" * 60)
print("END OF PERFORMANCE")
print("=" * 60)