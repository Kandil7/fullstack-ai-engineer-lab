# Lecture 05: Linear Regression

## Topic Overview

Linear Regression is one of the most fundamental and widely used algorithms in machine learning. It models the relationship between a dependent variable (target) and one or more independent variables (features) by fitting a linear equation to observed data. This lecture covers simple and multiple linear regression, model evaluation, and the assumptions behind the algorithm.

Linear Regression is often the first algorithm taught because it's simple, interpretable, and forms the basis for many more complex algorithms.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand the concept of linear regression and the best fit line
2. Calculate slope and intercept manually
3. Use scikit-learn's `LinearRegression` to fit models
4. Make predictions on new data
5. Evaluate models using MSE, RMSE, and R-squared
6. Understand the difference between simple and multiple regression
7. Check the assumptions of linear regression
8. Apply train/test split for proper evaluation

---

## Key Concepts

### 1. What is Linear Regression?

Linear regression finds the best-fitting straight line through a set of data points. The line is defined by:

```
y = mx + b
```

Where:
- `y` = predicted value (target)
- `x` = input value (feature)
- `m` = slope (coefficient) — how much y changes for each unit change in x
- `b` = intercept — the value of y when x = 0

### 2. Finding the Best Fit Line

The "best fit" line minimizes the sum of squared residuals (errors):

```
Residual = Actual - Predicted = y - ŷ
```

**Ordinary Least Squares (OLS):**
```
Minimize: Σ(yᵢ - ŷᵢ)² = Σ(yᵢ - (mxᵢ + b))²
```

**Slope formula:**
```
m = Σ((xᵢ - x̄)(yᵢ - ȳ)) / Σ((xᵢ - x̄)²)
```

**Intercept formula:**
```
b = ȳ - m × x̄
```

### 3. Simple vs Multiple Regression

| Type | Features | Equation |
|------|----------|----------|
| Simple | 1 feature | y = mx + b |
| Multiple | Multiple features | y = b₀ + b₁x₁ + b₂x₂ + ... + bₙxₙ |

### 4. Model Evaluation

**Mean Squared Error (MSE):**
```
MSE = (1/n) × Σ(yᵢ - ŷᵢ)²
```

**Root Mean Squared Error (RMSE):**
```
RMSE = √MSE
```

**R-squared (R²):**
```
R² = 1 - (SS_res / SS_tot)
SS_res = Σ(yᵢ - ŷᵢ)²
SS_tot = Σ(yᵢ - ȳ)²
```

### 5. Assumptions of Linear Regression

1. **Linearity:** Relationship between X and y is linear
2. **Independence:** Observations are independent of each other
3. **Homoscedasticity:** Constant variance of residuals
4. **Normality:** Residuals are normally distributed
5. **No multicollinearity:** Features are not highly correlated (multiple regression)

---

## Code Examples

### Example 1: Manual Linear Regression

```python
import numpy as np

# House size vs price data
X = np.array([1000, 1500, 2000, 2500, 3000])
y = np.array([200000, 300000, 400000, 500000, 600000])

# Calculate slope (m) and intercept (b)
x_mean = np.mean(X)
y_mean = np.mean(y)

numerator = np.sum((X - x_mean) * (y - y_mean))
denominator = np.sum((X - x_mean) ** 2)
m = numerator / denominator
b = y_mean - m * x_mean

print(f"Slope (m): {m:.2f}")      # 200.00
print(f"Intercept (b): {b:.2f}")  # 0.00
print(f"Equation: y = {m:.2f}x + {b:.2f}")
```

### Example 2: Using sklearn LinearRegression

```python
from sklearn.linear_model import LinearRegression

# Reshape X to 2D (required by sklearn)
X_2d = X.reshape(-1, 1)

model = LinearRegression()
model.fit(X_2d, y)

print(f"Coefficient (slope): {model.coef_[0]:.2f}")
print(f"Intercept: {model.intercept_:.2f}")
```

### Example 3: Making Predictions

```python
# Predict prices for new house sizes
new_sizes = np.array([[1800], [2200], [2800]])
predictions = model.predict(new_sizes)

for size, price in zip(new_sizes.flatten(), predictions):
    print(f"Size: {size} sq ft → Predicted price: ${price:,.0f}")
```

### Example 4: Model Evaluation

```python
from sklearn.metrics import mean_squared_error, r2_score

y_pred = model.predict(X_2d)

mse = mean_squared_error(y, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y, y_pred)

print(f"Mean Squared Error: {mse:,.0f}")
print(f"Root Mean Squared Error: {rmse:,.0f}")
print(f"R-squared: {r2:.4f}")
```

### Example 5: Train/Test Split Evaluation

```python
from sklearn.model_selection import train_test_split

np.random.seed(42)
X = np.random.rand(100, 1) * 10
y = 2 * X.squeeze() + 3 + np.random.randn(100) * 0.5

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"Training set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}")
print(f"R-squared on test: {r2:.4f}")
print(f"RMSE on test: {rmse:.4f}")
```

### Example 6: Multiple Linear Regression

```python
# Features: square_feet, bedrooms, age
X_multi = np.array([
    [1500, 3, 10],
    [2000, 4, 5],
    [1200, 2, 15],
    [1800, 3, 8],
    [2200, 4, 3]
])
y_multi = np.array([300000, 450000, 250000, 400000, 500000])

model_multi = LinearRegression()
model_multi.fit(X_multi, y_multi)

print("Coefficients:")
print(f"  Square feet: {model_multi.coef_[0]:.2f}")
print(f"  Bedrooms: {model_multi.coef_[1]:.2f}")
print(f"  Age: {model_multi.coef_[2]:.2f}")
print(f"Intercept: {model_multi.intercept_:.2f}")

# Predict a new house
new_house = np.array([[1800, 3, 5]])
prediction = model_multi.predict(new_house)
print(f"\nPredicted price: ${prediction[0]:,.0f}")
```

---

## Common Mistakes to Avoid

1. **Using R² on training data** — Always evaluate on test set
2. **Ignoring assumptions** — Check linearity, normality, homoscedasticity
3. **Not reshaping X** — sklearn requires 2D input: `X.reshape(-1, 1)`
4. **Extrapolating far beyond training data** — Linear models may not hold
5. **Ignoring outliers** — They can heavily influence the regression line
6. **Not checking for multicollinearity** — Correlated features distort coefficients
7. **Assuming causation** — Correlation ≠ causation

---

## Best Practices

1. **Always split data** before evaluation (train/test split)
2. **Visualize the relationship** before fitting (scatter plot)
3. **Check residuals** for patterns (should be random)
4. **Use R² and RMSE together** — R² for relative fit, RMSE for absolute error
5. **Consider feature scaling** for multiple regression
6. **Start simple** — simple regression before multiple
7. **Document assumptions** — and verify them

---

## Practice Exercises

### Exercise 1: Manual Calculation
Given data points `(1, 3), (2, 5), (3, 7), (4, 9)`, calculate the slope and intercept manually.

### Exercise 2: Simple Regression
Generate 50 data points following `y = 3x + 2 + noise`. Fit a linear regression and print the coefficients.

### Exercise 3: Evaluation
Create a model, make predictions, and calculate MSE, RMSE, and R². What does each metric tell you?

### Exercise 4: Multiple Regression
Add two more features to a dataset. How do the coefficients change? Which feature is most important?

### Exercise 5: Assumptions
Check the four assumptions of linear regression on a dataset. Which assumptions are violated?

---

## Summary

| Concept | Description |
|---------|-------------|
| **Linear Regression** | Fits a straight line: y = mx + b |
| **Slope (m)** | Change in y per unit change in x |
| **Intercept (b)** | Value of y when x = 0 |
| **MSE** | Average squared error |
| **RMSE** | Square root of MSE (same units as y) |
| **R²** | Proportion of variance explained (0-1) |
| **Simple Regression** | One feature |
| **Multiple Regression** | Multiple features |

**Key Takeaway:** Linear regression is the foundation of ML. Master the concept of the best fit line, understand how to evaluate models with R² and RMSE, and always use train/test split for honest evaluation.

---

## Next Lecture

In [Lecture 06: Polynomial Regression](06-polynomial-regression-lecture.md), we'll extend linear regression to fit curved relationships using polynomial features.
