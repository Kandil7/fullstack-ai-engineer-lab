# Imbalanced Learning — Glossary

> Companion reference for the **Imbalanced Learning** lecture.

## Concepts

- **Imbalanced dataset**: One class far rarer than another (e.g., 2% positive).
- **Majority / minority class**: The common / rare outcome.
- **Accuracy paradox**: High accuracy with near-zero recall on imbalance.
- **`class_weight="balanced"`**: Scales class loss inversely to frequency — `n_samples / (n_classes * class_count)`.

## Resampling

- **Undersampling**: Drop majority-class samples (fast, loses data).
- **Oversampling**: Duplicate minority samples (risks overfitting).
- **SMOTE**: Synthetic Minority Oversampling — interpolate between minority samples and their k-nearest neighbors.
- **Resample-inside-CV rule**: Never resample before splitting, or synthetic samples leak across folds.

## Thresholds

- **Threshold moving**: Change the decision cutoff (`proba >= 0.15`) instead of the model.
- **Tradeoff**: Lower threshold → higher recall, lower precision; higher → the reverse.

## Evaluation

- **PR-AUC (average precision)**: Primary metric under imbalance — precision/recall over the positive class.
- **F-beta**: `beta=2` prioritizes recall; `beta=0.5` prioritizes precision.
- **StratifiedKFold**: Keeps the rare class present in every fold.
- **Confusion matrix**: TP/FP/TN/FN — the full picture.

## Real-World Patterns

- **Fraud**: balanced weights + PR-AUC + cost-based threshold.
- **Churn**: F2 with retention-revenue framing.
- **Medical screening**: maximize recall first, then manage FP cost.
