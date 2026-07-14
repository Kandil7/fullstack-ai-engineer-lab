# Lecture 07: R-squared (Coefficient of Determination)

## Topic Overview

R-squared (R²), also known as the Coefficient of Determination, is one of the most important metrics for evaluating regression models. It measures how well the model's predictions approximate the actual data points — essentially, what proportion of the variance in the target variable is explained by the features.

Understanding R² is crucial because it provides a standardized way to compare models and assess model quality. This lecture covers R² calculation, interpretation, adjusted R², and common pitfalls.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Define R-squared and explain what it measures
2. Calculate R-squared manually and using sklearn
3. Interpret R-squared values in context
4. Understand the relationship between R² and sum of squares
5. Use adjusted R² for comparing models with different numbers of features
6. Recognize when high R² doesn't mean a good model
7. Analyze residuals to validate model assumptions
8. Compare training and test R² to detect overfitting

---

## Key Concepts

### 1. What is R-squared?

R² measures the proportion of variance in the target variable that is predictable from the features.

**Range:** 0 to 1 (can be negative for very bad models)

| R² Value | Interpretation |
|----------|---------------|
| 1.0 | Perfect fit — model explains all variance |
| 0.75 | Strong fit — model explains 75% of variance |
| 0.50 | Moderate fit — model explains 50% of variance |
| 0.25 | Weak fit — model explains 25% of variance |
| 0.0 | No better than predicting the mean |
| < 0 | Worse than predicting the mean |

### 2. Sum of Squares Decomposition

R² is based on the decomposition of total variance:

```
Total Sum of Squares (TSS) = Σ(yᵢ - ȳ)²
  → Total variance in the data

Residual Sum of Squares (RSS) = Σ(yᵢ - ŷᵢ)²
  → Variance NOT explained by the model

Explained Sum of Squares (ESS) = Σ(ŷᵢ - ȳ)²
  → Variance explained by the model

TSS = RSS + ESS
```

### 3. R² Formula

```
R² = 1 - (RSS / TSS)
   = 1 - (Residual SS / Total SS)
   = ESS / TSS
   = (TSS - RSS) / TSS
```

**Interpretation:**
- If R² = 0.85, the model explains 85% of the variance
- The remaining 15% is unexplained (residuals)

### 4. Adjusted R²

Regular R² always increases when you add more features, even if they're useless. Adjusted R² penalizes for adding features that don't improve the model:

```
Adjusted R² = 1 - (1 - R²) × (n - 1) / (n - p - 1)
```

Where:
- n = number of samples
- p = number of features

### 5. Limitations of R²

- **High R² ≠ good model** — Can be misleading with spurious correlations
- **Doesn't indicate bias** — Model could be systematically wrong
- **Doesn't show residual patterns** — Always check residuals
- **Sensitive to outliers** — A few extreme points can inflate R²
- **Not comparable across datasets** — Depends on target variance

---

## Code Examples

### Example 1: Simple R-squared Calculation

```python
import numpy as np
from sklearn.linear_model import LinearRegression

np.random.seed(42)
X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(-1, 1)
y = 2 * X.flatten() + 1 + np.random.normal(0, 1, 10)

model = LinearRegression()
model.fit(X, y)
r_squared = model.score(X, y)

print(f"Coefficients: {model.coef_[0]:.4f}, Intercept: {model.intercept_:.4f}")
print(f"R-squared: {r_squared:.4f}")
print(f"Model explains {r_squared * 100:.1f}% of the variance")
```

### Example 2: Manual R-squared Calculation

```python
y_mean = np.full_like(y, np.mean(y))

# Total Sum of Squares (TSS)
tss = np.sum((y - y_mean) ** 2)

# Residual Sum of Squares (RSS)
y_pred = model.predict(X)
rss = np.sum((y - y_pred) ** 2)

# R-squared
r_squared_manual = 1 - (rss / tss)

print(f"Mean of y: {np.mean(y):.4f}")
print(f"Total Sum of Squares (TSS): {tss:.4f}")
print(f"Residual Sum of Squares (RSS): {rss:.4f}")
print(f"Manual R-squared: {r_squared_manual:.4f}")
print(f"sklearn R-squared: {r_squared:.4f}")
```

### Example 3: Good vs Bad Models

```python
np.random.seed(42)
X_strong = np.linspace(0, 10, 50).reshape(-1, 1)

# Strong relationship (low noise)
y_strong = 3 * X_strong.flatten() + 2 + np.random.normal(0, 0.5, 50)

# Weak relationship (high noise)
y_noisy = 0.5 * X_strong.flatten() + np.random.normal(0, 5, 50)

model_strong = LinearRegression().fit(X_strong, y_strong)
model_noisy = LinearRegression().fit(X_strong, y_noisy)

print(f"Strong relationship R²: {model_strong.score(X_strong, y_strong):.4f}")
print(f"Noisy relationship R²:  {model_noisy.score(X_strong, y_noisy):.4f}")
```

### Example 4: R-squared with Train/Test Split

```python
from sklearn.model_selection import train_test_split

np.random.seed(42)
X = np.random.rand(100, 1) * 10
y = 2.5 * X.flatten() + 5 + np.random.normal(0, 2, 100)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

train_r2 = model.score(X_train, y_train)
test_r2 = model.score(X_test, y_test)

print(f"Training R²:  {train_r2:.4f}")
print(f"Testing R²:   {test_r2:.4f}")
print(f"Gap:          {train_r2 - test_r2:.4f}")
```

### Example 5: Adjusted R-squared

```python
n = len(X_train)
p = 1  # number of features

adjusted_r2 = 1 - (1 - train_r2) * (n - 1) / (n - p - 1)

print(f"R-squared:       {train_r2:.4f}")
print(f"Adjusted R-squared: {adjusted_r2:.4f}")

# With multiple irrelevant features
np.random.seed(42)
X_multi = np.random.rand(100, 10)
X_multi[:, 0] = np.linspace(0, 10, 100)  # Only first feature is meaningful
y_multi = 2 * X_multi[:, 0] + np.random.normal(0, 1, 100)

model_multi = LinearRegression().fit(X_multi, y_multi)
r2_multi = model_multi.score(X_multi, y_multi)

p_multi = X_multi.shape[1]
adj_r2_multi = 1 - (1 - r2_multi) * (n - 1) / (n - p_multi - 1)

print(f"\nWith 10 features (only 1 meaningful):")
print(f"R-squared:       {r2_multi:.4f}")
print(f"Adjusted R-squared: {adj_r2_multi:.4f}")
```

### Example 6: Analyzing Residuals

```python
np.random.seed(42)
X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(-1, 1)
y = np.array([2.1, 4.0, 5.8, 8.2, 9.9, 12.1, 14.0, 15.8, 18.2, 20.1])

model = LinearRegression().fit(X, y)
y_pred = model.predict(X)
residuals = y - y_pred

print(f"{'X':>4} {'Actual':>8} {'Predicted':>10} {'Residual':>10}")
print("-" * 36)
for i in range(len(X)):
    print(f"{X[i][0]:>4.0f} {y[i]:>8.2f} {y_pred[i]:>10.2f} {residuals[i]:>10.4f}")

print(f"\nR-squared: {model.score(X, y):.4f}")
print(f"Mean residual: {residuals.mean():.4f}")  # Should be ≈ 0
```

---

## Common Mistakes to Avoid

1. **Reporting only training R²** — Always report test R²
2. **Assuming high R² = good model** — Check residuals!
3. **Using R² to compare different datasets** — R² depends on target variance
4. **Ignoring adjusted R²** — When comparing models with different feature counts
5. **Not checking for overfitting** — Large gap between train and test R²
6. **Over-interpreting R²** — It's one metric, not the whole story

---

## Best Practices

1. **Always use train/test split** — Report both train and test R²
2. **Use adjusted R²** for multiple regression
3. **Check residuals** for patterns (should be random)
4. **Consider domain context** — A "low" R² might be acceptable in some fields
5. **Compare with baseline** — Is your model better than just predicting the mean?
6. **Use multiple metrics** — R² + RMSE + residual analysis
7. **Visualize** — Plot actual vs predicted

---

## Practice Exercises

### Exercise 1: Manual R²
Calculate R² manually for: actual=[1,2,3,4], predicted=[1.1, 1.9, 3.2, 3.8].

### Exercise 2: Train vs Test
Train a linear regression and compare train R² and test R². What does the gap tell you?

### Exercise 3: Adjusted R²
Add 5 random (irrelevant) features to a dataset. Compare R² and adjusted R².

### Exercise 4: Residual Analysis
Plot residuals vs predicted values. Do they look random? What patterns might indicate problems?

### Exercise 5: Model Comparison
Compare R² of linear vs polynomial (degree 2) on the same data. Which is better?

---

## Summary

| Metric | Formula | Interpretation |
|--------|---------|---------------|
| **R²** | `1 - RSS/TSS` | Proportion of variance explained |
| **Adjusted R²** | `1 - (1-R²)(n-1)/(n-p-1)` | Penalizes for extra features |
| **TSS** | `Σ(y - ȳ)²` | Total variance |
| **RSS** | `Σ(y - ŷ)²` | Unexplained variance |

| R² Range | Interpretation |
|----------|---------------|
| 0.75 - 1.00 | Strong fit |
| 0.50 - 0.75 | Moderate fit |
| 0.25 - 0.50 | Weak fit |
| 0.00 - 0.25 | Very weak |
| < 0 | Worse than mean |

**Key Takeaway:** R² measures how well your model explains the variance in the data. Always use train/test split, check residuals, and consider adjusted R² when comparing models. A high R² is good but not sufficient — domain knowledge and residual analysis are equally important.

---

## Next Lecture

In [Lecture 08: Multiple Regression](08-multiple-regression-lecture.md), we'll extend linear regression to use multiple features and learn how to interpret coefficients.
