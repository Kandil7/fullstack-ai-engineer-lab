# Lecture 03: Neural Net Foundations (SGD)

## Topic Overview

In lessons 1–2 you trained and shipped a real model without knowing what
happened inside `fine_tune`. This lecture opens the box. At the center of
almost every modern model is one deceptively simple idea: **stochastic
gradient descent (SGD)** — nudging a bunch of numbers (the parameters) in
whatever direction makes the model's predictions a little less wrong, over
and over, until they stop improving.

We build this from first principles. We fit a quadratic with SGD by hand,
watch a learning rate that is too high blow up and one too low crawl, turn a
linear function into a neural net by adding a single nonlinearity (ReLU), and
finally connect it to the canonical fast.ai example: telling MNIST **3s from
7s**. Everything runs on plain PyTorch on a CPU — no GPU, no dataset
downloads required.

**Duration:** 3-4 hours
**Difficulty:** Intermediate
**Prerequisites:** Lectures 01-02

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Describe** the 7-step SGD process and explain what each step does.
2. **Explain** gradient descent geometrically as stepping downhill on a loss
   surface, using the gradient as the local slope.
3. **Use** PyTorch autograd — `requires_grad_()`, `.backward()`, `.grad` —
   to compute gradients automatically.
4. **Justify** why gradients must be zeroed each iteration and what happens
   if you forget.
5. **Implement** a full training loop from scratch to fit a quadratic with
   mean squared error.
6. **Diagnose** learning-rate problems (divergence vs. slow convergence) and
   describe the learning-rate-finder idea.
7. **Transform** a linear model into a neural network by stacking linear
   layers with a ReLU nonlinearity, and state the universal approximation
   idea.
8. **Rebuild** the same model "the fastai/PyTorch way" using `nn.Linear`,
   `nn.Sequential`, and `nn.Parameter`, and connect it to MNIST 3s-vs-7s.

---

## Key Concepts

### 1. The 7-Step SGD Process

Every model in this course learns with the same loop. Memorize these seven
steps — everything else is detail.

1. **Initialize** the weights (parameters) to random values.
2. **Predict** — run the inputs through the model to get outputs.
3. **Compute the loss** — a single number measuring how wrong the
   predictions are.
4. **Compute the gradients** — how the loss would change if each weight
   changed slightly.
5. **Step** — update each weight a little in the direction that reduces the
   loss (opposite the gradient), scaled by the learning rate.
6. **Repeat** from step 2.
7. **Stop** — when the model is good enough, or you run out of time/patience.

```text
        ┌──────────────┐
        │ 1. init      │
        └──────┬───────┘
               ▼
  ┌────►┌──────────────┐
  │     │ 2. predict   │
  │     └──────┬───────┘
  │            ▼
  │     ┌──────────────┐
  │     │ 3. loss      │
  │     └──────┬───────┘
  │            ▼
  │     ┌──────────────┐
  │     │ 4. gradients │
  │     └──────┬───────┘
  │            ▼
  │     ┌──────────────┐
  │     │ 5. step      │
  │     └──────┬───────┘
  │  6. repeat │
  └────────────┘
               ▼  (7. stop when good enough)
```

The only "smart" step is #4 → #5: gradients tell us which way is downhill,
and the step walks us that way.

### 2. Gradient Descent Intuition

Think of the loss as a function of the parameters. Fix the data; vary a
weight, and the loss traces out a curve. We want the bottom of that curve.

The **gradient** is the slope of the loss with respect to a parameter. If the
slope is positive, increasing the weight increases the loss, so we should
*decrease* the weight — i.e. move **opposite** the gradient. How far we move
is controlled by the **learning rate** (`lr`).

```text
loss
  │\
  │ \        we are here
  │  \        ●  slope (gradient) > 0
  │   \      /   → move LEFT (decrease weight)
  │    \    /
  │     \  /
  │      \/ ← minimum (goal)
  └───────────────── weight
```

The update rule is the whole of "learning":

```python
# new_weight = old_weight - learning_rate * gradient
weight = weight - lr * weight.grad
```

Because the gradient points *uphill*, subtracting it walks us *downhill*.

### 3. Tensors, Rank, and Shape

A **tensor** is a multi-dimensional array of numbers — PyTorch's core data
type. Its **rank** is the number of dimensions; its **shape** is the size
along each dimension.

```python
import torch

scalar = torch.tensor(3.0)          # rank 0, shape ()
vector = torch.tensor([1., 2., 3.]) # rank 1, shape (3,)
matrix = torch.tensor([[1., 2.],    # rank 2, shape (2, 2)
                       [3., 4.]])

print(vector.shape)  # torch.Size([3])
print(matrix.ndim)   # 2  (the rank)
```

```text
rank 0        rank 1            rank 2
 3.0        [1, 2, 3]        [[1, 2],
scalar       vector           [3, 4]]
                              matrix
```

A batch of 64 MNIST images flattened to 784 pixels is a rank-2 tensor of
shape `(64, 784)`. Getting shapes right is most of the debugging in deep
learning.

### 4. Autograd: `requires_grad_`, `.backward()`, `.grad`

PyTorch computes gradients for you. Mark a tensor with
`requires_grad_()` and PyTorch records every operation on it. Call
`.backward()` on the final loss and PyTorch fills in `.grad` for every
tracked tensor.

```python
import torch

# A parameter we want to optimize
x = torch.tensor(3.0).requires_grad_()

# Some computation ending in a single scalar
y = x ** 2                 # y = x^2
y.backward()               # compute dy/dx and store in x.grad

print(x.grad)              # tensor(6.)  because dy/dx = 2x = 2*3 = 6
```

```text
   forward  ─────────────►
   x=3  →  x**2  →  y=9
   ◄───────────── backward
   x.grad = 6   (dy/dx at x=3)
```

`.backward()` performs **backpropagation**: the chain rule applied
mechanically backward through the recorded operations.

### 5. Why You Must Zero the Gradients

PyTorch **accumulates** gradients into `.grad` — each `.backward()` *adds*
to whatever is already there. That is useful in a few advanced cases but is a
bug in the normal loop: on iteration 2 you would be using the sum of
iteration 1 and 2's gradients. So after stepping, reset with `grad.zero_()`.

```python
# after using the gradient to take a step:
weights.grad.zero_()   # in-place reset to zero (note trailing underscore)
```

```text
WITHOUT zero_():  grad = g1, then g1+g2, then g1+g2+g3 ...  (wrong)
WITH    zero_():  grad = g1, then g2,    then g3        ...  (correct)
```

Trailing-underscore methods in PyTorch (`zero_`, `requires_grad_`,
`add_`) mutate the tensor **in place**.

### 6. Mean Squared Error and the Loss Function

A **loss function** turns "how wrong are we?" into a single differentiable
number. For regression, **mean squared error (MSE)** is the standard choice:
average the squared differences between predictions and targets.

```python
def mse(preds: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
    return ((preds - targets) ** 2).mean()
```

Squaring makes all errors positive and punishes large errors more. It is
smooth, so its gradient is well-defined everywhere — exactly what SGD needs.
The loss must be a function whose gradient meaningfully points toward better
parameters, which is why we sometimes use a differentiable *surrogate* (like
MSE or cross-entropy) instead of the metric we actually care about (like
accuracy, which has zero gradient almost everywhere).

### 7. Learning Rate: Too High, Too Low, Just Right

The learning rate scales every step. Get it wrong and training fails in one
of two ways.

```text
lr too LOW           lr just RIGHT        lr too HIGH
   ●                    ●                     ●
    ●                    ●                   ↗   ↘
     ●                    ●                 ●       ● (diverges,
      ●                    ●               ↗   ↘       overshoots)
       ● (crawls)          ✓ (converges)  bounces out
```

- **Too low:** loss creeps down; training wastes time and may stall.
- **Too high:** steps overshoot the minimum; loss oscillates or explodes to
  `nan`.

The fast.ai **learning-rate finder** (`lr_find`) automates the search: it
starts with a tiny `lr` and increases it exponentially over a few mini-batches,
plotting loss vs. `lr`. You pick a rate on the steepest downslope, about one
order of magnitude before the loss bottoms out and starts climbing.

### 8. From a Linear Function to a Neural Net (ReLU)

A single linear layer computes `y = x @ w + b` — a weighted sum plus a
**bias**. Stacking two linear layers gains nothing: the composition of linear
functions is still linear. The magic ingredient is a **nonlinearity** between
them. The simplest is **ReLU** (Rectified Linear Unit): `max(x, 0)`.

```python
def relu(x: torch.Tensor) -> torch.Tensor:
    return x.clamp(min=0)          # same as torch.max(x, tensor(0.))

# A tiny neural net: linear -> relu -> linear
def simple_net(xb, w1, b1, w2, b2):
    l1 = xb @ w1 + b1              # linear layer 1
    l2 = relu(l1)                  # nonlinearity
    return l2 @ w2 + b2            # linear layer 2
```

```text
       w1,b1        ReLU         w2,b2
 x ──► linear ──► max(·,0) ──► linear ──► ŷ
       (learned)   (fixed)     (learned)
```

**Universal approximation:** with enough hidden units, a network of linear
layers separated by nonlinearities can approximate *any* continuous function
to arbitrary accuracy. ReLU is the kink that lets stacked lines bend into
curves. SGD is what finds the weights that make the bending fit your data.

---

## Code Examples

### Example 1: Fit a Quadratic with SGD (by hand)

A roller-coaster's speed over time follows a quadratic. We only observe noisy
measurements and want to recover the curve `a*t^2 + b*t + c`.

```python
import torch

torch.manual_seed(42)

# --- Synthetic "roller-coaster speed vs time" data -----------------------
time = torch.arange(0, 20, 1).float()                 # t = 0..19
true_a, true_b, true_c = 1.0, -15.0, 60.0
speed = true_a * time**2 + true_b * time + true_c
speed += 5 * torch.randn(len(time))                   # add measurement noise

# --- The model: a quadratic parameterised by (a, b, c) -------------------
def f(t: torch.Tensor, params: torch.Tensor) -> torch.Tensor:
    a, b, c = params
    return a * t**2 + b * t + c

def mse(preds: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
    return ((preds - targets) ** 2).mean()

# STEP 1: initialise parameters randomly, and track gradients
params = torch.randn(3).requires_grad_()
lr = 1e-5

def apply_step(params: torch.Tensor, show: bool = True) -> torch.Tensor:
    preds = f(time, params)          # STEP 2: predict
    loss = mse(preds, speed)         # STEP 3: compute loss
    loss.backward()                  # STEP 4: compute gradients
    with torch.no_grad():            # don't track the update itself
        params -= lr * params.grad   # STEP 5: step (downhill)
    params.grad.zero_()              # reset grads for next iteration
    if show:
        print(f"loss = {loss.item():.2f}")
    return params

# STEP 6: repeat
for _ in range(10):
    params = apply_step(params)
# STEP 7: stop — params now approximate (true_a, true_b, true_c)
print("learned params:", params.detach())
```

### Example 2: A Neural Net from Scratch on Toy Data

Same 7-step loop, but the model is now `linear -> ReLU -> linear`. This is
the smallest thing that is genuinely a "neural net."

```python
import torch

torch.manual_seed(0)

# Toy regression: y is a nonlinear function of a single input feature.
x = torch.linspace(-3, 3, 100).unsqueeze(1)   # shape (100, 1)
y = x**2 + torch.randn_like(x) * 0.3          # target is a parabola

n_hidden = 30

def init_params(size, std=1.0):
    return (torch.randn(size) * std).requires_grad_()

# Two linear layers with a ReLU between them.
w1 = init_params((1, n_hidden))
b1 = init_params(n_hidden)
w2 = init_params((n_hidden, 1))
b2 = init_params(1)
params = [w1, b1, w2, b2]

def relu(t): return t.clamp(min=0)

def model(xb):
    h = relu(xb @ w1 + b1)     # hidden layer with nonlinearity
    return h @ w2 + b2         # output layer

lr = 1e-2
for epoch in range(2000):
    preds = model(x)
    loss = ((preds - y) ** 2).mean()   # MSE
    loss.backward()
    with torch.no_grad():
        for p in params:
            p -= lr * p.grad           # step every parameter
            p.grad.zero_()             # then zero its gradient
    if epoch % 400 == 0:
        print(f"epoch {epoch:4d}  loss {loss.item():.4f}")

# The net has learned to bend two lines into a parabola.
```

### Example 3: The Same Net "the PyTorch/fastai Way" (MNIST 3s vs 7s)

By hand you manage every `w` and `b`. PyTorch's `nn` module packages a layer's
weights and bias into a module and registers them as `nn.Parameter` so an
optimizer can find them. This is exactly what fastai's `Learner` uses under
the hood for the canonical **3s-vs-7s** classifier.

```python
import torch
from torch import nn

torch.manual_seed(0)

# --- Stand-in for the real MNIST 3/7 data --------------------------------
# Real data: 28x28 grayscale images flattened to 784 pixels, label 0=three,
# 1=seven. Here we fabricate the SAME SHAPES so the code runs with no
# download: (n, 784) inputs, (n, 1) targets.
n = 256
train_x = torch.randn(n, 28 * 28)          # shape (256, 784)
train_y = (train_x.mean(dim=1, keepdim=True) > 0).float()  # fake 3-vs-7 label

# --- Baseline before learning: "pixel similarity" -------------------------
# fast.ai first shows a non-learned baseline: classify each image by whether
# it is closer to the AVERAGE 3 or the AVERAGE 7 (mean absolute pixel diff).
# A learned classifier should beat this simple baseline.

# --- The learned model: nn.Sequential of linear layers + ReLU -------------
model = nn.Sequential(
    nn.Linear(28 * 28, 30),   # weights + bias registered as nn.Parameter
    nn.ReLU(),
    nn.Linear(30, 1),
)

def batch_accuracy(preds, yb):
    correct = (preds.sigmoid() > 0.5) == (yb > 0.5)   # sigmoid -> probability
    return correct.float().mean()

opt = torch.optim.SGD(model.parameters(), lr=0.1)   # SGD over all params
loss_fn = nn.MSELoss()

for epoch in range(20):
    preds = model(train_x)
    loss = loss_fn(preds.sigmoid(), train_y)   # squash to [0,1] then compare
    loss.backward()
    opt.step()       # STEP 5: update every parameter
    opt.zero_grad()  # zero grads (opt wraps grad.zero_() for you)
    if epoch % 5 == 0:
        acc = batch_accuracy(model(train_x), train_y)
        print(f"epoch {epoch:2d}  loss {loss.item():.4f}  acc {acc.item():.3f}")
```

---

## Common Mistakes to Avoid

```python
# ❌ BAD: forgetting to zero the gradients — they accumulate across steps
for epoch in range(n):
    loss = mse(model(x), y)
    loss.backward()
    with torch.no_grad():
        params -= lr * params.grad   # grad still holds ALL previous grads!

# ✅ GOOD: zero the gradient after every step
for epoch in range(n):
    loss = mse(model(x), y)
    loss.backward()
    with torch.no_grad():
        params -= lr * params.grad
    params.grad.zero_()              # reset before the next backward()
```

```python
# ❌ BAD: updating parameters inside autograd tracking — corrupts the graph
loss.backward()
params -= lr * params.grad           # RuntimeError: a leaf Variable ...

# ✅ GOOD: wrap the in-place update in torch.no_grad()
loss.backward()
with torch.no_grad():
    params -= lr * params.grad       # update is not itself recorded
```

```python
# ❌ BAD: stacking linear layers with no nonlinearity — still just linear
def net(x):
    return (x @ w1 + b1) @ w2 + b2   # collapses to one linear layer

# ✅ GOOD: insert a nonlinearity so the net can model curves
def net(x):
    return relu(x @ w1 + b1) @ w2 + b2
```

---

## Best Practices

1. **Learn the 7 steps cold** — every model you meet is a variation on
   init → predict → loss → gradients → step → repeat → stop.
2. **Always zero gradients** each iteration (`grad.zero_()` or
   `opt.zero_grad()`); accumulation is a bug in the standard loop.
3. **Wrap parameter updates in `torch.no_grad()`** so the update is not
   recorded by autograd.
4. **Detach for reporting** (`loss.item()`, `tensor.detach()`) to avoid
   holding onto the computation graph or accidentally tracking gradients.
5. **Watch the loss go down.** If it is flat, `lr` is likely too low; if it
   oscillates or hits `nan`, `lr` is too high.
6. **Use a learning-rate finder** rather than guessing; pick a rate on the
   steep part of the curve.
7. **Print and check shapes** early — most bugs are shape mismatches, not
   math errors.
8. **Set a manual seed** (`torch.manual_seed`) while developing so runs are
   reproducible.
9. **Prefer `nn.Linear` / `nn.Sequential` / an optimizer** over hand-rolled
   parameters for anything beyond learning exercises.
10. **Establish a simple baseline first** (like pixel similarity) so you can
    tell whether the learned model is actually adding value.

---

## Practice Exercises

1. **Trace the gradient.** For `y = 3 * x**2` at `x = 2`, compute `x.grad` by
   hand, then verify with `requires_grad_()` and `.backward()`.
2. **Break it, then fix it.** Take the quadratic-fitting loop and remove
   `params.grad.zero_()`. Explain what happens to the loss, then restore it.
3. **Sweep the learning rate.** Run the quadratic fit with `lr` set to
   `1e-7`, `1e-5`, and `1e-2`. Describe divergence vs. slow convergence.
4. **Add a nonlinearity.** Start from a two-layer *linear* net that fails to
   fit a parabola; insert a ReLU and show it now fits.
5. **Rewrite by hand → PyTorch.** Convert the from-scratch neural net
   (Example 2) to use `nn.Sequential` and `torch.optim.SGD`, and confirm you
   get a comparable final loss.

---

## Summary

1. Models learn by **SGD**: initialize, predict, compute loss, compute
   gradients, step opposite the gradient, repeat, stop.
2. The **gradient** is the slope of the loss with respect to each parameter;
   the **learning rate** scales how far we step downhill.
3. PyTorch **autograd** (`requires_grad_`, `.backward()`, `.grad`) computes
   gradients automatically via backpropagation; you must **zero** them each
   iteration.
4. A **loss function** like **MSE** turns errors into one differentiable
   number that SGD can minimize.
5. A **linear layer** plus a **nonlinearity** (ReLU) is the atom of a neural
   net; stacked, they can approximate any continuous function.
6. `nn.Linear`, `nn.Sequential`, and `nn.Parameter` package this cleanly —
   the same machinery fastai uses for the MNIST 3s-vs-7s classifier.

**Next lecture:** [Lecture 04: Natural Language (NLP)](04-nlp-lecture.md) —
tokenization, numericalization, and fine-tuning a pretrained transformer.
