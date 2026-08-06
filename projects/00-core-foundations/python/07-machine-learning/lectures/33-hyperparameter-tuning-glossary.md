# Hyperparameter Tuning — Glossary 33

Companion lecture: `33-hyperparameter-tuning-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Bayesian search | Search strategy | Samples from a model of promising regions built from past trials |
| Budget | Search strategy | The fixed number of trials or wall-clock time a search may spend |
| Early stopping | Search strategy | Halt a trial when its metric is clearly not going to win |
| Grid search | Search strategy | Exhaustively tries every combination in a Cartesian product |
| Hyperparameter | Model | A training setting chosen before training, not learned from data |
| Log scale | Search strategy | Sampling magnitudes (1e-4..1e-1) evenly, not raw values |
| Model parameter | Model | A value learned from data by the optimizer (weights, coefficients) |
| Nested cross-validation | Evaluation | Outer folds evaluate a model whose hyperparameters were tuned inside each fold |
| Optimism | Evaluation | The inflation of a score caused by selecting on the same data that scores |
| Optuna | Library | The Bayesian optimization framework used in this module |
| Pruning | Search strategy | Discarding an unpromising trial mid-run to free budget |
| Random search | Search strategy | Samples combinations from a distribution within a fixed budget |
| Search space | Search strategy | The set of hyperparameters and their ranges to explore |
| TPE sampler | Library | Optuna's default sampler: Tree-structured Parzen Estimator |
| Test set | Evaluation | The one held-out split measured exactly once at the very end |
| Trial | Search strategy | One training run of one hyperparameter configuration |

## Detailed Definitions

### Bayesian search
**Definition**: A search strategy that builds a surrogate model of the objective
from completed trials and proposes the next configuration where improvement is
most likely. In Optuna this is the TPE sampler.
**Example**:
```python
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=20)
```
Output:
```
# trial i: value 0.902 ... trial j: value 0.917 (adaptively sampled)
```
**Complexity**: O(trials x train cost); fewer trials than random for equal quality.
**Related**: Random search, TPE sampler

### Budget
**Definition**: The limit — number of trials or wall-clock — placed on a search
before it starts. Everything else (sampler, pruning) is a way to spend that
budget well.
**Example**:
```python
study.optimize(objective, n_trials=50)   # hard cap of 50 trials
```
Output:
```
# StudyStatistics(number_of_finished_trials=50, ...)
```
**Related**: Grid search, Random search

### Early stopping
**Definition**: Stopping training of a trial as soon as its metric can no longer
win, based on intermediate reports. In Optuna, `trial.report()` +
`trial.should_prune()`.
**Example**:
```python
for epoch in range(100):
    trial.report(loss, epoch)
    if trial.should_prune():
        raise optuna.TrialPruned()
```
**Related**: Pruning, Budget

### Grid search
**Definition**: Enumerates every combination of the provided hyperparameter
values — the Cartesian product. Exhaustive and simple, but cost grows
exponentially with the number of dimensions.
**Example**:
```python
GridSearchCV(RandomForestClassifier(), {"max_depth": [3, 5, 10]}, cv=3)
```
Output:
```
# 3 fits per fold x 3 folds = 9 training runs
```
**Complexity**: O(v^d x folds x train cost).
**Related**: Random search, Search space

### Hyperparameter
**Definition**: A setting fixed before training — tree depth, regularization
strength, learning rate. Chosen by search, not by gradient descent.
**Example**:
```python
rf = RandomForestClassifier(n_estimators=200, max_depth=10)  # hyperparameters
```
**Related**: Model parameter

### Log scale
**Definition**: Sampling a hyperparameter evenly across powers of ten (1e-4,
1e-3, ..., 1e-1) instead of linearly. Correct for learning rates and
regularization strengths whose effect spans magnitudes.
**Example**:
```python
trial.suggest_float("C", 1e-3, 1e3, log=True)
```
**Related**: Search space, Bayesian search

### Model parameter
**Definition**: A value learned during training — the weights and biases of a
network, the coefficients of a linear model.
**Example**:
```python
model.fit(Xtr, ytr)   # learns model parameters
model.coef_           # the learned values
```
**Related**: Hyperparameter

### Nested cross-validation
**Definition**: Two loops. The outer loop holds out folds for evaluation; inside
each outer fold, an inner search tunes hyperparameters on the training part
only. Produces an honest estimate of the tuned pipeline's performance.
**Example**:
```python
for tr_o, va_o in KFold(5).split(Xtr):
    inner = GridSearchCV(LogisticRegression(), {"C": [...]}, cv=3)
    inner.fit(Xtr[tr_o], ytr[tr_o])
    outer_scores.append(roc_auc_score(ytr[va_o], inner.predict_proba(Xtr[va_o])[:, 1]))
```
**Related**: Optimism, Test set

### Optimism
**Definition**: The gap between a model's measured score and its true
generalization score, caused by selecting the model using the same data that
measures it. Nested CV exposes this gap.
**Related**: Nested cross-validation

### Optuna
**Definition**: The Bayesian optimization framework used in this module — study
objects, `suggest_*` search spaces, TPE sampler, pruning.
**Example**:
```python
import optuna
study = optuna.create_study(direction="maximize")
```
**Related**: Bayesian search, TPE sampler

### Pruning
**Definition**: The act of terminating an unpromising trial early so its budget
is re-spent on better candidates. Most valuable when training is slow.
**Related**: Early stopping, Budget

### Random search
**Definition**: Samples hyperparameter combinations randomly from the search
space within a fixed budget. Per-trial information is higher than grid because
each dimension is explored at more distinct values.
**Example**:
```python
RandomizedSearchCV(estimator, param_dist, n_iter=15, cv=3)
```
**Related**: Grid search, Bayesian search

### Search space
**Definition**: The hyperparameters to tune together with their ranges, kinds
(int, float, categorical), and scales (log or uniform).
**Related**: Log scale, Trial

### TPE sampler
**Definition**: Optuna's default sampler, Tree-structured Parzen Estimator —
builds two density models over good and bad trials and proposes candidates
likely to be good.
**Example**:
```python
sampler = optuna.samplers.TPESampler(seed=0)
```
**Related**: Bayesian search, Optuna

### Test set
**Definition**: The held-out split that evaluates the final, fully-tuned model
exactly once. Any use of it during tuning makes its score untrustworthy.
**Related**: Nested cross-validation, Optimism

### Trial
**Definition**: A single execution of the objective function with one
hyperparameter configuration — one training run with one score.
**Related**: Budget, Study

## Key Concepts Summary

### Honest evaluation
- Tune inside cross-validation; the outer folds are the honest measurement.
- The test set is measured once, at the end, never during search.
- The gap between nested and non-nested scores is selection optimism.

### Search strategy selection
- 1–2 dimensions: grid search is fine.
- Many dimensions, bounded budget: random search.
- Any budget, slow training: Bayesian search + pruning.

### Space design
- Log scale for magnitudes (learning rates, C).
- Freeze hyperparameters that barely matter; search the ones that do.
- Always pin seeds for reproducibility.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. The value learned from data by the optimizer — ___
2. Sampling evenly across powers of ten — ___
3. Terminating an unpromising trial early — ___
4. The inflation of a score from selecting on the scoring data — ___
5. Outer-fold evaluation with inner-fold tuning — ___
6. Exhaustive Cartesian-product search — ___
7. Optuna's default Bayesian sampler — ___
8. The held-out split measured exactly once — ___

**Answers:** 1-model parameter, 2-log scale, 3-pruning, 4-optimism,
5-nested cross-validation, 6-grid search, 7-TPE sampler, 8-test set
