# Practice Workbooks — Mastery Through Real-World Problems

> Companion practice system for the curriculum lectures. Every **section** of every lecture
> is paired with a **real-world problem** an AI engineer actually faces in production, and
> every **topic** inside that section gets three mastery levels with verification.

## The four workbooks

| # | Module | Lecture | Practice workbook | Track weeks |
|---|--------|---------|-------------------|-------------|
| 1 | LLM Fundamentals & API Integration | [`../lectures/01-llm-fundamentals.md`](../lectures/01-llm-fundamentals.md) | [`01-llm-fundamentals-practice.md`](01-llm-fundamentals-practice.md) | Week 1 |
| 2 | RAG Systems | [`../lectures/02-rag-systems.md`](../lectures/02-rag-systems.md) | [`02-rag-systems-practice.md`](02-rag-systems-practice.md) | Weeks 2–3 |
| 3 | AI Agents | [`../lectures/03-agents.md`](../lectures/03-agents.md) | [`03-agents-practice.md`](03-agents-practice.md) | Weeks 5–6 |
| 4 | Evaluation & Observability | [`../lectures/04-evaluation-observability.md`](../lectures/04-evaluation-observability.md) | [`04-evaluation-observability-practice.md`](04-evaluation-observability-practice.md) | Weeks 2–3, 7 |

## The mastery protocol (applies to every topic)

**A topic is mastered when all three levels are done AND verified — not when it "feels understood".**

```
Level 1 — Drill       (20–45 min)   mechanics: small, deterministic, assertable
Level 2 — Applied     (1–3 h)       real work inside DevMate, produces a repo artifact
Level 3 — Stretch     (3–6 h)       senior-grade: scale, failure, security, cost, trade-offs
```

Rules:

1. **Verify before moving on.** Level 1 needs an assertion/pytest result; Level 2 needs an
   artifact in the repo (file + measured output); Level 3 needs a written justification
   (ADR-style or `mistakes.md` entry). If you can't prove it, it isn't done.
2. **Applied tasks anchor to DevMate** — `projects/04-ai-engineering/devmate/` — per
   [ADR-0006](../../decisions/0006-adopt-master-ai-engineering-curriculum.md): curriculum
   content must be production-focused and trace to a DevMate concept or an interview answer.
3. **Every section's real-world problem is the lens.** Read it first; the drills exist to
   give you the tools the problem needs, the applied task is a slice of the problem, and the
   stretch task is the full problem under production constraints.
4. **Interview questions are answered out loud**, not in writing — 2-minute recorded answers
   per the track's Technical English rule (`docs/roadmap/active-track-10-week.md` §7).
5. **Failure modes are study material, not decoration.** When you hit one in a task, log it
   in `mistakes.md` — that is the track's explicit learning loop.

## Per-topic template (keep this format when extending)

```markdown
### Topic — Name

**Mastery =** <observable: "you can build X, explain Y, debug Z">

**Level 1 — Drill** (mechanics, 20–45 min)
- Task statement with starter code and expected output/assertions.

**Level 2 — Applied** (DevMate, 1–3 h)
- Task in the real repo: exact path(s), deliverable, acceptance criteria.

**Level 3 — Stretch** (production-grade, 3–6 h)
- Senior problem: scale, failure, security, cost, or a design trade-off
  requiring a written decision.

**Verify:** exact commands + expected results.

**Common failure modes:** symptom → cause → fix.

**Interview:** the question + what a strong answer covers (structure, not a script).
```

## Real-world problem standards

Each section opens with a **real-world problem** — not a toy. A good problem:

- Names a concrete business context (e.g., "a legal-tech startup", "an e-commerce copilot").
- States the failure or constraint that makes the topic necessary (cost blow-up, silent
  wrong answers, an agent that never terminates, a regression that shipped).
- Asks for a decision the engineer must make, with the trade-offs visible.
- Is solvable inside this repo (DevMate is the test corpus — the whole repo is indexable,
  and `evaluations/` is the measurement home).

## Definition-of-done for the whole system

- [ ] Every section 1.1–4.9 has a real-world problem.
- [ ] Every topic has Drill + Applied + Stretch + Verify + Failure modes + Interview.
- [ ] Every Applied task references an existing repo path (verified).
- [ ] `make eval`, `make ci`, and pytest commands cited are real (see
      `projects/04-ai-engineering/devmate/` and root `Makefile`).
- [ ] Each workbook links back to its lecture; each lecture links forward to its workbook.

*Created 2026-08-11 under ADR-0006 (production-focused curriculum anchored to DevMate).*
