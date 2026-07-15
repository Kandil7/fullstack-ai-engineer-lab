"""
W3Schools Python Tutorial - ML NN: Support Vector Machines
===========================================================
Topics: SVM Classifier, Hyperplane, Kernel Trick

Run: python 21-svm.py
Reference: https://www.w3schools.com/python/ml_svm.asp
"""

import numpy as np
from sklearn.svm import SVC, SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, r2_score
from sklearn.datasets import make_classification, make_circles
from sklearn.preprocessing import StandardScaler

# ============================================================
# What is SVM?
# ============================================================

# Example 1: SVM concept
print("Example 1: SVM Concept")
print("Support Vector Machine finds the best hyperplane to separate classes")
print("The hyperplane maximizes the margin between classes")
print("Support vectors are the closest points to the hyperplane")

# ============================================================
# Linear SVM
# ============================================================

# Example 2: Generate linear data
print("\nExample 2: Linear Data")
np.random.seed(42)
X, y = make_classification(
    n_samples=200, n_features=2, n_redundant=0,
    n_informative=2, random_state=42, n_clusters_per_class=1
)

print(f"Samples: {X.shape[0]}")
print(f"Features: {X.shape[1]}")

# Example 3: Train/test split
print("\nExample 3: Train/Test Split")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Example 4: Linear SVM
print("\nExample 4: Linear SVM")
svm_linear = SVC(kernel='linear', random_state=42)
svm_linear.fit(X_train_scaled, y_train)

y_pred = svm_linear.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.4f}")
print(f"Number of support vectors: {svm_linear.n_support_}")

# ============================================================
# Hyperplane
# ============================================================

# Example 5: Understanding hyperplane
print("\nExample 5: Hyperplane Concept")
print("In 2D: hyperplane is a line (ax + by = c)")
print("In 3D: hyperplane is a plane")
print("In higher dimensions: hyperplane is (n-1) dimensional")

print("\nSVM finds the hyperplane that maximizes the margin")
print("Margin = distance between hyperplane and nearest support vectors")

# ============================================================
# Kernel Trick
# ============================================================

# Example 6: Non-linear data
print("\nExample 6: Non-Linear Data")
X_circles, y_circles = make_circles(n_samples=200, noise=0.1, factor=0.5, random_state=42)

print("This data is not linearly separable")
print("We need the kernel trick to handle it")

# Example 7: Different kernels
print("\nExample 7: Different Kernels")
kernels = ['linear', 'rbf', 'poly', 'sigmoid']

X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
    X_circles, y_circles, test_size=0.2, random_state=42
)

scaler_c = StandardScaler()
X_train_c_scaled = scaler_c.fit_transform(X_train_c)
X_test_c_scaled = scaler_c.transform(X_test_c)

for kernel in kernels:
    svm = SVC(kernel=kernel, random_state=42)
    svm.fit(X_train_c_scaled, y_train_c)
    acc = accuracy_score(y_test_c, svm.predict(X_test_c_scaled))
    print(f"{kernel:>10}: Accuracy = {acc:.4f}")

# ============================================================
# SVM Parameters
# ============================================================

# Example 8: Key parameters
print("\nExample 8: SVM Parameters")
print("C: Regularization parameter (smaller = more regularization)")
print("gamma: Kernel coefficient (larger = more complex boundary)")
print("kernel: 'linear', 'rbf', 'poly', 'sigmoid'")

# Example 9: Parameter tuning
print("\nExample 9: Parameter Tuning")
results = []
for C in [0.1, 1, 10, 100]:
    for gamma in [0.1, 1, 10]:
        svm = SVC(kernel='rbf', C=C, gamma=gamma, random_state=42)
        svm.fit(X_train_scaled, y_train)
        acc = accuracy_score(y_test, svm.predict(X_test_scaled))
        results.append({'C': C, 'gamma': gamma, 'accuracy': acc})

# Find best
best = max(results, key=lambda x: x['accuracy'])
print(f"Best parameters: C={best['C']}, gamma={best['gamma']}")
print(f"Best accuracy: {best['accuracy']:.4f}")

# ============================================================
# Support Vectors
# ============================================================

# Example 10: Support vectors
print("\nExample 10: Support Vectors")
svm = SVC(kernel='rbf', random_state=42)
svm.fit(X_train_scaled, y_train)

print(f"Number of support vectors per class: {svm.n_support_}")
print(f"Total support vectors: {sum(svm.n_support_)}")
print(f"Support vectors shape: {svm.support_vectors_.shape}")

# ============================================================
# SVM for Regression
# ============================================================

# Example 11: SVR
print("\nExample 11: SVM for Regression")
np.random.seed(42)
X_reg = np.random.rand(200, 1) * 10
y_reg = 2 * X_reg.squeeze() + 3 + np.random.randn(200) * 0.5

X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

scaler_reg = StandardScaler()
X_train_reg_scaled = scaler_reg.fit_transform(X_train_reg)
X_test_reg_scaled = scaler_reg.transform(X_test_reg)

svr = SVR(kernel='rbf')
svr.fit(X_train_reg_scaled, y_train_reg)

r2 = r2_score(y_test_reg, svr.predict(X_test_reg_scaled))
print(f"SVR R^2 score: {r2:.4f}")

# ============================================================
# When to Use SVM
# ============================================================

# Example 12: Use cases
print("\nExample 12: When to Use SVM")
print("Advantages:")
print("  - Effective in high-dimensional spaces")
print("  - Memory efficient (uses support vectors only)")
print("  - Versatile (different kernels)")

print("\nDisadvantages:")
print("  - Slow on large datasets")
print("  - Sensitive to feature scaling")
print("  - Not good with noisy data")
print("  - No probability estimates by default")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("Summary:")
print("- SVM finds the best hyperplane to separate classes")
print("- Kernel trick handles non-linear data")
print("- RBF kernel is most common")
print("- Scale features before SVM")
print("- Good for high-dimensional data")
print("- Tune C and gamma for best performance")
print("="*60)