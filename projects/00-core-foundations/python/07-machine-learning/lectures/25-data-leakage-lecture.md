# Data Leakage — The 0.99 → 0.71 Story

> **Topic 25 — ML rigor series.** Target leakage, train/test contamination,
> temporal and group leakage, duplicate rows — and the worked example where a
> "0.99 accuracy" model collapses to its honest 0.71 once the leak is fixed.

Companion exercise: `25-data-leakage.py`

---

## 1. What Leakage Is

**Leakage** = information from outside the training set (the future, the test
set, or the target itself) reaches the model during training. The model
appears brilliant offline and fails in production, because the leaked signal
does not exist at prediction time.

## 2. The Five Leakage Classes

### a) Target leakage — features that encode the answer

A column like `days_since_last_order = 0` exactly when the customer churned is
a perfect predictor that **does not exist before the event**. Any feature
derived after the outcome is target leakage.

### b) Train/test contamination — preprocessing on all data

Fitting a scaler, imputer, or encoder on the **entire** dataset before
splitting bakes test statistics into the training transform.

### c) Temporal leakage — the future in the past

Random splitting on time-ordered data (financial, clickstream, sensors) puts
future rows in the training window. Splits must respect time.

### d) Group leakage — the same entity in both splits

Medical data has multiple rows per patient; a random split puts the same
patient in train **and** test, so the model memorizes patients instead of
learning the disease.

### e) Duplicate rows across splits

Duplicated rows (dedup bugs, join fan-out) can appear in both splits and are
trivially "predicted".

## 3. The Worked Example

Synthetic churn data with honest AUC ≈ 0.75:

| Intervention | Reported AUC |
|---|---|
| Clean data | 0.75 |
| Add target-leaky column | 0.99+ |
| Scaler fit on all data | 0.81 |
| Duplicate rows in both splits | 0.88 |

Fix the leaks and the number returns to ~0.71 — which is the number that
reproduces in production.

## 4. The Leakage Audit Checklist

1. Does any feature encode the target (post-event info)?
2. Is every scaler/encoder/imputer fit on **train only**?
3. Are there duplicated rows spanning train and test?
4. Is the split time-aware for temporal data?
5. Are groups (patient/company/session) kept together?
6. Is hyperparameter tuning inside cross-validation?

## Key Takeaways

1. Leakage inflates offline metrics and sinks production models.
2. Five classes: target, contamination, temporal, group, duplicates.
3. A suspiciously high score is a red flag — audit before celebrating.
4. Pipelines + proper splitters make leaks structurally impossible.
