"""
07-machine-learning — 36: PyTorch Tensors — The GPU Currency
============================================================
Topics: tensors, dtypes, devices (CPU/GPU), autograd and the computation
        graph, no_grad, broadcasting (shared with NumPy), reshape/permute

Why this matters for AI/backend engineering:
    Tensors are the unit of deep learning — every model input, weight, and
    gradient is one. Understanding shapes, dtypes, devices, and autograd is
    the difference between code that trains and code that OOMs or silently
    computes wrong.

Run:      python 36-pytorch-tensors.py
Verify:   python 36-pytorch-tensors.py --verify
Reference: https://pytorch.org/docs/stable/tensors.html
"""

from __future__ import annotations

import torch
import numpy as np

# ============================================================
# 1. Creating tensors
# ============================================================
print("Example 1: creating tensors")
t = torch.tensor([[1, 2, 3], [4, 5, 6]])
print(f"  from list: {t.shape}, {t.dtype}")

ones = torch.ones(2, 3)
zeros = torch.zeros(3)
randn = torch.randn(2, 2)
eye = torch.eye(3)
print(f"  ones {ones.shape}, zeros {zeros.shape}, randn {randn.shape}, eye {eye.shape}")

arr = np.array([1.0, 2.0, 3.0])
t_from_np = torch.from_numpy(arr)
back = t_from_np.numpy()
print(f"  numpy <-> torch roundtrip: {back}")

# ============================================================
# 2. dtypes matter (float32 is the DL default)
# ============================================================
print("\nExample 2: dtypes")
f64 = torch.tensor([1.0])          # float32 default
f16 = f64.half()
i64 = torch.tensor([1]).long()
print(f"  default float: {f64.dtype}, half: {f16.dtype}, long: {i64.dtype}")
print(f"  float16 memory: {f64.element_size()/2} vs {f16.element_size()} bytes/elem")

# ============================================================
# 3. Device — CPU vs GPU
# ============================================================
print("\nExample 3: device")
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"  using: {device}")
x = torch.randn(2, 2, device=device)
print(f"  tensor on {x.device}")
print("  model.to('cuda') moves weights; .cpu() moves back for numpy conversion")

# ============================================================
# 4. Autograd — the computation graph
# ============================================================
print("\nExample 4: autograd")
w = torch.tensor(3.0, requires_grad=True)
b = torch.tensor(1.0, requires_grad=True)
x = torch.tensor(2.0)
y = w * x + b          # forward
print(f"  y = {y.item()}")
y.backward()           # backprop
print(f"  dy/dw = {w.grad.item()}  (expect 2 = x)")
print(f"  dy/db = {b.grad.item()}  (expect 1)")

# ============================================================
# 5. no_grad — inference & feature extraction
# ============================================================
print("\nExample 5: no_grad")
with torch.no_grad():
    z = w * x + b      # no graph built, no memory for gradients
print(f"  z = {z.item()} (requires_grad={z.requires_grad})")
w.grad.zero_()         # gradients accumulate — always zero before backward
print("  zero_() clears accumulated gradients")

# ============================================================
# 6. Broadcasting — same rules as NumPy
# ============================================================
print("\nExample 6: broadcasting")
a = torch.randn(3, 1)
b = torch.randn(1, 4)
c = a * b              # (3,1) * (1,4) -> (3,4)
print(f"  ({list(a.shape)}) * ({list(b.shape)}) -> {list(c.shape)}")

# ============================================================
# 7. Reshape / permute / squeeze
# ============================================================
print("\nExample 7: shape manipulation")
t2 = torch.arange(12).reshape(3, 4)      # same data, new shape
tp = t2.permute(1, 0)                     # transpose dims (view, no copy)
ts = t2.unsqueeze(0).squeeze()            # add/remove dim of size 1
print(f"  reshape {list(t2.shape)}, permute -> {list(tp.shape)}, unsqueeze/squeeze -> {list(ts.shape)}")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary:")
print("- torch.Tensor = numpy + device + autograd")
print("- float32 everywhere; half for GPU memory savings")
print("- requires_grad=True builds the autograd graph")
print("- no_grad() for inference; zero_() between backward passes")
print("- Broadcasting rules are identical to NumPy")
print("=" * 60)


def _verify() -> None:
    # Recompute: grad was zeroed by zero_() in example 5
    w2 = torch.tensor(3.0, requires_grad=True)
    b2 = torch.tensor(1.0, requires_grad=True)
    (w2 * torch.tensor(2.0) + b2).backward()
    assert w2.grad.item() == 2.0, "dy/dw must equal x"
    assert b2.grad.item() == 1.0
    assert z.requires_grad is False, "no_grad blocks the graph"
    assert c.shape == (3, 4), "broadcasting"
    assert tp.shape == (4, 3)
    t3 = torch.tensor(np.array([1.0, 2.0]))
    assert torch.equal(t3, torch.from_numpy(t3.numpy()))
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()
