"""
W3Schools Python Tutorial - ML NN: Linear Regression
=====================================================
Topics: Simple Linear Regression, Best Fit Line, sklearn LinearRegression

Run: python 05-linear-regression.py
Reference: https://www.w3schools.com/python/ml_linear_regression.asp
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# ============================================================
# What is Linear Regression?
# ============================================================

# Example 1: Simple relationship
print("Example 1: Linear Relationship")
# Simulated data: house size vs price
np.random.seed(42)
X = np.array([[1000], [1500], [2000], [2500], [3000]])
y = np.array([200000, 300000, 400000, 500000, 600000])

print("House sizes (sq ft):", X.flatten())
print("Prices ($):", y)

# ============================================================
# Finding the Best Fit Line
# ============================================================

# Example 2: Manual calculation
print("\nExample 2: Manual Calculation")
# Simple linear regression: y = mx + b
# Calculate slope (m) and intercept (b)
x_mean = np.mean(X)
y_mean = np.mean(y)

numerator = np.sum((X.flatten() - x_mean) * (y - y_mean))
denominator = np.sum((X.flatten() - x_mean) ** 2)
m = numerator / denominator
b = y_mean - m * x_mean

print(f"Calculated slope (m): {m}")
print(f"Calculated intercept (b): {b}")
print(f"Equation: y = {m:.2f}x + {b:.2f}")

# ============================================================
# Using sklearn LinearRegression
# ============================================================

# Example 3: Fitting a model
print("\nExample 3: Using sklearn LinearRegression")
model = LinearRegression()
model.fit(X, y)

print(f"sklearn slope: {model.coef_[0]:.2f}")
print(f"sklearn intercept: {model.intercept_:.2f}")

# Example 4: Making predictions
print("\nExample 4: Making Predictions")
new_sizes = np.array([[1800], [2200], [2800]])
predictions = model.predict(new_sizes)

for size, price in zip(new_sizes.flatten(), predictions):
    print(f"Size: {size} sq ft -> Predicted price: ${price:,.0f}")

# ============================================================
# Evaluating the Model
# ============================================================

# Example 5: Model evaluation
print("\nExample 5: Model Evaluation")
# Predict on training data
y_pred = model.predict(X)

# Calculate metrics
mse = mean_squared_error(y, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y, y_pred)

print(f"Mean Squared Error: {mse:,.0f}")
print(f"Root Mean Squared Error: {rmse:,.0f}")
print(f"R-squared Score: {r2:.4f}")

# ============================================================
# Multiple Linear Regression
# ============================================================

# Example 6: Multiple features
print("\nExample 6: Multiple Linear Regression")
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

print("Coefficients:", model_multi.coef_)
print("Intercept:", model_multi.intercept_)

# ============================================================
# Train/Test Split
# ============================================================

# Example 7: Proper evaluation with split
print("\nExample 7: Train/Test Split Evaluation")
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
print(f"R-squared on test set: {r2:.4f}")
print(f"RMSE on test set: {rmse:.4f}")

# ============================================================
# Visualization Concept
# ============================================================

# Example 8: Data for visualization
print("\nExample 8: Data for Visualization")
print("To visualize the regression line:")
print("1. Plot the original data points")
print("2. Plot the regression line using model.predict()")
print("3. Add labels and title")

# ============================================================
# Assumptions of Linear Regression
# ============================================================

# Example 9: Checking assumptions
print("\nExample 9: Linear Regression Assumptions")
print("1. Linearity: Relationship between X and y is linear")
print("2. Independence: Observations are independent")
print("3. Homoscedasticity: Constant variance of errors")
print("4. Normality: Errors are normally distributed")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("Summary:")
print("- Linear regression finds the best fit line: y = mx + b")
print("- Use sklearn LinearRegression for easy implementation")
print("- Evaluate with R-squared, MSE, and RMSE")
print("- Always split data for proper evaluation")
print("- Multiple regression handles multiple features")
print("="*60)