# Offline Enablement: Ollama providers + 4 runtime bugs fixed

### Context

DevMate (projects/04-ai-engineering/devmate). Goal: run every Python entry point without internet or API keys. Session verified each claim with live runs: tests, ruff, mypy, and real Ollama/Qdrant roundtrips.

### Explanation

**What was blocking offline use (all verified by execution, not inference):**

1. `import devmate.index.embeddings` crashed without `OPENAI_API_KEY` — module-level `EmbeddingService()` hard-wired `OpenAIEmbeddingProvider`.
2. `async with tracer.trace(...)` raised `TypeError` at runtime — `trace` was a sync `@contextmanager`. 18 call sites affected, i.e. the whole ingest/ask/retrieval path had never actually run.
3. `RAGPipeline.__init__` had `self.embedding_service = embedding_service or embedding_service` (self-referential), so both services stayed `None`.
4. Streaming path: `await` on an async-generator function (TypeError), and the CLI iterated a coroutine.
5. Windows cp1252 console crashed on Rich's braille spinner (`\u2807`).
6. Chunk IDs were 16-hex md5 prefixes; Qdrant accepts only ints or full UUIDs, rejecting the whole upsert (`PointInsertOperations` 400).

**What was added:**

- `OllamaProvider` (`llm/client.py`): native `/api/chat`, NDJSON streaming, schema-structured output via `format`, token estimates via tiktoken. Registered unconditionally (no key needed); fallback chain starts at `DEFAULT_LLM_PROVIDER`.
- `OllamaEmbeddingProvider` (`index/embeddings.py`): `/api/embed`, batch size from settings, dimensions from a model map (`nomic-embed-text` -> 768).
- `get_embedding_provider()` factory with graceful fallback: `EMBEDDING_PROVIDER=openai` without a key warns and uses Ollama instead of raising at import.
- Per-provider model resolution in `LLMClient.complete` — `qwen2.5-coder:7b` for Ollama, `claude-3-5-sonnet` for Anthropic — so the cloud default model is never sent to a local server.
- `_DualContext` in `obs/tracing.py`: one fix that makes `trace()` work with both `with` and `async with`, repairing all 18 call sites at once.
- Offline-first config defaults: `default_llm_provider=ollama`, `embedding_dimensions=768`, `qdrant_vector_size=768` (vector size MUST match the embedding model), plus `.env` / `.env.example`.
- Makefile switched from `poetry run` (no lockfile exists) to the venv interpreter with `-m` module invocation.
- `qdrant-client` pinned `>=1.8.0,<1.9`: client 1.19 removed `.search()` (which `vector_store.py` uses) and mismatches the compose server `1.8.0`.

**Verification evidence (this session):**
- `ruff check` pass, `ruff format --check` 25 files clean, `mypy src/` 0 issues / 21 files, `pytest` 19 passed.
- Live Ollama: completion returned `OFFLINE-OK` (37 prompt / 5 completion tokens), stream returned `1, 2, 3`.
- Live embeddings: 768-dim vectors from `nomic-embed-text`.
- `devmate stats .` renders (encoding fixed); `devmate ingest .` wrote 500 vectors; `devmate ask "What is DevMate..."` answered with sources; `ask --stream` streamed; API `/health` returned `status: healthy`.
- Docker: started Docker Desktop, `devmate-qdrant` up on 6333 (image `qdrant/qdrant:v1.8.0`).

**Known limitations left open:**
- `make` is not installed on this machine; the `make ci` constituent commands were run directly instead. `docs-check`/`fresh-check` (POSIX shell loops) were not run.
- `devmate cost` shows 0 across processes — cost records are in-memory per process (pre-existing design).
- Qdrant client/server version warning is gone after the pin; other services (postgres/redis/langfuse) were not started — not needed for CLI/ask/serve.

### Alternatives

- **Cloud-stub approach (rejected):** fake LLM/embedding responses so the code runs but produces nothing useful offline. Rejected because Ollama with real local models was already installed and gives genuine answers.
- **sentence-transformers local embeddings (rejected):** `LocalEmbeddingProvider` already existed but needs a ~2GB model download and runs on CPU slowly; Ollama `nomic-embed-text` was already pulled (274MB) and serves over HTTP with batching.
- **Upgrade Qdrant server to 1.19 (rejected):** would need an image change plus rewriting `search()` to `query_points()`; downgrading the client to match the pinned server 1.8.0 required only a dependency change.
- **Change chunk IDs at the test contract (chosen over mapping in vector_store):** fixing `_generate_id` to full 32-hex md5 keeps one ID format everywhere instead of introducing a lossy Qdrant-side ID mapping; the single test assertion was updated with it.

### Rationale (Why this?)

The goal was genuine offline capability, not simulated success. Every fix targets a failure that was reproduced first. Offline-first defaults were chosen over `.env`-only configuration because pydantic resolves `.env` relative to the working directory — files run from elsewhere would otherwise still crash. The 768-dim default trio (embedding provider, dimensions, qdrant vector size) must change together or Qdrant rejects vectors at upsert.

### Exercises

1. Re-run the full chain after a cold start: stop Docker, start it, `devmate ingest . && devmate ask "How does fallback work?"`.
2. Unplug the network (or `wsl --shutdown` + disable adapters) and repeat the chain to prove no hidden egress.
3. Run `uv sync` in `projects/04-ai-engineering/devmate/` and confirm the `qdrant-client<1.9` pin holds.
4. Add a pytest that constructs `LLMClient()` with no keys and asserts `ollama` is registered — guards the offline contract.
5. Start the remaining compose services and verify Langfuse receives spans once `LANGFUSE_*` keys are set.

### Next Steps

Deferred, tracked elsewhere: A1 CI workflow (`.github/workflows/` still missing), `make` installation or a PowerShell-native `ci` target, legacy 34-file Python baseline (`admin/mastery-plan/10-remediation-backlog.md`), and cross-process cost persistence.

---
