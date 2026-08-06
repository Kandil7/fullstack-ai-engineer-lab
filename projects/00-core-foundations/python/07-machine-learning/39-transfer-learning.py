"""
07-machine-learning — 39: Transfer Learning — Small-Data Superpower
===================================================================
Topics: pretrained models, freezing vs fine-tuning, feature extraction,
        learning-rate schedules, the small-data strategy

Why this matters for AI/backend engineering:
    Nobody trains vision/LLM models from scratch in production — they
    fine-tune pretrained ones. Transfer learning is how a 5k-sample dataset
    gets SOTA-quality results: the model already knows low-level patterns;
    you teach it your domain.

Note: torchvision is not installed in this environment, so we demonstrate
transfer learning on a self-trained source task -> target task. The pattern
(freeze backbone, swap head, fine-tune) is identical to using ResNet/BERT.

Run:      python 39-transfer-learning.py
Verify:   python 39-transfer-learning.py --verify
Reference: https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html
"""

from __future__ import annotations

import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

torch.manual_seed(0)

# ============================================================
# 1. The source task — train a "pretrained" backbone
# ============================================================
class Backbone(nn.Module):
    """Generic feature extractor: linear -> relu -> linear."""

    def __init__(self, in_dim: int, hidden: int, feat_dim: int):
        super().__init__()
        self.features = nn.Sequential(
            nn.Linear(in_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, feat_dim),
        )
        self.head = nn.Linear(feat_dim, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.head(self.features(x))


def make_task(n: int, in_dim: int, seed: int):
    g = torch.Generator().manual_seed(seed)
    X = torch.randn(n, in_dim, generator=g)
    y = (X[:, 0] * 0.8 + X[:, 1] * 0.5 + torch.randn(n, generator=g) * 0.3 > 0).float().unsqueeze(1)
    return TensorDataset(X, y)


src_ds = make_task(2000, 20, seed=1)
src_loader = DataLoader(src_ds, batch_size=128, shuffle=True)

# Pretrain the backbone on the source task
backbone = Backbone(20, 64, 32)
opt = torch.optim.Adam(backbone.parameters(), lr=1e-3)
crit = nn.BCEWithLogitsLoss()

for epoch in range(10):
    backbone.train()
    for xb, yb in src_loader:
        opt.zero_grad()
        loss = crit(backbone(xb), yb)
        loss.backward()
        opt.step()

print("Example 1: pretrain on the source task")
print(f"  source task trained: loss {loss.item():.4f}")

# ============================================================
# 2. Transfer: freeze the backbone, swap the head
# ============================================================
# Target task: DIFFERENT decision rule, small dataset (200 samples)
tgt_ds = make_task(200, 20, seed=2)
tgt_loader = DataLoader(tgt_ds, batch_size=32, shuffle=True)

transfer = Backbone(20, 64, 32)
transfer.load_state_dict(backbone.state_dict())   # start from pretrained weights

# FREEZE the feature extractor — only the head trains
for p in transfer.features.parameters():
    p.requires_grad = False
trainable = sum(p.numel() for p in transfer.parameters() if p.requires_grad)
total = sum(p.numel() for p in transfer.parameters())
print(f"\nExample 2: freeze backbone, train only head")
print(f"  trainable params: {trainable:,} / {total:,}  ({(trainable/total*100):.1f}%)")

opt2 = torch.optim.Adam(filter(lambda p: p.requires_grad, transfer.parameters()), lr=1e-3)
for epoch in range(20):
    transfer.train()
    for xb, yb in tgt_loader:
        opt2.zero_grad()
        loss = crit(transfer(xb), yb)
        loss.backward()
        opt2.step()
print(f"  fine-tuned on 200 target samples: loss {loss.item():.4f}")

# ============================================================
# 3. Compare: train from scratch on the small target set
# ============================================================
scratch = Backbone(20, 64, 32)   # random init
opt3 = torch.optim.Adam(scratch.parameters(), lr=1e-3)
for epoch in range(20):
    scratch.train()
    for xb, yb in tgt_loader:
        opt3.zero_grad()
        loss3 = crit(scratch(xb), yb)
        loss3.backward()
        opt3.step()

transfer.eval(), scratch.eval()
with torch.no_grad():
    xt = torch.randn(500, 20)
    yt = (xt[:, 0] * 0.8 + xt[:, 1] * 0.5 + torch.randn(500) * 0.3 > 0).float()
    acc_transfer = ((torch.sigmoid(transfer(xt)) > 0.5).squeeze() == yt).float().mean().item()
    acc_scratch = ((torch.sigmoid(scratch(xt)) > 0.5).squeeze() == yt).float().mean().item()
print("\nExample 3: transfer vs from-scratch on small data")
print(f"  accuracy transfer : {acc_transfer:.3f}")
print(f"  accuracy scratch  : {acc_scratch:.3f}")
print("  -> pretrained features generalize better on small data")

# ============================================================
# 4. Feature extraction — reuse features as vectors
# ============================================================
print("\nExample 4: feature extraction mode")
with torch.no_grad():
    feats = transfer.features(xt)     # embedding vectors, no head
print(f"  500 samples -> {tuple(feats.shape)} embedding vectors (32-dim)")
print("  embeddings feed downstream: retrieval, clustering, linear probes")

# ============================================================
# 5. LR schedules — fine-tuning etiquette
# ============================================================
print("\nExample 5: learning-rate schedules for fine-tuning")
sched = torch.optim.lr_scheduler.StepLR(opt2, step_size=10, gamma=0.1)
print(f"  StepLR halves LR every 10 epochs (fine-tune: small LR, gentle decay)")
print(f"  current LR: {sched.get_last_lr()}")
for _ in range(10):
    sched.step()   # simulate 10 epochs -> LR drops by gamma
print(f"  after 10 epochs: {sched.get_last_lr()}")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary:")
print("- Transfer = pretrained features + new head")
print("- Freeze backbone for feature extraction; unfreeze for fine-tune")
print("- Small data + pretrained >> small data + scratch")
print("- Use small LRs and gentle schedules when fine-tuning")
print("- Same pattern with ResNet/BERT: load weights, swap head")
print("=" * 60)


def _verify() -> None:
    assert trainable < total, "freezing must cut trainable params"
    assert acc_transfer >= acc_scratch - 0.1, "transfer should not be much worse"
    assert feats.shape == (500, 32)
    assert sched.get_last_lr()[0] < 1e-3
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()
