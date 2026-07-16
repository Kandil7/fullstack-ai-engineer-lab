"""
=============================================================
EXERCISE 05: From-Scratch Model
=============================================================
Topic: Building a linear model and a neural net from tensors

Goal:
    Recreate fast.ai lesson 5 with pure torch + pandas. You will prep a small
    tabular dataset (a synthetic Titanic-style frame), normalize it, and train
    a linear model AND a one-hidden-layer neural net using a hand-written
    training loop -- no Learner, no nn.Linear, no optimizer.

Prerequisites:
    - Python 3.10+
    - torch
    - pandas
    Runs on CPU in seconds. No GPU or downloaded dataset required.
=============================================================
"""

from __future__ import annotations

import pandas as pd
import torch
from torch import Tensor

INDEP_COLS: list[str] = ["Age", "SibSp", "LogFare", "Sex_male", "Sex_female"]
DEP_COL: str = "Survived"


# ============================================================
# SECTION 1: Build and clean a tiny Titanic-style dataset
# ============================================================

def make_dataframe() -> pd.DataFrame:
    """Return a small synthetic frame with a missing value and a skewed Fare."""
    return pd.DataFrame(
        {
            "Age": [22.0, 38.0, 26.0, None, 35.0, 54.0, 2.0, 27.0],
            "SibSp": [1, 1, 0, 1, 0, 0, 3, 0],
            "Fare": [7.25, 71.28, 7.92, 53.1, 8.05, 51.86, 21.07, 11.13],
            "Sex": ["male", "female", "female", "female",
                    "male", "male", "male", "female"],
            "Survived": [0, 1, 1, 1, 0, 0, 0, 1],
        }
    )


def prep_data(df: pd.DataFrame) -> tuple[Tensor, Tensor]:
    """Impute, log-transform Fare, one-hot Sex, tensorize, and normalize."""
    df = df.copy()
    # EXERCISE: fill missing Age with the column MEDIAN (in place is fine).
    # df["Age"] = ...

    # EXERCISE: create a "LogFare" column using torch.log1p on the Fare values.
    # Hint: torch.log1p(torch.tensor(df["Fare"].values))
    # df["LogFare"] = ...

    # EXERCISE: one-hot encode the "Sex" column with pd.get_dummies.
    # Ensure the result has integer/float Sex_male and Sex_female columns.
    # df = pd.get_dummies(df, columns=["Sex"]).astype(float)

    indeps = torch.tensor(df[INDEP_COLS].values, dtype=torch.float)
    # EXERCISE: normalize each column by dividing by its per-column max.
    # Hint: indeps.max(dim=0).values
    # indeps = ...

    deps = torch.tensor(df[DEP_COL].values, dtype=torch.float)
    return indeps, deps


# ============================================================
# SECTION 2: Linear model from scratch
# ============================================================

def init_coeffs(n_coeff: int) -> Tensor:
    """Random coefficients centered on zero, tracking gradients."""
    torch.manual_seed(442)
    # EXERCISE: return torch.rand(n_coeff) - 0.5, then call .requires_grad_()
    # coeffs = ...
    # return coeffs
    raise NotImplementedError("Implement init_coeffs")


def calc_preds(coeffs: Tensor, indeps: Tensor) -> Tensor:
    """Linear model: dot product per row, squashed by sigmoid."""
    # EXERCISE: return torch.sigmoid((indeps * coeffs).sum(axis=1))
    raise NotImplementedError("Implement calc_preds")


def calc_loss(coeffs: Tensor, indeps: Tensor, deps: Tensor) -> Tensor:
    """Mean absolute error between predicted probability and 0/1 label."""
    # EXERCISE: return torch.abs(calc_preds(coeffs, indeps) - deps).mean()
    raise NotImplementedError("Implement calc_loss")


def one_epoch(coeffs: Tensor, indeps: Tensor, deps: Tensor, lr: float) -> float:
    """Run one gradient step and return the loss BEFORE the step."""
    loss = calc_loss(coeffs, indeps, deps)
    loss.backward()
    with torch.no_grad():
        # EXERCISE: subtract coeffs.grad * lr from coeffs (in place: sub_).
        # EXERCISE: then zero the gradient with coeffs.grad.zero_().
        pass
    return float(loss)


def train_linear(indeps: Tensor, deps: Tensor,
                 epochs: int = 30, lr: float = 2.0) -> Tensor:
    """Train the linear model and return the fitted coefficients."""
    coeffs = init_coeffs(indeps.shape[1])
    for _ in range(epochs):
        one_epoch(coeffs, indeps, deps, lr)
    return coeffs


def accuracy(coeffs: Tensor, indeps: Tensor, deps: Tensor) -> float:
    """Fraction of rows where (pred > 0.5) matches the label."""
    preds = calc_preds(coeffs, indeps)
    return float(((preds > 0.5) == deps.bool()).float().mean())


# ============================================================
# SECTION 3: Turn it into a neural net (hidden layer + ReLU)
# ============================================================

def init_nn(n_coeff: int, n_hidden: int = 20) -> list[Tensor]:
    """Two weight matrices + a constant, all tracking gradients."""
    torch.manual_seed(442)
    l1 = (torch.rand(n_coeff, n_hidden) - 0.5) / n_hidden
    l2 = torch.rand(n_hidden, 1) - 0.3
    const = torch.rand(1)
    return [t.requires_grad_() for t in (l1, l2, const)]


def nn_preds(coeffs: list[Tensor], indeps: Tensor) -> Tensor:
    """Forward pass: matmul -> ReLU -> matmul -> sigmoid."""
    l1, l2, const = coeffs
    # EXERCISE: res = torch.relu(indeps @ l1)
    # EXERCISE: res = res @ l2 + const
    # EXERCISE: return torch.sigmoid(res.squeeze())
    raise NotImplementedError("Implement nn_preds")


def nn_loss(coeffs: list[Tensor], indeps: Tensor, deps: Tensor) -> Tensor:
    return torch.abs(nn_preds(coeffs, indeps) - deps).mean()


def train_nn(indeps: Tensor, deps: Tensor,
             epochs: int = 30, lr: float = 1.5) -> list[Tensor]:
    """Same loop shape as the linear model, applied to a neural net."""
    coeffs = init_nn(indeps.shape[1])
    for _ in range(epochs):
        loss = nn_loss(coeffs, indeps, deps)
        loss.backward()
        with torch.no_grad():
            for layer in coeffs:
                layer.sub_(layer.grad * lr)
                layer.grad.zero_()
    return coeffs


# ============================================================
# SECTION 4: Run everything
# ============================================================

def main() -> None:
    indeps, deps = prep_data(make_dataframe())
    print(f"Prepared inputs shape: {tuple(indeps.shape)}")

    coeffs = train_linear(indeps, deps)
    print(f"Linear model accuracy: {accuracy(coeffs, indeps, deps):.3f}")

    nn_coeffs = train_nn(indeps, deps)
    nn_preds_out = nn_preds(nn_coeffs, indeps)
    nn_acc = float(((nn_preds_out > 0.5) == deps.bool()).float().mean())
    print(f"Neural net accuracy:   {nn_acc:.3f}")


if __name__ == "__main__":
    main()
