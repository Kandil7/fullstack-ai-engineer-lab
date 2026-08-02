<!-- markdownlint-disable MD029 MD036 -->
<!-- Question numbering is continuous 1-27 and cross-referenced from other docs
     (e.g. "Q13", "Q22-24"). Do not renumber per section. -->

# Interview Bank — AI/LLM Engineer

> 27 questions. Source: planning conversation 2026-07-31, decomposed 2026-08-02.
> **Questions 22–24 were lost when the conversation was distilled into
> `AI_Engineer_Roadmap.md` (which jumps 21 → 25); they are restored here.**

## How to use this

1. Two questions per day from week 8 onward.
2. Write the answer first — 5–10 lines.
3. Say it aloud, recorded, without reading.
4. Play it back, fix what was vague, repeat.

Behavioral answers use **STAR** — Situation, Task, Action, Result.

**Every technical answer should reference DevMate.** "In DevMate I measured…" beats "generally
one would…" in every case. That is the entire reason the project is built the way it is.

---

## Behavioral

Almost every interview opens here.

1. Walk me through your background and why you're interested in AI engineering.
2. Tell me about a project you built. What was the biggest technical challenge?
3. Describe a time you had to debug a system that wasn't behaving as expected.
4. How do you stay updated with the fast-moving AI/LLM landscape?
5. Tell me about a time you disagreed with a technical decision. How did you handle it?

**Preparation notes.** Q2 is DevMate — have one specific hard problem ready with numbers
attached. Q3 should come from `devmate/mistakes.md`, which is written for exactly this.
Q4 wants a concrete routine, not a list of newsletters.

---

## Technical — LLM and RAG

6. Walk me through how you'd design a RAG pipeline for a company with a million documents.
7. What's the difference between fine-tuning and RAG? When would you choose one over the other?
8. How do you handle hallucination in an LLM-powered application?
9. Explain chunking strategies. How do you decide chunk size for a given use case?
10. What's the difference between semantic search and keyword search? When would you combine them?
11. How would you evaluate the quality of a RAG system's responses?
12. What is prompt injection, and how do you defend against it?
13. Explain the trade-offs between different vector databases you've used.

**Preparation notes.** Q9 and Q13 are answerable with measurements because of the week 2–3 eval
harness and the Qdrant/Chroma comparison — cite the tables in `evaluations/rag/reports/`.
Q11 is RAGAS applied to your own golden set. Q12 is `devmate/src/devmate/guards/input.py` plus
the OWASP LLM top-10 tests. Q6 is scale reasoning: sharding, index refresh, ingest pipeline,
cost at a million documents.

Background: [`llm-production-architecture.md`](llm-production-architecture.md).

---

## Technical — system design

14. Design an AI-powered customer support chatbot for an e-commerce company. Walk me through
    your architecture.
15. How would you reduce latency in an LLM application without sacrificing quality?
16. How do you control costs in a production LLM system?
17. How would you handle a scenario where the LLM API you depend on goes down?
18. What monitoring would you put in place for an LLM application in production?

**Preparation notes.** Draw the pipeline from
[`llm-production-architecture.md#2-request-pipeline`](llm-production-architecture.md) and adapt
it out loud. Q16 is answerable in dollars — you tracked cost per request from week 1. Q17 is
the fallback chain built in week 7. Q18 is Langfuse, wired in week 1.

---

## Technical — agents

19. Explain the ReAct pattern. How does it differ from a simple prompt-response loop?
20. How do you prevent an agent from getting stuck in an infinite loop?
21. What's the role of function calling / tool use in agent systems?

**Preparation notes.** Q20 has a test behind it — week 6 requires provable loop prevention.
Cite the step cap and the detection mechanism. Bonus material: you built an MCP server, which
few candidates have; bring it up on Q21.

---

## Coding

*(Restored — these were dropped in the distilled roadmap.)*

22. Implement a simple caching mechanism for LLM API calls.
23. Write a function to chunk a large text document with overlap.
24. Given this API response, extract and structure the data using Pydantic.

**Preparation notes.** All three exist in DevMate: `cache/`, `ingest/chunkers/`, and
`llm/schemas.py`. Practice writing each from memory in under 15 minutes. Q23 in particular —
off-by-one errors at the overlap boundary are the standard failure, so write the edge-case
tests too. Expect a live-coding format; narrate while typing.

---

## Questions to ask them

Asking well-informed questions is itself a signal.

25. What does the LLM/AI stack look like here — which frameworks and vector DB do you use?
26. How does the team approach evaluation and monitoring for LLM features in production?
27. What's the biggest technical challenge the team is facing right now with AI features?

Q26 is the strongest of the three: teams doing evaluation seriously recognize the question, and
teams that aren't will reveal it.

---

## Two-minute explanations to have ready

Recorded in week 8, per the active track:

1. **What DevMate is** — problem, approach, outcome. No jargon.
2. **The RAG pipeline** — ingest through answer, with the measurements that drove each choice.
3. **The hardest bug** — symptom, hypotheses, diagnosis, fix, what changed afterward.

---

## Related

- [`llm-production-architecture.md`](llm-production-architecture.md) — Q6–Q21 background
- [`ml-fundamentals-map.md`](ml-fundamentals-map.md) — for fundamentals questions not covered here
- [`remote-job-logistics.md`](remote-job-logistics.md) — compensation and contract conversations
- [`../roadmap/active-track-10-week.md`](../roadmap/active-track-10-week.md) — week 8 preparation

*Extracted 2026-08-02 from `docs/plan/archive/Python-essentials-for-AI-engineers.md` (lines
2196–2266), restoring Q22–24 lost in `AI_Engineer_Roadmap.md`.*
