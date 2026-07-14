"""
W3Schools Python Tutorial - ML NN: Confusion Matrix
====================================================
Topics: Confusion Matrix, Accuracy, Precision, Recall, F1 Score

Run: python 12-confusion-matrix.py
Reference: https://www.w3schools.com/python/ml_confusion_matrix.asp
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (confusion_matrix, accuracy_score, 
                           precision_score, recall_score, f1_score,
                           classification_report)
from sklearn.datasets import make_classification

# ============================================================
# What is a Confusion Matrix?
# ============================================================

# Example 1: Simple confusion matrix
print("Example 1: Confusion Matrix Concept")
print("A confusion matrix shows the performance of a classifier")
print("It compares actual vs predicted labels")

# Create simple example
y_actual = np.array([1, 1, 0, 0, 1, 0, 1, 0, 0, 1])
y_predicted = np.array([1, 0, 0, 0, 1, 1, 1, 0, 0, 1])

cm = confusion_matrix(y_actual, y_predicted)
print(f"\nActual:    {y_actual}")
print(f"Predicted: {y_predicted}")
print(f"\nConfusion Matrix:\n{cm}")

# ============================================================
# Understanding the Matrix
# ============================================================

# Example 2: Matrix components
print("\nExample 2: Matrix Components")
tn, fp, fn, tp = cm.ravel()
print(f"True Negatives (TN): {tn} (correctly predicted 0)")
print(f"False Positives (FP): {fp} (incorrectly predicted 1)")
print(f"False Negatives (FN): {fn} (incorrectly predicted 0)")
print(f"True Positives (TP): {tp} (correctly predicted 1)")

# ============================================================
# Accuracy
# ============================================================

# Example 3: Accuracy calculation
print("\nExample 3: Accuracy")
accuracy = accuracy_score(y_actual, y_predicted)
print(f"Accuracy: {accuracy:.4f}")
print(f"Formula: (TP + TN) / (TP + TN + FP + FN)")
print(f"Calculation: ({tp} + {tn}) / ({tp} + {tn} + {fp} + {fn}) = {(tp+tn)/(tp+tn+fp+fn):.4f}")

# ============================================================
# Precision
# ============================================================

# Example 4: Precision
print("\nExample 4: Precision")
precision = precision_score(y_actual, y_predicted)
print(f"Precision: {precision:.4f}")
print(f"Formula: TP / (TP + FP)")
print(f"Calculation: {tp} / ({tp} + {fp}) = {tp/(tp+fp):.4f}")
print("Precision: Of all predicted positives, how many are actually positive?")

# ============================================================
# Recall (Sensitivity)
# ============================================================

# Example 5: Recall
print("\nExample 5: Recall")
recall = recall_score(y_actual, y_predicted)
print(f"Recall: {recall:.4f}")
print(f"Formula: TP / (TP + FN)")
print(f"Calculation: {tp} / ({tp} + {fn}) = {tp/(tp+fn):.4f}")
print("Recall: Of all actual positives, how many did we catch?")

# ============================================================
# F1 Score
# ============================================================

# Example 6: F1 Score
print("\nExample 6: F1 Score")
f1 = f1_score(y_actual, y_predicted)
print(f"F1 Score: {f1:.4f}")
print(f"Formula: 2 x (Precision x Recall) / (Precision + Recall)")
print(f"Calculation: 2 x ({precision:.4f} x {recall:.4f}) / ({precision:.4f} + {recall:.4f}) = {f1:.4f}")
print("F1 Score: Harmonic mean of precision and recall")

# ============================================================
# Real Example with Model
# ============================================================

# Example 7: Classification model
print("\nExample 7: Real Classification Example")
np.random.seed(42)
X, y = make_classification(
    n_samples=300, n_features=10, n_informative=5,
    n_redundant=2, random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Train model
model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
print(f"Confusion Matrix:\n{cm}")

# ============================================================
# Classification Report
# ============================================================

# Example 8: Full classification report
print("\nExample 8: Classification Report")
print(classification_report(y_test, y_pred))

# ============================================================
# Multi-class Confusion Matrix
# ============================================================

# Example 9: Multi-class example
print("\nExample 9: Multi-class Confusion Matrix")
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

cm = confusion_matrix(y_test, y_pred)
print(f"3-class Confusion Matrix:\n{cm}")
print(f"\nClass names: {iris.target_names}")

# ============================================================
# When to Use Each Metric
# ============================================================

# Example 10: Metric selection
print("\nExample 10: When to Use Each Metric")
print("Accuracy: When classes are balanced")
print("Precision: When false positives are costly (spam detection)")
print("Recall: When false negatives are costly (disease detection)")
print("F1 Score: When you need balance between precision and recall")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("Summary:")
print("- Confusion matrix shows TP, TN, FP, FN")
print("- Accuracy = (TP + TN) / Total")
print("- Precision = TP / (TP + FP)")
print("- Recall = TP / (TP + FN)")
print("- F1 Score = 2 x (Precision x Recall) / (Precision + Recall)")
print("- Choose metric based on problem requirements")
print("="*60)