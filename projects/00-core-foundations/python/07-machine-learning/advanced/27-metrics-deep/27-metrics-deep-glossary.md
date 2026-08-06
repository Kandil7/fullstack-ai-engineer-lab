# Metrics Deep Dive — Glossary

> Companion reference for the **Metrics Deep Dive** lecture.

## Classification Metrics

- **Accuracy**: `(TP + TN) / total` — misleading on imbalanced data.
- **Precision**: `TP / (TP + FP)` — how many alerts are right.
- **Recall / TPR**: `TP / (TP + FN)` — how many positives were caught.
- **F1**: harmonic mean of precision and recall.
- **F-beta**: weighted F — `beta=2` favors recall, `beta=0.5` favors precision.
- **ROC-AUC**: TPR vs FPR area — can mislead under extreme imbalance.
- **PR-AUC (average precision)**: precision vs recall over the positive class — honest on imbalance.
- **Log loss**: scores probabilities; penalizes confident errors.
- **Confusion matrix**: TP/FP/TN/FN layout.
- **`roc_curve` / `precision_recall_curve`**: curves for threshold analysis.

## Threshold Decisions

- **Threshold**: cutoff on predicted probability deciding the label.
- **Cost-based selection**: pick the threshold minimizing `fp_rate*cost_fp + (1-recall)*cost_fn`.
- **Business metrics**: dollars saved, alert volume, review load — the numbers executives care about.

## Regression Metrics

- **R²**: share of variance explained (`r2_score`).
- **RMSE**: `sqrt(MSE)` — same units as target, penalizes large errors.
- **MAE**: mean absolute error — robust to outliers.

## Multi-Class

- **macro averaging**: mean per-class metric — treats classes equally.
- **micro averaging**: pooled over all instances — favors large classes.
- **weighted averaging**: macro weighted by class frequency.

## Real-World Patterns

- **Fraud/churn**: PR-AUC primary, F-beta, cost-threshold selection.
- **Probability consumers**: log loss to validate calibration.
- **Reporting**: R² for execs, RMSE/MAE for engineers.
