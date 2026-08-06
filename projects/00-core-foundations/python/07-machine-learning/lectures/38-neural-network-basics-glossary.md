# Neural Network Basics — Glossary 38

Companion lecture: `38-neural-network-basics-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Activation | Layer | Non-linear function between layers that gives the net its power |
| Backprop | Training | Chain-rule computation of gradients through the graph |
| Batch norm | Regularization | Normalizes activations per channel to stabilize training |
| Dead ReLU | Failure | A ReLU unit stuck at zero, contributing no gradient |
| Dropout | Regularization | Randomly zeroes activations during training |
| Exploding gradients | Failure | Gradients growing through layers, diverging training |
| GELU | Activation | Smoothed ReLU, standard in transformer FFNs |
| Gradient flow | Training | How well signals survive backward passes |
| He init | Initialization | Kaiming initialization sized for ReLU networks |
| Initialization | Training | The starting scale of weights |
| LayerNorm | Regularization | Normalizes across features; used in transformers |
| Learning rate | Training | The step size of each optimizer update |
| LR range test | Training | Exponential LR sweep to find the best learning rate |
| NaN loss | Failure | Diverged training; check lr, data, loss in order |
| ReLU | Activation | max(0, x); the default hidden activation |
| Sigmoid | Activation | Squashes to 0..1; output use, bad in hidden layers |
| Softmax | Activation | Turns logits into a probability distribution |
| Vanishing gradients | Failure | Gradients shrinking through layers, starving early layers |
| Xavier init | Initialization | Glorot initialization sized for tanh/sigmoid networks |

## Detailed Definitions

### Activation
**Definition**: A non-linear function applied after a linear layer; without
them, stacked linear layers collapse into one linear layer. Choices: ReLU
(hidden), sigmoid/softmax (output).
**Example**:
```python
nn.Sequential(nn.Linear(10, 32), nn.ReLU(), nn.Linear(32, 1))
```
**Related**: ReLU, Sigmoid, GELU

### Backprop
**Definition**: Reverse-mode differentiation: the chain rule applied from loss
to inputs, giving every parameter its gradient.
**Related**: Gradient flow, Autograd

### Batch norm
**Definition**: Normalizes each channel's activations to zero mean / unit
variance per batch, then applies learned scale and shift. Stabilizes
training and allows higher learning rates. Uses running statistics in eval.
**Example**:
```python
nn.BatchNorm1d(8)
```
**Related**: LayerNorm, Gradient flow

### Dead ReLU
**Definition**: A ReLU unit whose inputs are always negative, so its output and
gradient are always zero. Caused by bad init or a too-high learning rate.
**Related**: ReLU, Learning rate

### Dropout
**Definition**: Randomly zeroes a fraction of activations each training step —
a cheap ensemble regularizer. Disabled in eval mode.
**Example**:
```python
nn.Dropout(p=0.5)   # keeps ~50% of units per step in train mode
```
**Related**: Regularization

### Exploding gradients
**Definition**: Gradients growing multiplicatively through layers until updates
overflow — the mirror image of vanishing gradients; fixed by norm, init,
residuals, and clipping.
**Related**: Vanishing gradients, Gradient flow

### GELU
**Definition**: Gaussian Error Linear Unit, a smooth ReLU approximation and the
standard hidden activation in transformer feed-forward networks.
**Related**: ReLU, Activation

### Gradient flow
**Definition**: The ease with which gradients propagate backward through the
network; poor flow means early layers learn slowly or not at all.
**Related**: Vanishing gradients, Backprop

### He init
**Definition**: Kaiming initialization with std sqrt(2/fan_in), designed for
ReLU networks to preserve signal variance.
**Example**:
```python
nn.init.kaiming_uniform_(layer.weight, a=0)
```
**Related**: Xavier init, Initialization

### Initialization
**Definition**: The scheme that sets starting weight values; its scale decides
whether forward signals and backward gradients survive.
**Related**: He init, Xavier init

### LayerNorm
**Definition**: Normalizes activations across features per sample rather than
per batch — the normalization used inside transformer blocks.
**Related**: Batch norm, Gradient flow

### Learning rate
**Definition**: The step size of each optimizer update; too high diverges, too
low stalls. The dominant training hyperparameter.
**Related**: LR range test

### LR range test
**Definition**: Training briefly while exponentially increasing the learning
rate, then choosing the rate at the steepest loss descent.
**Related**: Learning rate

### NaN loss
**Definition**: A diverged loss value signaling numerical collapse; debug in
order: learning rate, data (NaN/inf inputs), then loss function.
**Related**: Exploding gradients

### ReLU
**Definition**: Rectified Linear Unit, max(0, x) — cheap, non-saturating, the
default hidden activation. Risk: dead units.
**Related**: Activation, Dead ReLU

### Sigmoid
**Definition**: Squashes to (0,1); appropriate at a binary output, but its
saturation kills gradients in hidden layers.
**Related**: Activation

### Softmax
**Definition**: Normalizes a vector of logits into a probability distribution
summing to 1; the multi-class output activation.
**Related**: Activation

### Vanishing gradients
**Definition**: Gradients shrinking multiplicatively through layers so early
layers barely learn. Fixed by good init, normalization, and residual paths.
**Related**: Exploding gradients, Gradient flow

### Xavier init
**Definition**: Glorot initialization with std sqrt(1/fan_in), sized for
tanh/sigmoid activations.
**Example**:
```python
nn.init.xavier_uniform_(layer.weight)
```
**Related**: He init

## Key Concepts Summary

### Activation and init
- ReLU/GELU hidden; sigmoid/softmax output only.
- He init for ReLU, Xavier for tanh/sigmoid.
- Initialization scale decides whether signals survive.

### Stabilization
- Batch norm centers activations; LayerNorm is the transformer variant.
- Dropout regularizes in train mode, is off in eval mode.
- Residual connections fix depth-related gradient loss.

### Debugging order
- NaN loss: lr first, then data, then loss function.
- Divergence: lr too high; stagnation: lr too low — use the range test.
- Track gradient norms to catch vanishing early.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. max(0, x), the default hidden activation — ___
2. Gradients shrinking through layers — ___
3. Random zeroing of activations during training — ___
4. The step size of each optimizer update — ___
5. Kaiming init sized for ReLU nets — ___
6. Normalization across features, used in transformers — ___
7. Squashes logits to a probability distribution — ___
8. The chain rule applied backward through the graph — ___

**Answers:** 1-ReLU, 2-vanishing gradients, 3-dropout, 4-learning rate,
5-He init, 6-LayerNorm, 7-softmax, 8-backprop
