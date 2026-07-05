"""
W3Schools Python Tutorial - ML NN: Principal Component Analysis
===============================================================
Topics: PCA, Dimensionality Reduction, Explained Variance

Run: python 18-pca.py
Reference: https://www.w3schools.com/python/ml_pca.asp
"""

import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# ============================================================
# What is PCA?
# ============================================================

# Example 1: PCA concept
print("Example 1: PCA Concept")
print("Principal Component Analysis (PCA) reduces dimensions")
print("It finds new axes (principal components) that capture most variance")
print("Useful for visualization and reducing computation")

# ============================================================
# Loading Data
# ============================================================

# Example 2: Iris dataset
print("\nExample 2: Iris Dataset")
iris = load_iris()
X = iris.data
y = iris.target

print(f"Original shape: {X.shape}")
print(f"Features: {iris.feature_names}")
print(f"Classes: {iris.target_names}")

# ============================================================
# PCA Implementation
# ============================================================

# Example 3: Basic PCA
print("\nExample 3: Basic PCA")
# Scale data first
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

print(f"Original shape: {X.shape}")
print(f"PCA shape: {X_pca.shape}")
print(f"Reduced from {X.shape[1]} to {X_pca.shape[1]} dimensions")

# ============================================================
# Explained Variance
# ============================================================

# Example 4: Explained variance
print("\nExample 4: Explained Variance")
print(f"Explained variance ratio: {pca.explained_variance_ratio_}")
print(f"Total variance explained: {sum(pca.explained_variance_ratio_):.2%}")

# Example 5: Choosing number of components
print("\nExample 5: Choosing Components")
pca_full = PCA()
pca_full.fit(X_scaled)

cumulative_variance = np.cumsum(pca_full.explained_variance_ratio_)
print("Cumulative variance by component:")
for i, var in enumerate(cumulative_variance):
    print(f"  {i+1} components: {var:.2%}")

# ============================================================
# PCA for Visualization
# ============================================================

# Example 6: 2D visualization
print("\nExample 6: 2D Visualization Concept")
print("To visualize high-dimensional data in 2D:")
print("1. Apply PCA with n_components=2")
print("2. Plot the two principal components")
print("3. Color points by their class")

# ============================================================
# PCA for Speed
# ============================================================

# Example 7: Using PCA for faster training
print("\nExample 7: PCA for Faster Training")
# Original data
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Train on original data
model_orig = LogisticRegression(random_state=42, max_iter=200)
model_orig.fit(X_train, y_train)
acc_orig = accuracy_score(y_test, model_orig.predict(X_test))

# With PCA
pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)

model_pca = LogisticRegression(random_state=42, max_iter=200)
model_pca.fit(X_train_pca, y_train)
acc_pca = accuracy_score(y_test, model_pca.predict(X_test_pca))

print(f"Original ({X.shape[1]} features): Accuracy = {acc_orig:.4f}")
print(f"PCA ({X_pca.shape[1]} features): Accuracy = {acc_pca:.4f}")

# ============================================================
# Principal Components
# ============================================================

# Example 8: Understanding components
print("\nExample 8: Principal Components")
print(f"Principal components shape: {pca.components_.shape}")
print("\nFirst principal component:")
print(f"  {pca.components_[0]}")

print("\nSecond principal component:")
print(f"  {pca.components_[1]}")

# ============================================================
# Noise Reduction
# ============================================================

# Example 9: PCA for noise reduction
print("\nExample 9: PCA for Noise Reduction")
np.random.seed(42)
X_noisy = X_scaled + np.random.randn(*X_scaled.shape) * 0.5

# Apply PCA (reconstruct with fewer components)
pca_denoise = PCA(n_components=3)
X_reduced = pca_denoise.fit_transform(X_noisy)
X_reconstructed = pca_denoise.inverse_transform(X_reduced)

noise_original = np.mean((X_scaled - X_noisy) ** 2)
noise_removed = np.mean((X_scaled - X_reconstructed) ** 2)

print(f"MSE before PCA: {noise_original:.4f}")
print(f"MSE after PCA: {noise_removed:.4f}")
print("PCA can help reduce noise by keeping only important variance")

# ============================================================
# PCA Pipeline
# ============================================================

# Example 10: Complete pipeline
print("\nExample 10: PCA Pipeline")
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

# Create pipeline
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=2)),
    ('classifier', SVC(kernel='rbf'))
])

# Train
pipe.fit(X_train, y_train)

# Evaluate
y_pred = pipe.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Pipeline accuracy: {accuracy:.4f}")
print("Pipeline handles scaling, PCA, and classification")

# ============================================================
# When to Use PCA
# ============================================================

# Example 11: When to use PCA
print("\nExample 11: When to Use PCA")
print("Use PCA when:")
print("  - High-dimensional data (many features)")
print("  - Visualization of high-dim data")
print("  - Reducing computation time")
print("  - Noise reduction")

print("\nAvoid PCA when:")
print("  - Features are not correlated")
print("  - Interpretability is important")
print("  - Small dataset with few features")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("Summary:")
print("- PCA reduces dimensions while preserving variance")
print("- Use explained variance to choose components")
print("- Good for visualization and speed")
print("- Can help with noise reduction")
print("- Always scale data before PCA")
print("- Trade-off: less interpretability")
print("="*60)