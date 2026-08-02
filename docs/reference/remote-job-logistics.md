# Remote Job Logistics

> Platforms, contracts, payments, compensation. Source: planning conversation 2026-07-31,
> decomposed 2026-08-02. Applied in weeks 9–10 of the
> [active track](../roadmap/active-track-10-week.md).

Target: **remote roles with international companies**, not the local market. The compensation
gap between the two is the reason the whole plan is shaped this way.

---

## 1. Where to apply

| Platform | Type | Notes |
| --- | --- | --- |
| **Wellfound** (formerly AngelList) | startups hiring remote globally | strongest single source for this profile |
| **RemoteOK** · **We Work Remotely** | remote-only job boards | high volume, apply fast — good listings close quickly |
| **LinkedIn** (Remote filter) | everything + networking | still the highest-volume channel |
| **workatastartup.com** (Y Combinator) | YC companies, many remote-first | strong fit for portfolio-based hiring |
| **Toptal** · **Turing** | contracting / freelance | a viable entry route when direct employment stalls |

**Cadence:** 20 applications per week during weeks 9–10, logged in
`docs/tracking/applications.md`.

---

## 2. What actually gets you hired

For remote roles the GitHub profile *is* the CV. Screening is portfolio-first far more often
than credential-first, especially at startups.

- **A working, deployed project** with a public URL beats a list of technologies.
- **Clean, regular commit history** signals reliability to people who will never sit near you.
- **A professional README** — architecture diagram, measured results, cost figures, demo.
- **Open-source contributions** carry extra weight for remote specifically: they prove you can
  work with a distributed team without supervision.
- **Written communication.** Nearly every posting asks for it, and for remote work it is not
  boilerplate — most collaboration is asynchronous and written.

Most postings mentioning a CS degree treat it as preferred, not required. Portfolio and
demonstrated ability substitute in practice.

---

## 3. Contract types

| Type | What it means |
| --- | --- |
| **W-2 employee** | US employment: benefits, tax withheld. Rare for candidates outside the US. |
| **1099 contractor** | US independent contractor: higher gross, no benefits, self-managed taxes. |
| **EOR** (Employer of Record) | The company hires through Deel, Remote.com, Oyster, etc., which employs you locally. The most common structure for international remote hires. |
| **Direct contractor** | Contract straight with the company; you handle invoicing and local compliance. |

Understand which is being offered before discussing numbers — the same headline figure means
very different take-home across these.

---

## 4. Payments

Set this up **before** it is needed, not during an offer negotiation:

- **Wise** or **Payoneer** for receiving international payments.
- Check local regulations on receiving foreign currency and on declaring foreign income.
- Understand the fee structure — spread and transfer fees differ substantially between
  providers.

---

## 5. Timezone

Many US companies want **3–4 hours of overlap** with their team. This is one of the most common
silent filters in remote hiring.

Address it directly rather than waiting to be asked: state the overlap you can offer and be
concrete about which hours. Being explicit and flexible here removes a real objection.

---

## 6. Compensation benchmarks

⚠️ **Point-in-time figures (2026), US/remote market. Ranges are wide and move.** Use for
orientation, not as a negotiating position.

| Level | Base salary |
| --- | --- |
| Entry | $115K–$135K |
| Mid | $140K–$185K |
| Senior | $220K–$310K base ($340K–$550K total comp) |
| Staff / Principal | $280K–$400K base ($500K–$800K total comp) |
| Frontier labs (senior) | $300K–$500K+ total comp |

**The caveat matters more than the numbers.** "AI Engineer" spans at least five distinct jobs
— from wiring a RAG pipeline over a hosted API to training models on GPU clusters. The spread
between an applied generalist and a research engineer at the same nominal level can reach 3×.
Read the actual responsibilities in the posting before anchoring on a range.

---

## 7. Technical English

Required, and best acquired as a byproduct rather than as a separate subject.

- Code, comments, commits, PRs, documentation, and personal notes in English from day one.
- 3×/week, 30–45 minutes: an untranslated tech talk · an article read and summarized in writing
  · two minutes of recorded self-explanation.
- Weeks 7–8: mock interviews in English.
- Tools: Grammarly for writing; DeepL for checking a phrasing, not for wholesale translation.

The recorded self-explanation is the highest-value item — speaking is the weakest channel for
most non-native engineers and the one interviews test hardest.

---

## 8. Application tracking

`docs/tracking/applications.md`:

| Field | Purpose |
| --- | --- |
| Date, company, role, platform | volume and channel effectiveness |
| Stack from the posting | which technologies keep appearing |
| Status | applied / screened / interviewing / rejected / offer |
| Gap identified | **what you couldn't answer** |
| Action | the task created to close it |

The gap column is the point. Every rejection or stumble becomes a gap entry, and every gap
entry becomes a task. Ten applications with a closed feedback loop beat fifty without one.

---

## Related

- [`interview-bank.md`](interview-bank.md) — 27 questions with preparation notes
- [`../roadmap/active-track-10-week.md`](../roadmap/active-track-10-week.md) — weeks 9–10
- `docs/career/` — CV and recordings (created in week 8)

*Extracted 2026-08-02 from `docs/plan/archive/Python-essentials-for-AI-engineers.md`*
