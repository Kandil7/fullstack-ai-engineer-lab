# ADR-0004: Adopt the 10-week AI-Engineer track as the active plan

- **Status:** Accepted
- **Date:** 2026-08-02
- **Deciders:** Workspace owner
- **Tags:** roadmap, planning, ai, career

## Context

Three plans currently live in this repo and contradict each other on timeline, ordering,
technology, and target role:

| Document | Timeline | Ordering | Vehicle | Target role |
| --- | --- | --- | --- | --- |
| `docs/roadmap/master-roadmap.md` + `ROADMAP.md` | 12 months | Go → frontend → AI in months 10–12 | ThanaweyaGPT | Full-Stack AI Engineer |
| `docs/plan/7-Day-Full-Stack-AI-Plan.md` | 7 days | overview sweep of 7 layers | — | orientation only |
| `docs/plan/AI_Engineer_Roadmap.md` (added 2026-08-02) | 8–10 weeks | AI-first; Go absent entirely | DevMate | Remote AI Engineer (LLM/GenAI) |

`master-roadmap.md:3` declares itself "the single source of truth" and states "phases don't
change." That claim is no longer true, and nothing in the repo resolves the conflict. Every
planning session therefore begins by re-litigating which plan applies — the exact decision
fatigue `docs/tracking/current-focus.md` was created to eliminate.

Two further facts force the decision now.

**The 12-month plan is mis-calibrated against actual repo state.** It schedules "Python basics
for AI" at weeks 37–38 and "Simple chatbot with LLM API" at weeks 39–40. The repo already
contains 354 Python files: `01-core-python/` (41 topics with lecture + glossary each),
`02-advanced-python/` (all 20 topics — decorators, generators, context managers, async/await,
type hints, dataclasses, ABC, functools, itertools, descriptors, metaclasses, threading,
logging, patterns), `03-libraries/` (numpy, pandas, matplotlib, scipy), and
`05-web-frameworks/fastapi/` (25 topics, each with a matching exercise). Following the 12-month
plan as written means spending months 1–9 on material the owner has substantially completed,
then reaching the AI work — the actual goal — in mid-2027.

**The output mode is inverted.** `projects/04-ai-engineering/` holds 6,947 lines of finished AI
exercises (LLM API integration, prompt engineering, vector embeddings, RAG at 835 lines, agents
at 892, evaluation at 823, deployment, multi-agent, safety) plus 10 agent exercises, 10 security
exercises, and a lecture + glossary + quiz for each. `grep -c TODO` across all 19 files returns
0 — these are finished reference implementations, not practice scaffolds. Meanwhile the folders
that would hold a running system are empty:

```text
projects/04-ai-engineering/rag-system/         → .gitkeep + README
projects/04-ai-engineering/prompt-engineering/ → .gitkeep + README
projects/04-ai-engineering/embeddings/         → .gitkeep + README
projects/07-capstone/thanaweyagpt/*            → .gitkeep + README (all 5 subdirs)
```

The repo produces curriculum, not deployed systems. Both source plan documents warn about this
failure mode explicitly (`Python-essentials-for-AI-engineers.md:1963`: "at a certain point,
talking about learning becomes a substitute for learning"). No plan change fixes this by itself;
the plan must be paired with a constraint on output mode (see Consequences).

## Decision Drivers

- **Stated goal is employment**, specifically a remote AI/LLM engineering role, not breadth of
  coursework. Time-to-first-application is the metric that matters.
- **Actual completed work** is Python + FastAPI + AI curriculum — not Go, not frontend. The plan
  should start from where the owner is, not where the 12-month plan assumed they would be.
- **Market alignment.** The 10-week plan's focus (RAG + agents + production concerns) matches
  current remote job postings; `Python-essentials-for-AI-engineers.md:2095-2113` documents a
  requirement-by-requirement match against real listings.
- **Availability is full-time** (5+ hours/day), which is what makes a 10-week compression
  feasible at all.
- **One cumulative project** beats scattered demos for portfolio and interview narrative.
- **Sunk artifacts must not be discarded.** ADRs, templates, workflows, registries, and the
  existing curriculum stay valuable regardless of which plan governs.

## Options Considered

### Option A — Keep the 12-month master-roadmap; treat the new plan as reference

- Pros: no churn in existing tracking artifacts; preserves the Full-Stack framing including Go
  and Flutter; the roadmap's phase structure is already wired into `milestones.md`,
  `progress-dashboard.md`, and `skills-matrix.md`.
- Cons: schedules already-completed Python work across months 1–9; defers the actual goal to
  mid-2027; ignores that the owner's demonstrated momentum is entirely in Python/AI; leaves the
  contradiction between plans unresolved for another year.

### Option B — Adopt the 10-week AI-first track; demote the 12-month plan to a long track

- Pros: starts from actual completed state; time-to-application ~3 months; single cumulative
  deployable project; matches current market demand; the 12-month plan survives as a
  post-employment depth track rather than being deleted.
- Cons: Go, Flutter, and Next.js work pauses indefinitely; the "Full-Stack" identity narrows to
  "AI Engineer with backend fundamentals"; classical ML/DL is deferred (addressed below);
  requires rewriting the tracking layer.

### Option C — Run both in parallel (AI-first primary, 2 days/week on Go)

- Pros: keeps the full-stack story alive; hedges if AI roles prove harder to land than expected.
- Cons: 10-week compression assumes full-time focus — removing 2 days/week makes it a 16-week
  plan while presenting as a 10-week one; splits attention across two unrelated stacks during
  the phase that most needs depth; neither track reaches a deployable state on schedule.

## Decision

Adopt **Option B**. The 10-week AI-Engineer track becomes the **active plan of record**, ported
into `docs/roadmap/active-track-10-week.md` as a versioned English artifact.
`docs/roadmap/master-roadmap.md` is **demoted to the long track** — retained, explicitly marked
non-active, and repositioned as post-employment depth (Go services, Flutter/Next.js clients,
ThanaweyaGPT capstone).

Four corrections are applied to the source plan as part of adoption, each recorded in the active
track document:

1. **Evaluation moves from week 8 to weeks 2–3.** The source plan asks the learner to "try 3
   chunking strategies and compare results" in week 3 while introducing RAGAS in week 8. Without
   a measurement harness that comparison produces opinions, not data. A golden-set eval harness
   is now a week 2–3 deliverable and a precondition for the chunking ADR.
2. **Observability moves from week 8 to week 1.** The source transcript itself advises connecting
   Langfuse "from day one of this phase, not last"
   (`Python-essentials-for-AI-engineers.md:1742`); the distilled roadmap contradicted its own
   source. Tracing and per-request cost tracking are week 1 deliverables.
3. **CI/CD is added at week 0.** The source plan contains no CI across all 10 weeks, while
   simultaneously arguing that the GitHub profile *is* the CV for remote hiring
   (`Python-essentials-for-AI-engineers.md:2050`). A repo with no pipeline is a visible negative
   to exactly the audience being targeted.
4. **A 3-day SQL sprint is added to week 4.** SQL is listed as required twice in the source
   (lines 54 and 1798) and scheduled zero times. It is folded into week 4 as persistence for
   conversations and eval runs rather than as standalone study.

Two scope decisions are recorded explicitly rather than left implicit:

- **Classical ML/DL is deliberately deferred**, not omitted. No scikit-learn, no PyTorch, no
  attention-mechanism internals during weeks 0–10. This is defensible for an applied-LLM
  generalist role and indefensible for a research-leaning one; the source document itself warns
  that "AI Engineer" spans roles with a 3× pay spread
  (`Python-essentials-for-AI-engineers.md:1992`). A deferred ML sprint is scheduled at week 11+
  into the existing `projects/00-core-foundations/python/07-machine-learning/` folder.
- **10 weeks of work are planned into a 12-week window.** The source plan has zero buffer; one
  bad week cascades through every subsequent one. Two float weeks are built in and are not to be
  filled with new scope.

## Consequences

- **Positive:** one unambiguous plan of record; work starts from actual completed state rather
  than a stale assumption; a single deployable artifact (DevMate) accumulates portfolio value
  every week; time-to-first-application drops from ~14 months to ~10 weeks; the four corrections
  close defects that would otherwise have produced unmeasurable results (chunking without eval)
  or an unhireable-looking repo (no CI).
- **Negative:** Go and frontend skills stall — the `auth-service` MVP (M4) and the Flutter/Next.js
  phases are indefinitely deferred; the "Full-Stack AI Engineer" title the repo is named after
  becomes aspirational rather than descriptive for the next several months; classical ML remains
  a known gap that will surface in interviews for research-adjacent roles; the entire tracking
  layer must be rewritten, and milestones M1–M9 are largely deferred rather than completed.
- **Watch:** the buffer weeks must stay empty. The observed failure mode in this repo is scope
  expansion into curriculum authoring; if week-11 and week-12 float absorb new lecture/glossary
  work, the plan has failed in the same way its predecessor did.
- **Enforcement rule adopted with this ADR:** *no new lecture, glossary, or quiz file is created
  until DevMate is deployed at a public URL.* Given a 6,947-lines-written to 0-services-running
  ratio, this constraint is the operative part of the decision, not the schedule.
- **Follow-ups:**
  - [ADR-0005](0005-vector-db-qdrant-over-chromadb.md) — resolve the Qdrant/ChromaDB conflict the
    new plan introduces.
  - A staleness test is added to `tests/repo-structure/validate.ps1` so that
    `docs/tracking/current-focus.md` older than 8 days fails the suite. The tracking layer went
    five weeks stale under the previous plan; a red test is more reliable than a habit.
  - Reassess this ADR at the week-10 boundary or on first job offer, whichever comes first.

## Links

- Related ADRs: [0001](0001-repo-centric-workspace.md) (repo-centric workspace),
  [0003](0003-hybrid-stack-go-fastapi.md) (hybrid stack — now partially dormant, since the Go
  layer pauses), [0005](0005-vector-db-qdrant-over-chromadb.md)
- Active plan: `docs/roadmap/active-track-10-week.md`
- Demoted long track: `docs/roadmap/master-roadmap.md`
- Source documents (archived): `docs/plan/archive/AI_Engineer_Roadmap.md`,
  `docs/plan/archive/Python-essentials-for-AI-engineers.md`
- Decomposed reference material: `docs/reference/`
