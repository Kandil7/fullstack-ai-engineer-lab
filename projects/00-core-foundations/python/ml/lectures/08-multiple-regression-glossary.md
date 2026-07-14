# Glossary: Multiple Regression

## Quick Reference Table

| Term | Definition | Category |
|------|-----------|----------|
| Multiple Regression | Regression with multiple features | Algorithm |
| Coefficient | Weight for each feature | Parameter |
| Intercept | Base prediction when all features = 0 | Parameter |
| Feature Importance | Relative contribution of features | Concept |
| Multicollinearity | High correlation between features | Problem |
| Adjusted R² | R² adjusted for number of features | Metric |
| Standardized Coefficients | Coefficients on same scale | Technique |
| Variance Inflation Factor | Measure of multicollinearity | Metric |
| Partial Regression | Effect of one feature holding others constant | Concept |
| Control Variable | Feature held constant in analysis | Concept |
| Ordinary Least Squares | Method for fitting regression | Method |
| Matrix Notation | y = Xb + e | Formalism |
| Design Matrix | Matrix of feature values | Data Structure |
| Residual | Difference between actual and predicted | Concept |
| Heteroscedasticity | Non-constant variance of residuals | Problem |
| Homoscedasticity | Constant variance of residuals | Goal |
| Linearity | Linear relationship assumption | Assumption |
| Independence | Observations are independent | Assumption |
| Normality | Residuals are normally distributed | Assumption |
| Endogeneity | Correlation between features and error | Problem |

---

## Detailed Definitions

### C

#### Coefficient
**Definition:** The weight or multiplier assigned to each feature in a multiple regression model. Represents the expected change in the target for a one-unit change in that feature, holding all other features constant.

**Example:**
```python
from sklearn.linear_model import LinearRegression
import numpy as np

X = np.array([
    [1500, 3, 10],
    [2000, 4, 5],
    [1200, 2, 15],
    [1800, 3, 8],
    [2200, 4, 3]
])
y = np.array([300000, 450000, 250000, 400000, 500000])

model = LinearRegression()
model.fit(X, y)

# Coefficients for each feature
print(f"Square feet coeff: {model.coef_[0]:.2f}")
print(f"Bedrooms coeff: {model.coef_[1]:.2f}")
print(f"Age coeff: {model.coef_[2]:.2f}")
```

**Interpretation:**
- Positive coefficient → feature increases target
- Negative coefficient → feature decreases target
- Magnitude → strength of effect

**Related Terms:** Intercept, Feature Importance, Standardized Coefficients

---

### F

#### Feature Importance
**Definition:** A measure of how much each feature contributes to the model's predictions. In linear regression, this can be derived from coefficient magnitudes (when features are scaled).

**Example:**
```python
import numpy as np

# Absolute coefficients as importance
abs_coef = np.abs(model.coef_)
importance = abs_coef / abs_coef.sum()

feature_names = ['Square Feet', 'Bedrooms', 'Age']
for name, imp in sorted(zip(feature_names, importance), 
                       key=lambda x: x[1], reverse=True):
    print(f"  {name}: {imp:.3f} ({imp*100:.1f}%)")
```

**Related Terms:** Coefficients, Permutation Importance, Feature Selection

---

### I

#### Intercept
**Definition:** The predicted value of the target when all features are zero. Also called the constant or bias term.

**Example:**
```python
model = LinearRegression()
model.fit(X, y)

print(f"Intercept: {model.intercept_:.2f}")
# If intercept = 50000, then a house with 0 sqft, 0 bedrooms,
# and 0 years age would be predicted to cost $50,000
# (often not meaningful in practice)
```

**Related Terms:** Coefficient, Bias, Constant

---

### M

#### Multicollinearity
**Definition:** When two or more features in a multiple regression model are highly correlated, making it difficult to isolate the individual effect of each feature.

**Example:**
```python
import numpy as np
import pandas as pd

# Create correlated features
np.random.seed(42)
x1 = np.random.rand(100)
x2 = x1 * 0.9 + np.random.randn(100) * 0.1  # Highly correlated with x1

# Check correlation
correlation = np.corrcoef(x1, x2)[0, 1]
print(f"Correlation: {correlation:.4f}")  # Close to 1.0

# This causes unstable coefficients
```

**Signs of multicollinearity:**
- Coefficients change dramatically when features are added/removed
- High R² but individual coefficients are not significant
- Standard errors of coefficients are large

**Solutions:**
- Remove one of the correlated features
- Use dimensionality reduction (PCA)
- Use regularization (Ridge, Lasso)

**Related Terms:** Variance Inflation Factor, Correlation, Regularization

#### Multiple Linear Regression
**Definition:** An extension of simple linear regression that models the relationship between two or more features and a target using a linear equation.

**Equation:**
```
y = b₀ + b₁x₁ + b₂x₂ + ... + bₙxₙ
```

**Example:**
```python
from sklearn.linear_model import LinearRegression

# Multiple features
X = np.array([
    [1500, 3, 10],  # sqft, bedrooms, age
    [2000, 4, 5],
    [1200, 2, 15]
])
y = np.array([300000, 450000, 250000])

model = LinearRegression()
model.fit(X, y)

print(f"Coefficients: {model.coef_}")
print(f"Intercept: {model.intercept_:.2f}")

# Predict
new_house = np.array([[1800, 3, 5]])
prediction = model.predict(new_house)
print(f"Predicted price: ${prediction[0]:,.0f}")
```

**Related Terms:** Simple Linear Regression, Coefficients, Feature Matrix

---

### S

#### Standardized Coefficients
**Definition:** Coefficients obtained after standardizing features (mean=0, std=1). Allows direct comparison of feature importance regardless of original scales.

**Example:**
```python
from sklearn.preprocessing import StandardScaler

# Standardize features
scaler = StandardScaler()
X_standardized = scaler.fit_transform(X)

model = LinearRegression()
model.fit(X_standardized, y)

# Now coefficients are directly comparable
print("Standardized coefficients:")
for name, coef in zip(feature_names, model.coef_):
    print(f"  {name}: {coef:.2f}")
# Larger absolute value = more important
```

**Related Terms:** StandardScaler, Feature Importance, Coefficients

---

### V

#### Variance Inflation Factor (VIF)
**Definition:** A measure of how much the variance of a coefficient is inflated due to multicollinearity. VIF > 5-10 indicates problematic multicollinearity.

**Formula:**
```
VIF = 1 / (1 - R²ᵢ)
```
where R²ᵢ is the R² from regressing feature i on all other features.

**Example:**
```python
import numpy as np
from sklearn.linear_model import LinearRegression

def calculate_vif(X):
    vif_scores = []
    for i in range(X.shape[1]):
        # Regress feature i on all other features
        X_other = np.delete(X, i, axis=1)
        y_i = X[:, i]
        
        model = LinearRegression()
        model.fit(X_other, y_i)
        r2 = model.score(X_other, y_i)
        
        vif = 1 / (1 - r2) if r2 < 1 else np.inf
        vif_scores.append(vif)
    return vif_scores

vif_scores = calculate_vif(X)
for name, vif in zip(feature_names, vif_scores):
    print(f"  {name}: VIF = {vif:.2f}")
```

**Interpretation:**
- VIF = 1: No multicollinearity
- VIF 1-5: Moderate multicollinearity
- VIF > 5-10: High multicollinearity (problematic)

**Related Terms:** Multicollinearity, Correlation, Regularization

---

## Key Formulas

| Formula | Expression | Description |
|---------|-----------|-------------|
| Multiple regression | `y = b₀ + Σbᵢxᵢ` | Linear combination |
| Coefficient | `b = (X'X)⁻¹X'y` | Matrix solution |
| R² | `1 - RSS/TSS` | Variance explained |
| Adjusted R² | `1 - (1-R²)(n-1)/(n-p-1)` | Penalizes features |
| VIF | `1/(1-R²ᵢ)` | Multicollinearity measure |

---

## Python Import Cheat Sheet

```python
# Linear Regression
from sklearn.linear_model import LinearRegression

# Scaling
from sklearn.preprocessing import StandardScaler

# Metrics
from sklearn.metrics import r2_score, mean_squared_error

# Train/test split
from sklearn.model_selection import train_test_split

# Pandas for data
import pandas as pd

# Statsmodels for detailed statistics (optional)
import statsmodels.api as sm

# Workflow
model = LinearRegression()
model.fit(X_train, y_train)
print(f"Coefficients: {model.coef_}")
print(f"Intercept: {model.intercept_}")
print(f"R²: {model.score(X_test, y_test):.4f}")
```
