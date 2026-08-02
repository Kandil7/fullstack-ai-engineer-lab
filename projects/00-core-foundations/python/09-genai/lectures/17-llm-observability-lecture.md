# GenAI — 17: LLM Observability

## Topic Overview

LLM observability is the practice of recording, tracing, and monitoring every
LLM call and agent step — the prompts, completions, tokens, latency, cost,
and outcomes — so that you can debug failures, track cost, detect drift, and
prove quality in production. Classic software observability (logs, metrics,
traces) applies, but LLM systems add unique needs: **prompt-level tracing**
(what exactly was sent and returned), **token accounting** (cost per call),
**drift signals** (refusal rates, response-length drift — Phase 8 L11 ideas
applied to LLMs), and **evaluation-in-production** (sampling outputs for
quality review, L20).

The standard toolkit: **LangSmith** and **Langfuse** (LLM-native tracing:
traces per call with prompts, completions, token counts, latency, cost, and
annotations), plus the classic stack (Prometheus/Grafana for metrics,
structured logs). The AI engineer's job: decide *what* to capture (with a
privacy filter), attach IDs for correlation, and turn the stream into
actionable signals (dashboards, alerts, sampling queues).

Why this matters: LLM systems fail in ways classic monitoring misses —
a prompt regression degrades answers without any error, a model update
changes behavior silently, cost creeps up invisibly. Observability is the
only way to see these. And the data you capture is also the *evaluation
substrate*: production samples feed the eval harness (L20).

## Learning Objectives

By the end of this lecture, you will be able to:
1. Instrument an LLM call with a trace: prompt, completion, tokens, latency, cost
2. Attach IDs (trace/request/user) for cross-system correlation
3. Filter sensitive data (PII) before logging
4. Track the key LLM metrics: latency percentiles, token rates, error rates, refusal rate
5. Detect behavioral drift: refusal-rate and response-length shifts
6. Sample production traffic for quality review (feeding L20)
7. Build dashboards and alerts from the trace stream

## Prerequisites

| Need | Where |
|---|---|
| API clients | `09-genai/lectures/02-api-clients-lecture.md` |
| Monitoring (Phase 8) | `08-mlops/lectures/11-monitoring-and-drift-lecture.md` |
| Cost tracking (Phase 8) | `08-mlops/lectures/15-cost-optimization-lecture.md` |
| Evaluation | `09-genai/lectures/20-evaluation-frameworks-lecture.md` |

## 1. The Trace: Every Call, Every Field

A trace is the complete record of one call (or one agent run — a tree of
calls). The minimal capture:

```python
def traced_call(llm_client, messages, *, trace_id, user_id,
                metadata=None, pii_filter=redact) -> dict:
    """Complete a call AND capture the observability record."""
    t0 = time.perf_counter()
    resp = llm_client.complete(messages)
    latency_ms = (time.perf_counter() - t0) * 1000
    trace = {
        "trace_id": trace_id,
        "user_id": user_id,                       # hashed if needed
        "model": resp.model,
        "prompt": pii_filter(messages),           # redact PII before logging
        "completion": pii_filter(resp.content),
        "prompt_tokens": resp.prompt_tokens,
        "completion_tokens": resp.completion_tokens,
        "latency_ms": round(latency_ms, 1),
        "cost_usd": round(estimate_cost(resp), 6),
        "metadata": metadata or {},
        "ts": int(time.time()),
    }
    log_trace(trace)                              # → Langfuse/LangSmith/JSONL
    return resp
```

Output:
```
Trace logged: {trace_id, model, tokens, latency_ms, cost_usd, ...}
```

**Every field is a future question:** cost (L18 dashboards), latency (SLOs),
tokens (budgets), prompt+completion (debugging and L20 sampling).

## 2. Correlation IDs: The Join Key

A trace is useless if it can't be joined to the request that produced it. The
**trace_id** flows through the whole stack: the HTTP request (L7 header), the
agent run (L14), the DB query, the log lines. When a user reports a bad
answer, the trace_id is the breadcrumb to every record:

```python
import uuid

def new_trace_id() -> str:
    return f"tr_{uuid.uuid4().hex[:16]}"

# HTTP layer: X-Trace-ID header → LLM trace → agent trace → log lines
# Incident flow: user says "wrong answer" → trace_id → replay the trace
```

Output:
```
tr_9f2c1b7a3d4e5f60 — one id joining the request, the calls, the logs.
```

**The discipline:** propagate the id end-to-end (FastAPI middleware, agent
loop, tool calls). An observability system without correlation is a pile of
disconnected numbers.

## 3. Privacy Filtering: What NOT to Log

Prompts and completions contain user data. Logging raw PII is itself an
incident (and a compliance violation). The filter is non-negotiable:

```python
import re

PII_PATTERNS = [
    (re.compile(r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b"), "[CARD]"),
    (re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b"), "[EMAIL]"),
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[SSN]"),
]

def redact(text: str) -> str:
    for pattern, repl in PII_PATTERNS:
        text = pattern.sub(repl, text)
    return text

print(redact("card 4111 1111 1111 1111 for user a@b.com"))
```

Output:
```
"card [CARD] for user [EMAIL]"
```

**Design choice:** log redacted prompts/completions for *all* traffic, or
full details for a sampled subset (with consent). Redaction-at-write beats
redaction-at-read (the full data never hits the store).

## 4. The Metrics: What to Track

| Metric | Definition | Signal |
|---|---|---|
| latency p50/p95/p99 | per-call ms | SLO health |
| token rate | tokens/sec | throughput + cost |
| error rate | 4xx/5xx/timeouts / calls | provider health (L2) |
| cost per call / day | tokens × price | budget (L18) |
| **refusal rate** | "I don't know" / total | knowledge-gap signal |
| **response length** | completion tokens | behavioral drift |
| cache hit rate | cached / total | cost optimization (L18) |

```python
def track_refusal(completion: str) -> bool:
    """Detect the honest-refusal pattern (L9) as a monitored signal."""
    return completion.strip() == "I don't have that information."
```

Output:
```
Refusal-rate rising = the knowledge base has a gap — a product signal, not
just a model signal.
```

## 5. Behavioral Drift: Watching the Distribution

Phase 8 Lecture 11's drift idea applies to LLM behavior: refusal rate and
response-length distributions shifting signal *something changed* (model
update, prompt regression, traffic shift) — even when no error occurs:

```python
def drift_flag(daily: list[float], baseline: float, threshold: float = 0.15) -> bool:
    """Flag if the trailing window drifted from baseline by > threshold."""
    avg = sum(daily[-7:]) / len(daily[-7:])
    return abs(avg - baseline) / max(abs(baseline), 1e-9) > threshold

print(drift_flag([0.04, 0.05, 0.12, 0.18, 0.21, 0.22, 0.24], 0.05))
```

Output:
```
True   — refusal rate drifted 4.7x from baseline; investigate the cause.
```

## 6. Sampling for Production Evaluation

You can't human-review every call, and you can't LLM-judge every call either
(cost — L18). Sample deterministically: a random or score-based sample feeds
the L20 evaluation harness:

```python
import random

def sample_for_review(trace: dict, rate: float = 0.05) -> bool:
    """Deterministic-ish sampling: keep a fraction for quality review."""
    return random.random() < rate

# sampled traces → human or LLM-judge review (L20) → quality report
# + flagged traces (refusals, high cost, errors) always sampled
```

Output:
```
5% random + 100% of flagged traces → the production quality review queue.
```

## Every Use Case

- **Incident debugging**: a bad answer → trace_id → full call history.
- **Cost tracking**: per-app/per-feature cost dashboards (L18).
- **Latency SLOs**: p95 alert when generation slows (provider or prompt bloat).
- **Quality monitoring**: sampled outputs → L20 review scores.
- **Drift detection**: refusal-rate and length-drift alerts.
- **Model/prompt rollout**: observability confirms a rollout behaves as evals predicted.
- **Compliance**: retention, redaction, and audit of the LLM layer.
- **Agent tracing**: full step trees (L14) with per-step tokens/cost.

## Real-World Use Cases for AI Engineers

- **Support copilot incident**: a user got a wrong refund answer. The
  trace_id from the HTTP header replays the full call: prompt, retrieved
  chunks, completion, tokens. Root cause: a stale chunk (L8 ingestion issue)
  — fixed in the corpus, not the model.
- **Cost spike detection**: the Monday cost dashboard showed a 3x spike; the
  per-feature traces traced it to a feature shipping 4k-token prompts instead
  of 500 — the observability data made the fix a query, not a mystery (L18).
- **Model-version regression**: after a model bump, refusal rate drifted up
  4x; the drift alert fired *before* user complaints — the team compared
  traces and reverted the model. The eval (L20) confirmed.
- **Fintech compliance**: traces are redacted (L17 privacy filter), retained
  per policy, and auditable — "show me what the model said and why" is a
  query, satisfying the model-risk review.
- **Platform team**: one shared tracing layer (Langfuse) across 15 apps —
  cost, latency, and refusal-rate dashboards per app; the platform's
  observability *is* the quality gate for LLM features.

## Common Mistakes to Avoid

### Mistake 1: Logging raw PII
Prompts/completions carry user data. Redact at write time, always.

### Mistake 2: No trace IDs
Without correlation, a bad answer is un-debuggable. Propagate trace_id
everywhere.

### Mistake 3: Metrics only, no content
Latency/tokens without prompts can't debug a bad answer. Capture both
(redacted).

### Mistake 4: No sampling for quality
Never seeing production outputs = blind quality. Sample + review (L20).

### Mistake 5: Ignoring behavioral drift
No error ≠ healthy. Refusal-rate and length drift are the early signals.

### Mistake 6: Infinite retention
Storage grows (cost — L15). Retention policy per trace tier (e.g. 30d for
details, 12mo for metrics).

### Mistake 7: Observability after the incident
Instrument from day one; retrofitting traces is archaeology.

## Best Practices

1. Capture prompt, completion, tokens, latency, cost per call (redacted)
2. Propagate trace_id end-to-end (HTTP → agent → tools → logs)
3. Redact PII at write time; filter by default
4. Track latency, token rate, error rate, cost, refusal rate
5. Alert on behavioral drift (refusal, length) — not just errors
6. Sample traffic (random + flagged) into the L20 review queue
7. Set retention policies per trace tier
8. Build per-feature dashboards (cost, latency, quality)
9. Use an LLM-native tracing tool (Langfuse/LangSmith) + metrics stack
10. Review observability with the eval harness — production data feeds evals

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Log trace per call | O(1) | O(trace) | sample at high volume |
| Redact PII | O(text) | O(1) | regex precompile |
| Drift compute | O(windows) | O(1) | pre-aggregated daily |
| Sampling review | per sample | O(samples) | score-based sampling |

## AI Engineering Relevance

**Where this shows up:** every LLM feature in production. Observability is
the difference between "users report a problem" and "the refusal-rate drift
alert fired Tuesday" — plus the raw material for cost control (L18) and
production evaluation (L20).

| Concept here | Used for |
|---|---|
| Traces | full call records, replayable |
| IDs | correlation across the stack |
| Redaction | privacy + compliance |
| Metrics + drift | SLOs, cost, behavior signals |
| Sampling | the production → eval pipeline |

**Scale note:** at 1M calls/day, sample traces aggressively (1-5% full
detail, 100% metrics) and pre-aggregate; the *metrics* scale cheaply, the
*content* doesn't. At any scale, trace_ids and redaction are non-negotiable.

## Practice Exercises

### Exercise 1: Redactor (Easy)
Implement `redact` with card/email/SSN patterns and test each on a sample.

### Exercise 2: Traced Call (Medium)
Build `traced_call` around a mock client and assert the trace contains model,
tokens, latency, cost, and redacted prompt/completion.

### Exercise 3: Drift Flag (Medium)
Implement `drift_flag` and assert it fires on a 4x shift but not on noise.

### Exercise 4: Sampling Queue (Hard)
Build `sample_for_review` with deterministic rules (random rate + always-
flag refusals/errors/high-cost); assert flagged traces are always sampled and
the overall rate is as configured.

## Summary

| Concept | Description |
|---|---|
| Trace | full per-call record (redacted) |
| Correlation IDs | trace_id end-to-end |
| Metrics | latency, tokens, cost, errors, refusal |
| Behavioral drift | the early no-error signal |
| Sampling | production outputs → L20 review |

LLM observability makes the generative layer visible: every call recorded
(redacted), every incident traceable by ID, every cost and latency signal
dashboards, and every drift caught before users complain. It is the eyes of
the system — and the bridge from production traffic to the evaluation
harness (L20).

## Quick Reference

| Task | Idiom |
|---|---|
| Capture | trace: prompt, completion, tokens, latency, cost |
| Correlate | trace_id header → all layers |
| Redact | regex PII patterns at write |
| Detect | refusal-rate / length drift alerts |
| Sample | 5% random + 100% flagged → L20 queue |

## Next Steps

Next: **[18 Caching and Cost](18-caching-and-cost-lecture.md)** — making LLM
systems affordable: caches, batching, and model tiering.
Continues in: **[Phase 9 — GenAI](../../09-genai/README.md)**.
Official docs: https://langfuse.com/docs, https://docs.smith.langchain.com/
