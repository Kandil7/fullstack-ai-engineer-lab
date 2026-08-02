# Inference Optimization — Glossary 08

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Accuracy Cost | Optimization | The quality lost for a speed/size win |
| Batching | Optimization | Running many inputs in one call |
| Distillation | Optimization | Training a small model to mimic a large one |
| fp16 | Optimization | 16-bit half-precision floats |
| int8 | Optimization | 8-bit integer quantization |
| Latency Curve | Optimization | Measured latency vs accuracy per candidate |
| ONNX | Optimization | Portable model graph format |
| Pruning | Optimization | Removing low-importance weights |
| Quantization | Optimization | Reducing bit width of weights |
| Throughput | SLO | Predictions per second |

## Detailed Definitions
### Accuracy Cost
**Definition**: The measurable drop in quality a technique trades for speed.
**Related**: Latency Curve

### Batching
**Definition**: Processing N inputs together to amortize fixed cost.
```python
per_item = (base + N * unit) / N
```
**Related**: Throughput

### Distillation
**Definition**: Training a smaller "student" model to reproduce a larger
"teacher's" outputs.
**Related**: Pruning

### fp16
**Definition**: 16-bit floats - half the size of fp32, faster on modern GPUs.
**Related**: Quantization

### int8
**Definition**: 8-bit integers - 1/4 the size of fp32; often 2-4x faster.
**Related**: Quantization

### Latency Curve
**Definition**: The measured relationship between a technique and latency vs
accuracy - the evidence for choosing.
**Related**: Accuracy Cost

### ONNX
**Definition**: An open, portable format for trained models, optimized by ONNX
Runtime.
**Related**: Quantization

### Pruning
**Definition**: Removing weights with negligible contribution to shrink the
model.
**Related**: Distillation

### Quantization
**Definition**: Representing weights with fewer bits (int8, fp16).
**Related**: int8

### Throughput
**Definition**: Predictions completed per second; the other half of the
latency/throughput tradeoff.
**Related**: Batching

## Key Concepts Summary
### The Optimization Trio
- Quantization (smaller/faster)
- Pruning (sparser)
- Distillation (smaller model)

### The Rule
- Measure accuracy cost AND latency gain before shipping

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Quantization — ___
2. Batching — ___
3. Pruning — ___
4. Distillation — ___
5. Throughput — ___

**Answers:** 1-b, 2-c, 3-d, 4-e, 5-a where a=predictions/sec, b=bit-width
reduction, c=grouped requests, d=weight removal, e=small-model-from-big.
