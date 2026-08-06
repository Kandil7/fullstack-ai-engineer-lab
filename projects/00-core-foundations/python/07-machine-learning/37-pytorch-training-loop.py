"""
07-machine-learning — 37: PyTorch Training Loop — The Canonical Pattern
=======================================================================
Topics: nn.Module, Dataset/DataLoader, loss/optimizer, the canonical loop,
        overfitting a single batch as the FIRST debugging step, model.eval
        vs train, device placement

Why this matters for AI/backend engineering:
    Every PyTorch project — from research to production — runs the same
    6-line training loop. Knowing it cold, plus the "overfit one batch"
    debug trick, saves days of confusion.

Run:      python 37-pytorch-training-loop.py
Verify:   python 37-pytorch-training-loop.py --verify
Reference: https://pytorch.org/tutorials/beginner/basics/optimization_tutorial.html
"""

from __future__ import annotations

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, TensorDataset

torch.manual_seed(0)

# ============================================================
# 1. nn.Module — define the model
# ============================================================
class TwoLayerNet(nn.Module):
    def __init__(self, in_dim: int, hidden: int, out_dim: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, out_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


model = TwoLayerNet(10, 32, 1)
print("Example 1: model definition")
print(f"  params: {sum(p.numel() for p in model.parameters()):,}")

# ============================================================
# 2. Dataset & DataLoader — batching
# ============================================================
X = torch.randn(1000, 10)
y = (X[:, 0] * 0.7 + X[:, 1] * 0.3 + torch.randn(1000) * 0.5 > 0).float().unsqueeze(1)
dataset = TensorDataset(X, y)
loader = DataLoader(dataset, batch_size=64, shuffle=True)
print("\nExample 2: DataLoader")
print(f"  batches per epoch: {len(loader)}  batch size: 64")

# ============================================================
# 3. Loss + optimizer + the canonical loop
# ============================================================
criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-2)


def train_one_epoch(m, dataloader, crit, opt) -> float:
    m.train()
    total_loss, n_batches = 0.0, 0
    for xb, yb in dataloader:
        opt.zero_grad()
        logits = m(xb)
        loss = crit(logits, yb)
        loss.backward()
        opt.step()
        total_loss += loss.item()
        n_batches += 1
    return total_loss / n_batches


print("\nExample 3: canonical training loop")
for epoch in range(3):
    loss = train_one_epoch(model, loader, criterion, optimizer)
    print(f"  epoch {epoch+1}: loss {loss:.4f}")

# ============================================================
# 4. The debug trick: overfit a single batch first
# ============================================================
print("\nExample 4: overfit one batch (debugging first step)")
debug_model = TwoLayerNet(10, 32, 1)
debug_opt = torch.optim.Adam(debug_model.parameters(), lr=1e-2)
xb, yb = next(iter(loader))
for step in range(50):
    debug_opt.zero_grad()
    loss = criterion(debug_model(xb), yb)
    loss.backward()
    debug_opt.step()
print(f"  loss on ONE batch after 50 steps: {loss.item():.4f}  (should drop well below 0.5)")
print("  if a model can't overfit one batch, the bug is in the code, not the data")

# ============================================================
# 5. eval mode + inference
# ============================================================
model.eval()
with torch.no_grad():
    logits = model(X[:10])
    probs = torch.sigmoid(logits)
print("\nExample 5: inference")
print(f"  probabilities: {torch.round(probs.squeeze() * 1000) / 1000}")
print("  model.eval() disables dropout/batchnorm training behavior")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary:")
print("- nn.Module: define forward(); params auto-collected")
print("- DataLoader: batching + shuffling")
print("- Loop: zero_grad -> forward -> loss -> backward -> step")
print("- DEBUG: overfit a single batch before touching real data")
print("- eval() + no_grad() for inference")
print("=" * 60)


def _verify() -> None:
    assert loss.item() < 0.5, "single-batch overfit must succeed"
    assert len(loader) == 16, "1000 rows / 64 = 16 batches (last partial)"
    assert sum(p.numel() for p in model.parameters()) > 0
    assert probs.shape == (10, 1)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()
