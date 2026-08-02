# Phase 2 — Athar & Baligh (deferred)

> **Not active.** Begins after the [10-week active track](active-track-10-week.md) reaches
> milestone A7 (portfolio complete) — realistically during weeks 9–10 while applications are
> out, or after a first offer.
>
> This document supersedes `docs/plan/archive/remote-ai-engineer-8-week-sprint.md`, which
> proposed Athar as the *primary* showcase. That ordering was reversed on 2026-08-02: DevMate
> ships first because it needs no content sourcing and no Arabic-retrieval evaluation work.
> The sprint's week-by-week structure and hiring-signal framing are preserved below.

---

## Why these projects, and why second

**Athar** — an Arabic-first Islamic-text RAG system. **Baligh** — Arabic LLM fine-tuning.

Both are genuinely differentiated: very few candidates have shipped Arabic retrieval or
Arabic fine-tuning, and both are hard in ways that are interesting to talk about (morphology,
diacritics, tokenizer behaviour on Arabic, dialect variance, scarce evaluation data).

They come **second** because each carries a cost DevMate does not: sourcing and licensing a
corpus, and building Arabic-language evaluation from scratch. Paying those costs before the
first job application delays the application. Paying them after turns a strong portfolio into
a distinctive one.

Existing groundwork:
[`docs/learning/deep-dives/athar-retrieval-deep-dive.md`](../learning/deep-dives/athar-retrieval-deep-dive.md),
[`docs/learning/deep-dives/baligh-training-deep-dive.md`](../learning/deep-dives/baligh-training-deep-dive.md).

---

## What DevMate transfers

Athar is not started from zero. Reusable from DevMate:

| Component | Reuse |
| --- | --- |
| `VectorStore` Protocol + Qdrant adapter | direct |
| Eval harness (`run_ragas.py`, golden-set format) | direct; new dataset |
| LLM client — streaming, retries, fallback | direct |
| Tracing and cost accounting | direct |
| FastAPI + Docker + deploy pipeline | direct |
| Guardrails | direct |
| Chunkers | **rewritten** — Arabic text structure differs fundamentally from code |
| Embedding model choice | **re-evaluated** — must be multilingual or Arabic-specific |

Roughly 70% of the infrastructure carries over. The work is in the 30% that doesn't.

---

## Sprint plan

Each week ends with a **visible artifact**. A week producing only notes is not done.

| Week | Objective | Deliverable | Hiring signal |
| --- | --- | --- | --- |
| 1 | Corpus acquisition and cleaning; licensing and provenance settled | `athar/docs/corpus.md`, ingestion pipeline | data engineering; handling messy real sources |
| 2 | Arabic-aware chunking — verse, hadith, and passage boundaries rather than character counts | `athar/src/chunkers/`, comparison note | domain-informed retrieval design |
| 3 | Arabic golden set + retrieval experiments across ≥3 strategies | `athar/eval/golden-ar.jsonl`, benchmark table | evidence-based iteration in a low-resource language |
| 4 | Evaluation harness and failure taxonomy | `athar/docs/rag-evaluation.md` | measuring quality, not demoing it |
| 5 | Agent/tool orchestration for one genuinely useful workflow | `athar/src/agent/` | agentic design |
| 6 | Package and deploy as a public demo | Dockerfile, public URL, `/health` | end-to-end ownership |
| 7 | **Baligh** — training/eval/release structure; model card | `baligh/docs/`, pipeline summary, model card | depth beyond RAG; model-side competence |
| 8 | Case studies and portfolio integration | `docs/writing/case-studies.md`, CV and README refresh | communicating value |

---

## Delivery standards

- One visible artifact per week, minimum.
- Documentation written during implementation, never after.
- Daily commits; comprehensible branch history.
- **Scope control: no third major project.** DevMate and Athar/Baligh is the ceiling.
- Measurable progress over feature count.

---

## Done criteria

Phase 2 is complete when you have:

- A second public demo or deployable endpoint (Athar).
- An evaluation document with metrics and failure analysis for Arabic retrieval.
- An agent/tool prototype in the Athar domain.
- Baligh as evidence of model-side depth — training pipeline and model card.
- A portfolio README in English presenting both projects as one coherent story.

---

## Portfolio framing

Three projects, three distinct claims:

- **DevMate** — production engineering: RAG, agents, MCP, evaluation, observability, deployment.
- **Athar** — domain depth: Arabic-first retrieval, a genuinely hard problem, evaluation built
  where no benchmark existed.
- **Baligh** — model-side breadth: fine-tuning, training pipeline, release discipline.

Together they answer "can you build production LLM systems?", "can you handle a hard domain?",
and "do you understand the model layer, not just the API?"

---

## Related

- [`active-track-10-week.md`](active-track-10-week.md) — must complete first
- [ADR-0004](../decisions/0004-adopt-10-week-ai-engineer-track.md) — the sequencing decision
- [`../learning/deep-dives/athar-retrieval-deep-dive.md`](../learning/deep-dives/athar-retrieval-deep-dive.md)
- [`../learning/deep-dives/baligh-training-deep-dive.md`](../learning/deep-dives/baligh-training-deep-dive.md)
- `docs/plan/archive/remote-ai-engineer-8-week-sprint.md` — the superseded original

*Created 2026-08-02.*
