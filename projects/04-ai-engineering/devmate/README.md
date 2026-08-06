# DevMate

AI assistant for code repositories. Ingests a GitHub repo or docs folder, answers
questions about it, explains code, and proposes changes.

Built as the vehicle for the [10-week AI Engineer track](../../../docs/roadmap/active-track-10-week.md):
RAG + agents + MCP + observability in one continuously-growing system.

## Status

| Milestone | Status |
| --- | --- |
| A1 — CI green + `devmate stats` CLI | In progress |
| A2 — LLM layer traced and costed | Planned |
| A3 — RAG with measured eval | Planned |
| A4 — Deployed at a public URL | Planned |
| A5 — Agent with 4 tools + MCP | Planned |
| A6 — Production hardening | Planned |
| A7 — Portfolio | Planned |

## Quick start (local)

```powershell
# 1. Create the environment (Python >= 3.11)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"

# 2. Repository statistics (Week 0 deliverable)
devmate stats .

# 3. Infra (Postgres / Redis / Qdrant / Langfuse)
docker compose -f ../../../infra/docker/docker-compose.yml up -d

# 4. Quality gates — same as CI
make ci
```

## Layout

```text
src/devmate/
  cli/        typer CLI: stats, ask, ingest, serve, cost
  ingest/     repository reader + chunkers
  index/      embeddings + vector store (Qdrant)
  retrieve/   hybrid retrieval + RAG pipeline
  llm/        LLM client, schemas, prompts
  obs/        Langfuse tracing + cost tracking
  agent/      tools + ReAct loop
  mcp/        MCP server
  api/        FastAPI application
  db/         SQLAlchemy models
  cache/      semantic cache (Redis)
  guards/     input/output guardrails
```

## Documentation

- [Full completion execution plan](../../../docs/learning/design/project-plan-devmate-completion.md)
- [Failure modes](docs/failure-modes.md)
- [State audit](docs/state-audit.md)
