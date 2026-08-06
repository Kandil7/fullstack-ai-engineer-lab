# Ensembling — Glossary 34

Companion lecture: `34-ensembling-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Bagging | Technique | Train members on bootstrap samples to decorrelate errors |
| Bias | Theory | Systematic error a model makes regardless of the sample |
| Blending | Technique | Weighted average of models' probabilities, no meta-training |
| Diversity | Theory | The degree to which ensemble members make different mistakes |
| Ensemble | Technique | Multiple models combined into one stronger predictor |
| Hard voting | Technique | Majority label over members' predicted classes |
| Meta-model | Technique | The combiner trained on base models' out-of-fold predictions |
| Out-of-fold (OOF) | Correctness | Predictions on data a base model did not train on |
| Soft voting | Technique | Average of members' class probabilities, optionally weighted |
| Stacking | Technique | A meta-model learns how to combine base models |
| Variance | Theory | Error from sensitivity to the particular training sample |
| VotingClassifier | Library | sklearn's voting ensemble |
| StackingClassifier | Library | sklearn's stacking ensemble with internal CV |
| Weight | Technique | Per-member trust factor in soft voting or blending |
| Correlation | Theory | Statistical agreement of members' prediction vectors |

## Detailed Definitions

### Bagging
**Definition**: Training each ensemble member on a different bootstrap sample of
the data so their errors decorrelate. Random forests are bagged trees.
**Example**:
```python
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=100)   # 100 bagged trees
```
**Complexity**: Training x members; parallelizable.
**Related**: Diversity, Variance

### Bias
**Definition**: The component of error that persists across samples — the model
is systematically wrong. Averaging does not fix bias; only a better model does.
**Related**: Variance, Ensemble

### Blending
**Definition**: Combining models by a fixed weighted average of their
probabilities, with no meta-model. Simplest to serve and explain; the
production favorite.
**Example**:
```python
blend = 0.5 * gb_proba + 0.3 * rf_proba + 0.2 * lr_proba
```
**Complexity**: O(k) per prediction.
**Related**: Soft voting, Stacking

### Diversity
**Definition**: The degree to which members' errors are uncorrelated — the
measurable source of ensemble gain. Correlation near 1 means no gain available.
**Example**:
```python
corr = np.corrcoef(preds_rf, preds_gb)[0, 1]
```
**Related**: Correlation, Bagging

### Ensemble
**Definition**: A set of models combined so their strengths add and their
errors cancel. Effective only when members are diverse.
**Related**: Voting, Stacking, Blending

### Hard voting
**Definition**: Ensemble prediction by majority vote of the members' class
labels. Simple and robust, but ignores probability confidence.
**Example**:
```python
VotingClassifier(estimators=[...], voting="hard")
```
**Related**: Soft voting

### Meta-model
**Definition**: In stacking, the model trained on base models' out-of-fold
predictions to learn the best combination.
**Related**: Stacking, Out-of-fold

### Out-of-fold (OOF) predictions
**Definition**: Predictions produced by a base model on data excluded from its
own training. Required as the meta-model's features to avoid leakage.
**Related**: Stacking, Meta-model

### Soft voting
**Definition**: Ensemble prediction by averaging members' class probabilities,
optionally weighted by trust.
**Example**:
```python
VotingClassifier(estimators=[...], voting="soft", weights=[2, 1, 1])
```
**Related**: Hard voting, Blending

### Stacking
**Definition**: A two-level ensemble: base models predict, a meta-model learns
to combine their out-of-fold predictions.
**Example**:
```python
StackingClassifier(estimators=[...], final_estimator=LogisticRegression(), cv=5)
```
**Related**: Meta-model, OOF predictions

### Variance
**Definition**: The component of error caused by sensitivity to the particular
training sample. Averaging diverse models reduces variance.
**Related**: Bias, Bagging

### VotingClassifier
**Definition**: sklearn's ensemble that combines estimators by hard or soft
voting.
**Related**: Soft voting, Hard voting

### StackingClassifier
**Definition**: sklearn's implementation of stacking with internal
cross-validation that generates out-of-fold predictions.
**Related**: Stacking, Meta-model

### Weight
**Definition**: A per-member multiplier on its probability contribution; used
to trust stronger models more in soft voting and blending.
**Related**: Soft voting, Blending

### Correlation
**Definition**: Statistical agreement between members' prediction vectors;
the inverse measure of diversity.
**Related**: Diversity

## Key Concepts Summary

### The ensemble principle
- Ensemble value = error diversity. Identical models = identical mistakes.
- Averaging reduces variance, not bias.
- Measure correlation before building.

### The three techniques
- Hard voting: majority label, ignores confidence.
- Soft voting: averaged probabilities, usually best simple choice.
- Stacking: meta-model on OOF predictions — never in-sample predictions.
- Blending: fixed weighted average, simplest for production.

### Cost discipline
- Inference cost multiplies by member count.
- Ensemble only when the gain beats the latency/explainability/maintenance price.
- Retrain and re-evaluate all members when data changes.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Error component that persists across samples — ___
2. Majority vote over class labels — ___
3. Weighted average with no meta-model — ___
4. The measurable source of ensemble gain — ___
5. Predictions on data the base model never trained on — ___
6. The combiner trained on OOF predictions — ___
7. Averaged probabilities with optional weights — ___
8. Error from sensitivity to the training sample — ___

**Answers:** 1-bias, 2-hard voting, 3-blending, 4-diversity, 5-out-of-fold,
6-meta-model, 7-soft voting, 8-variance
