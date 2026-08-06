# Lecture 08: Multiple Regression

## Topic Overview

Multiple Regression extends simple linear regression to use multiple features (independent variables) to predict a single target variable. This is more realistic than simple regression because most real-world predictions depend on multiple factors. This lecture covers fitting multiple regression models, interpreting coefficients, feature importance, and evaluation.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand the difference between simple and multiple regression
2. Prepare multi-feature datasets for regression
3. Fit a multiple regression model using sklearn
4. Interpret coefficients for each feature
5. Calculate and interpret R² for multiple regression
6. Determine feature importance from coefficients
7. Make predictions on new data with multiple features
8. Use Pandas DataFrames for cleaner workflow

---

## Key Concepts

### 1. Multiple Regression Equation

```
y = b₀ + b₁x₁ + b₂x₂ + b₃x₃ + ... + bₙxₙ
```

Where:
- `y` = predicted target
- `b₀` = intercept (value when all features are 0)
- `b₁, b₂, ...` = coefficients (effect of each feature)
- `x₁, x₂, ...` = feature values

### 2. Coefficient Interpretation

Each coefficient represents the change in the target for a one-unit change in that feature, **holding all other features constant**.

Example: Price = 100000 + 150 × sqft + 20000 × bedrooms - 1000 × age

- Each additional square foot adds $150 to price
- Each additional bedroom adds $20,000 to price
- Each year of age reduces price by $1,000

### 3. Feature Importance

Coefficient magnitudes indicate relative importance, but only when features are on the same scale. For features with different scales, standardize first.

### 4. Assumptions

Same as simple linear regression:
1. Linearity
2. Independence
3. Homoscedasticity
4. Normality of residuals
5. No multicollinearity (features shouldn't be highly correlated)

---

## Code Examples

### Example 1: Creating Feature Matrix

```python
import numpy as np

np.random.seed(42)
n_samples = 200

square_feet = np.random.randint(800, 3500, n_samples)
bedrooms = np.random.randint(1, 6, n_samples)
age = np.random.randint(0, 50, n_samples)

# Known relationship: Price = 150*sqft + 20000*bed - 1000*age + noise
price = (150 * square_feet + 
         20000 * bedrooms - 
         1000 * age + 
         np.random.randn(n_samples) * 20000)

# Stack features into matrix
X = np.column_stack([square_feet, bedrooms, age])
y = price

print(f"Feature matrix shape: {X.shape}")  # (200, 3)
print(f"Target shape: {y.shape}")            # (200,)
```

### Example 2: Fitting the Model

```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

print("Coefficients:")
print(f"  Square feet: {model.coef_[0]:.2f}")
print(f"  Bedrooms: {model.coef_[1]:.2f}")
print(f"  Age: {model.coef_[2]:.2f}")
print(f"Intercept: {model.intercept_:.2f}")
```

### Example 3: Regression Equation

```python
print(f"Price = {model.intercept_:.0f}")
print(f"       + {model.coef_[0]:.0f} × SquareFeet")
print(f"       + {model.coef_[1]:.0f} × Bedrooms")
print(f"       + {model.coef_[2]:.0f} × Age")
```

### Example 4: Model Evaluation

```python
from sklearn.metrics import mean_squared_error, r2_score

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:,.0f}")
print(f"Root Mean Squared Error: {rmse:,.0f}")
print(f"R-squared: {r2:.4f}")
```

### Example 5: Feature Importance

```python
feature_names = ['Square Feet', 'Bedrooms', 'Age']
importance = np.abs(model.coef_) / np.abs(model.coef_).sum()

for name, imp in sorted(zip(feature_names, importance), 
                       key=lambda x: x[1], reverse=True):
    print(f"  {name}: {imp:.3f} ({imp*100:.1f}%)")
```

### Example 6: Predicting New Houses

```python
new_houses = np.array([
    [1500, 3, 10],   # 1500 sqft, 3 bedrooms, 10 years old
    [2500, 4, 5],    # 2500 sqft, 4 bedrooms, 5 years old
    [1200, 2, 20]    # 1200 sqft, 2 bedrooms, 20 years old
])

predictions = model.predict(new_houses)

for i, (house, pred) in enumerate(zip(new_houses, predictions)):
    print(f"House {i+1}: {house[0]} sqft, {house[1]} bedrooms, {house[2]} years")
    print(f"  Predicted price: ${pred:,.0f}")
```

### Example 7: Using Pandas DataFrame

```python
import pandas as pd

df = pd.DataFrame({
    'square_feet': square_feet,
    'bedrooms': bedrooms,
    'age': age,
    'price': price
})

X = df[['square_feet', 'bedrooms', 'age']]
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

print(f"R² score: {model.score(X_test, y_test):.4f}")
```

---

## Common Mistakes to Avoid

1. **Ignoring multicollinearity** — Correlated features distort coefficients
2. **Using raw coefficients for importance** — Scale features first
3. **Not evaluating on test set** — Training R² is always higher
4. **Assuming causation** — Correlation ≠ causation
5. **Ignoring residuals** — Always check for patterns

---

## Best Practices

1. **Start with a correlation matrix** — Check for multicollinearity
2. **Standardize features** — For fair coefficient comparison
3. **Use adjusted R²** — When comparing models with different feature counts
4. **Visualize residuals** — Check assumptions
5. **Use Pandas** — Cleaner data manipulation
6. **Document feature meanings** — Know what each coefficient represents

---

## Practice Exercises

### Exercise 1: Two-Feature Model
Create a dataset with 2 features and fit a multiple regression. Print the equation.

### Exercise 2: Feature Importance
Which feature has the largest absolute coefficient? Is it the most important?

### Exercise 3: Prediction
Predict the price of a house with 2000 sqft, 3 bedrooms, and 7 years old.

### Exercise 4: Evaluation
Compare R² of simple (1 feature) vs multiple (3 features) regression.

### Exercise 5: Multicollinearity
Create two highly correlated features. How do coefficients change?

---

## Summary

| Concept | Description |
|---------|-------------|
| **Multiple Regression** | Uses multiple features to predict target |
| **Coefficient** | Effect of one feature (holding others constant) |
| **Intercept** | Base value when all features are 0 |
| **Feature Importance** | Relative contribution of each feature |
| **R²** | Proportion of variance explained |
| **Multicollinearity** | Problem when features are highly correlated |

**Key Takeaway:** Multiple regression is the workhorse of predictive modeling. Each coefficient tells you the effect of one feature while holding others constant. Always evaluate on a test set and check for multicollinearity.

---

## Next Lecture

In [Lecture 09: Feature Scaling](09-scale-lecture.md), we'll learn about different scaling techniques and when to use each one.
