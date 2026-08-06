"""
07-machine-learning — 38: Neural Network Basics — Layers, Init, Regularization
==============================================================================
Topics: layers & activations, weight initialization, backprop intuition,
        vanishing/exploding gradients, batch norm & dropout, learning rate

Why this matters for AI/backend engineering:
    Training instability is the #1 deep learning failure: NaN losses,
    dead ReLUs, diverging training. Understanding init, activations, and
    regularization is what lets you FIX those instead of guessing seeds.

Run:      python 38-neural-network-basics.py
Verify:   python 38-neural-network-basics.py --verify
Reference: https://pytorch.org/docs/stable/nn.init.html
"""

from __future__ import annotations

import torch
import torch.nn as nn

torch.manual_seed(0)

# ============================================================
# 1. Activations — the non-linearity menu
# ============================================================
print("Example 1: activations")
x = torch.linspace(-3, 3, 7)
print(f"  x        : {x.tolist()}")
print(f"  sigmoid  : {torch.round(torch.sigmoid(x) * 1000) / 1000}  (squashes to 0..1)")
print(f"  tanh     : {torch.round(torch.tanh(x) * 1000) / 1000}  (squashes to -1..1)")
print(f"  relu     : {torch.relu(x).tolist()}  (kills negatives)")
print(f"  softmax  : {torch.round(torch.softmax(x, dim=0) * 1000) / 1000}  (probability distribution)")

# ============================================================
# 2. Weight initialization — why it matters
# ============================================================
print("\nExample 2: initialization controls gradient flow")
lin = nn.Linear(512, 512)
with torch.no_grad():
    lin.weight.normal_(0, 10)          # BAD: huge weights
std_bad = lin.weight.std().item()

nn.init.kaiming_uniform_(lin.weight, a=0)   # GOOD (default for ReLU nets)
std_good = lin.weight.std().item()
print(f"  bad init  std={std_bad:.2f}  -> activations explode / vanish")
print(f"  kaiming   std={std_good:.4f} -> stable signal")

# Demonstrate the vanishing gradient problem
def grad_norm_depth(depth: int, init_fn) -> float:
    layers = [nn.Linear(100, 100) for _ in range(depth)]
    for l in layers:
        init_fn(l.weight)
        l.bias.data.zero_()
    z = torch.randn(64, 100)
    for l in layers:
        z = torch.tanh(l(z))
    z.sum().backward()
    norms = [l.weight.grad.norm().item() for l in layers]
    return norms[0], norms[-1]

first, last = grad_norm_depth(10, lambda w: nn.init.xavier_uniform_(w))
print(f"\n  gradient norm first layer: {first:.2e}")
print(f"  gradient norm last layer : {last:.2e}")
print("  -> gap = vanishing/exploding gradient; batchnorm/skip-conns fix it")

# ============================================================
# 3. BatchNorm & Dropout — regularization pair
# ============================================================
print("\nExample 3: batch norm + dropout")
bn = nn.BatchNorm1d(8)
d = nn.Dropout(p=0.5)
data = torch.randn(4, 8)
print(f"  bn mean per channel after norm: {torch.round(bn(data).mean(dim=0) * 10000) / 10000}")
print(f"  dropout keeps ~{int((d(data) != 0).float().mean() * 100)}% alive (train mode)")

bn.eval()   # eval uses running stats, not batch stats
print(f"  in eval, batchnorm uses running stats (stable for inference)")

# ============================================================
# 4. Learning rate — the most important hyperparameter
# ============================================================
print("\nExample 4: learning rate sweep intuition")
for lr in [1e-1, 1e-2, 1e-4]:
    m = nn.Linear(4, 1)
    opt = torch.optim.SGD(m.parameters(), lr=lr)
    loss0 = None
    for _ in range(5):
        opt.zero_grad()
        l = ((m(torch.randn(8, 4)) - 1) ** 2).mean()
        l.backward()
        opt.step()
        loss0 = l.item()
    print(f"  lr={lr:.0e}: loss after 5 steps {loss0:.4f}")

# ============================================================
# 5. Backprop intuition — chain rule through layers
# ============================================================
print("\nExample 5: backprop = chain rule")
w1 = torch.tensor(2.0, requires_grad=True)
w2 = torch.tensor(3.0, requires_grad=True)
x = torch.tensor(1.5)
loss = (w1 * w2 * x) ** 2
loss.backward()
print(f"  dL/dw1 = {w1.grad.item():.1f}  (expect 2*(w1*w2*x)*(w2*x) = {2*(w1.item()*w2.item()*x.item())*(w2.item()*x.item()):.1f})")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary:")
print("- ReLU for hidden, softmax/sigmoid for output")
print("- kaiming/xavier init prevents vanishing/exploding gradients")
print("- BatchNorm stabilizes; Dropout regularizes")
print("- LR dominates training success — tune it first")
print("- Backprop = chain rule; autograd does it automatically")
print("=" * 60)


def _verify() -> None:
    assert std_bad > std_good, "bad init must be wider than kaiming"
    bn.train()  # training mode: normalize with batch statistics
    assert abs(bn(data).mean(dim=0).max().item()) < 0.1, "batchnorm centers channels in train mode"
    assert last < first, "gradients should shrink toward early layers (vanishing demo)"
    assert w1.grad.item() > 0
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()
