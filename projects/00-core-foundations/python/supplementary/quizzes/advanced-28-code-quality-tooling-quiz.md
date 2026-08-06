# Code Quality Tooling Quiz

## Topic Overview
This quiz covers Python code quality tooling: `ast`-based lint rules
(B006, E722, C901, D100, E501), noqa discipline, formatters, static typing
with mypy, security linting (bandit, pip-audit), and CI gating.

## Instructions
- 20 questions, 4 options each
- Suggested time: 25 minutes
- 1 point per correct answer

---

## Questions

### Question 1
**What does the B006 rule detect?**

A) Bare `except:` clauses
B) Mutable default arguments like `def f(x=[])`
C) Lines longer than 88 characters
D) Missing docstrings

**Difficulty:** Easy

---

### Question 2
**Why is a bare `except:` dangerous in a training script?**

A) It is slow to compile
B) It catches `KeyboardInterrupt` and `SystemExit`, so Ctrl-C cannot stop the run
C) It only catches network errors
D) It makes the linter fail with a syntax error

**Difficulty:** Easy

---

### Question 3
**What is the output of this code?**
```python
import ast

src = "def f(a=None, b=[]):\n    return b\n"
tree = ast.parse(src)
fn = tree.body[0]
defaults = [type(d).__name__ for d in fn.args.defaults]
print(defaults)
```

A) `['NoneType', 'List']`
B) `['Constant', 'List']`
C) `['Constant', 'ListComp']`
D) `['Name', 'List']`

**Difficulty:** Medium

---

### Question 4
**What is cyclomatic complexity of this function?**
```python
def f(a, b):
    if a:
        return 1
    if b:
        return 2
    return 0
```

A) 1
B) 2
C) 3
D) 4

**Difficulty:** Medium

---

### Question 5
**Which of these is the correct noqa discipline?**

A) `# noqa` at the top of every file
B) `except:  # noqa: E722 - caller validated input; deliberate catch-all`
C) Adding `ignore = ["E722"]` to the project config
D) Deleting the rule from the linter's documentation

**Difficulty:** Easy

---

### Question 6
**What is the output of this code?**
```python
def suppressed_lines(source):
    return {i + 1 for i, line in enumerate(source.splitlines())
            if "# noqa" in line}

src = "x = 1  # noqa\n\ny = 2\n"
print(sorted(suppressed_lines(src)))
```

A) `[1]`
B) `[1, 3]`
C) `[2]`
D) `[]`

**Difficulty:** Easy

---

### Question 7
**What is the primary difference between a linter and a formatter?**

A) A linter is faster than a formatter
B) A linter reports problems; a formatter rewrites the code
C) A formatter only works on Python 3.12+
D) They are the same tool with different names

**Difficulty:** Easy

---

### Question 8
**What is the output of this code?**
```python
def find_bare_excepts(source):
    tree = ast.parse(source)
    return [h.lineno for node in ast.walk(tree)
            if isinstance(node, ast.Try)
            for h in node.handlers if h.type is None]

src = "try:\n    x()\nexcept ValueError:\n    pass\nexcept:\n    pass\n"
print(find_bare_excepts(src))
```

A) `[3]`
B) `[5]`
C) `[3, 5]`
D) `[]`

**Difficulty:** Medium

---

### Question 9
**Which tool would flag this code in a CI pipeline?**
```python
import pickle
model = pickle.load(open("uploaded_model.pkl", "rb"))
```

A) black — the file is not formatted
B) bandit — unpickling untrusted data is a code-execution risk
C) mypy — the return type is unknown
D) pip-audit — pickle is a known vulnerable library

**Difficulty:** Medium

---

### Question 10
**What is the output of this code?**
```python
import ast

def complexity(src):
    tree = ast.parse(src)
    fn = tree.body[0]
    n = 0
    for child in ast.walk(fn):
        if isinstance(child, ast.BoolOp):
            n += len(child.values) - 1
        elif isinstance(child, ast.If):
            n += 1
    return 1 + n

src = "def f(x):\n    if x and y or z:\n        return 1\n    return 0\n"
print(complexity(src))
```

A) 3
B) 4
C) 5
D) 6

**Difficulty:** Hard

---

### Question 11
**Why must `ast.parse` be called only once in a multi-rule linter?**

A) Because `ast.parse` has a side effect on the module namespace
B) Because parsing is O(N) and re-parsing per rule makes the linter O(R*N) for no benefit
C) Because a tree cannot be walked twice
D) Because `ast.parse` deletes the source string

**Difficulty:** Medium

---

### Question 12
**What is the output of this code?**
```python
import ast

def docstring_check(src):
    tree = ast.parse(src)
    return [(n.lineno, n.name) for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef)
            and ast.get_docstring(n) is None]

src = 'def a():\n    """Has a doc."""\n    pass\n\ndef b():\n    pass\n'
print(docstring_check(src))
```

A) `[(1, 'a')]`
B) `[(4, 'b')]`
C) `[(1, 'a'), (4, 'b')]`
D) `[]`

**Difficulty:** Medium

---

### Question 13
**What does mypy catch that a linter cannot?**

A) Style violations like trailing whitespace
B) Type-contract violations, e.g. a function annotated `-> float` returning `None`
C) Mutable default arguments
D) Missing docstrings

**Difficulty:** Easy

---

### Question 14
**What is the output of this code?**
```python
config = {"select": ["B006", "E722", "C901"], "ignore": ["E722"]}
active = set(config["select"]) - set(config["ignore"])
print(sorted(active))
```

A) `['B006', 'C901']`
B) `['B006', 'E722', 'C901']`
C) `['E722']`
D) `[]`

**Difficulty:** Easy

---

### Question 15
**What is the point of pre-commit when CI already runs the gate?**

A) Pre-commit replaces CI entirely
B) Pre-commit runs the checks locally before the commit, so CI only sees clean code
C) Pre-commit is a linter that runs inside the editor
D) Pre-commit only checks commit message formatting

**Difficulty:** Easy

---

### Question 16
**What is the output of this code?**
```python
def gate(source):
    suppressed = {1}
    violations = [(1, "B006"), (2, "E722")]
    return [v for v in violations if v[0] not in suppressed]

print(gate("def f(x=[]):\n    pass\n"))
```

A) `[]`
B) `[(1, 'B006')]`
C) `[(2, 'E722')]`
D) `[(1, 'B006'), (2, 'E722')]`

**Difficulty:** Medium

---

### Question 17
**A teammate proposes `ignore = ["E501"]` project-wide because generated
files exceed the line length. What is the better practice?**

A) Accept it — generated files are not reviewed anyway
B) Use per-file-ignores scoped to the generated files only
C) Increase the line length cap to 500
D) Delete the generated files from the repository

**Difficulty:** Medium

---

### Question 18
**What is the output of this code?**
```python
import ast

def count_decisions(node):
    n = 0
    for child in ast.walk(node):
        if isinstance(child, (ast.For, ast.While)):
            n += 1
    return n

tree = ast.parse("def f():\n    for i in range(3):\n        pass\n    while False:\n        pass\n")
print(1 + count_decisions(tree.body[0]))
```

A) 2
B) 3
C) 4
D) 5

**Difficulty:** Medium

---

### Question 19
**Why does a regex-based Python checker fail where an AST-based one succeeds?**

A) Regexes are slower than AST walks
B) A regex cannot know whether `except:` is real code or text inside a string literal
C) Regexes cannot be compiled on Windows
D) AST walks work only on formatted code

**Difficulty:** Hard

---

### Question 20
**Which sequence of tools is the correct production gate order?**

A) pip-audit → black → mypy → bandit → lint
B) lint → format check → mypy → bandit → pip-audit
C) mypy → lint → pip-audit → black → bandit
D) bandit → mypy → format → lint → pip-audit

**Difficulty:** Hard

---

## Score Tracking
Count your correct answers: _____ / 20

**Scoring Guide:**
- 18-20: Excellent! You can gate a codebase.
- 14-17: Good! Review the rule mechanics you missed.
- 10-13: Fair. Re-read the key concepts sections.
- Below 10: Revisit the lecture and the exercise before the next attempt.

---

## Answer Key

1. **B) Mutable default arguments like `def f(x=[])`** — B006 detects
   defaults that are mutable literals or `list()`/`dict()`/`set()` calls.
   A is E722, C is E501, D is D100 — all real rules, but different codes.

2. **B) It catches `KeyboardInterrupt` and `SystemExit`** — a bare
   `except:` swallows everything, including the signals meant to stop a
   run. A is wrong (bare except is not slow), C is wrong (it catches all
   exceptions, not just network), D is wrong (it is valid syntax, which is
   exactly the problem).

3. **B) `['Constant', 'List']`** — `None` parses to a `Constant` node;
   `[]` parses to a `List` node. A is wrong because the AST has no
   `NoneType` node; C is wrong because `[]` is a literal, not a
   comprehension; D is wrong because `None` is not a `Name`.

4. **C) 3** — complexity = 1 + number of decisions = 1 + 2 `if`s = 3.
   A (1) ignores the branches entirely; B (2) counts only one branch;
   D (4) wrongly counts the `return` statements as decisions.

5. **B) `except: # noqa: E722 - reason`** — coded, scoped, and justified.
   A is blanket suppression (weakest form); C is project-wide disable
   (hides every future case); D is not how rules work.

6. **A) `[1]`** — only line 1 contains `# noqa`. Line 3 (`y = 2`) has no
   comment. B would be right only if line 3 carried a noqa too; C ignores
   that line 1 matches; D misses the match on line 1.

7. **B) A linter reports problems; a formatter rewrites the code** — the
   linter leaves the source untouched. A is false (not the defining
   difference), C is false (formatters are version-agnostic), D is false
   (ruff bundles both, but they are distinct functions).

8. **B) `[5]`** — only the *bare* handler at line 5 fires; the named
   `except ValueError` at line 3 has `h.type` set. A picks the wrong line,
   C lists the named handler too, D misses the bare handler entirely.

9. **B) bandit** — `pickle.load` on an uploaded file executes arbitrary
   code during deserialization; bandit's B301 rule flags it. A is wrong
   (formatting is not the risk), C is wrong (mypy checks types, and the
   real danger is execution), D is wrong (pickle is stdlib, not a CVE'd
   dependency).

10. **B) 4** — the walker counts the BoolOp `x and y or z` (3 values →
    2 points) and one `if` (1 point): n = 3, so 1 + 3 = 4. A (3) forgets
    that a 3-value BoolOp contributes 2 points; C (5) and D (6) overcount
    the branch structure.

11. **B) Parsing is O(N) and re-parsing per rule makes the linter O(R*N)**
    — parse once, then run R cheap walks over the same tree. A is false
    (parse is pure), C is false (trees are reusable), D is false (the
    source string is not consumed).

12. **B) `[(4, 'b')]`** — `a` has a docstring, `b` does not; the AST
    reports `b` at its definition line 4. A points at the wrong function,
    C lists the documented function too, D misses the violation.

13. **B) Type-contract violations** — mypy checks annotations statically;
    returning `None` from a `-> float` function is invisible to lint but
    fatal at runtime. A, C, D are all lint-domain checks.

14. **A) `['B006', 'C901']`** — ignore removes E722 from the selected
    set. B shows the full set before ignore, C shows only the ignored
    rule, D would require ignoring everything.

15. **B) Pre-commit runs the checks locally before the commit** — CI is
    the backstop; pre-commit is the front line. A is false (CI still
    gates merges), C is false (it is a git hook, not an editor plugin),
    D is false (it runs the same checks, not commit-message linting).

16. **C) `[(2, 'E722')]`** — the filter drops violations on suppressed
    line 1, keeping line 2. A drops everything, B keeps the suppressed
    one, D applies no suppression at all.

17. **B) Use per-file-ignores scoped to the generated files** — the rule
    stays on for reviewed code, and generated files are exempted exactly
    where the exemption is needed. A hides future violations in reviewed
    files, C weakens the rule everywhere, D is not a lint solution.

18. **B) 3** — 1 base + 1 `for` + 1 `while` = 3. A (2) counts only one
    loop, C (4) counts the `pass` bodies as decisions, D (5) counts
    `range(3)` as a loop.

19. **B) A regex cannot know whether `except:` is real code or text**
    — the AST distinguishes `Try` nodes from `Constant` string contents;
    a regex pattern matches both. A is a performance myth (regexes can be
    fast but structurally blind), C is false, D is false (ASTs parse any
    valid source).

20. **B) lint → format check → mypy → bandit → pip-audit** — local-first
    order: fast mechanical checks first, then contracts, then security,
    then the slow dependency audit. The other orders either audit before
    linting (slow feedback) or skip a layer's position in the pipeline.
