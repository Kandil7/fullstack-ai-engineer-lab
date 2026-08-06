# 07-machine-learning — 36: PyTorch Tensors — The GPU Currency

Companion exercise: `36-pytorch-tensors.py`

---

## Topic Overview

A tensor is to deep learning what an array is to NumPy — the fundamental data
unit — plus two additions: a **device** (CPU or GPU) and the **autograd**
computation graph. Every model input, weight, and gradient in PyTorch is a
tensor. Understanding shapes, dtypes, device placement, and autograd is the
difference between code that trains and code that OOMs, silently computes
wrong, or blocks the CPU with accidental transfers.

This topic builds the tensor foundation: creation, dtypes, devices, autograd,
`no_grad`, broadcasting (identical rules to NumPy), and shape manipulation.
Everything in the rest of the deep-learning track — training loops, networks,
transfer learning, transformers — is composed of these primitives.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Create tensors from lists, NumPy arrays, and factory functions.
2. Explain the role of dtypes, especially float32 as the DL default.
3. Move tensors between CPU and GPU and explain the transfer cost.
4. Explain autograd and the computation graph.
5. Read `requires_grad` and gradients after `backward()`.
6. Use `torch.no_grad()` for inference and feature extraction.
7. Apply NumPy broadcasting rules to tensors.
8. Use reshape, permute, unsqueeze, and squeeze correctly.

## Prerequisites

| Need | Where |
|---|---|
| NumPy arrays | `03-libraries/numpy/lectures/04-array-indexing-lecture.md` |
| Broadcasting | `03-libraries/numpy/lectures/29-broadcasting-deep-lecture.md` |
| Gradient descent intuition | `05-linear-regression.py` |

## 1. Creating Tensors

```python
import torch
t = torch.tensor([[1, 2, 3], [4, 5, 6]])
print(t.shape, t.dtype)                    # torch.Size([2, 3]) torch.int64

ones = torch.ones(2, 3)
zeros = torch.zeros(3)
randn = torch.randn(2, 2)
eye = torch.eye(3)
```

Output:
```
torch.Size([2, 3]) torch.int64
```

Note the default integer dtype is `int64`, and the default float dtype is
`float32` — unlike NumPy's `float64`. That difference is deliberate: deep
learning uses float32 for speed and memory.

## 2. NumPy <-> Tensor Roundtrip

```python
arr = np.array([1.0, 2.0, 3.0])
t = torch.from_numpy(arr)     # shares memory with arr
back = t.numpy()              # back to NumPy
```

Output:
```
[1. 2. 3.]
```

`from_numpy` shares memory — mutating one side mutates the other. Detach with
`.clone()` when you need independence.

## 3. Dtypes — float32 Is the DL Default

```python
f64 = torch.tensor([1.0])          # float32 by default
f16 = f64.half()                   # half precision
i64 = torch.tensor([1]).long()     # int64
print(f64.dtype, f16.dtype, i64.dtype)
```

Output:
```
torch.float32 torch.float16 torch.int64
```

float16 halves memory and speeds up GPU math (with reduced precision — used for
inference and mixed-precision training). Cast with `.half()`, `.float()`,
`.double()`, `.long()`.

## 4. Device — CPU vs GPU

```python
device = "cuda" if torch.cuda.is_available() else "cpu"
x = torch.randn(2, 2, device=device)
```

Output:
```
tensor on cpu   # or cuda:0 when a GPU is present
```

Rules of thumb: `model.to(device)` moves all weights at once; move data to the
same device as the model or every op does a slow host-device transfer; move
back to CPU with `.cpu()` before converting to NumPy (`tensor.numpy()` fails on
GPU tensors).

## 5. Autograd — The Computation Graph

Tensors with `requires_grad=True` record operations so gradients can be
computed by reverse-mode differentiation.

```python
w = torch.tensor(3.0, requires_grad=True)
b = torch.tensor(1.0, requires_grad=True)
x = torch.tensor(2.0)
y = w * x + b
y.backward()
print(w.grad, b.grad)          # dy/dw = x = 2.0 ; dy/db = 1.0
```

Output:
```
tensor(2.) tensor(1.)
```

The graph records the forward operations; `backward()` walks it in reverse
applying the chain rule. This is backprop, automated.

## 6. no_grad — Inference and Feature Extraction

```python
with torch.no_grad():
    z = w * x + b              # no graph, no gradient memory
```

Output:
```
z requires_grad=False
```

Use `no_grad` for any evaluation pass: it halves memory and speeds inference
because no graph is built.

## 7. Gradients Accumulate — Zero Before Backward

```python
optimizer.zero_grad()   # or w.grad.zero_()
loss.backward()
optimizer.step()
```

Output:
```
# without zero_grad, gradients add across iterations and training diverges
```

This is the most common beginner bug: forgetting `zero_grad()` means gradients
accumulate and the optimizer takes increasingly wrong steps.

## 8. Broadcasting — Same Rules as NumPy

```python
a = torch.randn(3, 1)
b = torch.randn(1, 4)
c = a * b                 # (3,1) * (1,4) -> (3,4)
```

Output:
```
(3, 1) * (1, 4) -> (3, 4)
```

Broadcasting aligns trailing dimensions and expands size-1 dimensions — the
exact NumPy rules from `29-broadcasting-deep`. It is how batch operations
(vectorized over examples) are written.

## 9. Reshape / Permute / Unsqueeze / Squeeze

```python
t2 = torch.arange(12).reshape(3, 4)   # same data, new shape (view when possible)
tp = t2.permute(1, 0)                 # transpose dims (view, no copy)
ts = t2.unsqueeze(0).squeeze()        # add/remove size-1 dims
```

Output:
```
reshape [3, 4], permute -> [4, 3], unsqueeze/squeeze -> [3, 4]
```

`reshape` may copy; `permute`, `unsqueeze`, `squeeze` are views. For code that
must never copy, use `tensor.contiguous()` after ops that produce non-contiguous
views before `.view()`.

## 10. Common Mistakes to Avoid

### Mistake 1: Forgetting zero_grad()
```
# WRONG
loss.backward(); optimizer.step()      # gradients accumulate every step
# CORRECT
optimizer.zero_grad(); loss.backward(); optimizer.step()
```

### Mistake 2: Converting a GPU tensor to NumPy directly
```
# WRONG
tensor.numpy()    # RuntimeError on cuda tensors
# CORRECT
tensor.cpu().numpy()
```

### Mistake 3: Mixing devices in one expression
```
# WRONG
model.to("cuda"); out = model(data_cpu)     # implicit slow transfer per op
# CORRECT — move data to the model's device
```

### Mistake 4: Using .view() on a non-contiguous tensor
```
# WRONG
t.permute(1, 0).view(-1)      # RuntimeError: view size is not compatible
# CORRECT
t.permute(1, 0).contiguous().view(-1)
```

### Mistake 5: Building graphs during evaluation
```
# WRONG
with torch.no_grad() missing on the eval loop   # wasted memory, slower
# CORRECT
with torch.no_grad(): ...
```

## 11. Best Practices

1. Use float32 as the default; half only for inference or mixed precision.
2. Move the model once with `.to(device)`; move batches to match.
3. Wrap every evaluation pass in `torch.no_grad()`.
4. Zero gradients before every `backward()`.
5. Prefer `reshape` over `view` unless you verified contiguity.
6. Keep the NumPy <-> torch boundary explicit; share memory only deliberately.
7. Check `tensor.device` when shapes are right but results are wrong.
8. Use broadcasting over explicit loops for batch operations.
9. Pin seeds (`torch.manual_seed(0)`) for reproducible runs.
10. Profile with `torch.cuda` timing before assuming GPU speed.

## 12. Summary

| Concept | Description |
|---|---|
| Tensor | NumPy array + device + autograd graph |
| float32 | The DL default dtype |
| Device | CPU or GPU; move model and data together |
| Autograd | Automatic reverse-mode differentiation via the graph |
| no_grad | Inference mode: no graph, less memory |
| zero_grad | Required before each backward pass |
| Broadcasting | NumPy rules apply identically |
| Views | permute/unsqueeze/squeeze share memory; reshape may copy |

## Quick Reference

| Task | Idiom |
|---|---|
| Create | `torch.tensor([...])`, `torch.ones(...)`, `torch.randn(...)` |
| Cast dtype | `t.float()`, `t.half()`, `t.long()` |
| Move device | `t.to("cuda")`, `t.cpu()` |
| No graph | `with torch.no_grad():` |
| Clear grads | `optimizer.zero_grad()` |
| NumPy roundtrip | `torch.from_numpy(a)`, `t.cpu().numpy()` |
| Shape ops | `reshape`, `permute`, `unsqueeze`, `squeeze`, `contiguous` |

## Next Steps

Next: **[37 — PyTorch Training Loop](37-pytorch-training-loop-lecture.md)** — the canonical pattern that uses these tensors.

Continues in: **[38 — Neural Network Basics](38-neural-network-basics-lecture.md)** — layers, init, regularization.

Official docs: <https://pytorch.org/docs/stable/tensors.html> · <https://pytorch.org/docs/stable/notes/autograd.html>
