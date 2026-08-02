# Current Focus — Execution Window

> What to work on RIGHT NOW. Update weekly. Be specific — this replaces decision fatigue.
>
> ⚠️ A staleness test in `tests/repo-structure/validate.ps1` fails the suite if this file is
> more than 8 days old. It went five weeks stale under the previous plan.

**Last updated:** 2026-08-02

---

## Active Window

**Week 0** — 2026-08-03 → 2026-08-05 (2–3 days)

**Plan:** [Active Track — 10-Week AI Engineer](../roadmap/active-track-10-week.md)
(adopted 2026-08-02 by [ADR-0004](../decisions/0004-adopt-10-week-ai-engineer-track.md))

**Project:** DevMate — `projects/04-ai-engineering/devmate/`

**Content track (new):** [ADR-0006](../decisions/0006-adopt-master-ai-engineering-curriculum.md)
lifted the lecture moratorium. The Master AI Engineering curriculum
(`projects/04-ai-engineering/master-ai-engineering/`) is now a study track that feeds the A7
portfolio and the 27 interview answers. It is consumed **after** the day's building, never
instead of it.

---

## Main Goal

Get the repo to a green CI state, ship the first DevMate command, **and repair the legacy
Python baseline** (34 failing files, `admin/mastery-plan/10-remediation-backlog.md`) so the
whole repo is honest. Week 0 is infrastructure and debt, not study.

---

## Today's Tasks

1. `make ci` passes for DevMate — verify locally, fix any lint/mypy/test gaps
2. Write DevMate unit tests (`tests/unit/`) — repo reader, chunkers, cost tracker
3. Repair Tier 0 backlog R1–R7 + R9 (hang, syntax, API drift, encoding, deps, SQL, Mongo, docs)
4. Build the **Master AI Engineering** module — 12 topics × (lecture, glossary, quiz, exercise,
   case study, code challenge)
5. Fill the empty modules: `embeddings/`, `prompt-engineering/`, `rag-system/`
6. Update registries (`prompt-registry.yaml`, `skills-registry.yaml`) and module READMEs

---

## Week 0 Success Criteria

- [ ] `make ci` passes locally
- [ ] GitHub Actions green on `master`
- [ ] `devmate stats .` prints correct statistics for this repo
- [ ] Tests exist and pass for the stats command
- [ ] Legacy backlog R1–R7, R9 closed (reproduce + verify each fix)
- [ ] `master-ai-engineering/` module complete with all 12 topics and content types
- [ ] `embeddings/`, `prompt-engineering/`, `rag-system/` no longer empty

---

## Do Not Work On

- ❌ **Unanchored lectures** — curriculum content must trace to a DevMate concept or an
  interview answer (ADR-0006). No "tutorial for its own sake".
- ❌ Go / auth-service — paused under ADR-0004, lives in the long track
- ❌ Flutter / Next.js — paused
- ❌ Athar / Baligh — [phase 2](../roadmap/phase-2-athar-baligh.md), after A7
- ❌ RAG implementation beyond the existing scaffold — week 2, after the eval harness exists
- ❌ Classical ML / PyTorch — deferred to week 11+ (A10)
- ❌ R8 pandas renumbering + R10 CI matrix — staged follow-ups; they risk churn this window

---

## Active Milestones

| ID | Milestone | Week | Status |
| --- | --- | --- | --- |
| A1 | CI green + `devmate stats` CLI | 0 | In Progress |
| A2 | LLM layer traced and costed | 1 | Planned |
| A3 | RAG with measured eval + 2 ADRs | 2–3 | Planned |
| A4 | **Deployed at a public URL** | 4 | Planned |

Full list: [`../roadmap/milestones.md`](../roadmap/milestones.md)

---

## Next Window Preview

**Week 1** (2026-08-06 → 2026-08-12) — LLM layer. Claude API with streaming, structured
outputs, retries. **Langfuse tracing and cost tracking wired in from day one**, not at the
end. First 10 golden cases. `devmate ask "<question>"` working end to end.

---

## Blockers

> What's preventing progress? Empty = no blockers.

- — (poetry is not installed on this machine; DevMate checks run under the CI workflow or a
  local venv)

---

## Notes

- Read *AI Engineering* (Huyen) ch. 1–3 during week 1 — **after** each day's building.
- English-only from here: code, comments, commits, PRs, docs, and personal notes.
- Stuck longer than 45 minutes → log it in `mistakes.md` and move on.
