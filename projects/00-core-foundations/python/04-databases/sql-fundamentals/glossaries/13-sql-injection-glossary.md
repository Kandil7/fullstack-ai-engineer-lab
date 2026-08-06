# SQL Injection — Glossary 13

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Comment out | Attack | Attacker's `--` or `/* */` truncates the rest of the SQL |
| f-string SQL | Anti-pattern | Interpolating values into SQL text — the vulnerability |
| Identifier whitelist | Defense | Allow only known table/column names for dynamic identifiers |
| Injection | Attack | User input interpreted as SQL syntax |
| OR 1=1 | Attack | Classic tautology; makes the WHERE always true |
| Parameterized query | Defense | ? placeholders; values can never be syntax |
| Prepared statement | Defense | SQL compiled once; parameters bound separately |
| Sanitization | Defense | Making input safe before use; parameters are the gold standard |
| Stacked statements | Attack | Multiple statements in one string; sqlite3 blocks them |
| SQL syntax vs data | Model | The core distinction parameters enforce |
| Union-based attack | Attack | UNION SELECT appends attacker rows to results |
| Whitelist | Defense | Closed set of permitted identifiers |
| Executescript | Driver | Allows multi-statement SQL; NEVER for user input |
| Blind injection | Attack | Probing via true/false responses without visible results |
| Placeholder | Defense | ? or :name marker holding a value's slot |
| Error-based attack | Attack | Crafting input that leaks schema via error messages |
| Time-based attack | Attack | Timing differences reveal conditions |
| Defense in depth | Strategy | Parameters + validation + least privilege together |
| Least privilege | Strategy | Database user can do only what the app needs |
| SQLSTATE | Errors | Standardized error codes; hint at leak risks |

## Detailed Definitions

### Injection
**Definition**: Supplying input that the query builder concatenates
into SQL text, letting the input become syntax. The top web
vulnerability for decades.
**Example** (the vulnerability):
```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
conn.execute("INSERT INTO users (name) VALUES (?)", ("admin",))
name = "x' OR '1'='1"
rows = conn.execute(f"SELECT * FROM users WHERE name = '{name}'").fetchall()
print(f"rows leaked: {len(rows)}")
```
```text
rows leaked: 1
```
**Related**: OR 1=1, f-string SQL

### f-string SQL
**Definition**: Building SQL strings with f-strings — every value
becomes a potential injection point. Never acceptable for values.
**Related**: Injection, Parameterized query

### OR 1=1
**Definition**: The classic tautology: `WHERE name = 'x' OR '1'='1'`
is always true, returning every row — login bypass, data exfiltration.
**Related**: Injection, Comment out

### Parameterized query
**Definition**: `execute("SELECT * FROM users WHERE name = ?", (name,))`
— the engine treats the parameter as data, never syntax. The fix for
injection, in one line.
**Example**:
```python
rows = conn.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchall()
print(f"rows with parameters: {len(rows)}")
```
```text
rows with parameters: 0
```
**Related**: Prepared statement, Placeholder

### Prepared statement
**Definition**: SQL compiled once with placeholders, then executed
with bound values — the mechanism parameterization relies on.
**Related**: Parameterized query, Placeholder

### Sanitization
**Definition**: Making input safe — parameter binding is the gold
standard; escaping and validation are fallbacks for special cases
(identifiers).
**Related**: Parameterized query, Whitelist

### Comment out
**Definition**: `' OR '1'='1' --` uses `--` to comment out the rest of
the query, neutralizing trailing clauses the developer added.
**Related**: Injection, OR 1=1

### Stacked statements
**Definition**: `'; DROP TABLE x; --` — multiple statements in one
string. sqlite3's execute() rejects them; executescript() does not.
**Related**: Executescript, Injection

### SQL syntax vs data
**Definition**: The model behind parameters: the statement text is
fixed, values flow through placeholders; the two can never mix.
**Related**: Parameterized query, Placeholder

### Union-based attack
**Definition**: `UNION SELECT` appends attacker-chosen rows/columns to
the result — extracting other tables' data.
**Related**: Injection, Error-based attack

### Whitelist
**Definition**: For dynamic identifiers (table names, ORDER BY
columns), validate against a fixed list; never accept raw input.
**Related**: Identifier whitelist, Sanitization

### Executescript
**Definition**: Executes multi-statement SQL text — useful for
schema scripts, catastrophic for user input. Never pass input to it.
**Related**: Stacked statements, Sanitization

### Blind injection
**Definition**: Probing conditions through true/false differences or
delays when results aren't visible — slower but just as dangerous.
**Related**: Time-based attack, Injection

### Placeholder
**Definition**: The ? or :name marker in a statement that reserves a
slot for a bound value.
**Related**: Parameterized query, Prepared statement

### Error-based attack
**Definition**: Crafting input whose error messages reveal table and
column names — schema disclosure via exceptions. Never echo raw
errors to users.
**Related**: Union-based attack, Blind injection

### Time-based attack
**Definition**: Injecting delays (e.g., heavy subqueries) and measuring
response time to confirm conditions without any output.
**Related**: Blind injection, Injection

### Defense in depth
**Definition**: Layering: parameters everywhere + input validation +
least privilege + no raw error leakage — any one layer can fail
safely.
**Related**: Least privilege, Parameterized query

### Least privilege
**Definition**: The database user runs only the operations the app
needs (e.g., no DROP for app accounts) — limits blast radius.
**Related**: Defense in depth, Stacked statements

### Identifier whitelist
**Definition**: Dynamic names resolved through a fixed mapping:
`sort = {"created": "created_at", "name": "name"}[user_input]`.
**Related**: Whitelist, Sanitization

## Key Concepts Summary

### The vulnerability
- f-string/concatenated SQL turns values into syntax.
- OR 1=1, comments, UNION, and stacked statements exploit it.
- Attack surface: WHERE clauses, ORDER BY, LIMIT, identifiers.

### The fix
- Parameterized queries everywhere: ? or :name placeholders.
- Identifiers go through whitelists, never raw.
- executescript() is for scripts, not input.

### Defense in depth
- Parameters + validation + least privilege + no error leakage.
- sqlite3's execute() blocking stacked statements is a guardrail —
  keep it by never using executescript() with user data.

## Practice Terms

Match each term to its definition.

1. Injection — ___
2. Parameterized query — ___
3. OR 1=1 — ___
4. Stacked statements — ___
5. Whitelist — ___
6. Executescript — ___
7. Blind injection — ___
8. Least privilege — ___

A. Input becomes SQL syntax
B. ? placeholders; values stay data
C. Tautology making WHERE always true
D. Multiple statements in one string
E. Closed set of permitted identifiers
F. Multi-statement execution; never for input
G. Probing via true/false or timing without output
H. DB user can do only what the app needs

**Answers:** 1-A, 2-B, 3-C, 4-D, 5-E, 6-F, 7-G, 8-H
