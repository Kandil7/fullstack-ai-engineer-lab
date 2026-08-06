# Validation Strategies — Glossary

> Companion reference for the **Validation Strategies** lecture.

## Splitters

- **`KFold(n_splits, shuffle=True)`**: Baseline K-fold CV for IID data.
- **`StratifiedKFold`**: K-fold preserving class proportions per fold — for imbalanced targets.
- **`GroupKFold`**: K-fold where groups never straddle folds — for grouped data.
- **`GroupShuffleSplit`**: Shuffle split respecting groups.
- **`TimeSeriesSplit(n_splits)`**: Expanding-window splits; each train fold ends before its test fold begins.
- **`train_test_split`**: One-shot random holdout; `stratify=` preserves class balance.

## Discipline

- **Nested CV**: Inner loop tunes hyperparameters; outer loop scores the tuned pipeline on unseen folds — the honest tuning estimate.
- **Train/validation/test**: 60/20/20 discipline — val for tuning, test scored once at the end.
- **`cross_val_score`**: Convenience wrapper computing the metric across folds.
- **Optimistic bias**: Any CV score that used the same data to choose params or transforms is inflated.

## When CV Lies

- Random split on temporal data (temporal leakage).
- Unstratified folds on rare classes (fold missing the minority).
- Groups split across folds (group leakage).
- Tuning outside CV (selection baked into the score).
- Preprocessing fit on all data before CV (contamination).

## Real-World Patterns

- **Fraud**: `StratifiedKFold` + PR-AUC.
- **Time series**: `TimeSeriesSplit`, never shuffle.
- **Medical/grouped**: `GroupKFold` by patient.
- **Tuning**: nested CV or an explicit inner GridSearch per outer fold.
