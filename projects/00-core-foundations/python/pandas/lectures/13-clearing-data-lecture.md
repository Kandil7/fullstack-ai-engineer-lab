# Lecture 13: Clearing Data in Pandas

## Learning Objectives

By the end of this lecture, you will be able to:
- Identify and handle missing values (NaN, None, empty strings)
- Remove or fill duplicates from a DataFrame
- Fix data type mismatches and convert columns
- Rename columns and index values for consistency
- Detect and remove outliers
- Apply string cleaning operations to text columns
- Build a repeatable data cleaning pipeline

---

## 1. Why Data Cleaning Matters

Real-world data is messy. Surveys have incomplete responses, APIs return null fields, CSV exports contain trailing whitespace, and database exports mix types. **Data cleaning typically consumes 60–80% of a data scientist's time.**

The goal is not to make data perfect — it is to make it **consistent** and **analysis-ready**.

---

## 2. Inspecting Your Data

Before cleaning, understand what you have.

### 2.1 Basic Inspection

```python
import pandas as pd
import numpy as np

df = pd.read_csv('raw_sales.csv')

# Shape and structure
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
df.info()
df.head(10)
df.tail(5)
```

### 2.2 Statistical Summary

```python
# Numerical columns
df.describe()

# All columns including strings
df.describe(include='all')

# Unique values per column
for col in df.columns:
    print(f"{col}: {df[col].nunique()} unique values")
```

### 2.3 Identifying Missing Values

```python
# Total missing per column
print(df.isnull().sum())

# Percentage missing per column
print((df.isnull().sum() / len(df) * 100).round(2))

# Rows with ANY missing value
missing_rows = df[df.isnull().any(axis=1)]
print(f"Rows with missing data: {len(missing_rows)}")
```

---

## 3. Handling Missing Values

### 3.1 Types of Missing Data

| Type | Representation | Common Cause |
|------|---------------|--------------|
| NaN | `np.nan` | Numeric fields with no value |
| None | `None` | Python null |
| Empty string | `""` or `" "` | Form submissions |
| Placeholder | `"N/A"`, `"-"`, `"unknown"` | Data entry conventions |

### 3.2 Removing Missing Values

```python
# Drop rows with ANY missing value
df_clean = df.dropna()

# Drop rows where ALL values are missing
df_clean = df.dropna(how='all')

# Drop rows missing values in specific columns
df_clean = df.dropna(subset=['price', 'quantity'])

# Drop columns with more than 50% missing
threshold = len(df) * 0.5
df_clean = df.dropna(thresh=threshold, axis=1)
```

### 3.3 Filling Missing Values

```python
# Fill with a constant
df['category'] = df['category'].fillna('Unknown')

# Fill with mean/median/mode
df['price'] = df['price'].fillna(df['price'].median())
df['rating'] = df['rating'].fillna(df['rating'].mean())
df['status'] = df['status'].fillna(df['status'].mode()[0])

# Forward fill (useful for time series)
df['temperature'] = df['temperature'].ffill()

# Backward fill
df['temperature'] = df['temperature'].bfill()

# Interpolation (linear for numeric)
df['stock_price'] = df['stock_price'].interpolate(method='linear')

# Fill with different values per column
fill_values = {
    'price': df['price'].median(),
    'quantity': 0,
    'category': 'Unknown',
    'date': pd.NaT
}
df = df.fillna(fill_values)
```

### 3.4 Replace Placeholder Values

```python
# Replace common placeholders with actual NaN
placeholders = ['N/A', 'n/a', 'NA', '-', '--', 'unknown', 'UNKNOWN', '']
df = df.replace(placeholders, np.nan)

# Now handle NaN normally
df = df.dropna(subset=['critical_column'])
```

---

## 4. Removing Duplicates

### 4.1 Finding Duplicates

```python
# Exact row duplicates
print(f"Duplicate rows: {df.duplicated().sum()}")

# Show duplicates
df[df.duplicated(keep=False)]

# Duplicates based on specific columns
df.duplicated(subset=['order_id', 'product_id']).sum()
```

### 4.2 Removing Duplicates

```python
# Remove exact duplicates (keep first)
df = df.drop_duplicates()

# Remove duplicates based on specific columns
df = df.drop_duplicates(subset=['email'], keep='last')

# Remove all duplicates (keep none)
df = df.drop_duplicates(keep=False)
```

---

## 5. Fixing Data Types

### 5.1 Common Type Issues

```python
# Numeric stored as string
df['price'] = pd.to_numeric(df['price'], errors='coerce')  # Invalid becomes NaN

# Date stored as string
df['date'] = pd.to_datetime(df['date'], errors='coerce', format='%Y-%m-%d')

# Boolean stored as string
df['is_active'] = df['is_active'].map({'Yes': True, 'No': False, True: True, False: False})

# Category (saves memory)
df['region'] = df['region'].astype('category')
```

### 5.2 Handling Mixed Types

```python
# Check what's actually in a column
print(df['price'].apply(type).value_counts())

# Force conversion — bad values become NaN
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Log what was converted
bad_mask = df['price'].isna() & df['price_raw'].notna()
print(f"Converted {bad_mask.sum()} invalid values to NaN")
```

---

## 6. String Cleaning

### 6.1 Whitespace and Case

```python
# Strip leading/trailing whitespace
df['name'] = df['name'].str.strip()

# Normalize case
df['email'] = df['email'].str.lower()
df['name'] = df['name'].str.title()

# Remove extra spaces
df['address'] = df['address'].str.replace(r'\s+', ' ', regex=True)
```

### 6.2 Pattern Cleaning

```python
# Remove non-numeric characters from phone numbers
df['phone'] = df['phone'].str.replace(r'[^\d]', '', regex=True)

# Extract numbers from mixed strings
df['amount'] = df['amount_text'].str.extract(r'(\d+\.?\d*)').astype(float)

# Standardize email domains
df['email_domain'] = df['email'].str.split('@').str[1]
```

---

## 7. Renaming Columns

```python
# Rename specific columns
df = df.rename(columns={
    'old_name': 'new_name',
    'Price ($)': 'price_usd',
    'Date of Birth': 'birth_date'
})

# Clean all column names at once
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('[^a-z0-9_]', '', regex=True)

# Using a function
df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
```

---

## 8. Outlier Detection

### 8.1 IQR Method

```python
def remove_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return df[(df[column] >= lower) & (df[column] <= upper)]

df = remove_outliers_iqr(df, 'price')
```

### 8.2 Z-Score Method

```python
from scipy import stats

z_scores = np.abs(stats.zscore(df['price']))
df = df[z_scores < 3]  # Remove rows with z-score > 3
```

---

## 9. Building a Cleaning Pipeline

```python
def clean_sales_data(df):
    """Complete data cleaning pipeline."""
    df = df.copy()

    # 1. Replace placeholders
    df = df.replace(['N/A', 'n/a', '-', '', 'unknown'], np.nan)

    # 2. Strip strings
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.strip()

    # 3. Fix types
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0).astype(int)

    # 4. Fill missing
    df['category'] = df['category'].fillna('Uncategorized')
    df['price'] = df['price'].fillna(df['price'].median())

    # 5. Remove duplicates
    df = df.drop_duplicates(subset=['order_id'])

    # 6. Remove outliers
    Q1 = df['price'].quantile(0.25)
    Q3 = df['price'].quantile(0.75)
    IQR = Q3 - Q1
    df = df[(df['price'] >= Q1 - 1.5 * IQR) & (df['price'] <= Q3 + 1.5 * IQR)]

    # 7. Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    return df

clean_df = clean_sales_data(raw_df)
```

---

## 10. Common Mistakes

1. **Filling before understanding** — Always inspect missing patterns first. If 80% of a column is missing, dropping it is better than imputing.
2. **Using mean for skewed data** — Use median when data has outliers or is skewed.
3. **Dropping too aggressively** — `dropna()` on a large DataFrame may remove most of your data.
4. **Not preserving originals** — Always work on a copy: `df = raw_df.copy()`.
5. **Ignoring datetime parsing errors** — `errors='coerce'` silently converts bad dates to NaT. Log these.
6. **Cleaning after analysis** — Clean FIRST, then analyze. Dirty data produces wrong conclusions.

---

## 11. Best Practices

1. **Profile first** — Run `.info()`, `.describe()`, `.isnull().sum()` before any cleaning.
2. **Log every change** — Track what you removed or modified for reproducibility.
3. **Use `errors='coerce'`** — Safer than `errors='raise'` when converting types.
4. **Chain cleaning steps** — Build a reusable function or pipeline.
5. **Validate after cleaning** — Re-run `.info()` and `.describe()` to confirm.
6. **Keep raw data** — Never overwrite your source files.

---

## 12. Exercises

### Exercise 1: Basic Cleaning
Given this DataFrame, clean it completely:
```python
data = {
    'name': [' Alice ', 'BOB', 'charlie', None, 'Eve'],
    'age': ['25', 'thirty', '28', '22', '35'],
    'score': [88.5, None, 92.0, 76.5, None],
    'grade': ['A', 'B', 'N/A', 'A', 'B']
}
df = pd.DataFrame(data)
```

### Exercise 2: Pipeline
Write a function `clean_orders(df)` that:
- Removes rows with missing `order_id`
- Converts `amount` to numeric (coerce errors)
- Fills missing `status` with "pending"
- Removes exact duplicate rows

### Exercise 3: Outlier Removal
Load a dataset with a `price` column, identify outliers using IQR, and report how many rows were removed.

---

## 13. Summary

| Concept | Key Method | When to Use |
|---------|-----------|-------------|
| Missing values | `isnull()`, `fillna()`, `dropna()` | Always — first step in cleaning |
| Duplicates | `duplicated()`, `drop_duplicates()` | After identifying unique keys |
| Type conversion | `to_numeric()`, `to_datetime()` | When types don't match expectations |
| String cleaning | `.str.strip()`, `.str.lower()` | Before joins or grouping |
| Outlier removal | IQR or z-score | Before statistical analysis |
| Pipeline | Reusable function | Production and repeatable work |

**Key takeaway**: Data cleaning is not optional — it is the foundation of reliable analysis. Clean data leads to correct insights; dirty data leads to confident wrong answers.

---

*Next: [14 – Adding New Columns](14-data-new-column-lecture.md)*
