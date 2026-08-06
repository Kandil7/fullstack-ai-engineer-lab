# PyTorch Tensors — Glossary 36

Companion lecture: `36-pytorch-tensors-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Autograd | Core | Automatic differentiation via the recorded computation graph |
| Backward | Core | The call that walks the graph in reverse computing gradients |
| Broadcasting | Core | Aligning shapes by expanding size-1 dims (NumPy rules) |
| Computation graph | Core | The recorded forward operations used for backprop |
| Contiguous | Shape | Memory laid out in row-major order; required by `.view()` |
| Device | Hardware | CPU or GPU where a tensor's memory lives |
| float16 | Dtype | Half precision: half the memory, less precision |
| float32 | Dtype | The DL default precision |
| Gradient | Core | The derivative of the loss with respect to a tensor |
| requires_grad | Core | Flag that makes a tensor participate in autograd |
| no_grad | Core | Context manager that disables graph building |
| Permute | Shape | Transpose dimensions as a view (no copy) |
| Reshape | Shape | Give the data a new shape (view when possible, else copy) |
| Squeeze | Shape | Remove size-1 dimensions |
| Tensor | Core | NumPy array + device + autograd graph |
| Unsqueeze | Shape | Add a size-1 dimension |
| zero_grad | Core | Clear accumulated gradients before the next backward |

## Detailed Definitions

### Autograd
**Definition**: PyTorch's automatic differentiation engine. Operations on
tensors with `requires_grad=True` are recorded so gradients can be computed by
reverse-mode differentiation.
**Example**:
```python
y = w * x + b      # recorded
y.backward()       # computed
```
**Related**: Computation graph, Backward

### Backward
**Definition**: The method that runs reverse-mode differentiation on the
computation graph, populating `.grad` on every leaf with `requires_grad=True`.
**Related**: Autograd, Gradient

### Broadcasting
**Definition**: The rule that expands size-1 dimensions so tensors of
different shapes can be combined — identical to NumPy: align trailing
dimensions, expand 1s.
**Example**:
```python
a = torch.randn(3, 1); b = torch.randn(1, 4)
c = a * b          # (3, 4)
```
**Related**: Tensor

### Computation graph
**Definition**: The directed graph of forward operations connecting inputs to
the loss; autograd walks it backward.
**Related**: Autograd, Backward

### Contiguous
**Definition**: A tensor whose elements are laid out in memory in row-major
order. `.view()` requires contiguity; call `.contiguous()` after `permute` or
transpose-style ops.
**Related**: Permute, Reshape

### Device
**Definition**: The hardware (`cpu` or `cuda:N`) where tensor storage lives.
Model and data must share a device or every operation pays a transfer.
**Related**: Tensor

### float16
**Definition**: Half-precision float. Half the memory of float32; used for
inference and mixed-precision training on GPUs.
**Related**: float32

### float32
**Definition**: The default floating-point dtype in PyTorch — the standard for
deep learning weights and activations.
**Related**: float16

### Gradient
**Definition**: The derivative of the loss with respect to a tensor, stored in
`.grad` after `backward()`. Used by optimizers to update weights.
**Related**: Backward, Autograd

### requires_grad
**Definition**: The tensor flag that opts it into the autograd graph; only
tensors with this flag receive gradients.
**Related**: Autograd, Gradient

### no_grad
**Definition**: A context manager that disables graph building — used for
inference and feature extraction to save memory and time.
**Example**:
```python
with torch.no_grad():
    preds = model(x)
```
**Related**: Autograd

### Permute
**Definition**: Reorder a tensor's dimensions as a view that shares memory.
`t.permute(1, 0)` transposes a 2-D tensor.
**Related**: Contiguous, Reshape

### Reshape
**Definition**: Give a tensor's data a new shape. Returns a view when
possible, a copy otherwise — use `reshape` when contiguity is uncertain.
**Example**:
```python
torch.arange(12).reshape(3, 4)
```
**Related**: View, Contiguous

### Squeeze
**Definition**: Remove dimensions of size 1 from a tensor's shape.
**Example**:
```python
t.unsqueeze(0).squeeze()   # add then remove a size-1 dim
```
**Related**: Unsqueeze

### Tensor
**Definition**: The fundamental data structure: a typed, multi-dimensional
array with a device and optional autograd participation.
**Related**: Device, Dtype

### Unsqueeze
**Definition**: Insert a size-1 dimension at a given position.
**Related**: Squeeze

### zero_grad
**Definition**: The call that clears accumulated gradients. Required before
each `backward()` or gradients sum across iterations.
**Example**:
```python
optimizer.zero_grad()
```
**Related**: Gradient

## Key Concepts Summary

### The tensor mental model
- Tensor = NumPy array + device + autograd graph.
- float32 is the default; half for memory savings.
- Model and data must share a device.

### Autograd discipline
- `requires_grad=True` builds the graph; `no_grad()` disables it for inference.
- Zero gradients before every backward pass.
- Backprop is the chain rule, automated by the graph.

### Shape operations
- reshape (may copy), permute/unsqueeze/squeeze (views).
- Non-contiguous views need `.contiguous()` before `.view()`.
- Broadcasting rules are identical to NumPy.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Automatic differentiation via the recorded graph — ___
2. The DL default precision — ___
3. Clearing accumulated gradients before backward — ___
4. Context manager that disables graph building — ___
5. The hardware where tensor memory lives — ___
6. Reordering dimensions as a view — ___
7. Expanding size-1 dims so shapes combine — ___
8. The flag that opts a tensor into autograd — ___

**Answers:** 1-autograd, 2-float32, 3-zero_grad, 4-no_grad, 5-device,
6-permute, 7-broadcasting, 8-requires_grad
