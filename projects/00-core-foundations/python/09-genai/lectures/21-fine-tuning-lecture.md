# GenAI — 21: Fine-Tuning

## Topic Overview

Fine-tuning is adapting a pretrained model to your task and domain by training
it further on your data — the "beyond prompting" lever when prompts and RAG
hit their ceiling. The modern practice is **PEFT** (Parameter-Efficient
Fine-Tuning): **LoRA** (Low-Rank Adaptation) trains a small set of adapter
weights instead of the full model, cutting compute and storage by orders of
magnitude while matching or approaching full fine-tuning quality. This lecture
covers the *when*, *how*, and *whether* of fine-tuning — because the most
important skill is knowing when NOT to fine-tune.

The decision ladder (measure at every rung — L20):

```
1. Prompting (L4) — zero cost, try first
2. RAG (L9) — add knowledge without retraining
3. Few-shot prompting — more examples
4. Fine-tuning (LoRA) — when format/tone/domain behavior is the problem
```

Fine-tuning changes **behavior** (format, style, tone, task adherence), not
**knowledge** (it cannot reliably add facts the base model lacks — that's
RAG's job). It shines when: your task has a distinct format the base model
won't reliably follow, your domain's style matters, or latency/cost demand a
smaller model that fine-tuning makes competent.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Decide when fine-tuning beats prompting/RAG (the decision ladder)
2. Prepare a fine-tuning dataset (format, quality, size, split)
3. Run LoRA fine-tuning with Hugging Face PEFT (or a provider API)
4. Choose LoRA hyperparameters (rank, alpha, learning rate)
5. Evaluate the fine-tuned model vs baseline (L20 discipline)
6. Serve the adapter (merge or adapter-only, with the base model)
7. Avoid overfitting, data contamination, and regressions

## Prerequisites

| Need | Where |
|---|---|
| LLM fundamentals | `09-genai/lectures/01-llm-fundamentals-lecture.md` |
| Evaluation | `09-genai/lectures/20-evaluation-frameworks-lecture.md` |
| Structured output | `09-genai/lectures/03-structured-output-lecture.md` |
| Phase 8 training | `08-mlops/lectures/01-reproducibility-lecture.md` |

## 1. The Decision: When to Fine-Tune

Ask three questions before spending compute:

| Question | If yes... | Then |
|---|---|---|
| Is the task format distinct (JSON, legal tone, code style)? | fine-tune helps | LoRA on a small model |
| Is prompt+RAG already at 90%? | the last 10% may cost more than it's worth | measure (L20) first |
| Do you need lower serving cost/latency? | fine-tune a smaller model | distill/adapt down |
| Is the problem *knowledge* (new facts)? | fine-tuning is wrong | RAG (L9) |

The professional answer is usually "measure first": build the prompt/RAG
baseline, eval it (L20), and only fine-tune when the gap is real and the
format/behavior hypothesis holds.

## 2. The Dataset: Quality Over Quantity

Fine-tuning datasets are small — hundreds to thousands of examples — and
quality-dominant. The format mirrors the task:

```python
FINE_TUNE_EXAMPLES = [
    {
        "messages": [
            {"role": "system", "content": "You extract JSON from contracts."},
            {"role": "user", "content": "Section 4.2: Company pays $50k within 30 days."},
            {"role": "assistant",
             "content": '{"obligation": "payment", "amount": 50000, "term_days": 30}'},
        ]
    },
    # 200-2,000 more, covering the format's edge cases
]
```

Output:
```
200 quality examples with exact target format > 20,000 noisy ones.
```

**Dataset rules:** cover the *output distribution* you want (edge cases
included); split train/val (don't tune on your eval set — L20 discipline);
dedupe and decontaminate (remove near-duplicates of eval/benchmark items);
and review a sample by hand — garbage in, fine-tuned garbage out.

## 3. LoRA: The Efficient Method

LoRA freezes the base weights and trains low-rank adapter matrices injected
into the attention layers. The adapter is tiny (1-10% of the model) and
separate — train it, merge it, or serve it alongside the base:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, TaskType

base = AutoModelForCausalLM.from_pretrained("microsoft/phi-2")
lora_cfg = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,                    # rank: adapter capacity (8-64 typical)
    lora_alpha=32,           # scaling; rule of thumb ~2x r
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"],   # attention projections
)
peft_model = get_peft_model(base, lora_cfg)
print("trainable %:", round(peft_model.num_parameters(only_trainable=True)
      / peft_model.num_parameters() * 100, 2))
```

Output:
```
trainable %: 1.12   — training 1% of the parameters, not 100%
```

**Hyperparameter rules of thumb:** `r` 8-64 (task complexity), `alpha` ~2x
`r`, small LR (1e-4 to 3e-4), a few epochs (1-3 for small datasets —
overfitting is the common failure).

## 4. Training: Reproducibility Discipline

Fine-tuning is training — Phase 8 Lecture 1 discipline applies: seed,
version the data, track the run, gate with evals:

```python
def train_lora(dataset_path: str, output_dir: str, *, seed: int = 42,
               epochs: int = 3, lr: float = 2e-4) -> str:
    # Phase 8 L1: seed everything before training
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    # ... load tokenized dataset, TrainingArguments(lr, epochs, seed) ...
    # trainer.train() → save adapter to output_dir
    return f"{output_dir}/adapter"     # the LoRA adapter artifact
```

Output:
```
adapter/  (a few MB — vs a multi-GB full model)
```

The adapter is the *new model version*: it gets its own registry entry (L4
discipline), its own eval run (L20), and its own serving path (L22/L5).

## 5. Evaluating the Fine-Tune

The iron rule: the fine-tuned model must beat the baseline on the *same*
frozen eval suite (L20) — never assume "fine-tuned = better":

```python
def decide_finetune(baseline: dict, finetuned: dict, keys: list[str],
                    tol: float = 0.02) -> tuple[bool, dict]:
    deltas = {k: round(finetuned[k] - baseline[k], 3) for k in keys}
    regressions = {k: d for k, d in deltas.items() if d < -tol}
    return (not regressions, {"deltas": deltas, "regressions": regressions})

print(decide_finetune({"acc": 0.84}, {"acc": 0.91}, ["acc"]))
```

Output:
```
(True, {'deltas': {'acc': 0.07}, 'regressions': {}})   → ship the adapter
```

**Watch for regressions:** fine-tuning can hurt out-of-domain behavior and
safety — eval both the target task *and* a general capability suite (L19
attack suite included) before shipping.

## 6. Serving the Adapter

Two serving modes:

| Mode | What | Use when |
|---|---|---|
| **Merged** | adapter weights added into the base → one model file | simple serving, fixed adapter |
| **Adapter-only** | base + tiny adapter loaded at runtime (PEFT) | multiple adapters, hot-swap |

```python
# merged: one artifact, standard serving (L5/L7)
merged = peft_model.merge_and_unload()
merged.save_pretrained("outputs/model-merged")

# adapter-only: base + adapter → hot-swappable per tenant
from peft import PeftModel
model = PeftModel.from_pretrained(base, "outputs/adapter")
```

Output:
```
merged → model-merged/ (single artifact, deploy like any model, L5-L7)
adapter-only → base + 50MB adapter; swap adapters without reloading base.
```

**Multi-tenant story:** adapter-only serving lets one base model serve many
clients' fine-tunes — the economics (L18) of fine-tuning at scale.

## Every Use Case

- **Format enforcement**: JSON/legal/code-style outputs the base won't follow reliably.
- **Domain tone**: medical, legal, financial writing styles.
- **Small-model competence**: make a 3B model good enough to serve cheaply (L18).
- **Personalization**: per-tenant/company adapters on one base.
- **Classification via LM**: domain-specific label sets.
- **Efficiency**: replace few-shot-heavy prompts with a fine-tuned small model.
- **Tool-calling reliability**: fine-tune for a specific tool set (L13).
- **Non-English domains**: adapt to language/style distributions.

## Real-World Use Cases for AI Engineers

- **Legal contract extraction**: a base model extracts clause JSON at 82%
  format compliance; after 800-example LoRA fine-tune, 98% — the format is
  now *the model's default*, not a prompt's wish. The eval (L20) proved it
  before serving.
- **Support reply generation**: fine-tuning a small model on company tone +
  policy format let the team serve replies at 1/10th the cost of the
  big-model prompt approach (L18) — latency and cost drove the decision.
- **Fintech tool calling**: a LoRA fine-tune for the specific tool schemas
  (L13) lifted correct tool-call rate 12 points — fewer retries, lower
  latency.
- **Multi-tenant SaaS**: one base model + per-tenant adapters (legal firm A's
  style, firm B's) served adapter-only — each firm's adapter is a versioned
  artifact in the registry (L4), swapped without reloading the base.
- **Healthcare documentation**: a domain-tuned model produces the clinic's
  note format; the general-capability eval (L20) confirmed no safety
  regression before the clinical pilot.

## Common Mistakes to Avoid

### Mistake 1: Fine-tuning for knowledge
The model can't "learn your database" — it memorizes examples and
hallucinates. Use RAG for facts.

### Mistake 2: Tiny noisy datasets
Garbage in, tuned garbage out. 200 quality examples beat 20k scraped ones.

### Mistake 3: No eval vs baseline
"Fine-tuned = better" is a hypothesis. Measure on the frozen suite (L20).

### Mistake 4: Tuning on the eval set
Data contamination inflates scores. Split train/val; keep eval clean.

### Mistake 5: Overfitting (too many epochs)
Small datasets overfit fast. 1-3 epochs, watch val loss.

### Mistake 6: Ignoring general-capability regression
Fine-tuning can hurt general behavior and safety. Eval both axes.

### Mistake 7: No reproducibility discipline
Unseeded, unversioned fine-tuning violates Phase 8 L1. Seed + version + track.

## Best Practices

1. Exhaust prompting + RAG before fine-tuning; measure the gap (L20)
2. Build a small, quality dataset covering the target format + edge cases
3. Use LoRA/PEFT — tiny trainable fraction, tiny artifacts
4. Seed and version everything (Phase 8 L1 discipline)
5. Eval vs baseline on the frozen suite AND a general-capability suite
6. Register the adapter as a model version with lineage (L4)
7. Serve merged (simple) or adapter-only (multi-tenant, hot-swap)
8. Watch for overfitting: few epochs, small LR
9. Decontaminate the dataset (no eval/benchmark overlap)
10. Treat the adapter as a deployable artifact (CI gates, L12 pattern)

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Dataset prep | hours | O(data) | — |
| LoRA train (3B, 500 examples) | minutes-hours on 1 GPU | O(adapter) | — |
| Full fine-tune | days, many GPUs | O(model) | LoRA (near-parity) |
| Eval vs baseline | minutes | O(1) | — |
| Adapter-only serving | +50-500MB | per-adapter | merged for single-tenant |

## AI Engineering Relevance

**Where this shows up:** the "prompt ceiling" — when format, tone, or
task-behavior fidelity matters more than prompting can deliver. Fine-tuning
(LoRA) is the controlled, measured, artifact-grade way to get there.

| Concept here | Used for |
|---|---|
| Decision ladder | prompt → RAG → few-shot → fine-tune |
| LoRA/PEFT | efficient adaptation |
| Dataset discipline | quality over quantity |
| Eval vs baseline | measured wins only |
| Adapter artifacts | versioned, served, swapped |

**Scale note:** at many tenants or high QPS, adapter-only serving + a small
tuned model is where the economics (L18) and the capability meet — one base,
many cheap competent servants.

## Practice Exercises

### Exercise 1: Decision Ladder (Easy)
Given four scenarios (format problem, knowledge gap, style problem, prompt at
95%), choose the right lever and justify each.

### Exercise 2: Dataset Prep (Medium)
Write `prepare_dataset(examples, format_fn, split)` that formats examples
into the chat shape, dedupes, and splits train/val; assert the splits and the
format.

### Exercise 3: Eval Decision (Medium)
Implement `decide_finetune` and test: improvement passes, regression on the
general suite blocks, tie passes.

### Exercise 4: Adapter Lifecycle (Hard)
Simulate the lifecycle: baseline eval → LoRA train (mock) → adapter eval →
registry registration (L4) → serving choice (merged vs adapter-only) — with
asserts that a regressing adapter never registers.

## Summary

| Concept | Description |
|---|---|
| Decision ladder | prompt → RAG → few-shot → fine-tune |
| LoRA/PEFT | train 1-10%, not 100% |
| Dataset | small, quality, format-complete |
| Eval | vs baseline + general suite (L20) |
| Adapter artifact | versioned, served, swappable |

Fine-tuning (LoRA) is the "beyond prompting" lever for format, tone, and
task behavior — efficient, artifact-grade, and strictly measured against the
baseline. The discipline — decide with the ladder, prepare quality data, eval
both axes, version the adapter — is what turns fine-tuning from a party
trick into a production practice.

## Quick Reference

| Task | Idiom |
|---|---|
| Decide | prompt → RAG → few-shot → fine-tune |
| Adapt | LoRA `r=16, alpha=32, lr=2e-4` |
| Eval | frozen suite + general suite (L20) |
| Serve | merged (single) or adapter-only (multi) |
| Gate | adapter must beat baseline |

## Next Steps

Next: **[22 Local Models](22-local-models-lecture.md)** — running models
in-house: vLLM, quantization, and the self-hosted path.
Continues in: **[Phase 9 — GenAI](../../09-genai/README.md)**.
Official docs: https://huggingface.co/docs/peft, https://huggingface.co/docs/trl
