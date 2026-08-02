# Fine-Tuning — Glossary 21

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Adapter | Tuning | A small trainable module over frozen weights |
| Epoch | Training | One full pass over the training set |
| Eval Loss | Training | Loss on held-out data; overfit detector |
| Fine-Tuning | Tuning | Further training a model on your data |
| Instruction Tuning | Data | Training on instruction/input/output triples |
| LoRA | Tuning | Low-rank adapters for efficient tuning |
| Overfitting | Failure | Memorizing training data, failing new data |
| Prompt Engineering | Alternative | Adapting behavior at inference time |

## Detailed Definitions
### Adapter
**Definition**: A compact trainable layer stack attached to frozen base
weights.
**Related**: LoRA

### Epoch
**Definition**: One complete pass through the training dataset.
**Related**: Eval Loss

### Eval Loss
**Definition**: Loss on the held-out set; rising while train loss falls signals
overfitting.
**Related**: Overfitting

### Fine-Tuning
**Definition**: Continued training of a pretrained model on task-specific
data.
**Related**: LoRA

### Instruction Tuning
**Definition**: Fine-tuning on instruction/input/output triples to teach task
behavior.
**Related**: Fine-Tuning

### LoRA
**Definition**: Freezing base weights and training low-rank adapters - a
fraction of the cost of full tuning.
**Related**: Adapter

### Overfitting
**Definition**: The model memorizes training examples and generalizes poorly.
**Related**: Eval Loss

### Prompt Engineering
**Definition**: The cheaper alternative: adapting behavior via prompts, not
weights.
**Related**: Fine-Tuning

## Key Concepts Summary
### The Decision
- Prompt first; fine-tune with evidence

### The Rules
- Quality data over quantity
- LoRA by default
- Always evaluate against baseline

## Practice Terms
Match each term to its definition (answers at the bottom).
1. LoRA — ___
2. Overfitting — ___
3. Eval loss — ___
4. Instruction tuning — ___
5. Adapter — ___

**Answers:** 1-c, 2-e, 3-b, 4-a, 5-d where a=triple-based training, b=held-out
loss, c=low-rank tuning, d=trainable module, e=memorization failure.
