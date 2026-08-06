# Transfer Learning — Glossary 39

Companion lecture: `39-transfer-learning-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Adapter | Technique | A small trainable module added to a frozen pretrained model |
| Backbone | Model | The pretrained feature extractor reused for a new task |
| Catastrophic forgetting | Failure | Destroying pretrained knowledge by training too aggressively |
| Embedding | Output | The feature vector produced by the backbone without the head |
| Feature extraction | Technique | Using the frozen backbone as a fixed vectorizer |
| Fine-tuning | Technique | Training (parts of) the pretrained model on the target task |
| Freeze | Technique | Setting requires_grad=False to stop weight updates |
| Head | Model | The task-specific output layers swapped onto the backbone |
| Linear probe | Technique | Training a linear classifier on frozen features |
| LoRA | Technique | Low-rank adapters for efficient LLM fine-tuning |
| Pretraining | Phase | The expensive source-task training that creates the backbone |
| Small-data strategy | Recipe | Head -> top blocks -> whole net, measuring at each step |
| Source task | Phase | The task that produced the reusable features |
| Target task | Phase | The task you actually need to solve |
| Transfer learning | Technique | Reusing features learned on a source task for a target task |
| Warmup | Schedule | Gradually ramping the LR at the start of fine-tuning |
| state_dict | Mechanics | The mapping of parameter names to tensors, used by load/save |

## Detailed Definitions

### Adapter
**Definition**: A small trainable module inserted into or beside a frozen
pretrained model, so only the adapter (not the backbone) is updated. LoRA is
the dominant adapter family for LLMs.
**Related**: LoRA, Fine-tuning

### Backbone
**Definition**: The pretrained feature extractor portion of a model, reused
(possibly frozen) for a new task.
**Example**:
```python
backbone.features     # the reusable part; head is task-specific
```
**Related**: Head, Pretraining

### Catastrophic forgetting
**Definition**: The destruction of pretrained knowledge when fine-tuning with
too large a learning rate or too much data pressure. Prevention: small LRs,
frozen backbones, adapters.
**Related**: Fine-tuning, Learning rate

### Embedding
**Definition**: The dense vector representation of an input produced by the
backbone without the task head — the input to retrieval, clustering, or a
linear probe.
**Example**:
```python
with torch.no_grad():
    feats = model.features(x)   # (N, d) embeddings
```
**Related**: Feature extraction, Linear probe

### Feature extraction
**Definition**: Using the frozen backbone as a fixed vectorizer — one forward
pass, no gradients, cacheable output.
**Related**: Embedding, Freeze

### Fine-tuning
**Definition**: Continuing training of (part of) a pretrained model on the
target task, at a small learning rate to protect pretrained weights.
**Related**: Freeze, Transfer learning

### Freeze
**Definition**: Setting `requires_grad=False` so a parameter is not updated
during training.
**Example**:
```python
for p in model.features.parameters():
    p.requires_grad = False
```
**Related**: Fine-tuning, Parameters

### Head
**Definition**: The task-specific output layers (classifier, regression head)
attached to the shared backbone; swapped per task.
**Related**: Backbone

### Linear probe
**Definition**: Training a linear classifier on frozen features to evaluate
feature quality or to classify without fine-tuning the backbone.
**Related**: Feature extraction, Embedding

### LoRA
**Definition**: Low-Rank Adaptation — freezing base weights and training small
low-rank update matrices, the standard efficient fine-tuning method for LLMs.
**Related**: Adapter, Fine-tuning

### Pretraining
**Definition**: The source-task training (huge data, huge cost) that produces a
reusable backbone; done once, inherited everywhere.
**Related**: Source task, Backbone

### Small-data strategy
**Definition**: The fine-tuning ladder for limited target data: freeze all and
train the head, then progressively unfreeze top blocks, measuring performance
at every rung.
**Related**: Fine-tuning, Transfer learning

### Source task
**Definition**: The task whose training produced the features you reuse (e.g.,
ImageNet, Common Crawl).
**Related**: Pretraining

### Target task
**Definition**: The actual problem you need to solve with the transferred
model (e.g., your classification, your QA).
**Related**: Transfer learning

### Transfer learning
**Definition**: Applying knowledge learned on one task to improve learning on
another, typically by reusing pretrained features.
**Related**: Fine-tuning, Feature extraction

### Warmup
**Definition**: Ramping the learning rate from near zero over the first steps
or epochs, protecting the pretrained weights from early large updates.
**Related**: Fine-tuning, Learning rate

### state_dict
**Definition**: A dict mapping parameter names to tensors; used to save,
load, and transfer weights between models.
**Example**:
```python
model.load_state_dict(pretrained.state_dict(), strict=False)
```
**Related**: Backbone, Fine-tuning

## Key Concepts Summary

### The transfer recipe
- Pretrain once (expensive), reuse everywhere.
- Freeze the backbone; train the head.
- Unfreeze top blocks only when needed, at 10x-smaller LRs.

### Mechanics
- requires_grad=False freezes; filter trainable params for the optimizer.
- load_state_dict with strict=False when head sizes differ.
- Feature extraction: one forward pass, no gradients, cacheable.

### Decision rules
- Relevant source task: transfer wins on small data — measure it.
- Unrelated source: from-scratch may win; reconsider.
- Protect pretrained knowledge: small LRs, warmup, adapters.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. The pretrained feature extractor being reused — ___
2. Setting requires_grad=False on parameters — ___
3. The task-specific output layers swapped per task — ___
4. Producing vectors with the frozen backbone — ___
5. The fine-tuning ladder for small data — ___
6. Destroying pretrained knowledge by aggressive training — ___
7. The expensive training that created the backbone — ___
8. Low-rank update matrices for LLM fine-tuning — ___

**Answers:** 1-backbone, 2-freeze, 3-head, 4-feature extraction,
5-small-data strategy, 6-catastrophic forgetting, 7-pretraining, 8-LoRA
