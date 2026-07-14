"""
W3Schools Python Tutorial - ML NN: Polynomial Regression
=========================================================
Topics: Polynomial Features, Curved Relationships, Degree Selection

Run: python 06-polynomial-regression.py
Reference: https://www.w3schools.com/python/ml_polynomial_regression.asp
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# ============================================================
# Why Polynomial Regression?
# ============================================================

# Example 1: Non-linear relationship
print("Example 1: Non-linear Relationship")
# Simulated data: growth that slows down
np.random.seed(42)
X = np.linspace(0, 10, 100).reshape(-1, 1)
y = 0.5 * X.squeeze()**2 - 3 * X.squeeze() + 10 + np.random.randn(100) * 2

print("This data follows a quadratic pattern (parabola)")
print("Simple linear regression won't fit well")

# ============================================================
# Polynomial Features
# ============================================================

# Example 2: Creating polynomial features
print("\nExample 2: Polynomial Features")
# Original feature: x
# Polynomial features: x, x^2, x³, ...

poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

print(f"Original shape: {X.shape}")
print(f"Polynomial shape: {X_poly.shape}")
print(f"Feature names: {poly.get_feature_names_out()}")

# Example 3: What the features look like
print("\nExample 3: Feature Transformation")
print("Original X (first 3 rows):")
print(X[:3])
print("\nPolynomial X (first 3 rows):")
print(X_poly[:3])

# ============================================================
# Fitting Polynomial Regression
# ============================================================

# Example 4: Degree 2 (quadratic)
print("\nExample 4: Quadratic Regression (degree=2)")
poly2 = PolynomialFeatures(degree=2, include_bias=False)
X_poly2 = poly2.fit_transform(X)

model2 = LinearRegression()
model2.fit(X_poly2, y)

print(f"Coefficients: {model2.coef_}")
print(f"Intercept: {model2.intercept_}")

# Example 5: Degree 3 (cubic)
print("\nExample 5: Cubic Regression (degree=3)")
poly3 = PolynomialFeatures(degree=3, include_bias=False)
X_poly3 = poly3.fit_transform(X)

model3 = LinearRegression()
model3.fit(X_poly3, y)

print(f"Coefficients: {model3.coef_}")
print(f"Intercept: {model3.intercept_}")

# ============================================================
# Comparing Degrees
# ============================================================

# Example 6: Model comparison
print("\nExample 6: Comparing Different Degrees")
degrees = [1, 2, 3, 4, 5]
results = []

for degree in degrees:
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    X_poly = poly.fit_transform(X)
    
    model = LinearRegression()
    model.fit(X_poly, y)
    
    y_pred = model.predict(X_poly)
    r2 = r2_score(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    
    results.append({
        'degree': degree,
        'r2': r2,
        'rmse': rmse,
        'n_features': X_poly.shape[1]
    })
    print(f"Degree {degree}: R^2={r2:.4f}, RMSE={rmse:.4f}, Features={X_poly.shape[1]}")

# ============================================================
# Overfitting vs Underfitting
# ============================================================

# Example 7: Overfitting demonstration
print("\nExample 7: Overfitting with High Degree")
# Use degree 15 (will overfit)
poly15 = PolynomialFeatures(degree=15, include_bias=False)
X_poly15 = poly15.fit_transform(X)

model15 = LinearRegression()
model15.fit(X_poly15, y)

y_pred15 = model15.predict(X_poly15)
r2_15 = r2_score(y, y_pred15)

print(f"Degree 15: R^2={r2_15:.4f} (looks good but overfits!)")
print("Overfitting: Model memorizes noise instead of learning pattern")

# ============================================================
# Train/Test Split for Selection
# ============================================================

# Example 8: Proper degree selection
print("\nExample 8: Proper Degree Selection")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

best_degree = 1
best_r2 = -np.inf
results_test = []

for degree in range(1, 8):
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)
    
    model = LinearRegression()
    model.fit(X_train_poly, y_train)
    
    y_pred_test = model.predict(X_test_poly)
    r2_test = r2_score(y_test, y_pred_test)
    
    results_test.append({'degree': degree, 'r2_test': r2_test})
    
    if r2_test > best_r2:
        best_r2 = r2_test
        best_degree = degree
    
    print(f"Degree {degree}: Test R^2={r2_test:.4f}")

print(f"\nBest degree: {best_degree} (Test R^2={best_r2:.4f})")

# ============================================================
# Prediction with Polynomial Model
# ============================================================

# Example 9: Making predictions
print("\nExample 9: Predictions with Polynomial Model")
# Use the best degree model
poly_best = PolynomialFeatures(degree=best_degree, include_bias=False)
X_poly_best = poly_best.fit_transform(X)

model_best = LinearRegression()
model_best.fit(X_poly_best, y)

# Predict new values
X_new = np.array([[2], [5], [8]])
X_new_poly = poly_best.transform(X_new)
predictions = model_best.predict(X_new_poly)

for x_val, pred in zip(X_new.flatten(), predictions):
    print(f"X={x_val} -> Predicted y={pred:.2f}")

# ============================================================
# When to Use Polynomial Regression
# ============================================================

# Example 10: Use cases
print("\nExample 10: When to Use Polynomial Regression")
print("Use polynomial regression when:")
print("1. Relationship between X and y is non-linear")
print("2. You can see curvature in scatter plots")
print("3. Linear regression gives poor R^2 score")
print("Be careful of:")
print("1. Overfitting with high degrees")
print("2. Extrapolation beyond training data range")
print("3. Multicollinearity with high-degree terms")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("Summary:")
print("- Polynomial regression fits curved relationships")
print("- Use PolynomialFeatures to create x^2, x³, etc.")
print("- Choose degree based on test performance")
print("- Higher degrees risk overfitting")
print("- Always evaluate on test set")
print("="*60)