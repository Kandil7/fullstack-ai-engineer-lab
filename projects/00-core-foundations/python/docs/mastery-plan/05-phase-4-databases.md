# Phase 4 — Databases (`04-databases/`)

> **Current:** 23 exercises (MySQL 12, MongoDB 11), 23 lectures. **20/23 pass — 3 fail.**
> **Target:** ~56 exercises across 5 backends including **Postgres, Redis, and a vector DB**.
>
> This is the **weakest section relative to its importance**. Data access is where
> backend engineers spend most of their time and where most production incidents
> originate, and the current content teaches neither real drivers nor performance.

---

## 1. Current State and Its Central Problem

| Backend | Files | Lectures | Smoke result |
|---|---|---|---|
| MySQL | 12 | 12 | 11/12 — **1 fail** (R5) |
| MongoDB | 11 | 11 | 9/11 — **2 fail** (R6) |

**The problem: neither backend is real.**

- MySQL exercises use `sqlite3` as a stand-in (documented in `README.md`)
- MongoDB exercises use **Python dicts** as a document simulator

This has three consequences:

1. **It teaches a dialect that does not exist.** `08-delete.py` fails precisely
   because it writes MySQL `DELETE ... LIMIT` against sqlite3 (R5). The
   simulation leaks.
2. **The simulator hides bugs.** Both MongoDB failures (R6) are bugs *in the
   simulator*, not in MongoDB concepts. Learners debug the teaching apparatus
   instead of learning aggregation.
3. **Nothing performance-related can be taught.** No `EXPLAIN` plans, no index
   effects, no connection pooling, no transaction isolation, no lock contention —
   the entire senior-level surface of database work is unreachable through a dict.

`infra/docker/docker-compose.yml` **already provides Postgres, Redis, and Qdrant.**
The infrastructure to fix this exists and is unused.

### 1.1 Coverage gaps (measured, repo-wide `.py`)

| Concept | Files | Note |
|---|---|---|
| `alembic` (migrations) | **0** | Schema evolution never taught |
| `redis` | 1 | Caching never taught |
| `qdrant` | **0** | Vector search never taught, despite `infra/docker/qdrant/` existing |
| `sqlalchemy` | 4 | All in FastAPI, not Phase 4 |
| connection pooling | 4 | Mentioned, never exercised |
| `N+1` | 2 | The most common ORM performance bug |
| transactions | 7 | Mentioned; isolation levels absent |
| `EXPLAIN` | 7 | Mentioned; never run against a real planner |

---

## 2. Decision: Move to Real Databases via Docker

**Recommendation:** keep sqlite3 for the zero-setup on-ramp, then teach real
Postgres, Redis, and Qdrant against `infra/docker/`.

| Option | Verdict |
|---|---|
| Keep simulators only | ✗ Cannot teach indexes, plans, pooling, isolation — the senior content |
| Replace with real DBs entirely | ✗ Loses the zero-install first lesson |
| **Tiered: sqlite3 → Postgres → Redis → Qdrant** | ✓ On-ramp preserved, ceiling removed |

Every real-DB exercise must **skip cleanly** when the service is absent, so CI and
a learner without Docker are never blocked:

```python
try:
    conn = psycopg.connect(DSN, connect_timeout=2)
except psycopg.OperationalError:
    print("[skip] Postgres not running — docker compose up -d postgres")
    sys.exit(0)          # skip, not fail
```

---

## 3. `04-databases/sql-fundamentals/` (new, 14 topics)

Pure SQL against sqlite3 — zero install, and SQL is the transferable skill.
Replaces the mislabeled "mysql" directory.

| # | Topic | Concepts |
|---|---|---|
| 01 | `01-relational-model.py` | Tables, rows, keys, relations, NULL semantics (**`NULL != NULL`**), set thinking |
| 02 | `02-ddl-schema.py` | `CREATE`/`ALTER`/`DROP`; types; `NOT NULL`; `DEFAULT`; `CHECK`; primary/foreign keys |
| 03 | `03-insert-update-delete.py` | DML; `RETURNING`; upsert (`ON CONFLICT`); bulk insert; **portable `DELETE` with `LIMIT`** (fixes R5's lesson) |
| 04 | `04-select-basics.py` | Projection, `WHERE`, `ORDER BY`, `LIMIT`/`OFFSET`, `DISTINCT`, aliases |
| 05 | `05-filtering-advanced.py` | `IN`/`BETWEEN`/`LIKE`; `IS NULL`; boolean logic; three-valued logic traps |
| 06 | `06-aggregation.py` | `COUNT`/`SUM`/`AVG`/`MIN`/`MAX`; `GROUP BY`; `HAVING` vs `WHERE`; `COUNT(*)` vs `COUNT(col)` |
| 07 | `07-joins.py` | INNER/LEFT/RIGHT/FULL/CROSS; self-join; multi-join; **join cardinality and row explosion** |
| 08 | `08-subqueries-ctes.py` | Scalar/row/table subqueries; correlated subqueries; `WITH` CTEs; recursive CTEs; readability |
| 09 | `09-window-functions.py` | `OVER`; `PARTITION BY`; `ROW_NUMBER`/`RANK`/`DENSE_RANK`; `LAG`/`LEAD`; running totals; frames |
| 10 | `10-indexes-and-plans.py` ⭐ | B-tree mechanics; `EXPLAIN QUERY PLAN`; covering and composite indexes; **column order matters**; when an index is unused; write-cost tradeoff |
| 11 | `11-transactions.py` | ACID; `BEGIN`/`COMMIT`/`ROLLBACK`; savepoints; isolation levels; anomalies (dirty/phantom/non-repeatable); deadlock |
| 12 | `12-normalization.py` | 1NF–3NF; when to denormalize; star schema; surrogate vs natural keys |
| 13 | `13-sql-injection.py` | Parameterized queries; **why string interpolation is never acceptable**; identifier vs value binding; least privilege; ORM does not automatically save you |
| 14 | `14-query-optimization.py` | Reading plans; sargable predicates; avoiding `SELECT *`; pagination (keyset vs offset); `N+1`; batching |

`10` and `14` are the topics that make someone employable at a senior level, and
neither is reachable through the current dict/sqlite mix.

---

## 4. `04-databases/postgres/` (new, 12 topics)

Real Postgres via `infra/docker/`. **Includes pgvector** — the simplest production
vector store and the natural bridge to Phase 9.

| # | Topic | Concepts |
|---|---|---|
| 01 | `01-setup-and-psycopg.py` | Docker up; `psycopg3` connect; DSN; cursors; `with` blocks; server vs client cursors |
| 02 | `02-postgres-types.py` | `JSONB`, arrays, `UUID`, `ENUM`, `NUMERIC` vs `float`, `TIMESTAMPTZ`, ranges, `text` vs `varchar` |
| 03 | `03-jsonb-queries.py` | `->`/`->>`/`@>`; GIN indexes; JSONB vs normalized columns; when a document column is right |
| 04 | `04-indexes-postgres.py` | B-tree, GIN, GiST, BRIN, Hash; partial and expression indexes; `EXPLAIN (ANALYZE, BUFFERS)`; `pg_stat_user_indexes` |
| 05 | `05-transactions-mvcc.py` | MVCC; snapshot isolation; `SERIALIZABLE` and retry loops; `SELECT FOR UPDATE`; advisory locks; bloat and `VACUUM` |
| 06 | `06-connection-pooling.py` | Why pooling is mandatory; `psycopg_pool`; sizing; `PgBouncer`; pool exhaustion; **serverless pooling problem** |
| 07 | `07-full-text-search.py` | `tsvector`/`tsquery`; ranking; GIN; stemming; **when FTS beats vector search** — hybrid retrieval foundation |
| 08 | `08-pgvector.py` ⭐ | `vector` type; `<->`/`<=>`/`<#>` operators; HNSW and IVFFlat; index parameters; recall/latency tradeoff; **filtered vector search** |
| 09 | `09-hybrid-search.py` ⭐ | Combining FTS + pgvector; Reciprocal Rank Fusion; weighting; why hybrid beats either alone |
| 10 | `10-migrations-alembic.py` | Alembic; autogenerate and its limits; up/down; **zero-downtime patterns** (expand/contract); data migrations; migration review |
| 11 | `11-performance-tuning.py` | `pg_stat_statements`; slow query log; `work_mem`; table partitioning; `ANALYZE`; bloat; `pg_stat_activity` |
| 12 | `12-backup-and-reliability.py` | `pg_dump`/`pg_restore`; PITR; replication; read replicas; failover; RPO/RTO |

Topics `08` and `09` mean a learner can build production RAG on Postgres alone —
the cheapest and most operationally sane starting point.

---

## 5. `04-databases/sqlalchemy/` (new, 10 topics)

Currently `sqlalchemy` appears in only 4 files, all in FastAPI. It deserves
first-class treatment: it is the Python data-access layer.

| # | Topic | Concepts |
|---|---|---|
| 01 | `01-core-vs-orm.py` | Two layers; `text()`; when Core beats ORM; engine and dialects |
| 02 | `02-declarative-models.py` | `DeclarativeBase`; `Mapped`/`mapped_column` (2.0 typed style); constraints; `__table_args__` |
| 03 | `03-session-lifecycle.py` | Unit of work; identity map; `flush` vs `commit`; expiry; detached instances; **session-per-request** |
| 04 | `04-relationships.py` | `relationship()`; one-to-many, many-to-many, self-referential; `back_populates`; cascades |
| 05 | `05-querying-2.0.py` | `select()`; filters; joins; `aliased`; scalars; `execute` vs `scalars`; pagination |
| 06 | `06-eager-loading.py` ⭐ | **The N+1 problem, demonstrated with query counts**; `selectinload` vs `joinedload` vs `subqueryload`; `lazy=` strategies |
| 07 | `07-async-sqlalchemy.py` | `AsyncEngine`/`AsyncSession`; `async with`; greenlet bridge; async pooling; FastAPI integration |
| 08 | `08-advanced-patterns.py` | Hybrid properties; custom types; events; bulk operations; `returning()`; window functions via ORM |
| 09 | `09-testing-with-db.py` | Transactional rollback fixtures; per-test schema; factories; `testcontainers`; **sqlite-vs-Postgres divergence in tests** |
| 10 | `10-repository-pattern.py` | Repository abstraction; Unit of Work; keeping domain logic out of the ORM; testability tradeoffs |

`06` deserves emphasis: N+1 appears in 2 files today and is the single most common
performance defect in ORM-backed services.

---

## 6. `04-databases/redis/` (new, 8 topics)

`redis` appears in 1 file. `infra/docker/redis/` exists and is unused.

| # | Topic | Concepts |
|---|---|---|
| 01 | `01-introduction.py` | Data structures over key-value; `redis-py`; connection pooling; **when Redis is the wrong tool** |
| 02 | `02-data-structures.py` | Strings, hashes, lists, sets, sorted sets, bitmaps, HyperLogLog; complexity per op |
| 03 | `03-caching-patterns.py` ⭐ | Cache-aside, write-through, write-behind; TTL; **stampede and its mitigations** (jitter, locks, early recompute); invalidation |
| 04 | `04-rate-limiting.py` | Fixed window, sliding window, token bucket; `INCR`+`EXPIRE`; atomicity via Lua; distributed limits |
| 05 | `05-pubsub-and-streams.py` | Pub/Sub vs Streams; consumer groups; acknowledgment; at-least-once delivery; backpressure |
| 06 | `06-distributed-locks.py` | `SET NX PX`; lock expiry; fencing tokens; Redlock and its critics; **when you actually need one** |
| 07 | `07-session-and-queues.py` | Session storage; job queues; priority queues via sorted sets; `RQ`/Celery brokers |
| 08 | `08-persistence-and-ops.py` | RDB vs AOF; eviction policies (`allkeys-lru` etc.); memory reporting; `SCAN` not `KEYS`; cluster basics |

**AI relevance:** `03` is the highest-ROI cost optimization in LLM engineering —
caching embeddings and completions. `04` is how you stay inside provider rate
limits. `05` decouples ingestion from indexing.

---

## 7. `04-databases/mongodb/` (11 → 12, real driver)

Fix R6 (two simulator bugs), then replace the dict simulator with real MongoDB via
Docker, keeping the same topic progression so existing lectures stay valid.

| # | Topic | Change |
|---|---|---|
| 01–11 | existing progression | Port to `pymongo` against Docker; **fix R6 in `06-query` and `11-aggregation`** |
| 12 | `12-mongo-vs-sql.py` (new) | Document vs relational modeling; embedding vs referencing; when *not* to use Mongo; transactions in Mongo; index types; the honest tradeoff discussion |

Adding `12` is important: the module currently presents MongoDB without ever
saying when a relational store is the better choice, which is most of the time for
the systems this curriculum targets.

---

## 8. `04-databases/vector-stores/` (new, 8 topics)

The bridge to Phase 9. `qdrant` currently appears in **0** files despite
`infra/docker/qdrant/config/` existing.

| # | Topic | Concepts |
|---|---|---|
| 01 | `01-vector-search-fundamentals.py` | Embeddings as points; cosine/dot/L2; brute force O(n·d); why ANN; **recall vs latency is the central tradeoff** |
| 02 | `02-ann-algorithms.py` | HNSW (graph, `M`, `ef_construction`, `ef_search`); IVF; PQ and compression; LSH; index build cost; parameter effects measured |
| 03 | `03-qdrant.py` | Collections; payloads; upsert; filtered search; quantization; snapshots; the Docker service already in `infra/` |
| 04 | `04-chroma-and-faiss.py` | Chroma for local dev; FAISS as a library not a server; persistence; when each fits |
| 05 | `05-pgvector-revisited.py` | Cross-ref Postgres `08`; **why one database beats two** for most systems; operational simplicity |
| 06 | `06-metadata-filtering.py` | Pre- vs post-filtering; correctness *and* recall implications; payload indexing; tenant isolation |
| 07 | `07-hybrid-and-reranking.py` | Dense + sparse (BM25/SPLADE); RRF; cross-encoder reranking; latency budget; measured quality lift |
| 08 | `08-production-vector-search.py` | Incremental indexing; reindex without downtime; sharding; monitoring recall drift; cost per million vectors; **embedding version migration** |

---

## 9. Retrofit and Standards

`_verify()` for all files. Database-specific patterns:

```python
def _verify() -> None:
    # Always run against a throwaway schema, always clean up
    with connect() as conn:
        conn.execute("CREATE TEMP TABLE t (id INTEGER PRIMARY KEY, v TEXT)")
        conn.execute("INSERT INTO t (v) VALUES (?)", ("a",))         # parameterized
        assert conn.execute("SELECT COUNT(*) FROM t").fetchone()[0] == 1

        # Assert the *plan*, not just the result — this is the senior skill
        plan = conn.execute("EXPLAIN QUERY PLAN SELECT * FROM t WHERE id = 1").fetchall()
        assert any("SEARCH" in str(r) for r in plan), "PK lookup must use an index, not SCAN"
    print("[OK] all checks passed")
```

**Rules for this phase**
- Every real-DB file skips gracefully (exit 0) when the service is down
- Every file creates and drops its own schema — no shared mutable state
- **Every query is parameterized**, including in throwaway examples
- Index lectures assert on `EXPLAIN` output, not only on results
- Credentials from `os.environ` with dev defaults, never hardcoded
- Add `psycopg[binary]>=3.1`, `sqlalchemy>=2.0`, `alembic>=1.13`,
  `redis>=5.0`, `pymongo>=4.6`, `qdrant-client>=1.7`, `pgvector>=0.2` to requirements

---

## 10. Deliverables

| Item | Count |
|---|---|
| Fixes (R5, R6) | 3 |
| `sql-fundamentals/` | 14 |
| `postgres/` | 12 |
| `sqlalchemy/` | 10 |
| `redis/` | 8 |
| `mongodb/` port + new topic | 12 |
| `vector-stores/` | 8 |
| **Total exercises** | **64** (from 23) |
| Lecture+glossary pairs | 64 |
| Docker compose additions | Postgres, Redis, Qdrant wiring |
| Challenges | 64 dirs |
| Quizzes | ~10 |

---

## 11. Sequencing

| Step | Work | Depends on |
|---|---|---|
| 1 | Fix R5, R6 | Tier 0 |
| 2 | `sql-fundamentals/` (sqlite3, no Docker) | — |
| 3 | Docker wiring + skip-if-absent helper | — |
| 4 | `postgres/` `01`–`07`, `10`–`12` | step 3 |
| 5 | `sqlalchemy/` | step 4 |
| 6 | `redis/` | step 3 |
| 7 | `mongodb/` port | step 3 |
| 8 | `postgres/08`–`09` (pgvector, hybrid) | step 4 |
| 9 | `vector-stores/` | step 8 |
| 10 | Challenges + quizzes | after exercises |

Steps 2 and 6 need no Docker and can start immediately.

---

## 12. Exit Criteria

- [ ] Zero failures (from 3)
- [ ] Real Postgres, Redis, MongoDB, Qdrant exercised via `infra/docker/`
- [ ] Every real-DB file skips cleanly without Docker; CI green either way
- [ ] `EXPLAIN`-plan assertions present in index and optimization topics
- [ ] N+1 demonstrated with actual query counts, then fixed
- [ ] SQL injection shown as exploitable, then parameterized
- [ ] Migrations taught with a zero-downtime pattern
- [ ] pgvector + hybrid search working — a complete RAG store on Postgres alone
- [ ] Every file parameterizes queries; zero string-interpolated SQL in the tree

---

*Phase 4 of [00-MASTER-PLAN.md](00-MASTER-PLAN.md). Fixes: [10-remediation-backlog.md](10-remediation-backlog.md) R5/R6. Feeds Phase 9: [08-phase-7-9-ml-mlops-genai.md](08-phase-7-9-ml-mlops-genai.md).*
