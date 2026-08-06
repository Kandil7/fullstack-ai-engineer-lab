# Lecture 04: Cleaning Data

## Topic Overview

Data cleaning (also called data cleansing or data wrangling) is the process of detecting and correcting (or removing) corrupt, inaccurate, incomplete, or irrelevant records from a dataset. Real-world data is messy — it contains missing values, duplicates, outliers, inconsistent formats, and scaling issues. This lecture covers all essential data cleaning techniques that prepare your data for machine learning.

Data scientists typically spend 60-80% of their time on data cleaning. Clean data is the foundation of reliable ML models — garbage in, garbage out.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Identify and handle missing values (drop, fill, impute)
2. Detect and remove duplicate rows
3. Apply Min-Max normalization to scale features
4. Apply StandardScaler for Z-score normalization
5. Detect and handle outliers using the IQR method
6. Apply log transformations for skewed data
7. Build a complete data cleaning pipeline
8. Choose appropriate scaling methods based on data characteristics

---

## Key Concepts

### 1. Missing Values

Missing data is one of the most common data quality issues. Values may be missing due to:
- Data entry errors
- Sensor failures
- Survey non-responses
- Merging datasets with different fields

**Detection:**
```python
df.isnull().sum()           # Count missing per column
df.isnull().sum().sum()     # Total missing
df.isnull().mean() * 100    # Percentage missing
```

**Handling Strategies:**

| Strategy | When to Use | Pros | Cons |
|----------|-------------|------|------|
| **Drop rows** | Few missing values | Simple | Loses data |
| **Drop columns** | Many missing in one column | Preserves rows | Loses features |
| **Mean/Median imputation** | Numerical, no outliers | Preserves distribution | Reduces variance |
| **Mode imputation** | Categorical data | Preserves categories | May create bias |
| **Forward/Back fill** | Time series data | Preserves temporal pattern | May propagate errors |

### 2. Duplicates

Duplicate rows can bias ML models by giving disproportionate weight to certain observations.

```python
df.duplicated()           # Boolean mask of duplicates
df.duplicated().sum()     # Count of duplicates
df.drop_duplicates()      # Remove duplicates
```

### 3. Data Normalization

Different features often have different scales:
- Age: 0-100
- Salary: 20,000-200,000
- Square feet: 500-5,000

Without normalization, algorithms like k-NN, SVM, and gradient descent will be biased toward features with larger scales.

**Min-Max Normalization (0-1 scaling):**
```
X_normalized = (X - X_min) / (X_max - X_min)
```

**Standardization (Z-score):**
```
X_standardized = (X - mean) / std
```

### 4. Outlier Detection

Outliers are data points that significantly differ from other observations. They can:
- Skew statistical measures
- Mislead model training
- Dominate distance-based algorithms

**IQR Method:**
```
IQR = Q3 - Q1
Lower bound = Q1 - 1.5 × IQR
Upper bound = Q3 + 1.5 × IQR
```

### 5. Feature Scaling

Different algorithms have different requirements:

| Algorithm | Needs Scaling? | Why |
|-----------|---------------|-----|
| k-NN | Yes | Distance-based |
| SVM | Yes | Distance-based |
| Linear Regression | Optional | Coefficients interpret scale |
| Decision Trees | No | Split-based, scale-invariant |
| Random Forest | No | Split-based |
| Neural Networks | Yes | Gradient-based optimization |

---

## Code Examples

### Example 1: Detecting Missing Values

```python
import numpy as np
import pandas as pd

data = {
    'age': [25, 30, np.nan, 45, 50],
    'salary': [50000, 60000, 75000, np.nan, 90000],
    'experience': [2, 5, 8, 12, np.nan]
}
df = pd.DataFrame(data)

print("Missing values per column:")
print(df.isnull().sum())
print(f"\nTotal missing: {df.isnull().sum().sum()}")
print(f"\nMissing percentage:")
print(df.isnull().mean() * 100)
```

### Example 2: Handling Missing Values

```python
# Option 1: Drop rows with any missing values
df_dropped = df.dropna()
print("After dropping rows:")
print(df_dropped)

# Option 2: Fill with column mean (numerical data)
df_mean = df.fillna(df.mean())
print("\nFilled with means:")
print(df_mean)

# Option 3: Fill with specific value
df_zero = df.fillna(0)
print("\nFilled with zeros:")
print(df_zero)

# Option 4: Fill with median (robust to outliers)
df_median = df.fillna(df.median())
print("\nFilled with medians:")
print(df_median)
```

### Example 3: Removing Duplicates

```python
data = {
    'name': ['Alice', 'Bob', 'Alice', 'Charlie', 'Bob'],
    'age': [25, 30, 25, 35, 30],
    'salary': [50000, 60000, 50000, 70000, 60000]
}
df = pd.DataFrame(data)

print("Original data:")
print(df)

# Find duplicates
duplicates = df.duplicated()
print(f"\nDuplicate rows: {duplicates.sum()}")

# Remove duplicates
df_unique = df.drop_duplicates()
print("\nAfter removing duplicates:")
print(df_unique)
```

### Example 4: Min-Max Normalization

```python
from sklearn.preprocessing import MinMaxScaler

data = np.array([[25, 50000], [30, 60000], [35, 75000], [40, 90000]])
print("Original data:")
print(data)

scaler = MinMaxScaler()
normalized = scaler.fit_transform(data)
print("\nNormalized (0-1 range):")
print(normalized)
```

**Explanation:**
- `fit_transform()` computes min/max and applies transformation
- Each feature is scaled independently to [0, 1]
- Formula: `new_val = (val - min) / (max - min)`

### Example 5: StandardScaler (Z-score)

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
standardized = scaler.fit_transform(data)
print("Standardized (mean=0, std=1):")
print(standardized)
print(f"\nMean: {standardized.mean(axis=0)}")  # ≈ [0, 0]
print(f"Std: {standardized.std(axis=0)}")       # ≈ [1, 1]
```

**Explanation:**
- `fit_transform()` computes mean/std and applies transformation
- Each feature has mean=0 and std=1
- Formula: `new_val = (val - mean) / std`

### Example 6: Outlier Detection (IQR Method)

```python
np.random.seed(42)
data = np.random.randn(100)
data = np.append(data, [10, -10])  # Add obvious outliers

Q1 = np.percentile(data, 25)
Q3 = np.percentile(data, 75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = data[(data < lower_bound) | (data > upper_bound)]
print(f"Q1: {Q1:.2f}, Q3: {Q3:.2f}, IQR: {IQR:.2f}")
print(f"Bounds: [{lower_bound:.2f}, {upper_bound:.2f}]")
print(f"Outliers detected: {len(outliers)}")
print(f"Outlier values: {outliers}")
```

### Example 7: Log Transformation

```python
data = np.array([1, 10, 100, 1000, 10000])
log_data = np.log10(data)

print("Original (skewed):", data)
print("Log-transformed:", log_data)
# [0, 1, 2, 3, 4] — much more uniform
```

**Explanation:**
- Log transformation compresses large values and spreads small values
- Useful for right-skewed data (income, population, etc.)
- `np.log10()` for base-10 log, `np.log()` for natural log

### Example 8: Complete Cleaning Pipeline

```python
from sklearn.preprocessing import StandardScaler

# Create dirty data
np.random.seed(42)
df_dirty = pd.DataFrame({
    'age': [25, 30, np.nan, 45, 50, 25, 30],
    'salary': [50000, 60000, 75000, np.nan, 90000, 50000, 60000],
    'experience': [2, 5, 8, 12, np.nan, 2, 5]
})

print("Original dirty data:")
print(df_dirty)

# Step 1: Remove duplicates
df_clean = df_dirty.drop_duplicates()
print("\nAfter removing duplicates:")
print(df_clean)

# Step 2: Fill missing values
df_clean = df_clean.fillna(df_clean.mean())
print("\nAfter filling missing values:")
print(df_clean)

# Step 3: Scale features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(df_clean)
print("\nAfter standardization:")
print(features_scaled)
```

---

## Common Mistakes to Avoid

1. **Filling missing values before train/test split** — Causes data leakage
2. **Using mean imputation with outliers** — Mean is sensitive to outliers
3. **Scaling test data with test statistics** — Use training statistics only
4. **Not checking for duplicates** — Can bias model training
5. **Removing too many rows** — May lose valuable information
6. **Ignoring missing data mechanism** — MCAR, MAR, MNAR require different approaches
7. **Not documenting cleaning steps** — Makes results non-reproducible

---

## Best Practices

1. **Always explore first** — Understand your data before cleaning
2. **Split before preprocessing** — Prevent data leakage
3. **Use pipelines** — Automate and document cleaning steps
4. **Choose imputation strategy based on data** — Mean for normal, median for skewed
5. **Keep original data** — Always maintain a copy before cleaning
6. **Validate after cleaning** — Check that cleaning didn't introduce new issues
7. **Document everything** — Record what you changed and why

---

## Practice Exercises

### Exercise 1: Missing Values
Create a DataFrame with 10 rows and 3 columns, where each column has a different number of missing values. Calculate the percentage missing for each column.

### Exercise 2: Duplicates
Create a DataFrame with 5 duplicate rows out of 15 total. Remove duplicates and verify the result.

### Exercise 3: Normalization
Apply both Min-Max and StandardScaler to a dataset with features in different ranges. Compare the results.

### Exercise 4: Outliers
Generate 100 random data points with 5 outliers. Use the IQR method to detect them. What percentage are outliers?

### Exercise 5: Pipeline
Write a function that takes a dirty DataFrame and returns a clean, scaled version. Test it on data with missing values, duplicates, and different scales.

---

## Summary

| Technique | Purpose | When to Use |
|-----------|---------|-------------|
| **Drop rows** | Remove incomplete data | Few missing values |
| **Fill with mean/median** | Impute missing values | Numerical data |
| **Fill with mode** | Impute missing values | Categorical data |
| **Drop duplicates** | Remove redundant data | Duplicate rows exist |
| **Min-Max scaling** | Normalize to [0,1] | Need bounded values |
| **StandardScaler** | Normalize to N(0,1) | Normally distributed data |
| **IQR method** | Detect outliers | Data with extreme values |
| **Log transform** | Reduce skewness | Right-skewed data |

**Key Takeaway:** Data cleaning is the most time-consuming but critical step in ML. Always handle missing values, remove duplicates, scale features appropriately, and detect outliers before training any model.

---

## Next Lecture

In [Lecture 05: Linear Regression](05-linear-regression-lecture.md), we'll learn the fundamentals of linear regression — finding the best fit line and making predictions.
