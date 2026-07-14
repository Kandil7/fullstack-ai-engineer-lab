# Glossary: Feature Scaling

## Quick Reference Table

| Term | Definition | Category |
|------|-----------|----------|
| Feature Scaling | Transforming features to common scale | Process |
| StandardScaler | Z-score normalization (mean=0, std=1) | Tool |
| MinMaxScaler | Scale to [0, 1] range | Tool |
| RobustScaler | Scale using median and IQR | Tool |
| Standardization | Z-score normalization | Technique |
| Normalization | Scaling to [0, 1] range | Technique |
| Data Leakage | Test info leaking into training | Problem |
| Pipeline | Sequence of preprocessing steps | Tool |
| Fit | Compute statistics from training data | Action |
| Transform | Apply scaling to data | Action |
| fit_transform | Fit and transform in one step | Action |
| Inverse Transform | Reverse the scaling | Method |
| Feature Range | Min and max values of a feature | Concept |
| Mean | Average of feature values | Statistic |
| Standard Deviation | Spread of feature values | Statistic |
| Median | Middle value of feature values | Statistic |
| IQR | Interquartile Range (Q3 - Q1) | Statistic |
| Outlier | Data point far from others | Concept |
| Scaling Factor | Multiplier applied to features | Concept |
| Bias Term | Intercept in linear models | Concept |

---

## Detailed Definitions

### D

#### Data Leakage
**Definition:** When information from outside the training dataset is used to create the model, typically by fitting scalers or preprocessors on the entire dataset before splitting.

**Example:**
```python
# WRONG: Data leakage
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Uses ALL data statistics
X_train, X_test = train_test_split(X_scaled, test_size=0.2)

# CORRECT: No leakage
X_train, X_test = train_test_split(X, test_size=0.2)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # Only training data
X_test_scaled = scaler.transform(X_test)         # Use training statistics
```

**Related Terms:** Train/Test Split, Fit, Transform, Preprocessing

---

### F

#### fit_transform
**Definition:** A method that computes the scaling parameters (fit) and applies the transformation (transform) in one step. Should only be used on training data.

**Example:**
```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # Fit + transform
# Equivalent to:
# scaler.fit(X_train)
# X_train_scaled = scaler.transform(X_train)
```

**Related Terms:** fit, transform, fit_transform

#### Fit (Scaling)
**Definition:** Computing the scaling parameters (mean, std, min, max, median, IQR) from the training data. These parameters are then used to transform both training and new data.

**Example:**
```python
scaler = StandardScaler()
scaler.fit(X_train)  # Computes mean and std for each feature

print(f"Means: {scaler.mean_}")
print(f"Stds: {scaler.scale_}")
```

**Related Terms:** Transform, fit_transform, Statistics

---

### I

#### Inverse Transform
**Definition:** A method that reverses the scaling transformation, converting scaled data back to the original scale.

**Example:**
```python
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)
X_original = scaler.inverse_transform(X_scaled)

print(f"Original: {X_train[0]}")
print(f"Scaled: {X_scaled[0]}")
print(f"Inverse: {X_original[0]}")
# Original ≈ Inverse (with floating point precision)
```

**Related Terms:** Transform, Fit, Scaling

#### IQR (Interquartile Range)
**Definition:** The range between the first quartile (Q1) and third quartile (Q3). Used by RobustScaler to scale features in a way that's resistant to outliers.

**Formula:**
```
IQR = Q3 - Q1
```

**Example:**
```python
import numpy as np

data = np.array([10, 20, 30, 40, 50, 100])
Q1 = np.percentile(data, 25)
Q3 = np.percentile(data, 75)
IQR = Q3 - Q1
print(f"Q1: {Q1}, Q3: {Q3}, IQR: {IQR}")
```

**Related Terms:** RobustScaler, Quartiles, Outliers

---

### M

#### MinMaxScaler
**Definition:** A preprocessing tool that transforms features by scaling them to a fixed range, typically [0, 1], using the formula: X_scaled = (X - X_min) / (X_max - X_min).

**Example:**
```python
from sklearn.preprocessing import MinMaxScaler
import numpy as np

data = np.array([[100, 0.5], [200, 1.0], [300, 1.5]])
scaler = MinMaxScaler()
scaled = scaler.fit_transform(data)

print("Original:\n", data)
print("Scaled:\n", scaled)
# Feature 1: [0, 0.5, 1]
# Feature 2: [0, 0.5, 1]
```

**Properties:**
- Output range: [0, 1] (default)
- Sensitive to outliers
- Preserves relationships between data points

**Related Terms:** StandardScaler, RobustScaler, Normalization

---

### N

#### Normalization
**Definition:** The process of scaling features to a standard range. Can refer to Min-Max scaling [0,1] or other bounded transformations.

**Example:**
```python
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
X_normalized = scaler.fit_transform(X)
print(f"Min: {X_normalized.min(axis=0)}")  # [0, 0]
print(f"Max: {X_normalized.max(axis=0)}")  # [1, 1]
```

**Related Terms:** Standardization, MinMaxScaler, Feature Scaling

---

### R

#### RobustScaler
**Definition:** A preprocessing tool that scales features using the median and interquartile range (IQR), making it robust to outliers.

**Formula:**
```
X_scaled = (X - median) / IQR
```

**Example:**
```python
from sklearn.preprocessing import RobustScaler
import numpy as np

# Data with outliers
data = np.array([[50], [55], [60], [65], [200]])
scaler = RobustScaler()
scaled = scaler.fit_transform(data)

print("Original:", data.flatten())
print("Robust-scaled:", scaled.flatten())
# Outlier (200) has less influence than with StandardScaler
```

**Related Terms:** StandardScaler, MinMaxScaler, Outliers, IQR

---

### S

#### StandardScaler
**Definition:** A preprocessing tool that standardizes features by removing the mean and scaling to unit variance (Z-score normalization).

**Formula:**
```
X_scaled = (X - mean) / std
```

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

**Properties:**
- Output: mean=0, std=1
- Sensitive to outliers
- Best for normally distributed data

**Related Terms:** MinMaxScaler, RobustScaler, Standardization

#### Standardization
**Definition:** The process of transforming features to have zero mean and unit variance. Also called Z-score normalization.

**Formula:**
```
Z = (X - μ) / σ
```

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

---

## Key Formulas

| Formula | Expression | Description |
|---------|-----------|-------------|
| StandardScaler | `(x - mean) / std` | Z-score normalization |
| MinMaxScaler | `(x - min) / (max - min)` | Scale to [0,1] |
| RobustScaler | `(x - median) / IQR` | Outlier-resistant |
| IQR | `Q3 - Q1` | Interquartile range |
| Z-Score | `(x - μ) / σ` | Standard score |

---

## Python Import Cheat Sheet

```python
# Scalers
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# Pipeline
from sklearn.pipeline import Pipeline

# Train/test split
from sklearn.model_selection import train_test_split

# Workflow
X_train, X_test = train_test_split(X, test_size=0.2)

# Option 1: Manual
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Option 2: Pipeline (recommended)
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LinearRegression())
])
pipe.fit(X_train, y_train)
predictions = pipe.predict(X_test)
```
