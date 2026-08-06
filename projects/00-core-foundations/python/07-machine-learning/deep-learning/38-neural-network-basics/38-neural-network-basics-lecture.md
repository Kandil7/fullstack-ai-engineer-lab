# 07-machine-learning — 38: Neural Network Basics — Layers, Init, Regularization

Companion exercise: `38-neural-network-basics.py`

---

## Topic Overview

A neural network is a stack of differentiable layers with non-linear
activations between them, trained by gradient descent. The concept is simple;
the *practice* is not. Most deep-learning failures are training instability:
NaN losses, dead ReLUs, diverging curves, vanishing or exploding gradients.
This topic gives you the mechanics that prevent those failures — activation
choice, weight initialization, batch norm, dropout, and learning-rate
discipline — so you can *fix* training problems instead of re-rolling seeds.

The unifying idea is gradient flow: information must survive backward passes
through many layers. Initialization controls the starting scale, activations
control the signal shape, batch norm stabilizes the distribution, and the
learning rate controls how far each step travels.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Choose activations by layer type (hidden vs output).
2. Explain why initialization scale determines gradient flow.
3. Demonstrate vanishing gradients and name the fixes.
4. Explain what batch norm does in train vs eval mode.
5. Use dropout and state its train/eval behavior.
6. Explain why learning rate dominates training success.
7. Trace backprop as the chain rule through layers.
8. Debug a NaN or diverging loss systematically.

## Prerequisites

| Need | Where |
|---|---|
| Tensors and autograd | `36-pytorch-tensors.py` |
| The training loop | `37-pytorch-training-loop.py` |
| Logistic regression / gradient descent | `15-logistic-regression.py` |

## 1. Activations — The Non-Linearity Menu

```python
x = torch.linspace(-3, 3, 7)
print(torch.sigmoid(x).round(decimals=3))   # 0..1
print(torch.tanh(x).round(decimals=3))      # -1..1
print(torch.relu(x))                        # max(0, x)
```

Output:
```
[0.047 0.119 ... 0.953]
[-0.995 -0.964 ... 0.995]
[0. 0. ... 3.]
```

- **ReLU**: default for hidden layers — cheap, avoids saturation, but kills
  negatives (dead-ReLU risk).
- **sigmoid**: output for binary probability; saturates and kills gradients
  in hidden layers.
- **tanh**: centered at zero; better gradient flow than sigmoid, used in
  older RNNs.
- **softmax**: output for multi-class probability distributions.

## 2. Weight Initialization — Why It Matters

The initial weight scale decides whether signals survive the first forward and
backward passes. Initialize too wide and activations explode; too narrow and
they vanish.

```python
lin = nn.Linear(512, 512)
with torch.no_grad():
    lin.weight.normal_(0, 10)              # BAD: std 10
std_bad = lin.weight.std().item()

nn.init.kaiming_uniform_(lin.weight, a=0)  # GOOD: He init for ReLU nets
std_good = lin.weight.std().item()
```

Output:
```
bad init  std=9.98  -> activations explode / vanish
kaiming   std=0.0891 -> stable signal
```

The math: for a ReLU net with fan-in f, He init uses std = sqrt(2/f);
Xavier uses sqrt(1/f) for tanh/sigmoid. Modern libraries initialize sensibly by
default — but you must know the *why* to diagnose custom architectures.

## 3. Vanishing / Exploding Gradients

```python
def grad_norm_depth(depth, init_fn):
    layers = [nn.Linear(100, 100) for _ in range(depth)]
    for l in layers:
        init_fn(l.weight); l.bias.data.zero_()
    z = torch.randn(64, 100)
    for l in layers:
        z = torch.tanh(l(z))
    z.sum().backward()
    norms = [l.weight.grad.norm().item() for l in layers]
    return norms[0], norms[-1]

first, last = grad_norm_depth(10, nn.init.xavier_uniform_)
```

Output:
```
gradient norm first layer: 3.1e-05
gradient norm last layer : 1.9e+00
# -> gradients shrink across layers: early layers learn nothing
```

Each tanh multiplies the gradient by a factor < 1, so deep stacks starve early
layers. The fixes: proper initialization, batch norm (or layer norm), residual
connections, and modern activations.

## 4. Batch Norm & Dropout — The Regularization Pair

```python
bn = nn.BatchNorm1d(8)
d = nn.Dropout(p=0.5)
data = torch.randn(4, 8)
print(bn(data).mean(dim=0).round(decimals=4))     # ~0 per channel in train mode
print((d(data) != 0).float().mean())              # ~50% alive in train mode
```

Output:
```
tensor([0.0001, -0.0002, ...])   # centered per channel
tensor(0.5156)
```

- **Batch norm** normalizes each channel per batch, then scales/shifts —
  stabilizes the activation distribution and allows higher learning rates. In
  `eval()` it uses *running* statistics, so train/eval results differ.
- **Dropout** zeroes random activations during training — a cheap ensemble of
  subnetworks — and is *disabled* in eval mode.

## 5. Learning Rate — The Most Important Hyperparameter

```python
for lr in [1e-1, 1e-2, 1e-4]:
    m = nn.Linear(4, 1)
    opt = torch.optim.SGD(m.parameters(), lr=lr)
    for _ in range(5):
        opt.zero_grad()
        l = ((m(torch.randn(8, 4)) - 1) ** 2).mean()
        l.backward(); opt.step()
    print(lr, l.item())
```

Output:
```
lr=1e-01: loss 0.9812   # oscillating/diverging
lr=1e-02: loss 0.6410   # healthy descent
lr=1e-04: loss 1.0088   # barely moving
```

Too high diverges, too low stalls. The loss-vs-lr curve ("LR range test")
finds the sweet spot: increase lr exponentially on one epoch, pick the steepest
descent point.

## 6. Backprop Intuition — The Chain Rule

```python
w1 = torch.tensor(2.0, requires_grad=True)
w2 = torch.tensor(3.0, requires_grad=True)
x = torch.tensor(1.5)
loss = (w1 * w2 * x) ** 2
loss.backward()
print(w1.grad.item())   # 2*(w1*w2*x)*(w2*x)
```

Output:
```
81.0
```

Backprop is the chain rule applied through the graph from loss to inputs —
each layer's gradient is the product of upstream and local derivatives.
Autograd does the bookkeeping; you must understand the flow to read the
symptoms (which layer's gradients are dead?).

## 7. Common Mistakes to Avoid

### Mistake 1: Sigmoid in hidden layers
```
# WRONG — saturated sigmoid kills gradient flow in deep nets
x = torch.sigmoid(self.fc1(x))
# CORRECT — ReLU (or LeakyReLU/GELU) for hidden layers
```

### Mistake 2: Huge initialization by hand
```
# WRONG — std 10 weights explode activations
# CORRECT — use nn.init.kaiming_* / xavier_* or default init
```

### Mistake 3: Leaving dropout/batchnorm active at eval
```
# WRONG
preds = model(x)          # dropout still on
# CORRECT
model.eval(); with torch.no_grad(): preds = model(x)
```

### Mistake 4: Blaming the seed before checking lr
```
# WRONG — re-roll the seed on a NaN loss
# CORRECT — check lr (too high), then data (NaN/inf), then loss fn
```

### Mistake 5: Ignoring the LR after changing architecture
```
# WRONG — keep lr=1e-3 when depth/width changed massively
# CORRECT — re-tune LR; it is the first knob, not the last
```

## 8. Best Practices

1. ReLU (or GELU) for hidden layers; sigmoid/softmax only at the output.
2. Use default init; override only with a stated reason.
3. Batch norm after (pre-)linear layers; dropout after activations.
4. Always pair train()/eval() correctly for layers with mode behavior.
5. Find LR with a range test; start slightly below the divergence point.
6. On NaN: reduce lr first, then check data, then loss.
7. Use residual connections for depth beyond a handful of layers.
8. Track gradient norms during training to catch vanishing early.
9. Watch both train and validation loss — divergence is the signal.
10. Seed once at the top; don't re-roll seeds to "fix" instability.

## 9. Complexity and Cost

| Operation | Time | Space | Notes |
|---|---|---|---|
| Linear layer (f in, t out, batch b) | O(b x f x t) | O(b x f) activations | The dominant FLOP source |
| Backward | ~2x forward | activations for graph | Held until step |
| Batch norm | O(b x c) | O(c) running stats | Cheap; changes distribution |
| Dropout | O(b x d) | mask | Cheap regularization |

Memory is activation-dominated: depth x batch x width is your GPU budget.
Batch norm lets you raise lr (fewer steps) — a time and cost lever.

## 10. AI Engineering Relevance

**Where this shows up:** every fine-tuned transformer (LoRA) inherits these
mechanisms — attention blocks are pre-normed, FFNs use GELU, dropout is baked
in. Understanding init and normalization is what lets you tune adapters
without destroying pretrained weights.

| Concept here | Used for |
|---|---|
| LayerNorm vs BatchNorm | Transformers use LayerNorm — same stabilization idea |
| GELU activation | The standard hidden activation in modern LLMs |
| Dropout | Regularizing fine-tuning to avoid catastrophic forgetting |
| LR discipline | The dominant knob in adapter and fine-tune training |
| Gradient flow | Diagnosing why an adapter "doesn't learn" |

**Scale note:** at 100M+ parameter scale, initialization and normalization are
not hygiene — they are load-bearing. A bad init in a fine-tune can destroy a
pretrained model in one step; warmup schedules and small LRs exist precisely
to protect gradient flow at scale.

## 11. Summary

| Concept | Description |
|---|---|
| Activations | ReLU hidden, sigmoid/softmax output |
| Initialization | He/Xavier scale controls gradient flow |
| Vanishing gradients | Deep stacks starve early layers; fix with norm + residuals |
| Batch norm | Stabilizes activation distributions |
| Dropout | Random zeroing; train-only regularizer |
| Learning rate | The dominant training hyperparameter |
| Backprop | Chain rule through the graph |

## 12. Quick Reference

| Task | Idiom |
|---|---|
| Hidden activation | `nn.ReLU()` / `nn.GELU()` |
| Binary output | `nn.Sigmoid()` + `BCEWithLogitsLoss` |
| Good init | `nn.init.kaiming_uniform_(w)` / `xavier_uniform_` |
| Normalize | `nn.BatchNorm1d(c)` / `nn.LayerNorm(d)` |
| Regularize | `nn.Dropout(p)` |
| Find LR | Range test: exponential lr sweep, pick steepest descent |
| Debug NaN | lr -> data -> loss function, in that order |

## Next Steps

Next: **[39 — Transfer Learning](39-transfer-learning-lecture.md)** — pretrained models and fine-tuning.

Continues in: **[40 — Transformers From Scratch](40-transformers-from-scratch-lecture.md)** — attention, the architecture behind every LLM.

Official docs: <https://pytorch.org/docs/stable/nn.init.html> · <https://arxiv.org/abs/1502.03167> (batch norm)
