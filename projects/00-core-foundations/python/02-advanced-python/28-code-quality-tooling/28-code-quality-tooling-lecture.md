# Advanced Python — 28: Code Quality Tooling

## Topic Overview

Code quality tooling is the difference between a codebase that stays
reviewable at 100k lines and one that drowns in its own bugs. The modern
Python stack — `ruff` for lint+format, `black` for style, `mypy` for static
types, `pre-commit` for local gating, `bandit` for security smells, and
`pip-audit` for dependency CVEs — exists because Python's dynamism gives
you a long runway to write code that *works* and a short one to write code
that is *maintainable*.

This lecture teaches the *mechanics*: what each tool checks, how the checks
work under the hood (almost all of them are `ast` walks), and how to wire
them into a CI gate. Crucially, we implement a miniature linter in pure
Python so the concepts run anywhere — including offline CI where the real
tools are not installed. The exercise file `28-code-quality-tooling.py`
builds exactly that.

Where this fits: Phase 2 is about production Python. Topics 18 (testing),
19 (logging), and 27 (packaging) are your other quality pillars; this topic
is the gatekeeper that runs before any of them get reviewed.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain what each tool in the stack does and where it runs (locally vs CI)
2. Write `ast`-based rules for mutable defaults, bare excepts, and complexity
3. Compute cyclomatic complexity and state what a sane CI cap is
4. Use `# noqa` correctly: scoped, coded, and justified
5. Configure select/ignore rule sets and reason about what a gate rejects
6. Distinguish lint (style + smells) from static typing (`mypy`) from
   security scanning (`bandit`, `pip-audit`)
7. Wire a gate into pre-commit and CI so bad code never merges
8. Diagnose why a rule fired by reading its message, not suppressing it

## Prerequisites

| Need | Where |
|---|---|
| `ast` module basics (parse, walk) | `01-core-python` modules on syntax & AST |
| Testing and CI mentality | `18-unit-testing-lecture.md` |
| Packaging and tool config | `27-packaging-and-distribution-lecture.md` |
| Type hints (for `mypy` context) | `05-type-hints-lecture.md` |

---

## 1. The Toolchain Map

Six tools, one pipeline. Learn the *layer* each one guards:

| Tool | Layer | Catches |
|---|---|---|
| `ruff` | lint + format | style, smells, unused imports, bugs (B006, E722) |
| `black` | format | formatting disagreements (subsumed by ruff format) |
| `mypy` | static types | wrong types, None leaks, broken contracts |
| `pre-commit` | orchestration | runs the above locally before every commit |
| `bandit` | security lint | `eval`, shell=True, weak hashes, pickle of untrusted |
| `pip-audit` | dependencies | known CVEs in your dependency tree |

The key insight: **each tool is a different failure class**. Lint is about
how the code *looks* and obvious smells; mypy is about what the code
*claims*; bandit is about what the code *enables an attacker to do*;
pip-audit is about what your *dependencies* do.

```python
# The pipeline in one shell line (pre-commit runs this locally):
# ruff check . && ruff format --check . && mypy src/
# then in CI: bandit -r src/ && pip-audit
print("gate order: lint -> format -> types -> security -> deps")
```

Output:

```text
gate order: lint -> format -> types -> security -> deps
```

---

## 2. Why Lint Rules Are AST Walks

A linter does not read text like a human; it parses your file into an
abstract syntax tree and walks it. This is why `except:` inside a string
literal is never flagged, and why a regex-based checker is a category error.

```python
import ast

source = "def f(a=[]):\n    return a\n"
tree = ast.parse(source)
node = tree.body[0]
print(type(node).__name__, "with defaults:",
      [type(d).__name__ for d in node.args.defaults])
```

Output:

```text
FunctionDef with defaults: ['List']
```

A `List` default is mutable. A `Constant` default is not. The AST *knows*
this; a regex cannot. Every rule in the rest of this lecture is a small
walk over the same tree.

---

## 3. Rule: Mutable Default Arguments (B006)

```python
def append_item(store=[]):   # B006: the SAME list is shared across calls
    store.append(len(store))
    return store
```

The first call returns `[0]`, the second `[0, 1]` — state leaking through
what looks like a pure function. In notebook-derived ML code this shows up
as "the second training run behaved differently."

```python
def find_mutable_defaults(source):
    tree = ast.parse(source)
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for default in node.args.defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    hits.append((node.lineno, node.name))
    return hits

print(find_mutable_defaults("def f(a=[]): pass\ndef g(a=None): pass"))
```

Output:

```text
[(1, 'f')]
```

The fix is always the same: use `None` and build the mutable inside.

---

## 4. Rule: Bare Except (E722)

`except:` with no exception type catches `KeyboardInterrupt` and
`SystemExit` too. During a 40-hour training run, that means Ctrl-C *does
not stop the process* — the most expensive bug a bare except can hide.

```python
import ast

def find_bare_excepts(source):
    tree = ast.parse(source)
    return [h.lineno for node in ast.walk(tree)
            if isinstance(node, ast.Try)
            for h in node.handlers if h.type is None]

src = "try:\n    risky()\nexcept:\n    pass\n"
print(find_bare_excepts(src))
```

Output:

```text
[3]
```

Same idea, different node: `ast.Try.handlers[].type is None`. Rules are
cheap once you know which node to look at.

---

## 5. Cyclomatic Complexity (C901)

Complexity = 1 + every decision point: `if`, `for`, `while`, `except`,
ternary, and each `and`/`or`. It answers "how many independent paths must
a test cover?" Teams commonly gate at 10; at 15+ a function is
untestable and should be split.

```python
import ast

def count_decisions(node):
    n = 0
    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.For, ast.While,
                              ast.ExceptHandler, ast.IfExp)):
            n += 1
        elif isinstance(child, ast.BoolOp):
            n += len(child.values) - 1
    return n

src = ("def tangled(a, b):\n"
       "    if a and b or a:\n"
       "        for i in range(10):\n"
       "            if i % 2:\n"
       "                return i\n")
tree = ast.parse(src)
fn = tree.body[0]
print(f"complexity: {1 + count_decisions(fn)}")
```

Output:

```text
complexity: 6
```

1 base + 1 `if` + 1 `and/or` + 1 `for` + 1 inner `if` = 5 decisions... plus
the BoolOp with 3 values counts as 2, giving 6. The exact arithmetic is
less important than the trend: nested branches are expensive to test, so
the metric pushes you toward flat, composable functions.

---

## 6. Text-Level Rules: Docstrings, Line Length, Whitespace

Some rules are text, not AST: `D100` (missing docstring), `E501` (line too
long), `W291` (trailing whitespace). These are the rules that make *diffs*
reviewable: a trailing space in a diff line is noise; an 300-char line
hides the change.

```python
def missing_docstrings(source):
    tree = ast.parse(source)
    return [(n.lineno, n.name) for n in ast.walk(tree)
            if isinstance(n, (ast.FunctionDef, ast.ClassDef))
            and ast.get_docstring(n) is None]

print(missing_docstrings("def f():\n    pass\n"))
```

Output:

```text
[(1, 'f')]
```

Why docstrings matter beyond politeness: `help()`, IDEs, and documentation
generators all read them — and a missing docstring usually means nobody
knows what the function *guarantees*.

---

## 7. noqa Discipline

`# noqa: CODE` suppresses one rule on one line. Discipline means three
things: (1) always name the code, (2) always give the reason, (3) never
suppress a rule project-wide because one spot annoys you.

```python
# The three forms:
x = 1  # noqa: E501   -- coded, no reason (acceptable for generated lines)
y = 2  # noqa: E501 - long URL required by spec
z = 3  # noqa        -- blanket: suppresses EVERY rule on this line (weakest)
```

```python
def suppressed_lines(source):
    return {i + 1 for i, line in enumerate(source.splitlines())
            if "# noqa" in line}

src = "def f(x=[]):  # noqa: B006 - API contract requires a shared list\n"
print(sorted(suppressed_lines(src)))
```

Output:

```text
[1]
```

The gate then drops any violation whose line is in the suppressed set. A
blanket `# noqa` at the top of a file is a bug report you have not read yet.

---

## 8. Config and CI Gating

Real tools are configured: ruff has `select`/`ignore`, `per-file-ignores`,
line length, and target version. The gate combines everything and fails
the build on any violation. Pre-commit runs it *locally* so CI only sees
clean code — a gate that runs only after merge is a post-mortem, not a gate.

```python
from dataclasses import dataclass, field

RULES = ("B006", "E722", "C901", "D100", "E501", "W291")

@dataclass
class LintConfig:
    select: set[str] = field(default_factory=lambda: set(RULES))
    ignore: set[str] = field(default_factory=set)
    max_complexity: int = 10

cfg = LintConfig(ignore={"E722"})
print("active rules:", sorted(cfg.select - cfg.ignore))
```

Output:

```text
active rules: ['B006', 'C901', 'D100', 'E501', 'W291']
```

The gate function (full version in the exercise) parses once, runs every
selected rule, honors noqa, and returns a clean/pass verdict. In CI you
exit non-zero on any violation; locally, pre-commit refuses the commit.

---

## 9. Static Typing: mypy

Lint catches what is *obviously* wrong; mypy catches what is *inconsistent*.
A function annotated `-> list[float]` that returns `None` on some path
passes lint and crashes at runtime — mypy finds it before merge.

```python
from typing import Optional

def mean(values: list[float]) -> float:
    if not values:
        return None  # mypy error: Incompatible return value type
    return sum(values) / len(values)
```

The fix is either a proper error path (`raise ValueError`) or a `None`
return type. The discipline — annotate first, let mypy adjudicate the
contract — is why typed ML codebases refactor safely: the type checker
finds every call site that assumed the old behavior.

---

## 10. Security Lint and Dependency Audit

`bandit` scans for the same class of bugs as topic 33: `eval`/`exec` on
untrusted input, `shell=True`, weak hash algorithms, `pickle.load` of
untrusted files. `pip-audit` queries CVE feeds against your lockfile —
a dependency you pinned in January may have a disclosed RCE in July, and
nothing in your own code will ever tell you.

```python
# bandit flags this immediately:
# subprocess.call("ls " + user_input, shell=True)   # B602
# eval(user_input)                                  # B307
# pickle.load(open(model_path, "rb"))               # B301 if untrusted
print("security lint = topic 33 as an automated rule set")
```

Output:

```text
security lint = topic 33 as an automated rule set
```

The pattern to internalize: **lint for your own mistakes, audit for
everyone else's**. You can read all your code; you cannot read all of
numpy's.

---

## Common Mistakes to Avoid

### Mistake 1: Suppressing instead of reading
```
# WRONG — hides every future bare except too
[tool.ruff]
ignore = ["E722"]
# CORRECT — one line, one reason
except:  # noqa: E722 - deliberated, documented, tested
```

### Mistake 2: Only linting in CI
```
# WRONG — bugs are found after merge, during review
# CORRECT — pre-commit runs the same rules locally at commit time
```

### Mistake 3: Regex-based "linting" of Python
```
# WRONG — a regex cannot know this except: is inside a string
# CORRECT — ast.parse and walk the tree; structure over text
```

### Mistake 4: Ignoring the complexity cap "just for this one function"
```
# WRONG — every function starts as "just this one"
# CORRECT — split, or add the noqa with a reason and a refactor ticket
```

### Mistake 5: Running black and ruff format with conflicting settings
```
# WRONG — two formatters fighting produces churn commits
# CORRECT — ruff format is black-compatible; use one or the other
```

### Mistake 6: Treating mypy errors as optional
```
# WRONG — `# type: ignore` without a ticket
# CORRECT — strict mode in CI; ignore only with a reason
```

## Best Practices

1. **Parse once, walk once** — every rule should reuse a single `ast.parse`
2. **Gate at 10 complexity** — split anything above; it is un-reviewable
3. **Noqa with code and reason** — `# noqa: E501 - URL required by spec`
4. **Run the gate locally via pre-commit** — CI is the backstop, not the front line
5. **Lint + format + types in one command** — one entry point, zero excuses
6. **Pin tool versions** — a new ruff release re-lints your whole history
7. **Bandit on every PR** — security smells found early cost nothing
8. **pip-audit weekly in CI** — CVEs land in dependencies you already have
9. **Keep the gate fast** — if lint takes minutes, developers skip it
10. **Read the rule docs before suppressing** — most rules have a fix hint

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| `ast.parse` | O(N) | O(N) | — (unavoidable, C-speed) |
| `ast.walk` per rule | O(N) | O(depth) | one walk for all rules |
| Regex scanning source | O(N) | O(N) | — (but cannot see structure) |
| `mypy` on a package | ~seconds–minutes | O(project) | incremental mode |
| `pip-audit` | ~seconds | small | lockfile scanning, no install |
| Black/ruff format on 10k lines | < 1s | small | — |

The cost model that matters: **lint is free, review is expensive, and a
production bug found after deploy is the most expensive thing in the
table**. Pay the O(N) walk; skip the 2-hour debugging session.

## AI Engineering Relevance

**Where this shows up:** an ML repo that grew from notebooks. The classic
failure chain: a notebook becomes a training script, the script becomes a
service, and the mutable-default bug that was harmless in a notebook is
now silently corrupting a shared cache in production.

| Concept here | Used for |
|---|---|
| B006 mutable defaults | catching `def embed(texts=[])` cache corruption |
| E722 bare except | preventing Ctrl-C from being swallowed mid-training |
| C901 complexity | keeping a 200-line preprocessing "function" reviewable |
| D100 docstrings | forcing `RetrievedChunk` semantics to be written down |
| mypy strict | typing `Retriever` so Qdrant/Chroma are interchangeable |
| bandit + pip-audit | flagging `pickle.load(model)` and CVE-ridden deps |

**Scale note:** at 10k lines lint is instant and you can skip it; at 500k
lines (three services sharing a `rag_utils` package) an unformatted
codebase costs a day of review per week. The gate is what keeps a
fast-moving ML team fast: machines check the 80% of review that is
mechanical, humans review the 20% that is judgment.

## Practice Exercises

### Exercise 1: Flag trailing whitespace (Difficulty: Easy)
Write `trailing_ws(source: str) -> list[int]` returning line numbers that
end in a space or tab.

### Exercise 2: Detect unused imports (Difficulty: Medium)
Write `unused_imports(source: str) -> list[str]` using `ast.Import` /
`ast.ImportFrom`, comparing imported names against every `ast.Name` id in
the tree. Skip `*` imports.

### Exercise 3: Complexity budget (Difficulty: Medium)
Write `over_budget(source: str, cap: int) -> list[str]` returning function
names whose cyclomatic complexity exceeds `cap`.

### Exercise 4: noqa-aware gate (Difficulty: Hard)
Write `gate(source: str, rules: dict[str, bool]) -> tuple[bool, list[str]]`
that runs a rule set (mutable defaults, bare except, missing docstrings),
honors `# noqa: CODE` per line, and returns `(clean, fired_rules)`.

### Exercise 5: Report as JSON (Difficulty: Hard)
Wrap the gate in `lint_json(path: str) -> str` that reads a file, runs
the rules, and returns a JSON string with violations grouped by rule and
sorted by line — stable output suitable for CI artifacts.

## Summary

| Concept | Description |
|---|---|
| Toolchain layers | lint → format → types → security → deps, each a different failure class |
| AST-based rules | parse once, walk; structure beats regex |
| B006 / E722 | mutable defaults and bare excepts — the two notebook-bug classics |
| C901 complexity | 1 + decision points; gate at 10 |
| noqa | scoped, coded, reasoned suppression — never blanket |
| CI gate | pre-commit locally, exit non-zero in CI |
| mypy / bandit / pip-audit | contracts, security smells, dependency CVEs |

Code quality tooling is not bureaucracy; it is the machinery that makes
review possible at scale. A team that lints, formats, types, and audits
mechanically spends its review hours on design instead of whitespace and
shipped bugs.

## Quick Reference

| Task | Idiom |
|---|---|
| Lint + fix | `ruff check . --fix` |
| Format check | `ruff format --check .` |
| Type check | `mypy src/ --strict` |
| Run locally on commit | add the tools to `.pre-commit-config.yaml` |
| Suppress one line | `x = 1  # noqa: E501 - reason` |
| Parse once | `tree = ast.parse(src)` then walk |
| Complexity of a function | `1 + count of if/for/while/except/and/or/ternary` |
| Security scan | `bandit -r src/` |
| Dependency CVEs | `pip-audit` (weekly in CI) |

## Next Steps

Next: **[29 — Functional Python](29-functional-python-lecture.md)** — pure
functions and immutable data, which are the code-quality ideas applied at
the design level (a functional core is the best "lint-free" code there is).

Continues in: **[Phase 3 — Libraries](../../03-libraries/README.md)** —
reproducible data pipelines depend on the discipline this topic installs.

Official docs:
- [ast — Abstract Syntax Trees](https://docs.python.org/3/library/ast.html)
- [ast module for annotations](https://docs.python.org/3/library/ast.html)
- [ruff rules](https://docs.astral.sh/ruff/rules/)
- [mypy](https://mypy.readthedocs.io/)
- [bandit](https://bandit.readthedocs.io/)
- [pip-audit](https://pypi.org/project/pip-audit/)
