# Matplotlib 23 — ML Visualization Quiz

20 questions · 6 Easy · 9 Medium · 5 Hard · ≥8 code-output.
Answers with full explanations and distractor analysis at the end.

Shared data (seeded, used below):
```python
import numpy as np
rng = np.random.default_rng(42)
n = 1000
y_true = np.concatenate([np.zeros(700), np.ones(300)]).astype(int)
y_score = np.concatenate([rng.normal(0.0, 1.0, 700), rng.normal(2.2, 1.0, 300)])
```

---

## Easy

**E1.** A learning curve plots:

- A) train/validation score vs training-set size
- B) loss vs accuracy
- C) accuracy vs precision
- D) epoch vs learning rate

**E2.** A confusion matrix's diagonal represents:

- A) correct predictions per class
- B) errors per class
- C) precision per class
- D) the number of classes

**E3 (code-output).** What prints?
```python
from sklearn.metrics import roc_curve
fpr, tpr, _ = roc_curve(y_true, y_score)
print(fpr[0] == 0.0, tpr[0] == 0.0)
print(abs(fpr[-1] - 1.0) < 1e-12, abs(tpr[-1] - 1.0) < 1e-12)
```

- A) `True True` `True True`
- B) `True True` `False False`
- C) `False False` `True True`
- D) `True False` `True True`

**E4 (code-output).** What prints?
```python
import numpy as np
y_true = np.array([5.0, 7.0])
y_pred = np.array([4.5, 8.0])
print((y_true - y_pred).tolist())
```

- A) `[0.5, -1.0]`
- B) `[-0.5, 1.0]`
- C) `[0.5, 1.0]`
- D) `[-0.5, -1.0]`

**E5.** For a *rare* positive class, prefer:

- A) the PR curve over the ROC curve
- B) the ROC curve over the PR curve
- C) neither — use the learning curve
- D) a confusion matrix only

**E6 (code-output).** What prints?
```python
from sklearn.metrics import auc, roc_curve
fpr, tpr, _ = roc_curve(y_true, y_score)
print(round(float(auc(fpr, tpr)), 4))
```

- A) `0.9416`
- B) `0.5`
- C) `1.0`
- D) `0.8926`

---

## Medium

**M1.** A funnel-shaped residual cloud (spread grows with prediction
magnitude) indicates:

- A) heteroscedasticity — variance grows with magnitude
- B) a perfectly calibrated model
- C) class imbalance
- D) a bug in `ax.axhline`

**M2.** The horizontal dashed line at 0 in a residual plot marks:

- A) the zero-error line — bias shows as systematic deviation
- B) the mean prediction
- C) the decision threshold
- D) the training accuracy

**M3 (code-output).** What prints?
```python
from sklearn.metrics import confusion_matrix
y_pred = np.clip(y_true + rng.choice([-1, 0, 0, 0, 1], 1000), 0, 2)
cm = confusion_matrix(y_true, y_pred, labels=[0, 1, 2])
print(cm.shape)
print(int(cm[0, 0]))
```

- A) `(3, 3)` and a positive integer (correct negatives for class 0)
- B) `(2, 2)` `1`
- C) `(3, 3)` `0`
- D) `(1000, 1000)` `300`

**M4.** Feature importance is best plotted as:

- A) a horizontal bar chart, sorted, top features first
- B) a scatter plot of features vs labels
- C) a pie chart
- D) a 3D surface

**M5.** The ROC curve's chance line is:

- A) the diagonal from (0, 0) to (1, 1) — AUC 0.5
- B) the horizontal axis
- C) the vertical axis
- D) a circle of radius 1

**M6 (code-output).** What prints?
```python
print(0.0 <= float(auc(*roc_curve(y_true, y_score)[:2])) <= 1.0)
```

- A) `True`
- B) `False`
- C) `None`
- D) raises `TypeError`

**M7 (code-output).** What prints?
```python
import numpy as np
train = np.array([0.94, 0.95, 0.96])
valid = np.array([0.93, 0.90, 0.87])
print(train[-1] > train[0], valid[-1] < valid[0])
```

- A) `True True`
- B) `True False`
- C) `False True`
- D) `False False`

**M8.** On a balanced problem, the PR curve:

- A) flattens toward the class prior — ROC is the better view
- B) is always better than ROC
- C) is undefined
- D) shows the same shape as ROC

**M9.** Which plots belong in a model card / fairness review?

- A) feature importance and confusion matrix
- B) only the loss curve
- C) only the embedding scatter
- D) only the learning curve

---

## Hard

**H1 (code-output).** What prints?
```python
import numpy as np
from sklearn.metrics import auc, roc_curve
fpr, tpr, _ = roc_curve(y_true, y_score)
order = np.argsort(y_score)[::-1]
y_t = y_true[order]
tp = np.cumsum(y_t)
recall = tp / max(int(tp[-1]), 1)
precision = tp / np.maximum(tp + np.cumsum(1 - y_t), 1)
precision = np.concatenate([[precision[0]], precision])
recall = np.concatenate([[0.0], recall])
pr_auc = float(np.trapezoid(precision, recall))
print(round(pr_auc, 4))
```

- A) `0.8926`
- B) `0.9416`
- C) `0.5`
- D) `1.0`

**H2.** Why does PR degrade visibly on rare positives while ROC stays
high?

- A) precision divides by (TP+FP), so a few false positives wreck it
  when positives are rare; ROC's FPR denominator is huge
- B) ROC ignores thresholds
- C) PR is computed on a different seed
- D) ROC is always 1.0 for rare classes

**H3.** `assert fpr[0] == 0.0 and abs(fpr[-1] - 1.0) < 1e-12` in a
verify function guards against:

- A) a broken ROC implementation that doesn't pad the endpoints
- B) a bug in the colormap
- C) too few classes
- D) the chance line missing

**H4.** The "operating point" is:

- A) the threshold chosen on the ROC/PR curve (the elbow) for
  deployment
- B) the first threshold
- C) the point where AUC is measured
- D) the training endpoint of the learning curve

**H5.** For an ML eval dashboard rendered nightly in CI, the correct
pattern is:

- A) render the six canonical plots from the eval JSON with fixed
  seeds, assert artifacts exist and curves have sane endpoints
- B) open an interactive window and screenshot it manually
- C) only print numeric metrics, never plot
- D) use a GUI backend and keep figures open

---

## Answer Key

**E1 — A.** Learning curve = scores vs training-set size.
*Distractors:* B/C/D mix unrelated pairs.

**E2 — A.** Diagonal cells count correct predictions per class.
*Distractors:* B is the off-diagonal; C is a different metric; D is
the matrix dimension.

**E3 — A.** ROC is padded to start at (0,0) and end at (1,1) exactly.
*Distractors:* B/C/D break one or both endpoint claims.

**E4 — A.** Residual = y_true − y_pred: 5.0−4.5 = 0.5, 7.0−8.0 = −1.0
(positive = under-predicting).
*Distractors:* B is the flipped sign convention; C/D mix signs.

**E5 — A.** PR exposes precision collapse when positives are rare.
*Distractors:* B is right for balanced problems; C/D dodge the choice.

**E6 — A.** Seeded separation yields ROC AUC 0.9416 (verified).
*Distractors:* B is chance; C is perfect; D is the PR AUC.

**M1 — A.** A funnel = heteroscedasticity (variance grows with
magnitude).
*Distractors:* B/C/D are unrelated readings.

**M2 — A.** The zero line makes bias visible as systematic deviation.
*Distractors:* B/C/D are other concepts.

**M3 — A.** 3 classes → 3×3; `cm[0,0]` counts true negatives of class
0 — positive here.
*Distractors:* B wrong shape; C claims zero (wrong); D is sample
count, not class count.

**M4 — A.** Sorted horizontal bars are the canonical importance plot.
*Distractors:* B/C/D are wrong chart types.

**M5 — A.** The diagonal is the chance line (AUC 0.5).
*Distractors:* B/C/D are geometry noise.

**M6 — A.** AUC lies in [0, 1] by construction; the seeded value
0.9416 satisfies it.
*Distractors:* B/C/D are wrong.

**M7 — A.** Train improves while validation degrades — the widening
gap is the overfit signature.
*Distractors:* B/C/D are false readings of the flags.

**M8 — A.** PR flattens to the prior on balanced data — ROC is the
right view.
*Distractors:* B/C/D are false.

**M9 — A.** Governance artifacts: feature importance + confusion
matrix (plus residuals/ROC).
*Distractors:* B/C/D each omit the required plots.

**H1 — A.** The PR AUC for the seeded data is 0.8926 (verified).
*Distractors:* B is the ROC AUC; C is chance; D is perfect.

**H2 — A.** Precision = TP/(TP+FP): with rare positives, a handful of
FPs drops precision hard; ROC's FPR divides by all negatives, so it
barely moves.
*Distractors:* B/C/D are false.

**H3 — A.** Endpoint padding is a correctness property of the curve —
the verify assertion catches broken implementations.
*Distractors:* B/C/D are unrelated.

**H4 — A.** The deployment threshold is picked at the elbow of the
curve.
*Distractors:* B/C/D are other points.

**H5 — A.** Nightly CI rendering from JSON with fixed seeds and
artifact assertions — the production pattern.
*Distractors:* B is manual; C loses visual signal; D blocks CI.

---

**Scoring:** 17+ Expert · 13–16 Practitioner · 8–12 Proficient · <8 Novice.
**Related:** [Lecture 23](03-libraries/matplotlib/lectures/23-ml-visualization-lecture.md) ·
[Glossary 23](03-libraries/matplotlib/lectures/23-ml-visualization-glossary.md) ·
[Challenge 23](03-libraries/matplotlib/challenges/23-ml-visualization/README.md)
