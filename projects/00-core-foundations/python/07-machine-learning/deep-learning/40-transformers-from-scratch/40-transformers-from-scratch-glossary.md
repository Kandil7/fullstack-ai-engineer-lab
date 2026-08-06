# Transformers From Scratch — Glossary 40

Companion lecture: `40-transformers-from-scratch-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Attention | Core | Mechanism where tokens exchange info weighted by relevance |
| Attention head | Core | One attention function in one projection subspace |
| Causal mask | Core | Restricts attention to past tokens (autoregressive decoding) |
| Context window | System | The sequence length S an LLM can attend over |
| Feed-forward (FFN) | Block | Per-token MLP: expand -> activate -> contract |
| KV cache | System | Cached K/V tensors so generation reuses past computation |
| LayerNorm | Block | Normalization across features per token |
| Multi-head attention | Core | Parallel attention functions in different subspaces |
| O(S^2) | Cost | Quadratic growth of attention compute/memory with length |
| Positional encoding | Core | Sin/cos signal adding order information |
| Pre-norm | Block | LayerNorm before the sublayer (modern transformer default) |
| Q/K/V | Core | Query, key, value projections of the input |
| Residual connection | Block | x + sublayer(x): gradient highway around sublayers |
| Scaled dot-product attention | Core | softmax(QK^T / sqrt(d_k)) V |
| Self-attention | Core | Attention where Q, K, V all derive from the same sequence |
| Transformer block | Block | Attention + FFN + residuals + norms, the LLM building block |

## Detailed Definitions

### Attention
**Definition**: The operation computing a weighted sum of values, where each
token's weights are its relevance to every other token. The core of the
transformer.
**Example**:
```python
weights = torch.softmax(Q @ K.T / math.sqrt(d_k), dim=-1)
out = weights @ V
```
**Complexity**: O(S^2 x d).
**Related**: Scaled dot-product attention, Self-attention

### Attention head
**Definition**: One attention computation in one projected subspace of size
d_model/n_heads; multiple heads run in parallel.
**Related**: Multi-head attention

### Causal mask
**Definition**: A mask zeroing attention from future tokens, used in decoder
LLMs so token i only attends to tokens 0..i during autoregressive generation.
**Example**:
```python
scores = scores.masked_fill(mask == 0, float("-inf"))
```
**Related**: Attention, Context window

### Context window
**Definition**: The sequence length S a model can attend over — bounded by the
O(S^2) memory/compute cost of attention.
**Related**: O(S^2), KV cache

### Feed-forward (FFN)
**Definition**: A per-token two-layer MLP (expand to ff_dim, activate,
contract to d_model) applied identically to every position; the bulk of a
transformer's parameters.
**Related**: Transformer block

### KV cache
**Definition**: Cached key/value tensors from previous generation steps so each
new token attends to history without recomputing — the memory that grows with
context length during inference.
**Related**: Context window, Attention

### LayerNorm
**Definition**: Normalizes each token's features to zero mean / unit variance
with learned scale and shift; applied before sublayers (pre-norm).
**Related**: Pre-norm, Transformer block

### Multi-head attention
**Definition**: h parallel attention functions, each in a d_model/h subspace,
concatenated and projected — lets the model attend in different ways at once.
**Related**: Attention head, Self-attention

### O(S^2)
**Definition**: The quadratic growth of attention time and memory with sequence
length S — the dominant cost fact driving context limits, chunking, and
KV-cache engineering.
**Example**:
```python
s * s   # token pairs to score for length s
```
**Related**: Context window, KV cache

### Positional encoding
**Definition**: A deterministic sin/cos signal added to embeddings so the
permutation-invariant attention can use token order.
**Example**:
```python
pe[:, 0::2] = torch.sin(pos * div)
pe[:, 1::2] = torch.cos(pos * div)
```
**Related**: Self-attention

### Pre-norm
**Definition**: LayerNorm placed before the attention/FFN sublayer, the modern
transformer default (vs post-norm in the original paper).
**Related**: LayerNorm, Residual connection

### Q/K/V
**Definition**: Query, key, and value projections of the input; queries score
against keys to weight values.
**Related**: Scaled dot-product attention

### Residual connection
**Definition**: x + sublayer(x) — lets gradients flow around the sublayer,
enabling deep stacks.
**Example**:
```python
x = x + self.attn(self.norm1(x))
```
**Related**: Transformer block, Pre-norm

### Scaled dot-product attention
**Definition**: The core equation: softmax(QK^T / sqrt(d_k)) V, with scaling
preventing softmax saturation at large d_k.
**Related**: Attention, Q/K/V

### Self-attention
**Definition**: Attention where Q, K, and V all derive from the same sequence —
each token attends to the other tokens in that sequence.
**Related**: Attention, Multi-head attention

### Transformer block
**Definition**: The stackable unit of an LLM: multi-head attention + FFN, each
with pre-norm and a residual connection. LLMs are stacks of these blocks.
**Related**: Residual connection, Feed-forward

## Key Concepts Summary

### The attention equation
- Attention = softmax(QK^T / sqrt(d_k)) V.
- Q/K/V are projections of the input; weights sum to 1 over keys.
- Scaling by sqrt(d_k) keeps logits at unit variance — no saturation.

### The block anatomy
- Multi-head attention (parallel subspaces) -> add residual -> FFN -> add residual.
- Pre-norm (LayerNorm before sublayers) is the modern default.
- Positional encoding adds order to permutation-invariant attention.

### The cost story
- Attention is O(S^2) in sequence length — the central engineering constraint.
- KV caches, chunking, and sliding windows all fight this curve.
- This architecture powers every modern LLM.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. softmax(QK^T / sqrt(d_k)) V — ___
2. The quadratic growth of attention with sequence length — ___
3. Cached tensors so generation reuses past computation — ___
4. Attention where Q, K, V derive from the same sequence — ___
5. The gradient highway x + sublayer(x) — ___
6. Sin/cos signal adding order information — ___
7. LayerNorm placed before the sublayer — ___
8. Parallel attention functions in different subspaces — ___

**Answers:** 1-scaled dot-product attention, 2-O(S^2), 3-KV cache,
4-self-attention, 5-residual connection, 6-positional encoding, 7-pre-norm,
8-multi-head attention
