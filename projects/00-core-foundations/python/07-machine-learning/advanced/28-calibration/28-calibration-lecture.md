# Probability Calibration — Trustworthy Numbers

> **Topic 28 — ML rigor series.** Why raw model scores are often not
> probabilities, Platt scaling, isotonic regression, reliability diagrams,
> and why uncalibrated probabilities break downstream decisions.

Companion exercise: `28-calibration.py`

---

## 1. The Problem: Scores ≠ Probabilities

Many models — SVC, boosting, neural nets — output numbers that *look* like
probabilities but aren't. An SVC's raw score might say 0.80 while only 55% of
those predictions are true.

**Calibration** is the property: *among predictions of 0.80, exactly 80% are
true.*

## 2. Why It Matters Downstream

When probabilities feed automated decisions (auto-approve, queue, price,
route), miscalibration means systematically wrong choices:

- A system that auto-refunds when `P(return) < 0.2` is relying on those
  numbers being real probabilities.
- Uncalibrated 0.8s that are actually 0.55 → too many refunds, lost money.

## 3. Reliability Diagrams

Bin predictions by score and plot predicted vs actual positive rate:

```
predicted 0.20 -> actual 0.42   [BIAS]
predicted 0.60 -> actual 0.58   [OK ]
predicted 0.90 -> actual 0.74   [BIAS]
```

A model perfectly on the diagonal is perfectly calibrated.

## 4. Fixing Calibration

### Platt scaling (sigmoid)
Fit a logistic function to map raw scores → calibrated probabilities. Smooth,
parametric, good when the miscalibration is a monotone transform.

```python
CalibratedClassifierCV(model, method="sigmoid", cv=5)
```

### Isotonic regression
Non-parametric, monotone fit — more flexible, needs more data, best when the
distortion is irregular.

### The critical rule
Calibrate on a **held-out set**, never on the training data — or you'll fit
the calibration to the same noise the model memorized.

## 5. Measuring Calibration

- **Brier score**: mean squared error of probabilities — lower is better.
- **Log loss**: also rewards calibrated probabilities.
- **Reliability diagram**: visual, per-bin honesty check.

## 6. Real-World Use Case — Loan Auto-Approval

```python
# 1. Train the model
model.fit(X_train, y_train)
# 2. Calibrate on validation data (never train)
calibrated = CalibratedClassifierCV(model, method="isotonic", cv=5)
calibrated.fit(X_val, y_val)
# 3. Auto-approve only when P(default) < 0.05 — now the number is trustworthy
p = calibrated.predict_proba(X_loan)[:, 1]
```

## Key Takeaways

1. Raw scores from SVC/boosting/NN are usually not probabilities.
2. Reliability diagrams reveal systematic bias by bin.
3. Platt = smooth sigmoid fit; isotonic = flexible monotone fit.
4. Calibrate on held-out data only.
5. Uncalibrated probabilities break every downstream cost decision.
