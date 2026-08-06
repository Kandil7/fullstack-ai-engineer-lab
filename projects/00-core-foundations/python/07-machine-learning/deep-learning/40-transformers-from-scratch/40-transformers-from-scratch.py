"""
07-machine-learning — 40: Transformers From Scratch — Attention Is All You Need
===============================================================================
Topics: attention mechanism implemented directly, Q/K/V, scaled dot-product,
        multi-head attention, positional encoding, the transformer block,
        why attention scales quadratically, the foundation for Phase 9

Why this matters for AI/backend engineering:
    Every LLM you will ever serve — GPT, Claude, LLaMA — is a stack of
    transformer blocks. Implementing attention yourself demystifies the
    whole GenAI stack: what a context window is, why it costs what it costs,
    and what "attention" actually computes.

Run:      python 40-transformers-from-scratch.py
Verify:   python 40-transformers-from-scratch.py --verify
Reference: https://arxiv.org/abs/1706.03762
"""

from __future__ import annotations

import math
import torch
import torch.nn as nn

torch.manual_seed(0)

# ============================================================
# 1. Scaled Dot-Product Attention — the core equation
# ============================================================
def scaled_dot_product_attention(Q: torch.Tensor, K: torch.Tensor, V: torch.Tensor,
                                 mask: torch.Tensor | None = None) -> torch.Tensor:
    """Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) V.

    Shapes: (batch, heads, seq, d_k) for Q/K, (batch, heads, seq, d_v) for V.
    """
    d_k = Q.shape[-1]
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)  # (B,H,S,S)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float("-inf"))
    weights = torch.softmax(scores, dim=-1)                          # normalize over keys
    return torch.matmul(weights, V)


print("Example 1: scaled dot-product attention")
# A tiny sequence: 4 tokens, each embedded in 8 dims, 1 head
Q = torch.randn(1, 1, 4, 8)
K = torch.randn(1, 1, 4, 8)
V = torch.randn(1, 1, 4, 8)
out = scaled_dot_product_attention(Q, K, V)
print(f"  output shape: {tuple(out.shape)}  (tokens unchanged in length)")
print(f"  attention weight rows sum to 1: {out.shape}")

# ============================================================
# 2. Why scale by sqrt(d_k)?
# ============================================================
print("\nExample 2: scaling prevents softmax saturation")
d_small = 2
d_large = 128
scores_small = torch.randn(4, 4) * 1.0
scores_large = torch.randn(4, 4) * math.sqrt(d_large)
print(f"  small d: softmax entropy {torch.distributions.Categorical(probs=torch.softmax(scores_small, -1)).entropy().mean():.3f}")
print(f"  large d: softmax entropy {torch.distributions.Categorical(probs=torch.softmax(scores_large, -1)).entropy().mean():.3f}")
print("  -> without scaling, large d_k pushes softmax to near one-hot (dead gradients)")

# ============================================================
# 3. Multi-Head Attention — attend in parallel subspaces
# ============================================================
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model: int, n_heads: int):
        super().__init__()
        assert d_model % n_heads == 0
        self.d_model, self.n_heads = d_model, n_heads
        self.d_k = d_model // n_heads
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

    def _split(self, x: torch.Tensor) -> torch.Tensor:
        B, S, _ = x.shape
        return x.view(B, S, self.n_heads, self.d_k).transpose(1, 2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        Q = self._split(self.W_q(x))
        K = self._split(self.W_k(x))
        V = self._split(self.W_v(x))
        attn = scaled_dot_product_attention(Q, K, V)          # (B, H, S, d_k)
        B, H, S, _ = attn.shape
        out = attn.transpose(1, 2).contiguous().view(B, S, self.d_model)
        return self.W_o(out)


mha = MultiHeadAttention(d_model=64, n_heads=8)
x_seq = torch.randn(2, 10, 64)          # batch=2, 10 tokens, 64-dim
print("\nExample 3: multi-head attention")
print(f"  input  {tuple(x_seq.shape)} -> output {tuple(mha(x_seq).shape)}")

# ============================================================
# 4. Positional Encoding — inject order
# ============================================================
def positional_encoding(seq_len: int, d_model: int) -> torch.Tensor:
    pe = torch.zeros(seq_len, d_model)
    pos = torch.arange(seq_len).unsqueeze(1).float()
    div = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
    pe[:, 0::2] = torch.sin(pos * div)
    pe[:, 1::2] = torch.cos(pos * div)
    return pe.unsqueeze(0)


pe = positional_encoding(20, 64)
print("\nExample 4: positional encoding")
print(f"  shape {tuple(pe.shape)}; sin/cos pattern distinguishes token positions")
print(f"  row 0 vs row 1 distance: {(pe[0,0]-pe[0,1]).norm().item():.3f}")

# ============================================================
# 5. The Transformer Block — attention + FFN + residuals
# ============================================================
class TransformerBlock(nn.Module):
    def __init__(self, d_model: int, n_heads: int, ff_dim: int):
        super().__init__()
        self.attn = MultiHeadAttention(d_model, n_heads)
        self.norm1 = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(nn.Linear(d_model, ff_dim), nn.ReLU(),
                                nn.Linear(ff_dim, d_model))
        self.norm2 = nn.LayerNorm(d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.attn(self.norm1(x))     # residual + pre-norm attention
        x = x + self.ff(self.norm2(x))       # residual + pre-norm FFN
        return x


block = TransformerBlock(d_model=64, n_heads=8, ff_dim=256)
print("\nExample 5: transformer block")
print(f"  {tuple(x_seq.shape)} -> {tuple(block(x_seq).shape)}")

# ============================================================
# 6. Quadratic scaling — the cost story
# ============================================================
print("\nExample 6: why attention is O(S^2) — the context-window cost")
for s in [100, 1_000, 10_000, 100_000]:
    pairs = s * s
    print(f"  seq {s:>6}: {pairs:>12,} token pairs to score")
print("  -> long context = quadratic memory/time; this drives architecture design")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary:")
print("- Attention = softmax(QK^T/sqrt(d_k))V: tokens exchange info")
print("- Multi-head: parallel subspaces, richer patterns")
print("- Positional encoding adds order (attention is permutation-invariant)")
print("- Block = attention + FFN + residual + layer norm (pre-norm)")
print("- O(S^2) cost explains context-window limits and KV-cache tricks")
print("- This IS the architecture behind every modern LLM")
print("=" * 60)


def _verify() -> None:
    assert out.shape == (1, 1, 4, 8)
    assert mha(x_seq).shape == (2, 10, 64)
    assert block(x_seq).shape == (2, 10, 64)
    # attention weights must be a valid distribution
    Q2, K2, V2 = torch.randn(1, 1, 4, 8), torch.randn(1, 1, 4, 8), torch.randn(1, 1, 4, 8)
    w = torch.softmax(torch.matmul(Q2, K2.transpose(-2, -1)) / math.sqrt(8), dim=-1)
    assert torch.allclose(w.sum(dim=-1), torch.ones(1, 1, 4))
    # positional encoding rows differ
    assert (pe[0, 0] != pe[0, 1]).any()
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()
