# Phase 6 — Data Structures & Algorithms (`06-data-structures-algorithms/`)

> **Current:** 20 exercises, 20 lectures, 20 glossaries. **16/20 pass — 4 fail.**
> **Target:** 40 exercises, all self-verifying, with an interview-pattern track.
>
> This section is the module's **best on complexity** (29 lecture files mention
> Big-O) and its **worst on correctness** (4 failures, including a file that hangs
> forever and two with genuine logic bugs).

---

## 1. Current State

| # | File | Status |
|---|---|---|
| 01 | `01-introduction.py` | pass |
| 02 | `02-arrays.py` | pass |
| 03 | `03-stacks.py` | pass |
| 04 | `04-queues.py` | ❌ **R1.1 — hangs forever** (exit 124) |
| 05 | `05-linked-lists.py` | pass |
| 06 | `06-hash-tables.py` | pass |
| 07 | `07-trees.py` | ❌ **R3 — `UnicodeEncodeError`** (box-drawing chars) |
| 08 | `08-binary-trees.py` | ❌ **R1.4 — `list` has no `popleft`** (3 sites) |
| 09 | `09-binary-search-trees.py` | ❌ **R1.3 — `BSTNode` has no `.val`** |
| 10 | `10-avl-trees.py` | pass |
| 11 | `11-graphs.py` | pass |
| 12 | `12-linear-search.py` | pass |
| 13 | `13-binary-search.py` | pass |
| 14 | `14-bubble-sort.py` | pass |
| 15 | `15-selection-sort.py` | pass |
| 16 | `16-insertion-sort.py` | pass |
| 17 | `17-quick-sort.py` | pass |
| 18 | `18-counting-sort.py` | pass |
| 19 | `19-radix-sort.py` | pass |
| 20 | `20-merge-sort.py` | pass |

### 1.1 The irony worth naming in the lectures

Three of the four failures are *themselves* the lessons the section teaches:

- **R1.4** — `08-binary-trees.py` uses `queue = [root]` then `.popleft()`. The fix
  is `deque`. This is exactly the `list`-vs-`deque` cost distinction. `list.pop(0)`
  is O(n); `deque.popleft` is O(1).
- **R1.1** — `04-queues.py` deadlocks because a bounded producer/consumer runs on
  one thread. This is the canonical concurrency bug the file is meant to teach.
- **R1.3** — `09-binary-search-trees.py` mixes two node types (`.val` vs `.data`),
  a type-consistency failure that `assert`s would have caught immediately.

**Use each as a worked "Common Mistake" in its lecture**, with the broken code, the
failure, and the fix. A real bug from your own tree teaches better than a synthetic one.

---

## 2. Gaps

| Gap | Detail |
|---|---|
| No self-verification | **0 of 21** files contain `assert` — which is why 4 broke silently |
| Complexity stated, never measured | Lectures say O(n log n); no file demonstrates the curve empirically |
| No interview patterns | Individual structures taught; the **patterns** that solve problems (two pointers, sliding window, BFS/DFS templates) are absent |
| No dynamic programming | Zero coverage — a standard interview and optimization topic |
| No greedy / backtracking | Absent |
| Missing structures | Tries, heaps as a topic, union-find, segment trees, LRU cache |
| No graph algorithms beyond traversal | No Dijkstra, topological sort, MST, cycle detection |
| No AI-engineering bridge | The retrieval/embedding connection is never drawn |

---

## 3. Fix and Retrofit the Existing 20 (Tier 0 + 1)

### 3.1 The four fixes
Detailed in [10-remediation-backlog.md](10-remediation-backlog.md) R1.1, R1.3, R1.4, R3.
`04-queues.py` (the hang) is the **single highest-priority fix in the whole plan** —
it blocks any CI run over this directory.

### 3.2 `_verify()` for all 20

DSA is the easiest section to assert well, because correctness is unambiguous:

```python
def _verify() -> None:
    # 1. Correctness against a known-good reference
    data = [5, 2, 9, 1, 5, 6]
    assert quick_sort(data.copy()) == sorted(data), "quick_sort must match sorted()"

    # 2. Edge cases — where real bugs live
    assert quick_sort([]) == [], "empty input"
    assert quick_sort([1]) == [1], "single element"
    assert quick_sort([2, 2, 2]) == [2, 2, 2], "all duplicates"
    assert quick_sort([3, 2, 1]) == [1, 2, 3], "reverse-sorted (worst case)"

    # 3. Structural invariants
    bst = BST()
    for v in [50, 30, 70, 20, 40]:
        bst.insert(v)
    assert bst.in_order() == sorted([50, 30, 70, 20, 40]), \
        "BST in-order traversal must yield sorted output"

    # 4. Property-based: random inputs, invariant must hold
    import random
    rng = random.Random(42)
    for _ in range(100):
        arr = [rng.randint(-50, 50) for _ in range(rng.randint(0, 30))]
        assert merge_sort(arr.copy()) == sorted(arr), f"failed on {arr}"

    print("[OK] all checks passed")
```

The property-based loop is worth emphasizing: 100 random arrays with a fixed seed
would have caught the `.val`/`.data` bug on the first run.

### 3.3 Add empirical complexity demonstration

Lectures assert O(n log n) but nothing shows it. Add a measured growth table per
algorithm — printed, never asserted on time:

```python
# Operation counts (deterministic — safe to assert), not wall-clock
for n in (100, 1_000, 10_000):
    comparisons = count_comparisons(bubble_sort, make_input(n))
    print(f"n={n:>6}  comparisons={comparisons:>12,}  n^2={n**2:>12,}")
# Assert the *shape*: quadratic growth ~100x when n grows 10x
assert 50 < c_10000 / c_1000 < 200, "bubble sort must show quadratic growth"
```

Counting operations instead of timing makes complexity **verifiable in CI** — the
right way to teach cost.

### 3.4 Add AI relevance to all 20 lectures

| Structure/Algorithm | AI-engineering use |
|---|---|
| Hash tables | Token→ID vocab; dedup document IDs; embedding cache keys |
| Heaps | **Top-k retrieval** — `heapq.nlargest(k)` is O(n log k) vs `sorted()[:k]` O(n log n) |
| Binary search | `bisect` on a sorted score list; finding a threshold; quantile lookup |
| BSTs / balanced trees | Ordered index structures; range queries over metadata |
| Graphs + BFS/DFS | Knowledge graphs; agent tool dependency resolution; document link traversal |
| Sorting | Reranking candidates; stable sort for tie-breaking by score |
| Linked lists | LRU cache internals (with a hash map) — the standard cache design |
| Tries | Prefix search; autocomplete; tokenizer vocabularies |
| Union-find | Clustering near-duplicate documents |

---

## 4. New Topics 21–40

### 4.1 Missing structures (21–26)

| # | Topic | Concepts |
|---|---|---|
| 21 | `21-heaps-and-priority-queues.py` | Binary heap invariant; sift up/down; `heapify` is O(n) not O(n log n); `heapq` API; **top-k as the canonical use**; k-way merge; median maintenance with two heaps |
| 22 | `22-tries.py` | Prefix tree; insert/search/`starts_with`; space vs time; compressed tries; autocomplete; **tokenizer vocabularies** |
| 23 | `23-union-find.py` | Disjoint set; union by rank; path compression; near-O(1) amortized; connected components; **near-duplicate clustering** |
| 24 | `24-lru-cache.py` | Hash map + doubly linked list; O(1) get/put; `OrderedDict` shortcut; `functools.lru_cache` internals; LFU contrast; **embedding cache design** |
| 25 | `25-bloom-filters.py` | Probabilistic membership; false positives (never false negatives); sizing and hash count; **dedup at scale before hitting the DB**; Count-Min Sketch |
| 26 | `26-segment-and-fenwick-trees.py` | Range queries; point updates; O(log n) both; prefix sums; when a simple prefix array suffices |

### 4.2 Graph algorithms (27–30)

| # | Topic | Concepts |
|---|---|---|
| 27 | `27-graph-representations.py` | Adjacency list vs matrix — space/time tradeoff; weighted, directed; edge lists; when each fits |
| 28 | `28-shortest-paths.py` | Dijkstra with a heap; Bellman-Ford (negative weights); A* with heuristics; BFS as unweighted shortest path |
| 29 | `29-topological-sort.py` | Kahn's algorithm; DFS-based; cycle detection; **task/tool dependency resolution**; DAG scheduling |
| 30 | `30-mst-and-connectivity.py` | Kruskal (with union-find), Prim; bridges and articulation points; strongly connected components |

### 4.3 Algorithmic paradigms (31–34)

| # | Topic | Concepts |
|---|---|---|
| 31 | `31-dynamic-programming.py` ⭐ | Memoization vs tabulation; optimal substructure; overlapping subproblems; 1-D and 2-D; space optimization; classics (LCS, knapsack, edit distance); **edit distance for fuzzy matching** |
| 32 | `32-greedy-algorithms.py` | Greedy-choice property; when greedy is provably optimal and when it fails; interval scheduling; Huffman coding; proof sketches |
| 33 | `33-backtracking.py` | Systematic search; pruning; N-queens, subsets, permutations, sudoku; complexity of search trees; constraint propagation |
| 34 | `34-divide-and-conquer.py` | Recurrences and the Master Theorem; merge/quick revisited; binary-search variants; closest pair; matrix multiplication |

### 4.4 Interview patterns (35–40) ⭐

This is the missing layer: individual structures are taught, but the *patterns* that
actually solve problems are not. This track is what makes someone interview-ready.

| # | Topic | Concepts |
|---|---|---|
| 35 | `35-two-pointers.py` | Opposite ends; same direction; fast/slow (cycle detection); partitioning; sorted-array pairs; in-place dedup |
| 36 | `36-sliding-window.py` | Fixed and variable windows; window invariants; longest/shortest substring problems; **streaming context windows** |
| 37 | `37-prefix-sums-and-hashing.py` | Prefix sums; difference arrays; subarray-sum with a hash map; 2-D prefix sums; rolling hash |
| 38 | `38-tree-and-graph-patterns.py` | DFS/BFS templates; recursion vs explicit stack; level-order; path problems; lowest common ancestor; serialize/deserialize |
| 39 | `39-complexity-analysis-deep.py` | Amortized analysis (why `list.append` is O(1)); space complexity including recursion stack; best/average/worst; **how to estimate before coding** |
| 40 | `40-problem-solving-framework.py` | UMPIRE method; clarifying constraints; brute force → optimize; pattern recognition; **communicating while coding**; testing your own solution |

---

## 5. Deliverables

| Item | Count |
|---|---|
| Fixes (R1.1, R1.3, R1.4, R3) | 4 |
| `_verify()` retrofits | 20 |
| Empirical complexity demos | 20 |
| AI-relevance retrofits | 20 |
| New topics `21`–`40` | 20 |
| New lecture+glossary pairs | 40 |
| Challenges | 40 dirs × 3 tiers |
| Quizzes | 20 (7 exist) |
| Interview guides | 8 (7 exist) |

---

## 6. Sequencing

| Step | Work | Notes |
|---|---|---|
| 1 | **Fix R1.1 (hang)** | Blocks CI over the directory — do first |
| 2 | Fix R1.3, R1.4, R3 | Logic + encoding |
| 3 | `_verify()` in 20 files, with property-based loops | Would have caught steps 1–2 |
| 4 | Empirical complexity + AI relevance | Parallelizable |
| 5 | `21`–`26` (structures) | `21-heaps` and `24-lru-cache` first — direct AI use |
| 6 | `27`–`30` (graphs) | After `21` (Dijkstra needs heaps) |
| 7 | `31`–`34` (paradigms) | Independent |
| 8 | `35`–`40` (patterns) | Best done last — synthesizes everything |
| 9 | Challenges + quizzes | After exercises |

---

## 7. Exit Criteria

- [ ] Zero failures (from 4); nothing hangs
- [ ] 40 exercises, each with `_verify()` including edge cases and a property-based loop
- [ ] Complexity claims **demonstrated by operation counts**, not just asserted in prose
- [ ] Every lecture connects its structure to a retrieval/serving/ML use
- [ ] DP, greedy, and backtracking covered
- [ ] Interview-pattern track complete (`35`–`40`)
- [ ] Heaps, tries, union-find, LRU, Bloom filters present
- [ ] The three self-referential bugs (R1.1, R1.3, R1.4) documented as worked mistakes in their lectures

---

*Phase 6 of [00-MASTER-PLAN.md](00-MASTER-PLAN.md). Fixes: [10-remediation-backlog.md](10-remediation-backlog.md) R1.1/R1.3/R1.4/R3.*
