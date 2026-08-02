# GenAI — 18: Caching and Cost

## Topic Overview

Caching and cost engineering is what makes LLM products *economically
viable*: LLM calls are the most expensive per-operation unit in most stacks,
and the bill compounds with traffic (Phase 8 Lecture 15's recurring-cost
lesson applies with a vengeance). This lecture is the LLM-specific cost
playbook:

1. **Prompt caching**: identical or prefixed prompts reuse a cached
   completion (exact-match caching, or provider-side prefix caching).
2. **Semantic caching**: semantically similar queries reuse a cached answer
   (embedding-similarity lookup — L6) instead of a fresh generation.
3. **Batching**: process multiple requests per call where supported.
4. **Model tiering**: route easy queries to a cheap model, hard ones to an
   expensive model (classifier/routing).
5. **Token discipline**: shorter prompts, fewer redundant turns, structured
   budgets (L1/L16 discipline).

The math: a cache hit costs ~0 (a vector lookup) vs a generation costing
tokens + latency. At 1M calls/day, a 40% hit rate is 400k calls/day saved —
the difference between a viable product and a money pit.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Implement exact-match prompt caching with TTL
2. Implement semantic caching with embeddings + similarity thresholds
3. Track cache hit rate and measure the savings
4. Apply model tiering (cheap route for easy queries)
5. Budget tokens per call and per feature (L16 assembler discipline)
6. Avoid the caching pitfalls (staleness, poisoned cache, privacy)
7. Build the cost dashboard and alerts (L17 data + Phase 8 L15 pattern)

## Prerequisites

| Need | Where |
|---|---|
| Observability | `09-genai/lectures/17-llm-observability-lecture.md` |
| Embeddings | `09-genai/lectures/06-embeddings-lecture.md` |
| Cost (Phase 8) | `08-mlops/lectures/15-cost-optimization-lecture.md` |
| API clients | `09-genai/lectures/02-api-clients-lecture.md` |

## 1. Exact-Match Prompt Caching

The simplest win: identical prompts get cached completions. Many production
queries are repeated (popular support questions, common phrases):

```python
from functools import lru_cache

class ExactPromptCache:
    def __init__(self, ttl_s: int = 3600):
        self._cache: dict[str, tuple[float, str]] = {}
        self.ttl = ttl_s

    def get(self, prompt: str) -> str | None:
        entry = self._cache.get(prompt)
        if entry and (time.time() - entry[0]) < self.ttl:
            return entry[1]
        self._cache.pop(prompt, None)
        return None

    def set(self, prompt: str, completion: str) -> None:
        self._cache[prompt] = (time.time(), completion)

cache = ExactPromptCache()
cache.set("What is the refund policy?", "Refunds take 3-5 days.")
print(cache.get("What is the refund policy?"))
```

Output:
```
Refunds take 3-5 days.   (cache hit — no LLM call, no tokens, no latency)
```

**Provider-side option:** OpenAI/Anthropic cache repeated *prefixes*
(system prompt + few-shot) automatically, cutting cost for long shared
prompts — check your provider's pricing model; the design implication is
keeping shared prefixes stable.

## 2. Semantic Caching

Exact matches miss paraphrase. Semantic caching embeds the query (L6) and
returns a cached answer when a *similar* cached query exists above a
similarity threshold:

```python
class SemanticCache:
    def __init__(self, embed_fn, threshold: float = 0.92):
        self.embed = embed_fn
        self.threshold = threshold
        self._items: list[tuple[str, list[float], str]] = []   # query, vec, answer

    def get(self, query: str) -> str | None:
        qv = self.embed(query)
        for stored_q, stored_v, answer in self._items:
            if cosine_similarity(qv, stored_v) >= self.threshold:
                return answer
        return None

    def set(self, query: str, answer: str) -> None:
        self._items.append((query, self.embed(query), answer))

c = SemanticCache(embed_text)
c.set("How do I reset my password?", "Go to Settings → Security → Reset.")
print(c.get("How can I change my password?"))
```

Output:
```
Go to Settings → Security → Reset.   (paraphrase hit — no LLM call)
```

**The threshold is the quality/cost knob**: too high → misses; too low →
wrong answers served. Tune it with eval (L20) — a wrong cached answer is a
quality incident, not a saving.

## 3. The Cache Architecture: TTL, Invalidation, Poisoning

Caching has a dirty side:

| Risk | Mitigation |
|---|---|
| **Staleness** (facts change) | TTL per content type; short TTL for volatile facts |
| **Poisoning** (a bad answer cached) | never cache errors/low-confidence; cache eviction |
| **PII in cache** | hash keys; redact stored values (L17) |
| **Cache bloat** | LRU eviction + size caps |
| **Miss-path cost** | the embedding lookup costs ~0 vs generation |

```python
def cache_with_guard(cache, prompt, generate_fn, *, ttl, min_confidence=0.8):
    """Cache only confident, non-error completions."""
    hit = cache.get(prompt)
    if hit:
        return hit
    result = generate_fn(prompt)
    if result.get("error") is None and result.get("confidence", 1.0) >= min_confidence:
        cache.set(prompt, result["content"])
    return result["content"]
```

Output:
```
Hit → instant; Miss → generate → cache only if confident and error-free.
```

## 4. Model Tiering: The Router Pattern

Not every query needs the flagship model. A classifier (cheap model or
heuristics) routes easy queries to a cheap/small model and hard ones to the
big model — the biggest structural cost lever:

```python
def route_model(query: str, classify_fn) -> str:
    """Return the model for this query: cheap default, premium for hard."""
    return "gpt-4o-mini" if classify_fn(query) == "easy" else "gpt-4o"

# 80% easy → 80% of traffic at 1/20th the price
# measured: eval (L20) must confirm the cheap route doesn't regress quality
```

Output:
```
easy query → gpt-4o-mini (cheap); hard query → gpt-4o (premium)
```

**The discipline:** routing is a *quality* decision with a cost benefit —
eval the routed system (L20) before believing the savings. A router that
saves 80% but breaks 5% of answers is not a saving.

## 5. Token Discipline: The Free Levers

Before any cache, the cheapest cost control is tokens:

| Lever | Saving | Where |
|---|---|---|
| Shorter system prompts | per-call prompt tokens | L4 |
| Context truncation/summary | history tokens per call | L16 |
| max_tokens caps | completion tokens | L1 |
| Fewer retries | ×N calls | L3 repair caps |
| Batch where possible | call overhead | L2 |

```python
def token_budget_check(prompt_tokens: int, completion_tokens: int,
                       prompt_cap: int, completion_cap: int) -> tuple[bool, str]:
    """Gate: no call exceeds its token budget (L17 metric feeds this)."""
    ok = prompt_tokens <= prompt_cap and completion_tokens <= completion_cap
    return (ok, f"prompt {prompt_tokens}/{prompt_cap}, "
                f"completion {completion_tokens}/{completion_cap}")

print(token_budget_check(4200, 150, 4000, 300))
```

Output:
```
(False, 'prompt 4200/4000, completion 150/300')   — over budget; shorten prompt
```

## 6. The Cost Dashboard and Alerts

Measure, then manage: per-feature cost from the L17 traces, with alerts at
budget thresholds (Phase 8 L15 pattern):

```python
def cost_summary(traces: list[dict]) -> dict:
    total = sum(t["cost_usd"] for t in traces)
    by_feature = {}
    for t in traces:
        f = t["metadata"].get("feature", "unknown")
        by_feature[f] = by_feature.get(f, 0.0) + t["cost_usd"]
    return {"total_usd": round(total, 2),
            "by_feature": {k: round(v, 2) for k, v in by_feature.items()},
            "avg_cost_per_call": round(total / max(len(traces), 1), 5)}
```

Output:
```
{'total_usd': 312.4, 'by_feature': {'support': 210.1, 'search': 82.3,
 'summary': 20.0}, 'avg_cost_per_call': 0.0008}
```

Alert at 50/80/100% of the monthly budget; the by-feature breakdown tells
you *where* to apply the levers.

## Every Use Case

- **High-traffic support**: exact + semantic caching on FAQ queries.
- **Chat products**: prefix caching of system prompts + summary cache (L16).
- **Search enhancement**: semantic cache on repeated intents.
- **Agents (L14)**: caching repeated tool-result contexts and sub-answers.
- **Batch jobs**: dedup identical items before generating.
- **Multi-tenant SaaS**: per-tenant budgets and routing policies.
- **Multilingual**: shared cache keys across language variants (careful).
- **Internal tools**: model tiering (cheap for drafts, premium for finals).

## Real-World Use Cases for AI Engineers

- **Support copilot (SaaS)**: exact + semantic caching cut LLM calls 42% —
  the top-20 FAQ answers serve from cache, and the cost dashboard shows the
  saving monthly. The threshold was tuned with the L20 eval so paraphrases
  get correct cached answers.
- **Legal summarization**: batch jobs dedupe near-identical documents
  (semantic cache, L6 dedup synergy) before generating — 30% of the bill
  vanished without changing a single answer.
- **Routing at a fintech**: 78% of queries route to the cheap model with
  quality verified by the L20 eval (no regression on the frozen set); the
  other 22% keep the premium model. Cost dropped 61% at *measured* equal
  quality.
- **Chat product**: prompt-prefix caching (shared system prompt) + provider
  prefix caching cut per-turn cost 25%; the L16 summary pattern cut history
  tokens another 30%.
- **RAG service**: cache retrieval results for repeated queries (L12 rerank
  cache) — 35% of queries hit the cached top-k, skipping embed+search+rerank
  entirely.

## Common Mistakes to Avoid

### Mistake 1: Caching without TTL
Facts change; a stale cached answer is a quality incident. TTL everything.

### Mistake 2: Semantic threshold too loose
Wrong cached answers served. Tune with eval (L20).

### Mistake 3: Caching errors/low-confidence outputs
Poisoning the cache with bad answers. Never cache errors.

### Mistake 4: Storing PII in cache values
Hash keys, redact values (L17 discipline).

### Mistake 5: Routing to save money without eval
A router that regresses quality is not a saving. Measure (L20).

### Mistake 6: Ignoring provider prefix caching
Repeated prefixes cost real money; design stable shared prefixes.

### Mistake 7: No cache hit-rate monitoring
You can't manage what you don't measure. Track hit rate per feature (L17).

## Best Practices

1. Exact-match cache first (cheapest); semantic cache where paraphrases dominate
2. TTL per content type; short TTL for volatile facts
3. Cache only confident, error-free completions
4. Tune semantic thresholds with the L20 eval
5. Route by measured quality — cheap model for easy, premium for hard
6. Practice token discipline: shorter prompts, capped completions, summaries
7. Monitor hit rate + savings per feature (L17 dashboard)
8. Hash cache keys; redact stored values
9. Set budget alerts (50/80/100%) per feature
10. Evict LRU + size caps to bound cache growth

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Exact cache hit | ~0 | O(entries) | lru_cache |
| Semantic cache hit | embed + scan | O(entries) | ANN index at scale |
| Generate (miss) | 0.5-5s + tokens | — | cache! |
| Router classify | ~0 (cheap model) | — | heuristics first |
| Hit-rate monitor | O(traces) | O(1) | pre-aggregated |

## AI Engineering Relevance

**Where this shows up:** every LLM product's P&L. Caching + routing + token
discipline are the difference between "product" and "product that loses money
per query."

| Concept here | Used for |
|---|---|
| Exact + semantic cache | skip generations safely |
| TTL + poisoning guards | cache correctness |
| Model routing | quality-preserving cost cuts |
| Token discipline | the free levers |
| Dashboards + alerts | cost visibility |

**Scale note:** savings compound with traffic — a 40% hit rate on 1M
calls/day is 400k generations saved *every day*, forever. At any scale, the
thresholds and TTLs are tuned with the L20 eval, because a cached wrong
answer is worse than no cache.

## Practice Exercises

### Exercise 1: Exact Cache (Easy)
Implement `ExactPromptCache` with TTL; test hit, miss, and expiry.

### Exercise 2: Semantic Cache (Medium)
Implement `SemanticCache` with a mock embed_fn; assert a paraphrase above the
threshold hits and a dissimilar query misses.

### Exercise 3: Cache Guard (Medium)
Implement `cache_with_guard` and assert errors and low-confidence outputs are
never cached.

### Exercise 4: Router + Dashboard (Hard)
Build `route_model` (mock classifier) + `cost_summary` (L17-style traces);
assert: easy queries route cheap, the savings math is correct, and the
budget alert fires at the 80% threshold.

## Summary

| Concept | Description |
|---|---|
| Exact cache | identical prompts, zero cost |
| Semantic cache | paraphrases hit too |
| Guarding | TTL, no-poisoning, PII-safe |
| Model routing | cheap for easy, premium for hard |
| Token discipline | the free levers |
| Dashboards | measure before you manage |

Caching and cost engineering make LLM products viable: skip generations with
exact and semantic caches, route by measured quality, practice token
discipline, and watch the dashboard. The discipline — threshold tuning with
eval, TTL correctness, and no-cache-poisoning — is what turns aggressive
savings into *safe* savings.

## Quick Reference

| Task | Idiom |
|---|---|
| Exact cache | prompt → completion map + TTL |
| Semantic cache | embed + cosine ≥ threshold |
| Guard | TTL, min-confidence, no-errors |
| Route | classifier: cheap vs premium model |
| Watch | hit rate + cost per feature |

## Next Steps

Next: **[19 Guardrails and Safety](19-guardrails-and-safety-lecture.md)** —
keeping LLM systems safe: input/output filtering, refusal, and misuse defense.
Continues in: **[Phase 9 — GenAI](../../09-genai/README.md)**.
Official docs: https://platform.openai.com/docs/guides/prompt-caching,
https://www.anthropic.com/news/prompt-caching
