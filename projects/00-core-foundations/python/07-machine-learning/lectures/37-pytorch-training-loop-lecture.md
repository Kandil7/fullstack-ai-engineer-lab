# 07-machine-learning — 37: PyTorch Training Loop — The Canonical Pattern

Companion exercise: `37-pytorch-training-loop.py`

---

## Topic Overview

Every PyTorch project — from a research prototype to a production fine-tune —
runs the same few-line training loop: zero the gradients, run the model, compute
the loss, backpropagate, step the optimizer. This topic makes that loop
second nature and adds the single most valuable debugging trick in deep
learning: **overfit one batch first**. If your model cannot drive the loss down
on a single batch, the bug is in your code, not your data — and you find that
out in seconds instead of after an hour of training.

The topic covers `nn.Module` (how models are defined and parameters collected),
`Dataset`/`DataLoader` (batching and shuffling), the canonical loop, train vs
eval mode, device placement, and the overfit-one-batch debugging protocol.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Define a model as an `nn.Module` subclass with a `forward` method.
2. Explain how `model.parameters()` collects trainable weights automatically.
3. Build a `DataLoader` from a `Dataset` and compute batch counts.
4. Write the canonical training loop from memory.
5. Explain why `zero_grad` must precede `backward`.
6. Use the overfit-one-batch trick as a first debugging step.
7. Distinguish train mode from eval mode and when each is required.
8. Move a model and its data to a device correctly.

## Prerequisites

| Need | Where |
|---|---|
| Tensors and autograd | `36-pytorch-tensors.py` |
| Loss functions and SGD intuition | `05-linear-regression.py` |
| NumPy broadcasting | `03-libraries/numpy/lectures/29-broadcasting-deep-lecture.md` |

## 1. nn.Module — Define the Model

```python
import torch.nn as nn

class TwoLayerNet(nn.Module):
    def __init__(self, in_dim, hidden, out_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, out_dim),
        )

    def forward(self, x):
        return self.net(x)

model = TwoLayerNet(10, 32, 1)
print(sum(p.numel() for p in model.parameters()))
```

Output:
```
353   # 10*32 + 32 + 32*1 + 1
```

`nn.Module` subclasses register submodules and parameters automatically — no
manual bookkeeping. `forward()` defines the computation; you never call
`model.forward(x)` directly (hooks and eval mode rely on the `__call__` path).

## 2. Dataset & DataLoader — Batching and Shuffling

```python
from torch.utils.data import TensorDataset, DataLoader

dataset = TensorDataset(X, y)                       # (features, targets) pairs
loader = DataLoader(dataset, batch_size=64, shuffle=True)
```

Output:
```
batches per epoch: 16   # 1000 rows / 64
```

`DataLoader` yields `(x_batch, y_batch)` tuples. `shuffle=True` breaks
correlation between consecutive batches (essential for SGD); for
time-series use `shuffle=False` and split chronologically.

## 3. Loss + Optimizer + The Canonical Loop

```python
criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-2)

def train_one_epoch(m, dataloader, crit, opt):
    m.train()
    total_loss, n = 0.0, 0
    for xb, yb in dataloader:
        opt.zero_grad()
        logits = m(xb)
        loss = crit(logits, yb)
        loss.backward()
        opt.step()
        total_loss += loss.item()
        n += 1
    return total_loss / n
```

Output:
```
epoch 1: loss 0.5324
epoch 2: loss 0.4210
epoch 3: loss 0.3382
```

The five steps — `zero_grad -> forward -> loss -> backward -> step` — never
change order. `BCEWithLogitsLoss` combines sigmoid and BCE numerically
stably; you do not apply sigmoid before it.

## 4. The Debug Trick: Overfit a Single Batch

```python
xb, yb = next(iter(loader))
debug_model = TwoLayerNet(10, 32, 1)
opt = torch.optim.Adam(debug_model.parameters(), lr=1e-2)
for step in range(50):
    opt.zero_grad()
    loss = criterion(debug_model(xb), yb)
    loss.backward()
    opt.step()
print(loss.item())
```

Output:
```
loss on ONE batch after 50 steps: 0.0184   # should drop well below 0.5
```

If a model cannot memorize a single batch, the bug is structural: wrong shapes,
broken loss, dead activations, or a miswired forward. Fix it here, in seconds,
before touching real data.

## 5. Train vs Eval Mode

```python
model.train()      # enables dropout, batch-norm batch statistics
model.eval()       # disables them; uses running statistics
with torch.no_grad():
    logits = model(X[:10])
```

Output:
```
probabilities: tensor([0.1230, 0.8990, ...])
```

Forgetting `.eval()` during inference silently changes results for models with
dropout or batch norm. Forgetting `.train()` after eval breaks training the
same way.

## 6. Device Placement

```python
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
for xb, yb in loader:
    xb, yb = xb.to(device), yb.to(device)
```

Output:
```
# model and batch now share a device — no implicit transfers
```

Move the model once, move each batch to match. `TensorDataset` keeps data on
CPU; the `.to(device)` in the loop is the standard pattern.

## 7. Common Mistakes to Avoid

### Mistake 1: Missing zero_grad
```
# WRONG
loss.backward(); opt.step()          # gradients accumulate
# CORRECT
opt.zero_grad(); loss.backward(); opt.step()
```

### Mistake 2: Sigmoid then BCEWithLogitsLoss
```
# WRONG — double sigmoid: unstable and wrong
loss = criterion(torch.sigmoid(logits), y)
# CORRECT
loss = criterion(logits, y)          # BCEWithLogitsLoss includes sigmoid
```

### Mistake 3: Forgetting .eval() at inference
```
# WRONG — dropout still active during evaluation
preds = model(x)
# CORRECT
model.eval(); with torch.no_grad(): preds = model(x)
```

### Mistake 4: Calling model.forward(x) directly
```
# WRONG — bypasses hooks and eval-mode machinery
out = model.forward(x)
# CORRECT
out = model(x)
```

### Mistake 5: Training on unshuffled, correlated batches
```
# WRONG — loader without shuffle for non-sequential data
# CORRECT
DataLoader(ds, batch_size=64, shuffle=True)
```

## 8. Best Practices

1. Write the loop once as a function; never hand-copy it per experiment.
2. Overfit one batch before the first full run.
3. Track loss and a metric (accuracy/AUC) every epoch — loss alone lies.
4. Move the model and batches to the same device explicitly.
5. Use `model.eval()` + `torch.no_grad()` for all evaluation.
6. Log to a tracker (MLflow) from the first run — see `08-mlops/02`.
7. Use `shuffle=True` for i.i.d. data, `shuffle=False` for sequences.
8. Pin seeds for reproducible runs.
9. Keep batch size a power of two for GPU efficiency.
10. If loss is NaN, check lr first, then data, then the loss function.

## 9. Complexity and Cost

| Operation | Time per step | Space | Notes |
|---|---|---|---|
| Forward pass | O(parameters) | activations x batch | Grows with batch size |
| Backward pass | ~2x forward | graph of activations | Autograd holds the graph |
| Optimizer step | O(parameters) | optimizer state | Adam keeps momentum buffers |
| DataLoader yield | I/O bound | batch size | `num_workers>0` overlaps loading |

Memory is dominated by activations held for backprop — batch size is the lever
you turn to fit a GPU. Halving the batch halves activation memory.

## 10. AI Engineering Relevance

**Where this shows up:** every fine-tuning run — LoRA adapters, classifiers,
embedding models — is this loop with a different `forward`. The overfit-one-
batch trick is the standard first check when a training job diverges.

| Concept here | Used for |
|---|---|
| Canonical loop | The shape of every training and fine-tuning script |
| Overfit one batch | Debugging training code before spending GPU hours |
| DataLoader | Batching training corpora and streaming from disk |
| Train/eval mode | Correct validation and evaluation in every experiment |
| Device placement | GPU utilization and OOM avoidance in training services |

**Scale note:** at training-service scale the loop becomes distributed — data
parallel, sharded — but the per-step pattern is identical. The single-batch
check is even more valuable on a cluster, where debugging is expensive.

## 11. Summary

| Concept | Description |
|---|---|
| nn.Module | Class-based model; parameters collected automatically |
| DataLoader | Batching + shuffling over a Dataset |
| Canonical loop | zero_grad -> forward -> loss -> backward -> step |
| Overfit one batch | First debugging step; isolates code bugs from data bugs |
| train/eval | Mode switch for dropout and batch norm |
| Device | Move model and data together |

## 12. Quick Reference

| Task | Idiom |
|---|---|
| Define model | `class Net(nn.Module): def forward(self, x)` |
| Load batches | `DataLoader(TensorDataset(X, y), batch_size=64, shuffle=True)` |
| Loss | `nn.BCEWithLogitsLoss()` for binary classification |
| One step | `opt.zero_grad(); loss.backward(); opt.step()` |
| Debug | `for _ in range(50): ...` on one batch |
| Eval | `model.eval(); with torch.no_grad():` |

## Next Steps

Next: **[38 — Neural Network Basics](38-neural-network-basics-lecture.md)** — activations, initialization, regularization.

Continues in: **[39 — Transfer Learning](39-transfer-learning-lecture.md)** — freezing and fine-tuning pretrained models.

Official docs: <https://pytorch.org/tutorials/beginner/basics/optimization_tutorial.html>
