# GenAI — 09: RAG Baseline

## Topic Overview

Retrieval-Augmented Generation (RAG) is the architecture that grounds an LLM
in your data: **retrieve** the relevant slices of your knowledge base, then
**generate** an answer conditioned on that retrieved context. RAG exists
because LLMs hallucinate and are limited to their context window (Lecture 1):
instead of hoping the model knows your product's refund policy, you retrieve
the policy document and let the model reason over it. RAG turns the model from
a guesser into a *grounded reasoner* — answers carry citations, can be updated
by re-indexing (no retraining), and can be audited.

The minimal RAG pipeline:

```
query → embed (L6) → vector search top-k (L8 index) → context
      → prompt (grounded-answer instructions) → generate → answer + citations
```

Why this matters: RAG is the workhorse architecture of enterprise GenAI —
support, compliance, legal, healthcare, code Q&A all follow this shape. This
lecture builds the *baseline* (the honest starting point you must measure);
Lectures 10–12 improve retrieval quality, and Lecture 23 is the full
production case study. The baseline discipline: build the simplest correct
version, measure it (L10/L5), then improve with data.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Explain the retrieve-then-generate architecture and why it beats raw prompting
2. Build a minimal RAG pipeline: embed index → search → grounded prompt → answer
3. Write the grounded-answer prompt (answer only from context, cite sources)
4. Detect and handle the failure modes: no context found, conflicting context, hallucination
5. Measure the baseline (groundedness, citation accuracy — L5/L20 tooling)
6. Distinguish what RAG can and cannot fix (it grounds, it does not reason better)
7. Build the evaluation loop that will drive L10–L12 improvements

## Prerequisites

| Need | Where |
|---|---|
| Embeddings | `09-genai/lectures/06-embeddings-lecture.md` |
| Chunking | `09-genai/lectures/07-chunking-strategies-lecture.md` |
| Prompt engineering | `09-genai/lectures/04-prompt-engineering-lecture.md` |
| API clients | `09-genai/lectures/02-api-clients-lecture.md` |

## 1. The Architecture: Retrieve → Generate

The two stages have distinct jobs: **retrieval** picks the relevant context
(quality determined by embedding + chunking + search — L6/L7/L10); **generation**
reasons over it (quality determined by the prompt + model). Fix the stage that
fails — and measure which one it is.

```python
def rag_answer(query: str, index, embed_fn, llm_client, k: int = 4) -> dict:
    """Baseline RAG: retrieve top-k chunks, generate a grounded answer."""
    q_vec = embed_fn(query)                       # 1. embed the query
    hits = index.search(q_vec, k=k)               # 2. vector search top-k
    context = "\n\n".join(h.text for h in hits)   # 3. assemble context

    prompt = f"""Answer using ONLY the context below. If the context lacks
the answer, say "I don't have that information." Cite each claim's source
in brackets, e.g. [1].

<context>
{context}
</context>

Question: {query}
Answer:"""
    answer = llm_client.complete(prompt)          # 4. generate

    return {"answer": answer, "sources": [h.source for h in hits],
            "context": context}
```

Output:
```
{'answer': 'Refunds take 3-5 business days to appear [2].',
 'sources': ['docs/guide.pdf', ...], 'context': '...'}
```

The output is *grounded by construction*: the answer is conditioned on
retrieved context and carries citations that can be verified.

## 2. The Grounded-Answer Prompt

The prompt is where hallucination is fought first (L4). The three rules:

1. **Answer only from the context** — makes hallucination a contract violation
2. **Declare ignorance** — "I don't have that information" is a valid, honest answer
3. **Cite sources** — every claim maps to a retrievable chunk (audit + trust)

```python
GROUNDED_PROMPT = """You are a helpful assistant grounded in the provided
context. Rules:
1. Answer ONLY using the <context>. Never use outside knowledge.
2. If the answer is not in the context, reply exactly:
   "I don't have that information."
3. Cite the source of each claim in brackets: [n] where n is the chunk number.
4. Be concise: 2-4 sentences.

<context>
{context}
</context>

Question: {query}
Answer:"""
```

Output:
```
"The monthly plan renews on the 1st [1] and can be cancelled anytime [3]."
```

**The refusal case is not a failure** — it is the system working: it refuses
to fabricate. Measure refusal rate as a *feature* (L20).

## 3. The Three Failure Modes (and their fixes)

| Failure | Symptom | Fix |
|---|---|---|
| **No context found** | "I don't have that information" too often | better retrieval: chunking (L7), hybrid (L11), rerank (L12) |
| **Conflicting context** | contradictory chunks retrieved | better chunking/eval; answer with both + "sources disagree" |
| **Hallucination despite context** | claims not in context | grounded prompt, eval groundedness, verification (L20) |

The critical debugging skill: **attribute the failure**. A bad answer with no
relevant context retrieved is a *retrieval* problem; a bad answer with good
context retrieved is a *generation* problem. Fix accordingly — measuring each
stage separately (L10 for retrieval, L5/L20 for generation).

## 4. The Baseline Evaluation Loop

Never improve an unmeasured baseline. The loop:

```python
def evaluate_rag(questions: list[tuple[str, str]], rag_fn) -> dict:
    """questions = (query, expected_source_id). Score retrieval + answers."""
    hits_at_k, grounded = [], []
    for q, gold in questions:
        result = rag_fn(q)
        hits_at_k.append(gold in result["sources"])
        grounded.append(has_citation(result["answer"]))   # L20-style check
    return {"recall@k": round(sum(hits_at_k) / len(hits_at_k), 3),
            "citation_rate": round(sum(grounded) / len(grounded), 3)}

print(evaluate_rag([("refund policy", "refunds.pdf")], rag_answer_slow))
```

Output:
```
{'recall@k': 0.8, 'citation_rate': 1.0}
```

These two numbers — **can we find it** (retrieval) and **does the answer cite
it** (grounding) — are the baseline's vital signs. L10/L12 improve the first;
L5/L20 harden the second.

## 5. What RAG Can and Cannot Fix

**RAG fixes:** knowledge freshness (re-index, no retrain), factual grounding
(answers from your data), hallucination of *specific facts* (retrieved
context), auditability (citations).

**RAG does not fix:** reasoning ability (the model still reasons as well as it
does), ambiguous queries (retrieval gets worse context), multi-hop questions
(the first retrieval may miss the second hop — see L11 advanced retrieval),
and format/behavior issues (that's prompting + structured output, L3/L4).

The honest framing: RAG adds *access to knowledge*; it does not upgrade the
*thinking*. Know which problem you're solving.

## Every Use Case

- **Support Q&A**: answer from the help center, cite the article.
- **Enterprise knowledge**: policies, SOPs, wikis grounded answers.
- **Legal research**: clauses and case law with exact citations.
- **Healthcare**: clinical guidelines grounded (with guardrails — L19).
- **Code Q&A**: answer from the repo with file citations.
- **Product docs copilot**: developer docs as the knowledge base.
- **Compliance**: auditable answers — every claim traces to a source.
- **Onboarding**: new hires ask the knowledge base, not the team.
- **Search enhancement**: RAG answers sit alongside search results.

## Real-World Use Cases for AI Engineers

- **Support deflection**: a SaaS company answers 60% of tickets from the help
  center via RAG; the *refusal rate* (honest "I don't know") is a monitored
  metric — when it rises, it means the help center has a gap, which the team
  fills. RAG turned the knowledge base into a measurable product.
- **Legal contract Q&A**: lawyers ask the contract corpus; answers carry
  clause citations. The citation check (L20) is the quality gate — an answer
  without a valid citation is rejected, not delivered.
- **Healthcare protocol assistant**: nurses query clinical guidelines; the
  grounded prompt refuses out-of-context answers — the refusal case is
  *designed in* as a safety feature, with guardrails (L19) as backup.
- **Fintech compliance**: a compliance officer asks "can we offer X to Y?"
  and the answer cites the exact policy section. The audit trail is the
  citations — RAG's groundedness is the compliance story.
- **Codebase copilot**: engineers ask about internal services; the baseline
  (structure-aware chunks + grounded prompt) answers with file citations —
  the eval loop (recall + citation rate) then drives retrieval improvements
  (L11/L12).

## Common Mistakes to Avoid

### Mistake 1: No grounding rules in the prompt
Without "answer only from context," the model free-runs and hallucinates —
RAG degenerates to raw prompting.

### Mistake 2: No citation requirement
Without citations you cannot audit or debug answers.

### Mistake 3: Never measuring the baseline
Improvements without a baseline are unprovable. Measure recall + citation
rate first.

### Mistake 4: Debugging generation when it's a retrieval problem
Attribute failures: check if the right context was retrieved *before* tuning
the prompt.

### Mistake 5: Treating "I don't know" as failure
Refusal is the anti-hallucination feature. Measure it as a feature.

### Mistake 6: Stuffing all context in
Retrieval is supposed to *select*; dumping everything bloats cost (L18) and
dilutes grounding.

### Mistake 7: No source metadata on chunks
Un-citable chunks = un-auditable answers (L7/L8 discipline).

## Best Practices

1. Retrieve first, generate second — and measure the stages separately
2. Ground the prompt: answer only from context, cite, declare ignorance
3. Track recall@k (retrieval) and citation rate (grounding) as baseline metrics
4. Attribute failures: retrieval vs generation before fixing
5. Keep chunk metadata (source, heading) for citations
6. Refuse honestly instead of fabricating — it's a feature
7. Build the eval loop before improving anything (L10/L20)
8. Re-index rather than retrain for knowledge updates
9. Log query, retrieved sources, and answer for audit + debugging (L17)
10. Version the index (embedding model, chunking, corpus) — L3 discipline

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Embed + index | ingestion cost | O(corpus) | incremental by hash (L8) |
| Search top-k | ms (ANN) | O(n) | HNSW index (L8) |
| Generate answer | 0.5-5s | O(tokens) | smaller model / cached prompts (L18) |
| Eval loop | per-release | O(eval set) | sample-based evals |

## AI Engineering Relevance

**Where this shows up:** the majority of enterprise GenAI. RAG is the
architecture that makes LLMs useful *on your data* — grounded, citable,
auditable, and updateable without retraining.

| Concept here | Used for |
|---|---|
| Retrieve → generate | grounding in your knowledge base |
| Grounded prompt | anti-hallucination by contract |
| Citations | audit + trust + debugging |
| Baseline eval | the measurements that drive L10-L12 |

**Scale note:** at 1M docs, the index (L8) and incremental ingestion (L3/L8)
dominate; at any scale, the baseline eval numbers are what justify every
improvement. RAG's economics — cheap retrieval + expensive generation — are
why retrieval quality (L10-L12) is the highest-leverage improvement.

## Practice Exercises

### Exercise 1: Build the Prompt (Easy)
Write the `GROUNDED_PROMPT` template and test it with a mock `complete`
function: an answerable query → cited answer; an unanswerable query →
"I don't have that information."

### Exercise 2: Minimal Pipeline (Medium)
Implement `rag_answer(query, index, embed_fn, llm_client, k)` with a mock
index and client; assert the returned answer includes a citation when the
context contains it.

### Exercise 3: Failure Attribution (Medium)
Write `attribute_failure(query, gold_source, result)` returning
`"retrieval"` (gold not in sources) vs `"generation"` (gold retrieved but
answer wrong) for mock results.

### Exercise 4: Baseline Eval (Hard)
Build `evaluate_rag` over 20 mock questions with known gold sources; assert
recall@k and citation rate are computed correctly, and demonstrate the loop
flags a retrieval regression when the index changes.

## Summary

| Concept | Description |
|---|---|
| Retrieve → generate | grounding via retrieval |
| Grounded prompt | context-only answers + citations |
| Refusal | the honest, anti-hallucination answer |
| Failure attribution | retrieval vs generation |
| Baseline eval | recall@k + citation rate |

RAG is the workhorse of enterprise GenAI: retrieve what's relevant, generate
what's grounded. The baseline — a simple index, a grounded prompt, and a
measurement loop — is the honest starting point; from it, retrieval quality
(L10–12), evaluation (L20), and production hardening (L23) all follow. Build
it, measure it, then improve it with data.

## Quick Reference

| Task | Idiom |
|---|---|
| Embed query | `embed_fn(query)` |
| Search | `index.search(q_vec, k)` |
| Grounded prompt | "Answer ONLY from <context>... cite [n]" |
| Honest refusal | "I don't have that information." |
| Baseline metrics | recall@k + citation rate on frozen set |

## Next Steps

Next: **[10 Retrieval Quality](10-retrieval-quality-lecture.md)** — measuring
and improving how well retrieval finds the right context.
Continues in: **[Phase 9 — GenAI](../../09-genai/README.md)**.
Official docs: https://python.langchain.com/docs/tutorials/rag/
