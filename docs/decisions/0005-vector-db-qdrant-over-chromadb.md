# ADR-0005: Vector DB — Qdrant primary, ChromaDB as a one-week comparison

- **Status:** Accepted
- **Date:** 2026-08-02
- **Deciders:** Workspace owner
- **Tags:** ai, rag, infra, data

## Context

The newly adopted 10-week track ([ADR-0004](0004-adopt-10-week-ai-engineer-track.md)) specifies
**ChromaDB** as the vector database (`docs/plan/AI_Engineer_Roadmap.md:70, 216`). The repo is
already committed to **Qdrant** in five places:

- [ADR-0003](0003-hybrid-stack-go-fastapi.md) names Qdrant in the data layer.
- `infra/docker/docker-compose.yml` runs a Qdrant service.
- `infra/docker/qdrant/config/config.yaml` holds its configuration.
- `docs/cheat-sheets/qdrant.md` documents day-to-day usage.
- `docs/learning/paths/rag-qdrant.md`, `docs/learning/deep-dives/rag-system-deep-dive.md`, and
  `docs/learning/deep-dives/athar-retrieval-deep-dive.md` all assume it.

Adopting the plan verbatim would abandon working infrastructure and contradict an accepted ADR.
Ignoring the plan's choice would discard a genuine learning opportunity, since "explain the
trade-offs between vector databases you've used" is a standard interview question — it appears
as question 13 in the plan's own bank (`docs/plan/AI_Engineer_Roadmap.md:248`).

There is also a functional consideration specific to the week 2–3 deliverable. The active track
requires **hybrid retrieval** (dense + BM25 sparse) with reranking. Qdrant supports sparse
vectors and fusion natively. ChromaDB does not, so a hybrid implementation on Chroma means
running and merging a separate keyword index by hand.

## Decision Drivers

- **Don't abandon working infrastructure.** Qdrant is already containerized and configured; the
  setup cost is sunk.
- **Consistency with accepted decisions.** ADR-0003 committed to Qdrant; reversing it needs a
  reason stronger than "the new plan said Chroma."
- **Job-posting relevance.** Both Qdrant and Chroma appear by name in listings
  (`Python-essentials-for-AI-engineers.md:2102`), so neither choice is a market liability.
- **Hybrid search is a week 2–3 requirement**, and native support materially reduces the work.
- **Interview answer quality.** A measured comparison beats a memorized one. The difference
  between "Qdrant does hybrid natively, Chroma doesn't" and "I ran the same 25-question golden
  set through both and here are the recall and latency numbers" is the difference between a
  junior and a mid-level answer.
- **Portability is cheap if designed in.** A store abstraction costs little at the start and a
  great deal to retrofit.

## Options Considered

### Option A — ChromaDB only, following the plan literally

- Pros: zero setup; the plan's tutorials and examples work unmodified; simplest possible week 3.
- Cons: contradicts ADR-0003; abandons the existing compose service and config; no native hybrid
  search, so week 3's hybrid deliverable requires hand-rolling BM25 merge logic; leaves the
  Qdrant cheat-sheet and three deep-dives describing infrastructure no longer in use.

### Option B — Qdrant only

- Pros: simplest coherent choice; already running; native hybrid + payload filtering; consistent
  with every existing artifact.
- Cons: the "vector DB trade-offs" interview answer stays theoretical — the honest response
  becomes "I've only used one"; no exposure to the embedded/in-process model that Chroma
  represents, which is a real architectural category worth having touched.

### Option C — Qdrant primary, behind a `VectorStore` Protocol, with one week on Chroma

- Pros: keeps existing infrastructure and ADR-0003 intact; the Protocol makes the swap a
  configuration change rather than a rewrite; produces a measured comparison (recall@k, MRR,
  p50/p95 latency, ingest time, operational friction) on an identical golden set; demonstrates
  interface-driven design, which is itself reviewable evidence; the abstraction is genuinely
  useful later if a managed store is ever needed.
- Cons: roughly 1–2 extra days; a second adapter to keep working; mild risk that the Protocol is
  over-abstracted for a two-implementation problem.

## Decision

Adopt **Option C**.

**Qdrant is the primary store** for DevMate and for all downstream work. Retrieval code depends
on a `VectorStore` Protocol in `devmate/src/devmate/index/store.py`, never on a concrete client.
Two adapters implement it: `qdrant_store.py` (primary) and `chroma_store.py` (comparison).
Selection is by environment variable, not by code change.

The Protocol surface is kept deliberately small — roughly `upsert`, `search`, `delete`,
`count` — so that it stays a thin port rather than a framework. If a third store is ever needed
and the Protocol has to grow awkwardly, that is the signal to revisit this ADR rather than to
widen the interface.

**One comparison week** (inside weeks 2–3) runs the same 25-question golden set through both
adapters and records, in `evaluations/rag/reports/`:

| Dimension | Measured how |
| --- | --- |
| Retrieval quality | recall@5, recall@10, MRR on the golden set |
| Latency | p50 / p95 query latency at fixed corpus size |
| Ingest | wall-clock time to index the same corpus |
| Hybrid support | native vs. hand-rolled; lines of code required |
| Filtering | metadata/payload filter expressiveness |
| Operations | container footprint, persistence model, failure behaviour |

That report is the artifact that answers interview question 13, and it is cited from the
portfolio README.

## Consequences

- **Positive:** existing Qdrant infrastructure and ADR-0003 remain valid; hybrid search in week 3
  uses native support instead of hand-written fusion; the store swap is a config change; the
  comparison produces a citable eval report and converts a theoretical interview answer into a
  measured one; the Protocol is reviewable evidence of interface-driven design.
- **Negative:** two adapters to maintain instead of one; ~1–2 days of schedule; the Protocol adds
  one indirection layer that a single-store project would not need; the plan's Chroma-based
  tutorials need light translation to the Protocol.
- **Watch:** the comparison week is time-boxed. If the Chroma adapter is not producing numbers
  within two days, ship the Qdrant-only path and record the abandonment in the eval report —
  an honest "I started a comparison and cut it for time, here's what I had" is still a better
  interview answer than silence, and far better than a slipped schedule.
- **Follow-ups:**
  - Chunking-strategy ADR (week 3), which depends on the eval harness this decision assumes.
  - If DevMate is ever deployed somewhere without a container runtime, revisit — Chroma's
    embedded mode becomes an advantage in that scenario.

## Links

- Related ADRs: [0003](0003-hybrid-stack-go-fastapi.md) (committed to Qdrant),
  [0004](0004-adopt-10-week-ai-engineer-track.md) (adopted the plan that specified Chroma)
- Infrastructure: `infra/docker/docker-compose.yml`, `infra/docker/qdrant/config/config.yaml`
- Reference: `docs/cheat-sheets/qdrant.md`, `docs/learning/paths/rag-qdrant.md`
- Eval output: `evaluations/rag/reports/` (week 3)
- Interview question this answers: `docs/reference/interview-bank.md` Q13
