# GenAI: LLMs, RAG, Agents, and Production AI - Quiz

## Topic Overview
GenAI engineering covers LLM fundamentals, token economics, structured
output, prompt engineering, embeddings, RAG, retrieval quality, agents,
evaluation, guardrails, caching/cost, fine-tuning, and production systems.
This quiz covers the core concepts of the full GenAI stack.

**Difficulty Levels:** Easy | Medium | Hard
**Total Questions:** 20

---

## Questions

### Q1. What is an LLM fundamentally?
- **A)** A database of facts
- **B)** A next-token probability distribution conditioned on the prompt
- **C)** A search engine
- **D)** A deterministic program

**Correct Answer: B** — An LLM predicts the next token given the context. That's why hallucination is *default behavior* (it has no truth model) and output is sampled, not deterministic.

---

### Q2. What is the unit of LLM cost, context, and latency?
- **A)** Words
- **B)** Tokens
- **C)** Characters
- **D)** Sentences

**Correct Answer: B** — Everything is billed, bounded, and generated in tokens (~4 chars / 0.75 words in English). Never budget in words.

---

### Q3. What sampling parameter gives deterministic output?
- **A)** temperature = 1.0
- **B)** temperature = 0 (greedy)
- **C)** top_p = 0
- **D)** max_tokens = 0

**Correct Answer: B** — temperature=0 makes the model always take the argmax token — deterministic. Use it for extraction/classification; raise it only for creativity.

---

### Q4. Why does RAG exist?
- **A)** To make models faster
- **B)** To ground answers in retrieved knowledge within the context window (models can't know your data)
- **C)** To replace prompt engineering
- **D)** To reduce tokens

**Correct Answer: B** — The context window limits what the model can "see"; RAG retrieves the relevant slice of your knowledge base and grounds the answer in it — reducing hallucination and enabling updates by re-indexing.

---

### Q5. What is the key idea behind embeddings?
- **A)** Text becomes compressed bytes
- **B)** Semantic similarity maps to vector distance (cosine similarity)
- **C)** Text becomes tokens
- **D)** Words become one-hot vectors

**Correct Answer: B** — Embeddings place similar meanings near each other in vector space; cosine similarity on normalized vectors measures semantic closeness.

---

### Q6. Why chunk documents before embedding?
- **A)** To save disk space
- **B)** Small, self-contained, retrievable units that fit the context and stay semantically coherent
- **C)** To make the model smarter
- **D)** To avoid OCR

**Correct Answer: B** — Chunks that are too big are fuzzy and waste context; too small lose meaning. Chunking strategy is a *measured* retrieval-quality decision (recall@k).

---

### Q7. What does the grounded-answer prompt require?
- **A)** Answer from general knowledge
- **B)** Answer only from the provided context, cite sources, and refuse honestly when absent
- **C)** Always answer, even if unsure
- **D)** Never say "I don't know"

**Correct Answer: B** — "Answer ONLY from context + cite [n] + 'I don't have that information'" is the anti-hallucination contract. Honest refusal is a feature, not a failure.

---

### Q8. What is recall@k in retrieval evaluation?
- **A)** How many of the top-k were relevant (precision)
- **B)** Whether the right chunk made the top-k results
- **C)** The model's accuracy
- **D)** The server's response time

**Correct Answer: B** — recall@k asks "did we find the right context?" — the primary retrieval metric. Precision@k asks how many of the top-k were relevant.

---

### Q9. What is hybrid search?
- **A)** Running two models and averaging
- **B)** Running BM25 (lexical) + vector search (semantic) and fusing with RRF
- **C)** Searching two databases
- **D)** Using both CPU and GPU

**Correct Answer: B** — Vector search finds meaning; BM25 finds exact tokens (error codes, model numbers). Fusing both with Reciprocal Rank Fusion covers both query types.

---

### Q10. What is reranking?
- **A)** Training the model again
- **B)** A precision stage: score recall-stage candidates (top-50) with a stronger pairwise model, return the best top-5
- **C)** Re-embedding the corpus
- **D)** Sorting by token count

**Correct Answer: B** — Two-stage retrieval: cheap hybrid recall (top-50), then a cross-encoder or LLM reorders by true query-document relevance (top-5). Recall first, precision second.

---

### Q11. What is the "iron rule" of tool calling?
- **A)** Always trust the model's arguments
- **B)** Validate and schema-check the model's arguments BEFORE any tool executes
- **C)** Execute tools in parallel
- **D)** Never use tools

**Correct Answer: B** — The model's args are generated text. Parse + pydantic-validate before any side effect; invalid args are fed back as errors (self-correction), never executed.

---

### Q12. What is the ReAct pattern?
- **A)** React quickly to user input
- **B)** Reason → Act (call tool) → Observe (result) loop
- **C)** A React.js component
- **D)** A single LLM call

**Correct Answer: B** — ReAct loops reason → tool call → observation until the task is done. The trace is both the reasoning evidence and the audit trail.

---

### Q13. What is the most important guardrail for agent actions?
- **A)** Making all tools read-only
- **B)** Read tools auto-run; write tools require human approval; unknown tools deny
- **C)** Letting the model decide
- **D)** No guardrails for fast agents

**Correct Answer: B** — The read/write split + human approval on writes + unknown-default-deny is the safety boundary that lets agents exist with write capability.

---

### Q14. What does the L3 structured-output ladder progress through?
- **A)** Prompt → JSON mode → constrained decoding (schema-guaranteed)
- **B)** Prompt → more tokens → better model
- **C)** JSON → YAML → XML
- **D)** Regex → JSON → CSV

**Correct Answer: A** — Prompting is the soft baseline; JSON mode guarantees valid JSON; constrained decoding (schema) makes schema violations *impossible* during generation. Validate with pydantic at the boundary regardless.

---

### Q15. What is the #1 prompt-evaluation mistake?
- **A)** Not using enough examples
- **B)** Shipping prompt changes without measuring on a frozen eval set
- **C)** Using delimiters
- **D)** Writing system prompts

**Correct Answer: B** — "Feels better" is not a measurement. Every prompt change is a candidate on the frozen eval set; regressions block merges in CI.

---

### Q16. What is LLM-as-judge's key risk?
- **A)** It's too fast
- **B)** Judge drift and bias — calibrate against human scores on a sample
- **C)** It costs nothing
- **D)** It's always correct

**Correct Answer: B** — Judges drift, have biases, and format-error. Calibrate judge-human agreement periodically; use temperature 0 and structured output.

---

### Q17. What is semantic caching?
- **A)** Caching by exact prompt string
- **B)** Returning a cached answer when a *similar* (embedded-near) query was answered before
- **C)** Caching on the GPU
- **D)** Caching model weights

**Correct Answer: B** — Embed the query and compare cosine similarity to cached queries above a threshold — paraphrases skip generation. The threshold is tuned with eval: a wrong cached answer is an incident.

---

### Q18. What does the trace_id enable in LLM observability?
- **A)** Faster generation
- **B)** End-to-end correlation: replay a user's full call chain for debugging and audit
- **C)** Better prompts
- **D)** Model caching

**Correct Answer: B** — The trace_id flows through HTTP → agent → tools → logs, so a bad answer is reconstructable: prompts, chunks, tokens, latency, cost, and decisions.

---

### Q19. When is fine-tuning the wrong tool?
- **A)** For format enforcement
- **B)** For adding knowledge the base model lacks (use RAG instead)
- **C)** For domain tone
- **D)** For tool-calling reliability

**Correct Answer: B** — Fine-tuning changes behavior (format/tone/task adherence), not knowledge. New facts = RAG. The decision ladder: prompt → RAG → few-shot → fine-tune.

---

### Q20. What is LoRA's key property?
- **A)** It trains the full model
- **B)** It trains a tiny low-rank adapter (1-10% of params) — efficient and artifact-grade
- **C)** It requires no data
- **D)** It replaces the base model

**Correct Answer: B** — LoRA freezes base weights and trains small adapters: minutes-hours on one GPU, tiny artifacts, hot-swappable adapters per tenant, near full-fine-tune quality.

---

## Answer Key

| Q | Answer | Q | Answer |
|---|--------|---|--------|
| 1 | B | 11 | B |
| 2 | B | 12 | B |
| 3 | B | 13 | B |
| 4 | B | 14 | A |
| 5 | B | 15 | B |
| 6 | B | 16 | B |
| 7 | B | 17 | B |
| 8 | B | 18 | B |
| 9 | B | 19 | B |
| 10 | B | 20 | B |

---

## Score Tracking

| Difficulty | Questions | Correct | Score |
|------------|-----------|---------|-------|
| Easy (1-7) | 7 | ___/7 | ___% |
| Medium (8-14) | 7 | ___/7 | ___% |
| Hard (15-20) | 6 | ___/6 | ___% |
| **Total** | **20** | **___/20** | **___%** |

**Target:** 80%+ to demonstrate strong GenAI engineering knowledge
