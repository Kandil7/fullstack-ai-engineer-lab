# Lecture 05: From-Scratch Model

## Topic Overview

fast.ai lesson 5 takes the Titanic dataset and builds a working model **from
nothing but tensors** — no `Learner`, no `nn.Linear`, no optimizer. You clean
the data by hand, initialize coefficients with `torch.rand()`, write the
forward pass as a matrix multiply, define the loss, and step the coefficients
downhill yourself. Then you reframe the exact same code as a **neural network**
by adding a hidden layer and a ReLU, and finally stack layers into a deep net.
By the end you understand that a `Learner` is just this loop with the sharp
edges filed off.

**Duration:** 3-4 hours
**Difficulty:** Intermediate
**Prerequisites:** Lectures 01-03

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Prepare** tabular data from scratch: impute missing values, log-transform
   skewed columns, one-hot encode categoricals, and normalize.
2. **Explain** why normalization matters so no single column dominates the loss.
3. **Initialize** model coefficients as random tensors centered on zero.
4. **Implement** a linear model as `inputs @ coeffs` followed by a `sigmoid`.
5. **Write** a training loop by hand: predictions, loss, gradients, step.
6. **Extend** the linear model into a one-hidden-layer neural net with ReLU.
7. **Stack** layers into a deep net and manage initialization and gradient scale.
8. **Connect** every piece back to what `fastai`/`Learner` automates for you.

---

## Key Concepts

### 1. Data Prep From Scratch

Real tabular data is messy. Before any math, you fix three problems: missing
values, skewed distributions, and non-numeric categories.

```python
import torch
import pandas as pd

df = pd.read_csv("train.csv")

# 1. Missing values -> fill with mode (categorical) or median (numeric)
modes = df.mode().iloc[0]
df["Age"] = df["Age"].fillna(df["Age"].median())
df = df.fillna(modes)

# 2. Skewed column (Fare) -> log1p compresses the long tail
df["LogFare"] = torch.log1p(torch.tensor(df["Fare"].values))
```

`log1p(x) = log(1 + x)` is used instead of `log(x)` so that a fare of `0`
maps to `0` instead of `-inf`.

### 2. Dummy Variables (One-Hot Encoding)

A model multiplies numbers, so a column like `Sex` (`"male"`/`"female"`) or
`Pclass` (1/2/3) must become numeric. `pd.get_dummies` turns each category
into its own 0/1 column.

```python
df = pd.get_dummies(df, columns=["Sex", "Pclass", "Embarked"])
# Sex -> Sex_male, Sex_female
# Pclass -> Pclass_1, Pclass_2, Pclass_3
```

```
"male"   -> [Sex_male=1, Sex_female=0]
"female" -> [Sex_male=0, Sex_female=1]
Pclass 2 -> [Pclass_1=0, Pclass_2=1, Pclass_3=0]
```

Do NOT encode an ordinal integer as a single magnitude column unless the
ordering is genuinely linear — the model would assume class 3 is "three times"
class 1.

### 3. Normalization

Columns live on wildly different scales: `Age` spans 0-80, a dummy is 0-1,
`LogFare` maybe 0-6. If you multiply raw columns by random coefficients, the
big-magnitude columns swamp everything and dominate the gradient. Normalize
each column so they contribute comparably.

```python
t = torch.tensor(df[indep_cols].values, dtype=torch.float)
# divide each column by its max -> everything in [0, 1]
t = t / t.max(dim=0).values
```

```
BEFORE            AFTER (col / col.max)
Age    LogFare    Age    LogFare
22.0   2.11       0.27   0.35
38.0   4.28       0.48   0.71
```

### 4. A Linear Model From Scratch

Coefficients start as small random numbers centered on zero. The prediction is
a matrix multiply of inputs by coefficients, squashed through a sigmoid into a
probability.

```python
torch.manual_seed(442)
n_coeff = t.shape[1]
coeffs = torch.rand(n_coeff) - 0.5      # centered on 0, in [-0.5, 0.5]
coeffs.requires_grad_()

def calc_preds(coeffs, indeps):
    return torch.sigmoid((indeps * coeffs).sum(axis=1))
```

`(indeps * coeffs).sum(axis=1)` is a dot product per row — the same as
`indeps @ coeffs`. `sigmoid` maps any real number to `(0, 1)`:

```
sigmoid(z) = 1 / (1 + e^-z)
z -> -inf : 0      z = 0 : 0.5      z -> +inf : 1
```

### 5. Binary Loss and the Gradient Step

For a binary target (survived / didn't), a simple **mean absolute error**
between the predicted probability and the 0/1 label works and is easy to reason
about.

```python
def calc_loss(coeffs, indeps, deps):
    return torch.abs(calc_preds(coeffs, indeps) - deps).mean()

loss = calc_loss(coeffs, trn_indep, trn_dep)
loss.backward()                 # fills coeffs.grad

with torch.no_grad():
    coeffs.sub_(coeffs.grad * lr)   # step downhill
    coeffs.grad.zero_()             # reset for next epoch
```

`loss.backward()` computes `d(loss)/d(coeff)` for every coefficient.
`coeffs.sub_(coeffs.grad * lr)` moves each coefficient a small step in the
direction that reduces loss. **Zeroing the gradient** afterward is mandatory —
PyTorch accumulates gradients otherwise.

### 6. Matrix Multiplication and Broadcasting

Matrix multiplication `@` is THE core operation of deep learning. For a batch
of `N` rows with `C` features and a weight matrix of shape `(C, H)`:

```
(N, C) @ (C, H) -> (N, H)
   inner dims (C) must match; outer dims become the result shape
```

**Broadcasting** lets you combine tensors of different-but-compatible shapes
without writing loops. `(indeps * coeffs)` above works because `coeffs` of
shape `(C,)` is stretched across all `N` rows of `indeps` `(N, C)`:

```
(N, C) * (C,)  ->  (C,) is broadcast to (N, C)  ->  (N, C)
Rule: align shapes from the RIGHT; a dim of size 1 (or missing) stretches.
```

### 7. From Linear Model to Neural Net

A neural net is a linear layer, a nonlinearity, then more linear layers. Insert
a **hidden layer** of `n_hidden` neurons and a **ReLU** (`max(0, x)`) between
two matrix multiplies.

```python
def init_coeffs(n_hidden=20):
    l1 = (torch.rand(n_coeff, n_hidden) - 0.5) / n_hidden
    l2 = torch.rand(n_hidden, 1) - 0.3
    const = torch.rand(1)[0]
    return l1.requires_grad_(), l2.requires_grad_(), const.requires_grad_()

def calc_preds(coeffs, indeps):
    l1, l2, const = coeffs
    res = torch.relu(indeps @ l1)      # hidden layer + nonlinearity
    res = res @ l2 + const             # output layer
    return torch.sigmoid(res)
```

```
inputs (N,C) --@ l1--> (N,H) --relu--> (N,H) --@ l2--> (N,1) --sigmoid--> preds
```

Without the ReLU, two stacked matrix multiplies collapse into a single linear
map — the nonlinearity is what gives depth its power.

### 8. Deep vs Shallow, and Scaling Gradients

A **deep net** simply chains more `(matmul -> ReLU)` blocks. The catch is
initialization: naive random weights make activations (and therefore gradients)
grow or shrink exponentially with depth. Dividing each layer's init by its
fan-in (`/ n_hidden`) keeps the signal at a sane scale.

```python
def init_coeffs():
    hiddens = [10, 10]                 # two hidden layers -> "deep"
    sizes = [n_coeff] + hiddens + [1]
    n = len(sizes)
    layers = [(torch.rand(sizes[i], sizes[i+1]) - 0.3) / sizes[i+1] * 4
              for i in range(n - 1)]
    consts = [(torch.rand(1)[0] - 0.5) * 0.1 for _ in range(n - 1)]
    for layer in layers + consts:
        layer.requires_grad_()
    return layers, consts
```

This is exactly the machinery `nn.Linear` and `Kaiming` init hide from you.

---

## Code Examples

### Example 1: The Full From-Scratch Training Loop

```python
import torch
import pandas as pd

def prep_data(df: pd.DataFrame, indep_cols: list[str], dep_col: str
              ) -> tuple[torch.Tensor, torch.Tensor]:
    """Impute, dummy-encode, tensorize, and normalize."""
    df = df.copy()
    df = df.fillna(df.mode().iloc[0])
    indeps = torch.tensor(df[indep_cols].values, dtype=torch.float)
    indeps = indeps / indeps.max(dim=0).values      # normalize columns
    deps = torch.tensor(df[dep_col].values, dtype=torch.float)
    return indeps, deps

def calc_preds(coeffs: torch.Tensor, indeps: torch.Tensor) -> torch.Tensor:
    return torch.sigmoid((indeps * coeffs).sum(axis=1))

def calc_loss(coeffs: torch.Tensor, indeps: torch.Tensor,
              deps: torch.Tensor) -> torch.Tensor:
    return torch.abs(calc_preds(coeffs, indeps) - deps).mean()

def one_epoch(coeffs: torch.Tensor, indeps: torch.Tensor,
              deps: torch.Tensor, lr: float) -> None:
    loss = calc_loss(coeffs, indeps, deps)
    loss.backward()
    with torch.no_grad():
        coeffs.sub_(coeffs.grad * lr)
        coeffs.grad.zero_()
    print(f"loss: {loss:.3f}", end="; ")

def train(indeps: torch.Tensor, deps: torch.Tensor,
          epochs: int = 30, lr: float = 2.0) -> torch.Tensor:
    torch.manual_seed(442)
    coeffs = (torch.rand(indeps.shape[1]) - 0.5).requires_grad_()
    for _ in range(epochs):
        one_epoch(coeffs, indeps, deps, lr)
    return coeffs
```

### Example 2: Measuring Accuracy Against a Threshold

```python
def accuracy(coeffs: torch.Tensor, indeps: torch.Tensor,
             deps: torch.Tensor) -> float:
    """Predictions > 0.5 count as 'survived'; compare to labels."""
    preds = calc_preds(coeffs, indeps)
    correct = (preds > 0.5) == deps.bool()
    return correct.float().mean().item()

# A hand-rolled linear model typically lands around 0.78-0.82 on Titanic —
# competitive with an untuned framework model, which is the whole point.
```

### Example 3: The Same Loop, Now a Neural Net

```python
def init_nn(n_coeff: int, n_hidden: int = 20) -> list[torch.Tensor]:
    l1 = ((torch.rand(n_coeff, n_hidden) - 0.5) / n_hidden).requires_grad_()
    l2 = (torch.rand(n_hidden, 1) - 0.3).requires_grad_()
    const = torch.rand(1).requires_grad_()
    return [l1, l2, const]

def nn_preds(coeffs: list[torch.Tensor], indeps: torch.Tensor) -> torch.Tensor:
    l1, l2, const = coeffs
    res = torch.relu(indeps @ l1)
    res = res @ l2 + const
    return torch.sigmoid(res.squeeze())

# Only calc_preds changed. The loss, the loop, backward(), and the step are
# identical to the linear model. That is the core insight of the lesson.
```

---

## Common Mistakes to Avoid

### Mistake 1: Forgetting to Zero Gradients

```python
# BAD: gradients accumulate across epochs -> steps get wildly too big
loss.backward()
with torch.no_grad():
    coeffs.sub_(coeffs.grad * lr)   # grad never reset!

# GOOD: reset after every step
loss.backward()
with torch.no_grad():
    coeffs.sub_(coeffs.grad * lr)
    coeffs.grad.zero_()
```

### Mistake 2: Skipping Normalization

```python
# BAD: raw Age (0-80) dominates a 0/1 dummy; the model effectively ignores Sex
indeps = torch.tensor(df[cols].values, dtype=torch.float)

# GOOD: scale every column to a comparable range first
indeps = indeps / indeps.max(dim=0).values
```

### Mistake 3: Stacking Linear Layers Without a Nonlinearity

```python
# BAD: two matmuls with no ReLU collapse to ONE linear map -> no extra power
res = indeps @ l1
res = res @ l2

# GOOD: a nonlinearity between layers is what makes it a neural net
res = torch.relu(indeps @ l1)
res = res @ l2
```

---

## Best Practices

1. **Set a seed** (`torch.manual_seed`) so from-scratch runs are reproducible.
2. **Center coefficients on zero** (`torch.rand(...) - 0.5`) so early gradients
   point in useful directions.
3. **Normalize every input column** before training, not after.
4. **Log-transform skewed money/count columns** with `log1p`.
5. **Use `log1p`, not `log`,** to survive zero values.
6. **Zero gradients** after every optimizer step.
7. **Wrap parameter updates in `torch.no_grad()`** so the step itself isn't
   tracked by autograd.
8. **Divide layer inits by fan-in** to keep activations and gradients stable.
9. **Insert a ReLU between every pair of linear layers.**
10. **Change only `calc_preds`** when upgrading linear -> shallow -> deep; keep
    the loss and loop fixed so you can isolate what improved.

---

## Practice Exercises

1. Load Titanic, impute `Age` with the median and `Embarked` with the mode, and
   one-hot encode `Sex`, `Pclass`, and `Embarked`. Print the final tensor shape.
2. Implement `calc_preds`, `calc_loss`, and `one_epoch` for the linear model and
   train for 30 epochs. Report validation accuracy.
3. Replace `Fare` with `log1p(Fare)` and re-normalize. Does accuracy change?
4. Add a single hidden layer of 20 neurons + ReLU. Change ONLY `calc_preds` and
   the initializer; keep the loop identical. Compare accuracy to the linear run.
5. Stack two hidden layers into a deep net. Experiment with dividing the init by
   fan-in versus not, and observe the effect on the loss curve.

---

## Summary

You built a complete model with nothing but `torch` and `pandas`: cleaned and
normalized the data, initialized random coefficients, wrote the forward pass as
a matrix multiply through a sigmoid, defined a binary loss, and stepped the
coefficients downhill by hand. Then, by changing only the prediction function,
the same loop became a neural net (hidden layer + ReLU) and then a deep net.
The training loop — `calc_preds -> calc_loss -> backward -> step -> zero_grad`
— never changed. That loop, plus sensible initialization and normalization, is
precisely what `fastai`'s `Learner` automates on your behalf.

**Next lecture:** Lecture 06 — Random Forests & Tabular, where we leave gradient
descent behind and see when decision trees beat deep learning on tabular data.
