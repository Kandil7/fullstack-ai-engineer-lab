# LLM Applications in Production

> Reference for building and hardening LLM systems. Source: planning conversation
> 2026-07-31, decomposed 2026-08-02. Applied in
> [`projects/04-ai-engineering/devmate/`](../../projects/04-ai-engineering/devmate/).

Shipping an LLM demo takes an hour. Shipping a production LLM system means adding the layers
below — caching, guardrails, evaluation, monitoring, cost control — and reasoning about every
failure point. That gap is the job.

---

## 1. Why LLM systems differ from classical ML

| Concern | Classical ML | LLM system |
| --- | --- | --- |
| **Latency** | milliseconds | seconds — streaming is mandatory, not a nicety |
| **Cost** | ~fixed after training | per-request, token-metered, unbounded if unwatched |
| **Determinism** | same input → same output | same input → different output; breaks naive testing |
| **Evaluation** | clear accuracy/F1 | no single correct answer; needs judges and golden sets |
| **Failure mode** | wrong prediction | confident fabrication (hallucination) |
| **Security** | model theft, data poisoning | prompt injection — a class that didn't exist before |

Each row implies a subsystem. Streaming implies SSE and partial rendering. Per-request cost
implies metering and a budget. Non-determinism implies snapshot tests and mocked clients.
No-single-correct-answer implies an eval harness. Hallucination implies grounding and
faithfulness checks. Injection implies input guardrails.

---

## 2. Request pipeline

```text
User request
    ↓
API gateway            rate limiting, authentication
    ↓
Input guardrails       validation, prompt-injection detection, size limits
    ↓
Cache layer            Redis — semantic, not exact-match
    ↓
Orchestration          LangGraph / LangChain / hand-rolled
    ↓
Retrieval              vector DB — if RAG
    ↓
LLM call               with fallback to a second model
    ↓
Output guardrails      schema validation, PII scan, content filter
    ↓
Response (streamed) + logging + tracing + cost accounting
```

Every layer is optional in a demo and load-bearing in production. The ones most often skipped
and most often regretted: semantic caching (cost), input guardrails (security), and tracing
(debuggability).

---

## 3. Prompt engineering for production

Different discipline from experimentation. Prompts become code.

- **Version them.** Prompts change like code and need the same history and rollback.
- **Template them.** Separate logic from data — Jinja templates, not f-strings scattered
  through the codebase.
- **Write tight system prompts.** Role, boundaries, and output format stated precisely.
- **Include few-shot examples** in the prompt when quality justifies the token cost.
- **Force structured output.** Use tool-use / structured-output APIs rather than parsing prose.
  Prose parsing fails silently and at the worst time.

DevMate: `devmate/src/devmate/llm/prompts/` (Jinja), `llm/schemas.py` (Pydantic).

---

## 4. RAG in production

| Concern | What to decide |
| --- | --- |
| **Chunking** | fixed-size vs. recursive vs. semantic vs. structure-aware. For code, AST-aware boundaries beat character counts. |
| **Embedding model** | trade-off across accuracy, latency, cost, and dimensionality |
| **Vector DB** | Qdrant, Weaviate, Pinecone, pgvector, Chroma — see [ADR-0005](../decisions/0005-vector-db-qdrant-over-chromadb.md) |
| **Hybrid search** | dense + BM25 keyword; catches exact identifiers that embeddings blur |
| **Reranking** | a second pass over initial retrieval; usually the cheapest quality win available |
| **Context management** | what enters the window and what gets dropped as the corpus grows |

**The rule that matters:** decide none of these by intuition. Build the golden set and the
eval harness first, then let measurements choose. This is why the active track moves
evaluation from week 8 to weeks 2–3.

---

## 5. Cost optimization

- **Model routing** — a cheap model (Haiku) for simple work, a strong one only where needed.
  Often the single largest saving available.
- **Semantic caching** — cache on meaning, not string equality. Exact-match caching barely
  fires in conversational traffic.
- **Prompt compression** — fewer tokens for the same quality.
- **Batching** — when real-time isn't required.
- **Hard token limits** — per request and per user, enforced not advisory.

Measure first. Cost per request is a week-1 deliverable in the active track precisely so that
every later optimization can be shown to have worked.

---

## 6. Evaluation

- **LLM-as-judge** — a model scores outputs against criteria. Cheap, scalable, imperfect.
- **Human feedback** — thumbs up/down in the product; the only ground truth you get for free.
- **Golden datasets** — a fixed question/answer set every version is measured against. This is
  the regression suite for a non-deterministic system.
- **Metrics** — faithfulness (is the answer grounded in retrieved context?), answer relevance,
  context precision and recall.
- **Tools** — RAGAS, DeepEval, LangSmith, W&B Weave.

Without a golden set there is no way to know whether a change improved the system. With one,
"I tried three chunking strategies" becomes a table instead of an anecdote.

---

## 7. Guardrails and security

| Layer | Purpose |
| --- | --- |
| Input validation | block prompt injection and system-prompt extraction |
| Output filtering | stop harmful or sensitive content before it reaches the user |
| PII detection | find and redact personal data in both directions |
| Rate limiting | prevent abuse and runaway cost |

Tools: Guardrails AI, NeMo Guardrails, Llama Guard. Also: never store API keys in code, and
treat every user-supplied string that reaches a prompt as hostile.

---

## 8. Observability

Track: latency, token usage, cost per request, error rate, cache hit rate.

**Trace the whole pipeline, not just input and output.** When an answer is wrong you need to
see which step failed — retrieval returned nothing relevant, the rerank buried the right
chunk, the prompt template dropped a variable, the model ignored the context. Input/output
logging cannot distinguish these; span-level tracing can.

Also watch **drift in the questions being asked** — the distribution of user intent moves, and
a retrieval setup tuned for last month's questions quietly degrades.

Tools: Langfuse (self-hostable, free), LangSmith, Helicone, Arize Phoenix.

---

## 9. Agents in production

The hardest tier.

- **Tool use** — the model decides when to call which tool.
- **ReAct** — interleaved reasoning and acting.
- **Multi-agent** — LangGraph, CrewAI, AutoGen. Do not start here.
- **Error handling** — what happens on a failed tool call, and what stops an infinite loop.
  Step caps and loop detection are not optional.
- **Human in the loop** — approval gates before consequential actions.

**Build order that works:** one agent, one tool, no framework. Get it correct. Add a step cap.
Add a second tool. Only then consider a framework, and be able to say what it bought you.

---

## 10. Tooling summary

| Category | Options |
| --- | --- |
| Orchestration | LangChain, LangGraph, LlamaIndex |
| Serving | FastAPI; vLLM for self-hosted models |
| Vector DB | Qdrant, Pinecone, Weaviate, ChromaDB, pgvector |
| Evaluation | RAGAS, DeepEval |
| Observability | Langfuse, LangSmith, Helicone, Arize Phoenix |
| Guardrails | Guardrails AI, NeMo Guardrails, Llama Guard |
| Cache | Redis (semantic caching) |

---

## Related

- [`../roadmap/active-track-10-week.md`](../roadmap/active-track-10-week.md) — when each layer
  gets built
- [`../learning/deep-dives/rag-system-deep-dive.md`](../learning/deep-dives/rag-system-deep-dive.md)
- [`interview-bank.md`](interview-bank.md) — questions 6–21 map onto this document
- [`../cheat-sheets/prompt-design.md`](../cheat-sheets/prompt-design.md)

*Extracted 2026-08-02 from `docs/plan/archive/Python-essentials-for-AI-engineers.md`*
