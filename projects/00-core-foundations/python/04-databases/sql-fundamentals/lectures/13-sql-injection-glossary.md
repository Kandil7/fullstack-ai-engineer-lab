# SQL Injection — Glossary 13

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Bypass | Attack | A payload defeating a filter (`' OR '1'='1' --`) |
| Data vs code | Principle | Untrusted input must stay data, never become SQL |
| Identifier | SQL | A table/column name that changes the parse tree |
| Injection | Attack | Untrusted text merged into SQL text and executed |
| Least privilege | Defense | The app role can only do what the feature needs |
| Payload | Attack | The hostile input string |
| Parameterized query | Defense | Statement and values sent separately; values bound as data |
| Placeholder | Defense | `?` / `%s` / `:name` marking where a value binds |
| Raw SQL hook | Risk | ORM `text()` / `raw()` paths that rebuild SQL text |
| Second-order injection | Attack | A stored payload executed when later interpolated |
| Whitelist | Defense | The approved set an identifier must match |
| Wrapper | Defense | One audited function guarding all SQL-text construction |

## Detailed Definitions

### Bypass
**Definition**: A payload that defeats a filter without breaking syntax —
e.g. `' OR '1'='1' --` turning a login filter into a full-table read.
**Related**: Payload

### Data vs code
**Definition**: The core principle — input must be handled as data; any
path where it is parsed as grammar is an injection vector.
**Related**: Injection

### Identifier
**Definition**: A table or column name. Identifiers change how a statement
is parsed, so they cannot be parameterized — only whitelisted.
**Example**:
```python
if column not in {"id", "username", "role"}:
    raise ValueError("forbidden identifier")
```
**Related**: Whitelist

### Injection
**Definition**: The vulnerability class where untrusted text is concatenated
into SQL (or prompts, or shell) and executed as code.
**Related**: Data vs code

### Least privilege
**Definition**: Giving the application connection only the rights the
feature needs — reads read, writes write, and nobody can `DROP` — so a
successful injection cannot escalate.
**Related**: Whitelist

### Payload
**Definition**: The crafted input designed to change a query's meaning —
quotes, boolean tautologies, comment markers, stacked statements.
**Related**: Bypass

### Parameterized query
**Definition**: The fix: SQL text is fixed at parse time; values are bound
separately by the driver, so payloads are treated as literal data.
**Example**:
```python
conn.execute("SELECT * FROM users WHERE username = ?", (username,))
```
**Related**: Placeholder

### Placeholder
**Definition**: The marker in the SQL text where a value binds — `?` in
sqlite/MySQL, `%s` in psycopg, `:name` for named params.
**Related**: Parameterized query

### Raw SQL hook
**Definition**: An ORM API accepting SQL text (`text()`, `raw()`,
`exec_driver_sql`) — safe only if built with the same parameter/whitelist
discipline as raw drivers.
**Related**: Wrapper

### Second-order injection
**Definition**: A payload stored as data in one step, then read back and
interpolated into SQL in a later step — the delayed execution of the
injection.
**Related**: Injection

### Whitelist
**Definition**: The fixed set of allowed values an identifier must match
before it may appear in SQL — the only safe way to use dynamic identifiers.
**Related**: Identifier

### Wrapper
**Definition**: A single audited function through which all SQL-text
construction must pass, making the security boundary reviewable.
**Related**: Raw SQL hook

## Key Concepts Summary

### The attack chain
1. Input reaches SQL text (interpolation).
2. Payload changes the parse (`' OR '1'='1' --`).
3. Data that should be a value becomes instructions.
4. Without least privilege, the compromise spreads.

### The defense stack
- Parameters: values can never become code.
- Whitelists: identifiers must be approved.
- Least privilege: a breach stays contained.
- Wrappers: raw-text paths are auditable boundaries.

### The AI parallel
- SQL injection: untrusted text into SQL grammar.
- Prompt injection: untrusted text into instruction grammar.
- Both are fixed by separating data from code.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Untrusted text executed as SQL — ___
2. The marker where a value binds — ___
3. `' OR '1'='1' --` is one — ___
4. Statement and values sent separately — ___
5. An approved set for identifiers — ___
6. The app role can't DROP tables — ___
7. A payload stored now, executed later — ___
8. Table/column names in a query — ___

**Answers:** 1-injection, 2-placeholder, 3-payload, 4-parameterized query,
5-whitelist, 6-least privilege, 7-second-order injection, 8-identifier
