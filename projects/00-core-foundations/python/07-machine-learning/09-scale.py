"""
W3Schools Python Tutorial - ML NN: Feature Scaling
====================================================
Topics: StandardScaler, MinMaxScaler, When to Scale

Run: python 09-scale.py
Reference: https://www.w3schools.com/python/ml_data_scaling.asp
"""

import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# ============================================================
# Why Scale Features?
# ============================================================

# Example 1: Different scales problem
print("Example 1: Different Feature Scales")
# House data with different scales
np.random.seed(42)
square_feet = np.random.randint(800, 3500, 100)
bedrooms = np.random.randint(1, 6, 100)
price = 150 * square_feet + 20000 * bedrooms + np.random.randn(100) * 20000

print(f"Square feet range: {square_feet.min()} - {square_feet.max()}")
print(f"Bedrooms range: {bedrooms.min()} - {bedrooms.max()}")
print(f"Price range: ${price.min():,.0f} - ${price.max():,.0f}")
print("\nDifferent scales can bias models toward larger-scale features")

# ============================================================
# StandardScaler (Z-score Normalization)
# ============================================================

# Example 2: StandardScaler
print("\nExample 2: StandardScaler")
X = np.column_stack([square_feet, bedrooms])

scaler = StandardScaler()
X_standardized = scaler.fit_transform(X)

print("Original data (first 5 rows):")
print(X[:5])
print("\nStandardized data (first 5 rows):")
print(X_standardized[:5])
print(f"\nStandardized mean: {X_standardized.mean(axis=0)}")
print(f"Standardized std: {X_standardized.std(axis=0)}")

# ============================================================
# MinMaxScaler (0-1 Normalization)
# ============================================================

# Example 3: MinMaxScaler
print("\nExample 3: MinMaxScaler")
scaler = MinMaxScaler()
X_normalized = scaler.fit_transform(X)

print("Normalized data (first 5 rows):")
print(X_normalized[:5])
print(f"\nNormalized min: {X_normalized.min(axis=0)}")
print(f"Normalized max: {X_normalized.max(axis=0)}")

# ============================================================
# RobustScaler (Outlier-Resistant)
# ============================================================

# Example 4: RobustScaler
print("\nExample 4: RobustScaler")
# Data with outliers
np.random.seed(42)
data_with_outliers = np.random.randn(100, 2) * 10 + 50
data_with_outliers[0] = [200, 200]  # Outlier
data_with_outliers[1] = [-100, -100]  # Outlier

scaler = RobustScaler()
data_robust = scaler.fit_transform(data_with_outliers)

print("Original data stats:")
print(f"  Mean: {data_with_outliers.mean(axis=0)}")
print(f"  Std: {data_with_outliers.std(axis=0)}")
print("\nRobust-scaled data stats:")
print(f"  Mean: {data_robust.mean(axis=0):.2f}")
print(f"  Std: {data_robust.std(axis=0):.2f}")

# ============================================================
# When to Use Each Scaler
# ============================================================

# Example 5: Scaler selection guide
print("\nExample 5: When to Use Each Scaler")
print("StandardScaler: When data is approximately normal")
print("MinMaxScaler: When you need bounded values (0-1)")
print("RobustScaler: When data has outliers")
print("No scaling: For tree-based models (they don't need it)")

# ============================================================
# Impact on Model Performance
# ============================================================

# Example 6: Model with unscaled data
print("\nExample 6: Model Comparison")
np.random.seed(42)
X = np.random.rand(200, 2) * np.array([1000, 10])  # Different scales
y = 5 * X[:, 0] + 10 * X[:, 1] + np.random.randn(200) * 50

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Without scaling
model_unscaled = LinearRegression()
model_unscaled.fit(X_train, y_train)
r2_unscaled = r2_score(y_test, model_unscaled.predict(X_test))

# With StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model_scaled = LinearRegression()
model_scaled.fit(X_train_scaled, y_train)
r2_scaled = r2_score(y_test, model_scaled.predict(X_test_scaled))

print(f"R^2 without scaling: {r2_unscaled:.4f}")
print(f"R^2 with scaling: {r2_scaled:.4f}")

# ============================================================
# Feature Importance After Scaling
# ============================================================

# Example 7: Coefficients comparison
print("\nExample 7: Coefficients Comparison")
print("Unscaled model coefficients:")
print(f"  Feature 1: {model_unscaled.coef_[0]:.4f}")
print(f"  Feature 2: {model_unscaled.coef_[1]:.4f}")

print("\nScaled model coefficients:")
print(f"  Feature 1: {model_scaled.coef_[0]:.4f}")
print(f"  Feature 2: {model_scaled.coef_[1]:.4f}")

# ============================================================
# Scaling Pipeline
# ============================================================

# Example 8: Complete scaling pipeline
print("\nExample 8: Scaling Pipeline")
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

# Create pipeline
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LinearRegression())
])

# Train
pipe.fit(X_train, y_train)

# Predict
y_pred = pipe.predict(X_test)
r2 = r2_score(y_test, y_pred)

print(f"Pipeline R^2 score: {r2:.4f}")
print("Pipeline handles scaling automatically")

# ============================================================
# Scaling New Data
# ============================================================

# Example 9: Transforming new data
print("\nExample 9: Transforming New Data")
# Fit scaler on training data
scaler = StandardScaler()
scaler.fit(X_train)

# Transform new data
new_data = np.array([[500, 3], [2000, 4], [1000, 2]])
new_data_scaled = scaler.transform(new_data)

print("New data (original):")
print(new_data)
print("\nNew data (scaled):")
print(new_data_scaled)

# ============================================================
# Common Mistakes
# ============================================================

# Example 10: Scaling mistakes
print("\nExample 10: Common Scaling Mistakes")
print("1. Scaling test data with test statistics (use train statistics)")
print("2. Scaling target variable (usually not needed)")
print("3. Scaling before train/test split (causes data leakage)")
print("4. Forgetting to scale new data in production")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("Summary:")
print("- Feature scaling puts features on the same scale")
print("- StandardScaler: mean=0, std=1 (good for normal data)")
print("- MinMaxScaler: 0-1 range (good for bounded values)")
print("- RobustScaler: resistant to outliers")
print("- Always fit scaler on training data only")
print("- Use Pipeline for clean scaling workflow")
print("="*60)