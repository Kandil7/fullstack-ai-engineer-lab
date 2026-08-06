# Uvicorn & Gunicorn — Glossary 49

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| ASGI | Protocol | The async server spec FastAPI speaks |
| Bind | Server | The address/port the server listens on |
| CPU-bound | Workload | Work that uses a core; ~1 worker per core |
| Graceful timeout | Shutdown | The drain window after SIGTERM |
| Gunicorn | Manager | Forks and supervises worker processes |
| IO-bound | Workload | Work waiting on DB/API; workers oversubscribe |
| Keep-alive | Server | How long idle connections stay open |
| Reload | Dev | File-watch restarts — dev only |
| UvicornWorker | Integration | The worker class making gunicorn run uvicorn |
| Uvicorn | Server | The ASGI protocol server |
| Worker | Process | One process running the app |
| Memory-bound | Constraint | Workers capped by per-worker model RAM |

## Detailed Definitions

### ASGI
**Definition**: Asynchronous Server Gateway Interface — the protocol
between the server (uvicorn) and the app (FastAPI), replacing WSGI's
sync-only model.
**Related**: Uvicorn

### Bind
**Definition**: The listen address/port — `--bind 0.0.0.0:8000`; in a
container, `0.0.0.0` so the proxy can reach it.
**Related**: Uvicorn

### CPU-bound
**Definition**: Work using a core continuously (inference, heavy parsing)
— more workers than cores just context-switches.
**Related**: Worker

### Graceful timeout
**Definition**: The window gunicorn gives workers to finish in-flight
requests after SIGTERM — must cover the longest request.
**Related**: Keep-alive

### Gunicorn
**Definition**: The process manager — forks N workers, supervises and
restarts them, and owns the lifecycle.
**Related**: Uvicorn

### IO-bound
**Definition**: Work mostly waiting on external systems (DB, cache, APIs)
— the CPU is free while awaiting, so workers can exceed cores.
**Related**: CPU-bound

### Keep-alive
**Definition**: The seconds an idle connection stays open before the
server closes it — short values free sockets, too short hurts reuse.
**Related**: Graceful timeout

### Reload
**Definition**: `--reload` watches files and restarts on change — the dev
experience; in production, restarts belong to the orchestrator.
**Related**: Worker

### UvicornWorker
**Definition**: The gunicorn worker class bridging the manager to the
ASGI server — the production pair's joint.
**Related**: Gunicorn

### Uvicorn
**Definition**: The ASGI server accepting connections and running your
app — one process without a manager.
**Related**: Gunicorn

### Worker
**Definition**: One process running the app — the concurrency unit; the
count is the load-bearing deployment decision.
**Related**: Memory-bound

### Memory-bound
**Definition**: The constraint where per-worker model RAM (GB) caps
workers before cores do — the model-serving trap.
**Related**: Worker

## Key Concepts Summary

### The roles
- uvicorn: ASGI protocol server.
- gunicorn: process manager (forks, supervises).
- UvicornWorker: the joint — gunicorn managing uvicorn processes.

### The worker math
- CPU-bound: ~cores.
- IO-bound: 2–4× cores.
- Memory-bound: floor(mem / per-worker) — check before cores.

### The production rules
- `--reload` only in dev.
- Graceful timeout ≥ longest in-flight request.
- Orchestrator owns production restarts.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. The ASGI protocol server — ___
2. Forks and supervises workers — ___
3. One process running the app — ___
4. ~1 worker per core — ___
5. Workers oversubscribe — ___
6. Capped by per-worker model RAM — ___
7. Dev-only file-watch restarts — ___
8. The drain window after SIGTERM — ___

**Answers:** 1-uvicorn, 2-gunicorn, 3-worker, 4-CPU-bound, 5-IO-bound,
6-memory-bound, 7-reload, 8-graceful timeout
