"""
W3Schools Python Tutorial - ML NN: Linear Regression Example
=============================================================
Topics: Complete Linear Regression Project End-to-End

Run: python 14-linear-regression-example.py
Reference: https://www.w3schools.com/python/ml_linear_regression.asp
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# ============================================================
# Step 1: Problem Definition
# ============================================================

print("="*60)
print("LINEAR REGRESSION PROJECT: House Price Prediction")
print("="*60)

print("\nStep 1: Problem Definition")
print("- Predict house prices based on features")
print("- Features: square_feet, bedrooms, age, distance_to_center")
print("- Target: price")

# ============================================================
# Step 2: Data Generation
# ============================================================

print("\nStep 2: Data Generation")
np.random.seed(42)
n_samples = 500

# Generate features
square_feet = np.random.randint(800, 4000, n_samples)
bedrooms = np.random.randint(1, 6, n_samples)
age = np.random.randint(0, 50, n_samples)
distance_to_center = np.random.uniform(0.5, 20, n_samples)

# Generate target with realistic relationship
# Price = base + sqft*factor + bedrooms*factor - age*factor - distance*factor + noise
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

# ============================================================
# Step 3: Data Exploration
# ============================================================

print("\nStep 3: Data Exploration")
print("\nFirst 5 rows:")
print(df.head())

print("\nBasic statistics:")
print(df.describe())

print("\nData types:")
print(df.dtypes)

# ============================================================
# Step 4: Feature Engineering
# ============================================================

print("\nStep 4: Feature Engineering")

# Check correlations
print("\nFeature correlations with price:")
corr_with_price = df.corr()['price'].drop('price').sort_values(ascending=False)
print(corr_with_price)

# ============================================================
# Step 5: Data Preparation
# ============================================================

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

# ============================================================
# Step 6: Model Training
# ============================================================

print("\nStep 6: Model Training")

# Train linear regression model
model = LinearRegression()
model.fit(X_train_scaled, y_train)

print("Model trained successfully")
print(f"\nCoefficients:")
for feature, coef in zip(X.columns, model.coef_):
    print(f"  {feature}: {coef:.2f}")
print(f"\nIntercept: {model.intercept_:.2f}")

# ============================================================
# Step 7: Model Evaluation
# ============================================================

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
print(f"  R^2 Score: {train_r2:.4f}")
print(f"  RMSE: ${train_rmse:,.0f}")
print(f"  MAE: ${train_mae:,.0f}")

print("\nTest Set Metrics:")
print(f"  R^2 Score: {test_r2:.4f}")
print(f"  RMSE: ${test_rmse:,.0f}")
print(f"  MAE: ${test_mae:,.0f}")

# ============================================================
# Step 8: Model Interpretation
# ============================================================

print("\nStep 8: Model Interpretation")

print("\nFeature Importance (absolute coefficients):")
importance = np.abs(model.coef_)
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': importance
}).sort_values('importance', ascending=False)

for _, row in feature_importance.iterrows():
    print(f"  {row['feature']}: {row['importance']:.2f}")

print("\nInterpretation:")
print(f"  - Each additional square foot adds ~${model.coef_[0]:.0f} to price")
print(f"  - Each additional bedroom adds ~${model.coef_[1]:.0f} to price")
print(f"  - Each year of age reduces price by ~${abs(model.coef_[2]):.0f}")
print(f"  - Each km from center reduces price by ~${abs(model.coef_[3]):.0f}")

# ============================================================
# Step 9: Making Predictions
# ============================================================

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

# Scale features
new_houses_scaled = scaler.transform(new_houses)

# Make predictions
predictions = model.predict(new_houses_scaled)

print("\nPredictions:")
for i, (_, house) in enumerate(new_houses.iterrows()):
    print(f"  House {i+1}: {house['square_feet']} sqft, {house['bedrooms']} bedrooms")
    print(f"    Predicted price: ${predictions[i]:,.0f}")

# ============================================================
# Step 10: Model Summary
# ============================================================

print("\n" + "="*60)
print("PROJECT SUMMARY")
print("="*60)

print("\nModel Performance:")
print(f"  - R^2 Score: {test_r2:.4f} (explains {test_r2*100:.1f}% of price variance)")
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