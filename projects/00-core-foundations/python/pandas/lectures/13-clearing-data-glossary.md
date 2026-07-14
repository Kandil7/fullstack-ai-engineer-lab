# Glossary 13: Clearing Data

## Quick Reference

| Method / Function | Purpose | Returns |
|-------------------|---------|---------|
| `df.isnull()` | Detect missing values | Boolean DataFrame |
| `df.isnull().sum()` | Count missing per column | Series |
| `df.notnull()` | Detect non-missing values | Boolean DataFrame |
| `df.dropna()` | Remove rows with missing values | DataFrame |
| `df.fillna(value)` | Replace missing values | DataFrame |
| `df.ffill()` | Forward-fill missing values | DataFrame |
| `df.bfill()` | Backward-fill missing values | DataFrame |
| `df.interpolate()` | Estimate missing values | DataFrame |
| `df.duplicated()` | Detect duplicate rows | Boolean Series |
| `df.drop_duplicates()` | Remove duplicate rows | DataFrame |
| `pd.to_numeric()` | Convert to numeric type | Series |
| `pd.to_datetime()` | Convert to datetime type | Series |
| `df.replace()` | Replace specific values | DataFrame |
| `df.rename()` | Rename columns or index | DataFrame |
| `df.astype()` | Cast to specified dtype | DataFrame/Series |
| `df.info()` | Column types and null counts | None (prints) |
| `df.describe()` | Summary statistics | DataFrame |

---

## Alphabetical Definitions

### B

**Backward Fill (`bfill`)**
Fills missing values with the next valid observation. Useful for time series where future values can represent current state.
```python
df['price'] = df['price'].bfill()
```

### C

**Coerce (errors='coerce')**
A parameter in `to_numeric()` and `to_datetime()` that converts unparseable values to NaN instead of raising an error.
```python
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
```

### D

**Data Type Mismatch**
When a column contains values of inconsistent types (e.g., numbers stored as strings mixed with actual numbers). Detected with `df[col].apply(type).value_counts()`.

**DataFrame.info()**
Prints column names, non-null counts, dtypes, and memory usage. The first tool to run on any new dataset.
```python
df.info()
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 1000 entries, 0 to 999
# Data columns (total 5 columns):
#  #   Column    Non-Null Count  Dtype
# ---  ------    --------------  -----
#  0   name      995 non-null    object
```

**describe(include='all')**
Generates statistics for all columns including object (string) columns, showing unique counts, top values, and frequency.
```python
df.describe(include='all')
```

**Duplicate Rows**
Rows that are identical across all columns, or identical across a subset of key columns. Detected with `df.duplicated()`.
```python
# Exact duplicates
df.duplicated().sum()

# Duplicates on specific keys
df.duplicated(subset=['email'])
```

### F

**Fill Value**
A replacement value used with `fillna()` to substitute missing data. Can be a scalar, dictionary, or Series.
```python
df.fillna({'price': 0, 'name': 'Unknown', 'score': df['score'].mean()})
```

**Forward Fill (`ffill`)**
Propagates the last valid observation forward to fill gaps. Common in time series data.
```python
df['temperature'] = df['temperature'].ffill()
```

### I

**IQR (Interquartile Range)**
The range between the 25th and 75th percentiles. Used to detect outliers: values below Q1−1.5×IQR or above Q3+1.5×IQR are outliers.
```python
Q1 = df['price'].quantile(0.25)
Q3 = df['price'].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df['price'] < Q1 - 1.5*IQR) | (df['price'] > Q3 + 1.5*IQR)]
```

**Interpolation**
Estimates missing values based on surrounding data. Linear interpolation draws a straight line between known points.
```python
df['stock'] = df['stock'].interpolate(method='linear')
```

### M

**Missing Value**
A cell with no data, represented as `np.nan` (float), `None` (Python null), `pd.NaT` (datetime), or placeholder strings like `"N/A"`.
```python
df.isnull().sum()  # Count per column
```

### N

**NaN (Not a Number)**
Pandas' default representation for missing numeric values. `np.nan` is a float, so it forces float dtype in integer columns.

**Non-Destructive Cleaning**
Working on a copy of the DataFrame to preserve the original data.
```python
df_clean = df.copy()
df_clean = df_clean.dropna()
# Original df unchanged
```

### P

**Placeholder Values**
Strings like "N/A", "-", "unknown", or empty strings that represent missing data but are not actual NaN. Must be replaced with NaN before using `fillna()` or `dropna()`.
```python
df = df.replace(['N/A', '-', '', 'unknown'], np.nan)
```

**Pipeline (Cleaning)**
A sequence of data cleaning steps wrapped in a reusable function. Ensures consistency and reproducibility.
```python
def clean_data(df):
    df = df.replace(['N/A', ''], np.nan)
    df = df.dropna(subset=['id'])
    df = df.drop_duplicates()
    return df
```

### R

**rename()**
Changes column names or index labels. Accepts a dictionary mapping old names to new names.
```python
df = df.rename(columns={'old': 'new', 'Price ($)': 'price_usd'})
```

**replace()**
Substitutes specific values throughout the DataFrame. Useful for converting placeholder strings to NaN.
```python
df = df.replace({'N/A': np.nan, '-': np.nan})
```

### S

**String Cleaning**
Operations on text columns: stripping whitespace, normalizing case, removing special characters. Done with the `.str` accessor.
```python
df['name'] = df['name'].str.strip().str.title()
```

**strip()**
Removes leading and trailing whitespace from string values.
```python
df['name'] = df['name'].str.strip()
```

### T

**Type Conversion (astype)**
Changes the dtype of a column. Use `pd.to_numeric()` or `pd.to_datetime()` for safer conversion with error handling.
```python
df['quantity'] = df['quantity'].astype(int)          # Direct cast
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')  # Safe cast
```

### Z

**Z-Score**
Number of standard deviations from the mean. Values with |z| > 3 are commonly considered outliers.
```python
from scipy import stats
z = np.abs(stats.zscore(df['price']))
df_clean = df[z < 3]
```

---

## Code Examples

### Example 1: Complete Cleaning Workflow

```python
import pandas as pd
import numpy as np

# Load messy data
df = pd.read_csv('messy_data.csv')

# Step 1: Replace placeholders
df = df.replace(['N/A', 'n/a', '-', '', 'unknown'], np.nan)

# Step 2: Inspect
print("Missing values:\n", df.isnull().sum())

# Step 3: Drop rows missing critical fields
df = df.dropna(subset=['id', 'date'])

# Step 4: Fill remaining
df['category'] = df['category'].fillna('Other')
df['price'] = df['price'].fillna(df['price'].median())

# Step 5: Fix types
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Step 6: Remove duplicates
df = df.drop_duplicates()

# Step 7: Clean strings
for col in df.select_dtypes(include='object'):
    df[col] = df[col].str.strip().str.title()

# Step 8: Validate
print("\nAfter cleaning:")
df.info()
print(df.describe())
```

### Example 2: Outlier Detection

```python
def flag_outliers(df, columns, method='iqr', threshold=1.5):
    """Add boolean columns flagging outliers."""
    for col in columns:
        if method == 'iqr':
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            df[f'{col}_outlier'] = (df[col] < Q1 - threshold*IQR) | \
                                    (df[col] > Q3 + threshold*IQR)
        elif method == 'zscore':
            from scipy import stats
            z = np.abs(stats.zscore(df[col].dropna()))
            df[f'{col}_outlier'] = False
            df.loc[df[col].notna(), f'{col}_outlier'] = z > threshold
    return df

df = flag_outliers(df, ['price', 'quantity'], method='iqr')
print(df[['price', 'price_outlier']].query('price_outlier == True'))
```

---

## Related Terms

| Term | Related To | Connection |
|------|-----------|------------|
| `NaN` | `isnull()`, `fillna()` | The missing value marker pandas uses |
| `astype()` | `to_numeric()`, `to_datetime()` | Type conversion methods |
| `str.strip()` | `str.lower()`, `str.replace()` | String accessor methods |
| `IQR` | `quantile()`, `describe()` | Outlier detection metric |
| `ffill` / `bfill` | `interpolate()` | Missing value filling strategies |
| `dropna` | `drop_duplicates()` | Row removal operations |
| `coerce` | `errors` parameter | Safe type conversion strategy |

---

*See also: [Lecture 13](13-clearing-data-lecture.md) | [Lecture 14 – New Columns](14-data-new-column-lecture.md)*
