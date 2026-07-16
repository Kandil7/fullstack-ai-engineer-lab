# Lecture 19: Naive Bayes

## Topic Overview

Naive Bayes is a family of probabilistic classifiers based on Bayes' theorem with the "naive" assumption that features are independent. Despite this often-violated assumption, Naive Bayes works surprisingly well in practice, especially for text classification. This lecture covers Bayes' theorem, Gaussian Naive Bayes, and practical applications like spam detection.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand Bayes' theorem and how it applies to classification
2. Explain the "naive" independence assumption
3. Implement Gaussian Naive Bayes with scikit-learn
4. Choose the right Naive Bayes variant for your data
5. Evaluate Naive Bayes models
6. Apply to text classification problems
7. Understand advantages and limitations

---

## Key Concepts

### 1. Bayes' Theorem

```
P(class|features) = P(features|class) × P(class) / P(features)
```

Where:
- `P(class|features)` = Posterior probability (what we want)
- `P(features|class)` = Likelihood
- `P(class)` = Prior probability
- `P(features)` = Evidence (constant for all classes)

### 2. The "Naive" Assumption

Features are conditionally independent given the class:

```
P(x₁, x₂, ..., xₙ|class) = P(x₁|class) × P(x₂|class) × ... × P(xₙ|class)
```

### 3. Naive Bayes Variants

| Variant | Data Type | Use Case |
|---------|-----------|----------|
| **GaussianNB** | Continuous (normal) | General classification |
| **MultinomialNB** | Discrete counts | Text (word counts) |
| **BernoulliNB** | Binary (0/1) | Text (word presence) |

### 4. Why It Works Despite Independence Assumption

- Independence assumption is often violated in practice
- But classification only needs correct ranking, not exact probabilities
- Errors from violating assumption often cancel out

---

## Code Examples

### Example 1: Bayes' Theorem Calculation

```python
# Disease test example
p_disease = 0.01  # 1% prevalence
p_positive_given_disease = 0.99  # 99% sensitivity
p_positive_given_no_disease = 0.05  # 5% false positive rate

# P(positive) = P(positive|disease) × P(disease) + P(positive|no disease) × P(no disease)
p_positive = (p_positive_given_disease * p_disease + 
              p_positive_given_no_disease * (1 - p_disease))

# P(disease|positive) = P(positive|disease) × P(disease) / P(positive)
p_disease_given_positive = (p_positive_given_disease * p_disease / p_positive)

print(f"P(disease) = {p_disease}")
print(f"P(positive|disease) = {p_positive_given_disease}")
print(f"P(positive|no disease) = {p_positive_given_no_disease}")
print(f"P(disease|positive) = {p_disease_given_positive:.4f}")
# Output: P(disease|positive) = 0.1667 (16.67%)
# Despite 99% sensitivity, only 16.67% chance of having disease!
```

### Example 2: Gaussian Naive Bayes

```python
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import make_classification

# Generate data
np.random.seed(42)
X, y = make_classification(
    n_samples=300, n_features=4, n_informative=3,
    n_redundant=1, n_classes=2, random_state=42
)

print(f"Samples: {X.shape[0]}")
print(f"Features: {X.shape[1]}")
print(f"Classes: {np.unique(y)}")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train GaussianNB
model = GaussianNB()
model.fit(X_train, y_train)

print(f"\nClass priors: {model.class_prior_}")
print(f"Class counts: {model.class_count_}")

# Predictions
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
```

### Example 3: Probabilistic Predictions

```python
# Predict probabilities
y_prob = model.predict_proba(X_test)

print("First 5 predictions:")
for i in range(5):
    print(f"  Sample {i+1}: Predicted={y_pred[i]}, "
          f"P(class 0)={y_prob[i, 0]:.3f}, "
          f"P(class 1)={y_prob[i, 1]:.3f}")

# Probability interpretation
print("\nProbability interpretation:")
print(f"  Sum of probabilities: {y_prob[0].sum():.4f} (always 1)")
print(f"  Prediction: {'class 1' if y_prob[0, 1] > 0.5 else 'class 0'}")
```

### Example 4: Multinomial Naive Bayes

```python
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

# Text classification example
documents = [
    "buy cheap viagra now",
    "free money click here",
    "meeting tomorrow at 3pm",
    "project deadline friday",
    "win free lottery ticket",
    "lunch at noon today",
    "discount pharmacy online",
    "team standup meeting",
    "claim your prize now",
    "report due next week"
]

labels = [1, 1, 0, 0, 1, 0, 1, 0, 1, 0]  # 1=spam, 0=not spam

# Convert text to word counts
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(documents)

print(f"Vocabulary size: {len(vectorizer.vocabulary_)}")
print(f"Document-term matrix shape: {X.shape}")

# Train MultinomialNB
model = MultinomialNB()
model.fit(X, labels)

# Predict on new document
new_doc = ["free viagra discount"]
X_new = vectorizer.transform(new_doc)
prediction = model.predict(X_new)
probability = model.predict_proba(X_new)

print(f"\nNew document: {new_doc[0]}")
print(f"Prediction: {'spam' if prediction[0] == 1 else 'not spam'}")
print(f"Probability: {probability[0]}")
```

### Example 5: Bernoulli Naive Bayes

```python
from sklearn.naive_bayes import BernoulliNB

# Binary features (word presence/absence)
X_binary = (X.toarray() > 0).astype(int)

model_bernoulli = BernoulliNB()
model_bernoulli.fit(X_binary, labels)

# Predict
X_new_binary = vectorizer.transform(new_doc).toarray()
X_new_binary = (X_new_binary > 0).astype(int)
prediction = model_bernoulli.predict(X_new_binary)

print(f"BernoulliNB prediction: {'spam' if prediction[0] == 1 else 'not spam'}")
```

### Example 6: Feature Independence Check

```python
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.datasets import make_classification

# Create correlated features
np.random.seed(42)
n = 200
x1 = np.random.randn(n)
x2 = x1 * 0.8 + np.random.randn(n) * 0.2  # Correlated with x1
x3 = np.random.randn(n)  # Independent

X = np.column_stack([x1, x2, x3])
y = (x1 + x3 > 0).astype(int)

# Naive Bayes still works despite correlation
model = GaussianNB()
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f"Accuracy with correlated features: {scores.mean():.4f}")
print("Naive Bayes still works despite violated independence assumption!")
```

### Example 7: Naive Bayes vs Other Algorithms

```python
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
import numpy as np

np.random.seed(42)
X, y = make_classification(n_samples=500, n_features=10, 
                           n_informative=5, random_state=42)

models = {
    'Naive Bayes': GaussianNB(),
    'Logistic Regression': LogisticRegression(random_state=42),
    'SVM': SVC(random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
}

print("Model Comparison (5-fold CV accuracy):")
print("-" * 40)
for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
    print(f"{name:25s}: {scores.mean():.4f} +/- {scores.std():.4f}")
```

---

## Common Mistakes to Avoid

### Mistake 1: Using GaussianNB on Non-Normal Data

```python
import numpy as np

# GaussianNB assumes features are normally distributed
# Check distribution first

from scipy import stats

np.random.seed(42)
X = np.random.exponential(size=(100, 3))  # Exponential (not normal!)

# Test normality
for i in range(3):
    stat, p = stats.shapiro(X[:, i])
    print(f"Feature {i}: p-value = {p:.4f} {'Normal' if p > 0.05 else 'Not normal'}")

# SOLUTION: Transform data or use different algorithm
from sklearn.preprocessing import PowerTransformer
scaler = PowerTransformer(method='yeo-johnson')
X_transformed = scaler.fit_transform(X)
```

### Mistake 2: Not Handling Zero Probabilities

```python
# Problem: If a feature value never appears with a class,
# P(feature|class) = 0, which zeros out the entire probability

# SOLUTION: Use Laplace smoothing (alpha parameter)
from sklearn.naive_bayes import MultinomialNB

# Default alpha=1.0 (Laplace smoothing)
model = MultinomialNB(alpha=1.0)

# For no smoothing (can cause issues)
# model = MultinomialNB(alpha=0.0)  # DON'T DO THIS
```

### Mistake 3: Ignoring Feature Correlation

```python
# Naive Bayes assumes features are independent
# Highly correlated features can hurt performance

import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score

np.random.seed(42)
n = 200

# Highly correlated features
x1 = np.random.randn(n)
x2 = x1 * 0.95 + np.random.randn(n) * 0.05  # Very correlated
X = np.column_stack([x1, x2])
y = (x1 > 0).astype(int)

# Naive Bayes may struggle
model = GaussianNB()
scores = cross_val_score(model, X, y, cv=5)
print(f"Accuracy with correlated features: {scores.mean():.4f}")

# SOLUTION: Remove one of correlated features or use PCA
from sklearn.decomposition import PCA
pca = PCA(n_components=1)
X_pca = pca.fit_transform(X)
scores_pca = cross_val_score(model, X_pca, y, cv=5)
print(f"Accuracy with PCA: {scores_pca.mean():.4f}")
```

---

## Best Practices

### 1. Check Feature Distribution

```python
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def check_normality(X, feature_names):
    """Check if features are normally distributed."""
    for i, name in enumerate(feature_names):
        stat, p = stats.shapiro(X[:, i])
        status = "Normal" if p > 0.05 else "Not normal"
        print(f"{name}: p={p:.4f} ({status})")

# Use GaussianNB only for normal features
# Use MultinomialNB for count data
# Use BernoulliNB for binary data
```

### 2. Use Appropriate Variant

```python
# Text with word counts → MultinomialNB
from sklearn.naive_bayes import MultinomialNB
model = MultinomialNB()

# Text with word presence → BernoulliNB
from sklearn.naive_bayes import BernoulliNB
model = BernoulliNB()

# Continuous features → GaussianNB
from sklearn.naive_bayes import GaussianNB
model = GaussianNB()
```

### 3. Tune Alpha Parameter

```python
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score
import numpy as np

# Test different alpha values
alphas = [0.001, 0.01, 0.1, 0.5, 1.0, 2.0, 5.0]
for alpha in alphas:
    model = MultinomialNB(alpha=alpha)
    scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
    print(f"alpha={alpha:6.3f}: {scores.mean():.4f}")
```

### 4. Use for Baseline

```python
# Naive Bayes is fast and often a good baseline
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score

model = GaussianNB()
scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f"Baseline accuracy: {scores.mean():.4f}")
```

---

## Practice Exercises

### Exercise 1: Spam Classification

```python
"""
Build a spam classifier with Naive Bayes.
1. Create synthetic email data
2. Convert to word counts
3. Train MultinomialNB
4. Evaluate performance
"""
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import numpy as np

# Sample data
spam_emails = [
    "buy cheap viagra now",
    "free money click here",
    "win lottery prize",
    "discount pharmacy online",
    "claim your free gift",
    "urgent money transfer",
    "free trial offer",
    "make money fast"
]

ham_emails = [
    "meeting tomorrow at 3pm",
    "project deadline friday",
    "lunch at noon today",
    "team standup meeting",
    "report due next week",
    "check out this article",
    "thanks for your help",
    "see you at conference"
]

emails = spam_emails + ham_emails
labels = [1] * len(spam_emails) + [0] * len(ham_emails)

# Your code here
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(emails)

X_train, X_test, y_train, y_test = train_test_split(
    X, labels, test_size=0.25, random_state=42
)

model = MultinomialNB()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=['Ham', 'Spam']))

# Test on new email
new_email = ["free money now"]
X_new = vectorizer.transform(new_email)
print(f"New email: '{new_email[0]}'")
print(f"Prediction: {'Spam' if model.predict(X_new)[0] == 1 else 'Ham'}")
```

### Exercise 2: Compare Naive Bayes Variants

```python
"""
Compare different Naive Bayes variants on the same dataset.
1. Generate classification data
2. Test GaussianNB, MultinomialNB, BernoulliNB
3. Compare accuracy
"""
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
import numpy as np

np.random.seed(42)
X, y = make_classification(n_samples=200, n_features=10, 
                           n_informative=5, random_state=42)

# Your code here
X_positive = X - X.min(axis=0) + 1  # Make values positive for MultinomialNB
X_binary = (X > 0).astype(int)

models = {
    'GaussianNB': GaussianNB(),
    'MultinomialNB': MultinomialNB(),
    'BernoulliNB': BernoulliNB()
}

for name, model in models.items():
    if name == 'MultinomialNB':
        scores = cross_val_score(model, X_positive, y, cv=5, scoring='accuracy')
    elif name == 'BernoulliNB':
        scores = cross_val_score(model, X_binary, y, cv=5, scoring='accuracy')
    else:
        scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
    print(f"{name:20s}: {scores.mean():.4f} +/- {scores.std():.4f}")
```

### Exercise 3: Text Classification Pipeline

```python
"""
Build a complete text classification pipeline.
1. Load text data
2. Vectorize with TF-IDF
3. Train Naive Bayes
4. Evaluate with cross-validation
"""
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score

# Sample data
documents = [
    "machine learning algorithms",
    "deep neural networks",
    "python programming tutorial",
    "data science workshop",
    "artificial intelligence research",
    "software engineering practices",
    "web development framework",
    "database optimization techniques"
]

labels = [1, 1, 0, 1, 1, 0, 0, 0]  # 1=ML, 0=Software

# Your code here
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('nb', MultinomialNB())
])

scores = cross_val_score(pipeline, documents, labels, cv=3, scoring='accuracy')
print(f"Cross-validation accuracy: {scores.mean():.4f}")

# Fit and predict
pipeline.fit(documents, labels)
new_doc = ["neural network training"]
prediction = pipeline.predict(new_doc)
print(f"New document: '{new_doc[0]}'")
print(f"Prediction: {'ML' if prediction[0] == 1 else 'Software'}")
```

---

## Summary

| Concept | Description |
|---------|-------------|
| **Bayes' Theorem** | P(class\|features) = P(features\|class) × P(class) / P(features) |
| **Naive Assumption** | Features are conditionally independent |
| **GaussianNB** | For continuous features (normal distribution) |
| **MultinomialNB** | For discrete counts (text word counts) |
| **BernoulliNB** | For binary features (word presence) |
| **Laplace Smoothing** | Handles zero probabilities (alpha parameter) |

### Key Takeaways

1. Naive Bayes is **fast** and works well as a **baseline**
2. Despite the "naive" assumption, it often **performs well**
3. Choose the right variant for your data type
4. **Great for text classification** (spam, sentiment)
5. **No hyperparameters to tune** (except alpha)

---

## Next Steps

- **Lecture 20**: Random Forest — Ensemble methods
- **Lecture 21**: SVM — Support Vector Machines
- **Lecture 22**: Cross-Validation — Proper evaluation

---

## References

- [W3Schools - Naive Bayes](https://www.w3schools.com/python/ml_naive_bayes.asp)
- [Scikit-learn Documentation - Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html)
- [Wikipedia - Naive Bayes](https://en.wikipedia.org/wiki/Naive_Bayes_classifier)
