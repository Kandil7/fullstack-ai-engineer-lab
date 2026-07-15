# Glossary: Support Vector Machines (Lecture 21)

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| SVM | Finds maximum margin hyperplane | `SVC()` |
| Hyperplane | Decision boundary separating classes | ax + by = c |
| Margin | Distance to nearest support vectors | Maximized by SVM |
| Support Vectors | Points closest to hyperplane | `svm.support_vectors_` |
| Kernel Trick | Maps data to higher dimensions | 'rbf', 'poly', 'linear' |
| RBF Kernel | Radial Basis Function (most common) | `kernel='rbf'` |
| C Parameter | Regularization strength | Small C = more regularization |
| gamma | Kernel coefficient | Large gamma = complex boundary |
| Linear SVM | Linear kernel for linearly separable data | `kernel='linear'` |
| Polynomial SVM | Polynomial kernel | `kernel='poly'` |
| Soft Margin | Allows some misclassification | C parameter controls |
| Hard Margin | No misclassification allowed | Rarely used |
| SVR | Support Vector Regression | `SVR()` |
| Decision Function | Distance to hyperplane | `svm.decision_function()` |
| Platt Scaling | Probability calibration for SVM | `probability=True` |

---

## Detailed Term Definitions

### Support Vector Machine (SVM)

**Definition:** A supervised learning algorithm that finds the optimal hyperplane to separate classes by maximizing the margin between them.

**Example:**
```python
from sklearn.svm import SVC
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

X, y = make_classification(n_samples=200, n_features=2, 
                           n_redundant=0, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features (IMPORTANT!)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train SVM
svm = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42)
svm.fit(X_train_scaled, y_train)

# Evaluate
accuracy = accuracy_score(y_test, svm.predict(X_test_scaled))
print(f"Accuracy: {accuracy:.4f}")
```

**Related Terms:** Maximum Margin, Support Vectors, Kernel Trick

---

### Hyperplane

**Definition:** The decision boundary that separates classes in SVM. In n-dimensional space, it's an (n-1)-dimensional surface.

**Example:**
```python
from sklearn.svm import SVC
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=200, n_features=2, 
                           n_redundant=0, random_state=42)

svm = SVC(kernel='linear', random_state=42)
svm.fit(X, y)

# For linear SVM, hyperplane is defined by coefficients
# Decision function: w·x + b = 0
print(f"Coefficients (w): {svm.coef_[0]}")
print(f"Intercept (b): {svm.intercept_[0]}")

# Equation: w[0]*x1 + w[1]*x2 + b = 0
```

**Related Terms:** Decision Boundary, Margin, Linear Classifier

---

### Margin

**Definition:** The distance between the hyperplane and the nearest support vectors. SVM maximizes this margin.

**Example:**
```python
from sklearn.svm import SVC
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=200, n_features=2, 
                           n_redundant=0, random_state=42)

svm = SVC(kernel='linear', random_state=42)
svm.fit(X, y)

# Decision function gives signed distance to hyperplane
decision_values = svm.decision_function(X)

# Margin is the minimum absolute decision value
margin = np.min(np.abs(decision_values))
print(f"Minimum margin: {margin:.4f}")

# Support vectors are exactly on the margin boundary
support_mask = np.zeros(len(X), dtype=bool)
support_mask[svm.support_] = True
print(f"Support vectors on margin: {sum(support_mask)}")
```

**Related Terms:** Support Vectors, Maximum Margin Classifier

---

### Support Vectors

**Definition:** The data points that lie closest to the decision boundary. Only these points determine the hyperplane position.

**Example:**
```python
from sklearn.svm import SVC
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=200, n_features=10, 
                           n_informative=5, random_state=42)

svm = SVC(kernel='rbf', random_state=42)
svm.fit(X, y)

print(f"Number of support vectors per class: {svm.n_support_}")
print(f"Total support vectors: {sum(svm.n_support_)}")
print(f"Support vectors shape: {svm.support_vectors_.shape}")

# Get support vector indices
support_indices = svm.support_
print(f"Support vector indices (first 10): {support_indices[:10]}")
```

**Related Terms:** Decision Boundary, Margin, Sparse Model

---

### Kernel Trick

**Definition:** A technique that transforms data to higher dimensions where it becomes linearly separable, without explicitly computing the transformation.

**Example:**
```python
from sklearn.svm import SVC
from sklearn.datasets import make_circles
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Non-linear data
X, y = make_circles(n_samples=200, noise=0.1, factor=0.5, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Linear kernel fails on non-linear data
svm_linear = SVC(kernel='linear')
svm_linear.fit(X_train_scaled, y_train)
acc_linear = accuracy_score(y_test, svm_linear.predict(X_test_scaled))

# RBF kernel handles non-linearity
svm_rbf = SVC(kernel='rbf')
svm_rbf.fit(X_train_scaled, y_train)
acc_rbf = accuracy_score(y_test, svm_rbf.predict(X_test_scaled))

print(f"Linear kernel: {acc_linear:.4f}")
print(f"RBF kernel: {acc_rbf:.4f}")
```

**Related Terms:** RBF Kernel, Polynomial Kernel, Higher Dimensions

---

### RBF Kernel (Radial Basis Function)

**Definition:** The most commonly used kernel for SVM. Maps data to infinite-dimensional space using Gaussian functions.

**Formula:**
```
K(x, x') = exp(-γ||x - x'||²)
```

**Example:**
```python
from sklearn.svm import SVC
from sklearn.datasets import make_moons
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV

X, y = make_moons(n_samples=200, noise=0.1, random_state=42)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Tune gamma for RBF kernel
param_grid = {'C': [0.1, 1, 10], 'gamma': [0.1, 1, 10]}
grid = GridSearchCV(SVC(kernel='rbf'), param_grid, cv=5)
grid.fit(X_scaled, y)

print(f"Best parameters: {grid.best_params_}")
print(f"Best accuracy: {grid.best_score_:.4f}")
```

**Related Terms:** Kernel Trick, gamma Parameter

---

### C Parameter

**Definition:** Regularization parameter controlling the trade-off between maximizing margin and minimizing classification error.

- Small C: More regularization, simpler model, wider margin
- Large C: Less regularization, complex model, narrower margin

**Example:**
```python
from sklearn.svm import SVC
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler

X, y = make_classification(n_samples=200, n_features=10, 
                           n_informative=5, random_state=42)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("Effect of C parameter:")
for C in [0.001, 0.01, 0.1, 1, 10, 100, 1000]:
    svm = SVC(kernel='rbf', C=C, random_state=42)
    scores = cross_val_score(svm, X_scaled, y, cv=5, scoring='accuracy')
    print(f"  C={C:7.3f}: {scores.mean():.4f}")
```

**Related Terms:** Regularization, Margin, gamma

---

### gamma Parameter

**Definition:** Kernel coefficient for RBF and polynomial kernels. Controls the influence of individual training examples.

- Small gamma: Far reach, smoother boundary
- Large gamma: Close reach, complex boundary

**Example:**
```python
from sklearn.svm import SVC
from sklearn.datasets import make_moons
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score

X, y = make_moons(n_samples=200, noise=0.1, random_state=42)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("Effect of gamma parameter:")
for gamma in [0.001, 0.01, 0.1, 1, 10, 100]:
    svm = SVC(kernel='rbf', gamma=gamma, random_state=42)
    scores = cross_val_score(svm, X_scaled, y, cv=5, scoring='accuracy')
    print(f"  gamma={gamma:7.3f}: {scores.mean():.4f}")
```

**Related Terms:** C Parameter, Kernel Coefficient

---

### Linear SVM

**Definition:** SVM with a linear kernel, suitable for linearly separable data. Faster than non-linear kernels.

**Example:**
```python
from sklearn.svm import SVC
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X, y = make_classification(n_samples=200, n_features=2, 
                           n_redundant=0, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

svm_linear = SVC(kernel='linear', C=1.0, random_state=42)
svm_linear.fit(X_train_scaled, y_train)

accuracy = accuracy_score(y_test, svm_linear.predict(X_test_scaled))
print(f"Linear SVM accuracy: {accuracy:.4f}")
```

**Related Terms:** RBF Kernel, Linear Classifier

---

### Polynomial SVM

**Definition:** SVM with a polynomial kernel, suitable for polynomial relationships between features.

**Example:**
```python
from sklearn.svm import SVC
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler

X, y = make_classification(n_samples=200, n_features=2, 
                           n_redundant=0, random_state=42)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Different polynomial degrees
for degree in [2, 3, 4, 5]:
    svm = SVC(kernel='poly', degree=degree, random_state=42)
    svm.fit(X_scaled, y)
    n_sv = sum(svm.n_support_)
    print(f"Degree {degree}: Support vectors={n_sv}")
```

**Related Terms:** Kernel Trick, RBF Kernel

---

### Soft Margin

**Definition:** Allows some misclassifications to achieve a wider, more generalizable margin. Controlled by C parameter.

**Example:**
```python
from sklearn.svm import SVC
from sklearn.datasets import make_classification
import numpy as np

# Add some noise to make data not perfectly separable
np.random.seed(42)
X, y = make_classification(n_samples=200, n_features=2, 
                           n_redundant=0, flip_y=0.1, random_state=42)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Hard margin (large C) - tries to classify everything correctly
svm_hard = SVC(kernel='linear', C=1000)
svm_hard.fit(X_scaled, y)
train_acc = (svm_hard.predict(X_scaled) == y).mean()

# Soft margin (small C) - allows some errors
svm_soft = SVC(kernel='linear', C=0.1)
svm_soft.fit(X_scaled, y)
train_acc_soft = (svm_soft.predict(X_scaled) == y).mean()

print(f"Hard margin (C=1000) train accuracy: {train_acc:.4f}")
print(f"Soft margin (C=0.1) train accuracy: {train_acc_soft:.4f}")
print("Soft margin is often more generalizable!")
```

**Related Terms:** C Parameter, Overfitting, Generalization

---

### SVR (Support Vector Regression)

**Definition:** Regression variant of SVM that finds a function that deviates from target values by at most epsilon.

**Example:**
```python
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
import numpy as np

np.random.seed(42)
X = np.random.rand(200, 1) * 10
y = 2 * X.squeeze() + 3 + np.random.randn(200) * 0.5

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

svr = SVR(kernel='rbf', C=1.0, epsilon=0.1)
svr.fit(X_train_scaled, y_train)

y_pred = svr.predict(X_test_scaled)
r2 = r2_score(y_test, y_pred)
print(f"SVR R² Score: {r2:.4f}")
```

**Related Terms:** SVM, Regression, Epsilon

---

## Formulas Summary

| Formula | Expression |
|---------|-----------|
| RBF Kernel | K(x, x') = exp(-γ\|\|x - x'\|\|²) |
| Linear Kernel | K(x, x') = x · x' |
| Polynomial Kernel | K(x, x') = (γx · x' + r)^d |
| Decision Function | f(x) = sign(w · x + b) |
| Margin | 2 / \|\|w\|\| |

---

## Code Snippets Quick Reference

```python
# SVM Classification
from sklearn.svm import SVC
svm = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42)
svm.fit(X_train_scaled, y_train)
y_pred = svm.predict(X_test_scaled)

# SVM Regression
from sklearn.svm import SVR
svr = SVR(kernel='rbf', C=1.0, epsilon=0.1)
svr.fit(X_train_scaled, y_train)

# Support Vectors
print(svm.n_support_)
print(svm.support_vectors_)

# Decision Function
distances = svm.decision_function(X_test_scaled)

# Probability (requires Platt scaling)
svm_prob = SVC(kernel='rbf', probability=True)
svm_prob.fit(X_train_scaled, y_train)
probabilities = svm_prob.predict_proba(X_test_scaled)

# Pipeline
from sklearn.pipeline import Pipeline
pipe = Pipeline([('scaler', StandardScaler()), ('svm', SVC())])
```

---

## Common Pitfalls

1. **Not scaling** — SVM is very sensitive to feature scales
2. **Wrong kernel** — Linear kernel fails on non-linear data
3. **Poor C/gamma tuning** — Default may not be optimal
4. **Large datasets** — SVM is O(n²) to O(n³)
5. **No probabilities** — Use probability=True for probabilities

---

## Further Reading

- [Scikit-learn - SVM](https://scikit-learn.org/stable/modules/svm.html)
- [Wikipedia - SVM](https://en.wikipedia.org/wiki/Support_vector_machine)
- [MIT OpenCourseWare - SVM](https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/pages/lecture-16-learning-support-vector-machines/)
