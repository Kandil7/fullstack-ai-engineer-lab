# Glossary: From-Scratch Model

Key terms for building a linear model and neural network from tensors, using
the Titanic dataset with pure `torch` and `pandas`.

---

## Quick Reference Table

| Term | One-line definition |
|------|---------------------|
| Tensor | A multi-dimensional array; the core data structure of PyTorch. |
| Matrix multiplication | `A @ B`; the dot-product operation at the heart of every layer. |
| Broadcasting | Automatic stretching of compatible shapes so element-wise ops work without loops. |
| Dummy variable / one-hot | Encoding a category as its own 0/1 column via `pd.get_dummies`. |
| Normalization | Rescaling each column so no feature dominates by magnitude. |
| Log transform | Applying `log1p` to compress a long-tailed, skewed column. |
| Sigmoid | `1/(1+e^-z)`; squashes any real number into `(0, 1)`. |
| Coefficient / weight | A learnable parameter multiplied against an input feature. |
| Initialization | Choosing starting parameter values (e.g. `rand()-0.5`, fan-in scaling). |
| Hidden layer | An intermediate layer of neurons between input and output. |
| ReLU | `max(0, x)`; the nonlinearity that gives depth its power. |
| Layer | One linear map (`@`) optionally followed by a nonlinearity. |
| Deep vs shallow net | More stacked layers (deep) vs one/none (shallow). |
| Loss (binary) | Scalar error between predicted probability and 0/1 label. |
| Gradient step | Updating parameters by `param -= grad * lr`. |
| Epoch | One full pass computing loss and updating over the training data. |

---

## Detailed Definitions

### Tensor
A multi-dimensional numeric array and PyTorch's fundamental type. Inputs,
coefficients, activations, and gradients are all tensors. Created here with
`torch.tensor(df[cols].values, dtype=torch.float)`. Calling
`.requires_grad_()` tells autograd to track operations for backpropagation.

### Matrix Multiplication
The operation `A @ B`: for `(N, C) @ (C, H)` the shared inner dimension `C` is
summed over, producing `(N, H)`. Every layer's forward pass is a matrix
multiply. `(indeps * coeffs).sum(axis=1)` is the same as `indeps @ coeffs` for a
1-D coefficient vector.

### Broadcasting
PyTorch's rule for combining tensors of different shapes without explicit loops.
Shapes are aligned from the right; a dimension of size 1 (or absent) is
stretched to match. `indeps (N, C) * coeffs (C,)` broadcasts `coeffs` across all
`N` rows. Broadcasting avoids slow Python loops and keeps code vectorized.

### Dummy Variable / One-Hot Encoding
Turning a categorical column into numeric 0/1 columns, one per category, using
`pd.get_dummies(df, columns=[...])`. `Sex` becomes `Sex_male` and `Sex_female`.
Required because a model multiplies numbers and cannot consume raw strings.
Avoids falsely implying an ordering that a single integer column would.

### Normalization
Rescaling each input column to a comparable range, e.g. `t / t.max(dim=0)`.
Without it, a large-magnitude column (`Age` 0-80) dominates a 0/1 dummy, so the
model effectively ignores the small-scale features and gradient descent is
poorly conditioned.

### Log Transform
Applying `torch.log1p(x) = log(1 + x)` to a skewed, long-tailed column such as
`Fare`. Compresses extreme values so a few large fares don't dominate, and
`log1p` (unlike `log`) safely maps `0` to `0` instead of `-inf`.

### Sigmoid
The function `sigmoid(z) = 1 / (1 + e^-z)`, mapping any real number into the
open interval `(0, 1)`. Used as the final activation so the model output reads
as a probability. `z=0` gives `0.5`; large positive/negative `z` saturates near
`1`/`0`.

### Coefficient / Weight
A learnable parameter multiplied against an input feature. In the linear model
there is one coefficient per column; in a neural net, weights form matrices
(`l1`, `l2`). Initialized small and centered on zero, then updated by gradient
descent.

### Initialization
Choosing starting values for parameters. Here: `torch.rand(n) - 0.5` centers a
linear model's coefficients on zero. For deep nets, each layer's random init is
divided by its fan-in (`/ n_hidden`) so activations and gradients neither
explode nor vanish with depth — the manual version of Kaiming/Xavier init.

### Hidden Layer
An intermediate layer of neurons sitting between the input and the output layer.
Adding one (`indeps @ l1` with `n_hidden` units) plus a ReLU is what turns a
linear model into a neural network capable of representing nonlinear patterns.

### ReLU (Rectified Linear Unit)
The nonlinearity `torch.relu(x) = max(0, x)`. Placed between linear layers, it
prevents the layers from collapsing into a single linear map, which is what lets
a multi-layer network learn nonlinear functions.

### Layer
One linear transformation (a matrix multiply, optionally plus a bias/constant),
usually followed by a nonlinearity. Chaining layers builds a network; the output
layer typically has a single unit for binary classification.

### Deep vs Shallow Net
A **shallow** net has zero or one hidden layer; a **deep** net stacks several
`(matmul -> ReLU)` blocks. Depth increases representational capacity but demands
careful initialization and gradient scaling to train stably.

### Loss (Binary)
A scalar measuring how wrong the model is on a binary target. Here it is the
mean absolute error `torch.abs(preds - deps).mean()` between the sigmoid
probability and the 0/1 label. Lower is better; `backward()` differentiates it
with respect to every coefficient.

### Gradient Step
The parameter update that moves downhill on the loss surface:
`coeffs.sub_(coeffs.grad * lr)` inside `torch.no_grad()`. The learning rate `lr`
scales the step. Gradients must be zeroed afterward (`coeffs.grad.zero_()`)
because PyTorch accumulates them by default.

### Epoch
One complete iteration of the training loop over the data: compute predictions,
compute loss, `backward()`, step the parameters, zero the gradients. Training
repeats for many epochs until the loss stops improving.

### Autograd / `backward()`
PyTorch's automatic differentiation engine. Calling `loss.backward()` walks the
computation graph and populates `.grad` on every tensor with `requires_grad=True`,
giving the derivative of the loss with respect to that tensor.

### `torch.no_grad()`
A context manager that disables gradient tracking. The parameter update is
wrapped in it so the step itself is not recorded as part of the graph, avoiding
incorrect gradients and unnecessary memory use.

---

## Summary

These terms cover the full from-scratch pipeline: shape data into normalized
tensors, initialize coefficients, run the forward pass as a matrix multiply
through a sigmoid, measure a binary loss, and step downhill with autograd —
then generalize the forward pass into hidden layers and ReLUs to form a neural
net. Master these and the `Learner` abstraction stops being magic.

**Next:** See Lecture 06 — Random Forests & Tabular for a non-gradient approach
to the same kind of tabular problem.
