# Glossary: Naive Bayes (Lecture 19)

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Naive Bayes | Probabilistic classifier using Bayes' theorem | `GaussianNB()` |
| Bayes' Theorem | P(A\|B) = P(B\|A) × P(A) / P(B) | Posterior probability |
| Prior Probability | Initial probability of class | P(spam) = 0.3 |
| Likelihood | P(features\|class) | P(word\|spam) |
| Posterior | P(class\|features) after seeing data | P(spam\|word) |
| Evidence | P(features) - constant for all classes | Normalizing factor |
| Independence Assumption | Features are conditionally independent | "Naive" part |
| GaussianNB | For continuous (normal) features | General classification |
| MultinomialNB | For discrete count features | Text word counts |
| BernoulliNB | For binary features | Word presence/absence |
| Laplace Smoothing | Adds alpha to avoid zero probabilities | alpha=1.0 |
| Class Prior | P(class) - proportion of each class | `model.class_prior_` |
| Log Probability | Log of probabilities (numerical stability) | `model.predict_proba()` |

---

## Detailed Term Definitions

### Naive Bayes

**Definition:** A family of probabilistic classifiers based on Bayes' theorem with the "naive" assumption that features are conditionally independent given the class.

**Example:**
```python
from sklearn.naive_bayes import GaussianNB
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Generate data
X, y = make_classification(n_samples=200, n_features=4, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Naive Bayes
model = GaussianNB()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")
```

**Related Terms:** Bayes' Theorem, Classification, Probabilistic Model

---

### Bayes' Theorem

**Definition:** A mathematical formula for updating probabilities based on new evidence.

**Formula:**
```
P(A|B) = P(B|A) × P(A) / P(B)
```

**Example:**
```python
# Medical test example
p_disease = 0.01  # Prior: 1% have disease
p_positive_given_disease = 0.99  # Sensitivity: 99%
p_positive_given_no_disease = 0.05  # False positive: 5%

# P(positive)
p_positive = (p_positive_given_disease * p_disease + 
              p_positive_given_no_disease * (1 - p_disease))

# P(disease|positive) - Posterior
p_disease_given_positive = (p_positive_given_disease * p_disease / p_positive)

print(f"Prior P(disease): {p_disease}")
print(f"Posterior P(disease|positive): {p_disease_given_positive:.4f}")
# Despite 99% test accuracy, only 16.67% chance of disease given positive test!
```

**Related Terms:** Prior, Likelihood, Posterior, Evidence

---

### Prior Probability

**Definition:** The initial probability of a class before observing any features. Calculated from class frequencies in training data.

**Example:**
```python
from sklearn.naive_bayes import GaussianNB
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=200, n_features=4, 
                           weights=[0.7, 0.3], random_state=42)

model = GaussianNB()
model.fit(X, y)

print(f"Class priors: {model.class_prior_}")
print(f"Class counts: {model.class_count_}")
print(f"Manual priors: {np.bincount(y) / len(y)}")
```

**Related Terms:** Likelihood, Posterior, Class Distribution

---

### Likelihood

**Definition:** The probability of observing the features given a specific class. P(features|class).

**Example:**
```python
from sklearn.naive_bayes import GaussianNB
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=200, n_features=2, random_state=42)

model = GaussianNB()
model.fit(X, y)

# For GaussianNB, likelihood is modeled as normal distribution
print("Class 0 statistics:")
print(f"  Mean: {model.theta_[0]}")
print(f"  Variance: {model.var_[0]}")

print("\nClass 1 statistics:")
print(f"  Mean: {model.theta_[1]}")
print(f"  Variance: {model.var_[1]}")

# Likelihood of a point given class 0
from scipy.stats import norm
point = X[0]
likelihood_0 = np.prod(norm.pdf(point, model.theta_[0], np.sqrt(model.var_[0])))
print(f"\nLikelihood of point given class 0: {likelihood_0:.6f}")
```

**Related Terms:** Prior, Posterior, Gaussian Distribution

---

### Posterior Probability

**Definition:** The probability of a class after observing the features. P(class|features). This is what Naive Bayes calculates.

**Example:**
```python
from sklearn.naive_bayes import GaussianNB
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=200, n_features=4, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = GaussianNB()
model.fit(X_train, y_train)

# Get posterior probabilities
y_prob = model.predict_proba(X_test)

print("First 3 samples - Posterior probabilities:")
for i in range(3):
    print(f"  Sample {i+1}: P(class 0)={y_prob[i, 0]:.3f}, P(class 1)={y_prob[i, 1]:.3f}")
    print(f"           Prediction: {model.predict(X_test[i:i+1])[0]}")
```

**Related Terms:** Prior, Likelihood, Evidence, Prediction

---

### Independence Assumption

**Definition:** The "naive" assumption that all features are conditionally independent given the class label.

**Mathematical Form:**
```
P(x₁, x₂, ..., xₙ|class) = P(x₁|class) × P(x₂|class) × ... × P(xₙ|class)
```

**Example:**
```python
# For spam classification:
# P("free", "money" | spam) = P("free" | spam) × P("money" | spam)
# This assumes "free" and "money" are independent given spam
# In reality, they often appear together!

# Despite this violation, Naive Bayes still works well for classification
# because it only needs to rank classes correctly, not estimate exact probabilities
```

**Related Terms:** Conditional Independence, Feature Independence

---

### GaussianNB

**Definition:** Naive Bayes variant that assumes features follow a normal (Gaussian) distribution within each class.

**Example:**
```python
from sklearn.naive_bayes import GaussianNB
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

model = GaussianNB()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"GaussianNB accuracy: {accuracy:.4f}")

# Check learned parameters
print(f"\nClass priors: {model.class_prior_}")
print(f"Class means:\n{model.theta_}")
print(f"Class variances:\n{model.var_}")
```

**When to Use:**
- Continuous features
- Features approximately normally distributed
- General classification tasks

**Related Terms:** MultinomialNB, BernoulliNB, Normal Distribution

---

### MultinomialNB

**Definition:** Naive Bayes variant for discrete count data, commonly used for text classification with word counts or TF-IDF.

**Example:**
```python
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Text data
documents = [
    "buy cheap viagra now",
    "free money click here",
    "meeting tomorrow at 3pm",
    "project deadline friday",
    "win free lottery",
    "team standup meeting"
]
labels = [1, 1, 0, 0, 1, 0]  # 1=spam, 0=ham

# Vectorize
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(documents)

# Train
model = MultinomialNB()
model.fit(X, labels)

# Predict
new_doc = ["free money now"]
X_new = vectorizer.transform(new_doc)
prediction = model.predict(X_new)
print(f"Prediction: {'spam' if prediction[0] == 1 else 'ham'}")
```

**When to Use:**
- Text classification (word counts, TF-IDF)
- Discrete count features
- Document classification

**Related Terms:** GaussianNB, BernoulliNB, Text Classification

---

### BernoulliNB

**Definition:** Naive Bayes variant for binary features (0/1), such as word presence/absence in text.

**Example:**
```python
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

# Text data
documents = [
    "buy cheap viagra",
    "free money now",
    "meeting tomorrow",
    "project deadline"
]
labels = [1, 1, 0, 0]

# Vectorize (binary)
vectorizer = CountVectorizer(binary=True)
X = vectorizer.fit_transform(documents).toarray()

# Train
model = BernoulliNB()
model.fit(X, labels)

# Predict
new_doc = ["free viagra"]
X_new = vectorizer.transform(new_doc).toarray()
prediction = model.predict(X_new)
print(f"Prediction: {'spam' if prediction[0] == 1 else 'ham'}")

# Compare with MultinomialNB
from sklearn.naive_bayes import MultinomialNB
model_multi = MultinomialNB()
model_multi.fit(X, labels)
print(f"MultinomialNB prediction: {'spam' if model_multi.predict(X_new)[0] == 1 else 'ham'}")
```

**When to Use:**
- Binary features (presence/absence)
- Short text documents
- When frequency doesn't matter

**Related Terms:** GaussianNB, MultinomialNB, Binary Features

---

### Laplace Smoothing

**Definition:** A technique to handle zero probabilities by adding a small value (alpha) to all feature counts.

**Formula:**
```
P(xᵢ|class) = (count(xᵢ, class) + α) / (count(class) + α × |V|)
```

Where:
- `α` = smoothing parameter (default 1.0)
- `|V|` = vocabulary size

**Example:**
```python
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

# Documents with rare words
documents = [
    "buy viagra now",
    "free money here",
    "meeting tomorrow",
    "project deadline"
]
labels = [1, 1, 0, 0]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(documents)

# Without smoothing (alpha=0) - can cause zero probabilities
# model_no_smooth = MultinomialNB(alpha=0.0)  # DON'T DO THIS

# With smoothing (alpha=1.0 - default)
model = MultinomialNB(alpha=1.0)
model.fit(X, labels)

# With more smoothing (alpha=10.0)
model_smooth = MultinomialNB(alpha=10.0)
model_smooth.fit(X, labels)

# New document with unseen word
new_doc = ["rareword xyz"]
X_new = vectorizer.transform(new_doc)
print(f"Prediction (alpha=1.0): {model.predict(X_new)[0]}")
print(f"Prediction (alpha=10.0): {model_smooth.predict(X_new)[0]}")
```

**Related Terms:** Smoothing, Zero Probability, Alpha Parameter

---

### Class Prior

**Definition:** The prior probability of each class, estimated from the proportion of training samples in each class.

**Example:**
```python
from sklearn.naive_bayes import GaussianNB
from sklearn.datasets import make_classification
import numpy as np

# Imbalanced classes
X, y = make_classification(n_samples=200, n_features=4,
                           weights=[0.7, 0.3], random_state=42)

print(f"Class distribution: {np.bincount(y)}")
print(f"Class proportions: {np.bincount(y) / len(y)}")

model = GaussianNB()
model.fit(X, y)

print(f"\nLearned priors: {model.class_prior_}")
```

**Related Terms:** Prior Probability, Class Distribution, Imbalanced Data

---

## Formulas Summary

| Formula | Expression |
|---------|-----------|
| Bayes' Theorem | P(A\|B) = P(B\|A) × P(A) / P(B) |
| Independence | P(x₁,x₂\|c) = P(x₁\|c) × P(x₂\|c) |
| Laplace Smoothing | (count + α) / (total + α × V) |
| Gaussian Likelihood | (1/√(2πσ²)) × exp(-(x-μ)²/(2σ²)) |

---

## Code Snippets Quick Reference

```python
# GaussianNB
from sklearn.naive_bayes import GaussianNB
model = GaussianNB()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)

# MultinomialNB
from sklearn.naive_bayes import MultinomialNB
model = MultinomialNB(alpha=1.0)
model.fit(X_train_counts, y_train)

# BernoulliNB
from sklearn.naive_bayes import BernoulliNB
model = BernoulliNB()
model.fit(X_binary, y_train)

# Text Vectorization
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(documents)

# Check learned parameters
print(model.class_prior_)  # Prior probabilities
print(model.theta_)  # Mean (GaussianNB)
print(model.var_)  # Variance (GaussianNB)
```

---

## Common Pitfalls

1. **Wrong variant** — GaussianNB for counts, MultinomialNB for continuous
2. **Not smoothing** — Zero probabilities crash the model
3. **Correlated features** — Violates independence assumption
4. **Non-normal features** — GaussianNB assumes normality
5. **Ignoring priors** — Class imbalance affects predictions

---

## Further Reading

- [Scikit-learn - Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html)
- [Wikipedia - Naive Bayes](https://en.wikipedia.org/wiki/Naive_Bayes_classifier)
- [Machine Learning Mastery - Naive Bayes](https://machinelearningmastery.com/naive-bayes-for-machine-learning/)
