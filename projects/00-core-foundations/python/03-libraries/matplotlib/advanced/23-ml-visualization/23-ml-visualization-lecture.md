# Matplotlib Lecture 23: ML Visualization

## 🎯 Topic Overview

Every model you ship needs a report: does it generalize (learning
curve), where does it err (confusion matrix, residuals), what is the
best operating point (ROC/PR), and what drove the prediction (feature
importance, embedding scatter). This lecture builds the six canonical
ML debug plots with synthetic data only — no real models, no fitting
cost — using `sklearn.metrics` when available and a numpy fallback
otherwise.

## 📚 Learning Objectives

1. Plot a learning curve (train vs validation score vs dataset size).
2. Render a confusion matrix heatmap and read the off-diagonal
   confusions.
3. Draw ROC and PR curves and pick the operating point; interpret AUC.
4. Plot residuals vs predictions and recognize bias/variance funnels.
5. Visualize feature importance and 2D embedding projections.

## 📋 Prerequisites

| Topic | Needed For |
|-------|-----------|
| Lectures 21-22 (OO API, styling) | All plots |
| `np.cumsum`, `np.trapezoid` | Section 3 (ROC/PR) |
| `sklearn.metrics` (optional) | `roc_curve`, `auc`, `confusion_matrix` |

---

## 1. Learning Curve: Does More Data Help?

Train/validation score vs training-set size. **Converging curves** mean
more data keeps helping; a **widening gap** between train and
validation means overfitting. The synthetic version models the two
shapes directly:

```python
sizes = np.arange(100, 2001, 100)
train = 0.94 - 0.06 * np.exp(-sizes / 400) + rng.normal(0, 0.004, sizes.size)
valid = 0.90 - 0.12 * np.exp(-sizes / 500) + rng.normal(0, 0.005, sizes.size)
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(sizes, train, label="train", color="tab:blue")
ax.plot(sizes, valid, label="validation", color="tab:orange")
```

Assertions that keep the plot honest: `train[-1] > train[0]`,
`valid[-1] > valid[0]`, `np.all(train >= valid)`.

## 2. Confusion Matrix: Where the Errors Land

A heatmap of true vs predicted class. The diagonal is the win;
off-diagonal cells name the *systematic* confusion (e.g., "versicolor
predicted as setosa"). Reading the matrix tells you which classes need
more data or a dedicated decision rule — accuracy alone hides this.

```python
y_true = rng.integers(0, 3, 300)
y_pred = np.clip(y_true + rng.choice([-1, 0, 0, 0, 1], 300), 0, 2)
cm = confusion_matrix(y_true, y_pred, labels=[0, 1, 2])
im = ax.imshow(cm, cmap="viridis")
ax.set_xticks(range(3), labels); ax.set_yticks(range(3), labels)
for i in range(3):
    for j in range(3):
        ax.text(j, i, str(cm[i, j]), ha="center", va="center")
```

Use a perceptually uniform map (`viridis`) — a confusion matrix is
continuous data. For >5 classes, log-scale the counts so rare errors
stay visible.

## 3. ROC and PR Curves: Choosing the Operating Point

- **ROC** (TPR vs FPR across thresholds) summarizes separation for any
  threshold. AUC = probability a random positive scores above a random
  negative.
- **PR** (precision vs recall) is the right view when the positive
  class is *rare* — ROC can look great while precision is useless.

```python
fpr, tpr, _ = roc_curve(y_true, y_score)
ax1.plot(fpr, tpr, color="tab:blue")
ax1.plot([0, 1], [0, 1], "k--", alpha=0.4)      # chance line
ax1.set_title(f"ROC (AUC={roc_auc:.3f})")
```

The curve must start at (0, 0) and end at (1, 1); the **elbow** is
where you pick the deployment threshold. PR AUC is the trapezoidal area
under precision-recall. On balanced problems PR collapses to a
horizontal line — use ROC there; on rare positives, use PR.

## 4. Residuals: Prediction Error vs Prediction

Residual = `y_true - y_pred`. Plot residual against prediction:

- A **horizontal cloud around zero** → unbiased model.
- A **funnel shape** → variance grows with magnitude (heteroscedastic).
- A **tilted cloud** → systematic bias (the model consistently
  under/over-predicts in a region).

```python
ax.scatter(y_pred, residual, s=12, alpha=0.6, color="tab:blue")
ax.axhline(0.0, color="tab:red", lw=1.2, ls="--")
```

The zero line makes bias visible at a glance. Testable claim:
`len(ax.collections) == 1` (the scatter).

## 5. Feature Importance and Embedding Scatter

**Feature importance** — horizontal bar chart, top features first —
goes into the model card and the fairness review:

```python
order = np.argsort(importance)
ax.barh(np.array(names)[order], importance[order], color="tab:green")
```

**Embedding scatter** — a 2D projection of high-dim vectors (what
t-SNE/UMAP produce), colored by label:

```python
ax.scatter(points[:, 0], points[:, 1], c=labels, cmap="viridis", s=14)
```

Both are the "what drove the prediction" plots: importance names the
features, embeddings show whether classes separate in representation
space (e.g., retrieval quality before/after fine-tuning).

---

## ⚠️ Common Mistakes to Avoid

1. **Reporting only accuracy** — `print(f"{acc:.3f}")` hides class
   confusion; ship matrix + ROC + residuals, one figure each.
2. **ROC for rare classes, PR for balanced ones** — PR collapses to a
   horizontal line when positives are common; ROC lies when positives
   are rare. Pick per problem.
3. **Not closing figures in a loop** — every `plt.subplots()` without
   `plt.close(fig)` leaks a canvas; close after `savefig`.
4. **Fitting real models for demo plots** — you do not need to train a
   classifier to demonstrate a confusion matrix; synthetic data makes
   the lecture deterministic and instant.
5. **`jet` on the confusion matrix** — continuous data, use
   `viridis`/PU maps.

## ✅ Best Practices

- Seed everything (`np.random.default_rng(42)`) so plots and assertions
  are reproducible.
- Verify the math claims in `_verify()`: ROC endpoints `(0,0)`/`(1,1)`,
  AUC in `[0,1]`, `train >= valid` on the learning curve.
- Use sklearn metrics when installed; ship a numpy fallback so CI
  without sklearn still runs.
- One message per figure: annotate the elbow, the funnel, the confusion.
- Assert artifacts: `png.exists() and png.stat().st_size > 1000`.

## 📊 Complexity and Cost

| Plot | Data | Cost |
|------|------|------|
| Learning curve | sizes × 2 series | O(n) |
| Confusion matrix | n predictions, c classes | O(n) build, O(c²) render |
| ROC/PR | n scores | O(n log n) sort |
| Residuals | n pairs | O(n) |
| Feature importance | f features | O(f log f) sort |
| Embedding scatter | n points | O(n) |

None of these plots fit a model — they are pure metrics over
predictions, so they are cheap even for large eval sets. The expensive
step is *generating* predictions, which happens once and is cached.

## 🤖 AI Engineering Relevance

- **The standard eval kit**: these six plots are the debugging kit for
  any training pipeline — a CI job can render them every run from the
  eval JSON.
- **Operating-point decisions**: the ROC/PR elbow is where the
  deployment threshold gets chosen; the plot *is* the decision record.
- **Model cards**: feature importance and the confusion matrix are
  required artifacts for model governance and fairness review.
- **Embedding quality**: the 2D scatter is the cheapest proxy for
  retrieval quality after fine-tuning an embedding model.

## 🏋️ Practice Exercises

1. Add a 7-class confusion matrix and log-scale the colorbar; verify
   the diagonal is still the brightest row.
2. Plot ROC and PR for a *rare-positive* synthetic set (5% positives)
   and confirm PR degrades visibly while ROC stays high.
3. Make the residual plot reveal a funnel: generate
   `y = 2x + x * noise` and assert the spread grows with `y_pred`.
4. Reorder feature importance bars ascending and assert the tallest
   bar is on top in the rendered axes.

## 📌 Summary

- Learning curve → generalization; confusion matrix → error structure.
- ROC for balanced, PR for rare positives; the elbow is the operating
  point; AUC summarizes the curve.
- Residuals expose bias and heteroscedasticity around the zero line.
- Feature importance + embedding scatter answer "what drove the
  prediction".
- All synthetic, all deterministic, all verifiable with `_verify()`.

## 📖 Quick Reference

| Plot | Key Call |
|------|----------|
| Learning curve | `ax.plot(sizes, train); ax.plot(sizes, valid)` |
| Confusion matrix | `ax.imshow(cm, cmap="viridis")` |
| ROC | `fpr, tpr, _ = roc_curve(y_true, y_score)` |
| PR | cumulative `tp`, `fp` → `precision = tp/(tp+fp)` |
| AUC | `auc(fpr, tpr)` / `np.trapezoid(precision, recall)` |
| Residuals | `ax.scatter(y_pred, residual); ax.axhline(0)` |
| Importance | `ax.barh(names[order], importance[order])` |
| Embedding | `ax.scatter(X, Y, c=labels, cmap="viridis")` |

## ➡️ Next Steps

- Lecture 24 (Saving and Export): turn these six plots into
  CI-verifiable artifacts — DPI, vector vs raster, tight bbox,
  transparency.
- Reference: https://scikit-learn.org/stable/visualizations.html
