"""
Pandas Categorical Data: Categorical, get_dummies, factorize
=============================================================

Working with categorical data efficiently in pandas.
"""

import pandas as pd
import numpy as np

np.random.seed(42)

# =============================================================================
# 1. CATEGORICAL DTYPE BASICS
# =============================================================================

print("=" * 60)
print("1. CATEGORICAL DTYPE BASICS")
print("=" * 60)

# Create categorical
s = pd.Series(['low', 'medium', 'high', 'low', 'high', 'medium'])
cat_s = s.astype('category')

print("Original:", s.tolist())
print("Categorical:")
print(cat_s)
print(f"Categories: {cat_s.cat.categories.tolist()}")
print(f"Codes: {cat_s.cat.codes.tolist()}")
print(f"Dtype: {cat_s.dtype}")
print()

# Memory savings
large_s = pd.Series(np.random.choice(['A', 'B', 'C', 'D'], 100000))
large_cat = large_s.astype('category')
print(f"String series memory: {large_s.memory_usage(deep=True) / 1024:.1f} KB")
print(f"Categorical memory: {large_cat.memory_usage(deep=True) / 1024:.1f} KB")
print()

# =============================================================================
# 2. ORDERED CATEGORIES
# =============================================================================

print("=" * 60)
print("2. ORDERED CATEGORIES")
print("=" * 60)

# Ordered categorical
ordered_cat = pd.Categorical(
    ['low', 'medium', 'high', 'low', 'high'],
    categories=['low', 'medium', 'high'],
    ordered=True
)

print("Ordered categorical:")
print(ordered_cat)
print(f"Categories: {ordered_cat.categories.tolist()}")
print(f"Ordered: {ordered_cat.ordered}")
print()

# Comparisons work with ordered
print("Comparison (ordered):")
print(ordered_cat > 'low')
print(ordered_cat[ordered_cat > 'low'])
print()

# Sorting respects order
df = pd.DataFrame({'priority': ordered_cat})
print("Sorted by ordered category:")
print(df.sort_values('priority'))
print()

# =============================================================================
# 3. CATEGORY OPERATIONS
# =============================================================================

print("=" * 60)
print("3. CATEGORY OPERATIONS")
print("=" * 60)

cat = pd.Categorical(['a', 'b', 'c', 'a', 'b', 'a'], categories=['a', 'b', 'c', 'd'])
print(f"Categories: {cat.categories.tolist()}")
print(f"Codes: {cat.codes.tolist()}")
print()

# Rename categories
cat_renamed = cat.rename_categories({'a': 'alpha', 'b': 'beta', 'c': 'gamma', 'd': 'delta'})
print(f"Renamed: {cat_renamed.categories.tolist()}")
print()

# Add categories
cat_added = cat.add_categories(['e', 'f'])
print(f"Added categories: {cat_added.categories.tolist()}")
print()

# Remove categories
cat_removed = cat_remove = cat.remove_categories(['c', 'd'])
print(f"Removed categories: {cat_removed.categories.tolist()}")
print()

# Reorder categories
cat_reordered = cat.reorder_categories(['c', 'b', 'a', 'd'])
print(f"Reordered: {cat_reordered.categories.tolist()}")
print()

# Set categories (can add/remove/reorder in one step)
cat_set = cat.set_categories(['a', 'b', 'c', 'd', 'e'])
print(f"Set categories: {cat_set.categories.tolist()}")
print()

# =============================================================================
# 4. WORKING WITH CATEGORICAL IN DATAFRAMES
# =============================================================================

print("=" * 60)
print("4. CATEGORICAL IN DATAFRAMES")
print("=" * 60)

df = pd.DataFrame({
    'product': ['A', 'B', 'A', 'C', 'B', 'A'],
    'region': ['North', 'South', 'North', 'East', 'South', 'West'],
    'sales': [100, 200, 150, 300, 250, 120],
    'quarter': ['Q1', 'Q1', 'Q2', 'Q2', 'Q3', 'Q3']
})

# Convert to categorical
df['product'] = df['product'].astype('category')
df['region'] = df['region'].astype('category')
df['quarter'] = pd.Categorical(df['quarter'], categories=['Q1', 'Q2', 'Q3', 'Q4'], ordered=True)

print("DataFrame with categoricals:")
print(df)
print(f"\nDtypes:\n{df.dtypes}")
print()

# GroupBy with categorical (preserves categories)
grouped = df.groupby('product')['sales'].sum()
print("GroupBy preserves categories:")
print(grouped)
print()

# Pivot table with categorical
pivot = pd.pivot_table(df, values='sales', index='product', columns='quarter', aggfunc='sum')
print("Pivot table (Q4 shows as NaN since no data):")
print(pivot)
print()

# =============================================================================
# 5. ONE-HOT ENCODING (GET_DUMMIES)
# =============================================================================

print("=" * 60)
print("5. ONE-HOT ENCODING - GET_DUMMIES")
print("=" * 60)

# Simple get_dummies
data = pd.Series(['a', 'b', 'c', 'a', 'b'])
dummies = pd.get_dummies(data)
print("Basic get_dummies:")
print(dummies)
print()

# With prefix
dummies_prefixed = pd.get_dummies(data, prefix='cat')
print("With prefix:")
print(dummies_prefixed)
print()

# DataFrame get_dummies
df_demo = pd.DataFrame({
    'color': ['red', 'blue', 'green', 'red'],
    'size': ['S', 'M', 'L', 'M'],
    'value': [10, 20, 30, 40]
})

dummies_df = pd.get_dummies(df_demo, columns=['color', 'size'])
print("DataFrame get_dummies:")
print(dummies_df)
print()

# Drop first (avoid multicollinearity)
dummies_drop = pd.get_dummies(df_demo, columns=['color', 'size'], drop_first=True)
print("Drop first:")
print(dummies_drop)
print()

# Dummy NA
data_na = pd.Series(['a', 'b', None, 'a'])
dummies_na = pd.get_dummies(data_na, dummy_na=True)
print("With dummy_na=True:")
print(dummies_na)
print()

# =============================================================================
# 6. FACTORIZE
# =============================================================================

print("=" * 60)
print("6. FACTORIZE - ENCODE AS INTEGERS")
print("=" * 60)

data = pd.Series(['a', 'b', 'c', 'a', 'b', 'a'])
codes, uniques = pd.factorize(data)
print("Factorize:")
print(f"Codes: {codes}")
print(f"Uniques: {uniques.tolist()}")
print()

# With NA
data_na = pd.Series(['a', 'b', None, 'a'])
codes_na, uniques_na = pd.factorize(data_na, use_na_sentinel=True)
print("Factorize with NA:")
print(f"Codes: {codes_na} (-1 = NA)")
print(f"Uniques: {uniques_na.tolist()}")
print()

# Sort by frequency
codes_freq, uniques_freq = pd.factorize(data, sort=True)
print("Factorize sorted by frequency:")
print(f"Codes: {codes_freq}")
print(f"Uniques: {uniques_freq.tolist()}")
print()

# =============================================================================
# 7. ADVANCED CATEGORICAL TECHNIQUES
# =============================================================================

print("=" * 60)
print("7. ADVANCED TECHNIQUES")
print("=" * 60)

# Target encoding (mean encoding)
df_train = pd.DataFrame({
    'category': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C'],
    'target': [1, 0, 1, 0, 0, 1, 1, 1]
})

# Compute target mean per category
target_means = df_train.groupby('category')['target'].mean()
print("Target means:")
print(target_means)
print()

# Map to new data
df_test = pd.DataFrame({'category': ['A', 'B', 'C', 'D']})
df_test['target_encoded'] = df_test['category'].map(target_means)
print("Target encoding on test (D is unseen):")
print(df_test)
print()

# Handle unseen categories
df_test['target_encoded_filled'] = df_test['category'].map(target_means).fillna(target_means.mean())
print("With fallback to global mean:")
print(df_test)
print()

# Frequency encoding
freq_encoding = df_train['category'].value_counts() / len(df_train)
df_test['freq_encoded'] = df_test['category'].map(freq_encoding).fillna(0)
print("Frequency encoding:")
print(df_test)
print()

# =============================================================================
# 8. CATEGORICAL FOR ML
# =============================================================================

print("=" * 60)
print("8. CATEGORICAL FOR ML PIPELINES")
print("=" * 60)

from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
import pandas as pd

# Sample data
df_ml = pd.DataFrame({
    'color': ['red', 'blue', 'green', 'red', 'blue'],
    'size': ['S', 'M', 'L', 'M', 'S'],
    'material': ['cotton', 'wool', 'silk', 'cotton', 'wool'],
    'price': [10, 20, 30, 15, 25]
})

# Pandas approach: get_dummies
X_pandas = pd.get_dummies(df_ml[['color', 'size', 'material']], drop_first=True)
print("Pandas get_dummies for ML:")
print(X_pandas)
print()

# Sklearn approach (for pipelines)
categorical_cols = ['color', 'size', 'material']
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(drop='first', sparse_output=False), categorical_cols)
    ],
    remainder='passthrough'
)

X_sklearn = preprocessor.fit_transform(df_ml)
feature_names = preprocessor.get_feature_names_out()
print("Sklearn OneHotEncoder:")
print(pd.DataFrame(X_sklearn, columns=feature_names))
print()

# Ordinal encoding (for tree-based models)
ordinal = OrdinalEncoder(categories=[['S', 'M', 'L'], ['cotton', 'silk', 'wool'], ['blue', 'green', 'red']])
X_ordinal = ordinal.fit_transform(df_ml[['size', 'material', 'color']])
print("Ordinal encoding:")
print(pd.DataFrame(X_ordinal, columns=['size_ord', 'material_ord', 'color_ord']))
print()

print("=" * 60)
print("END OF CATEGORICAL DATA")
print("=" * 60)