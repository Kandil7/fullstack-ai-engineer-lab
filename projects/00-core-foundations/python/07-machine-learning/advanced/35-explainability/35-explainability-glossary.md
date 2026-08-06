# Explainability — Glossary 35

Companion lecture: `35-explainability-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Collinearity | Limit | Correlated features that split explanatory credit |
| Global explanation | Method | What features matter overall across the dataset |
| Importance std | Method | Uncertainty of a feature's importance across shuffles |
| LIME | Method | Local surrogate that perturbs an instance and fits a linear model |
| Local explanation | Method | Why a specific prediction was made |
| Local surrogate | Method | A simple model approximating a complex one near one point |
| Partial dependence | Method | Average prediction as one feature varies, others held |
| Permutation importance | Method | Score drop when a feature's values are shuffled |
| SHAP | Method | Shapley-value-based attribution of predictions to features |
| Spurious correlation | Limit | A proxy relationship the model learned that is not causal |
| Uncertainty | Method | Variance across repeated importance measurements |
| Causality | Limit | A relationship explanations cannot prove |
| Validation | Practice | Confirming model correctness before explaining it |
| RBF kernel | Method | Distance weighting used by LIME-style surrogates |
| Proxy | Limit | A correlated stand-in feature the model exploits |

## Detailed Definitions

### Collinearity
**Definition**: Two or more features that are strongly correlated, so
attribution methods split credit between them arbitrarily. Check with
`np.corrcoef` or VIF before trusting feature-level importance.
**Example**:
```python
np.corrcoef(X[:, 0], X[:, 1])[0, 1]   # 0.98 -> treat with suspicion
```
**Related**: Permutation importance, Spurious correlation

### Global explanation
**Definition**: An explanation of overall model behavior — which features drive
predictions across the whole dataset. Permutation importance and partial
dependence are global methods.
**Related**: Local explanation

### Importance std
**Definition**: The standard deviation of a feature's importance across the
`n_repeats` shuffles. A mean importance much larger than its std is reliable.
**Example**:
```python
pi = permutation_importance(rf, X, y, n_repeats=10)
print(pi.importances_mean[i], pi.importances_std[i])
```
**Related**: Permutation importance, Uncertainty

### LIME
**Definition**: Local Interpretable Model-agnostic Explanations — perturbs an
instance, weights perturbations by distance, and fits a linear surrogate to
approximate the model locally.
**Related**: Local surrogate, Local explanation

### Local explanation
**Definition**: An explanation of a single prediction — "this loan was denied
because income=40k and age=22".
**Related**: Global explanation, LIME

### Local surrogate
**Definition**: A simple, interpretable model (e.g., linear) fit to a complex
model's behavior in the neighborhood of one instance. Accurate locally,
meaningless far away.
**Related**: LIME

### Partial dependence
**Definition**: The average prediction as one feature varies over a grid while
all other features keep their observed values. Reveals the shape of an effect.
**Example**:
```python
from sklearn.inspection import partial_dependence
pd_res = partial_dependence(rf, X, [0])
```
**Related**: Global explanation

### Permutation importance
**Definition**: The drop in model score when a feature's values are shuffled.
A large drop means the feature mattered; a near-zero drop means it did not.
Model-agnostic.
**Example**:
```python
permutation_importance(rf, Xte, yte, n_repeats=10)
```
**Complexity**: O(features x repeats x predict).
**Related**: Global explanation, Collinearity

### SHAP
**Definition**: Shapley-value-based attribution giving each feature a fair share
of each prediction. Powerful but expensive; use approximations at scale.
**Related**: Local explanation, LIME

### Spurious correlation
**Definition**: A relationship the model learned that is real in the data but
not causal — e.g., using zip code as a proxy for income. Explanations will
faithfully report it, which is exactly why explanations need data review.
**Related**: Proxy, Collinearity

### Uncertainty
**Definition**: The variability of an explanation across random repeats or
folds. Explanations without uncertainty can mislead.
**Related**: Importance std

### Causality
**Definition**: The claim that a feature causes an outcome. Explanations
describe model behavior on data; they cannot establish causation.
**Related**: Spurious correlation

### Validation
**Definition**: Confirming the model generalizes correctly (no leakage, sound
metrics) before interpreting it. Explaining a broken model is worse than not
explaining it.
**Related**: Causality

### RBF kernel
**Definition**: The exponential distance weighting used to emphasize
perturbations close to the explained instance in a LIME-style surrogate.
**Related**: LIME, Local surrogate

### Proxy
**Definition**: A feature that stands in for another (often protected)
attribute, letting the model exploit associations it should not.
**Related**: Spurious correlation

## Key Concepts Summary

### Two question types
- Global: which features matter overall? -> permutation importance, PDP.
- Local: why this prediction? -> LIME-style surrogates.
- Both are needed; neither substitutes for the other.

### The limits
- Explanations describe, they do not prove causality.
- Collinearity splits credit; spurious correlations get faithfully reported.
- Local surrogates are approximations valid only near the instance.

### The discipline
- Report uncertainty (mean +/- std).
- Validate the model before explaining it.
- Pair explanations with data-quality review.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Score drop when a feature's values are shuffled — ___
2. Average prediction as one feature varies — ___
3. A simple model approximating a complex one near one point — ___
4. Correlated features splitting explanatory credit — ___
5. The claim explanations cannot prove — ___
6. Variance across repeated importance measurements — ___
7. Why a specific prediction was made — ___
8. A correlated stand-in feature the model exploits — ___

**Answers:** 1-permutation importance, 2-partial dependence, 3-local surrogate,
4-collinearity, 5-causality, 6-uncertainty, 7-local explanation, 8-proxy
