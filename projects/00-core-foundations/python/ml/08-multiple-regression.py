"""
W3Schools Python Tutorial - ML NN: Multiple Regression
=======================================================
Topics: Multiple Features, Coefficient Interpretation, R-squared Score

Run: python 08-multiple-regression.py
Reference: https://www.w3schools.com/python/ml_multiple_regression.asp
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# ============================================================
# What is Multiple Regression?
# ============================================================

# Example 1: Multiple features
print("Example 1: Multiple Features")
# House price prediction with multiple features
np.random.seed(42)
n_samples = 200

# Generate features
square_feet = np.random.randint(800, 3500, n_samples)
bedrooms = np.random.randint(1, 6, n_samples)
age = np.random.randint(0, 50, n_samples)

# Generate target with known relationship
# Price = 150 * sqft + 20000 * bedrooms - 1000 * age + noise
price = (150 * square_feet + 
         20000 * bedrooms - 
         1000 * age + 
         np.random.randn(n_samples) * 20000)

print(f"Features: square_feet, bedrooms, age")
print(f"Target: price")
print(f"Number of samples: {n_samples}")

# ============================================================
# Preparing the Data
# ============================================================

# Example 2: Create feature matrix
print("\nExample 2: Feature Matrix")
X = np.column_stack([square_feet, bedrooms, age])
y = price

print("Feature matrix shape:", X.shape)
print("Target vector shape:", y.shape)

# Example 3: First few samples
print("\nExample 3: Sample Data")
print("First 5 samples:")
print("Square Feet | Bedrooms | Age | Price")
for i in range(5):
    print(f"{X[i, 0]:>11} | {X[i, 1]:>8} | {X[i, 2]:>3} | ${y[i]:,.0f}")

# ============================================================
# Fitting the Model
# ============================================================

# Example 4: Train/test split
print("\nExample 4: Train/Test Split")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training set: {len(X_train)} samples")
print(f"Test set: {len(X_test)} samples")

# Example 5: Fit multiple regression model
print("\nExample 5: Fitting the Model")
model = LinearRegression()
model.fit(X_train, y_train)

print("Model coefficients:")
print(f"  Square feet: {model.coef_[0]:.2f}")
print(f"  Bedrooms: {model.coef_[1]:.2f}")
print(f"  Age: {model.coef_[2]:.2f}")
print(f"  Intercept: {model.intercept_:.2f}")

# ============================================================
# Interpreting Coefficients
# ============================================================

# Example 6: Coefficient interpretation
print("\nExample 6: Coefficient Interpretation")
print("Each coefficient represents the change in target for one unit change in feature:")
print(f"  - Each additional square foot adds ${model.coef_[0]:.0f} to price")
print(f"  - Each additional bedroom adds ${model.coef_[1]:.0f} to price")
print(f"  - Each year of age reduces price by ${abs(model.coef_[2]):.0f}")

# Example 7: Equation
print("\nExample 7: Regression Equation")
print(f"Price = {model.intercept_:.0f}")
print(f"       + {model.coef_[0]:.0f} x SquareFeet")
print(f"       + {model.coef_[1]:.0f} x Bedrooms")
print(f"       + {model.coef_[2]:.0f} x Age")

# ============================================================
# Evaluating the Model
# ============================================================

# Example 8: Predictions and evaluation
print("\nExample 8: Model Evaluation")
y_pred = model.predict(X_test)

# Calculate metrics
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:,.0f}")
print(f"Root Mean Squared Error: {rmse:,.0f}")
print(f"R-squared Score: {r2:.4f}")

# Example 9: Understanding R-squared
print("\nExample 9: R-squared Interpretation")
print(f"R^2 = {r2:.4f} means:")
print(f"  {r2*100:.1f}% of the variance in price is explained by the features")
print("  R^2 ranges from 0 to 1 (higher is better)")
print("  1.0 = perfect prediction, 0.0 = no better than mean")

# ============================================================
# Making Predictions
# ============================================================

# Example 10: Predict new houses
print("\nExample 10: Predicting New Houses")
new_houses = np.array([
    [1500, 3, 10],   # 1500 sqft, 3 bedrooms, 10 years old
    [2500, 4, 5],    # 2500 sqft, 4 bedrooms, 5 years old
    [1200, 2, 20]    # 1200 sqft, 2 bedrooms, 20 years old
])

predictions = model.predict(new_houses)

for i, (house, pred) in enumerate(zip(new_houses, predictions)):
    print(f"House {i+1}: {house[0]} sqft, {house[1]} bedrooms, {house[2]} years")
    print(f"  Predicted price: ${pred:,.0f}")

# ============================================================
# Feature Importance
# ============================================================

# Example 11: Feature importance
print("\nExample 11: Feature Importance")
# Calculate absolute coefficients (normalized)
abs_coef = np.abs(model.coef_)
importance = abs_coef / abs_coef.sum()

feature_names = ['Square Feet', 'Bedrooms', 'Age']
for name, imp in sorted(zip(feature_names, importance), 
                       key=lambda x: x[1], reverse=True):
    print(f"  {name}: {imp:.3f} ({imp*100:.1f}%)")

# ============================================================
# Multiple Regression with Pandas
# ============================================================

# Example 12: Using DataFrame
print("\nExample 12: Using Pandas DataFrame")
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

print("Model trained successfully")
print(f"R^2 score: {model.score(X_test, y_test):.4f}")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("Summary:")
print("- Multiple regression uses multiple features to predict target")
print("- Coefficients show feature importance and direction")
print("- R-squared measures how well features explain variance")
print("- Always evaluate on test set, not training set")
print("- Feature importance helps understand the model")
print("="*60)