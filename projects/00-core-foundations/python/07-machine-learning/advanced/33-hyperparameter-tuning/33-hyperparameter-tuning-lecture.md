# 07-machine-learning — 33: Hyperparameter Tuning — Search Inside CV

Companion exercise: `33-hyperparameter-tuning.py`

---

## Topic Overview

Hyperparameters are the settings chosen *before* training: the depth of a tree,
the strength of a regularizer, the learning rate of an optimizer. Unlike the
model weights, they are not learned from data — they are searched. This topic is
about doing that search **honestly**: grid search, random search, and Bayesian
search (Optuna), the cost of each, and the single rule that separates
professional tuning from amateur tuning — **the search must live inside
cross-validation, never outside it**.

Tuning is where most ML leakage sneaks in. The classic mistake: try a hundred
hyperparameter combinations on the full dataset, pick the best one, then report
a cross-validated score for it. That number is optimistic — the model was
selected *because* it did well on those exact folds, so the folds are no longer
unseen. Nested cross-validation exists precisely to produce an honest number.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Distinguish model parameters (learned) from hyperparameters (searched).
2. Explain why grid search explodes combinatorially with dimensions.
3. Explain why random search covers the space better per trial than grid.
4. Use Optuna to define a search space and run a Bayesian study.
5. Use pruning and TPE sampling to cut search cost.
6. Implement tuning inside cross-validation (nested CV) for honest scores.
7. Explain why you must never touch the test set while tuning.
8. Choose a search strategy by dimensionality and budget.

## Prerequisites

| Need | Where |
|---|---|
| Cross-validation | `22-cross-validation.py`, `26-validation-strategies.py` |
| Gradient boosting / random forests | `20-random-forest.py`, `30-gradient-boosting.py` |
| Scikit-learn pipelines | `24-sklearn-pipelines.py` |
| Metrics (AUC) | `12-confusion-matrix.py`, `27-metrics-deep.py` |

## 1. Parameters vs Hyperparameters

**Model parameters** — weights, biases, coefficients — are learned from data by
the optimizer. **Hyperparameters** — `n_estimators`, `max_depth`, `C`, `lr` —
are set before training and control *how* learning happens. You cannot gradient-
descend over a discrete value like `max_depth`; you have to search.

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=200, max_depth=10)  # 200, 10 = hyperparameters
rf.fit(Xtr, ytr)                                             # weights = parameters (learned)
```

Output:
```
# (fit silently; the estimator now holds learned parameters)
```

## 2. Grid Search — Exhaustive but Expensive

Grid search tries every combination in a Cartesian product. With 3 values for
each of 2 hyperparameters that is 9 fits; with 5 values each of 5 dimensions it
is 3125 fits — and each fit is itself cross-validated.

```python
from sklearn.model_selection import GridSearchCV

grid = GridSearchCV(RandomForestClassifier(random_state=0),
                    {"n_estimators": [50, 100, 200], "max_depth": [5, 10, None]},
                    cv=3, scoring="roc_auc")
grid.fit(Xtr, ytr)
print(grid.best_params_, round(grid.best_score_, 3))
```

Output:
```
{'max_depth': 10, 'n_estimators': 100} 0.912
```

**Cost:** O(combinations x folds x train cost). Fine for one or two dimensions;
hopeless past four.

## 3. Random Search — Same Budget, Better Coverage

Random search samples combinations from a distribution instead of enumerating
them. With a fixed budget of trials it explores far more *values per dimension*,
which matters because typically only a few hyperparameters actually drive
performance.

```python
from sklearn.model_selection import RandomizedSearchCV

param_dist = {"n_estimators": [50, 100, 200, 300],
              "max_depth": [3, 5, 10, None],
              "min_samples_leaf": [1, 2, 5, 10]}
rnd = RandomizedSearchCV(RandomForestClassifier(random_state=0), param_dist,
                         n_iter=15, cv=3, scoring="roc_auc", random_state=0)
rnd.fit(Xtr, ytr)
```

Output:
```
# 15 trials sampled from the 64-combination space, best params reported
```

**Cost:** O(budget x folds x train cost). The budget is under your control —
the key practical advantage.

## 4. Optuna — Bayesian Search That Adapts

Bayesian search (TPE in Optuna) models *which regions of the space are
promising* from past trials and proposes the next candidate there. It spends
trials where they pay off.

```python
import optuna

def objective(trial):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 50, 300),
        "max_depth": trial.suggest_int("max_depth", 3, 15),
        "max_features": trial.suggest_categorical("max_features", ["sqrt", "log2"]),
    }
    model = RandomForestClassifier(random_state=0, **params)
    return cross_val_score(model, Xtr, ytr, cv=3, scoring="roc_auc").mean()

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=20)
print(study.best_value, study.best_params)
```

Output:
```
0.917 {'n_estimators': 178, 'max_depth': 9, 'max_features': 'sqrt'}
```

**Cost:** O(trials x folds x train cost), but with fewer trials than grid/random
for the same result because the sampler learns.

## 5. Pruning — Stop Unpromising Trials Early

If a trial is clearly losing after a few epochs or folds, stop it and spend the
budget elsewhere. Optuna supports this via `Trial.report()` + `Trial.should_prune()`.
With fast sklearn models pruning matters less; with deep learning it can cut
10x of the wall-clock cost.

## 6. Search-Space Design — What to Actually Vary

| Hyperparameter | Typical range | Notes |
|---|---|---|
| `max_depth` | 3–15 (int) | Deeper = more capacity = more overfit |
| `min_samples_leaf` | 1–10 (int) | Larger = stronger regularization |
| `n_estimators` / `n_rounds` | 50–300 (int) | Diminishing returns; use early stopping |
| `learning_rate` | 1e-3–1 (log scale) | Log scale: `suggest_float(..., log=True)` |
| `C` (regularization) | 1e-3–1e3 (log) | Log scale |
| `batch_size`, `lr`, `momentum` | varies | Deep learning |

Log-scale suggestions are crucial — `C=0.001` and `C=0.01` differ as much as
`C=10` and `C=100`.

## 7. THE Rule: Tuning Inside CV, Not Outside

The honest protocol: the *outer* loop splits the data into folds; inside each
outer fold, an *inner* search picks the best hyperparameters **on the training
part of that fold only**, and the held-out outer fold evaluates the chosen
configuration.

```python
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

outer_aucs = []
for tr_o, va_o in KFold(5, shuffle=True, random_state=0).split(Xtr):
    inner = GridSearchCV(LogisticRegression(max_iter=1000),
                         {"C": [0.01, 0.1, 1, 10]}, cv=3, scoring="roc_auc")
    inner.fit(Xtr[tr_o], ytr[tr_o])                       # tune on training part only
    outer_aucs.append(roc_auc_score(ytr[va_o], inner.predict_proba(Xtr[va_o])[:, 1]))

print(f"nested mean AUC: {np.mean(outer_aucs):.3f}")      # the honest number
```

Output:
```
nested mean AUC: 0.871
```

The difference between nested and non-nested scores is the **optimism** of your
selection process. Report the nested number.

## 8. Common Mistakes to Avoid

### Mistake 1: Tuning on the full dataset, then reporting CV
```
# WRONG — folds have already seen the selected model
GridSearchCV(...).fit(X, y)          # search on ALL data
report(grid.best_score_)             # optimistic

# CORRECT — nested CV, or at minimum tune inside the training split only
```

### Mistake 2: Peeking at the test set while tuning
```
# WRONG
GridSearchCV(...).fit(X_train, y_train)
best = grid.best_estimator_
grid.score(X_test, y_test)           # used test to pick C, then "measured" it
```
The test set is measured exactly once, at the very end.

### Mistake 3: Uniform-scale searches over log-scale hyperparameters
```
# WRONG — C sampled evenly 0..100, tiny values effectively never tried
suggest_float("C", 0, 100)
# CORRECT
suggest_float("C", 1e-3, 1e3, log=True)
```

### Mistake 4: Grid search on >4 dimensions
```
# WRONG — 5^5 = 3125 combinations, almost all wasted
# CORRECT — random search or Optuna with a real budget
```

### Mistake 5: Searching then throwing away the search
```
# WRONG — tune, then retrain by hand with "rounded" values
# CORRECT — ship the exact best configuration, pinned
```

## 9. Best Practices

1. Set a budget before you start — trials and wall-clock.
2. Tune inside CV (nested); report the nested number.
3. Use log scales for magnitude-spanning hyperparameters.
4. Prefer Optuna/TPE over grid when the space has more than 3 dimensions.
5. Use pruning for any slow-to-train model.
6. Pin `random_state`/`seed` in the search so results are reproducible.
7. Track every trial (params + score) — a study log beats memory.
8. Vary only hyperparameters that matter; freeze the rest.
9. Never use the test set during search.
10. Record the final chosen config in the experiment tracker.

## 10. Complexity and Cost

| Operation | Cost | Cheaper alternative |
|---|---|---|
| Grid search, d dims, v values each | O(v^d x folds x train) | Random search O(budget x folds x train) |
| Random search, fixed budget | O(budget x folds x train) | Bayesian search — same budget, better points |
| Bayesian (TPE) search | O(trials x folds x train) | Add pruning to cut slow trials |
| Nested CV | outer folds x inner cost | Single split when data is scarce but report honestly |

The dominant cost is **training time per trial**. Pruning and smart samplers
attack exactly that term.

## 11. AI Engineering Relevance

**Where this shows up:** every model you ship — a reranker, a classifier, a
fine-tuned adapter — has hyperparameters that were searched before deployment.

| Concept here | Used for |
|---|---|
| Tuning inside CV | Producing an honest, non-optimistic evaluation in model cards and release reports |
| Bayesian search | Cutting GPU hours when tuning LLM adapters or embedding models |
| Log-scale search spaces | Sampling learning rates and regularization across magnitudes |
| Pruning | Stopping unpromising fine-tuning runs early, saving cost |
| Study logging | Reproducing and auditing which config produced a deployed model |

**Scale note:** at 100+ trials per model and multiple models per quarter, search
cost becomes a real line item. A well-designed search (Bayesian + pruning +
budgeted) is an order of magnitude cheaper than grid and produces the same or
better models.

## 12. Summary

| Concept | Description |
|---|---|
| Parameters | Learned by the optimizer from data |
| Hyperparameters | Set before training; must be searched |
| Grid search | Exhaustive; only for 1–2 dimensions |
| Random search | Better coverage per trial; budget-controlled |
| Bayesian search (Optuna) | Adapts sampling to promising regions |
| Nested CV | The honest evaluation of a tuned model |
| Pruning | Early stop of unpromising trials |

Tuning is where the gap between "a model that ran" and "a model that is
trusted" opens. The discipline is not the search algorithm — it is the honesty
of the evaluation. Tune inside CV, measure the test set once, and record
everything.

## Quick Reference

| Task | Idiom |
|---|---|
| Exhaustive small search | `GridSearchCV(estimator, param_grid, cv=k)` |
| Budgeted search | `RandomizedSearchCV(..., n_iter=N)` |
| Adaptive search | `optuna.create_study(...)` + `trial.suggest_*` |
| Log-scale parameter | `trial.suggest_float("lr", 1e-4, 1e-1, log=True)` |
| Early stop in Optuna | `trial.report(v, step); if trial.should_prune(): raise optuna.TrialPruned()` |
| Honest evaluation | Nested CV: outer fold evaluates, inner search tunes |

## Next Steps

Next: **[34 — Ensembling](34-ensembling-lecture.md)** — combining tuned models.

Continues in: **[08-mlops — 02 Experiment Tracking](../../08-mlops/lectures/02-experiment-tracking-lecture.md)** — recording search results for reproducibility.

Official docs: <https://optuna.readthedocs.io/> · <https://scikit-learn.org/stable/modules/grid_search.html>
