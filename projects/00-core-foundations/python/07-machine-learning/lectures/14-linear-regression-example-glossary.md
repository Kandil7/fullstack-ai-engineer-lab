# Glossary: Linear Regression Example (Lecture 14)

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Linear Regression | Models relationship between features and continuous target | `LinearRegression()` |
| Intercept (β₀) | Baseline prediction when all features are 0 | `model.intercept_` |
| Coefficients (β) | Weight for each feature showing impact | `model.coef_` |
| R² Score | Proportion of variance explained (0-1) | `r2_score(y_true, y_pred)` |
| RMSE | Root Mean Squared Error (same unit as target) | `np.sqrt(mean_squared_error())` |
| MAE | Mean Absolute Error (average absolute deviation) | `mean_absolute_error()` |
| Train/Test Split | Dividing data for training and evaluation | `train_test_split()` |
| Feature Scaling | Normalizing features to same scale | `StandardScaler()` |
| Overfitting | Model performs well on training but poorly on test | Train R² >> Test R² |
| Underfitting | Model performs poorly on both train and test | Both scores low |
| Pipeline | Chained preprocessing and model steps | `Pipeline()` |
| Residual | Difference between actual and predicted value | `y - y_pred` |
| Multicollinearity | High correlation between features | VIF > 5 |
| Bias | Error from wrong assumptions in model | Underfitting |
| Variance | Error from sensitivity to training data | Overfitting |

---

## Detailed Term Definitions

### Linear Regression

**Definition:** A statistical method that models the relationship between a dependent variable (target) and one or more independent variables (features) by fitting a linear equation to observed data.

**Formula:**
```
y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ + ε
```

**Example:**
```python
from sklearn.linear_model import LinearRegression
import numpy as np

# Simple linear regression
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 5, 4, 6])

model = LinearRegression()
model.fit(X, y)

print(f"Coefficient: {model.coef_[0]:.4f}")
print(f"Intercept: {model.intercept_:.4f}")

# Predict
X_new = np.array([[6]])
prediction = model.predict(X_new)
print(f"Prediction for X=6: {prediction[0]:.4f}")
```

**Related Terms:** Multiple Linear Regression, Polynomial Regression, Ridge Regression

---

### Intercept (β₀)

**Definition:** The predicted value of the target variable when all feature values are zero. Also called the bias term.

**Example:**
```python
from sklearn.linear_model import LinearRegression
import numpy as np

X = np.array([[1], [2], [3], [4], [5]])
y = np.array([3, 5, 7, 9, 11])  # y = 2x + 1

model = LinearRegression()
model.fit(X, y)

print(f"Intercept (β₀): {model.intercept_:.4f}")
print(f"Coefficient (β₁): {model.coef_[0]:.4f}")

# When X=0, y = intercept = 1.0
# When X=1, y = 1.0 + 2.0*1 = 3.0
```

**Related Terms:** Coefficients, Bias Term, Baseline

---

### Coefficients (β₁, β₂, ..., βₙ)

**Definition:** Weights assigned to each feature, representing the change in the target variable for a one-unit change in the feature (holding other features constant).

**Example:**
```python
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

np.random.seed(42)
X = pd.DataFrame({
    'sqft': [1000, 1500, 2000, 2500, 3000],
    'bedrooms': [2, 3, 3, 4, 4]
})
y = np.array([200000, 275000, 350000, 425000, 500000])

model = LinearRegression()
model.fit(X, y)

print("Coefficients:")
for feature, coef in zip(X.columns, model.coef_):
    print(f"  {feature}: {coef:.2f}")

# Interpretation:
# Each additional sqft adds ~$150 to price
# Each additional bedroom adds ~$25000 to price
```

**Related Terms:** Feature Importance, Weight, Partial Regression Coefficient

---

### R² Score (Coefficient of Determination)

**Definition:** The proportion of variance in the target variable that is predictable from the features. Ranges from 0 to 1, where 1 indicates perfect prediction.

**Formula:**
```
R² = 1 - (SS_res / SS_tot)
SS_res = Σ(yᵢ - ŷᵢ)²  (residual sum of squares)
SS_tot = Σ(yᵢ - ȳ)²   (total sum of squares)
```

**Example:**
```python
from sklearn.metrics import r2_score
import numpy as np

y_actual = np.array([3, -0.5, 2, 7])
y_predicted = np.array([2.5, 0.0, 2, 8])

r2 = r2_score(y_actual, y_predicted)
print(f"R² Score: {r2:.4f}")
# Output: 0.9486 (explains 94.86% of variance)

# Manual calculation
ss_res = np.sum((y_actual - y_predicted) ** 2)
ss_tot = np.sum((y_actual - np.mean(y_actual)) ** 2)
r2_manual = 1 - (ss_res / ss_tot)
print(f"Manual R²: {r2_manual:.4f}")
```

**Related Terms:** Explained Variance, Goodness of Fit, RMSE

---

### RMSE (Root Mean Squared Error)

**Definition:** The square root of the average squared differences between predicted and actual values. Has the same unit as the target variable.

**Formula:**
```
RMSE = √[(1/n) Σ(yᵢ - ŷᵢ)²]
```

**Example:**
```python
from sklearn.metrics import mean_squared_error
import numpy as np

y_actual = np.array([3, -0.5, 2, 7])
y_predicted = np.array([2.5, 0.0, 2, 8])

mse = mean_squared_error(y_actual, y_predicted)
rmse = np.sqrt(mse)

print(f"MSE: {mse:.4f}")
print(f"RMSE: {rmse:.4f}")
# Output: MSE: 0.375, RMSE: 0.6124
```

**Interpretation:**
- RMSE = 25000 means average prediction error is $25,000
- Lower RMSE is better
- Sensitive to outliers (penalizes large errors more)

**Related Terms:** MSE, MAE, Residuals

---

### MAE (Mean Absolute Error)

**Definition:** The average of absolute differences between predicted and actual values. Less sensitive to outliers than RMSE.

**Formula:**
```
MAE = (1/n) Σ|yᵢ - ŷᵢ|
```

**Example:**
```python
from sklearn.metrics import mean_absolute_error
import numpy as np

y_actual = np.array([3, -0.5, 2, 7])
y_predicted = np.array([2.5, 0.0, 2, 8])

mae = mean_absolute_error(y_actual, y_predicted)
print(f"MAE: {mae:.4f}")
# Output: 0.5

# Manual calculation
mae_manual = np.mean(np.abs(y_actual - y_predicted))
print(f"Manual MAE: {mae_manual:.4f}")
```

**Interpretation:**
- MAE = 20000 means average absolute error is $20,000
- More robust to outliers than RMSE
- Easier to interpret (direct average error)

**Related Terms:** RMSE, MSE, Residuals

---

### Train/Test Split

**Definition:** Dividing the dataset into training and testing sets to evaluate model performance on unseen data.

**Example:**
```python
from sklearn.model_selection import train_test_split
import numpy as np

X = np.random.randn(100, 5)
y = np.random.randn(100)

# 80/20 split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Total samples: {len(X)}")
print(f"Training samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")

# With stratification (for classification)
y_class = (y > 0).astype(int)
X_train, X_test, y_train, y_test = train_test_split(
    X, y_class, test_size=0.2, random_state=42, stratify=y_class
)
```

**Parameters:**
- `test_size`: Fraction for test set (0.2 = 20%)
- `random_state`: Seed for reproducibility
- `stratify`: Maintain class distribution (classification)

**Related Terms:** Validation Set, Cross-Validation, Data Leakage

---

### Feature Scaling

**Definition:** Normalizing features to have similar scales, important for algorithms sensitive to feature magnitudes.

**Example:**
```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import numpy as np

X = np.array([[1000, 2], [2000, 3], [3000, 4], [4000, 5]])

# StandardScaler (mean=0, std=1)
scaler_standard = StandardScaler()
X_standard = scaler_standard.fit_transform(X)
print("StandardScaler:")
print(X_standard)

# MinMaxScaler (range 0-1)
scaler_minmax = MinMaxScaler()
X_minmax = scaler_minmax.fit_transform(X)
print("\nMinMaxScaler:")
print(X_minmax)
```

**Why scale?**
- Features have different units (sqft vs bedrooms)
- Some algorithms (KNN, SVM, gradient descent) require scaling
- Coefficients become comparable

**Related Terms:** StandardScaler, MinMaxScaler, Normalization, Standardization

---

### Overfitting

**Definition:** When a model learns noise in training data instead of the underlying pattern, performing well on training but poorly on test data.

**Example:**
```python
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score
import numpy as np

np.random.seed(42)
X = np.random.randn(100, 1)
y = 2 * X.squeeze() + np.random.randn(100) * 0.5

# Good fit
model_1 = LinearRegression()
model_1.fit(X, y)
train_r2_1 = r2_score(y, model_1.predict(X))

# Overfitting (high-degree polynomial)
poly = PolynomialFeatures(degree=15)
X_poly = poly.fit_transform(X)
model_15 = LinearRegression()
model_15.fit(X_poly, y)
train_r2_15 = r2_score(y, model_15.predict(X_poly))

print(f"Linear model - Train R²: {train_r2_1:.4f}")
print(f"Polynomial (15) - Train R²: {train_r2_15:.4f}")

# The polynomial model overfits (high train R² but will fail on test)
```

**Solutions:**
- Use simpler models
- Regularization (Ridge, Lasso)
- More training data
- Cross-validation

**Related Terms:** Underfitting, Bias-Variance Tradeoff, Regularization

---

### Underfitting

**Definition:** When a model is too simple to capture the underlying pattern in the data, performing poorly on both training and test data.

**Example:**
```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import numpy as np

np.random.seed(42)
X = np.random.randn(100, 1)
y = X.squeeze() ** 2 + np.random.randn(100) * 0.5  # Non-linear relationship

# Linear model underfits quadratic relationship
model = LinearRegression()
model.fit(X, y)
train_r2 = r2_score(y, model.predict(X))

print(f"Linear model on quadratic data - Train R²: {train_r2:.4f}")
# Low R² indicates underfitting
```

**Solutions:**
- Use more complex models
- Add polynomial features
- Add more features
- Reduce regularization

**Related Terms:** Overfitting, Bias-Variance Tradeoff, Model Complexity

---

### Pipeline

**Definition:** A sequence of processing steps chained together, ensuring consistent preprocessing and model training.

**Example:**
```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np

np.random.seed(42)
X = np.random.randn(100, 3)
y = X @ np.array([1, 2, 3]) + np.random.randn(100) * 0.5

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Create pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LinearRegression())
])

# Train (automatically scales)
pipeline.fit(X_train, y_train)

# Predict (automatically scales)
score = pipeline.score(X_test, y_test)
print(f"Pipeline R²: {score:.4f}")

# Save and load
import joblib
joblib.dump(pipeline, 'model_pipeline.pkl')
loaded_pipeline = joblib.load('model_pipeline.pkl')
```

**Benefits:**
- Prevents data leakage
- Reproducible workflows
- Easy to save/load
- Clean code

**Related Terms:** Transformer, Estimator, Data Leakage

---

### Residual

**Definition:** The difference between the actual and predicted value for a data point. Residual = y - ŷ.

**Example:**
```python
from sklearn.linear_model import LinearRegression
import numpy as np

X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 5, 4, 6])

model = LinearRegression()
model.fit(X, y)

y_pred = model.predict(X)
residuals = y - y_pred

print("Actual:", y)
print("Predicted:", np.round(y_pred, 2))
print("Residuals:", np.round(residuals, 2))

# Residual analysis
print(f"\nMean residual: {np.mean(residuals):.4f}")
print(f"Std residual: {np.std(residuals):.4f}")
```

**Analysis:**
- Mean residual should be ~0
- Residuals should be randomly distributed
- No pattern in residuals vs predicted plot

**Related Terms:** Error Term, Residual Analysis, Homoscedasticity

---

### Multicollinearity

**Definition:** When two or more independent variables are highly correlated, making it difficult to isolate their individual effects on the target.

**Example:**
```python
import numpy as np
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor

np.random.seed(42)
n = 100

# Create multicollinear features
x1 = np.random.randn(n)
x2 = x1 * 0.9 + np.random.randn(n) * 0.1  # Highly correlated with x1
x3 = np.random.randn(n)  # Independent

df = pd.DataFrame({'x1': x1, 'x2': x2, 'x3': x3})

# Calculate VIF
def calculate_vif(df):
    vif_data = pd.DataFrame()
    vif_data["feature"] = df.columns
    vif_data["VIF"] = [variance_inflation_factor(df.values, i) 
                       for i in range(df.shape[1])]
    return vif_data

print(calculate_vif(df))
# x1 and x2 will have high VIF (>5-10)
```

**Solutions:**
- Remove one of the correlated features
- Use PCA for dimensionality reduction
- Use regularization (Ridge, Lasso)

**Related Terms:** Variance Inflation Factor (VIF), Feature Selection, Regularization

---

### Bias

**Definition:** Error due to wrong assumptions in the learning algorithm, causing the model to miss relevant relations. High bias leads to underfitting.

**Example:**
```python
# Linear model trying to fit non-linear data = High Bias
# The model assumes linearity but reality is quadratic

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

np.random.seed(42)
X = np.random.randn(100, 1)
y = X.squeeze() ** 2  # Quadratic relationship

model = LinearRegression()
model.fit(X, y)

y_pred = model.predict(X)
bias = np.mean((y - np.mean(y)) ** 2) - np.var(y - y_pred)
print(f"Approximate bias²: {bias:.4f}")
```

**Related Terms:** Variance, Bias-Variance Tradeoff, Underfitting

---

### Variance

**Definition:** Error due to sensitivity to small fluctuations in the training set. High variance leads to overfitting.

**Example:**
```python
# High-degree polynomial = High Variance
# Small changes in training data cause large changes in model

import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

np.random.seed(42)
X = np.random.randn(50, 1)
y = X.squeeze() ** 2 + np.random.randn(50) * 0.5

# Fit high-degree polynomial
poly = PolynomialFeatures(degree=10)
X_poly = poly.fit_transform(X)
model = LinearRegression()
model.fit(X_poly, y)

# Small perturbation causes large model change
X_test = np.array([[1.0]])
X_test_poly = poly.transform(X_test)
pred1 = model.predict(X_test_poly)[0]

# Add noise to training data
y_noisy = y + np.random.randn(50) * 0.1
model2 = LinearRegression()
model2.fit(X_poly, y_noisy)
pred2 = model2.predict(X_test_poly)[0]

print(f"Prediction 1: {pred1:.4f}")
print(f"Prediction 2: {pred2:.4f}")
print(f"Difference: {abs(pred1 - pred2):.4f}")
```

**Related Terms:** Bias, Bias-Variance Tradeoff, Overfitting

---

### Bias-Variance Tradeoff

**Definition:** The balance between two sources of error: bias (underfitting) and variance (overfitting). The goal is to find the model complexity that minimizes total error.

**Example:**
```python
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

np.random.seed(42)
X = np.random.randn(100, 1)
y = X.squeeze() ** 2 + np.random.randn(100) * 0.5

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Test different polynomial degrees
for degree in [1, 3, 5, 10, 15]:
    poly = PolynomialFeatures(degree=degree)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)
    
    model = LinearRegression()
    model.fit(X_train_poly, y_train)
    
    train_mse = mean_squared_error(y_train, model.predict(X_train_poly))
    test_mse = mean_squared_error(y_test, model.predict(X_test_poly))
    
    print(f"Degree {degree:2d}: Train MSE={train_mse:.4f}, Test MSE={test_mse:.4f}")

# Optimal: Degree 2 (matches true relationship)
```

**Related Terms:** Bias, Variance, Model Complexity, Regularization

---

## Formulas Summary

| Formula | Expression |
|---------|-----------|
| Linear Regression | y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ |
| R² Score | R² = 1 - (SS_res / SS_tot) |
| RMSE | RMSE = √[(1/n) Σ(yᵢ - ŷᵢ)²] |
| MAE | MAE = (1/n) Σ|yᵢ - ŷᵢ| |
| MSE | MSE = (1/n) Σ(yᵢ - ŷᵢ)² |
| Residual | e = y - ŷ |
| VIF | VIF = 1 / (1 - R²) |

---

## Code Snippets Quick Reference

```python
# Linear Regression
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# Evaluation
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)

# Train/Test Split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Pipeline
from sklearn.pipeline import Pipeline
pipeline = Pipeline([('scaler', StandardScaler()), ('model', LinearRegression())])

# Cross-Validation
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5, scoring='r2')

# Save Model
import joblib
joblib.dump(model, 'model.pkl')
model = joblib.load('model.pkl')
```

---

## Common Pitfalls

1. **Not scaling features** — Coefficients become incomparable
2. **Fitting scaler on test data** — Data leakage
3. **Not checking for overfitting** — Always compare train/test scores
4. **Ignoring assumptions** — Check residual plots
5. **Not using pipelines** — Manual scaling leads to errors

---

## Further Reading

- [Scikit-learn - Linear Models](https://scikit-learn.org/stable/modules/linear_model.html)
- [Wikipedia - Linear Regression](https://en.wikipedia.org/wiki/Linear_regression)
- [STATSmodels - Linear Regression](https://www.statsmodels.org/stable/regression.html)
