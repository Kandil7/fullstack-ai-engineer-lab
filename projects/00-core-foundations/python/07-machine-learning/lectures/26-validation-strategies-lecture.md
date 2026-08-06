# Validation Strategies — When CV Lies

> **Topic 26 — ML rigor series.** K-fold, stratified, group, and time-series
> splitting; nested CV for tuning; train/val/test discipline — and when
> cross-validation gives a lying estimate.

Companion exercise: `26-validation-strategies.py`

---

## 1. Why the Splitter Matters

The number your model reports is a **claim about production**. The splitter
decides whether that claim is true. Use the wrong splitter and you get
confident, wrong numbers.

## 2. The Splitters

### KFold
Shuffles and divides into K folds. Fine for IID data with balanced classes.

### StratifiedKFold
Preserves class proportions in every fold — essential when the positive class
is rare. Without it, a fold can randomly lack the minority class entirely.

### GroupKFold
Keeps groups (patients, companies, sessions) entirely inside one fold —
prevents group leakage.

### TimeSeriesSplit
Expanding-window splits for temporal data: each training fold is a strict
prefix of its test fold's past. Never `shuffle` time.

## 3. Nested CV — Tuning Inside CV

Tuning outside CV (pick best params on the whole train set, then report a CV
score) is itself a form of leakage: the data used to choose hyperparameters
was also used to score them.

**Nested CV**: an inner loop picks hyperparameters per outer fold; the outer
loop scores the resulting pipeline on data the inner loop never saw. The
result is the number to trust.

## 4. Train / Validation / Test Discipline

The three-way split:

- **Train** (60%): fit models.
- **Validation** (20%): tune hyperparameters, pick the model.
- **Test** (20%): score exactly once, at the very end.

Touching the test set repeatedly is testing on the test set — the fastest way
to make it lie.

## 5. When CV Lies

- Random `KFold` on **time-ordered** data (future leaks into train).
- No stratification on rare classes.
- Groups split across folds.
- Tuning outside CV.
- Leaky preprocessing fit on all data before CV.

## Key Takeaways

1. Splitter choice = the honesty of your reported number.
2. Stratify for imbalance, group for entities, time for sequences.
3. Tune inside CV (nested) or accept optimistic scores.
4. Test set is scored once, at the end, or it stops being a test set.
