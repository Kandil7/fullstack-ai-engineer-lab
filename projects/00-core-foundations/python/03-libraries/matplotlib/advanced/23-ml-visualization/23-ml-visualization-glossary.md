# Matplotlib Lecture 23: ML Visualization — Glossary

## Quick Reference

| Term | Definition | Example |
|------|-----------|---------|
| Learning curve | Train/val score vs training-set size | `ax.plot(sizes, train); ax.plot(sizes, valid)` |
| Confusion matrix | True vs predicted class heatmap | `ax.imshow(cm, cmap="viridis")` |
| ROC curve | TPR vs FPR across thresholds | `fpr, tpr, _ = roc_curve(y_true, y_score)` |
| PR curve | Precision vs recall across thresholds | cumulative `tp`/`fp` → precision, recall |
| AUC | Area under the curve (summary) | `auc(fpr, tpr)` |
| Operating point | Chosen threshold (the elbow) | pick where TPR/FPR trade-off is best |
| Residual | `y_true - y_pred` | `ax.scatter(y_pred, residual)` |
| Heteroscedastic | Variance grows with magnitude (funnel) | funnel-shaped residual cloud |
| Feature importance | Contribution of each feature | `ax.barh(names[order], importance[order])` |
| Embedding scatter | 2D projection of high-dim vectors | `ax.scatter(X, Y, c=labels, cmap="viridis")` |
| `roc_curve` | sklearn metric (or numpy fallback) | `from sklearn.metrics import roc_curve` |

## Detailed Definitions

**Learning curve** — Plot of train and validation scores against the
number of training rows. Converging curves → more data helps; a
widening train/validation gap → overfitting. The synthetic form models
`train = high - decay * exp(-size/τ) + noise` and `valid` slightly
lower.

**Confusion matrix** — An c×c heatmap of true vs predicted classes.
The diagonal is correct predictions; off-diagonal cells reveal
*systematic* confusion between specific classes — the information
accuracy hides.

**ROC curve** — Receiver Operating Characteristic: TPR (recall)
against FPR for every threshold, from (0,0) to (1,1). The area under it
(AUC) is the probability a random positive scores above a random
negative. Best for balanced problems.

**PR curve** — Precision vs recall across thresholds. Better than ROC
when the positive class is *rare*, where ROC can look great while
precision is useless. On balanced problems PR flattens — use ROC there.

**AUC** — Area under the curve, 0.5 = chance, 1.0 = perfect. ROC AUC
via `sklearn.metrics.auc`; PR AUC via `np.trapezoid(precision, recall)`.

**Residual** — `y_true - y_pred`, plotted against the prediction. A
cloud centered on zero → unbiased; a funnel → heteroscedasticity
(variance grows with magnitude); a tilted cloud → systematic bias.

**Feature importance** — Per-feature contribution scores, usually a
sorted horizontal bar chart. A required artifact for model cards and
fairness review.

**Embedding scatter** — Points from a 2D projection (t-SNE/UMAP) of
high-dimensional vectors, colored by label. Shows whether classes
separate in representation space.

## Key Concepts Summary

- Six canonical plots: learning curve, confusion matrix, ROC/PR,
  residuals, feature importance, embedding scatter.
- ROC for balanced problems; PR for rare positives; the elbow is the
  operating point.
- All metrics are pure functions of predictions — no model fitting
  needed for the plots.

## Practice Terms

1. Which plot tells you the model is overfitting?
2. When should you prefer PR over ROC?
3. What does a funnel-shaped residual cloud indicate?
4. What are the required endpoints of an ROC curve?
5. Which plot goes into a model card for governance?

*(Answers: 1. Learning curve with a widening train/val gap. 2. When
the positive class is rare. 3. Heteroscedasticity — variance grows
with magnitude. 4. (0, 0) and (1, 1). 5. Feature importance — and the
confusion matrix.)*
