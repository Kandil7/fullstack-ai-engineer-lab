# FastAPI — 28: Pagination and Filtering

Companion exercise: `28-pagination-and-filtering.py`

---

## Topic Overview

Every list endpoint eventually outgrows returning everything. Pagination and
filtering are how list endpoints stay fast, bounded, and predictable as the
underlying table grows. This topic covers the two pagination families —
offset/limit and keyset (cursor) — and, critically, *why offset breaks at
scale*: an offset query must skip `offset` rows before returning `limit` of
them, an O(offset) scan that grows linearly with table depth. Keyset
pagination turns the query into an index range scan, O(limit), independent of
position — and is robust to inserts and deletes between pages.

Filtering is the sibling concern: explicit query parameters are readable,
documentable, and safe; filter DSLs trade that for generality. The choice is
an engineering decision, not a fashion decision.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Implement offset/limit pagination and state its scaling behavior.
2. Explain why offset pagination degrades on deep pages.
3. Implement keyset/cursor pagination on a stable sort key.
4. Explain why keyset pagination is robust to concurrent writes.
5. Design explicit, safe filter query parameters.
6. Choose between explicit params and a filter DSL.
7. Emit RFC 8288 `Link` headers for standard pagination.
8. Decide when to include a total-count and when to skip it.

## Prerequisites

| Need | Where |
|---|---|
| Query parameters | `04-query-parameters.py` |
| Response models | `06-response-model.py` |
| Database/SQL | `04-databases/sql-fundamentals/04-select-basics.py` |
| Indexes | `04-databases/sql-fundamentals/10-indexes-and-plans.py` |

## 1. Offset Pagination — The Classic

```python
@app.get("/api/offset")
def offset_page(limit: int = Query(20, ge=1, le=100),
                offset: int = Query(0, ge=0)):
    items = DB[offset:offset + limit]
    return {"items": items, "total": len(DB)}
```

Output:
```
# GET /api/offset?limit=20&offset=40 -> rows 40..59
```

Simple, easy to reason about, and the first thing everyone builds. Its cost is
hidden: the database still scans `offset + limit` rows and discards `offset`
of them.

## 2. Why Offset Breaks at Scale

An offset query is `LIMIT :n OFFSET :m`. The planner scans `m + n` rows, skips
`m`, returns `n`. At offset 100,000 on a million-row table, that is 100,000
rows scanned to return 20. The scan grows linearly with table depth — the
deeper you page, the slower every page gets, even though each page is the same
size.

```text
page 1:  scan 20   rows, return 20   (fast)
page 5000: scan 100,000 rows, return 20   (slow)
```

It also breaks under writes: inserting a row shifts every offset after it, so
page N+1 can skip or repeat rows. This is "the offset problem."

## 3. Keyset (Cursor) Pagination — The Fix

```python
@app.get("/api/keyset")
def keyset_page(limit: int = Query(20, ge=1, le=100),
                cursor: str | None = None):
    start = int(cursor) if cursor else -1
    items = [r for r in DB if r["id"] > start][:limit]
    last_id = items[-1]["id"] if items else start
    return {"items": items,
            "next_cursor": str(last_id) if len(items) == limit else None,
            "has_more": len(items) == limit}
```

Output:
```
# page 1 -> next_cursor: "19"; page 2 starts at id > 19
```

The query becomes `WHERE id > :last ORDER BY id LIMIT :n` — an index range
scan that touches exactly `n` rows no matter how deep you are. Requirements:

- A **stable, unique, ordered** key (a primary key or created_at+id).
- The cursor is **opaque** — clients must never construct it.
- New inserts land after the cursor, so pages never shift under you.

## 4. Sorting with Keyset — Composite Cursors

When the sort is not by id, the cursor must encode the full sort key. Sorting
by `score DESC, id DESC`, the cursor is `"score:42,id:100"` and the query is:

```sql
WHERE (score, id) < (:score, :id) ORDER BY score DESC, id DESC LIMIT :n
```

This is where the "unique key" requirement becomes load-bearing: without the
id tiebreaker, equal scores produce unstable page boundaries.

## 5. Filtering — Explicit Parameters vs DSL

```python
@app.get("/api/search")
def search(name_contains: str | None = None,
           min_score: int | None = None,
           sort: str = Query("id", pattern="^(id|score|name)$")):
    ...
```

Output:
```
# GET /api/search?name_contains=gpu&min_score=500&sort=score
```

- **Explicit params**: readable, type-checked, self-documenting, validation
  for free (the `pattern=` on sort whitelists values). Right choice when the
  filter space is closed — which is most of the time.
- **Filter DSL** (`filters=score:gt:500,status:in:active`): general but
  unreadable, hard to validate, and each operator is a code path. Right choice
  only when the filter space is genuinely open (reporting, analytics).

## 6. Link Headers — The Standard Contract

RFC 8288 `Link` headers let clients navigate without guessing URLs:

```python
def build_link_headers(base, page, limit):
    if page.next_cursor:
        return {"Link": f'<{base}?limit={limit}&cursor={page.next_cursor}>; rel="next"'}
    return {}
```

Output:
```
# Link: </api/keyset?limit=20&cursor=19>; rel="next"
```

`rel="next"`, `rel="prev"`, `rel="first"`, `rel="last"` (last is only
meaningful for offset — keyset has no last page by construction).

## 7. The Total-Count Trap

`{"total": len(DB)}` forces a `COUNT(*)` on every request — an O(n) table scan
on large tables, often the single most expensive part of a list endpoint. Trade:

- **Offset pagination**: total is natural and cheap to compute *sometimes*.
- **Keyset pagination**: `has_more` is O(limit); total is always extra.
- Rule: return total on page 1 (or when explicitly requested); skip it on deep
  pages.

## 8. Common Mistakes to Avoid

### Mistake 1: Deep offset on large tables
```python
# WRONG — page 100k scans 100k rows
items = DB[offset:offset + limit]
# CORRECT — keyset/cursor for anything beyond a few thousand rows
```

### Mistake 2: Cursor = raw index into a mutable table
```python
# WRONG — integer position shifts when rows are inserted/deleted
# CORRECT — cursor = the last seen stable key (id / created_at+id)
```

### Mistake 3: Letting clients build cursors
```python
# WRONG — cursor is "id=5", clients reverse-engineer and skip
# CORRECT — opaque token; encode+sign if abuse is a concern
```

### Mistake 4: Unvalidated sort/filter strings
```python
# WRONG — sort=db;drop returns an injection or 500
# CORRECT — whitelist with pattern= or an enum
```

### Mistake 5: COUNT(*) on every page
```python
# WRONG — total computed for every deep page
# CORRECT — has_more on deep pages; total only when asked
```

## 9. Best Practices

1. Default to keyset pagination for anything that may exceed ~10k rows.
2. Keep cursors opaque; never document their internal format.
3. Use a stable composite key for non-id sorts.
4. Whitelist sort and filter values at the boundary.
5. Emit `Link` headers for machine-readable navigation.
6. Return `has_more` (O(limit)) over `total` (O(n)) on deep pages.
7. Bound `limit` (e.g. 1..100) at the schema level.
8. Prefer explicit query params; reserve DSLs for open filter spaces.
9. Test pagination under concurrent inserts.
10. Document the cursor's expiry policy if it can go stale.

## 10. Complexity and Cost

| Approach | Query cost | Write robustness | Total-count |
|---|---|---|---|
| Offset | O(offset + limit) scan | Breaks (rows shift) | Natural |
| Keyset | O(limit) range scan | Stable | Extra O(n) if requested |
| Filtered search | O(scan or index) | n/a | Index-dependent |

The keyset win is asymptotic: page cost is constant in position. That is the
whole argument.

## 11. AI Engineering Relevance

**Where this shows up:** every list-shaped surface — document search results,
retrieval candidate lists, vector-store pagination, model version histories.

| Concept here | Used for |
|---|---|
| Keyset pagination | Paging through retrieval results without O(n) scans |
| Cursor stability | Paginating a vector store while new vectors are indexed |
| Filtering | Metadata-filtered retrieval (tenant, date range, type) |
| Sort whitelist | Allowing sort-by-score only in search APIs |
| Link headers | Standard pagination contracts for ML APIs |

**Scale note:** at 100M+ rows, offset pagination is not slow — it is
unusable. Keyset pagination is the difference between a search API that
degrades gracefully and one that falls over at page 50.

## 12. Summary

| Concept | Description |
|---|---|
| Offset pagination | LIMIT + OFFSET; simple, O(offset) scan |
| Keyset pagination | WHERE key > :last; O(limit), write-robust |
| Cursor | Opaque token encoding the last seen stable key |
| Filtering | Explicit params or DSL by filter-space shape |
| Link headers | RFC 8288 machine-readable navigation |
| Total-count trap | COUNT(*) per page is O(n); use has_more |

## Quick Reference

| Task | Idiom |
|---|---|
| Offset (small tables) | `offset: int = Query(0, ge=0)`, slice |
| Keyset | `WHERE id > :cursor ORDER BY id LIMIT :n` |
| Composite sort | cursor encodes `(score, id)`; row-value comparison |
| Bound limits | `limit: int = Query(20, ge=1, le=100)` |
| Whitelist sort | `sort: str = Query("id", pattern="^(id|score)$")` |
| Navigation | `Link: <...>; rel="next"` |

## Next Steps

Next: **[29 — Error Handling (RFC 9457)](29-error-handling-rfc9457-lecture.md)** — consistent, client-actionable errors.

Continues in: **[04-databases — sql-fundamentals 10 Indexes](../../04-databases/sql-fundamentals/lectures/10-indexes-and-plans-lecture.md)** — the index behind keyset pagination.

Official docs: <https://www.rfc-editor.org/rfc/rfc8288.html> · <https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design#pagination>
