# Glossary: Polynomial Regression

## Quick Reference Table

| Term | Definition | Category |
|------|-----------|----------|
| Polynomial Regression | Fits non-linear relationships using polynomial features | Algorithm |
| Polynomial Features | Features created by raising original features to powers | Technique |
| Degree | Maximum power of polynomial (2 = quadratic) | Parameter |
| Quadratic | Polynomial of degree 2 (parabola) | Type |
| Cubic | Polynomial of degree 3 | Type |
| Overfitting | Model memorizes noise in training data | Problem |
| Underfitting | Model is too simple to capture pattern | Problem |
| Bias-Variance Tradeoff | Balance between model complexity and generalization | Concept |
| include_bias | Whether to include constant term | Parameter |
| fit_transform | Fit to training data and transform | Method |
| transform | Apply transformation to new data | Method |
| Extrapolation | Predicting outside training data range | Concept |
| Multicollinearity | High correlation between polynomial features | Problem |
| Regularization | Technique to prevent overfitting | Technique |
| Cross-validation | Method for model selection | Technique |
| Feature Engineering | Creating new features from existing ones | Process |
| Non-linear | Relationships that aren't straight lines | Concept |
| Curvature | Degree of bending in data | Concept |
| Interpolation | Predicting within training data range | Concept |
| Generalization | Ability to perform well on new data | Concept |

---

## Detailed Definitions

### B

#### Bias-Variance Tradeoff
**Definition:** The fundamental tension in ML between model bias (errors from overly simple models) and model variance (errors from overly complex models). The goal is to find the balance that minimizes total error.

**Example:**
```python
# High bias (underfitting) — too simple
from sklearn.linear_model import LinearRegression
simple_model = LinearRegression()  # Degree 1
simple_model.fit(X_train, y_train)
print(f"Train R²: {simple_model.score(X_train, y_train):.2f}")  # Low
print(f"Test R²: {simple_model.score(X_test, y_test):.2f}")    # Low

# High variance (overfitting) — too complex
poly15 = PolynomialFeatures(degree=15)
X_train_poly = poly15.fit_transform(X_train)
complex_model = LinearRegression()
complex_model.fit(X_train_poly, y_train)
print(f"Train R²: {complex_model.score(X_train_poly, y_train):.2f}")  # High
print(f"Test R²: {complex_model.score(X_test_poly, y_test):.2f}")     # Low
```

**Visual intuition:**
```
Error
  │
  │  \                    /
  │   \  Bias²          / Variance
  │    \              /
  │     \           /
  │      \________/  ← Total error (sweet spot)
  │
  └──────────────────────── Model Complexity
  Low                      High
```

**Related Terms:** Overfitting, Underfitting, Regularization

---

### D

#### Degree
**Definition:** The highest power used in polynomial features. Determines the complexity of the polynomial model.

| Degree | Name | Shape | Features (1D) |
|--------|------|-------|---------------|
| 1 | Linear | Straight line | x |
| 2 | Quadratic | Parabola | x, x² |
| 3 | Cubic | S-curve | x, x², x³ |
| 4 | Quartic | W-shape | x, x², x³, x⁴ |

**Example:**
```python
from sklearn.preprocessing import PolynomialFeatures

# Different degrees
for degree in [1, 2, 3, 4]:
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    X_poly = poly.fit_transform(X)
    print(f"Degree {degree}: {X_poly.shape[1]} features")
# Degree 1: 1 features
# Degree 2: 2 features
# Degree 3: 3 features
# Degree 4: 4 features
```

**Related Terms:** Polynomial Features, Overfitting, Model Complexity

---

### E

#### Extrapolation
**Definition:** Making predictions outside the range of the training data. Polynomial models are particularly unreliable for extrapolation as they can diverge rapidly.

**Example:**
```python
import numpy as np

# Training data: x in [0, 10]
X_train = np.linspace(0, 10, 100).reshape(-1, 1)
y_train = 0.5 * X_train.squeeze()**2

# Extrapolation: x = 15 (outside training range)
X_extrapolate = np.array([[15]])
# Polynomial model might predict wildly different values
# Linear model would be more stable
```

**Warning:** Never trust polynomial predictions far outside the training range!

**Related Terms:** Interpolation, Generalization, Overfitting

---

### I

#### Interpolation
**Definition:** Making predictions within the range of the training data. This is where polynomial models typically perform well.

**Example:**
```python
# Training data: x in [0, 10]
# Interpolation: predicting for x = 5 (within range) — reliable
# Extrapolation: predicting for x = 20 (outside range) — unreliable
```

**Related Terms:** Extrapolation, Training Range, Generalization

---

### O

#### Overfitting
**Definition:** When a model learns the training data too well, including noise and outliers, resulting in excellent training performance but poor test performance. High-degree polynomials are prone to overfitting.

**Example:**
```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# High degree = overfitting
poly = PolynomialFeatures(degree=15, include_bias=False)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

model = LinearRegression()
model.fit(X_train_poly, y_train)

train_r2 = r2_score(y_train, model.predict(X_train_poly))
test_r2 = r2_score(y_test, model.predict(X_test_poly))

print(f"Train R²: {train_r2:.4f}")  # Very high (e.g., 0.99)
print(f"Test R²: {test_r2:.4f}")    # Low (e.g., -2.5)
print("Gap indicates overfitting!")
```

**Signs of overfitting:**
- Train R² much higher than test R²
- Model has many parameters relative to data points
- Prediction curve is very wiggly

**Related Terms:** Underfitting, Regularization, Bias-Variance Tradeoff

---

### P

#### Polynomial Features
**Definition:** Features created by raising original features to powers. Transforms the feature space to allow linear regression to fit non-linear relationships.

**Example:**
```python
from sklearn.preprocessing import PolynomialFeatures
import numpy as np

X = np.array([[2], [3], [4]])

# Degree 2
poly2 = PolynomialFeatures(degree=2, include_bias=False)
X_poly2 = poly2.fit_transform(X)
print(f"Degree 2: {X_poly2}")
# [[ 2,  4],   # [x, x²]
#  [ 3,  9],
#  [ 4, 16]]

# Degree 3
poly3 = PolynomialFeatures(degree=3, include_bias=False)
X_poly3 = poly3.fit_transform(X)
print(f"Degree 3: {X_poly3}")
# [[ 2,  4,  8],   # [x, x², x³]
#  [ 3,  9, 27],
#  [ 4, 16, 64]]
```

**With multiple features (degree 2):**
```python
X = np.array([[2, 3]])
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)
# Features: [x1, x2, x1², x1*x2, x2²]
```

**Related Terms:** Degree, Feature Engineering, Linear Regression

#### Polynomial Regression
**Definition:** A form of regression analysis where the relationship between the independent and dependent variable is modeled as an nth degree polynomial. Despite the name, it's still a linear model — linear in the coefficients.

**Equation:**
```
y = b₀ + b₁x + b₂x² + b₃x³ + ... + bₙxⁿ
```

**Example:**
```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

# Complete polynomial regression pipeline
model = Pipeline([
    ('poly', PolynomialFeatures(degree=2, include_bias=False)),
    ('linear', LinearRegression())
])

model.fit(X_train, y_train)
r2 = model.score(X_test, y_test)
print(f"Polynomial Regression R²: {r2:.4f}")
```

**Related Terms:** Linear Regression, Polynomial Features, Non-linear

---

### U

#### Underfitting
**Definition:** When a model is too simple to capture the underlying patterns in the data, resulting in poor performance on both training and test data.

**Example:**
```python
# Data follows a curve, but we fit a straight line
from sklearn.linear_model import LinearRegression

# True relationship: quadratic
X = np.linspace(0, 10, 100).reshape(-1, 1)
y = 0.5 * X.squeeze()**2

# Fitting linear model (degree 1)
model = LinearRegression()
model.fit(X, y)
r2 = model.score(X, y)
print(f"Linear fit R²: {r2:.4f}")  # Low — model is too simple
```

**Signs of underfitting:**
- Low R² on both train and test
- Model can't capture obvious patterns
- High bias

**Related Terms:** Overfitting, Bias, Model Complexity

---

## Key Formulas

| Formula | Expression | Description |
|---------|-----------|-------------|
| Quadratic | `y = b₀ + b₁x + b₂x²` | Degree 2 polynomial |
| Cubic | `y = b₀ + b₁x + b₂x² + b₃x³` | Degree 3 polynomial |
| General | `y = b₀ + Σbᵢxⁱ` | Degree n polynomial |
| Feature count | `n_features × degree` | Approximate feature count |
| Bias² | `(E[ŷ] - y)²` | Error from simplicity |
| Variance | `E[(ŷ - E[ŷ])²]` | Error from complexity |

---

## Python Import Cheat Sheet

```python
# Polynomial Features
from sklearn.preprocessing import PolynomialFeatures

# Linear Regression (used internally)
from sklearn.linear_model import LinearRegression

# Pipeline (clean workflow)
from sklearn.pipeline import Pipeline

# Metrics
from sklearn.metrics import r2_score, mean_squared_error

# Train/test split
from sklearn.model_selection import train_test_split

# Quick polynomial regression
model = Pipeline([
    ('poly', PolynomialFeatures(degree=2)),
    ('linear', LinearRegression())
])
model.fit(X_train, y_train)
score = model.score(X_test, y_test)
```
