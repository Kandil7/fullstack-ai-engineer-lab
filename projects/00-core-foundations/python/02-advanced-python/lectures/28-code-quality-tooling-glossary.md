# Code Quality Tooling — Glossary 28

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| `ast` walk | Tooling | A single traversal of the syntax tree; the mechanism behind every lint rule |
| B006 | Rule | Ruff rule: mutable default arguments (`def f(x=[])`) |
| bandit | Tool | Security linter: `eval`, `shell=True`, weak hashes, unsafe pickle |
| black | Tool | Opinionated code formatter: one style, zero configuration |
| CI gate | Process | A pipeline step that fails the build when a rule fires |
| C901 | Rule | Ruff rule: cyclomatic complexity above the configured cap |
| cyclomatic complexity | Metric | 1 + number of decision points in a function |
| D100 | Rule | Ruff rule: missing module/function/class docstring |
| E501 | Rule | Ruff rule: line exceeds the maximum length |
| E722 | Rule | Ruff rule: bare `except:` with no exception type |
| formatter | Tool | Rewrites code to a canonical style (black / ruff format) |
| linter | Tool | Reports code smells without changing the code |
| mypy | Tool | Static type checker; verifies annotations without running code |
| `# noqa` | Discipline | Per-line suppression of one or more lint rules |
| pip-audit | Tool | Scans dependencies against public CVE databases |
| pre-commit | Tool | Runs configured hooks locally before every commit |
| ruff | Tool | Fast Python linter + formatter (replaces flake8/isort/black) |
| select/ignore | Config | Which rules run; which are disabled in a linter config |
| static typing | Concept | Checking types at analysis time, not runtime |
| W291 | Rule | Ruff rule: trailing whitespace at end of line |

## Detailed Definitions

### `ast` walk
**Definition**: Parsing source into an abstract syntax tree and visiting
every node once. Lint rules are predicates over node types — a regex
cannot know that `except:` is inside a string literal; the AST can.
**Example**:
```python
import ast

def mutable_defaults(source: str) -> list[tuple[int, str]]:
    tree = ast.parse(source)
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for default in node.args.defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    hits.append((node.lineno, node.name))
    return hits

print(mutable_defaults("def f(a=[]):\n    return a\n"))
```
```text
[(1, 'f')]
```
**Complexity**: O(N) time, O(N) space for the tree.
**Related**: B006, cyclomatic complexity, linter

### B006
**Definition**: Ruff rule code for *mutable default argument*. The default
object is created once at function definition, so all calls share it.
**Example**:
```python
def buggy(store=[]):
    store.append(1)
    return store

print(buggy(), buggy())
```
```text
[1] [1, 1]
```
**Related**: `ast` walk, linter, Common Mistakes (Mistake 1)

### bandit
**Definition**: A security-focused linter that scans source for dangerous
patterns: `eval`/`exec`, `shell=True`, MD5/SHA1 password hashing, and
`pickle.load` on untrusted input. It is the automated form of topic 33.
**Example**:
```python
# bandit -r .  reports:
# B307: Use of possibly insecure function: eval
# B602: subprocess call with shell=True seems unsafe
print("bandit turns security review into a rule set")
```
```text
bandit turns security review into a rule set
```
**Related**: pip-audit, CI gate, security lint

### black
**Definition**: An opinionated formatter — it rewrites code to a single
canonical style so formatting arguments disappear from review. `ruff
format` implements the same style at higher speed.
**Example**:
```python
# Before black:
def f(  a,b,c   ):return a+b+c
# After black:
def f(a, b, c):
    return a + b + c
print("one style, zero configuration")
```
```text
one style, zero configuration
```
**Related**: formatter, ruff, pre-commit

### CI gate
**Definition**: The step in a pipeline that runs the lint/format/type/
security checks and fails the build on any violation. A gate that runs
only after merge is not a gate.
**Example**:
```python
def gate(source: str) -> bool:
    """True if no selected rule fires. Exit code drives CI."""
    return not lint_source(source).violations  # simplified

print(gate("def f(a=[]):\n    return a\n"))
```
```text
False
```
**Related**: pre-commit, select/ignore, linter

### C901
**Definition**: Ruff rule for functions whose cyclomatic complexity exceeds
the cap (default 10). Fires per function; the message names the function.
**Example**:
```python
src = ("def f(x):\n"
       "    if x:\n"
       "        for i in range(3):\n"
       "            if i:\n"
       "                return i\n"
       "    return 0\n")
# complexity = 1 + if + for + if = 4
print("C901 message: 'f: complexity 4 > 10' would NOT fire; 12 would")
```
```text
C901 message: 'f: complexity 4 > 10' would NOT fire; 12 would
```
**Related**: cyclomatic complexity, CI gate, Best Practices

### cyclomatic complexity
**Definition**: A count of independent paths through a function:
`1 + if + for + while + except + ternary + (and/or operators)`. Values
above ~10 are hard to test; above 15 they are untestable.
**Example**:
```python
def count_decisions(node):
    n = 0
    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.For, ast.While, ast.IfExp)):
            n += 1
        elif isinstance(child, ast.BoolOp):
            n += len(child.values) - 1
    return n

import ast
tree = ast.parse("def f(a):\n    if a and b:\n        return 1\n")
print(1 + count_decisions(tree.body[0]))
```
```text
3
```
**Related**: C901, CI gate, code review

### D100
**Definition**: Ruff rule: public module/class/function lacks a docstring.
Docstrings are the contract readers and `help()` rely on.
**Example**:
```python
def f():  # D100 fires here
    pass

def g():
    """Add one."""  # D100 satisfied
    pass
print("D100: missing docstring reported at line 1")
```
```text
D100: missing docstring reported at line 1
```
**Related**: linter, `ast` walk, code review

### E501
**Definition**: Ruff rule: a line is longer than the configured maximum
(88 by default). Long lines hide changes in diffs and break terminal
readers.
**Example**:
```python
short = "x = 1"
long_line = "result = some_function(alpha, beta, gamma, delta, epsilon, zeta, eta, theta)"
print(len(long_line) > 88)
```
```text
True
```
**Related**: formatter, black, code review

### E722
**Definition**: Ruff rule: bare `except:` with no exception type. It
catches `KeyboardInterrupt` and `SystemExit`, which is how a long
training run refuses to stop on Ctrl-C.
**Example**:
```python
try:
    risky()
except:  # E722 fires
    pass
print("bare except hides KeyboardInterrupt and SystemExit")
```
```text
bare except hides KeyboardInterrupt and SystemExit
```
**Related**: B006, linter, `ast` walk

### formatter
**Definition**: A tool that rewrites source to a canonical style. Unlike a
linter, it *changes* the code; that is the point — formatting becomes a
machine decision, not a review topic.
**Example**:
```python
print("black/ruff format: machine-owned formatting")
```
```text
black/ruff format: machine-owned formatting
```
**Related**: black, ruff, pre-commit

### linter
**Definition**: A tool that analyzes source and *reports* problems without
changing it. Modern linters parse to an AST and walk it (see `ast` walk).
**Example**:
```python
print("linter: reports; formatter: rewrites")
```
```text
linter: reports; formatter: rewrites
```
**Related**: ruff, `ast` walk, CI gate

### mypy
**Definition**: A static type checker that verifies annotations without
running the program. It finds `None`-leaks, wrong argument types, and
contract violations at merge time instead of runtime.
**Example**:
```python
def mean(values: list[float]) -> float:
    if not values:
        return None  # mypy: Incompatible return value type
    return sum(values) / len(values)
print("mypy catches the annotation/runtime mismatch")
```
```text
mypy catches the annotation/runtime mismatch
```
**Related**: static typing, CI gate, type hints

### `# noqa`
**Definition**: An inline comment that suppresses lint rules on the line it
appears on. Discipline: name the code, give the reason, never suppress
project-wide.
**Example**:
```python
def f(x=[]):  # noqa: B006 - shared list is the API contract
    return x
print("suppressed: B006 no longer fires on line 1")
```
```text
suppressed: B006 no longer fires on line 1
```
**Related**: B006, linter, Best Practices

### pip-audit
**Definition**: A tool that scans your lockfile/requirements against public
CVE databases and reports known-vulnerable dependencies. Your own code
can be perfect and still be compromised by a dependency.
**Example**:
```python
# pip-audit --requirement requirements.txt
print("pip-audit answers: which dependencies are known-bad?")
```
```text
pip-audit answers: which dependencies are known-bad?
```
**Related**: bandit, CI gate, dependency management

### pre-commit
**Definition**: A framework that installs git hooks running your tools
(lint, format, secrets scan) before each commit. It is the *local* front
line; CI is the backstop.
**Example**:
```python
# .pre-commit-config.yaml (excerpt)
# - repo: https://github.com/astral-sh/ruff-pre-commit
#   hooks: [{id: ruff, args: [check, --fix]}]
print("pre-commit: refuse the commit, not the merge")
```
```text
pre-commit: refuse the commit, not the merge
```
**Related**: CI gate, ruff, black

### ruff
**Definition**: A fast Python linter and formatter written in Rust,
replacing flake8, isort, and black in one tool. Its rules have codes
(B006, E722, C901, D100, E501, W291 used throughout this glossary).
**Example**:
```python
# ruff check . --fix
print("ruff: lint + format at compile-tool speed")
```
```text
ruff: lint + format at compile-tool speed
```
**Related**: linter, formatter, `# noqa`, select/ignore

### select/ignore
**Definition**: Linter configuration controlling which rules run:
`select` names the rule universe, `ignore` removes rules from it. Ignoring
a rule globally is a decision that deserves a comment.
**Example**:
```python
config = {"select": ["B006", "E722", "C901"], "ignore": ["E722"]}
active = set(config["select"]) - set(config["ignore"])
print(sorted(active))
```
```text
['B006', 'C901']
```
**Related**: ruff, CI gate, `# noqa`

### static typing
**Definition**: Checking type consistency at analysis time using the
annotations, without executing the program. Catches a class of bugs that
lint cannot see because they only manifest on some inputs.
**Example**:
```python
from typing import Optional

def f(x: int) -> Optional[int]:
    return None if x < 0 else x

print("static typing: contracts checked before runtime")
```
```text
static typing: contracts checked before runtime
```
**Related**: mypy, type hints, CI gate

### W291
**Definition**: Ruff rule: trailing whitespace. Invisible in most editors,
visible as noise in every diff.
**Example**:
```python
line = "x = 1  "   # two trailing spaces
print(line.rstrip() == "x = 1" and line != line.rstrip())
```
```text
True
```
**Related**: E501, formatter, code review

## Key Concepts Summary

### The Toolchain Is Layered
- **Lint** (ruff): style + smells + obvious bugs — how the code looks
- **Format** (black/ruff format): one canonical style — how the code is written
- **Types** (mypy): contracts checked without running — what the code claims
- **Security** (bandit, pip-audit): your mistakes and your dependencies' mistakes
- **Local vs CI** (pre-commit then gate): refuse the commit, then the merge

### Rules Are AST Predicates
- Parse once, walk once — every rule is a node-type check
- B006: mutable defaults; E722: bare except; C901: decision count
- D100/E501/W291: the text-level rules that make diffs reviewable
- `# noqa: CODE - reason` is the escape hatch with discipline

### The Gate Is the Product
- Fail the build on violations; print stable, sorted reports
- Complexity cap ~10 keeps functions testable
- Speed matters: a gate that takes minutes is skipped by developers

## Practice Terms

Match each term to its definition (answers at the bottom).

1. B006 — ___
2. cyclomatic complexity — ___
3. bandit — ___
4. `# noqa` — ___
5. pre-commit — ___
6. mypy — ___
7. E722 — ___
8. pip-audit — ___

A. Runs configured checks locally before every commit
B. Security linter for `eval`, `shell=True`, weak hashes
C. Rule: mutable default arguments
D. Rule: bare except with no exception type
E. 1 + number of decision points in a function
F. Per-line suppression of lint rules
G. Static type checker for annotated contracts
H. Scans dependencies against public CVE databases

**Answers:** 1-C, 2-E, 3-B, 4-F, 5-A, 6-G, 7-D, 8-H
