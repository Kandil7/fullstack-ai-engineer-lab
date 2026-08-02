"""
W3Schools Python Tutorial - ML NN: Correlation
===============================================
Topics: Correlation Matrix, Feature Correlation with Target

Run: python 13-correlation.py
Reference: https://www.w3schools.com/python/ml_correlation.asp
"""

import numpy as np
import pandas as pd
from sklearn.datasets import make_regression

# ============================================================
# What is Correlation?
# ============================================================

# Example 1: Correlation concept
print("Example 1: Correlation Concept")
print("Correlation measures the linear relationship between two variables")
print("Range: -1 (perfect negative) to +1 (perfect positive)")
print("0 means no linear relationship")

# ============================================================
# Calculating Correlation
# ============================================================

# Example 2: Simple correlation
print("\nExample 2: Simple Correlation")
np.random.seed(42)
x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y = 2 * x + np.random.randn(10) * 2  # Strong positive correlation

# Manual calculation
x_mean = np.mean(x)
y_mean = np.mean(y)

numerator = np.sum((x - x_mean) * (y - y_mean))
denominator = np.sqrt(np.sum((x - x_mean)**2) * np.sum((y - y_mean)**2))
correlation = numerator / denominator

print(f"X: {x}")
print(f"Y: {y}")
print(f"Correlation: {correlation:.4f}")

# Example 3: Different correlation types
print("\nExample 3: Correlation Types")
# Perfect positive
x_perfect = np.array([1, 2, 3, 4, 5])
y_perfect_pos = np.array([2, 4, 6, 8, 10])
corr_pos = np.corrcoef(x_perfect, y_perfect_pos)[0, 1]
print(f"Perfect positive: {corr_pos:.4f}")

# Perfect negative
y_perfect_neg = np.array([10, 8, 6, 4, 2])
corr_neg = np.corrcoef(x_perfect, y_perfect_neg)[0, 1]
print(f"Perfect negative: {corr_neg:.4f}")

# No correlation
y_random = np.array([5, 2, 8, 1, 9])
corr_none = np.corrcoef(x_perfect, y_random)[0, 1]
print(f"No correlation: {corr_none:.4f}")

# ============================================================
# Correlation Matrix
# ============================================================

# Example 4: Correlation matrix
print("\nExample 4: Correlation Matrix")
np.random.seed(42)
n_samples = 100

# Generate correlated features
X1 = np.random.randn(n_samples)
X2 = X1 * 0.8 + np.random.randn(n_samples) * 0.2  # Correlated with X1
X3 = np.random.randn(n_samples)  # Independent
X4 = -X1 * 0.6 + np.random.randn(n_samples) * 0.4  # Negatively correlated

data = np.column_stack([X1, X2, X3, X4])
df = pd.DataFrame(data, columns=['X1', 'X2', 'X3', 'X4'])

# Calculate correlation matrix
corr_matrix = df.corr()
print("Correlation Matrix:")
print(corr_matrix)

# ============================================================
# Interpreting Correlation
# ============================================================

# Example 5: Correlation interpretation
print("\nExample 5: Interpreting Correlation Values")
print("Correlation strength:")
print("  0.0 - 0.2: Very weak")
print("  0.2 - 0.4: Weak")
print("  0.4 - 0.6: Moderate")
print("  0.6 - 0.8: Strong")
print("  0.8 - 1.0: Very strong")

# ============================================================
# Feature Correlation with Target
# ============================================================

# Example 6: Correlation with target
print("\nExample 6: Feature Correlation with Target")
np.random.seed(42)
X, y = make_regression(n_samples=200, n_features=5, noise=0.5, random_state=42)

# Create DataFrame
feature_names = [f'Feature_{i}' for i in range(X.shape[1])]
df = pd.DataFrame(X, columns=feature_names)
df['target'] = y

# Calculate correlations with target
target_corr = df.corr()['target'].drop('target')
print("Feature correlations with target:")
print(target_corr.sort_values(ascending=False))

# ============================================================
# Highly Correlated Features
# ============================================================

# Example 7: Finding highly correlated features
print("\nExample 7: Highly Correlated Features")
# Create features with high correlation
np.random.seed(42)
X1 = np.random.randn(100)
X2 = X1 * 0.95 + np.random.randn(100) * 0.05  # Very high correlation
X3 = np.random.randn(100)

df_features = pd.DataFrame({'X1': X1, 'X2': X2, 'X3': X3})
corr_matrix = df_features.corr()

print("Correlation Matrix:")
print(corr_matrix)

# Find pairs with correlation > 0.8
high_corr_pairs = []
for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        if abs(corr_matrix.iloc[i, j]) > 0.8:
            high_corr_pairs.append((
                corr_matrix.columns[i],
                corr_matrix.columns[j],
                corr_matrix.iloc[i, j]
            ))

print("\nHighly correlated pairs (|corr| > 0.8):")
for feat1, feat2, corr in high_corr_pairs:
    print(f"  {feat1} & {feat2}: {corr:.4f}")

# ============================================================
# Using Correlation for Feature Selection
# ============================================================

# Example 8: Feature selection
print("\nExample 8: Using Correlation for Feature Selection")
np.random.seed(42)
X, y = make_regression(n_samples=200, n_features=10, n_informative=3, random_state=42)

feature_names = [f'Feature_{i}' for i in range(X.shape[1])]
df = pd.DataFrame(X, columns=feature_names)
df['target'] = y

# Calculate correlations
target_corr = df.corr()['target'].drop('target').abs()

# Select features with correlation > 0.1
important_features = target_corr[target_corr > 0.1].index.tolist()
print(f"Selected features (|corr| > 0.1): {important_features}")

# ============================================================
# Correlation vs Causation
# ============================================================

# Example 9: Correlation != Causation
print("\nExample 9: Correlation != Causation")
print("High correlation does NOT mean causation")
print("Example: Ice cream sales correlate with drowning incidents")
print("  - Both increase in summer")
print("  - Ice cream doesn't cause drowning")
print("  - Temperature is a confounding variable")

# ============================================================
# Visualization Concept
# ============================================================

# Example 10: Correlation heatmap
print("\nExample 10: Correlation Heatmap")
print("To visualize correlation matrix:")
print("1. Create correlation matrix with df.corr()")
print("2. Use seaborn heatmap:")
print("   import seaborn as sns")
print("   sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')")
print("3. Use matplotlib for customization")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("Summary:")
print("- Correlation measures linear relationship between variables")
print("- Range: -1 to +1")
print("- Correlation matrix shows pairwise relationships")
print("- Use correlation for feature selection")
print("- Remember: correlation != causation")
print("- Visualize with heatmaps for better understanding")
print("="*60)