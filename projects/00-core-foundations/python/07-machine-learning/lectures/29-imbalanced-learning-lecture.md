# Imbalanced Learning — When 99% Accuracy Is Failure

> **Topic 29 — ML rigor series.** Class weights, resampling (undersample,
> oversample, SMOTE), threshold moving, and honest evaluation when the
> positive class is 1%.

Companion exercise: `29-imbalanced-learning.py`

---

## 1. The Imbalance Reality

Fraud, churn, disease screening, anomaly detection — the highest-value
problems are imbalanced. A model that always predicts the majority class is
99% accurate and 100% useless. The question is never "accuracy" but "how many
positives did we catch, at what cost?"

## 2. Strategy 1 — Class Weights

The one-line fix: `class_weight="balanced"` scales each class's loss inversely
to its frequency, so the rare class matters as much as the common one.

```python
LogisticRegression(class_weight="balanced")
```

Trees support `class_weight` too; sklearn's balanced formula is
`n_samples / (n_classes * class_count)`.

## 3. Strategy 2 — Resampling

- **Undersample** the majority class (fast, discards data).
- **Oversample** the minority class by duplication (risk: overfitting).
- **SMOTE**: synthesize new minority samples by interpolating between a
  sample and its k nearest neighbors — the standard, most robust approach.

```python
# SMOTE core idea (implemented from scratch in the exercise):
new = X_minor[i] + lambda * (X_minor[neighbor] - X_minor[i])
```

Resample **inside cross-validation** — resampling before CV leaks synthetic
samples across folds.

## 4. Strategy 3 — Threshold Moving

Keep the model; change the decision boundary. Default `0.5` is arbitrary on
imbalance — lower it to catch more positives (recall up, precision down) or
raise it to reduce alert noise:

```python
pred = proba >= 0.2   # business-tuned threshold
```

## 5. Honest Evaluation Under Imbalance

- **PR-AUC** is the primary metric (positive-class only).
- **F-beta** (e.g. F2) matches recall-first business goals.
- **Stratified CV** keeps the rare class in every fold.
- Report the **confusion matrix** — not just one number.

## 6. Real-World Use Case — Fraud Detection

```python
model = RandomForestClassifier(class_weight="balanced")
model.fit(X_train, y_train)
proba = model.predict_proba(X_test)[:, 1]
# Business review cost caps alerts: pick threshold where FP cost is acceptable
pred = proba >= 0.15
print(f"caught {recall_score(y, pred):.0%} of fraud with {pred.mean():.0%} alert rate")
```

## Key Takeaways

1. Accuracy is meaningless when positives are rare.
2. `class_weight="balanced"` is the 1-line first fix.
3. SMOTE synthesizes minority samples — resample inside CV.
4. Threshold moving trades precision ↔ recall at the business level.
5. PR-AUC + F-beta + stratified CV = the honest report card.
