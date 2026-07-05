"""
W3Schools Python Tutorial - ML NN: Cleaning Data
=================================================
Topics: Missing Values, Duplicates, Normalization, Feature Scaling

Run: python 04-clean-data.py
Reference: https://www.w3schools.com/python/ml_data_cleaning.asp
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# ============================================================
# Why Clean Data?
# ============================================================

# Example 1: Dirty data example
print("Example 1: Why Clean Data?")
print("Machine learning models require clean, numerical data")
print("Common issues: missing values, duplicates, outliers, scaling")

# ============================================================
# Handling Missing Values
# ============================================================

# Example 2: Creating data with missing values
print("\nExample 2: Data with Missing Values")
data = {
    'age': [25, 30, np.nan, 45, 50],
    'salary': [50000, 60000, 75000, np.nan, 90000],
    'experience': [2, 5, 8, 12, np.nan]
}
df = pd.DataFrame(data)
print(df)

# Example 3: Finding missing values
print("\nExample 3: Finding Missing Values")
print(f"Missing values per column:\n{df.isnull().sum()}")
print(f"Total missing values: {df.isnull().sum().sum()}")

# Example 4: Removing missing values
print("\nExample 4: Removing Missing Values")
df_dropped = df.dropna()
print("After dropping rows with missing values:")
print(df_dropped)

# Example 5: Filling missing values
print("\nExample 5: Filling Missing Values")
# Fill with mean
df_mean = df.fillna(df.mean())
print("Filled with column means:")
print(df_mean)

# Fill with specific value
df_zero = df.fillna(0)
print("\nFilled with zeros:")
print(df_zero)

# ============================================================
# Removing Duplicates
# ============================================================

# Example 6: Duplicate data
print("\nExample 6: Duplicate Data")
data = {
    'name': ['Alice', 'Bob', 'Alice', 'Charlie', 'Bob'],
    'age': [25, 30, 25, 35, 30],
    'salary': [50000, 60000, 50000, 70000, 60000]
}
df = pd.DataFrame(data)
print("Original data:")
print(df)

# Example 7: Finding duplicates
print("\nExample 7: Finding Duplicates")
duplicates = df.duplicated()
print(f"Duplicate rows:\n{duplicates}")
print(f"Number of duplicates: {duplicates.sum()}")

# Example 8: Removing duplicates
print("\nExample 8: Removing Duplicates")
df_unique = df.drop_duplicates()
print("After removing duplicates:")
print(df_unique)

# ============================================================
# Data Normalization
# ============================================================

# Example 9: Why normalize?
print("\nExample 9: Why Normalize?")
print("Different features may have different scales")
print("Example: age (0-100) vs salary (0-1000000)")
print("Normalization puts features on the same scale")

# Example 10: Min-Max Normalization
print("\nExample 10: Min-Max Normalization (0-1 range)")
data = np.array([[25, 50000], [30, 60000], [35, 75000], [40, 90000]])
print("Original data:")
print(data)

scaler = MinMaxScaler()
normalized = scaler.fit_transform(data)
print("\nNormalized data:")
print(normalized)

# ============================================================
# Feature Scaling
# ============================================================

# Example 11: Standardization (Z-score)
print("\nExample 11: Standardization (Z-score)")
scaler = StandardScaler()
standardized = scaler.fit_transform(data)
print("Standardized data (mean=0, std=1):")
print(standardized)
print(f"Mean: {standardized.mean(axis=0)}")
print(f"Std: {standardized.std(axis=0)}")

# Example 12: When to use each method
print("\nExample 12: When to Use Each Method")
print("Min-Max: When you need bounded values (0-1)")
print("Standardization: When data is approximately normally distributed")
print("Robust Scaling: When data has outliers (uses median and IQR)")

# ============================================================
# Handling Outliers
# ============================================================

# Example 13: Detecting outliers
print("\nExample 13: Detecting Outliers")
np.random.seed(42)
data = np.random.randn(100)
data = np.append(data, [10, -10])  # Add outliers

# Using IQR method
Q1 = np.percentile(data, 25)
Q3 = np.percentile(data, 75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = data[(data < lower_bound) | (data > upper_bound)]
print(f"Number of outliers detected: {len(outliers)}")
print(f"Outlier values: {outliers}")

# ============================================================
# Data Transformation
# ============================================================

# Example 14: Log transformation
print("\nExample 14: Log Transformation")
data = np.array([1, 10, 100, 1000, 10000])
log_data = np.log10(data)
print("Original (skewed):", data)
print("Log-transformed:", log_data)

# ============================================================
# Pipeline Example
# ============================================================

# Example 15: Complete cleaning pipeline
print("\nExample 15: Complete Cleaning Pipeline")
# Create dirty data
np.random.seed(42)
df_dirty = pd.DataFrame({
    'age': [25, 30, np.nan, 45, 50, 25, 30],
    'salary': [50000, 60000, 75000, np.nan, 90000, 50000, 60000],
    'experience': [2, 5, 8, 12, np.nan, 2, 5]
})

print("Original dirty data:")
print(df_dirty)

# Step 1: Remove duplicates
df_clean = df_dirty.drop_duplicates()
print("\nAfter removing duplicates:")
print(df_clean)

# Step 2: Fill missing values
df_clean = df_clean.fillna(df_clean.mean())
print("\nAfter filling missing values:")
print(df_clean)

# Step 3: Scale features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(df_clean)
print("\nAfter standardization:")
print(features_scaled)

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("Summary:")
print("- Always handle missing values before modeling")
print("- Remove duplicate rows to avoid bias")
print("- Normalize or standardize features for better performance")
print("- Use appropriate scaling method based on data distribution")
print("- Consider outlier detection and treatment")
print("="*60)