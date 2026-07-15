# Lecture 06: Polynomial Regression

## Topic Overview

Polynomial Regression extends linear regression to model non-linear relationships between features and targets. Instead of fitting a straight line, it fits a curved line (polynomial) by creating additional features (x², x³, etc.). This lecture covers polynomial features, degree selection, overfitting vs underfitting, and how to choose the right polynomial degree.

Many real-world relationships are non-linear — growth curves, diminishing returns, seasonal patterns. Polynomial regression provides a simple way to capture these patterns while still using the familiar linear regression framework.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand why polynomial regression is needed for non-linear data
2. Create polynomial features using `PolynomialFeatures`
3. Fit polynomial regression models with different degrees
4. Compare models with different polynomial degrees
5. Understand overfitting with high-degree polynomials
6. Use train/test split to select the best degree
7. Make predictions with polynomial models
8. Know when to use polynomial regression vs other methods

---

## Key Concepts

### 1. Why Polynomial Regression?

Linear regression assumes a straight-line relationship:
```
y = b₀ + b₁x
```

But many relationships are curved:
```
y = b₀ + b₁x + b₂x²  (quadratic — parabola)
y = b₀ + b₁x + b₂x² + b₃x³  (cubic)
```

**Polynomial regression transforms the feature space:**
```
Original: x
Polynomial (degree 2): x, x²
Polynomial (degree 3): x, x², x³
```

### 2. Polynomial Features

`PolynomialFeatures` creates new features by raising existing features to powers:

| Degree | Features Created |
|--------|-----------------|
| 1 | x |
| 2 | x, x² |
| 3 | x, x², x³ |
| 4 | x, x², x³, x⁴ |

**With multiple features (degree 2):**
```
[x₁, x₂] → [x₁, x₂, x₁², x₁x₂, x₂²]
```

### 3. Overfitting vs Underfitting

```
Degree 1 (Underfitting):    Straight line, misses curvature
Degree 2 (Good fit):        Matches the curve
Degree 15 (Overfitting):    Wiggly line, memorizes noise
```

**Bias-Variance Tradeoff:**
- Low degree → High bias (underfitting)
- High degree → High variance (overfitting)

### 4. Degree Selection

Use cross-validation or test set performance to choose the best degree:

```
For degree in 1 to N:
    Fit model on training data
    Evaluate on test data
    Track R² or RMSE
Choose degree with best test performance
```

---

## Code Examples

### Example 1: Non-linear Data

```python
import numpy as np

# Data that follows a quadratic pattern
np.random.seed(42)
X = np.linspace(0, 10, 100).reshape(-1, 1)
y = 0.5 * X.squeeze()**2 - 3 * X.squeeze() + 10 + np.random.randn(100) * 2

print("This data follows a quadratic pattern (parabola)")
print("Simple linear regression won't fit well")
```

### Example 2: Creating Polynomial Features

```python
from sklearn.preprocessing import PolynomialFeatures

# Degree 2 polynomial features
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

print(f"Original shape: {X.shape}")        # (100, 1)
print(f"Polynomial shape: {X_poly.shape}")  # (100, 2)
print(f"Feature names: {poly.get_feature_names_out()}")

# Show the transformation
print("\nOriginal X (first 3 rows):")
print(X[:3])
print("\nPolynomial X (first 3 rows):")
print(X_poly[:3])  # [x, x²]
```

**Explanation:**
- `include_bias=False` excludes the constant term (we'll use LinearRegression's intercept instead)
- Each row now has 2 features: [x, x²]
- The model will learn: y = b₀ + b₁x + b₂x²

### Example 3: Quadratic Regression (Degree 2)

```python
from sklearn.linear_model import LinearRegression

poly2 = PolynomialFeatures(degree=2, include_bias=False)
X_poly2 = poly2.fit_transform(X)

model2 = LinearRegression()
model2.fit(X_poly2, y)

print(f"Coefficients: {model2.coef_}")
print(f"Intercept: {model2.intercept_}")
```

### Example 4: Comparing Different Degrees

```python
degrees = [1, 2, 3, 4, 5]

for degree in degrees:
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    X_poly = poly.fit_transform(X)
    
    model = LinearRegression()
    model.fit(X_poly, y)
    
    y_pred = model.predict(X_poly)
    r2 = r2_score(y, y_pred)
    
    print(f"Degree {degree}: R²={r2:.4f}, Features={X_poly.shape[1]}")
```

### Example 5: Overfitting with High Degree

```python
# Degree 15 (will overfit)
poly15 = PolynomialFeatures(degree=15, include_bias=False)
X_poly15 = poly15.fit_transform(X)

model15 = LinearRegression()
model15.fit(X_poly15, y)

y_pred15 = model15.predict(X_poly15)
r2_15 = r2_score(y, y_pred15)

print(f"Degree 15 R²: {r2_15:.4f} (looks good but overfits!)")
print("Overfitting: Model memorizes noise instead of learning pattern")
```

### Example 6: Proper Degree Selection with Train/Test Split

```python
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

best_degree = 1
best_r2 = -np.inf

for degree in range(1, 8):
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)  # Use same transform!
    
    model = LinearRegression()
    model.fit(X_train_poly, y_train)
    
    y_pred_test = model.predict(X_test_poly)
    r2_test = r2_score(y_test, y_pred_test)
    
    print(f"Degree {degree}: Test R²={r2_test:.4f}")
    
    if r2_test > best_r2:
        best_r2 = r2_test
        best_degree = degree

print(f"\nBest degree: {best_degree} (Test R²={best_r2:.4f})")
```

**Key insight:** Notice we use `poly.transform(X_test)` instead of `poly.fit_transform(X_test)`. The test data must use the same transformation as the training data.

### Example 7: Predictions with Polynomial Model

```python
# Use the best degree
poly_best = PolynomialFeatures(degree=best_degree, include_bias=False)
X_poly_best = poly_best.fit_transform(X)

model_best = LinearRegression()
model_best.fit(X_poly_best, y)

# Predict new values
X_new = np.array([[2], [5], [8]])
X_new_poly = poly_best.transform(X_new)
predictions = model_best.predict(X_new_poly)

for x_val, pred in zip(X_new.flatten(), predictions):
    print(f"X={x_val} → Predicted y={pred:.2f}")
```

---

## Common Mistakes to Avoid

1. **Using high degree without regularization** — Causes overfitting
2. **Fitting polynomial on test data** — Always transform test data with training transform
3. **Extrapolating beyond training range** — Polynomial models can diverge wildly outside training data
4. **Ignoring multicollinearity** — High-degree features are highly correlated
5. **Not visualizing** — Always plot to see if the fit makes sense
6. **Choosing degree based on training R²** — Always use test set

---

## Best Practices

1. **Start with degree 2** — Only increase if needed
2. **Use train/test split** for degree selection
3. **Visualize the fit** — Plot data and regression curve
4. **Consider regularization** — Ridge or Lasso for high-degree polynomials
5. **Be cautious with extrapolation** — Polynomials can explode outside training range
6. **Compare with other models** — Non-linear models may be better

---

## Practice Exercises

### Exercise 1: Quadratic Fit
Generate data following `y = 2x² - 3x + 5 + noise`. Fit a degree-2 polynomial and verify the coefficients are close to [2, -3].

### Exercise 2: Degree Comparison
Test degrees 1 through 10 on the same dataset. Plot R² vs degree. What's the optimal degree?

### Exercise 3: Overfitting
Fit a degree-20 polynomial. Compare training and test R². What do you observe?

### Exercise 4: Prediction
Using a degree-3 model, predict y for x = [1.5, 3.5, 6.5].

### Exercise 5: Multi-feature Polynomial
Create a dataset with 2 features. Apply degree-2 polynomial features. How many features are created?

---

## Summary

| Concept | Description |
|---------|-------------|
| **Polynomial Regression** | Fits curved relationships using polynomial features |
| **PolynomialFeatures** | Creates x², x³, etc. from original features |
| **Degree** | Maximum power of polynomial (2 = quadratic) |
| **Underfitting** | Degree too low, misses pattern |
| **Overfitting** | Degree too high, memorizes noise |
| **Best Practice** | Use train/test split to choose degree |

**Key Takeaway:** Polynomial regression extends linear regression to capture non-linear patterns. Use `PolynomialFeatures` to create polynomial terms, and always use train/test split to select the optimal degree and avoid overfitting.

---

## Next Lecture

In [Lecture 07: R-squared](07-r-squared-lecture.md), we'll dive deep into the R² metric — understanding what it measures, how to interpret it, and its limitations.
