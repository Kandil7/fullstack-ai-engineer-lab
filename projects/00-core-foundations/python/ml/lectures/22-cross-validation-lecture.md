# Lecture 22: Cross-Validation

## Topic Overview

Cross-validation is a technique for evaluating machine learning models by splitting data into multiple folds and training/testing on different combinations. This lecture covers K-Fold, Stratified K-Fold, different scoring metrics, and best practices for reliable model evaluation.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand why cross-validation is better than a single train/test split
2. Implement K-Fold and Stratified K-Fold cross-validation
3. Use cross_val_score for easy evaluation
4. Choose appropriate scoring metrics
5. Apply cross-validation to both classification and regression
6. Select the optimal number of folds

---

## Key Concepts

### 1. Why Cross-Validation?

A single train/test split can give unreliable estimates due to randomness. Cross-validation provides more robust evaluation by using all data for both training and testing.

### 2. K-Fold Cross-Validation

Splits data into K equal folds, trains on K-1 folds, tests on the remaining fold. Repeats K times.

### 3. Stratified K-Fold

Preserves class distribution in each fold. Essential for imbalanced datasets.

### 4. Leave-One-Out (LOO)

Special case where K = number of samples. Very expensive but no bias.

---

## Code Examples

### Example 1: Problem with Single Split

```python
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score

X, y = make_classification(n_samples=200, n_features=10, random_state=42)

# Different random splits give different results
print("Different random splits give different accuracy scores:")
for i in range(5):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2  # No random_state = different each time
    )
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"  Split {i+1}: {acc:.4f}")

print("\nCross-validation gives more reliable estimates!")
```

### Example 2: K-Fold Cross-Validation

```python
import numpy as np
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score

X, y = make_classification(n_samples=200, n_features=10, random_state=42)

# Manual K-Fold
kf = KFold(n_splits=5, shuffle=True, random_state=42)

scores = []
for train_idx, val_idx in kf.split(X):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]
    
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    score = accuracy_score(y_val, model.predict(X_val))
    scores.append(score)

print(f"Fold scores: {[f'{s:.4f}' for s in scores]}")
print(f"Mean: {np.mean(scores):.4f} +/- {np.std(scores):.4f}")
```

### Example 3: Using cross_val_score

```python
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=200, n_features=10, random_state=42)

model = LogisticRegression(random_state=42)
cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')

print(f"CV scores: {[f'{s:.4f}' for s in cv_scores]}")
print(f"Mean: {cv_scores.mean():.4f}")
print(f"Std: {cv_scores.std():.4f}")
```

### Example 4: Stratified K-Fold

```python
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score
import numpy as np

# Imbalanced dataset
X, y = make_classification(n_samples=200, n_features=10, 
                           weights=[0.7, 0.3], random_state=42)

print(f"Original class distribution: {np.bincount(y)}")

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
stratified_scores = []

for train_idx, val_idx in skf.split(X, y):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]
    
    # Check distribution
    train_dist = np.bincount(y_train)
    val_dist = np.bincount(y_val)
    
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    score = accuracy_score(y_val, model.predict(X_val))
    stratified_scores.append(score)

print(f"Stratified CV scores: {[f'{s:.4f}' for s in stratified_scores]}")
print(f"Mean: {np.mean(stratified_scores):.4f}")
```

### Example 5: Different Scoring Metrics

```python
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=200, n_features=10, random_state=42)

model = LogisticRegression(random_state=42)

# Different metrics
metrics = ['accuracy', 'f1', 'precision', 'recall', 'roc_auc']
print("Different Scoring Metrics:")
print("-" * 35)

for metric in metrics:
    scores = cross_val_score(model, X, y, cv=5, scoring=metric)
    print(f"{metric:12s}: {scores.mean():.4f} +/- {scores.std():.4f}")
```

### Example 6: Cross-Validation for Regression

```python
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
import numpy as np

X, y = make_regression(n_samples=200, n_features=5, noise=0.5, random_state=42)

model = LinearRegression()

# Different regression metrics
r2_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
neg_mse_scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_squared_error')

print(f"R² scores: {[f'{s:.4f}' for s in r2_scores]}")
print(f"Mean R²: {r2_scores.mean():.4f}")
print(f"Mean MSE: {-neg_mse_scores.mean():.4f}")
```

### Example 7: Choosing Number of Folds

```python
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=200, n_features=10, random_state=42)

model = LogisticRegression(random_state=42)
results = []

print("Effect of Number of Folds:")
for k in [3, 5, 10, 15, 20]:
    scores = cross_val_score(model, X, y, cv=k, scoring='accuracy')
    results.append({'k': k, 'mean': scores.mean(), 'std': scores.std()})
    print(f"K={k:2d}: Mean={scores.mean():.4f} +/- {scores.std():.4f}")
```

### Example 8: Cross-Validation vs Holdout

```python
print("Holdout (single split):")
print("  ✓ Fast")
print("  ✓ Simple")
print("  ✗ Less reliable")
print("  ✗ Wastes data")

print("\nCross-validation:")
print("  ✓ More reliable")
print("  ✓ Uses all data for training")
print("  ✗ Slower")
print("  ✗ More complex")

print("\nRecommendations:")
print("  - Use 5 or 10 folds for good balance")
print("  - Use stratified for classification")
print("  - Use cross-validation for model selection")
print("  - Use test set only for final evaluation")
```

---

## Common Mistakes to Avoid

### Mistake 1: Using CV for Final Evaluation

```python
# WRONG: Using CV score as final performance
cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
final_score = cv_scores.mean()  # This is for model selection only!

# CORRECT: Use test set for final evaluation
# 1. Use CV to select best model/hyperparameters
# 2. Train on full training set
# 3. Evaluate ONCE on test set
model.fit(X_train, y_train)
test_score = model.score(X_test, y_test)  # Final evaluation
```

### Mistake 2: Not Stratifying for Imbalanced Data

```python
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=200, n_features=10, 
                           weights=[0.7, 0.3], random_state=42)

# WRONG: Regular KFold on imbalanced data
kf = KFold(n_splits=5, shuffle=True, random_state=42)
for train_idx, val_idx in kf.split(X):
    print(f"Train class dist: {np.bincount(y[train_idx])}")

# CORRECT: StratifiedKFold preserves class distribution
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
for train_idx, val_idx in skf.split(X, y):
    print(f"Train class dist: {np.bincount(y[train_idx])}")
```

### Mistake 3: Data Leakage

```python
# WRONG: Fitting scaler on all data before CV
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # WRONG! Uses test data info

# CORRECT: Fit scaler within CV loop
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression())
])
scores = cross_val_score(pipeline, X, y, cv=5)  # Correct!
```

---

## Best Practices

### 1. Use Pipeline to Prevent Leakage

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression(random_state=42))
])

scores = cross_val_score(pipeline, X, y, cv=5, scoring='accuracy')
print(f"CV accuracy: {scores.mean():.4f}")
```

### 2. Report Mean and Std

```python
scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f"Accuracy: {scores.mean():.4f} +/- {scores.std():.4f}")
```

### 3. Use 5 or 10 Folds

```python
# 5 or 10 folds is usually a good balance
scores_5 = cross_val_score(model, X, y, cv=5, scoring='accuracy')
scores_10 = cross_val_score(model, X, y, cv=10, scoring='accuracy')

print(f"5 folds: {scores_5.mean():.4f} +/- {scores_5.std():.4f}")
print(f"10 folds: {scores_10.mean():.4f} +/- {scores_10.std():.4f}")
```

### 4. Use Stratified for Classification

```python
from sklearn.model_selection import cross_val_score, StratifiedKFold

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=skf, scoring='accuracy')
```

---

## Practice Exercises

### Exercise 1: Compare CV Methods

```python
"""
Compare KFold vs StratifiedKFold on imbalanced data.
1. Create imbalanced dataset
2. Apply both methods
3. Compare results
"""
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=200, n_features=10, 
                           weights=[0.7, 0.3], random_state=42)

# Your code here
kf = KFold(n_splits=5, shuffle=True, random_state=42)
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

model = LogisticRegression(random_state=42)

scores_kf = cross_val_score(model, X, y, cv=kf, scoring='f1')
scores_skf = cross_val_score(model, X, y, cv=skf, scoring='f1')

print(f"KFold F1: {scores_kf.mean():.4f} +/- {scores_kf.std():.4f}")
print(f"StratifiedKFold F1: {scores_skf.mean():.4f} +/- {scores_skf.std():.4f}")
```

### Exercise 2: Model Selection with CV

```python
"""
Use cross-validation to select the best model.
1. Compare Logistic Regression, SVM, Random Forest
2. Use CV for fair comparison
3. Select best model
"""
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

models = {
    'Logistic Regression': Pipeline([
        ('scaler', StandardScaler()),
        ('model', LogisticRegression(random_state=42))
    ]),
    'SVM': Pipeline([
        ('scaler', StandardScaler()),
        ('model', SVC(random_state=42))
    ]),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
}

for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
    print(f"{name:25s}: {scores.mean():.4f} +/- {scores.std():.4f}")
```

### Exercise 3: Hyperparameter Tuning with CV

```python
"""
Tune hyperparameters using cross-validation.
1. Tune C for SVM
2. Use GridSearchCV
3. Report best parameters
"""
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('svm', SVC())
])

param_grid = {
    'svm__C': [0.1, 1, 10, 100],
    'svm__gamma': [0.1, 1, 10]
}

grid = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
grid.fit(X, y)

print(f"Best parameters: {grid.best_params_}")
print(f"Best CV accuracy: {grid.best_score_:.4f}")
```

---

## Summary

| Concept | Description |
|---------|-------------|
| **Cross-Validation** | Evaluate model using multiple train/test splits |
| **K-Fold** | Split into K folds, rotate test set |
| **Stratified K-Fold** | Preserves class distribution |
| **cross_val_score** | Easy way to run CV |
| **Scoring Metrics** | accuracy, f1, precision, recall, etc. |
| **Pipeline** | Prevents data leakage |

### Key Takeaways

1. **Always use cross-validation** for model evaluation
2. Use **StratifiedKFold** for classification
3. Use **pipelines** to prevent data leakage
4. Report **mean ± std** of CV scores
5. Use CV for **model selection**, test set for **final evaluation**

---

## Next Steps

- **Lecture 23**: KNN — Instance-based learning
- **Review previous lectures** with proper evaluation

---

## References

- [W3Schools - Cross Validation](https://www.w3schools.com/python/ml_cross_validation.asp)
- [Scikit-learn Documentation - CV](https://scikit-learn.org/stable/modules/cross_validation.html)
- [Wikipedia - Cross-validation](https://en.wikipedia.org/wiki/Cross-validation_(statistics))
