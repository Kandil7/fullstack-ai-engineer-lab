# Gradient Boosting — The Tabular Champion

> **Topic 30 — Modeling depth.** Boosting intuition, sklearn's
> `GradientBoosting` vs `HistGradientBoosting`, early stopping, key
> hyperparameters, native categorical handling, and why GBDTs beat neural
> nets on tabular data.

Companion exercise: `30-gradient-boosting.py`

---

## 1. Boosting Intuition — Learn From Your Mistakes

Boosting builds a **sequence** of shallow trees, each trained to correct the
errors of the ensemble so far:

1. Train tree 1 on the data.
2. Tree 2 predicts the *residuals* (errors) of tree 1.
3. Tree 3 predicts the residuals of trees 1+2. And so on.

The final prediction is the weighted sum of all trees. This is *gradient*
boosting because each tree fits the gradient of the loss.

## 2. sklearn's Two Flavors

```python
# Classic — small/medium data
GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3)

# Fast — large data (LightGBM-style histogram binning, native NaN + categoricals)
HistGradientBoostingClassifier(max_iter=200, learning_rate=0.1)
```

`HistGradientBoosting*` bins continuous features into histograms → drastically
faster training and built-in handling of missing values and categoricals.

## 3. The Key Hyperparameters

| Param | Effect |
|---|---|
| `n_estimators` / `max_iter` | Number of trees (capacity) |
| `learning_rate` | Step size per tree; lower → more trees needed |
| `max_depth` | Interaction order (usually 3–6) |
| `subsample` | Row sampling → variance reduction |
| `min_samples_leaf` | Regularization → smoother predictions |
| `n_iter_no_change` | Early-stopping patience |

**The golden rule**: `learning_rate` and tree count trade off. Lower the LR,
raise the tree budget, and let **early stopping** find the sweet spot.

## 4. Early Stopping

```python
HistGradientBoostingClassifier(max_iter=1000, early_stopping=True,
                               validation_fraction=0.2, n_iter_no_change=10)
```

Watch validation loss during training; stop when it stops improving. This
replaces blind `n_estimators` guessing.

## 5. Why GBDTs Beat Neural Nets on Tabular

- **Trees handle mixed, messy, scaled-irrelevant features** natively.
- **No feature scaling** needed.
- **Native missing value handling** (histogram flavor).
- **Native categoricals** (LightGBM / sklearn HistGB `categorical_features`).
- Small-to-medium tabular datasets don't have the volume NNs need.
- Neural nets win on **text, images, audio** — high-dimensional, structured
  data. Use the right tool.

## 6. Real-World Use Case — Churn Prediction

```python
model = HistGradientBoostingClassifier(
    max_iter=500, learning_rate=0.05, max_depth=5,
    early_stopping=True, n_iter_no_change=20, random_state=0,
)
model.fit(X_train, y_train)   # X may contain NaN and categoricals directly
```

## Key Takeaways

1. Boosting = additive sequence of shallow trees fixing prior errors.
2. `learning_rate` ↔ `n_estimators` tradeoff; use early stopping.
3. HistGradientBoosting scales and handles categoricals/NaN natively.
4. GBDTs are the default for tabular; NNs win on text/image/sound.
