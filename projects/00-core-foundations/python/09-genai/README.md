# Phase 9 — GenAI: LLMs, RAG, Agents, and Production AI

The master-AI-engineering phase: LLM fundamentals, retrieval-augmented
generation, agents, evaluation, fine-tuning, local models, and the production
systems built on them.

## Exercises (25)

| # | File | Topics |
|---|------|--------|
| 1 | 01-llm-fundamentals.py | Next-token prediction, tokens, context window, sampling |
| 2 | 02-api-clients.py | OpenAI/Anthropic, abstraction, retries, streaming, local |
| 3 | 03-structured-output.py | JSON mode, constrained decoding, pydantic, repair |
| 4 | 04-prompt-engineering.py | System prompts, few-shot, CoT, delimiters, prompt-as-code |
| 5 | 05-prompt-evaluation.py | Eval sets, scoring, A/B, CI gates |
| 6 | 06-embeddings.py | Cosine similarity, API/local, search, dedup |
| 7 | 07-chunking-strategies.py | Fixed/sentence/paragraph/recursive, metadata, eval |
| 8 | 08-document-processing.py | PDFs, tables, OCR, cleaning, structure, gates |
| 9 | 09-rag-baseline.py | Retrieve → generate, grounded prompts, citations |
| 10 | 10-retrieval-quality.py | recall@k, precision@k, MRR, attribution, CI gates |
| 11 | 11-advanced-retrieval.py | Hybrid BM25+vector, RRF, rewriting, decomposition |
| 12 | 12-reranking.py | Cross-encoders, two-stage retrieval, latency budgets |
| 13 | 13-tool-calling.py | Tool schemas, validation, execution loop, allowlists |
| 14 | 14-agent-patterns.py | ReAct, plan-execute, reflection, state machines, budgets |
| 15 | 15-multi-agent.py | Orchestrator/workers, contracts, parallelism, degradation |
| 16 | 16-memory-and-context.py | Truncation, summarization, facts, episodic memory |
| 17 | 17-llm-observability.py | Traces, correlation IDs, redaction, drift metrics |
| 18 | 18-caching-and-cost.py | Exact/semantic caches, model routing, token discipline |
| 19 | 19-guardrails-and-safety.py | Input/output gates, injection defense, action approval |
| 20 | 20-evaluation-frameworks.py | Datasets, evaluators, LLM-judge, gates, leaderboards |
| 21 | 21-fine-tuning.py | Decision ladder, LoRA/PEFT, datasets, adapter lifecycle |
| 22 | 22-local-models.py | vLLM, quantization, fleet math, hosted-vs-local |
| 23 | 23-case-study-rag-service.py | Production RAG service end-to-end |
| 24 | 24-case-study-agent.py | Production tool-using agent with approvals |
| 25 | 25-case-study-extraction.py | Production document extraction pipeline |

## Lectures

Every topic has a **full-detail lecture** (`lectures/NN-topic-lecture.md`) and
a **glossary** (`lectures/NN-topic-glossary.md`). Each lecture explains the
complete topic, every use case, and real-world scenarios for AI engineers in
production.

## Prerequisites

- Phase 8 MLOps (`08-mlops/`)
- Python + NumPy + pandas + scikit-learn
- Optional: `openai`, `anthropic`, `sentence-transformers`, `pydantic`,
  `fastapi` (see `requirements.txt`)

## Running

```bash
python 09-genai/01-llm-fundamentals.py      # run one exercise
python run_smoke_tests.py --phase 9         # run the whole phase
pytest tests/unit/test_genai.py -q          # unit tests
```

## Production Path

The three capstones (`23-case-study-rag-service.py`, `24-case-study-agent.py`,
`25-case-study-extraction.py`) are the production templates: a RAG service, a
tool-using agent, and a document-extraction pipeline — each built from the
phase's lectures on the Phase 8 assembly line.
