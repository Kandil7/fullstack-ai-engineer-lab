"""
W3Schools Python Tutorial - ML 07: R-squared (Coefficient of Determination)
===========================================================================
Topics: R-squared score, explained variance, model evaluation metrics

Run: python 07-r-squared.py
Reference: https://www.w3schools.com/python/python_ml_r_squared.asp
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# ============================================================
# What is R-squared?
# ============================================================
# R-squared (R2) measures how well a regression model fits the data.
# It ranges from 0 to 1 (can be negative for very bad models):
#   - R2 = 1.0: Perfect fit (model explains all variance)
#   - R2 = 0.5: Model explains 50% of variance
#   - R2 = 0.0: Model explains none of the variance (same as predicting mean)

print("--- What is R-squared? ---")
print("R-squared measures how well regression predictions match actual data")
print("Range: 0 to 1 (1 = perfect fit)")
print()

# ============================================================
# Example 1: Simple R-squared Calculation
# ============================================================
print("--- Example 1: Simple R-squared ---")

# Known relationship: y = 2x + 1 + noise
np.random.seed(42)
X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(-1, 1)
y = 2 * X.flatten() + 1 + np.random.normal(0, 1, 10)

model = LinearRegression()
model.fit(X, y)
r_squared = model.score(X, y)

print(f"Coefficients: {model.coef_[0]:.4f}, Intercept: {model.intercept_:.4f}")
print(f"R-squared: {r_squared:.4f}")
print(f"R-squared (percent): {r_squared * 100:.2f}%")
print(f"Model explains {r_squared * 100:.1f}% of the variance in y")
print()

# ============================================================
# Example 2: R-squared vs Predicting Mean
# ============================================================
print("--- Example 2: R-squared vs Mean Prediction ---")

y_mean = np.full_like(y, np.mean(y))

# Total Sum of Squares (TSS) - variance from mean
tss = np.sum((y - y_mean) ** 2)

# Residual Sum of Squares (RSS) - variance from model
y_pred = model.predict(X)
rss = np.sum((y - y_pred) ** 2)

# R-squared = 1 - (RSS / TSS)
r_squared_manual = 1 - (rss / tss)

print(f"Mean of y: {np.mean(y):.4f}")
print(f"Total Sum of Squares (TSS): {tss:.4f}")
print(f"Residual Sum of Squares (RSS): {rss:.4f}")
print(f"Manual R-squared: {r_squared_manual:.4f}")
print(f"sklearn R-squared: {r_squared:.4f}")
print(f"Match: {np.isclose(r_squared_manual, r_squared)}")
print()

# ============================================================
# Example 3: Comparing Good vs Bad Models
# ============================================================
print("--- Example 3: Good vs Bad Model ---")

# Strong linear relationship
np.random.seed(42)
X_strong = np.linspace(0, 10, 50).reshape(-1, 1)
y_strong = 3 * X_strong.flatten() + 2 + np.random.normal(0, 0.5, 50)

# Weak/noisy relationship
y_noisy = 0.5 * X_strong.flatten() + np.random.normal(0, 5, 50)

model_strong = LinearRegression()
model_strong.fit(X_strong, y_strong)
r2_strong = model_strong.score(X_strong, y_strong)

model_noisy = LinearRegression()
model_noisy.fit(X_strong, y_noisy)
r2_noisy = model_noisy.score(X_strong, y_noisy)

print(f"Strong relationship R2: {r2_strong:.4f}")
print(f"Noisy relationship R2:  {r2_noisy:.4f}")
print()

# ============================================================
# Example 4: R-squared with Train/Test Split
# ============================================================
print("--- Example 4: R-squared with Train/Test Split ---")

np.random.seed(42)
X = np.random.rand(100, 1) * 10
y = 2.5 * X.flatten() + 5 + np.random.normal(0, 2, 100)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

train_r2 = model.score(X_train, y_train)
test_r2 = model.score(X_test, y_test)

print(f"Training R2:  {train_r2:.4f}")
print(f"Testing R2:   {test_r2:.4f}")
print(f"Gap:          {train_r2 - test_r2:.4f}")
print()

# ============================================================
# Example 5: Adjusted R-squared
# ============================================================
print("--- Example 5: Adjusted R-squared ---")

# Adjusted R2 penalizes for adding useless features
# Formula: 1 - (1 - R2) * (n - 1) / (n - p - 1)
# Where n = samples, p = features

n = len(X_train)
p = 1  # number of features

adjusted_r2 = 1 - (1 - train_r2) * (n - 1) / (n - p - 1)

print(f"R-squared:       {train_r2:.4f}")
print(f"Adjusted R-squared: {adjusted_r2:.4f}")
print()

# With multiple irrelevant features
np.random.seed(42)
X_multi = np.random.rand(100, 10)  # 10 features, only first is meaningful
X_multi[:, 0] = np.linspace(0, 10, 100)
y_multi = 2 * X_multi[:, 0] + np.random.normal(0, 1, 100)

model_multi = LinearRegression()
model_multi.fit(X_multi, y_multi)

r2_multi = model_multi.score(X_multi, y_multi)
p_multi = X_multi.shape[1]
adj_r2_multi = 1 - (1 - r2_multi) * (n - 1) / (n - p_multi - 1)

print(f"With 10 features (only 1 meaningful):")
print(f"R-squared:       {r2_multi:.4f}")
print(f"Adjusted R-squared: {adj_r2_multi:.4f}")
print()

# ============================================================
# Example 6: Predictions and Residuals
# ============================================================
print("--- Example 6: Predictions and Residuals ---")

np.random.seed(42)
X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(-1, 1)
y = np.array([2.1, 4.0, 5.8, 8.2, 9.9, 12.1, 14.0, 15.8, 18.2, 20.1])

model = LinearRegression()
model.fit(X, y)

y_pred = model.predict(X)
residuals = y - y_pred

print(f"{'X':>4} {'Actual':>8} {'Predicted':>10} {'Residual':>10}")
print("-" * 36)
for i in range(len(X)):
    print(f"{X[i][0]:>4.0f} {y[i]:>8.2f} {y_pred[i]:>10.2f} {residuals[i]:>10.4f}")

print(f"\nR-squared: {model.score(X, y):.4f}")
print(f"Mean squared error: {np.mean(residuals**2):.4f}")
print(f"Root mean squared error: {np.sqrt(np.mean(residuals**2)):.4f}")
print()

# ============================================================
# Example 7: Multiple R-squared (Multiple Regression)
# ============================================================
print("--- Example 7: Multiple R-squared ---")

np.random.seed(42)
n_samples = 100
X1 = np.random.uniform(1, 10, n_samples)
X2 = np.random.uniform(0, 5, n_samples)
X = np.column_stack([X1, X2])
y = 2 * X1 + 3 * X2 + np.random.normal(0, 2, n_samples)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

print(f"Coefficients: X1={model.coef_[0]:.4f}, X2={model.coef_[1]:.4f}")
print(f"Intercept: {model.intercept_:.4f}")
print(f"Training R2: {model.score(X_train, y_train):.4f}")
print(f"Testing R2:  {model.score(X_test, y_test):.4f}")
print()

# ============================================================
# Example 8: R-squared Guidelines
# ============================================================
print("--- Example 8: R-squared Guidelines ---")

print("R-squared interpretations:")
print("  0.75 - 1.00 : Strong fit")
print("  0.50 - 0.75 : Moderate fit")
print("  0.25 - 0.50 : Weak fit")
print("  0.00 - 0.25 : Very weak/no fit")
print()
print("IMPORTANT: High R2 does NOT mean the model is good!")
print("- R2 can be high even if model is wrong (spurious correlations)")
print("- Always check residuals for patterns")
print("- Use adjusted R2 when comparing models with different features")
print("- Consider domain knowledge, not just R2")
print()

# ============================================================
# Summary
# ============================================================
print("--- Summary ---")
print("1. R-squared measures how well model explains variance in data")
print("2. Range: 0 (bad) to 1 (perfect), can be negative")
print("3. Formula: 1 - (Residual SS / Total SS)")
print("4. Adjusted R2 penalizes for adding useless features")
print("5. High R2 doesn't guarantee a good model")
print("6. Always check residuals and use domain knowledge")
print("7. train_test_split helps detect overfitting")
