# Lecture 14: Linear Regression — Complete End-to-End Example

## Topic Overview

This lecture presents a complete, real-world linear regression project from start to finish. We'll build a house price prediction model, covering every step of the ML pipeline: problem definition, data generation, exploration, preparation, training, evaluation, and interpretation. This is a practical walkthrough that demonstrates how linear regression works in production scenarios.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Define a regression problem and identify features/targets
2. Generate realistic synthetic data for experimentation
3. Perform data exploration and understand distributions
4. Engineer features and check correlations
5. Split data into training and test sets properly
6. Scale features using StandardScaler
7. Train a linear regression model with scikit-learn
8. Evaluate models using R², RMSE, and MAE
9. Interpret model coefficients for business insights
10. Make predictions on new, unseen data

---

## Key Concepts

### 1. The Linear Regression Model

Linear regression models the relationship between features (X) and a continuous target (y) using a linear equation:

```
y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ + ε
```

Where:
- `y` = predicted value (target)
- `β₀` = intercept (bias term)
- `β₁, β₂, ..., βₙ` = coefficients (weights)
- `x₁, x₂, ..., xₙ` = features
- `ε` = error term (noise)

### 2. Cost Function (Mean Squared Error)

The model learns by minimizing the cost function:

```
MSE = (1/n) Σ(yᵢ - ŷᵢ)²
```

Where:
- `yᵢ` = actual value
- `ŷᵢ` = predicted value
- `n` = number of samples

### 3. Evaluation Metrics

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **R² Score** | 1 - (SS_res / SS_tot) | Proportion of variance explained (0-1) |
| **RMSE** | √(MSE) | Average prediction error (same unit as target) |
| **MAE** | (1/n) Σ|yᵢ - ŷᵢ| | Average absolute error |

### 4. Assumptions of Linear Regression

1. **Linearity**: Relationship between features and target is linear
2. **Independence**: Observations are independent
3. **Homoscedasticity**: Constant variance of residuals
4. **Normality**: Residuals are normally distributed
5. **No multicollinearity**: Features are not highly correlated

---

## Complete Code Walkthrough

### Step 1: Problem Definition

```python
print("="*60)
print("LINEAR REGRESSION PROJECT: House Price Prediction")
print("="*60)

print("\nStep 1: Problem Definition")
print("- Predict house prices based on features")
print("- Features: square_feet, bedrooms, age, distance_to_center")
print("- Target: price")
```

**Why this matters:** Always start with a clear problem statement. Define what you're predicting (target) and what information you're using (features).

### Step 2: Data Generation

```python
import numpy as np
import pandas as pd

np.random.seed(42)
n_samples = 500

# Generate features
square_feet = np.random.randint(800, 4000, n_samples)
bedrooms = np.random.randint(1, 6, n_samples)
age = np.random.randint(0, 50, n_samples)
distance_to_center = np.random.uniform(0.5, 20, n_samples)

# Generate target with realistic relationship
price = (50000 + 
         150 * square_feet + 
         25000 * bedrooms - 
         1000 * age - 
         5000 * distance_to_center + 
         np.random.randn(n_samples) * 25000)

# Create DataFrame
df = pd.DataFrame({
    'square_feet': square_feet,
    'bedrooms': bedrooms,
    'age': age,
    'distance_to_center': distance_to_center,
    'price': price
})

print(f"Generated {n_samples} samples")
print(f"Features: square_feet, bedrooms, age, distance_to_center")
print(f"Target: price")
```

**Key insight:** The data generation formula shows the true relationships:
- Each square foot adds ~$150
- Each bedroom adds ~$25,000
- Each year of age reduces price by ~$1,000
- Each km from center reduces price by ~$5,000

### Step 3: Data Exploration

```python
print("\nStep 3: Data Exploration")

# First look at the data
print("\nFirst 5 rows:")
print(df.head())

# Statistical summary
print("\nBasic statistics:")
print(df.describe())

# Data types check
print("\nData types:")
print(df.dtypes)
```

**What to look for:**
- Missing values (NaN)
- Outliers (extreme values)
- Feature ranges (are they similar?)
- Distribution shapes

### Step 4: Feature Engineering

```python
print("\nStep 4: Feature Engineering")

# Check correlations
print("\nFeature correlations with price:")
corr_with_price = df.corr()['price'].drop('price').sort_values(ascending=False)
print(corr_with_price)
```

**Why correlations matter:** Features with higher absolute correlation to the target are likely more predictive. This helps identify which features to keep.

### Step 5: Data Preparation

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

print("\nStep 5: Data Preparation")

# Separate features and target
X = df.drop('price', axis=1)
y = df['price']

print(f"Features shape: {X.shape}")
print(f"Target shape: {y.shape}")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nTraining set: {len(X_train)} samples")
print(f"Test set: {len(X_test)} samples")

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

**Critical concepts:**
- **80/20 split**: 80% training, 20% testing
- **random_state=42**: Ensures reproducibility
- **fit_transform** on training data only
- **transform** on test data (no fitting!)

### Step 6: Model Training

```python
from sklearn.linear_model import LinearRegression

print("\nStep 6: Model Training")

# Train linear regression model
model = LinearRegression()
model.fit(X_train_scaled, y_train)

print("Model trained successfully")
print(f"\nCoefficients:")
for feature, coef in zip(X.columns, model.coef_):
    print(f"  {feature}: {coef:.2f}")
print(f"\nIntercept: {model.intercept_:.2f}")
```

**Interpretation:**
- Coefficients show the impact of each feature (after scaling)
- Positive coefficient: feature increases price
- Negative coefficient: feature decreases price

### Step 7: Model Evaluation

```python
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

print("\nStep 7: Model Evaluation")

# Predictions
y_pred_train = model.predict(X_train_scaled)
y_pred_test = model.predict(X_test_scaled)

# Training metrics
train_r2 = r2_score(y_train, y_pred_train)
train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
train_mae = mean_absolute_error(y_train, y_pred_train)

# Test metrics
test_r2 = r2_score(y_test, y_pred_test)
test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
test_mae = mean_absolute_error(y_test, y_pred_test)

print("\nTraining Set Metrics:")
print(f"  R² Score: {train_r2:.4f}")
print(f"  RMSE: ${train_rmse:,.0f}")
print(f"  MAE: ${train_mae:,.0f}")

print("\nTest Set Metrics:")
print(f"  R² Score: {test_r2:.4f}")
print(f"  RMSE: ${test_rmse:,.0f}")
print(f"  MAE: ${test_mae:,.0f}")
```

**Metrics interpretation:**
- **R² = 0.95** means 95% of price variance is explained by the model
- **RMSE = $25,000** means average prediction error is $25,000
- **MAE = $20,000** means average absolute error is $20,000
- Training and test scores should be similar (no overfitting)

### Step 8: Model Interpretation

```python
print("\nStep 8: Model Interpretation")

# Feature importance
importance = np.abs(model.coef_)
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': importance
}).sort_values('importance', ascending=False)

print("\nFeature Importance (absolute coefficients):")
for _, row in feature_importance.iterrows():
    print(f"  {row['feature']}: {row['importance']:.2f}")

print("\nInterpretation:")
print(f"  - Each additional square foot adds ~${model.coef_[0]:.0f} to price")
print(f"  - Each additional bedroom adds ~${model.coef_[1]:.0f} to price")
print(f"  - Each year of age reduces price by ~${abs(model.coef_[2]):.0f}")
print(f"  - Each km from center reduces price by ~${abs(model.coef_[3]):.0f}")
```

**Business insights:**
- Square footage is the strongest predictor
- Distance from center has negative impact
- Newer houses are valued higher

### Step 9: Making Predictions

```python
print("\nStep 9: Making Predictions")

# New houses to predict
new_houses = pd.DataFrame({
    'square_feet': [1500, 2500, 3500],
    'bedrooms': [3, 4, 5],
    'age': [10, 5, 2],
    'distance_to_center': [5.0, 2.0, 10.0]
})

print("\nNew houses to predict:")
print(new_houses)

# Scale features (use the SAME scaler!)
new_houses_scaled = scaler.transform(new_houses)

# Make predictions
predictions = model.predict(new_houses_scaled)

print("\nPredictions:")
for i, (_, house) in enumerate(new_houses.iterrows()):
    print(f"  House {i+1}: {house['square_feet']} sqft, {house['bedrooms']} bedrooms")
    print(f"    Predicted price: ${predictions[i]:,.0f}")
```

**Important:** Always use the same scaler that was fit on training data!

### Step 10: Model Summary

```python
print("\n" + "="*60)
print("PROJECT SUMMARY")
print("="*60)

print("\nModel Performance:")
print(f"  - R² Score: {test_r2:.4f} (explains {test_r2*100:.1f}% of price variance)")
print(f"  - RMSE: ${test_rmse:,.0f} (average prediction error)")
print(f"  - MAE: ${test_mae:,.0f} (average absolute error)")

print("\nKey Insights:")
print("  - Square footage is the strongest predictor")
print("  - Distance from center negatively impacts price")
print("  - Newer houses are valued higher")
print("  - Additional bedrooms increase value")

print("\nLimitations:")
print("  - Only considers 4 features")
print("  - Assumes linear relationships")
print("  - Does not account for location quality, amenities, etc.")

print("\nNext Steps:")
print("  - Add more features (location, condition, etc.)")
print("  - Try polynomial regression for non-linear relationships")
print("  - Use cross-validation for more robust evaluation")
print("="*60)
```

---

## Common Mistakes to Avoid

### Mistake 1: Not Scaling Features

```python
# WRONG: Using unscaled features
model = LinearRegression()
model.fit(X_train, y_train)  # Works but coefficients are hard to interpret

# CORRECT: Scale features first
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
model.fit(X_train_scaled, y_train)  # Coefficients are now comparable
```

### Mistake 2: Fitting Scaler on Test Data

```python
# WRONG: Fitting scaler on test data (data leakage!)
scaler.fit_transform(X_test)  # DON'T DO THIS!

# CORRECT: Only transform test data
X_test_scaled = scaler.transform(X_test)  # Use fit from training
```

### Mistake 3: Not Checking for Overfitting

```python
# Check if training score >> test score
if train_r2 - test_r2 > 0.1:
    print("WARNING: Possible overfitting!")
    print("Consider: regularization, more data, or simpler model")
```

### Mistake 4: Ignoring Assumptions

```python
import matplotlib.pyplot as plt

# Check residual distribution
residuals = y_test - y_pred_test

plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.scatter(y_pred_test, residuals)
plt.xlabel('Predicted')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted')
plt.axhline(y=0, color='r', linestyle='--')

plt.subplot(1, 2, 2)
plt.hist(residuals, bins=20)
plt.xlabel('Residual')
plt.ylabel('Frequency')
plt.title('Residual Distribution')

plt.tight_layout()
plt.show()
```

---

## Best Practices

### 1. Always Split Data Before Any Preprocessing

```python
# CORRECT workflow:
# 1. Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 2. Fit scaler on training data only
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# 3. Transform test data
X_test_scaled = scaler.transform(X_test)

# 4. Train model
model.fit(X_train_scaled, y_train)

# 5. Evaluate
score = model.score(X_test_scaled, y_test)
```

### 2. Use Cross-Validation for Robust Evaluation

```python
from sklearn.model_selection import cross_val_score

model = LinearRegression()
cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='r2')

print(f"CV R² scores: {cv_scores}")
print(f"Mean R²: {cv_scores.mean():.4f} +/- {cv_scores.std():.4f}")
```

### 3. Document Your Pipeline

```python
# Create a reproducible pipeline
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LinearRegression())
])

# Train
pipeline.fit(X_train, y_train)

# Predict (automatically scales)
predictions = pipeline.predict(X_test)
```

### 4. Save Your Model for Production

```python
import joblib

# Save model and scaler
joblib.dump(pipeline, 'house_price_model.pkl')

# Load later
loaded_pipeline = joblib.load('house_price_model.pkl')
predictions = loaded_pipeline.predict(new_data)
```

---

## Practice Exercises

### Exercise 1: Add Polynomial Features

```python
"""
Extend the model to capture non-linear relationships.
1. Add polynomial features (degree 2)
2. Compare performance with linear model
3. Check for overfitting
"""
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score

# Your code here
poly_pipeline = Pipeline([
    ('poly', PolynomialFeatures(degree=2, include_bias=False)),
    ('scaler', StandardScaler()),
    ('model', LinearRegression())
])

poly_pipeline.fit(X_train, y_train)

# Evaluate
train_r2 = r2_score(y_train, poly_pipeline.predict(X_train))
test_r2 = r2_score(y_test, poly_pipeline.predict(X_test))

print(f"Polynomial (degree 2) - Train R²: {train_r2:.4f}, Test R²: {test_r2:.4f}")
```

### Exercise 2: Regularized Regression

```python
"""
Try Ridge and Lasso regression to handle potential overfitting.
1. Train Ridge regression (alpha=1.0)
2. Train Lasso regression (alpha=1.0)
3. Compare coefficients with linear regression
"""
from sklearn.linear_model import Ridge, Lasso

# Your code here
models = {
    'Linear': LinearRegression(),
    'Ridge': Ridge(alpha=1.0),
    'Lasso': Lasso(alpha=1.0)
}

for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    train_r2 = r2_score(y_train, model.predict(X_train_scaled))
    test_r2 = r2_score(y_test, model.predict(X_test_scaled))
    print(f"{name}: Train R²={train_r2:.4f}, Test R²={test_r2:.4f}")
```

### Exercise 3: Feature Selection

```python
"""
Use correlation analysis to select the best features.
1. Calculate feature correlations with target
2. Select top 2 features
3. Train model with only those features
4. Compare performance
"""
# Your code here
corr_with_price = df.corr()['price'].drop('price').abs().sort_values(ascending=False)
print("Feature correlations:")
print(corr_with_price)

# Select top 2 features
top_features = corr_with_price.index[:2].tolist()
print(f"\nTop features: {top_features}")

# Train model with selected features
X_train_selected = X_train[top_features]
X_test_selected = X_test[top_features]

scaler_selected = StandardScaler()
X_train_selected_scaled = scaler_selected.fit_transform(X_train_selected)
X_test_selected_scaled = scaler_selected.transform(X_test_selected)

model_selected = LinearRegression()
model_selected.fit(X_train_selected_scaled, y_train)

test_r2_selected = r2_score(y_test, model_selected.predict(X_test_selected_scaled))
print(f"Model with top 2 features - Test R²: {test_r2_selected:.4f}")
```

---

## Summary

| Step | Description | Key Function |
|------|-------------|--------------|
| 1. Problem Definition | Define target and features | — |
| 2. Data Generation | Create or load data | `pd.DataFrame()` |
| 3. Data Exploration | Understand distributions | `df.describe()`, `df.corr()` |
| 4. Feature Engineering | Check correlations | `df.corr()['target']` |
| 5. Data Preparation | Split and scale | `train_test_split()`, `StandardScaler()` |
| 6. Model Training | Fit the model | `model.fit()` |
| 7. Model Evaluation | Measure performance | `r2_score()`, `mean_squared_error()` |
| 8. Interpretation | Understand coefficients | `model.coef_`, `model.intercept_` |
| 9. Predictions | Use model on new data | `model.predict()` |
| 10. Summary | Document findings | — |

### Key Takeaways

1. **Always split data first** before any preprocessing
2. **Scale features** for comparable coefficients
3. **Evaluate on test set** to check for overfitting
4. **Interpret coefficients** for business insights
5. **Use pipelines** for reproducible workflows

---

## Next Steps

- **Lecture 15**: Logistic Regression — Extend to classification problems
- **Lecture 22**: Cross-Validation — More robust evaluation techniques
- **Lecture 20**: Random Forest — Ensemble methods for better performance

---

## References

- [W3Schools - Linear Regression](https://www.w3schools.com/python/ml_linear_regression.asp)
- [Scikit-learn Documentation - LinearRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)
- [Scikit-learn Documentation - Pipeline](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html)
