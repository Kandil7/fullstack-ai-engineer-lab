# Querying with select() — Glossary 05

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| aliased() | Query | A second reference to a mapped class for self-joins |
| and_ | Filter | AND-combines predicates explicitly |
| bound parameter | SQL | A value passed separately from the SQL text |
| distinct() | Query | Removes duplicate rows from a select |
| execute() | Session | Runs a statement and returns Row objects |
| func | Aggregation | SQL function namespace: count, max, avg, row_number |
| group_by | Aggregation | Groups rows for aggregate functions |
| in_ | Filter | Column IN (values...) membership |
| join() | Query | Inner join; ON clause inferred from the FK |
| keyset | Pagination | Cursor-based paging on the last-seen row |
| like | Filter | Pattern matching with % and _ wildcards |
| limit()/offset() | Pagination | Simple paging; OFFSET degrades at scale |
| or_ | Filter | OR-combines predicates |
| outerjoin() | Query | LEFT JOIN; keeps left rows without matches |
| Row | Result | A result row; positional and named access |
| scalars() | Session | Unwraps single-column results into values/objects |
| select() | Query | The 2.0 SELECT statement builder |
| tuple_ | Query | Row-value comparison for composite cursors |
| where() | Query | Adds WHERE conditions (AND-composed) |

## Detailed Definitions

### aliased()
**Definition**: Creates a second, distinct reference to a mapped class so a
table can be joined to itself (parent/child, duplicate detection).
**Example**:
```python
from sqlalchemy.orm import aliased
parent = aliased(PromptTemplate)
stmt = select(PromptTemplate.name, parent.name).join(
    parent, PromptTemplate.parent_id == parent.id)
```
**Related**: join(), self-referential (topic 04)

### and_
**Definition**: Explicit AND composition of predicates. `.where()` already
ANDs; `and_` is for inside `or_` or for building predicates dynamically.
**Example**:
```python
from sqlalchemy import and_
stmt = select(Experiment).where(
    and_(Experiment.model == "bert", Experiment.status == "done"))
```
**Related**: or_, where()

### bound parameter
**Definition**: A value passed separately from SQL text (`:name` -> dict).
The database treats it as data — injection-proof and quoting-safe.
**Related**: where(), select()

### distinct()
**Definition**: Adds DISTINCT — dedupes result rows. Needed when an object
list would otherwise repeat per joined row.
**Example**:
```python
stmt = select(Experiment).join(EvalMetric).distinct()
```
**Related**: join(), select()

### execute()
**Definition**: Runs a statement and returns `Row` objects — the API for
projections (subset of columns) and aggregates, where no ORM object exists.
**Example**:
```python
rows = session.execute(select(Experiment.name, Experiment.status)).all()
```
**Related**: scalars(), Row

### func
**Definition**: The SQL function namespace: `func.count`, `func.max`,
`func.avg`, `func.row_number` compile to the dialect's functions.
**Example**:
```python
from sqlalchemy import func
stmt = select(Experiment.model, func.max(EvalMetric.value)).group_by(Experiment.model)
```
**Related**: group_by, execute()

### group_by
**Definition**: Groups rows so aggregates compute per group — one output row
per distinct grouping value.
**Example**:
```python
stmt = select(Experiment.model, func.count()).group_by(Experiment.model)
```
**Related**: func, execute()

### in_
**Definition**: Column membership: `Experiment.status.in_(["done", "archived"])`.
**Example**:
```python
stmt = select(Experiment).where(Experiment.status.in_(["done", "archived"]))
```
**Related**: where(), or_

### join()
**Definition**: Inner join. The ON clause is inferred from the foreign key;
be explicit when multiple paths exist.
**Example**:
```python
stmt = select(Experiment).join(EvalMetric)
```
**Related**: outerjoin(), aliased()

### keyset
**Definition**: Cursor pagination: `WHERE id > :last ORDER BY id LIMIT n`.
Each page costs O(page_size); pages stay stable as rows arrive. The
production pager.
**Example**:
```python
stmt = select(Experiment).where(Experiment.id > last_id).order_by(Experiment.id).limit(20)
```
**Complexity**: O(page_size) per page.
**Related**: limit()/offset(), tuple_

### like
**Definition**: Pattern matching: `%` any sequence, `_` one char. Compiles to
LIKE with bound parameters.
**Example**:
```python
stmt = select(Experiment).where(Experiment.name.like("bert-%"))
```
**Related**: where(), bound parameter

### limit()/offset()
**Definition**: Simple paging. `OFFSET m` makes the DB read and discard m
rows — degrades at scale; fine for small tables.
**Example**:
```python
stmt = select(Experiment).order_by(Experiment.id).limit(20).offset(40)
```
**Complexity**: O(m + n) per page.
**Related**: keyset

### or_
**Definition**: Explicit OR composition of predicates.
**Example**:
```python
from sqlalchemy import or_
stmt = select(Experiment).where(or_(Experiment.status == "running", Experiment.model == "gpt2"))
```
**Related**: and_, where()

### outerjoin()
**Definition**: LEFT OUTER JOIN: every left-side row appears, with NULLs for
unmatched right side. The "include rows without children" query.
**Example**:
```python
stmt = select(Experiment.name, func.count(EvalMetric.id)).outerjoin(EvalMetric)
```
**Related**: join()

### Row
**Definition**: A result row from `execute()`: `row[0]` by position, `row.name`
by column name. The data shape of projections.
**Related**: execute(), scalars()

### scalars()
**Definition**: Executes a statement and unwraps single-column results —
values or ORM objects, not Rows. The default read API for entities.
**Example**:
```python
exps = session.scalars(select(Experiment)).all()
```
**Related**: execute(), select()

### select()
**Definition**: The 2.0 statement builder: `select(Experiment)` or
`select(Experiment.name, Experiment.status)`, composed with `.where()`,
`.join()`, `.order_by()`, `.limit()`.
**Related**: scalars(), execute(), where()

### tuple_
**Definition**: Row-value comparison: `tuple_(a, b) > (x, y)` compares
composite keys lexicographically — the multi-column keyset cursor.
**Example**:
```python
from sqlalchemy import tuple_
cursor = (last_id, last_name)
stmt = select(Experiment).where(
    tuple_(Experiment.id, Experiment.name) > cursor)
```
**Related**: keyset

### where()
**Definition**: Adds WHERE conditions; multiple calls AND together.
**Example**:
```python
stmt = select(Experiment).where(Experiment.status == "done").where(Experiment.model == "bert")
```
**Related**: and_, or_, select()

## Key Concepts Summary

### Read APIs
- `scalars()` for ORM objects; `execute()` for Rows and aggregates
- projections: select only the columns you need
- aggregates: func + group_by, run in the DB

### Join Shapes
- `join()` inferred ON; `outerjoin()` keeps left rows
- `aliased()` enables self-joins
- narrow joins before aggregating (filter metric first)

### Pagination
- OFFSET: simple, degrades
- keyset: O(page_size), stable pages
- `tuple_` for composite cursors

## Practice Terms

Match each term to its definition (answers at the bottom).

1. scalars() — ___
2. outerjoin() — ___
3. keyset — ___
4. aliased() — ___
5. group_by — ___
6. tuple_ — ___

A) Cursor pagination on the last-seen row
B) Unwraps single-column results into values/objects
C) LEFT JOIN keeping left rows without matches
D) Row-value comparison for composite cursors
E) Second reference to a class for self-joins
F) Groups rows for aggregates

**Answers:** 1-B, 2-C, 3-A, 4-E, 5-F, 6-D
