"""
W3Schools Python Tutorial - ML NN: Working with Datasets
=========================================================
Topics: Dataset Structure, Features/Targets, Train/Test Split, Pandas DataFrames

Run: python 03-data-set.py
Reference: https://www.w3schools.com/python/ml_data_set.asp
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# ============================================================
# Dataset Structure
# ============================================================

# Example 1: Basic dataset components
print("Example 1: Dataset Components")
# Features (X) and targets (y)
X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])  # Features
y = np.array([0, 1, 0, 1])  # Targets

print(f"Features shape: {X.shape}")
print(f"Targets shape: {y.shape}")
print(f"First sample features: {X[0]}")
print(f"First sample target: {y[0]}")

# ============================================================
# Features vs Targets
# ============================================================

# Example 2: Understanding features and targets
print("\nExample 2: Features vs Targets")
# Simulated house data
# Features: square_feet, bedrooms, age
# Target: price
house_features = np.array([
    [1500, 3, 10],
    [2000, 4, 5],
    [1200, 2, 15],
    [1800, 3, 8]
])

house_prices = np.array([300000, 450000, 250000, 400000])

print("Features (X):")
print(house_features)
print("\nTargets (y):")
print(house_prices)

# Example 3: Feature names
print("\nExample 3: Feature Names")
feature_names = ["square_feet", "bedrooms", "age"]
for i, name in enumerate(feature_names):
    print(f"Feature {i}: {name}")

# ============================================================
# Training and Test Data
# ============================================================

# Example 4: Why split data?
print("\nExample 4: Why Split Data?")
print("Training set: Used to train the model (usually 70-80%)")
print("Test set: Used to evaluate model performance (usually 20-30%)")
print("This prevents overfitting and gives honest performance estimate")

# Example 5: Simple split
print("\nExample 5: Manual Train/Test Split")
np.random.seed(42)
X = np.random.rand(100, 2)
y = np.random.randint(0, 2, 100)

# Simple 80/20 split
split_index = int(0.8 * len(X))
X_train, X_test = X[:split_index], X[split_index:]
y_train, y_test = y[:split_index], y[split_index:]

print(f"Training set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}")

# ============================================================
# Using Scikit-learn's train_test_split
# ============================================================

# Example 6: Proper train_test_split
print("\nExample 6: Using train_test_split")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training features shape: {X_train.shape}")
print(f"Test features shape: {X_test.shape}")
print(f"Training targets shape: {y_train.shape}")
print(f"Test targets shape: {y_test.shape}")

# Example 7: Stratified split
print("\nExample 7: Stratified Split")
from sklearn.datasets import make_classification

X, y = make_classification(
    n_samples=1000, n_features=10, n_informative=5,
    n_redundant=2, random_state=42
)

print(f"Original class distribution: {np.bincount(y)}")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

print(f"Training class distribution: {np.bincount(y_train)}")
print(f"Test class distribution: {np.bincount(y_test)}")

# ============================================================
# Working with Pandas DataFrames
# ============================================================

# Example 8: Creating a DataFrame
print("\nExample 8: Pandas DataFrame")
data = {
    'square_feet': [1500, 2000, 1200, 1800, 2200],
    'bedrooms': [3, 4, 2, 3, 4],
    'age': [10, 5, 15, 8, 3],
    'price': [300000, 450000, 250000, 400000, 500000]
}

df = pd.DataFrame(data)
print(df)

# Example 9: DataFrame operations
print("\nExample 9: DataFrame Operations")
print("Shape:", df.shape)
print("Columns:", list(df.columns))
print("\nFirst 3 rows:")
print(df.head(3))

# Example 10: Selecting features and targets from DataFrame
print("\nExample 10: Features and Targets from DataFrame")
X = df[['square_feet', 'bedrooms', 'age']].values
y = df['price'].values

print("Features (X):")
print(X[:3])
print("\nTargets (y):")
print(y[:3])

# ============================================================
# Data Loading
# ============================================================

# Example 11: Loading from CSV (conceptual)
print("\nExample 11: Loading Data")
print("To load from CSV:")
print("df = pd.read_csv('data.csv')")
print("X = df.drop('target_column', axis=1)")
print("y = df['target_column']")

# Example 12: Loading sklearn datasets
print("\nExample 12: Loading sklearn Datasets")
from sklearn.datasets import load_iris

iris = load_iris()
iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)
iris_df['species'] = iris.target

print("Iris dataset:")
print(iris_df.head())
print(f"\nShape: {iris_df.shape}")

# ============================================================
# Data Exploration
# ============================================================

# Example 13: Basic statistics
print("\nExample 13: Basic Statistics")
print(df.describe())

# Example 14: Data types
print("\nExample 14: Data Types")
print(df.dtypes)

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("Summary:")
print("- Datasets consist of features (X) and targets (y)")
print("- Always split data into training and test sets")
print("- Use train_test_split for proper splitting")
print("- Pandas DataFrames are convenient for data manipulation")
print("- Explore your data before modeling")
print("="*60)