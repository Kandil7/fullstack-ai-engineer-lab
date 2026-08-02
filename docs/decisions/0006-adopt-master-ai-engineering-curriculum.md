# ADR-0006: Lift the lecture moratorium — adopt the Master AI Engineering curriculum

- **Status:** Accepted
- **Date:** 2026-08-02
- **Deciders:** Workspace owner
- **Tags:** ai, curriculum, learning, content

## Context

[ADR-0004](0004-adopt-10-week-ai-engineer-track.md) established a **governing rule**: no new
lecture, glossary, or quiz file until DevMate is deployed at a public URL (week 4). The rule
existed because the repo held ~6,947 lines of AI teaching material and zero running services,
and the ratio needed to invert.

Two things changed since:

1. **DevMate is no longer zero running services.** The workspace now ships a substantial
   implementation — CLI (`stats`/`ask`/`ingest`/`serve`/`cost`), LLM client with tracing and
   cost tracking, RAG pipeline with three chunkers, vector-store protocol, API server, guards,
   semantic cache, and an MCP server — with CI gating it. The "zero services" premise of the
   moratorium no longer holds.
2. **The interview bank and portfolio milestones (A7–A9) require articulate, detailed answers.**
   Weeks 8–10 expect the owner to *explain every decision* and answer 27 interview questions.
   That depth is produced by teaching material — lectures, glossaries, exercises, quizzes, case
   studies — which the moratorium suppressed. The curriculum is now the *raw material for the
   portfolio*, not a substitute for building.

The owner additionally requested a **full, detailed Master AI Engineering curriculum** covering
LLMs, prompting, embeddings, RAG, agents, evaluation, observability, production deployment,
safety, fine-tuning, and system design — with lectures, glossaries, exercises, quizzes, code
examples, case studies, code challenges, and real-world production implementations.

## Decision Drivers

- **The ratio argument is satisfied differently now.** The leverage is no longer "stop writing
  lectures" but "each lecture must demonstrate production-grade knowledge" — measured against
  the DevMate codebase and interview answers, not against nothing.
- **Interview-readiness is a milestone.** A7 asks for drafted answers to 27 questions; a
  curriculum organized by the same topics is the fastest path to those drafts.
- **Repo convention is established.** `projects/04-ai-engineering/` already contains four
  modules (`ai-automation`, `agents`, `security`, `fastai-deep-learning`), each with
  `lectures/` (lecture + glossary per topic), `exercises/`, and `quizzes/`. A new module must
  follow the same convention and add the two requested content types: `case-studies/` and
  `challenges/`.
- **Legacy debt blocks the gate.** The Python legacy curriculum has 34 failing files
  (measured 2026-07-29, `projects/00-core-foundations/python/admin/mastery-plan/10-remediation-backlog.md`).
  The moratorium's spirit — don't build on a broken baseline — now applies to *repairing* that
  baseline, not to withholding new content.

## Options Considered

### Option A — Keep the moratorium until week 4, then build content

- Pros: plan fidelity; no rule churn.
- Cons: ignores that DevMate already ships; delays the interview-prep material until after the
  deploy window; leaves the legacy remediation backlog untouched for another month.

### Option B — Lift the rule via ADR, add the curriculum as a content track, repair the legacy backlog

- Pros: honest rule change recorded as an ADR (the repo's own process for changing plans);
  content track directly feeds A7 interview answers; legacy repairs restore the CI gate the
  moratorium was protecting.
- Cons: two workstreams (DevMate + curriculum) instead of one; must guard against the
  "lectures instead of shipping" failure mode the original rule feared.

### Option C — Lift the rule silently, no ADR

- Cons: violates the repo's own decision process ("record any change as an ADR, not a silent
  edit" — WEEKLY_PROTOCOL §6); would confuse the staleness test and future readers.

## Decision

Adopt **Option B**.

1. **The governing rule is amended.** New lectures, glossaries, quizzes, case studies, and
   challenges are permitted — *provided the curriculum content is production-focused and each
   module is anchored to the active DevMate work*. ADR-0004's governing rule is superseded by
   this ADR for the lecture/glossary/quiz restriction; everything else in ADR-0004 stands.
2. **A new content track is created:** `projects/04-ai-engineering/master-ai-engineering/` with
   the standard module layout plus `case-studies/` and `challenges/`. It is a **study track,
   not a schedule change** — the 10-week DevMate build remains the plan of record, and the
   curriculum is consumed *after* the day's building, per WEEKLY_PROTOCOL §2.
3. **The legacy remediation backlog is executed.** Tier 0 items R1–R7 and R9 from
   `10-remediation-backlog.md` are repaired (R8 renumbering and R10 CI extension are staged as
   follow-ups where they risk churn).
4. **The ratio rule is reframed in `current-focus.md`:** the repo must keep *at least one
   running service* (DevMate) and the curriculum must cite DevMate paths where relevant.

## Consequences

- **Positive:** interview-prep content exists in the same form as the interview bank expects;
  legacy files that taught wrong behavior stop doing so; the curriculum can reference a real
  codebase (DevMate) instead of abstract examples; the rule change is auditable in the decision
  log.
- **Negative:** two workstreams to keep coherent; the "lectures instead of shipping" failure
  mode needs active guarding (rule 6 in WEEKLY_PROTOCOL §9 now applies to the curriculum track:
  *every source studied produces an artifact*; here, every lecture must trace to a DevMate
  concept or interview answer).
- **Watch:** if the curriculum starts displacing Build time on the 10-week track for more than
  a week, the moratorium returns. That is a follow-up ADR, not a silent edit.
- **Follow-ups:**
  - R8 (pandas renumbering, 21 missing lecture/glossary pairs) and R10 (CI smoke harness
    matrix) staged after the priority repairs.
  - A7 portfolio drafting will pull directly from these modules.

## Links

- Supersedes (partially): [ADR-0004](0004-adopt-10-week-ai-engineer-track.md) governing rule §1
- Related: [ADR-0003](0003-hybrid-stack-go-fastapi.md), [ADR-0005](0005-vector-db-qdrant-over-chromadb.md)
- Backlog: `projects/00-core-foundations/python/admin/mastery-plan/10-remediation-backlog.md`
- Conventions: `projects/04-ai-engineering/ai-automation/`, `agents/`, `security/`
- Milestone this feeds: A7 (portfolio + 27 interview answers)
