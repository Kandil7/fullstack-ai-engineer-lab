# Glossary: Cleaning Data

## Quick Reference Table

| Term | Definition | Category |
|------|-----------|----------|
| Data Cleaning | Detecting and correcting corrupt data | Process |
| Missing Values | Data points that are absent or undefined | Problem |
| Duplicates | Identical rows in a dataset | Problem |
| Outliers | Data points far from others | Problem |
| Normalization | Scaling features to a fixed range | Technique |
| Standardization | Scaling features to mean=0, std=1 | Technique |
| Imputation | Replacing missing values | Technique |
| Mean Imputation | Filling missing with column mean | Technique |
| Median Imputation | Filling missing with column median | Technique |
| Min-Max Scaler | Scales to [0, 1] range | Tool |
| StandardScaler | Z-score normalization | Tool |
| RobustScaler | Outlier-resistant scaling | Tool |
| IQR | Interquartile Range (Q3 - Q1) | Metric |
| Skewness | Asymmetry of data distribution | Metric |
| Log Transform | Compress large values | Technique |
| Data Leakage | Test information leaking into training | Problem |
| Pipeline | Sequence of preprocessing steps | Tool |
| Fit | Compute statistics from data | Action |
| Transform | Apply transformation to data | Action |
| Fit-Transform | Fit and transform in one step | Action |

---

## Detailed Definitions

### C

#### Cleaning Pipeline
**Definition:** A sequence of data preprocessing steps that can be applied consistently to training and new data, ensuring reproducibility and preventing data leakage.

**Example:**
```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression

pipe = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler()),
    ('model', LinearRegression())
])

pipe.fit(X_train, y_train)
score = pipe.score(X_test, y_test)
```

**Related Terms:** Pipeline, fit, transform, Data Leakage

---

### D

#### Data Leakage
**Definition:** When information from outside the training dataset is used to create the model, leading to overly optimistic performance estimates that don't generalize to new data.

**Example:**
```python
# WRONG: Scaling before split (data leakage)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Uses ALL data statistics
X_train, X_test = train_test_split(X_scaled, test_size=0.2)

# CORRECT: Split first, then scale
X_train, X_test = train_test_split(X, test_size=0.2)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # Only training data
X_test_scaled = scaler.transform(X_test)         # Use training statistics
```

**Related Terms:** Train/Test Split, Fit, Transform, Preprocessing

---

### I

#### IQR (Interquartile Range)
**Definition:** The range between the first quartile (Q1, 25th percentile) and third quartile (Q3, 75th percentile). Used to detect outliers — values beyond Q1 - 1.5×IQR or Q3 + 1.5×IQR are considered outliers.

**Example:**
```python
import numpy as np

data = np.array([10, 12, 14, 15, 16, 18, 20, 100])
Q1 = np.percentile(data, 25)
Q3 = np.percentile(data, 75)
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers = data[(data < lower) | (data > upper)]
print(f"IQR: {IQR}, Bounds: [{lower}, {upper}]")
print(f"Outliers: {outliers}")  # [100]
```

**Related Terms:** Outliers, Quartiles, Median, Box Plot

#### Imputation
**Definition:** The process of replacing missing values with substituted values. Common strategies include mean, median, mode, or model-based imputation.

**Example:**
```python
import pandas as pd
import numpy as np

df = pd.DataFrame({'A': [1, np.nan, 3, np.nan, 5]})

# Mean imputation
df_mean = df.fillna(df.mean())

# Median imputation
df_median = df.fillna(df.median())

# Constant imputation
df_zero = df.fillna(0)

# Using sklearn
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='mean')
df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
```

**Related Terms:** Missing Values, Mean, Median, Mode, fillna

---

### L

#### Log Transformation
**Definition:** Applying the logarithm function to data to reduce skewness, compress large values, and make distributions more symmetric. Common for right-skewed data like income, population, or prices.

**Example:**
```python
import numpy as np

# Right-skewed data
income = np.array([30000, 40000, 50000, 60000, 1000000])
log_income = np.log10(income)

print("Original:", income)
print("Log-transformed:", log_income)
# [4.48, 4.60, 4.70, 4.78, 6.00] — much less skewed
```

**Related Terms:** Skewness, Normalization, Power Transform

---

### M

#### Mean Imputation
**Definition:** Replacing missing values with the mean of the non-missing values in that column. Simple but can reduce variance and distort relationships.

**Example:**
```python
import pandas as pd
import numpy as np

df = pd.DataFrame({'age': [25, 30, np.nan, 45, 50]})
mean_val = df['age'].mean()
df_filled = df.fillna(mean_val)

print(f"Mean: {mean_val:.1f}")  # 37.5
print(df_filled)
```

**Related Terms:** Median Imputation, Mode Imputation, Imputation

#### Median Imputation
**Definition:** Replacing missing values with the median of the non-missing values. More robust to outliers than mean imputation.

**Example:**
```python
import pandas as pd
import numpy as np

df = pd.DataFrame({'salary': [50000, 60000, 75000, np.nan, 200000]})
median_val = df['salary'].median()
df_filled = df.fillna(median_val)

print(f"Median: {median_val:.0f}")  # 67500 (robust to 200000 outlier)
print(df_filled)
```

**Related Terms:** Mean Imputation, Outliers, Imputation

#### MinMaxScaler
**Definition:** A preprocessing tool that transforms features by scaling them to a fixed range, typically [0, 1], using the formula: X_scaled = (X - X_min) / (X_max - X_min).

**Example:**
```python
from sklearn.preprocessing import MinMaxScaler
import numpy as np

data = np.array([[25, 50000], [30, 60000], [35, 75000], [40, 90000]])
scaler = MinMaxScaler()
scaled = scaler.fit_transform(data)

print("Original:\n", data)
print("Scaled:\n", scaled)
# Feature 1: [0, 0.33, 0.67, 1]
# Feature 2: [0, 0.29, 0.57, 1]
```

**Related Terms:** StandardScaler, RobustScaler, Normalization

---

### N

#### Normalization
**Definition:** The process of scaling features to a standard range. Can refer to Min-Max scaling [0,1] or other bounded transformations.

**Example:**
```python
from sklearn.preprocessing import MinMaxScaler

# Min-Max normalization to [0, 1]
scaler = MinMaxScaler()
X_normalized = scaler.fit_transform(X)
print(f"Min: {X_normalized.min(axis=0)}")  # [0, 0]
print(f"Max: {X_normalized.max(axis=0)}")  # [1, 1]
```

**Related Terms:** Standardization, MinMaxScaler, Feature Scaling

---

### O

#### Outliers
**Definition:** Data points that are significantly different from other observations. May indicate errors, natural variation, or rare events.

**Example:**
```python
import numpy as np

# IQR method for outlier detection
Q1 = np.percentile(data, 25)
Q3 = np.percentile(data, 75)
IQR = Q3 - Q1

# Outliers are outside [Q1 - 1.5*IQR, Q3 + 1.5*IQR]
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
outliers = data[(data < lower) | (data > upper)]
```

**Related Terms:** IQR, Z-Score, RobustScaler, Anomaly Detection

---

### R

#### RobustScaler
**Definition:** A preprocessing tool that scales features using statistics that are robust to outliers — the median and interquartile range (IQR).

**Formula:**
```
X_scaled = (X - median) / IQR
```

**Example:**
```python
from sklearn.preprocessing import RobustScaler
import numpy as np

data_with_outliers = np.array([[50], [55], [60], [65], [200]])
scaler = RobustScaler()
scaled = scaler.fit_transform(data_with_outliers)

print("Original:", data_with_outliers.flatten())
print("Robust-scaled:", scaled.flatten())
```

**Related Terms:** StandardScaler, MinMaxScaler, Outliers, Median

---

### S

#### StandardScaler
**Definition:** A preprocessing tool that standardizes features by removing the mean and scaling to unit variance (Z-score normalization): X_scaled = (X - mean) / std.

**Example:**
```python
from sklearn.preprocessing import StandardScaler
import numpy as np

data = np.array([[100, 0.5], [200, 1.0], [300, 1.5]])
scaler = StandardScaler()
scaled = scaler.fit_transform(data)

print("Standardized:\n", scaled)
print("Mean:", scaled.mean(axis=0))   # [0, 0]
print("Std:", scaled.std(axis=0))     # [1, 1]
```

**Related Terms:** MinMaxScaler, RobustScaler, Z-Score, Standardization

#### Standardization
**Definition:** The process of transforming features to have zero mean and unit variance. Also called Z-score normalization.

**Formula:**
```
Z = (X - μ) / σ
```
where μ is the mean and σ is the standard deviation.

**Example:**
```python
# Manual standardization
mean = X.mean(axis=0)
std = X.std(axis=0)
X_standardized = (X - mean) / std

# Using sklearn
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_standardized = scaler.fit_transform(X)
```

**Related Terms:** Normalization, Z-Score, StandardScaler

#### Skewness
**Definition:** A measure of the asymmetry of a data distribution. Positive skew = tail on right, negative skew = tail on left.

**Example:**
```python
import numpy as np
from scipy.stats import skew

# Right-skewed data
data = np.array([1, 2, 2, 3, 3, 3, 4, 100])
print(f"Skewness: {skew(data):.2f}")  # Positive = right-skewed

# Apply log transform to reduce skewness
log_data = np.log10(data)
print(f"Log skewness: {skew(log_data):.2f}")
```

**Related Terms:** Log Transform, Normal Distribution, Mean, Median

---

## Key Formulas

| Formula | Expression | Description |
|---------|-----------|-------------|
| Min-Max | `(x - min) / (max - min)` | Scale to [0, 1] |
| Z-Score | `(x - mean) / std` | Standardize to N(0,1) |
| IQR | `Q3 - Q1` | Interquartile range |
| Outlier Bound (low) | `Q1 - 1.5 × IQR` | Lower outlier threshold |
| Outlier Bound (high) | `Q3 + 1.5 × IQR` | Upper outlier threshold |
| Log Transform | `log10(x)` | Compress large values |
| Skewness | `E[(X-μ)³] / σ³` | Distribution asymmetry |

---

## Python Import Cheat Sheet

```python
# Pandas for data manipulation
import pandas as pd
import numpy as np

# Imputation
from sklearn.impute import SimpleImputer

# Scaling
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# Transformation
from sklearn.preprocessing import PowerTransformer, FunctionTransformer

# Pipelines
from sklearn.pipeline import Pipeline

# Outlier detection
from scipy import stats
```
