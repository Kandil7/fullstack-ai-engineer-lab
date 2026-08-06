"""
01-core-python — 49: Collections Toolkit — The Workhorses of Retrieval
======================================================================
Topics: deque (O(1) both ends, maxlen ring buffer), heapq (heappush/heappop/
        nlargest), bisect (bisect_left/insort, sorted-list maintenance),
        Counter (most_common), defaultdict, ChainMap

Why this matters for AI/backend engineering:
    heapq.nlargest(k, ...) IS top-k retrieval. deque(maxlen=n) is a sliding
    conversation window for a chat model. bisect maintains a sorted score list
    in O(log n). Counter aggregates token frequencies. These four stdlib tools
    replace half of what people reach for numpy or redis for.

Run:      python 49-collections-toolkit.py
Verify:   python 49-collections-toolkit.py --verify
Reference: https://docs.python.org/3/library/collections.html
"""

from __future__ import annotations

import bisect
import heapq
import sys
from collections import ChainMap, Counter, defaultdict, deque

# ============================================================
# 1. deque — O(1) Append/Pop at Both Ends
# ============================================================
# Complexity: append/appendleft/pop/popleft all O(1). list.insert(0, x) is
# O(n) — deque.appendleft is the cheaper alternative for a front-insert pattern.

# Example 1: ring buffer for a sliding window
recent = deque(maxlen=3)
for t in ["q1", "q2", "q3", "q4"]:
    recent.append(t)
print(f"Sliding window (maxlen=3): {list(recent)}")

# Example 2: popleft for FIFO queue (BFS-style processing)
jobs = deque(["a", "b", "c"])
print(f"Next job: {jobs.popleft()}, remaining: {list(jobs)}")

# Output:
# Sliding window (maxlen=3): ['q2', 'q3', 'q4']
# Next job: a, remaining: ['b', 'c']

# ============================================================
# 2. heapq — Priority Queue / Top-K
# ============================================================
# Complexity: heappush/heappop O(log n), heapify O(n), nlargest/nsmallest
# O(n log k). sorted(items)[:k] is O(n log n); heapq.nlargest is O(n log k).
# At n=1e6, k=10, that difference is the one that matters.

# Example 3: top-k retrieval with nlargest
scores = [0.1, 0.9, 0.4, 0.8, 0.3, 0.7, 0.2, 0.6]
top3 = heapq.nlargest(3, scores)
print(f"\nTop-3 scores: {top3}")

# Example 4: priority queue (smallest first)
pq: list[tuple[int, str]] = []
heapq.heappush(pq, (3, "embedding job"))
heapq.heappush(pq, (1, "health check"))
heapq.heappush(pq, (2, "rerank job"))
while pq:
    print(f"  run: {heapq.heappop(pq)[1]}")

# Output:
# Top-3 scores: [0.9, 0.8, 0.7]
#   run: health check
#   run: rerank job
#   run: embedding job

# ============================================================
# 3. bisect — Maintain a Sorted List in O(log n)
# ============================================================
# Complexity: bisect_left/bisect_right O(log n) comparisons; insort O(n) due
# to the list shift, but the search is O(log n). Use when reads vastly
# outnumber writes — otherwise a heap or sorted container is better.

# Example 5: insertion point and duplicate handling
data = [1, 3, 5, 7, 7, 9]
print(f"\nbisect_left(7)  -> {bisect.bisect_left(data, 7)}  (first 7)")
print(f"bisect_right(7) -> {bisect.bisect_right(data, 7)}  (after last 7)")

# Example 6: insort keeps the list sorted
xs: list[int] = [10, 20, 40]
bisect.insort(xs, 30)
print(f"After insort(30): {xs}")

# Output:
# bisect_left(7)  -> 3  (first 7)
# bisect_right(7) -> 5  (after last 7)
# After insort(30): [10, 20, 30, 40]

# ============================================================
# 4. Counter — Frequency Tables
# ============================================================
# Complexity: Counter(iterable) is O(n); most_common(k) is O(n log k).
# Counter also has a built-in + operator for merging counts.

# Example 7: token frequency + top-k
tokens = ["the", "cat", "the", "dog", "the", "cat"]
freq = Counter(tokens)
print(f"\nToken counts: {dict(freq)}")
print(f"Top-2: {freq.most_common(2)}")

# Example 8: merging counters across shards
shard_a = Counter(a=3, b=1)
shard_b = Counter(a=2, c=4)
print(f"Merged: {dict(shard_a + shard_b)}")

# Output:
# Token counts: {'the': 3, 'cat': 2, 'dog': 1}
# Top-2: [('the', 3), ('cat', 2)]
# Merged: {'a': 5, 'b': 1, 'c': 4}

# ============================================================
# 5. defaultdict — Auto-Initialized Values
# ============================================================
# Avoids the get/setdefault dance. The factory runs on missing keys only —
# it does NOT add the key on plain reads via __getitem__.

# Example 9: grouping with defaultdict(list)
groups = defaultdict(list)
for word in ["cat", "car", "dog", "door"]:
    groups[word[0]].append(word)
print(f"\nBy first letter: {dict(groups)}")

# ============================================================
# 6. ChainMap — Layered Lookups
# ============================================================
# Looks up keys through a stack of dicts; first hit wins. Perfect for
# layered config: overrides -> env -> defaults.

# Example 10: config precedence
defaults = {"lr": 1e-3, "seed": 0, "gpu": False}
env = {"gpu": True}
overrides = {"lr": 1e-4}
config = ChainMap(overrides, env, defaults)
print(f"\nChainMap lr={config['lr']} gpu={config['gpu']} seed={config['seed']}")

# Output:
# By first letter: {'c': ['cat', 'car'], 'd': ['dog', 'door']}
# ChainMap lr=0.0001 gpu=True seed=0

# ============================================================
# 7. Production Pattern — Hybrid Top-K Retrieval
# ============================================================
# Combine the toolkit: heapq for top-k, deque for a context window, Counter
# for query term frequency.

def top_k_by_score(docs: dict[str, float], k: int) -> list[tuple[str, float]]:
    """Return the k highest-scoring documents, ties broken stably."""
    if k <= 0:
        return []
    return heapq.nlargest(k, docs.items(), key=lambda item: item[1])


docs = {"doc_a": 0.85, "doc_b": 0.91, "doc_c": 0.78, "doc_d": 0.91}
print(f"\nTop-2 docs: {top_k_by_score(docs, 2)}")

# Output:
# Top-2 docs: [('doc_b', 0.91), ('doc_d', 0.91)]

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: list for a front-insert / sliding-window pattern
#   bad = [x] + items  or  items.insert(0, x)   # O(n) every time
# CORRECT:
#   good = deque(items, maxlen=64); good.appendleft(x)  # O(1)

# MISTAKE: sorted() for top-k
#   bad = sorted(scores, reverse=True)[:10]     # O(n log n) even for k=10
# CORRECT:
#   good = heapq.nlargest(10, scores)           # O(n log k)

# MISTAKE: defaultdict read creates keys by accident
#   d = defaultdict(list); len(d["missing"]) -> 0 AND d now has "missing"
# CORRECT:
#   good = use d.get("missing") if you only want to read

# MISTAKE: treating a heap as a sorted list (heap[0] is min, rest unordered)
#   bad = pq[1]  # not necessarily the second smallest
# CORRECT:
#   good = heapq.nsmallest(2, pq)

# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    # deque ring buffer evicts oldest
    d = deque(maxlen=3)
    for x in [1, 2, 3, 4]:
        d.append(x)
    assert list(d) == [2, 3, 4], "maxlen deque must evict the oldest"

    # popleft is FIFO
    q = deque(["a", "b"])
    assert q.popleft() == "a" and list(q) == ["b"]

    # heapq yields sorted order
    h: list[int] = []
    for x in [5, 1, 3]:
        heapq.heappush(h, x)
    assert [heapq.heappop(h) for _ in range(3)] == [1, 3, 5], \
        "heappop must return ascending order"

    # nlargest returns top-k
    assert heapq.nlargest(3, [0.1, 0.9, 0.4, 0.8]) == [0.9, 0.8, 0.4]

    # bisect on duplicates
    data = [1, 3, 5, 7, 7, 9]
    assert bisect.bisect_left(data, 7) == 3, "bisect_left -> first occurrence"
    assert bisect.bisect_right(data, 7) == 5, "bisect_right -> past last"
    xs = [10, 20, 40]
    bisect.insort(xs, 30)
    assert xs == [10, 20, 30, 40], "insort must keep the list sorted"

    # Counter
    freq = Counter(["a", "b", "a"])
    assert freq.most_common(1) == [("a", 2)], "most_common counts correctly"
    assert Counter(a=1) + Counter(a=1) == Counter(a=2), "counter merge"

    # defaultdict grouping
    g = defaultdict(list)
    g["c"].append(1)
    assert g["c"] == [1] and g["x"] == [], "factory runs on missing key"

    # ChainMap precedence: leftmost wins
    cfg = ChainMap({"lr": 1}, {"lr": 2, "seed": 5})
    assert cfg["lr"] == 1 and cfg["seed"] == 5, "leftmost dict wins"

    # Production top-k
    assert top_k_by_score(docs, 2)[0][0] == "doc_b", "top-k by score"

    # Degenerate top-k
    assert top_k_by_score(docs, 0) == [], "k<=0 must return empty"

    print("[OK] 49-collections-toolkit: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. deque: O(1) both ends; maxlen = sliding window")
        print("2. heapq.nlargest: O(n log k) top-k retrieval")
        print("3. bisect: O(log n) search in a sorted list")
        print("4. Counter.most_common: token frequency in one line")
        print("5. ChainMap: layered config with first-hit-wins")
        _verify()
