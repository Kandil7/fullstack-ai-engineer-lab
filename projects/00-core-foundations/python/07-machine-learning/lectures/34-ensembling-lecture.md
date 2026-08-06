# 07-machine-learning — 34: Ensembling — Voting, Stacking, Blending

Companion exercise: `34-ensembling.py`

---

## Topic Overview

Ensembling combines multiple models into one stronger predictor. The idea is
simple and deep: if models make **different** mistakes, averaging their
predictions cancels those mistakes out. This is how Kaggle winners and
production teams squeeze the last few points out of a problem. But ensembling
has real costs — complexity, latency, explainability, and maintenance — and
knowing **when not to ensemble** is as much an engineering skill as knowing how.

This topic covers the three canonical techniques: voting (majority rule on
labels or averaged probabilities), stacking (a meta-model learns how to combine
base models from out-of-fold predictions), and blending (a hand-weighted
average, the production favorite for its simplicity). The unifying principle is
**diversity**: an ensemble of identical models is just one model with extra
steps.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why ensembles work in terms of error diversity.
2. Implement hard voting and soft voting with `VotingClassifier`.
3. Explain why soft voting generally beats hard voting.
4. Implement stacking with out-of-fold predictions to avoid leakage.
5. Implement manual blending with weights.
6. Measure diversity between models and predict ensemble gain.
7. Decide when an ensemble is not worth the complexity.
8. State the serving cost of an ensemble in latency and memory.

## Prerequisites

| Need | Where |
|---|---|
| Decision trees / random forests | `11-decision-tree.py`, `20-random-forest.py` |
| Gradient boosting | `30-gradient-boosting.py` |
| Logistic regression / SVM | `15-logistic-regression.py`, `21-svm.py` |
| Cross-validation | `22-cross-validation.py` |
| Model evaluation (AUC) | `27-metrics-deep.py` |

## 1. The Intuition: Averaging Errors

A model's prediction error has two components: bias (systematic wrongness) and
variance (noise sensitivity). Averaging independent models reduces variance.
More precisely: if N models each have error e with correlation rho, the average
has error proportional to e * (rho + (1-rho)/N). Lower correlation = more gain.
Perfectly correlated models (rho=1) gain nothing.

```python
import numpy as np
preds_a = np.array([0.9, 0.1, 0.8, 0.2])
preds_b = np.array([0.8, 0.2, 0.9, 0.1])
print("avg:", np.round((preds_a + preds_b) / 2, 2))
```

Output:
```
avg: [0.85 0.15 0.85 0.15]
```

## 2. Hard Voting — Majority Label

Each model predicts a class label; the ensemble takes the majority vote.
Simple, robust, and it needs only `predict()` — but it throws away the models'
confidence.

```python
from sklearn.ensemble import VotingClassifier

voting_hard = VotingClassifier(
    estimators=[("rf", RandomForestClassifier(random_state=0)),
                ("gb", GradientBoostingClassifier(random_state=0)),
                ("lr", LogisticRegression(max_iter=1000))],
    voting="hard").fit(Xtr, ytr)
```

Output:
```
# predict() returns the majority-voted label for each row
```

## 3. Soft Voting — Average Probabilities

Soft voting averages each model's class *probabilities*. A confident model
pulls the ensemble its way. This preserves information, which is why soft voting
almost always beats hard voting.

```python
voting_soft = VotingClassifier(
    estimators=[...],
    voting="soft", weights=[1, 1, 1]).fit(Xtr, ytr)
# roc_auc on probabilities
```

Output:
```
# AUC computed from averaged probabilities — typically >= any single model
```

`weights` let you trust a better model more: `weights=[2, 1, 1]` doubles the
RF's vote.

## 4. Stacking — The Meta-Model Learns to Combine

Stacking trains base models, then trains a **meta-model** on their predictions.
The critical detail: the base models' predictions that feed the meta-model must
be **out-of-fold** — generated on data the base model did not train on —
otherwise the meta-model learns on leaked, overfit predictions and degrades on
new data.

```python
from sklearn.ensemble import StackingClassifier

stack = StackingClassifier(
    estimators=[("rf", RandomForestClassifier(random_state=0)),
                ("gb", GradientBoostingClassifier(random_state=0)),
                ("svc", SVC(probability=True, random_state=0))],
    final_estimator=LogisticRegression(max_iter=1000),
    cv=5).fit(Xtr, ytr)
```

Output:
```
# final_estimator trains on 5-fold out-of-fold predictions of the base models
```

sklearn's `StackingClassifier` does the out-of-fold split internally (`cv=5`).
If you build stacking by hand, you must do the same or you leak.

## 5. Blending — Weighted Average by Hand

Blending is stacking's simpler cousin: take the models' probability vectors and
average them with fixed weights. No meta-model, no extra training — easy to
serve, easy to explain, easy to tune.

```python
blend = 0.5 * preds["GB"] + 0.3 * preds["RF"] + 0.2 * preds["LR"]
```

Output:
```
# AUC of the weighted average — often within a hair of stacking
```

Weights are usually chosen on a validation split. Because there is no second
training phase, blending has the lowest leakage risk of the three methods.

## 6. Diversity — The Engine of Ensemble Gains

Measure the correlation of the models' prediction vectors. Lower correlation
means more room to gain; near-perfect correlation means the ensemble is
decorative.

```python
corr = np.corrcoef(preds["RF"], preds["GB"])[0, 1]
print(f"corr(RF, GB) = {corr:.3f}")
```

Output:
```
corr(RF, GB) = 0.742   # moderate — some gain available
```

Techniques that increase diversity: different algorithms, different feature
subsets, different data subsamples (bagging), different seeds, different
preprocessing.

## 7. When NOT to Ensemble

- The single best model is within 0.001 AUC of the ensemble.
- You must explain every prediction — SHAP on 5 models is 5x the work.
- Serving latency or cost budget is tight: 5 models = 5x inference.
- The data pipeline changes often — every change means retraining every member.
- The marginal gain does not pay for the operational complexity.

An ensemble is a maintenance commitment, not a free upgrade.

## 8. Common Mistakes to Avoid

### Mistake 1: Ensembling identical models
```
# WRONG — same algorithm, same seed, same data: no diversity, no gain
# CORRECT — vary algorithm, features, or data subsamples
```

### Mistake 2: Stacking with in-sample predictions (leakage)
```
# WRONG — meta-model trains on the base models' TRAINING predictions
oof = model.predict(X_train)   # overfit predictions leak into the meta-model
# CORRECT — out-of-fold predictions only (cv=5 inside StackingClassifier)
```

### Mistake 3: Using hard voting when models output probabilities
```
# WRONG — hard voting discards confidence
# CORRECT — soft voting with weights
```

### Mistake 4: Tuning ensemble weights on the test set
```
# WRONG — blend weights chosen by test-set performance
# CORRECT — validation split, test measured once
```

### Mistake 5: Forgetting the serving cost
```
# WRONG — 7-model stack in a 50ms-latency budget
# CORRECT — measure p99 latency and memory; blend two models if the budget is tight
```

## 9. Best Practices

1. Start with a strong single model; ensemble only if the gap is worth it.
2. Prefer soft voting or blending over hard voting.
3. Use out-of-fold predictions for any learned combiner.
4. Measure diversity before building — if models agree, stop.
5. Tune weights on a validation split, never the test set.
6. Record each member's individual score alongside the ensemble's.
7. Consider the serving cost before committing to N models.
8. Use blending for production simplicity; stacking when the gain justifies it.
9. Retrain and re-evaluate the whole ensemble when the data changes.
10. Document why each member was included.

## 10. Complexity and Cost

| Operation | Time | Space | Notes |
|---|---|---|---|
| Single model predict | O(1) per row | model size | The baseline |
| Voting (k models) | O(k) per row | k x model size | No extra training |
| Blending | O(k) per row | k x model size | No extra training |
| Stacking | O(k + meta) per row | k x model size + meta | Meta-model trains on OOF preds |
| Training cost | k x single-model train | — | Can be parallelized per member |

The ensemble multiplies inference cost by k. At 100k predictions/hour that
matters; at 1M/minute it decides the architecture.

## 11. AI Engineering Relevance

**Where this shows up:** production ML services routinely blend a fast model
with a slower, more accurate one; rerankers are ensembled with retrieval
scorers; LLM routing can be seen as a model-selection ensemble.

| Concept here | Used for |
|---|---|
| Blending | Combining BM25 and embedding scores in hybrid retrieval |
| Diversity | Choosing different retrieval strategies so failures don't overlap |
| Out-of-fold predictions | Building honest training sets for reranker meta-models |
| Soft voting | Weighted combination of multiple classifiers behind an API |
| Serving cost | Deciding how many models fit in the latency budget of an endpoint |

**Scale note:** the same math that justifies ensembling also warns at scale —
each added model multiplies infrastructure. Hybrid retrieval systems are often
"ensembles" of two scorers for this reason: the second model buys more than the
fifth.

## 12. Summary

| Concept | Description |
|---|---|
| Ensemble | Combine models that make different mistakes |
| Hard voting | Majority label; simple, ignores confidence |
| Soft voting | Averaged probabilities; usually better |
| Stacking | Meta-model learns to combine from out-of-fold predictions |
| Blending | Hand-weighted average; production favorite |
| Diversity | The measurable source of ensemble gain |
| When not to | Gain < cost in latency, explainability, or maintenance |

Ensembles convert error diversity into accuracy. The professional skill is
judging whether the conversion is worth the price — and measuring it before you
commit.

## Quick Reference

| Task | Idiom |
|---|---|
| Majority label | `VotingClassifier(estimators, voting="hard")` |
| Averaged probabilities | `VotingClassifier(..., voting="soft", weights=[...])` |
| Learned combiner | `StackingClassifier(estimators, final_estimator, cv=5)` |
| Simple production combo | `blend = w1*p1 + w2*p2 + w3*p3` |
| Measure diversity | `np.corrcoef(p1, p2)[0, 1]` |
| Honest stacking | OOF predictions only — never training predictions |

## Next Steps

Next: **[35 — Explainability](35-explainability-lecture.md)** — understanding why the model made a prediction.

Continues in: **[09-genai — 11 Advanced Retrieval](../../09-genai/lectures/11-advanced-retrieval-lecture.md)** — hybrid scoring as an ensemble of retrievers.

Official docs: <https://scikit-learn.org/stable/modules/ensemble.html>
