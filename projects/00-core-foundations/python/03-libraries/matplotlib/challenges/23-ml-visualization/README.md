# Challenge 23: ML Visualization

## 🥉 Bronze — ROC Endpoints (~15 min)

**Task:** Compute an ROC curve from synthetic scores and return the
curve arrays.

**Signature:**
```python
def roc_endpoints(y_true: np.ndarray, y_score: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
```

**Requirements:**
- Use `sklearn.metrics.roc_curve` when installed; otherwise a numpy
  threshold-sweep fallback (cumsum over sorted scores)
- Return `(fpr, tpr)`

| Input (700 neg / 300 pos, separated gaussians) | Expected |
|-------|----------|
| seeded arrays | `fpr[0] == 0.0`, `tpr[0] == 0.0`, ends at `(1.0, 1.0)` |

**Constraints:** must never print; must be deterministic for seeded
input. The endpoints `(0,0)` and `(1,1)` must hold exactly.

---

## 🥈 Silver — Confusion Structure (~35 min)

**Task:** Return the shape and diagonal sum of a confusion matrix —
the two numbers that make accuracy meaningful.

**Signature:**
```python
def confusion_stats(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, int]:
```

**Requirements:**
- 3-class synthetic predictions (seeded), labels `[0, 1, 2]`
- `cm = confusion_matrix(y_true, y_pred, labels=[0, 1, 2])`
  (sklearn, or numpy fallback)
- Return `{"shape": (3, 3), "diagonal": int}` where `diagonal` is
  `cm[i, i]` summed

| Input | Expected |
|-------|----------|
| 300 seeded samples | `shape == (3, 3)`; `diagonal == len(y_true)` when predictions are perfect |

**Constraints:** must work with and without sklearn (fallback).

---

## 🥇 Gold — Learning Curve Verdict (~75 min)

**Task:** Generate a deterministic synthetic learning curve and decide
whether "more data helps" for this model.

**Signature:**
```python
def learning_curve_improves() -> bool:
```

**Requirements:**
- `sizes = arange(100, 2001, 100)`; `train` saturates toward ~0.94,
  `valid` toward ~0.90, both with seeded noise
- Return True iff `train[-1] > train[0]`, `valid[-1] > valid[0]`, and
  `np.all(train >= valid)`

| Input | Expected |
|-------|----------|
| none (seeded rng inside) | `True` |

**Constraints:** the verdict must be a pure function of the synthetic
data — no fitting, no I/O; must stay deterministic across runs.
**Follow-up:** which condition would flip to False for an overfitting
model? (Answer: `np.all(train >= valid)` — validation falls below
train as the gap widens.)

---

## Running

```bash
python -m pytest 03-libraries/matplotlib/challenges/23-ml-visualization/test_challenge.py -v
```

## Test File Structure

```
challenges/23-ml-visualization/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
