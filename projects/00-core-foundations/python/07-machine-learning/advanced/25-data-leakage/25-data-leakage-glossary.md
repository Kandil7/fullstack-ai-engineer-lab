# Data Leakage — Glossary

> Companion reference for the **Data Leakage** lecture.

## Concepts

- **Leakage**: Outside information (future, test, or target) reaching the training process; inflates offline metrics.
- **Target leakage**: A feature derived from or encoding the outcome (e.g., `days_to_failure == 0` when already failed).
- **Train/test contamination**: Preprocessing fitted on all data before splitting; test statistics leak into train transforms.
- **Temporal leakage**: Future rows entering the training window via random splits on time-ordered data.
- **Group leakage**: Same entity (patient, company, session) appearing in both train and test splits.
- **Duplicate leakage**: Identical rows present in both splits.

## Tools & Fixes

- **`train_test_split`**: Split **before** any fitting — scalers/encoders fit on train only.
- **`TimeSeriesSplit`**: Expanding-window splits where each train fold strictly precedes its test fold.
- **`GroupShuffleSplit` / `GroupKFold`**: Splitters that keep groups intact.
- **`StratifiedKFold`**: Preserves class proportions per fold (imbalance safety).
- **`drop_duplicates`**: Remove duplicate rows before splitting.
- **Audit checklist**: 6 questions that catch all five leakage classes.
- **Leak-proof architecture**: Pipelines (fit-on-train) + correct splitters + duplicates removed.

## Real-World Patterns

- **Churn/fraud**: check for post-event features (`days_since_...`, outcome-derived flags).
- **Time series**: never `shuffle=True`; use `TimeSeriesSplit`.
- **Medical/multi-row entities**: split by entity with `Group*` splitters.
