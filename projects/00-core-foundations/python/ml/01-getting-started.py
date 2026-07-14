"""
W3Schools Python Tutorial - ML NN: Getting Started with Machine Learning
========================================================================
Topics: What is Machine Learning, Types of ML, ML Workflow, Scikit-learn Overview

Run: python 01-getting-started.py
Reference: https://www.w3schools.com/python/ml_getting_started.asp
"""

import numpy as np
from sklearn import datasets

# ============================================================
# What is Machine Learning?
# ============================================================

# Example 1: Simple data generation
print("Example 1: Generating sample data")
np.random.seed(42)
X = np.random.rand(100, 1) * 10
y = 2 * X.squeeze() + 3 + np.random.randn(100) * 0.5
print(f"Generated {len(X)} data points")

# Example 2: Types of Machine Learning
print("\nExample 2: Types of ML")
ml_types = {
    "Supervised Learning": "Learns from labeled data (classification, regression)",
    "Unsupervised Learning": "Finds patterns in unlabeled data (clustering, dimensionality reduction)",
    "Reinforcement Learning": "Learns through trial and error with rewards"
}
for ml_type, description in ml_types.items():
    print(f"{ml_type}: {description}")

# ============================================================
# Types of Supervised Learning
# ============================================================

# Example 3: Classification vs Regression
print("\nExample 3: Classification vs Regression")
print("Classification: Predict discrete categories (e.g., spam/not spam)")
print("Regression: Predict continuous values (e.g., house prices)")

# ============================================================
# ML Workflow Overview
# ============================================================

# Example 4: Basic ML workflow steps
print("\nExample 4: ML Workflow Steps")
workflow_steps = [
    "1. Collect Data",
    "2. Prepare Data (cleaning, preprocessing)",
    "3. Choose Model",
    "4. Train Model",
    "5. Evaluate Model",
    "6. Tune Parameters",
    "7. Deploy Model"
]
for step in workflow_steps:
    print(step)

# ============================================================
# Introduction to Scikit-learn
# ============================================================

# Example 5: Loading a built-in dataset
print("\nExample 5: Loading Iris dataset")
iris = datasets.load_iris()
print(f"Dataset shape: {iris.data.shape}")
print(f"Features: {iris.feature_names}")
print(f"Target classes: {list(iris.target_names)}")

# Example 6: Basic data exploration
print("\nExample 6: Exploring the data")
print(f"First 5 samples:\n{iris.data[:5]}")
print(f"First 5 targets: {iris.target[:5]}")

# ============================================================
# Your First ML Model
# ============================================================

# Example 7: Simple k-Nearest Neighbors
print("\nExample 7: Simple k-NN model")
from sklearn.neighbors import KNeighborsClassifier

# Split data (simple approach)
X_train, X_test = iris.data[:100], iris.data[100:]
y_train, y_test = iris.target[:100], iris.target[100:]

# Create and train model
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

# Make predictions
predictions = knn.predict(X_test)
accuracy = np.mean(predictions == y_test)
print(f"Simple model accuracy: {accuracy:.2%}")

# ============================================================
# Working with Different Data Types
# ============================================================

# Example 8: Numerical data
print("\nExample 8: Numerical data example")
numerical_data = np.array([[1.0, 2.0, 3.0],
                           [4.0, 5.0, 6.0],
                           [7.0, 8.0, 9.0]])
print(f"Numerical data shape: {numerical_data.shape}")

# Example 9: Categorical data encoding
print("\nExample 9: Encoding categorical data")
from sklearn.preprocessing import LabelEncoder

categories = np.array(['cat', 'dog', 'bird', 'cat', 'dog'])
le = LabelEncoder()
encoded = le.fit_transform(categories)
print(f"Original: {categories}")
print(f"Encoded: {encoded}")
print(f"Classes: {le.classes_}")

# ============================================================
# Key ML Libraries
# ============================================================

# Example 10: Essential libraries
print("\nExample 10: Key ML libraries")
libraries = {
    "NumPy": "Numerical computing",
    "Pandas": "Data manipulation and analysis",
    "Scikit-learn": "Machine learning algorithms",
    "Matplotlib": "Data visualization",
    "Seaborn": "Statistical visualization"
}
for lib, purpose in libraries.items():
    print(f"{lib}: {purpose}")

# Summary
print("\n" + "="*60)
print("Summary:")
print("- Machine Learning: Systems that learn from data")
print("- Main types: Supervised, Unsupervised, Reinforcement")
print("- Scikit-learn provides easy-to-use ML tools")
print("- Basic workflow: Data -> Prepare -> Train -> Evaluate")
print("="*60)