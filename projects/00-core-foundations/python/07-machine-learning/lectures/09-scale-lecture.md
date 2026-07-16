# Lecture 09: Feature Scaling

## Topic Overview

Feature scaling is the process of transforming features to a common scale without distorting differences in ranges. Many ML algorithms (k-NN, SVM, gradient descent, neural networks) are sensitive to the scale of features. This lecture covers StandardScaler, MinMaxScaler, RobustScaler, when to use each, and common scaling mistakes.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand why feature scaling is important
2. Apply StandardScaler for Z-score normalization
3. Apply MinMaxScaler for 0-1 normalization
4. Apply RobustScaler for outlier-resistant scaling
5. Know when to use each scaler
6. Avoid common scaling mistakes
7. Use pipelines for clean scaling workflows
8. Transform new data using training statistics

---

## Key Concepts

### 1. Why Scale Features?

Different features often have different scales:
- Age: 0-100
- Salary: 20,000-200,000
- Square feet: 500-5,000

**Problems without scaling:**
- Distance-based algorithms (k-NN, SVM) are dominated by large-scale features
- Gradient descent converges slower
- Coefficients are hard to compare

### 2. Scaling Methods

| Method | Formula | Range | Best For |
|--------|---------|-------|----------|
| **StandardScaler** | `(x - mean) / std` | -∞ to +∞ | Normal data |
| **MinMaxScaler** | `(x - min) / (max - min)` | [0, 1] | Bounded values |
| **RobustScaler** | `(x - median) / IQR` | -∞ to +∞ | Outliers |

### 3. When to Scale

| Algorithm | Needs Scaling? |
|-----------|---------------|
| k-NN | Yes |
| SVM | Yes |
| Linear Regression | Optional |
| Logistic Regression | Yes |
| Decision Trees | No |
| Random Forest | No |
| Neural Networks | Yes |
| PCA | Yes |

---

## Code Examples

### Example 1: Different Scales Problem

```python
import numpy as np

square_feet = np.random.randint(800, 3500, 100)
bedrooms = np.random.randint(1, 6, 100)

print(f"Square feet range: {square_feet.min()} - {square_feet.max()}")
print(f"Bedrooms range: {bedrooms.min()} - {bedrooms.max()}")
print("\nDifferent scales can bias distance-based models")
```

### Example 2: StandardScaler

```python
from sklearn.preprocessing import StandardScaler

X = np.column_stack([square_feet, bedrooms])

scaler = StandardScaler()
X_standardized = scaler.fit_transform(X)

print("Original (first 5 rows):")
print(X[:5])
print("\nStandardized (first 5 rows):")
print(X_standardized[:5])
print(f"\nStandardized mean: {X_standardized.mean(axis=0)}")  # ≈ [0, 0]
print(f"Standardized std: {X_standardized.std(axis=0)}")       # ≈ [1, 1]
```

### Example 3: MinMaxScaler

```python
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
X_normalized = scaler.fit_transform(X)

print("Normalized (first 5 rows):")
print(X_normalized[:5])
print(f"\nNormalized min: {X_normalized.min(axis=0)}")  # [0, 0]
print(f"Normalized max: {X_normalized.max(axis=0)}")     # [1, 1]
```

### Example 4: RobustScaler

```python
from sklearn.preprocessing import RobustScaler

# Data with outliers
np.random.seed(42)
data_with_outliers = np.random.randn(100, 2) * 10 + 50
data_with_outliers[0] = [200, 200]  # Outlier

scaler = RobustScaler()
data_robust = scaler.fit_transform(data_with_outliers)

print("Original stats:")
print(f"  Mean: {data_with_outliers.mean(axis=0)}")
print(f"  Std: {data_with_outliers.std(axis=0)}")
print("\nRobust-scaled stats:")
print(f"  Mean: {data_robust.mean(axis=0):.2f}")
print(f"  Std: {data_robust.std(axis=0):.2f}")
```

### Example 5: Impact on Model Performance

```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

np.random.seed(42)
X = np.random.rand(200, 2) * np.array([1000, 10])
y = 5 * X[:, 0] + 10 * X[:, 1] + np.random.randn(200) * 50

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Without scaling
model_unscaled = LinearRegression().fit(X_train, y_train)
r2_unscaled = r2_score(y_test, model_unscaled.predict(X_test))

# With StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model_scaled = LinearRegression().fit(X_train_scaled, y_train)
r2_scaled = r2_score(y_test, model_scaled.predict(X_test_scaled))

print(f"R² without scaling: {r2_unscaled:.4f}")
print(f"R² with scaling: {r2_scaled:.4f}")
```

### Example 6: Scaling Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LinearRegression())
])

pipe.fit(X_train, y_train)
r2 = r2_score(y_test, pipe.predict(X_test))

print(f"Pipeline R²: {r2:.4f}")
print("Pipeline handles scaling automatically")
```

### Example 7: Transforming New Data

```python
scaler = StandardScaler()
scaler.fit(X_train)  # Fit on training data ONLY

new_data = np.array([[500, 3], [2000, 4], [1000, 2]])
new_data_scaled = scaler.transform(new_data)

print("New data (original):")
print(new_data)
print("\nNew data (scaled):")
print(new_data_scaled)
```

---

## Common Mistakes to Avoid

1. **Scaling test data with test statistics** — Always use training statistics
2. **Scaling target variable** — Usually not needed for regression
3. **Scaling before train/test split** — Causes data leakage
4. **Forgetting to scale new data in production** — Use saved scaler
5. **Scaling tree-based models** — They don't need it
6. **Using MinMaxScaler with outliers** — Outliers compress the range

---

## Best Practices

1. **Fit scaler on training data only**
2. **Use pipeline** to avoid data leakage
3. **Save the scaler** for production use
4. **Choose scaler based on data** — StandardScaler for normal, RobustScaler for outliers
5. **Don't scale tree-based models** — They're scale-invariant

---

## Summary

| Scaler | Formula | Best For | Sensitive to Outliers? |
|--------|---------|----------|----------------------|
| StandardScaler | `(x-μ)/σ` | Normal data | Yes |
| MinMaxScaler | `(x-min)/(max-min)` | Bounded values | Yes |
| RobustScaler | `(x-median)/IQR` | Outlier data | No |

**Key Takeaway:** Feature scaling puts features on the same scale, which is essential for distance-based and gradient-based algorithms. Always fit the scaler on training data only and use pipelines to prevent data leakage.

---

## Next Lecture

In [Lecture 10: Train/Test Split](10-train-test-lecture.md), we'll dive deep into why splitting data is crucial and how to do it properly.
