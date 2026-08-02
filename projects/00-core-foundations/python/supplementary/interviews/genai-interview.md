# GenAI / LLM Engineer — Interview Questions

A senior-level interview bank covering the Phase 9 GenAI curriculum. Each
question includes the ideal answer's key points and a follow-up.

## Fundamentals & Prompting

### 1. "What is an LLM, and what are the operational consequences of that definition?"
**Key points:**
- A next-token probability distribution conditioned on the context (not a database, not a program)
- Consequences: non-determinism (sampling), hallucination (no truth model), context window limits, token-based cost/latency
- Engineering responses: temperature 0 for extraction, RAG for knowledge, structured output for reliability, evaluation for measurement

**Follow-up:** Why can't you "fix" hallucination with a better prompt alone? (It's a property of the paradigm — you manage it with grounding, verification, and guardrails.)

### 2. "How do you count and control LLM cost?"
**Key points:**
- Tokens are the unit: count with the model's actual tokenizer (~4 chars/token)
- Per-call cost = (prompt + completion tokens) × price; log `usage` on every call
- Levers: prompt caching (exact + semantic), model routing/tiering, token discipline (shorter prompts, summaries), max_tokens caps, batching
- Budget per feature; alert at 50/80/100%

**Follow-up:** What's semantic caching and its risk? (Embed the query, return a cached answer for similar queries above a threshold — tuned with eval; a wrong cached answer is an incident.)

### 3. "How do you get reliable JSON out of an LLM?"
**Key points:**
- The ladder: prompt with schema → JSON mode (`response_format`) → constrained/structured decoding (schema-guaranteed)
- Always validate at the boundary with pydantic (types, enums, ranges, additionalProperties: False)
- Bounded repair loop: feed validation errors back to the model, capped
- Log raw outputs + failures (repair rate is a quality metric)
- Never regex-scrape JSON out of prose

**Follow-up:** What's the difference between JSON mode and structured outputs? (JSON mode guarantees *valid* JSON; structured outputs guarantee *schema-conformant* output — constrained token decoding.)

### 4. "What makes a good prompt, and how do you prove it?"
**Key points:**
- System prompt: role + task + constraints + output format
- Few-shot examples for format/reasoning; delimiters (XML) separating instructions from data
- Chain-of-thought for reasoning, with the parseable answer on a constrained line
- Proof: a frozen eval set + scoring (exact/rubric/LLM-judge) — every change is a candidate, regressions block CI
- Prompts are code: versioned, deployed, logged with the model call

**Follow-up:** What is prompt injection and how do you defend? (Untrusted data containing instructions — delimit data regions, state data-is-not-instructions, verify output, and gate actions; defense in depth, measured with an attack suite.)

## RAG & Retrieval

### 5. "Build me a RAG system. Where do the quality levers live?"
**Key points:**
- Pipeline: ingest (parse→clean→chunk→embed→index) → retrieve (hybrid + rerank) → grounded generate
- Quality levers, in order of impact: chunking (heading-aware, measured), embedding model (evaluated), hybrid search (BM25+vector, RRF), reranking (cross-encoder), query rewriting/decomposition
- Metrics: recall@k + precision@k + MRR for retrieval; groundedness + citation rate for answers
- Gate every change on the frozen eval set in CI

**Follow-up:** A bad answer with no relevant context retrieved — where's the bug? (Retrieval problem; fix chunking/embedding/search. If good context was retrieved but the answer is wrong — generation problem; fix the prompt/grounding.)

### 6. "What is hybrid search and why do you need it?"
**Key points:**
- Vector search finds meaning; BM25 finds exact tokens (error codes, model numbers, names)
- They fail in opposite directions — run both, fuse with RRF (Reciprocal Rank Fusion: sum 1/(k+rank), no score normalization)
- Multi-stage: hybrid top-50 (recall) → cross-encoder rerank top-5 (precision)
- Budget the rerank stage (latency/cost); measure the gain on recall@k/MRR

**Follow-up:** When is reranking NOT worth it? (Easy corpora with high baseline recall, tight latency budgets, or trivial candidate sets — measure, then drop.)

### 7. "How do you evaluate retrieval quality?"
**Key points:**
- Frozen eval set: real queries + human-labeled gold chunks (never model-labeled)
- Metrics: recall@k (did we find it), precision@k (wasted context), MRR (how high the first right answer ranks), nDCG (graded)
- Attribute failures: query / chunking / embedding / index buckets
- Change one lever at a time; gate all retrieval changes in CI (candidate recall >= baseline - tol)
- Refresh the set periodically; watch production (L17)

**Follow-up:** How do you catch silent retrieval regressions? (CI gate on the frozen set + production monitoring — a chunking change that drops recall is blocked before deploy.)

## Agents & Safety

### 8. "How do you make an LLM agent production-safe?"
**Key points:**
- Tool registry: schemas + levels (read/write) + allowlist; unknown tools deny
- Validate args with pydantic before ANY execution; errors fed back for self-correction
- Bounded loop: max steps, max tokens, max cost — no runaway agents
- Write actions require human approval; read actions auto-run
- Persist state; resume from failure; trace everything (trace_id)
- Eval: completion rate + step efficiency on a frozen suite, gated in CI

**Follow-up:** Why does a state machine beat a free-form loop for regulated workflows? (The transitions ARE the compliance policy — the agent cannot skip validation and jump to payment.)

### 9. "What are the guardrails layers in an LLM system?"
**Key points:**
- Input gate: filter/block harmful or injected input before the model
- Output gate: check PII/policy/unsafe content before the user sees it
- Injection defense: delimit data, state data-is-not-instructions, verify
- Action gates: read auto, write approve, unknown deny
- Refusal + escalation paths defined
- Measure with an attack suite: catch rate AND false-positive rate (over-blocking is a bug)

**Follow-up:** Why is a single filter not enough? (Defense in depth — each layer catches what the others miss; injection into the model is caught at the output gate.)

### 10. "How do you evaluate a whole GenAI system?"
**Key points:**
- Frozen datasets (human-labeled gold), functional evaluators, a runner, CI gates
- Component-level: retrieval (L10), generation (groundedness), guardrails (attack suite), agents (completion + efficiency)
- LLM-as-judge only with calibration (judge-human agreement on a sample), temperature 0, structured output
- Gate every change: no regression on any tracked criterion
- Track quality over time (leaderboards per suite); refresh datasets

**Follow-up:** What's the danger of LLM-as-judge without calibration? (Judge drift and bias silently corrupt scores; format errors unparseable — calibrate against humans periodically.)

## Production & Strategy

### 11. "RAG vs fine-tuning: when do you pick which?"
**Key points:**
- Decision ladder: prompting → RAG → few-shot → fine-tuning
- RAG: knowledge/freshness/auditability — answers from your data, re-index to update
- Fine-tuning (LoRA): behavior/format/tone/task-adherence — NOT knowledge
- LoRA: tiny trainable fraction, small artifacts, hot-swappable adapters
- Measure: fine-tune must beat baseline on the frozen suite AND not regress general capability/safety

**Follow-up:** What is LoRA and why does it win? (Low-Rank Adaptation trains ~1-10% of params on one GPU in minutes-hours, near full-fine-tune quality, with versionable artifacts.)

### 12. "Hosted API vs local models: how do you decide?"
**Key points:**
- It's a measured trade: quality (same eval on both), cost (unit-cost math), latency, privacy/data-residency, ops burden, customization
- Stack: open weights + serving engine (vLLM/Ollama) + quantization (GPTQ/AWQ/GGUF)
- Client portability: OpenAI-compatible endpoints mean the same client code (Lecture 2)
- Right-size: fleet math (demand vs capacity), quantization VRAM math
- Recompute the decision as volume changes (crossover point)

**Follow-up:** Why is "local is cheaper" often wrong? (At low volume hosted wins on total cost; at high volume the crossover flips — the numbers decide, re-run at volume changes.)
