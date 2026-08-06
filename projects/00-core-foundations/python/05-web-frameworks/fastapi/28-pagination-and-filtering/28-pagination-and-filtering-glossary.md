# Pagination and Filtering — Glossary 28

Companion lecture: `28-pagination-and-filtering-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Cursor | Pagination | Opaque token encoding the last seen stable key |
| Filter DSL | Filtering | A mini-language encoding filters in query strings |
| has_more | Pagination | A cheap O(limit) signal that another page exists |
| Keyset pagination | Pagination | WHERE key > :last — index range scan, O(limit) |
| Link headers | Pagination | RFC 8288 rel=next/prev/first navigation |
| Offset pagination | Pagination | LIMIT + OFFSET; O(offset) scan, breaks under writes |
| Opaque token | Pagination | A client-unknowable value; never constructed by callers |
| Stable key | Pagination | Unique, ordered, immutable column driving cursors |
| Total-count trap | Pagination | The O(n) COUNT(*) cost hidden in list endpoints |
| Range scan | Database | Index traversal touching only the requested rows |
| Composite cursor | Pagination | Cursor encoding multiple sort key columns |
| Query parameter | Filtering | Explicit, typed, documentable filter input |
| Whitelist | Filtering | Allowing only known values for sort/filter fields |
| OFFSET | Pagination | The SQL clause skipping m rows before returning |
| Row-value comparison | Database | Comparing tuples (score, id) for composite cursors |
| rel="next" | Pagination | Link relation pointing to the following page |

## Detailed Definitions

### Cursor
**Definition**: An opaque token a client sends back to fetch the next page; it
encodes the last seen stable key but its internal format is never part of the
contract.
**Example**:
```python
# server encodes; client echoes; server never trusts construction
next_cursor = str(last_id)
```
**Related**: Opaque token, Keyset pagination

### Filter DSL
**Definition**: A query-string mini-language such as
`filters=score:gt:500,status:in:active`. General but unreadable and harder to
validate; choose only when the filter space is open.
**Related**: Query parameter

### has_more
**Definition**: A boolean response field indicating another page exists;
computed in O(limit) by checking whether a full page was returned.
**Related**: Keyset pagination, Total-count trap

### Keyset pagination
**Definition**: Paginating with `WHERE key > :last ORDER BY key LIMIT :n` — an
index range scan whose cost is independent of position and robust to
concurrent writes.
**Example**:
```python
start = int(cursor) if cursor else -1
items = [r for r in DB if r["id"] > start][:limit]
```
**Complexity**: O(limit) per page, regardless of depth.
**Related**: Offset pagination, Stable key

### Link headers
**Definition**: RFC 8288 response headers giving machine-readable navigation
(`<url>; rel="next"`), so clients never guess URLs.
**Related**: rel="next"

### Offset pagination
**Definition**: `LIMIT :n OFFSET :m` — returns rows m..m+n after scanning
m+n rows. Simple; cost grows linearly with position; breaks under inserts.
**Example**:
```python
items = DB[offset:offset + limit]
```
**Complexity**: O(offset + limit).
**Related**: Keyset pagination, OFFSET

### Opaque token
**Definition**: A cursor value whose internal structure clients cannot rely
on; may be encoded, compressed, or signed.
**Related**: Cursor

### Stable key
**Definition**: A unique, ordered, effectively immutable column (primary key,
or created_at + id) used as the keyset pagination boundary.
**Related**: Keyset pagination

### Total-count trap
**Definition**: The hidden O(n) `COUNT(*)` cost of returning `total` on every
page; mitigated by returning `has_more` instead on deep pages.
**Related**: has_more

### Range scan
**Definition**: An index operation fetching only rows within a bounded key
range — the mechanism that makes keyset pagination O(limit).
**Related**: Keyset pagination

### Composite cursor
**Definition**: A cursor encoding multiple sort columns (e.g. `"score:42,id:100"`)
so non-id sorts paginate stably via row-value comparison.
**Related**: Row-value comparison

### Query parameter
**Definition**: An explicit, typed request parameter used for filtering —
readable, validated, and documented by the framework.
**Example**:
```python
min_score: int | None = Query(None, ge=0)
```
**Related**: Filter DSL, Whitelist

### Whitelist
**Definition**: Restricting a value to a known set, e.g. sort by
`pattern="^(id|score)$"` — prevents injection and 500s from junk input.
**Related**: Query parameter

### OFFSET
**Definition**: The SQL clause that skips m rows; its scan cost is why offset
pagination degrades with depth.
**Related**: Offset pagination

### Row-value comparison
**Definition**: Comparing tuple keys `(score, id) < (:s, :i)` in SQL, enabling
composite cursors that stay stable with duplicate sort values.
**Related**: Composite cursor

### rel="next"
**Definition**: The RFC 8288 link relation signaling the next page; part of
the standard pagination contract.
**Related**: Link headers

## Key Concepts Summary

### The two pagination families
- Offset: simple, O(offset) scan, breaks under writes — fine to ~10k rows.
- Keyset: O(limit) range scan, write-robust — the default at scale.
- Keyset needs a stable unique key; composite cursors for other sorts.

### Filtering
- Explicit query params for closed filter spaces.
- Filter DSL only for genuinely open spaces.
- Whitelist sort/filter values at the boundary.

### Cost discipline
- has_more (O(limit)) instead of total (O(n)) on deep pages.
- Link headers standardize navigation.
- Cursors stay opaque; clients never construct them.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. WHERE key > :last pagination — ___
2. The O(n) cost hidden in total-count responses — ___
3. A client-unknowable page token — ___
4. LIMIT + OFFSET; O(offset) scan — ___
5. RFC 8288 navigation headers — ___
6. Encoding multiple sort columns in a cursor — ___
7. Restricting values to a known set — ___
8. The cheap signal that another page exists — ___

**Answers:** 1-keyset pagination, 2-total-count trap, 3-opaque token,
4-offset pagination, 5-link headers, 6-composite cursor, 7-whitelist,
8-has_more
