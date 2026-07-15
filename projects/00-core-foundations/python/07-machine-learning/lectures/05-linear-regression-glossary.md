# Glossary: Linear Regression

## Quick Reference Table

| Term | Definition | Category |
|------|-----------|----------|
| Linear Regression | Models linear relationship between X and y | Algorithm |
| Simple Regression | One feature (y = mx + b) | Type |
| Multiple Regression | Multiple features | Type |
| Coefficient | Weight assigned to each feature | Parameter |
| Intercept | Value of y when all features are 0 | Parameter |
| Slope | Change in y per unit change in x | Parameter |
| Best Fit Line | Line that minimizes squared residuals | Concept |
| Residual | Difference between actual and predicted | Metric |
| MSE | Mean Squared Error | Metric |
| RMSE | Root Mean Squared Error | Metric |
| R² | Coefficient of Determination | Metric |
| OLS | Ordinary Least Squares | Method |
| LinearRegression | Scikit-learn linear regression class | Tool |
| .fit() | Train the model | Method |
| .predict() | Make predictions | Method |
| .score() | Get R² score | Method |
| .coef_ | Learned coefficients | Attribute |
| .intercept_ | Learned intercept | Attribute |
| Overfitting | Model too complex for data | Problem |
| Underfitting | Model too simple for data | Problem |

---

## Detailed Definitions

### C

#### Coefficient
**Definition:** The weight or multiplier assigned to each feature in a linear regression model. Also called the slope or weight. Indicates the direction and magnitude of the relationship.

**Example:**
```python
from sklearn.linear_model import LinearRegression
import numpy as np

X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
y = np.array([10, 20, 30, 40])

model = LinearRegression()
model.fit(X, y)

print(f"Coefficients: {model.coef_}")  # [5, 5]
print(f"Feature 1 coefficient: {model.coef_[0]}")
print(f"Feature 2 coefficient: {model.coef_[1]}")
```

**Interpretation:**
- Positive coefficient → positive relationship with target
- Negative coefficient → negative relationship with target
- Magnitude → strength of the relationship

**Related Terms:** Intercept, Weight, Parameter, Feature Importance

#### Confidence Interval
**Definition:** A range of values that is likely to contain the true value of an unknown parameter, with a certain level of confidence (typically 95%).

**Example:**
```python
import statsmodels.api as sm

X = sm.add_constant(X)  # Add intercept
model = sm.OLS(y, X).fit()
print(model.conf_int(alpha=0.05))  # 95% confidence intervals
```

**Related Terms:** P-value, Statistical Significance

---

### I

#### Intercept
**Definition:** The value of the predicted target when all features are zero. Also called the bias or constant term. Represents where the regression line crosses the y-axis.

**Example:**
```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)

print(f"Intercept: {model.intercept_:.2f}")
# If intercept = 50000, then when all features are 0,
# the predicted value is 50000
```

**Related Terms:** Coefficient, Bias, Constant

---

### L

#### Linear Regression
**Definition:** A statistical method that models the relationship between a dependent variable and one or more independent variables by fitting a linear equation to observed data.

**Equation:**
```
Simple: y = b₀ + b₁x
Multiple: y = b₀ + b₁x₁ + b₂x₂ + ... + bₙxₙ
```

**Example:**
```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import numpy as np

# Generate data
np.random.seed(42)
X = np.random.rand(100, 1) * 10
y = 2.5 * X.squeeze() + 5 + np.random.randn(100) * 2

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate
r2 = r2_score(y_test, model.predict(X_test))
print(f"Coefficient: {model.coef_[0]:.2f}")
print(f"Intercept: {model.intercept_:.2f}")
print(f"R²: {r2:.4f}")
```

**Related Terms:** Simple Linear Regression, Multiple Linear Regression, OLS

---

### M

#### Mean Squared Error (MSE)
**Definition:** The average of the squared differences between predicted and actual values. Measures the average squared deviation of predictions from the truth.

**Formula:**
```
MSE = (1/n) × Σ(yᵢ - ŷᵢ)²
```

**Example:**
```python
from sklearn.metrics import mean_squared_error
import numpy as np

y_actual = np.array([3, 5, 7, 9])
y_predicted = np.array([2.5, 5.2, 6.8, 9.1])

mse = mean_squared_error(y_actual, y_predicted)
print(f"MSE: {mse:.4f}")  # 0.0825
```

**Related Terms:** RMSE, MAE, R², Loss Function

#### Multiple Linear Regression
**Definition:** An extension of simple linear regression that uses multiple features to predict the target. The model learns a coefficient for each feature.

**Equation:**
```
y = b₀ + b₁x₁ + b₂x₂ + ... + bₙxₙ
```

**Example:**
```python
from sklearn.linear_model import LinearRegression

# Features: square_feet, bedrooms, age
X = np.array([
    [1500, 3, 10],
    [2000, 4, 5],
    [1200, 2, 15]
])
y = np.array([300000, 450000, 250000])

model = LinearRegression()
model.fit(X, y)

print(f"Coefficients: {model.coef_}")
# [100, 50000, -2000] means:
# Each sq ft adds $100, each bedroom adds $50k, each year of age reduces $2k
```

**Related Terms:** Simple Linear Regression, Feature Importance, Multicollinearity

---

### O

#### OLS (Ordinary Least Squares)
**Definition:** The most common method for fitting linear regression models. It minimizes the sum of squared residuals between observed and predicted values.

**Objective:**
```
Minimize: Σ(yᵢ - ŷᵢ)²
```

**Example:**
```python
import statsmodels.api as sm

# OLS with statsmodels (provides statistical summary)
X_with_const = sm.add_constant(X)  # Add intercept term
model = sm.OLS(y, X_with_const).fit()
print(model.summary())
```

**Related Terms:** Linear Regression, Residual, Least Squares

---

### P

#### Prediction
**Definition:** The output of a trained model when given new input data. In linear regression, predictions are calculated using the learned coefficients and intercept.

**Example:**
```python
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on new data
X_new = np.array([[2000, 3, 5]])  # 2000 sqft, 3 bedrooms, 5 years old
predicted_price = model.predict(X_new)
print(f"Predicted price: ${predicted_price[0]:,.0f}")
```

**Related Terms:** Inference, Output, Coefficient, Intercept

---

### R

#### R-squared (R²)
**Definition:** A statistical measure of how well the regression predictions approximate the real data points. R² = 1 indicates perfect fit; R² = 0 indicates the model is no better than predicting the mean.

**Formula:**
```
R² = 1 - (SS_res / SS_tot)
SS_res = Σ(yᵢ - ŷᵢ)²  (residual sum of squares)
SS_tot = Σ(yᵢ - ȳ)²    (total sum of squares)
```

**Example:**
```python
from sklearn.metrics import r2_score
import numpy as np

y_actual = np.array([3, 5, 7, 9, 11])
y_predicted = np.array([2.8, 5.1, 6.9, 9.2, 10.8])

r2 = r2_score(y_actual, y_predicted)
print(f"R²: {r2:.4f}")  # 0.9976
```

**Interpretation:**
- R² = 1.0: Perfect predictions
- R² = 0.75: Model explains 75% of variance
- R² = 0.0: Model explains none (same as predicting mean)
- R² < 0: Model is worse than predicting mean

**Related Terms:** Adjusted R², Explained Variance, MSE

#### Residual
**Definition:** The difference between the actual (observed) value and the predicted value. Also called the error or prediction error.

**Formula:**
```
Residual = Actual - Predicted = y - ŷ
```

**Example:**
```python
model = LinearRegression()
model.fit(X, y)

y_pred = model.predict(X)
residuals = y - y_pred

print(f"Mean residual: {residuals.mean():.4f}")  # Should be ≈ 0
print(f"Residual std: {residuals.std():.4f}")
```

**Related Terms:** Error, SSE, MSE, Best Fit Line

#### RMSE (Root Mean Squared Error)
**Definition:** The square root of the average squared differences between predicted and actual values. Provides error in the same units as the target variable.

**Formula:**
```
RMSE = √MSE = √((1/n) × Σ(yᵢ - ŷᵢ)²)
```

**Example:**
```python
from sklearn.metrics import mean_squared_error
import numpy as np

y_actual = np.array([3, 5, 7, 9])
y_predicted = np.array([2.5, 5.2, 6.8, 9.1])

rmse = np.sqrt(mean_squared_error(y_actual, y_predicted))
print(f"RMSE: {rmse:.4f}")  # 0.2872
```

**Related Terms:** MSE, MAE, R²

---

### S

#### Simple Linear Regression
**Definition:** Linear regression with a single feature. Models the relationship between one independent variable and one dependent variable.

**Equation:**
```
y = b₀ + b₁x
```

**Example:**
```python
from sklearn.linear_model import LinearRegression

X = np.array([[1], [2], [3], [4], [5]])  # One feature
y = np.array([2, 4, 6, 8, 10])

model = LinearRegression()
model.fit(X, y)

print(f"y = {model.coef_[0]:.2f}x + {model.intercept_:.2f}")
# y = 2.00x + 0.00
```

**Related Terms:** Multiple Linear Regression, Linear Regression

#### Slope
**Definition:** The coefficient in simple linear regression that represents the change in y for each unit change in x. In multiple regression, each coefficient represents the effect of its feature.

**Example:**
```python
# In y = 2x + 3:
# Slope = 2 means: for each +1 in x, y increases by 2

model = LinearRegression()
model.fit(X, y)
slope = model.coef_[0]
print(f"Slope: {slope:.2f}")
```

**Related Terms:** Coefficient, Intercept, Gradient

---

## Key Formulas

| Formula | Expression | Description |
|---------|-----------|-------------|
| Line equation | `y = mx + b` | Simple linear regression |
| Multiple regression | `y = b₀ + Σbᵢxᵢ` | Multiple features |
| Slope (manual) | `Σ((x-x̄)(y-ȳ)) / Σ(x-x̄)²` | Calculate slope |
| Intercept (manual) | `ȳ - m×x̄` | Calculate intercept |
| MSE | `(1/n) × Σ(y-ŷ)²` | Average squared error |
| RMSE | `√MSE` | Error in original units |
| R² | `1 - SS_res/SS_tot` | Proportion of variance explained |

---

## Python Import Cheat Sheet

```python
# Linear Regression
from sklearn.linear_model import LinearRegression

# Metrics
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# Train/test split
from sklearn.model_selection import train_test_split

# Statistical analysis (optional)
import statsmodels.api as sm

# Visualization (optional)
import matplotlib.pyplot as plt

# Basic workflow
model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
r2 = r2_score(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
```
