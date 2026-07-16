"""
Exercise 03: Neural Net Foundations (SGD)
==========================================
Goal: Learn how models actually learn. Implement the 7-step SGD loop by hand,
fit a quadratic, watch the learning rate matter, then bend a linear model into
a neural net with a ReLU nonlinearity. Everything runs on CPU with pure torch
-- no GPU and no dataset download required.

Prerequisites:
    pip install torch

Run:
    python 03-neural-net-foundations.py
"""

from __future__ import annotations

import torch
from torch import Tensor


# ---------------------------------------------------------------------------
# 1. Autograd basics: requires_grad_, backward, grad
# ---------------------------------------------------------------------------

def autograd_demo() -> Tensor:
    """Show that PyTorch computes gradients for us.

    For y = x**2, dy/dx = 2x, so at x=3 the gradient is 6.
    """
    x = torch.tensor(3.0).requires_grad_()
    y = x ** 2
    y.backward()  # backpropagation fills x.grad
    print(f"[1] x=3, y=x^2 -> x.grad = {x.grad.item()} (expected 6.0)")

    # EXERCISE: change y to 3 * x**3 and predict x.grad before running.
    #           (d/dx of 3x^3 = 9x^2 = 81 at x=3)
    return x.grad


# ---------------------------------------------------------------------------
# 2. The model and the loss function (MSE)
# ---------------------------------------------------------------------------

def quadratic(t: Tensor, params: Tensor) -> Tensor:
    """A quadratic model a*t^2 + b*t + c parameterised by params=(a,b,c)."""
    a, b, c = params
    return a * t ** 2 + b * t + c


def mse(preds: Tensor, targets: Tensor) -> Tensor:
    """Mean squared error: the average squared difference."""
    return ((preds - targets) ** 2).mean()


# ---------------------------------------------------------------------------
# 3. Synthetic data: roller-coaster speed vs time (noisy quadratic)
# ---------------------------------------------------------------------------

def make_quadratic_data() -> tuple[Tensor, Tensor]:
    """Return (time, speed) where speed is a noisy quadratic of time."""
    torch.manual_seed(42)
    time = torch.arange(0, 20, 1).float()
    true_a, true_b, true_c = 1.0, -15.0, 60.0
    speed = true_a * time ** 2 + true_b * time + true_c
    speed = speed + 5 * torch.randn(len(time))  # measurement noise
    return time, speed


# ---------------------------------------------------------------------------
# 4. The 7-step SGD loop (by hand) to fit the quadratic
# ---------------------------------------------------------------------------

def fit_quadratic(time: Tensor, speed: Tensor, lr: float, epochs: int) -> Tensor:
    """Fit a*t^2 + b*t + c with hand-written SGD. Returns learned params."""
    params = torch.randn(3).requires_grad_()  # STEP 1: init

    for epoch in range(epochs):
        preds = quadratic(time, params)       # STEP 2: predict
        loss = mse(preds, speed)              # STEP 3: loss
        loss.backward()                       # STEP 4: gradients
        with torch.no_grad():
            params -= lr * params.grad        # STEP 5: step downhill
        params.grad.zero_()                   # zero grads for next iteration
        if epoch % max(1, epochs // 5) == 0:
            print(f"    epoch {epoch:4d}  loss {loss.item():10.2f}")

    # EXERCISE: comment out `params.grad.zero_()` and observe the loss blow up
    #           because gradients accumulate across iterations.
    return params.detach()


def learning_rate_experiment(time: Tensor, speed: Tensor) -> None:
    """Show divergence (lr too high) vs. slow convergence (lr too low)."""
    for lr in (1e-6, 1e-4):
        print(f"[4] fitting quadratic with lr={lr:.0e}")
        params = fit_quadratic(time, speed, lr=lr, epochs=20)
        print(f"    learned (a,b,c) = {params.tolist()}")

    # EXERCISE: add lr=1e-2 to the tuple above and watch the loss diverge
    #           to nan. Explain why in a comment.


# ---------------------------------------------------------------------------
# 5. From linear to neural net: add a ReLU nonlinearity
# ---------------------------------------------------------------------------

def relu(t: Tensor) -> Tensor:
    """Rectified Linear Unit: keep positives, clamp negatives to zero."""
    return t.clamp(min=0)


def make_parabola_data() -> tuple[Tensor, Tensor]:
    """Return (x, y) where y is a noisy parabola -- not linearly fittable."""
    torch.manual_seed(0)
    x = torch.linspace(-3, 3, 100).unsqueeze(1)  # shape (100, 1)
    y = x ** 2 + torch.randn_like(x) * 0.3
    return x, y


def init_param(size: tuple[int, ...] | int, std: float = 1.0) -> Tensor:
    """Initialise a learnable parameter tensor."""
    return (torch.randn(size) * std).requires_grad_()


def fit_neural_net(x: Tensor, y: Tensor, n_hidden: int, lr: float, epochs: int) -> float:
    """Fit y with a linear -> ReLU -> linear net. Returns final loss."""
    w1 = init_param((1, n_hidden), std=1.0)
    b1 = init_param(n_hidden, std=1.0)
    w2 = init_param((n_hidden, 1), std=1.0)
    b2 = init_param(1, std=1.0)
    params = [w1, b1, w2, b2]

    def model(xb: Tensor) -> Tensor:
        hidden = relu(xb @ w1 + b1)  # nonlinearity between the linear layers
        return hidden @ w2 + b2

    loss = torch.tensor(float("nan"))
    for epoch in range(epochs):
        loss = mse(model(x), y)
        loss.backward()
        with torch.no_grad():
            for p in params:
                p -= lr * p.grad
                p.grad.zero_()
        if epoch % max(1, epochs // 5) == 0:
            print(f"    epoch {epoch:4d}  loss {loss.item():.4f}")

    # EXERCISE: remove the relu() call so the net is purely linear. Show that
    #           the loss plateaus high -- stacked linear layers stay linear.
    return loss.item()


# ---------------------------------------------------------------------------
# 6. The PyTorch way: nn.Sequential + optimizer (MNIST 3s-vs-7s shapes)
# ---------------------------------------------------------------------------

def fit_pytorch_way(epochs: int = 20) -> float:
    """Rebuild the net with nn.Linear/nn.Sequential and torch.optim.SGD.

    Uses MNIST 3-vs-7 SHAPES (784-pixel inputs, binary label) with fabricated
    data so it runs with no download. Returns final accuracy.
    """
    from torch import nn

    torch.manual_seed(0)
    n = 256
    train_x = torch.randn(n, 28 * 28)  # (256, 784): flattened 28x28 images
    train_y = (train_x.mean(dim=1, keepdim=True) > 0).float()  # fake 3-vs-7

    model = nn.Sequential(
        nn.Linear(28 * 28, 30),  # weights + bias are nn.Parameter
        nn.ReLU(),
        nn.Linear(30, 1),
    )
    opt = torch.optim.SGD(model.parameters(), lr=0.1)
    loss_fn = nn.MSELoss()

    acc = torch.tensor(0.0)
    for epoch in range(epochs):
        preds = model(train_x).sigmoid()  # sigmoid -> probability in (0,1)
        loss = loss_fn(preds, train_y)
        loss.backward()
        opt.step()        # STEP 5 for every parameter at once
        opt.zero_grad()   # optimizer wraps grad.zero_() for us
        acc = (((model(train_x).sigmoid() > 0.5) == (train_y > 0.5))
               .float().mean())
        if epoch % 5 == 0:
            print(f"    epoch {epoch:2d}  loss {loss.item():.4f}  acc {acc.item():.3f}")

    # EXERCISE: swap nn.MSELoss for nn.BCELoss and compare final accuracy.
    return acc.item()


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main() -> None:
    print("== 1. Autograd basics ==")
    autograd_demo()

    print("\n== 4. Fit a quadratic with SGD at different learning rates ==")
    time, speed = make_quadratic_data()
    learning_rate_experiment(time, speed)

    print("\n== 5. Neural net (linear -> ReLU -> linear) fits a parabola ==")
    x, y = make_parabola_data()
    fit_neural_net(x, y, n_hidden=30, lr=1e-2, epochs=2000)

    print("\n== 6. The PyTorch way (MNIST 3s-vs-7s shapes) ==")
    fit_pytorch_way(epochs=20)


if __name__ == "__main__":
    main()
