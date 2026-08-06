# 07-machine-learning — 35: Explainability — Why Did the Model Say That?

Companion exercise: `35-explainability.py`

---

## Topic Overview

Explainability answers the question every stakeholder eventually asks: **why**?
Regulators need it for lending and hiring decisions, product teams need it to
trust a feature, and engineers need it to debug silent model failures. This
topic draws the crucial distinction between **global** explanations (which
features matter overall?) and **local** explanations (why THIS prediction?),
and builds both from first principles — permutation importance, partial
dependence, and a LIME-style local surrogate — so you understand what each
method actually computes instead of treating SHAP as a black box.

The discipline here is honesty: explanations describe what the model does with
the data it was given. They do not prove causality, and they can be fooled by
collinearity and data artifacts. An explanation is a debugging and trust tool,
not a verdict.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Distinguish global from local explanations and when each is needed.
2. Implement permutation importance and interpret its mean and std.
3. Implement partial dependence and read a feature's effect curve.
4. Build a LIME-style local surrogate from first principles.
5. Explain why local surrogates are approximations of a black box.
6. Name the failure modes of importance measures (collinearity, spurious correlation).
7. Explain why explanations describe, not guarantee, causality.
8. Pair explanation output with data-quality review in practice.

## Prerequisites

| Need | Where |
|---|---|
| Random forests | `20-random-forest.py` |
| Linear regression | `05-linear-regression.py` |
| Metrics | `27-metrics-deep.py` |
| Feature selection | `32-feature-selection.py` |

## 1. Global Explanations — What Matters Overall

Permutation importance answers: "if I shuffle this feature's values, how much
does the score drop?" A feature whose shuffling collapses the score is
important; one whose shuffling changes nothing is irrelevant. It is
model-agnostic — works on any fitted estimator.

```python
from sklearn.inspection import permutation_importance

pi = permutation_importance(rf, Xte, yte, n_repeats=10, random_state=0)
order = np.argsort(pi.importances_mean)[::-1]
print(order[:6], pi.importances_mean[order[:6]])
```

Output:
```
[ 1  3  0  ... ]  [0.093 0.071 0.055 ...]
# mean drop in score when each feature is shuffled; std is the uncertainty
```

`n_repeats` gives a mean and a standard deviation — report both, because a
feature whose importance is all noise is not reliably important.

## 2. Partial Dependence — How a Feature Drives Predictions

Partial dependence fixes all other features at their observed values and varies
one feature, plotting the average prediction. It shows the *shape* of the
effect — increasing, U-shaped, threshold — which permutation importance cannot.

```python
pd_res = partial_dependence(rf, Xte, [0], kind="average")
print(pd_res["average"][0])        # average prediction as f0 varies
```

Output:
```
[0.35 0.42 0.51 0.63 0.74]
# as f0 rises, average predicted probability rises — a positive monotone effect
```

## 3. Local Explanations — Why THIS Prediction

Local methods explain a single row. The workhorse idea (LIME) is: perturb the
instance, ask the model for predictions on the perturbations, weight them by
distance from the original, and fit a simple linear surrogate. The surrogate's
coefficients approximate the model's local behavior.

```python
def lime_local(model, instance, background, n_samples=500, seed=0):
    r = np.random.RandomState(seed)
    noise = r.normal(0, np.std(background, axis=0), size=(n_samples, instance.shape[0]))
    X_pert = np.clip(instance + noise, background.min(0), background.max(0))
    dist = np.linalg.norm(X_pert - instance, axis=1)
    kernel_w = np.exp(-(dist ** 2) / (2 * (np.median(dist) + 1e-9) ** 2))
    y_local = model.predict_proba(X_pert)[:, 1]
    surrogate = Ridge(alpha=1.0).fit(X_pert, y_local, sample_weight=kernel_w)
    return surrogate.coef_, surrogate.intercept_
```

Output:
```
# weights: feature f3 = +0.42 (PUSHES toward 1), f0 = -0.31 (PUSHES toward 0)
```

The surrogate is a **local linear approximation** of a non-linear model. It is
accurate near the instance and meaningless far from it.

## 4. Global vs Local — They Answer Different Questions

- Global: "income is the 2nd most important feature overall."
- Local: "this loan was denied because income=40k and age=22."

A feature can be globally unimportant yet decisive for a particular prediction,
and vice versa. Production systems usually need both: global for monitoring and
documentation, local for individual decisions and appeals.

## 5. The Limits of Explanations

- **Collinearity**: two correlated features split the credit; permutation
  importance may flip between them across shuffles.
- **Spurious correlation**: the model uses a proxy (e.g., zip code for race);
  the explanation faithfully reports the proxy.
- **Approximation**: local surrogates are linear models around a point — they
  cannot represent interactions far from it.
- **No causality**: explanations describe behavior on training-like data; they
  do not prove that a feature *causes* the outcome.
- **Data quality**: garbage features produce confident garbage explanations.

## 6. Common Mistakes to Avoid

### Mistake 1: Treating importance as causality
```
# WRONG — "income drives the prediction, therefore increasing income changes outcomes"
# CORRECT — "the model uses income as its strongest signal on this data"
```

### Mistake 2: Reporting only the mean, ignoring the std
```
# WRONG — feature with mean 0.05, std 0.2 is not reliably important
# CORRECT — report mean +/- std; demand mean >> std
```

### Mistake 3: Over-interpreting a single local explanation
```
# WRONG — one row's LIME weights as the model's "reason"
# CORRECT — local explanations are per-row; aggregate many rows for a global view
```

### Mistake 4: Trusting importance with collinear features
```
# WRONG — split credit between f1 and f2 that are 0.98 correlated
# CORRECT — inspect VIF/dropping one, or use grouped importance
```

### Mistake 5: Explaining a model you haven't validated
```
# WRONG — explain a leaky pipeline's predictions
# CORRECT — validate first; explanations of a broken model are poison
```

## 7. Best Practices

1. State whether you need global, local, or both before choosing a method.
2. Report importance with uncertainty (mean +/- std across repeats).
3. Pair every explanation with a data-quality review.
4. Use partial dependence to understand effect *shape*, not just rank.
5. Validate the model before explaining it.
6. Aggregate local explanations across a cohort before drawing conclusions.
7. Document the method and its limits alongside the numbers.
8. Prefer simple, robust methods when the audience is non-technical.
9. Check collinearity before trusting feature-level importance.
10. Remember: explanations support decisions; they do not replace judgment.

## 8. Complexity and Cost

| Operation | Time | Space | Notes |
|---|---|---|---|
| Permutation importance (k features, r repeats) | O(k x r x predict) | O(1) | Cheap on small models; the dominant term is predict |
| Partial dependence (grid of m values) | O(m x predict) | O(1) | Per feature |
| LIME local surrogate (n samples) | O(n x predict + n x d) | O(n x d) | Per instance — expensive at scale |
| SHAP (exact) | exponential worst case | model-dependent | Use approximations in production |

Explaining every prediction at high volume is a real cost — many systems
explain on request or sample explanations for monitoring.

## 9. AI Engineering Relevance

**Where this shows up:** model cards and audit reports, credit and hiring
decisions under regulation, debugging retrieval failures in RAG pipelines, and
monitoring drift in feature importance.

| Concept here | Used for |
|---|---|
| Permutation importance | Monitoring which features drive a production model; drift alarms |
| Partial dependence | Understanding how a price/score responds to a feature before policy changes |
| Local explanations | Individual decision audits and customer appeals |
| Global vs local | Documentation (global) + per-request accountability (local) |
| Limits of explanations | Writing honest model cards and regulatory responses |

**Scale note:** at production volume you cannot SHAP every request. The
pattern is: sample requests for local explanations, track global importance
per release, and alert when importance distributions shift — that is
explainability as an operational system.

## 10. Summary

| Concept | Description |
|---|---|
| Global explanation | Which features matter overall (permutation importance, PDP) |
| Local explanation | Why this prediction (LIME-style surrogate) |
| Permutation importance | Score drop when a feature is shuffled |
| Partial dependence | Average prediction as a feature varies |
| Local surrogate | Linear model fit around one instance |
| Limits | No causality, collinearity traps, approximations |

## 11. Quick Reference

| Task | Idiom |
|---|---|
| Global importance | `permutation_importance(model, X, y, n_repeats=10)` |
| Effect shape | `partial_dependence(model, X, [feat_idx])` |
| Local explanation | Fit `Ridge` on perturbed instances weighted by distance |
| Importance uncertainty | `importances_mean` +/- `importances_std` |
| Collinearity check | `np.corrcoef(X[:, i], X[:, j])` or VIF |

## 12. Next Steps

Next: **[36 — PyTorch Tensors](36-pytorch-tensors-lecture.md)** — the GPU currency of deep learning.

Continues in: **[09-genai — 20 Evaluation Frameworks](../../09-genai/lectures/20-evaluation-frameworks-lecture.md)** — measuring quality, not just explaining it.

Official docs: <https://scikit-learn.org/stable/modules/inspection.html> · <https://shap.readthedocs.io/>
