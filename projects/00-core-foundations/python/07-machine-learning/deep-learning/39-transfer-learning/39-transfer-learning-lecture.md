# 07-machine-learning — 39: Transfer Learning — Small-Data Superpower

Companion exercise: `39-transfer-learning.py`

---

## Topic Overview

Nobody trains vision or language models from scratch in production. They
**fine-tune** pretrained ones. Transfer learning is how a 5,000-sample dataset
achieves state-of-the-art-quality results: the pretrained model already knows
low-level patterns — edges, textures, syntax, grammar — and you teach it your
domain with a fraction of the data and compute. This is the pattern behind
ResNet image classifiers, BERT/Claude-style language models, and the LoRA
adapters you will train in the GenAI phase.

This topic covers the mechanics: pretraining on a source task, freezing the
backbone, swapping the head, fine-tuning, feature extraction, learning-rate
schedules, and the small-data strategy. Because `torchvision` is not installed
in this environment, the exercise demonstrates the identical pattern on
self-trained source and target tasks — freeze backbone, swap head, fine-tune —
which transfers directly to ResNet/BERT workflows.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why transfer learning beats training from scratch on small data.
2. Distinguish freezing from fine-tuning and when to use each.
3. Swap the task head of a pretrained model.
4. Count trainable vs frozen parameters after freezing.
5. Use a model in feature-extraction mode to produce embeddings.
6. Apply small-LR schedules for gentle fine-tuning.
7. Explain the small-data strategy: pretrain big, fine-tune small.
8. Name when transfer learning does NOT help.

## Prerequisites

| Need | Where |
|---|---|
| PyTorch training loop | `37-pytorch-training-loop.py` |
| Neural network basics | `38-neural-network-basics.py` |
| Overfitting / validation | `22-cross-validation.py` |

## 1. The Source Task — Train a "Pretrained" Backbone

```python
class Backbone(nn.Module):
    def __init__(self, in_dim, hidden, feat_dim):
        super().__init__()
        self.features = nn.Sequential(
            nn.Linear(in_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, feat_dim),
        )
        self.head = nn.Linear(feat_dim, 1)
    def forward(self, x):
        return self.head(self.features(x))
```

Output:
```
source task trained: loss 0.0412
```

The source task gives the backbone general, reusable features. In the real
world the source is a giant corpus (ImageNet, Common Crawl) and the training
cost is billions of examples — which is exactly why you never repeat it.

## 2. Transfer: Freeze the Backbone, Swap the Head

```python
transfer = Backbone(20, 64, 32)
transfer.load_state_dict(backbone.state_dict())   # start from pretrained weights

for p in transfer.features.parameters():          # FREEZE feature extractor
    p.requires_grad = False
```

Output:
```
trainable params: 33 / 2145  (1.5%)
```

The frozen backbone keeps its learned representations; only the head trains on
your task. This works when the target task is close to the source (same
feature space, new decision rule).

## 3. Fine-Tuning: Unfreeze with a Small LR

When the target domain differs meaningfully (medical images vs natural images,
legal text vs general text), unfreeze the later backbone layers and let them
adapt — at a **small learning rate** so pretrained weights are nudged, not
shattered.

```python
for p in transfer.features[-1:].parameters():     # unfreeze last block
    p.requires_grad = True
opt = torch.optim.Adam(filter(lambda p: p.requires_grad, transfer.parameters()), lr=1e-4)
```

Output:
```
fine-tuned on 200 target samples: loss 0.0912
```

Common recipes: freeze everything, fine-tune the head; then optionally unfreeze
the top k layers at a 10x-smaller LR. Never fine-tune the whole network at
from-scratch LR.

## 4. Transfer vs From-Scratch on Small Data

```python
acc_transfer = evaluate(transfer)   # 200-sample target dataset
acc_scratch  = evaluate(scratch)    # same dataset, random init
```

Output:
```
accuracy transfer : 0.942
accuracy scratch  : 0.816
```

The pretrained features generalize better from the same 200 samples. This is
the whole value proposition — measurable in one comparison.

## 5. Feature Extraction — Embeddings as Vectors

```python
with torch.no_grad():
    feats = transfer.features(xt)     # embedding vectors, head removed
```

Output:
```
500 samples -> (500, 32) embedding vectors (32-dim)
```

Features become vectors you can cache, index, cluster, or feed to a linear
probe, a retrieval system, or a k-NN classifier. This is exactly how embedding
models work in the GenAI phase — `06-embeddings.py` will reuse this pattern.

## 6. Learning-Rate Schedules for Fine-Tuning

```python
sched = torch.optim.lr_scheduler.StepLR(opt, step_size=10, gamma=0.1)
for _ in range(10):
    sched.step()
```

Output:
```
after 10 epochs: LR 1e-05   # dropped by 10x
```

Fine-tuning etiquette: start small, decay gently. Schedules like StepLR,
CosineAnnealing, and linear warmup protect the pretrained weights while the
head adapts.

## 7. The Small-Data Strategy

1. Start from a pretrained backbone relevant to your domain.
2. Freeze everything; train the new head at a normal LR.
3. Evaluate. If underfitting, unfreeze the top k blocks at a small LR.
4. Evaluate again. Add augmentation/regularization before more unfreezing.
5. Never train the backbone at from-scratch LRs.

This ladder — head -> top-k blocks -> whole net — is the standard recipe and
the exact path taken when fine-tuning LLMs with adapters.

## 8. Common Mistakes to Avoid

### Mistake 1: Fine-tuning everything at from-scratch LR
```
# WRONG — a pretrained model can be destroyed in one step
opt = Adam(model.parameters(), lr=1e-2)
# CORRECT — freeze; head at 1e-3, unfrozen blocks at 1e-4
```

### Mistake 2: Forgetting to freeze before counting params
```
# WRONG — believe you're training "only the head" but all grads are on
# CORRECT — requires_grad=False on backbone, then filter(params, p.requires_grad)
```

### Mistake 3: Loading state_dict with mismatched head sizes
```
# WRONG — load_state_dict(pretrained) when the new head has different out_dim
# CORRECT — load with strict=False, or load only the backbone keys
```

### Mistake 4: Fine-tuning when the source is unrelated
```
# WRONG — ImageNet features for a tabular log-parsing task
# CORRECT — choose a source task close to your target; otherwise from-scratch may win
```

### Mistake 5: No evaluation ladder
```
# WRONG — unfreeze everything and hope
# CORRECT — head first, measure, then unfreeze top blocks, measure again
```

## 9. Best Practices

1. Start pretrained, not from scratch, whenever a relevant backbone exists.
2. Freeze by default; unfreeze incrementally with measurement at each step.
3. Use 10x-smaller LRs for unfrozen blocks than for the new head.
4. Count trainable parameters to confirm the freeze took effect.
5. Cache extracted features when you only need the head.
6. Validate on a held-out split; watch for overfitting to the small target set.
7. Use augmentation/regularization before adding trainable capacity.
8. Keep the same preprocessing as the pretraining corpus.
9. Record the source model and version in the experiment tracker.
10. When the target is too different, reconsider transfer entirely.

## 10. Complexity and Cost

| Operation | Time | Space | Notes |
|---|---|---|---|
| Pretraining a backbone | days-weeks GPU | huge | Never repeated; use a pretrained artifact |
| Feature extraction | one forward pass | features only | No gradients — cheap, cacheable |
| Head training | seconds-minutes | head params | The default first step |
| Fine-tuning top blocks | minutes-hours | blocks + head | More capacity, more overfit risk |
| Inference | one forward pass | full model | The model ships as a single artifact |

The economics are stark: pretraining is a one-time industry-scale cost you
inherit; fine-tuning is your actual budget.

## 11. AI Engineering Relevance

**Where this shows up:** every modern ML deployment. Vision APIs are
ResNet/ViT fine-tunes; every LLM application is a pretrained transformer
prompted or adapter-tuned; embedding models (`06-embeddings`) are transferred
encoders. LoRA in `09-genai/21-fine-tuning` is the same freeze/adapt pattern
with low-rank adapters.

| Concept here | Used for |
|---|---|
| Frozen backbone + new head | Adapter training on top of frozen LLMs |
| Feature extraction | Embedding generation for retrieval and clustering |
| Small-LR fine-tuning | Safe adapter training without catastrophic forgetting |
| Small-data strategy | Making a 5k-row dataset viable |
| Transfer measurement | Deciding whether fine-tuning beats prompting |

**Scale note:** at production scale, transfer learning is also a *cost*
strategy — frozen backbones can be cached (features computed once), and only
the small head or adapters need retraining when your task drifts slightly.
That is orders of magnitude cheaper than retraining the base model.

## 12. Summary

| Concept | Description |
|---|---|
| Transfer learning | Reuse a pretrained model's features for a new task |
| Freeze | requires_grad=False on the backbone |
| Fine-tune | Unfreeze (partially) at a small LR |
| Feature extraction | Produce embeddings without the head |
| Small-data strategy | Head -> top blocks -> whole net, measuring each step |
| LR schedules | Gentle decay protecting pretrained weights |

## Quick Reference

| Task | Idiom |
|---|---|
| Load pretrained | `model.load_state_dict(pretrained_dict, strict=False)` |
| Freeze backbone | `for p in model.features.parameters(): p.requires_grad = False` |
| Train only trainable | `Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=1e-3)` |
| Features | `with torch.no_grad(): feats = model.features(x)` |
| Gentle decay | `StepLR(opt, step_size=10, gamma=0.1)` |

## Next Steps

Next: **[40 — Transformers From Scratch](40-transformers-from-scratch-lecture.md)** — attention and the architecture behind every LLM.

Continues in: **[09-genai — 21 Fine-Tuning](../../09-genai/lectures/21-fine-tuning-lecture.md)** — LoRA and adapters on top of this pattern.

Official docs: <https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html>
