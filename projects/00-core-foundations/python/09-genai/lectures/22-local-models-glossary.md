# Local Models — Glossary 22

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Fallback | Architecture | Escalation to a stronger model on weak results |
| Inference | Serving | Running a model to produce an output |
| License | Governance | Terms governing model weights use |
| Open-Weight | Model | Models with publicly available weights |
| Params | Model | The model's weight count (7B = 7 billion) |
| Quantization | Optimization | Storing weights in fewer bits |
| Tokenizer | Model | Text ↔ token IDs conversion |
| VRAM | Hardware | GPU memory that holds the model |

## Detailed Definitions
### Fallback
**Definition**: A designed path to a stronger model when local quality fails
a check.
**Related**: Inference

### Inference
**Definition**: The forward pass producing output for an input.
**Related**: Tokenizer

### License
**Definition**: Legal terms for using model weights; check before production.
**Related**: Open-Weight

### Open-Weight
**Definition**: Weights released for download and local execution.
**Related**: License

### Params
**Definition**: The count of trainable parameters; size/strength proxy.
**Related**: VRAM

### Quantization
**Definition**: Reducing weight precision (fp16→int8→int4) to save memory.
**Related**: VRAM

### Tokenizer
**Definition**: The component converting text to token IDs for the model.
**Related**: Inference

### VRAM
**Definition**: GPU memory; must hold model weights plus activations.
**Related**: Quantization

## Key Concepts Summary
### The Trade
- Privacy/cost vs quality/effort

### The Rules
- Check licenses
- Quantize to fit, validate quality
- Always have a fallback

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Quantization — ___
2. Params — ___
3. Open-weight — ___
4. VRAM — ___
5. Fallback — ___

**Answers:** 1-c, 2-e, 3-b, 4-a, 5-d where a=GPU memory, b=public weights,
c=bit reduction, d=stronger model path, e=weight count.
