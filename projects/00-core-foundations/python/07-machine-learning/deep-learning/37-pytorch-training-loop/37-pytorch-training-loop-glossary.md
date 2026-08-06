# PyTorch Training Loop — Glossary 37

Companion lecture: `37-pytorch-training-loop-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Backward | Loop | The call computing gradients via autograd |
| BCEWithLogitsLoss | Loss | Binary cross-entropy with built-in sigmoid, numerically stable |
| Canonical loop | Pattern | zero_grad -> forward -> loss -> backward -> step |
| DataLoader | Data | Iterator yielding batches with shuffling and workers |
| Dataset | Data | The collection of (input, target) pairs |
| Epoch | Loop | One full pass over the training data |
| eval mode | Mode | Disables dropout/batch-norm training behavior |
| forward | Model | The method defining the model's computation |
| Gradient | Loop | Loss derivative w.r.t. a parameter, used by the optimizer |
| Loss | Loop | The scalar objective minimized by training |
| nn.Module | Model | Base class for all neural network modules |
| Optimizer | Loop | The algorithm updating parameters from gradients |
| Overfit one batch | Debug | Drive loss down on a single batch to isolate code bugs |
| Parameters | Model | Trainable weights, collected by model.parameters() |
| Step | Loop | One optimizer update |
| train mode | Mode | Enables dropout and batch-norm batch statistics |
| zero_grad | Loop | Clearing accumulated gradients before backward |

## Detailed Definitions

### Backward
**Definition**: `loss.backward()` computes gradients for all parameters in the
graph via autograd, storing them in each parameter's `.grad`.
**Related**: Gradient, Canonical loop

### BCEWithLogitsLoss
**Definition**: Binary cross-entropy that applies sigmoid internally — use raw
logits, never pre-sigmoid probabilities. Numerically stable by design.
**Example**:
```python
criterion = nn.BCEWithLogitsLoss()
loss = criterion(model(xb), yb)      # not criterion(sigmoid(xb), yb)
```
**Related**: Loss

### Canonical loop
**Definition**: The five-step training pattern repeated for every batch:
zero gradients, forward pass, compute loss, backward pass, optimizer step.
**Example**:
```python
opt.zero_grad(); loss = crit(m(xb), yb); loss.backward(); opt.step()
```
**Related**: Epoch, Step

### DataLoader
**Definition**: An iterator that batches a Dataset, optionally shuffling and
loading with worker processes for speed.
**Example**:
```python
loader = DataLoader(ds, batch_size=64, shuffle=True)
```
**Related**: Dataset, Epoch

### Dataset
**Definition**: An object exposing `(input, target)` samples; `TensorDataset`
wraps tensors directly.
**Related**: DataLoader

### Epoch
**Definition**: One complete pass through the training data (all batches).
**Example**:
```python
for epoch in range(3):
    train_one_epoch(...)
```
**Related**: DataLoader, Canonical loop

### eval mode
**Definition**: `model.eval()` switches dropout off and batch norm to running
statistics — required for correct evaluation and inference.
**Related**: train mode

### forward
**Definition**: The `nn.Module` method defining the computation; call the model
(`model(x)`), never `model.forward(x)` directly.
**Related**: nn.Module

### Gradient
**Definition**: The derivative of the loss with respect to a parameter, stored
in `.grad` and consumed by the optimizer.
**Related**: Backward, Optimizer

### Loss
**Definition**: The scalar objective that training minimizes; its gradient
drives every parameter update.
**Related**: BCEWithLogitsLoss, Gradient

### nn.Module
**Definition**: The base class for all PyTorch networks; subclasses register
submodules and parameters automatically.
**Example**:
```python
class Net(nn.Module):
    def __init__(self): super().__init__(); self.fc = nn.Linear(10, 1)
    def forward(self, x): return self.fc(x)
```
**Related**: Parameters, forward

### Optimizer
**Definition**: The algorithm (SGD, Adam) that updates parameters from
gradients each step.
**Example**:
```python
optimizer = torch.optim.Adam(model.parameters(), lr=1e-2)
```
**Related**: Step, Gradient

### Overfit one batch
**Definition**: The debugging protocol of driving the loss near zero on a
single batch. If that fails, the bug is in the code, not the data.
**Related**: Canonical loop, Loss

### Parameters
**Definition**: The model's trainable weights, collected automatically by
`model.parameters()`.
**Related**: nn.Module, Optimizer

### Step
**Definition**: One optimizer update of the parameters from the current
gradients.
**Related**: Optimizer, Canonical loop

### train mode
**Definition**: `model.train()` enables dropout and batch-norm batch
statistics — the correct state for training.
**Related**: eval mode

### zero_grad
**Definition**: `optimizer.zero_grad()` clears accumulated gradients; without
it, gradients sum across iterations and training diverges.
**Related**: Gradient, Canonical loop

## Key Concepts Summary

### The loop
- Five steps, fixed order: zero_grad -> forward -> loss -> backward -> step.
- One epoch = one full pass; the loop repeats per batch per epoch.
- Loss alone lies — track a metric too.

### The modes
- train mode enables dropout/batch-norm training behavior.
- eval mode + no_grad is required for correct evaluation.
- Device placement: move the model once, batches each loop.

### Debugging
- Overfit one batch first: seconds, isolates code bugs.
- Double-sigmoid with BCEWithLogitsLoss is a silent correctness bug.
- Missing zero_grad is the most common divergence cause.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. The five-step training pattern — ___
2. Clearing accumulated gradients — ___
3. Binary cross-entropy with built-in sigmoid — ___
4. One full pass over the data — ___
5. Disables dropout during inference — ___
6. Driving loss to zero on one batch to isolate bugs — ___
7. The method defining a model's computation — ___
8. The algorithm updating parameters from gradients — ___

**Answers:** 1-canonical loop, 2-zero_grad, 3-BCEWithLogitsLoss, 4-epoch,
5-eval mode, 6-overfit one batch, 7-forward, 8-optimizer
