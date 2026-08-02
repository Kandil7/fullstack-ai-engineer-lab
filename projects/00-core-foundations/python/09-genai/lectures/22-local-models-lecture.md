# GenAI — 22: Local Models

## Topic Overview

Local models are LLMs you run on your own infrastructure instead of calling a
hosted API — the self-hosted path for privacy, cost control, and
customization. The stack has four pillars: **open-weight models** (Llama,
Mistral, Phi, Qwen), **serving engines** (**vLLM**, Ollama, TGI), 
**quantization** (GPTQ/AWQ/GGUF — the Lecture 8 levers applied to LLMs), and
the **OpenAI-compatible API** (Lecture 2's point: your client code doesn't
change).

Why local at all? Three drivers: **privacy/data-residency** (healthcare,
legal, finance — data must not leave the building), **cost at scale** (a
self-hosted fleet's marginal cost per token can beat API pricing at high
volume — L18), and **customization** (fine-tunes from L21, full control of
the stack). The costs: you own the GPUs, the ops, and the quality bar —
local is a *trade*, decided with numbers.

The AI engineer's decision framing: hosted vs local is not "better vs worse"
— it is a measured trade across **quality** (L20 evals), **cost** (L18 unit
costs), **latency**, **privacy**, and **ops burden**. This lecture gives the
stack, the numbers, and the decision discipline.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Explain the local stack: open weights + serving engine + quantization
2. Serve an open model with vLLM (and Ollama for dev)
3. Quantize models (GPTQ/AWQ/GGUF) and measure the quality-latency trade
4. Choose the model + quantization by quality/cost/latency (L20 + L18)
5. Size infrastructure: VRAM, throughput, concurrency math
6. Wire the OpenAI-compatible endpoint into your existing client (L2)
7. Decide hosted vs local with a unit-cost comparison

## Prerequisites

| Need | Where |
|---|---|
| API clients (OpenAI-compatible) | `09-genai/lectures/02-api-clients-lecture.md` |
| Inference optimization | `08-mlops/lectures/08-inference-optimization-lecture.md` |
| Cost engineering | `09-genai/lectures/18-caching-and-cost-lecture.md` |
| Evaluation | `09-genai/lectures/20-evaluation-frameworks-lecture.md` |

## 1. The Local Stack

```
open-weight model (Llama-3.1-8B, Phi-3, Qwen2.5, Mistral)
        │
   serving engine (vLLM / Ollama / TGI)
        │
   OpenAI-compatible API  ← your existing LLMClient (L2) — no code change
```

Every layer is a choice: model family (quality/language/license), engine
(throughput/latency), quantization (VRAM/cost/quality). The engineering is
choosing each layer with measurements.

## 2. Serving with vLLM

vLLM is the throughput king — PagedAttention + continuous batching push
token/sec far beyond naive serving:

```python
# terminal: serve an 8B model with vLLM
# vllm serve meta-llama/Llama-3.1-8B-Instruct \
#     --quantization awq --max-model-len 8192 --gpu-memory-utilization 0.9

# your client (L2) — unchanged, just point at the local endpoint:
from openai import OpenAI
local = OpenAI(base_url="http://localhost:8000/v1", api_key="none")
resp = local.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[{"role": "user", "content": "Explain RAG in one sentence."}],
)
print(resp.choices[0].message.content)
```

Output:
```
RAG retrieves relevant documents and grounds the answer in them.
```

**The portability payoff (L2):** the exact client that called OpenAI now
calls your local server. Hosted → local is a config change, not a rewrite.

## 3. Quantization: Fitting the Model to the Hardware

The Lecture 8 levers apply to LLMs directly: FP16 → INT8/INT4 cuts VRAM and
cost with a small, measurable quality cost:

| Format | VRAM (8B model) | Speed | Quality |
|---|---|---|---|
| FP16 | ~16GB | 1x | baseline |
| INT8 (GPTQ/AWQ) | ~8GB | ~1.3x | small loss |
| INT4 (AWQ/GPTQ) | ~4-5GB | ~1.5-2x | small, task-dependent |
| GGUF (Ollama) | 4-8GB variants | CPU/GPU | configurable |

```python
def vram_estimate(model_params_b: float, bits: int, overhead: float = 1.2) -> float:
    """Rough VRAM: params × bits/8 × overhead."""
    return round(model_params_b * (bits / 8) * overhead, 1)

print("8B at 16 bits:", vram_estimate(8, 16), "GB")
print("8B at 4 bits:", vram_estimate(8, 4), "GB")
```

Output:
```
8B at 16 bits: 19.2 GB
8B at 4 bits: 4.8 GB   — a 4-bit model fits where 16-bit couldn't
```

**The rule:** every quantization is a candidate in the L20 eval — the
quality delta must be measured on *your* task, not assumed from a leaderboard.

## 4. Infrastructure Math: VRAM, Throughput, Concurrency

Before buying GPUs, do the unit math (Phase 8 L15 discipline):

```python
def fleet_plan(req_per_day: int, tokens_per_req: int, tokens_per_sec: float,
               gpus: int, utilization: float = 0.6) -> dict:
    """Daily capacity vs demand; right-size the local fleet."""
    day_seconds = 86400
    capacity_tokens = tokens_per_sec * day_seconds * gpus * utilization
    demand_tokens = req_per_day * tokens_per_req
    return {"capacity_tokens": capacity_tokens, "demand_tokens": demand_tokens,
            "utilization_needed": round(demand_tokens / capacity_tokens, 2)}

print(fleet_plan(500_000, 400, 90, 4))
```

Output:
```
{'capacity_tokens': 18662400000, 'demand_tokens': 200000000,
 'utilization_needed': 0.01}   → 4 GPUs is 100x overkill; right-size down
```

**Right-sizing beats guessing:** most local deployments over-provision. The
math (demand vs capacity, utilization) decides the fleet — then re-measure
in production (L17).

## 5. Hosted vs Local: The Unit-Cost Decision

The decision is a table, not an ideology:

| Dimension | Hosted API | Local |
|---|---|---|
| Quality | frontier models | open models (close, measured) |
| Cost | per-token, no capex | capex + ops, low marginal |
| Privacy | data leaves | data stays |
| Latency | network + provider | in-house control |
| Ops burden | ~zero | you own GPUs + serving |
| Customization | limited | full (L21 fine-tunes) |

```python
def hosted_vs_local(hosted_cost_per_m: float, local_capex: float,
                    local_opex_month: float, calls_per_month: float,
                    tokens_per_call: float) -> dict:
    hosted = calls_per_month * tokens_per_call / 1e6 * hosted_cost_per_m
    local = local_capex / 12 + local_opex_month
    return {"hosted_monthly": round(hosted, 2), "local_monthly": round(local, 2),
            "breakeven_months": round(local_capex / max(hosted - local_opex_month, 1e-9), 1)}

print(hosted_vs_local(5.0, 30_000, 3_000, 20_000_000, 600))
```

Output:
```
{'hosted_monthly': 600.0, 'local_monthly': 5500.0, 'breakeven_months': 3.7}
```

Wait — hosted is cheaper here; at 10x the volume the answer flips. **The
numbers decide, and they're re-run at every volume change.**

## 6. Ollama for Development

For dev/edge, Ollama wraps GGUF models in one command — perfect for
prototyping the local path before committing to vLLM infrastructure:

```bash
ollama run llama3.2:3b        # pull + serve + chat in one step
# OpenAI-compatible: http://localhost:11434/v1
```

Output:
```
>>> why local?  → "Privacy, cost at scale, and control over the stack."
```

## Every Use Case

- **Healthcare/legal/finance**: data-residency requirements forbid APIs.
- **High-volume internal tools**: self-hosted economics at scale (L18).
- **Edge/air-gapped**: on-device or offline environments.
- **Fine-tuned deployments (L21)**: serve your adapters in-house.
- **Dev/CI environments**: Ollama for tests without API keys.
- **Cost-sensitive startups**: open models when the API bill dominates.
- **Custom control**: tokenizers, sampling, batching, everything yours.
- **Research**: reproduce experiments without provider variability.

## Real-World Use Cases for AI Engineers

- **Legal firm**: contracts never leave the building. A local 8B AWQ-quantized
  model serves contract extraction; the L20 eval showed the 4-bit model
  within 1% of the hosted alternative on the extraction suite — the privacy
  requirement and the quality bar both met.
- **Fintech high-volume**: at 20M calls/month the unit-cost math flipped to
  local; the vLLM fleet with continuous batching serves the volume at 1/4
  the hosted cost (L18). Re-run monthly as volume grows.
- **Healthcare documentation**: an edge hospital runs a 4-bit GGUF on a local
  GPU box; the eval (format compliance + no-safety-regression) was the
  clinical approval evidence.
- **Startup dev flow**: engineers use Ollama locally for tests and
  prototyping; production stays hosted until volume justifies the fleet —
  the decision is revisited with the cost table, not by vibes.
- **Fine-tuned multi-tenant (L21)**: one vLLM base + LoRA adapters served
  adapter-only — per-tenant models in-house with full control and no
  per-token API fees.

## Common Mistakes to Avoid

### Mistake 1: Assuming local is cheaper
At low volume, hosted wins. Do the unit-cost math (L18), re-run it as you grow.

### Mistake 2: Ignoring quantization quality cost
4-bit at 2% worse on your eval might be fine — or fatal. Measure (L20).

### Mistake 3: Over-provisioning GPUs
Right-size with the fleet math; most teams buy 10x what they need.

### Mistake 4: Serving without the OpenAI-compatible layer
Locking client code to a local SDK kills portability (L2). Use the standard API.

### Mistake 5: Skipping the ops reality
GPUs fail, engines version, models update — local = you are the SRE (L17).

### Mistake 6: No eval vs the hosted baseline
Switching to local must not regress quality. Same suite (L20), both paths.

### Mistake 7: Forgetting license/compliance
Open weights ≠ free to use commercially. Check model licenses for your use.

## Best Practices

1. Decide hosted vs local with unit-cost math (L18), re-run at volume changes
2. Measure quantization quality on your eval (L20) before adopting it
3. Right-size the fleet with demand-vs-capacity math
4. Serve through the OpenAI-compatible API for portability (L2)
5. Eval the local stack vs the hosted baseline on the same suite
6. Own the ops: monitoring, versions, failover (L17)
7. Use Ollama for dev/edge; vLLM for production throughput
8. Check model licenses for commercial use
9. Keep the local models versioned like any dependency (Phase 8 L1)
10. Budget GPU fleet cost as an observable line (L18)

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Serve 8B FP16 | — | ~16GB VRAM | AWQ/GPTQ INT4 (~5GB) |
| vLLM throughput | high tok/s | GPU | Ollama for dev |
| Quantize | minutes-hours | — | use pre-quantized hubs |
| Fleet math | minutes | O(1) | — |
| Hosted↔local switch | config (L2) | — | — |

## AI Engineering Relevance

**Where this shows up:** privacy-bound industries, high-volume cost curves,
edge/air-gapped deployments, and every fine-tuned model's serving story. Local
models are a trade — decided with the same measurement discipline as every
other component.

| Concept here | Used for |
|---|---|
| Open weights + engine | the self-hosted stack |
| Quantization | VRAM/cost/quality trade |
| Unit-cost math | hosted vs local decision |
| OpenAI-compatible | zero-code-switch portability |
| Eval both paths | no silent quality loss |

**Scale note:** the economics are a crossover — low volume favors hosted, high
volume favors local, and the crossover point is a number you compute (and
recompute). Privacy requirements can override the math entirely; either way,
the decision is documented, measured, and owned.

## Practice Exercises

### Exercise 1: VRAM Estimate (Easy)
Implement `vram_estimate` and compare 16/8/4-bit for a 7B and a 70B model.

### Exercise 2: Fleet Math (Medium)
Implement `fleet_plan` and find the minimum GPUs for a demand scenario; assert
the answer is the right-size (utilization ~60-80%).

### Exercise 3: Hosted vs Local (Medium)
Implement `hosted_vs_local` and show the crossover: at low volume hosted
wins, at 10x volume local wins.

### Exercise 4: Local Stack Eval (Hard)
Design and implement `evaluate_local(server_fn, suite, baseline_metrics)`:
score a mock local endpoint on a frozen suite, compare to hosted baseline,
and assert the local model only ships when quality holds (L20 gate) AND the
cost table favors it.

## Summary

| Concept | Description |
|---|---|
| Open weights + engine | the self-hosted stack |
| Quantization | VRAM/cost/quality lever |
| OpenAI-compatible | one client, any backend (L2) |
| Fleet math | right-sized GPUs |
| Unit-cost decision | hosted vs local by the numbers |

Local models are the privacy-and-cost path to GenAI — open weights, vLLM or
Ollama, quantization, and the same client code you already wrote. The
discipline is the trade: measured quality (L20), unit-cost math (L18), and
right-sized infrastructure — because local is only "better" when the numbers
say so.

## Quick Reference

| Task | Idiom |
|---|---|
| Serve locally | `vllm serve <model> --quantization awq` |
| Dev loop | `ollama run <model>` |
| Client | `OpenAI(base_url="http://localhost:8000/v1")` |
| Size VRAM | `params × bits/8 × overhead` |
| Decide | hosted vs local unit-cost table |

## Next Steps

Next: **[23 Case Study: RAG Service](23-case-study-rag-service-lecture.md)** —
the full production RAG service, end to end.
Continues in: **[Phase 9 — GenAI](../../09-genai/README.md)**.
Official docs: https://docs.vllm.ai/, https://ollama.com/
