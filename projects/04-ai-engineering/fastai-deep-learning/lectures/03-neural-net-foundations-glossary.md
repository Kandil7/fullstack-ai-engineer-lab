# Glossary: Neural Net Foundations (SGD)

## Quick Reference Table

| Term | One-Line Definition |
|------|---------------------|
| SGD | Stochastic Gradient Descent — the 7-step loop that trains models |
| Gradient | Slope of the loss with respect to a parameter |
| Learning rate | Scalar that scales the size of each SGD step |
| Loss function | Differentiable measure of how wrong predictions are |
| MSE | Mean squared error — average of squared prediction errors |
| Parameter / weight | A learnable number the model adjusts during training |
| Bias | A learnable offset added after the weighted sum |
| Activation | A layer's output value(s) |
| ReLU | Rectified Linear Unit — `max(x, 0)` nonlinearity |
| Sigmoid | Squashes any real number into the range (0, 1) |
| `requires_grad` | Flag telling PyTorch to track a tensor for gradients |
| Backpropagation | Chain-rule pass that computes gradients backward |
| `zero_grad` | Resetting accumulated gradients before the next step |
| Epoch | One full pass over the training data |
| Mini-batch | A small subset of data used for one SGD step |
| Tensor rank/shape | Number of dimensions / size along each dimension |

---

## Detailed Definitions

### SGD (Stochastic Gradient Descent)

**Definition:** The optimization algorithm at the heart of deep learning. It
repeatedly computes the gradient of the loss on a mini-batch and steps the
parameters a small amount opposite the gradient. "Stochastic" means each step
uses a random subset (mini-batch) of the data rather than all of it.

## Example
```python
opt = torch.optim.SGD(model.parameters(), lr=0.1)
for xb, yb in dataloader:
    loss = loss_fn(model(xb), yb)
    loss.backward()   # gradients
    opt.step()        # step opposite the gradient
    opt.zero_grad()   # reset for next step
```

**Related Terms:** Gradient, Learning rate, Mini-batch, Epoch

- The 7 steps: init, predict, loss, gradients, step, repeat, stop.
- Full-batch gradient descent uses all data per step; SGD uses batches.

---

### Gradient

**Definition:** The derivative of the loss with respect to a parameter — the
local slope of the loss surface. Its sign says which direction increases the
loss; SGD steps in the opposite direction.

## Example
```python
x = torch.tensor(3.0).requires_grad_()
y = x ** 2
y.backward()
print(x.grad)   # tensor(6.)  because d(x^2)/dx = 2x = 6
```

**Related Terms:** Backpropagation, Learning rate, `requires_grad`

- Stored in `tensor.grad` after `.backward()`.
- Points uphill, so we subtract it to descend.

---

### Learning Rate

**Definition:** A scalar hyperparameter (`lr`) that scales how far each SGD
step moves the parameters. Too high diverges; too low crawls.

## Example
```python
lr = 1e-2
with torch.no_grad():
    params -= lr * params.grad   # step size = lr * gradient
```

**Related Terms:** SGD, Gradient, Learning-rate finder

- fast.ai's `lr_find` sweeps `lr` and plots loss to pick a good value.
- Pick a rate on the steep downslope, before the loss bottoms out.

---

### Loss Function

**Definition:** A differentiable function that maps predictions and targets to
a single number measuring wrongness. SGD minimizes it. It is often a surrogate
for the true metric (e.g. MSE or cross-entropy standing in for accuracy).

## Example
```python
def mse(preds, targets):
    return ((preds - targets) ** 2).mean()
```

**Related Terms:** MSE, Sigmoid, Gradient

- Must have a useful gradient; accuracy is flat and unusable as a loss.

---

### MSE (Mean Squared Error)

**Definition:** The average of the squared differences between predictions and
targets. The standard regression loss: smooth, always positive, and it
penalizes large errors more heavily.

## Example
```python
loss = ((preds - targets) ** 2).mean()
# or:
loss = torch.nn.functional.mse_loss(preds, targets)
```

**Related Terms:** Loss function, Gradient

- Squaring makes errors positive and differentiable everywhere.

---

### Parameter / Weight

**Definition:** A learnable number inside the model, adjusted by SGD to reduce
the loss. In `nn` modules these are wrapped as `nn.Parameter` so optimizers
can find them via `model.parameters()`.

## Example
```python
layer = torch.nn.Linear(784, 30)
print(layer.weight.shape)  # torch.Size([30, 784])
print(list(layer.parameters()))  # weight + bias, both nn.Parameter
```

**Related Terms:** Bias, `requires_grad`, SGD

- `nn.Parameter` tensors automatically have `requires_grad=True`.

---

### Bias

**Definition:** A learnable offset added after the weighted sum in a linear
layer: `y = x @ w + b`. It lets a layer shift its output up or down
independent of the inputs.

## Example
```python
w = torch.randn(3, 1).requires_grad_()
b = torch.zeros(1).requires_grad_()
y = x @ w + b   # b is the bias term
```

**Related Terms:** Parameter / weight, Activation

- Without a bias, every layer output is forced through the origin.

---

### Activation

**Definition:** The output value(s) produced by a layer — the numbers flowing
between layers. "Activations" is the running result of the forward pass, as
opposed to "parameters" which are the learned weights.

## Example
```python
h = relu(x @ w1 + b1)   # h holds the hidden-layer activations
```

**Related Terms:** ReLU, Parameter / weight

- Distinguish activations (data-dependent) from parameters (learned).

---

### ReLU (Rectified Linear Unit)

**Definition:** The nonlinearity `max(x, 0)` — it passes positive values
through unchanged and clamps negatives to zero. Placing it between linear
layers lets a network model curves, not just straight lines.

## Example
```python
def relu(t):
    return t.clamp(min=0)   # or torch.nn.functional.relu(t)
```

**Related Terms:** Activation, Universal approximation, Bias

- Cheap to compute; its "kink" is what bends stacked lines into curves.

---

### Sigmoid

**Definition:** The function `1 / (1 + e^-x)` that squashes any real number
into `(0, 1)`. Used to turn a raw model output into something interpretable as
a probability, e.g. for binary classification like 3-vs-7.

## Example
```python
probs = preds.sigmoid()   # map raw outputs to (0, 1)
pred_class = probs > 0.5
```

**Related Terms:** Loss function, Activation

- Monotonic and smooth, so it has a well-defined gradient.

---

### `requires_grad`

**Definition:** A tensor flag that tells PyTorch to record operations on that
tensor so it can compute gradients during `.backward()`. Set it with the
in-place `requires_grad_()` method.

## Example
```python
params = torch.randn(3).requires_grad_()   # now tracked by autograd
```

**Related Terms:** Backpropagation, Gradient, `zero_grad`

- `nn.Parameter` tensors have this set automatically.

---

### Backpropagation / `.backward()`

**Definition:** The process of computing gradients by applying the chain rule
backward through the recorded operations. Calling `.backward()` on the scalar
loss fills in `.grad` for every tensor with `requires_grad=True`.

## Example
```python
loss = mse(model(x), y)
loss.backward()          # backprop: fills param.grad for all params
```

**Related Terms:** Gradient, `requires_grad`, `zero_grad`

- Must be called on a scalar (single-number) tensor.

---

### `zero_grad` / `grad.zero_()`

**Definition:** Resetting accumulated gradients to zero before the next
backward pass. PyTorch *adds* to `.grad` on each `.backward()`, so failing to
zero it mixes gradients from previous steps.

## Example
```python
params.grad.zero_()   # by hand
# or, with an optimizer:
opt.zero_grad()
```

**Related Terms:** Backpropagation, SGD, Gradient

- The trailing underscore means the operation mutates in place.

---

### Epoch

**Definition:** One complete pass over the entire training dataset. Training
usually runs for many epochs; within each epoch the data is split into
mini-batches.

## Example
```python
for epoch in range(10):
    for xb, yb in dataloader:   # one pass = one epoch
        ...
```

**Related Terms:** Mini-batch, SGD

- More epochs = more learning, up to the point of overfitting.

---

### Mini-batch

**Definition:** A small subset of the training data used to compute one SGD
step. Batching gives more stable gradients than single examples while being
far cheaper (and more parallel) than using the whole dataset at once.

## Example
```python
batch_size = 64
for i in range(0, len(x), batch_size):
    xb = x[i:i + batch_size]      # one mini-batch
    yb = y[i:i + batch_size]
```

**Related Terms:** SGD, Epoch

- Batch size trades gradient noise against memory and speed.

---

### Tensor Rank / Shape

**Definition:** A **tensor** is a multi-dimensional array. Its **rank** is the
number of dimensions (`ndim`); its **shape** is the size along each dimension.
Correct shapes are essential for matrix multiplication in layers.

## Example
```python
x = torch.randn(64, 784)
print(x.ndim)    # 2   (rank)
print(x.shape)   # torch.Size([64, 784])  (batch of 64, 784 pixels each)
```

**Related Terms:** Parameter / weight, Activation

- Most deep-learning bugs are shape mismatches, not math errors.

---

## Summary

SGD is the engine: it uses **gradients** (computed by **backpropagation**
through tensors marked `requires_grad`) to step **parameters** downhill on a
**loss function** like **MSE**, scaled by the **learning rate**, zeroing
gradients each iteration. Stacking **linear** layers (weights + **bias**) with
a **ReLU** nonlinearity turns a linear model into a neural net capable of
approximating any function, trained batch-by-batch across **epochs**.

**Next:** See [Lecture 04: Natural Language (NLP)](04-nlp-lecture.md) for
tokenization, numericalization, and fine-tuning pretrained transformers.
