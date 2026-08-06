# Metrics Deep Dive — Thresholds as Business Decisions

> **Topic 27 — ML rigor series.** Precision/recall tradeoffs, ROC-AUC vs PR-AUC
> (and when ROC misleads on imbalance), F-beta, log loss, threshold selection
> as a cost decision, regression metrics, multi-class averaging.

Companion exercise: `27-metrics-deep.py`

---

## 1. Accuracy Is Usually a Lie

A fraud dataset with 2% positives: a model that always predicts "no fraud" is
98% accurate and 100% useless. Accuracy hides what matters on imbalance —
**how many positives did we catch, and how many of our alerts were right?**

## 2. The Precision / Recall Tradeoff

- **Recall** = caught positives / all positives — "did we find them?"
- **Precision** = true alerts / all alerts — "when we say fraud, are we right?"

Raising the threshold raises precision but drops recall, and vice versa. The
right balance is a **business** question: a false positive costs money
(review time, refunds), a false negative costs money (lost fraud).

## 3. ROC-AUC vs PR-AUC — When ROC Misleads

- **ROC-AUC**: plots TPR vs FPR. FPR is over the (huge) negative class, so on
  extreme imbalance the curve can look great while the model is useless.
- **PR-AUC**: plots precision vs recall, both over the **positive** class.
  PR-AUC is brutally honest at 1% positives and is the primary metric for
  imbalanced problems.

## 4. F-beta & Log Loss

- **F1** = harmonic mean of precision and recall (equal weight).
- **F-beta** weights one side: `beta=2` favors recall, `beta=0.5` favors
  precision — match it to the cost structure.
- **Log loss** scores probabilities, not labels — heavily penalizes confident
  wrong predictions. The metric for calibrated probability models.

## 5. Threshold Selection as a Cost Decision

With costs per false positive and false negative, scan thresholds on the
validation set and pick the one minimizing expected cost:

```python
cost = fp_rate * cost_fp + (1 - recall) * cost_fn
best_threshold = thresholds[argmin(cost)]
```

This is how "99% accurate" models become "0.3% fraud caught with 5% alert
rate" models — and why threshold choice belongs to product, not just ML.

## 6. Regression Metrics

- **R²**: variance explained — good for reporting.
- **RMSE**: same units as y, penalizes big errors.
- **MAE**: robust to outliers.

## 7. Multi-Class Averaging

- **macro**: average per class, class-size independent — fair for rare classes.
- **micro**: global instance average — favors big classes.
- **weighted**: macro weighted by class frequency — a common default.

## Key Takeaways

1. Accuracy is meaningless on imbalance; use PR-AUC + F-beta.
2. Threshold = business decision (cost of FP vs FN).
3. ROC-AUC can look great while the model is useless at 1% positive.
4. Regression: R² to report, RMSE for units, MAE for robustness.
5. Multi-class: macro for fairness, micro for overall accuracy.
