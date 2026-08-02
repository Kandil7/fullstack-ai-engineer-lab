# MLOps — 08: Inference Optimization

## Topic Overview

Inference optimization is the discipline of making a trained model *fast and
cheap to run* at serving time without materially changing its predictions:
quantization (FP32→FP16/INT8), pruning, distillation, ONNX graph
optimizations, batching, and caching. The trained model's quality is a given;
inference optimization is where an ML engineer converts that quality into a
latency/cost budget the product can afford.

The leverage is enormous: a model that takes 25ms in Python may run in 2ms as
an ONNX FP16 graph on GPU or 1ms as INT8 on CPU — a 10-25x speedup with
negligible quality loss (or a tunable trade-off). For GPU serving, **batching**
is the single biggest lever: GPUs are throughput machines, and a batch of 32
predictions often costs barely more than a batch of 1.

Why this matters for an AI engineer: inference cost is a *recurring production
cost* — it is paid on every request, forever. The difference between a
naively served model and an optimized one is a difference in the company's
cloud bill and the user's perceived latency. This lecture gives you the
systematic playbook: measure first, then apply the cheapest effective lever.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Profile inference to find the real bottleneck (model vs preprocessing vs I/O)
2. Quantize a model to FP16/INT8 and measure the quality-latency trade-off
3. Use ONNX graph optimization (`graph_optimization_level`) safely
4. Apply dynamic batching for GPU serving
5. Prune and distill models for size reduction
6. Validate that optimizations preserved predictions (golden tests)
7. Build a decision playbook: which lever for which budget

## Prerequisites

| Need | Where |
|---|---|
| Model packaging | `08-mlops/lectures/05-model-packaging-lecture.md` |
| Model serving | `08-mlops/lectures/07-model-serving-lecture.md` |
| PyTorch basics | `07-machine-learning/` PyTorch lectures |
| Latency math | `08-mlops/lectures/07-model-serving-lecture.md` section 4 |

## 1. Measure First: The Optimization Playbook

Optimizing blind is guessing. The playbook is: **profile → identify the
bottleneck → apply the cheapest effective lever → validate → re-profile.**
Bottlenecks are usually one of: model compute (the weights), preprocessing
(feature engineering in Python), I/O (loading features from a DB), or the
framework overhead (Python interpreter for each op).

```python
import time

def profile_pipeline(preprocess_fn, predict_fn, sample, n=100):
    stages = {}
    t0 = time.perf_counter()
    for _ in range(n):
        x = preprocess_fn(sample)
    stages["preprocess_ms"] = ((time.perf_counter() - t0) / n) * 1000

    t0 = time.perf_counter()
    for _ in range(n):
        predict_fn(x)
    stages["predict_ms"] = ((time.perf_counter() - t0) / n) * 1000
    return stages

# profile output guides the next step:
# if predict_ms dominates → model optimization (quantization/ONNX/batching)
# if preprocess_ms dominates → vectorize with numpy/pandas, or move to batch
```

Output (conceptually):
```
{'preprocess_ms': 3.2, 'predict_ms': 21.4}   → optimize the model
```

## 2. Quantization: FP32 → FP16 → INT8

Quantization lowers numeric precision to reduce memory bandwidth and enable
vectorized instructions. The quality cost is usually small (≤1% relative error)
and the latency win is large.

| Precision | Size | CPU speedup | Notes |
|---|---|---|---|
| FP32 | 1.0x | 1.0x | baseline |
| FP16 (GPU) | 0.5x | ~2x on modern GPUs | negligible quality loss |
| INT8 (CPU/GPU) | 0.25x | 2–4x | small quality loss; needs calibration |
| FP16+INT8 | 0.25x | 3–6x | best on GPU with acceptable drift |

```python
# PyTorch: dynamic quantization (CPU) — 2-4x smaller/faster
import torch
model_int8 = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)
```

Output (conceptually):
```
model size: 250MB → 63MB, latency: 21ms → 7ms, acc: 0.918 → 0.916
```

**The golden rule:** every quantization step ships with a golden-output test
(Lecture 05) — the optimized model must agree with the FP32 model within a
declared tolerance on a frozen sample set. Optimization without validation is
how silent quality regressions happen.

## 3. ONNX Graph Optimization

ONNX runtime applies graph-level optimizations (operator fusion, constant
folding, memory planning) that a Python interpreter cannot. The same model
usually runs 2-5x faster through ONNX Runtime than raw Python/torch eager.

```python
import onnxruntime as ort

sess = ort.InferenceSession(
    "model.onnx",
    providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
    sess_options=ort.SessionOptions(),
)
sess_options = sess.get_session_options()
sess_options.graph_optimization_level = (
    ort.GraphOptimizationLevel.ORT_ENABLE_ALL
)
```

Output (conceptually):
```
ONNX Runtime: 21ms → 6ms on CPU, 21ms → 2.1ms on GPU
```

Note the **provider order**: CUDA first (preferred), CPU fallback — if a
provider is missing, the runtime falls through gracefully.

## 4. Dynamic Batching: The GPU Lever

GPUs amortize the kernel-launch overhead across a batch. Dynamic batching
collects requests for a few ms and predicts them together. Throughput scales
super-linearly with batch size up to the saturation point.

```python
def batched_predict(sess, inputs: list, batch_size: int = 32) -> list:
    """Predict in fixed batches; measure the per-batch time."""
    results = []
    for i in range(0, len(inputs), batch_size):
        batch = inputs[i:i + batch_size]
        results.extend(sess.run(None, {"X": batch})[0])
    return results

# empirical: batch of 32 on GPU ≈ 1.3x the time of batch of 1
# → 25x more work for 1.3x the time
```

Output (conceptually):
```
batch=1: 2.1ms/req → 476 QPS
batch=32: 2.8ms/req (amortized) → 11,400 QPS
```

Triton serves dynamic batching natively (`max_batch_size`, `dynamic_batching`
config); in DIY FastAPI you batch inside the worker queue.

## 5. Pruning and Distillation

For size-constrained deployments (edge, mobile, memory limits), reduce the
model itself:

- **Pruning**: zero out the smallest weights → sparser, smaller model.
- **Distillation**: train a small "student" to mimic a large "teacher" —
  a 10x smaller model within 1-2% of teacher quality on many tasks.

```python
# Structural pruning example (conceptual)
import torch.nn.utils.prune as prune
for name, module in model.named_modules():
    if isinstance(module, torch.nn.Linear):
        prune.l1_unstructured(module, name="weight", amount=0.3)
```

Output (conceptually):
```
pruned model: 80% zeros → 4x smaller file, 1.4x faster on CPU
```

Distillation is the AI-engineer's favorite because it produces a *smaller,
faster, still-quality* model that keeps the API contract unchanged — the
consumer never knows the model shrank.

## 6. The Decision Playbook

| Budget problem | Cheapest effective lever |
|---|---|
| Latency too high (CPU) | ONNX graph opt → INT8 quantization |
| Latency too high (GPU) | dynamic batching → FP16 |
| Memory/size constrained | INT8 → pruning → distillation |
| Throughput too low | batching → cache → scale pods |
| Cost too high | INT8 + batching, right-size the instance |
| Framework overhead | ONNX Runtime, avoid Python per-op overhead |

Always validate with golden outputs and the latency histogram (p50/p95/p99),
never just averages.

## Every Use Case

- **Real-time fraud/credit scoring**: shaving 15ms off p99 keeps the model in
  the transaction path.
- **High-QPS ranking**: INT8 + ONNX on CPU can serve 10k QPS without a GPU
  fleet — a direct cloud-bill win.
- **Mobile and edge**: 250MB model → 30MB via quantization + pruning fits on
  a phone.
- **GPU cost control**: batching lifts GPU utilization from 15% to 70%+,
  halving the serving fleet.
- **Serverless serving**: cold starts + latency budgets make every ms count;
  ONNX + INT8 are the standard lever.
- **Batch jobs**: faster inference shrinks nightly scoring windows.
- **Multi-tenant SaaS**: per-tenant latency isolation via batching policies.

## Real-World Use Cases for AI Engineers

- **Search ranking at a retailer**: the ranking model was 18ms in Python; the
  team exported to ONNX (6ms) and quantized to INT8 (2.5ms). p99 dropped below
  the 10ms search SLA, and the CPU-only fleet avoided a GPU purchase — the
  optimization *paid for itself*.
- **Fraud detection latency**: the endpoint sat in the payment path with a 40ms
  budget. Profiling showed 60% of the time was preprocessing in Python — the
  team vectorized preprocessing with numpy and moved it before the predict,
  meeting the budget without touching the model.
- **Healthcare edge sepsis model**: a 500MB torch model became a 60MB INT8
  ONNX model that runs on hospital edge hardware — the quantization golden
  test (agreement within 0.01 on 10k frozen samples) is what the clinical
  review accepted.
- **GPU fleet at a fintech**: dynamic batching lifted GPU utilization from 18%
  to 65%, cutting the serving bill ~3x with zero quality change — a quarterly
  cost review win.
- **LLM serving (Phase 9)**: the same levers apply to LLMs: FP16/INT8
  (GPTQ/AWQ), KV-cache optimization, and batching are exactly how a 100B model
  becomes economically servable.

## Common Mistakes to Avoid

### Mistake 1: Optimizing before profiling
Quantizing the model when the bottleneck is preprocessing wastes the lever.
Measure first.

### Mistake 2: No golden-output validation after quantization
A 1% silent quality drift is invisible in a latency test. Validate agreement
with the FP32 baseline.

### Mistake 3: INT8 without calibration
INT8 needs a calibration set to pick scales; naive conversion can spike error.

### Mistake 4: Optimizing the wrong layer
Distilling when batching would solve it — the playbook order matters.

### Mistake 5: Optimizing a cold model
Warm the model first; first-call latency (lazy init) is not steady-state.

### Mistake 6: Reporting averages only
p99 tells the real story; report the histogram.

## Best Practices

1. Profile before optimizing — the playbook starts with measurement
2. Golden-output validate every optimization step
3. Apply levers cheapest-first: ONNX → FP16 → INT8 → batching → pruning → distillation
4. Batch on GPU; cache repeated inputs on CPU
5. Use provider fallback order in ONNX Runtime
6. Quantize with a calibration set for INT8
7. Keep the FP32 artifact as the reference in the registry
8. Report p50/p95/p99 latency and QPS per configuration
9. Automate the comparison in CI (model + latency tests)
10. Document the trade-off table per model in the registry

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| ONNX export | minutes (once) | O(n) | — |
| INT8 quantization | minutes + calibration | 0.25x | FP16 first if GPU |
| Dynamic batching | config | O(batch) | — |
| Pruning | retrain/fine-tune | 0.3-0.5x | quantization if sufficient |
| Distillation | full student training | 0.1-0.3x | pruning if sufficient |

## AI Engineering Relevance

**Where this shows up:** every serving fleet's latency and cost SLOs; every
edge deployment; every GPU budget review.

| Concept here | Used for |
|---|---|
| Profiling | knowing which lever to pull |
| Quantization | size + latency at small quality cost |
| Batching | GPU throughput leverage |
| Golden validation | optimization without silent regression |

**Scale note:** at 1M predictions/day, a 10x latency/size improvement is a
10x reduction in the recurring serving cost — optimization is the AI
engineer's permanent budget lever.

## Practice Exercises

### Exercise 1: Profile and Decide (Easy)
Given a mock `profile_pipeline` output (preprocess 3ms, predict 21ms), choose
the right first lever and justify it in one sentence.

### Exercise 2: Quantization Trade-off (Medium)
Simulate FP32→FP16→INT8: given size and latency tables and a golden-tolerance
check, pick the best precision for a 2x latency budget with ≤1% error.

### Exercise 3: Batching Math (Medium)
Write `plan_batching(latency_batch1, batch_sizes, time_batch)` that returns
the batch size maximizing QPS under a latency-per-request budget.

### Exercise 4: Golden Validation (Hard)
Write `golden_validate(opt_predict, ref_predict, samples, tol)` that asserts
|opt - ref| ≤ tol on 1000 frozen samples and flags the first violating
sample — the CI gate for any optimization.

## Summary

| Concept | Description |
|---|---|
| Playbook | profile → lever → validate → re-profile |
| Quantization | FP16/INT8: size + latency, small quality cost |
| ONNX opt | graph fusion: 2-5x on CPU |
| Batching | the GPU throughput lever |
| Pruning/distillation | smaller models for size-constrained targets |

Inference optimization is the ML engineer's cost-and-latency lever: a
systematic, measurable playbook that turns "the model is too slow/expensive"
into a table of validated configurations. The discipline — measure, apply,
validate — is identical whether you're optimizing a 10MB tabular model or a
100B LLM.

## Quick Reference

| Task | Idiom |
|---|---|
| Profile | time preprocess vs predict separately |
| ONNX speedup | `onnxruntime.InferenceSession(providers=[...])` |
| INT8 PyTorch | `torch.quantization.quantize_dynamic(model, ...)` |
| GPU batching | Triton `dynamic_batching` or DIY worker queue |
| Validate | golden test: |opt - ref| ≤ tol on frozen samples |

## Next Steps

Next: **[09 Pipeline Orchestration](09-pipeline-orchestration-lecture.md)** —
orchestrating the training and serving pipelines as systems.
Continues in: **[Phase 8 MLOps](../../08-mlops/README.md)**.
Official docs: https://onnxruntime.ai/docs/performance/,
https://pytorch.org/docs/stable/quantization.html
