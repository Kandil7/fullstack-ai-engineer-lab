# Learning Path: FastAPI AI Services

**Last updated:** 2026-06-26

**Goal:** build the Python AI layer (RAG, embeddings, agents) that the Go core calls over HTTP.

**Primary project:** `projects/04-ai-engineering/rag-system`

## Milestones

1. **FastAPI fundamentals** — routers, dependency injection, middleware, Pydantic validation.
2. **LLM integration** — chat completions endpoint, structured outputs, streaming.
3. **Embeddings + Qdrant** — embed text, upsert vectors with metadata, similarity search.
4. **RAG endpoint** — `/ai/rag/query`: chunk → embed → retrieve → LLM → cited answer.
5. **Agents + tool calling** — agent loop, tool registry, memory.
6. **Eval + cost** — token accounting, latency budget, eval harness (see `evaluations/rag`).

## The 20% That Unlocks 80%

- Pydantic models as the request/response contract
- Async endpoints + background tasks
- Embedding dimensions and distance metrics in Qdrant
- Prompt structure: system + context + question; faithfulness vs hallucination

## API Surface (target)

`/ai/chat` · `/ai/embeddings` · `/ai/rag/query` · `/ai/agents/run`

## Self-Check

Can you explain: RAG pipeline stages, embedding vs token, tool calling, agent vs chatbot,
recall@k vs faithfulness?

## ملخص عربي (Arabic Summary)

مسار FastAPI لطبقة الذكاء: RAG وembeddings وagents كخدمة Python يستدعيها Go core عبر HTTP،
مع تقييم الجودة والتكلفة.
