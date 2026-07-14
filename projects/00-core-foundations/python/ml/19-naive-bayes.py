"""
W3Schools Python Tutorial - ML NN: Naive Bayes
================================================
Topics: GaussianNB, Bayes Theorem, Classification

Run: python 19-naive-bayes.py
Reference: https://www.w3schools.com/python/ml_naive_bayes.asp
"""

import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler

# ============================================================
# What is Naive Bayes?
# ============================================================

# Example 1: Naive Bayes concept
print("Example 1: Naive Bayes Concept")
print("Naive Bayes is a probabilistic classifier based on Bayes' theorem")
print("It assumes features are independent (the 'naive' assumption)")
print("Fast and works well with small datasets")

# ============================================================
# Bayes' Theorem
# ============================================================

# Example 2: Bayes' theorem
print("\nExample 2: Bayes' Theorem")
print("P(A|B) = P(B|A) x P(A) / P(B)")
print("\nIn classification:")
print("P(class|features) = P(features|class) x P(class) / P(features)")

# Example 3: Simple Bayes calculation
print("\nExample 3: Simple Bayes Calculation")
# Disease test example
# P(disease) = 0.01 (1% prevalence)
# P(positive|disease) = 0.99 (99% sensitivity)
# P(positive|no disease) = 0.05 (5% false positive rate)

p_disease = 0.01
p_positive_given_disease = 0.99
p_positive_given_no_disease = 0.05

# P(positive) = P(positive|disease) x P(disease) + P(positive|no disease) x P(no disease)
p_positive = (p_positive_given_disease * p_disease + 
              p_positive_given_no_disease * (1 - p_disease))

# P(disease|positive) = P(positive|disease) x P(disease) / P(positive)
p_disease_given_positive = (p_positive_given_disease * p_disease / p_positive)

print(f"P(disease) = {p_disease}")
print(f"P(positive|disease) = {p_positive_given_disease}")
print(f"P(positive|no disease) = {p_positive_given_no_disease}")
print(f"P(disease|positive) = {p_disease_given_positive:.4f}")

# ============================================================
# Gaussian Naive Bayes
# ============================================================

# Example 4: Generate classification data
print("\nExample 4: Classification Data")
np.random.seed(42)
X, y = make_classification(
    n_samples=300, n_features=4, n_informative=3,
    n_redundant=1, n_classes=2, random_state=42
)

print(f"Samples: {X.shape[0]}")
print(f"Features: {X.shape[1]}")
print(f"Classes: {np.unique(y)}")

# Example 5: Train/test split
print("\nExample 5: Train/Test Split")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Training set: {len(X_train)} samples")
print(f"Test set: {len(X_test)} samples")

# ============================================================
# Fitting the Model
# ============================================================

# Example 6: GaussianNB model
print("\nExample 6: GaussianNB Model")
model = GaussianNB()
model.fit(X_train, y_train)

print("Model trained successfully")
print(f"Class priors: {model.class_prior_}")
print(f"Class counts: {model.class_count_}")

# ============================================================
# Predictions
# ============================================================

# Example 7: Predictions
print("\nExample 7: Predictions")
# Predict classes
y_pred = model.predict(X_test)

# Predict probabilities
y_prob = model.predict_proba(X_test)

print("First 5 predictions:")
for i in range(5):
    print(f"  Sample {i+1}: Predicted={y_pred[i]}, "
          f"P(class 0)={y_prob[i, 0]:.3f}, "
          f"P(class 1)={y_prob[i, 1]:.3f}")

# ============================================================
# Model Evaluation
# ============================================================

# Example 8: Evaluation metrics
print("\nExample 8: Evaluation Metrics")
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
print(f"\nConfusion Matrix:\n{cm}")

# Classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# ============================================================
# Feature Independence
# ============================================================

# Example 9: Independence assumption
print("\nExample 9: Independence Assumption")
print("Naive Bayes assumes features are independent")
print("This is often violated in practice, but still works well!")
print("\nExample: 'spam' and 'free' are not independent")
print("  But Naive Bayes still classifies spam effectively")

# ============================================================
# Different Naive Bayes Variants
# ============================================================

# Example 10: Different variants
print("\nExample 10: Naive Bayes Variants")
print("GaussianNB: For continuous features (assumes normal distribution)")
print("MultinomialNB: For discrete counts (e.g., word frequencies)")
print("BernoulliNB: For binary features (0/1)")

# MultinomialNB example
from sklearn.naive_bayes import MultinomialNB

# Simulated text data (word counts)
np.random.seed(42)
X_text = np.random.randint(0, 10, (200, 5))
y_text = np.random.randint(0, 2, 200)

X_train_text, X_test_text, y_train_text, y_test_text = train_test_split(
    X_text, y_text, test_size=0.2, random_state=42
)

model_multi = MultinomialNB()
model_multi.fit(X_train_text, y_train_text)
acc_multi = accuracy_score(y_test_text, model_multi.predict(X_test_text))

print(f"\nMultinomialNB accuracy: {acc_multi:.4f}")

# ============================================================
# Practical Example: Text Classification
# ============================================================

# Example 11: Simple text classification
print("\nExample 11: Text Classification Concept")
print("For text classification with Naive Bayes:")
print("1. Convert text to feature vectors (TF-IDF, bag of words)")
print("2. Use MultinomialNB or BernoulliNB")
print("3. Works well for spam detection, sentiment analysis")

# ============================================================
# Naive Bayes vs Other Algorithms
# ============================================================

# Example 12: Comparison
print("\nExample 12: Naive Bayes vs Other Algorithms")
print("Advantages:")
print("  - Fast training and prediction")
print("  - Works well with small datasets")
print("  - Handles high-dimensional data")
print("  - No hyperparameters to tune")

print("\nDisadvantages:")
print("  - Independence assumption often violated")
print("  - Poor probability estimates")
print("  - Can be outperformed by more complex models")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("Summary:")
print("- Naive Bayes uses Bayes' theorem with independence assumption")
print("- GaussianNB for continuous features")
print("- MultinomialNB for discrete counts")
print("- Fast and works well with small data")
print("- Good baseline for text classification")
print("- Simple but effective algorithm")
print("="*60)