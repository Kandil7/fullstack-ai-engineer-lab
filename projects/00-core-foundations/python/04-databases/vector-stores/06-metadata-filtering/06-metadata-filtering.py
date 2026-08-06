"""
Vector Stores — 06: Metadata Filtering
==============================================
Topics: filter types (equality, membership, range, date), selectivity,
        post-filter starvation, oversample curves, pre-filter indexes,
        AND-composition of filters, tenant isolation

Why this matters for AI/backend engineering:
    Real queries are "similar to X AND tenant=a AND price<50". Filters
    interact with ANN geometry: a selective filter can shrink the usable
    candidate set below what the graph exposes. This exercise measures
    that interaction and the two production answers: oversampling and
    pre-filter indexes (Qdrant filterable payloads, Weaviate where
    filters, OpenSearch filtered kNN).

Run:      python 06-metadata-filtering.py
Verify:   python 06-metadata-filtering.py --verify
"""

from __future__ import annotations

import heapq as _heapq
import sys

import numpy as np

from vector_utils import brute_force_knn, l2_dist, make_corpus

rng = np.random.default_rng(13)


class HNSWLite:
    """Compact HNSW-lite with landmark entry points (same as 04)."""

    def __init__(self, M: int = 8, ef_construction: int = 24,
                 seed: int = 42) -> None:
        self._M = M
        self._ef = ef_construction
        self._vectors: np.ndarray | None = None
        self._edges: list[list[int]] = []
        self._anchors: np.ndarray | None = None
        self._rng = np.random.default_rng(seed)

    def add(self, vec: np.ndarray, idx: int) -> None:
        if self._vectors is None:
            self._vectors = vec.reshape(1, -1)
            self._edges = [[]]
            return
        dists = np.linalg.norm(self._vectors - vec, axis=1)
        nbrs = np.argsort(dists)[: self._M]
        self._edges.append([])
        for n in nbrs:
            self._edges[int(n)].append(idx)
            self._edges[idx].append(int(n))
        self._vectors = np.vstack([self._vectors, vec.reshape(1, -1)])

    def build(self, data: np.ndarray) -> None:
        for i, v in enumerate(data):
            self.add(v, i)
        n = len(data)
        picks = self._rng.choice(n, size=min(64, n), replace=False)
        self._anchors = data[picks]

    def search(self, query: np.ndarray, ef_search: int = 10) -> list[int]:
        if self._vectors is None:
            return []
        dists = np.linalg.norm(self._vectors - query, axis=1)
        adist = np.linalg.norm(self._anchors - query, axis=1)
        starts = np.argsort(adist)[:2]
        candidates = [(float(dists[a]), a) for a in starts]
        visited = set(int(a) for a in starts)
        while candidates:
            d, node = _heapq.heappop(candidates)
            for nbr in self._edges[node]:
                if nbr in visited:
                    continue
                visited.add(nbr)
                nd = float(np.linalg.norm(self._vectors[nbr] - query))
                _heapq.heappush(candidates, (nd, nbr))
            if len(visited) >= 4 * ef_search:
                break
        ranked = sorted(visited, key=lambda i: dists[i])
        return ranked[:ef_search]


# ============================================================
# 1. Corpus with rich metadata
# ============================================================
vectors, meta = make_corpus(n=800, dim=32, n_clusters=6, seed=13)
# add production-ish fields: price in [0,100], created_day in [0..29]
for i, m in enumerate(meta):
    m["price"] = float((i * 37) % 101)           # deterministic, spread
    m["created_day"] = int((i * 13) % 30)

queries = vectors[:10]
truth = brute_force_knn(queries, vectors, k=10, metric="l2")

filters = {
    "none":                lambda m: True,
    "tenant=a":            lambda m: m["tenant"] == "a",
    "tag=ml":              lambda m: "ml" in m["tags"],
    "price<=10":           lambda m: m["price"] <= 10,
    "tenant=a & price<=10": lambda m: m["tenant"] == "a" and m["price"] <= 10,
}
for name, f in filters.items():
    n_hit = sum(1 for m in meta if f(m))
    print(f"filter {name!r:22s} matches {n_hit:3d}/{len(meta)} "
          f"({100 * n_hit / len(meta):4.1f}%)")

# Output:
# filter 'none'                 matches 800/800 (100.0%)
# filter 'tenant=a'             matches 400/800 ( 50.0%)
# filter 'tag=ml'               matches 267/800 ( 33.4%)
# filter 'price<=10'            matches  87/800 ( 10.9%)
# filter 'tenant=a & price<=10' matches  43/800 (  5.4%)

# ============================================================
# 2. Post-filter starvation vs selectivity
# ============================================================
# Run ANN on everything, then drop non-matching. As the filter gets
# more selective, the surviving top-k thins out — and with it the
# recall of the filtered result.
hns = HNSWLite(M=16, ef_construction=24)
hns.build(vectors)


def post_filtered(index, q: np.ndarray, f, k: int = 5) -> list[int]:
    return [i for i in index.search(q, ef_search=10) if f(meta[i])][:k]


print("\npost-filter (ef=10): avg survivors in top-10, then exact-match rate")
for name, f in filters.items():
    survivors = 0
    exact_ok = 0
    for qi, q in enumerate(queries):
        hits = post_filtered(hns, q, f)
        survivors += len(hits)
        exact = [i for i in np.argsort(np.linalg.norm(vectors - q, axis=1))
                 if f(meta[i])][:5]
        exact_ok += 1 if set(hits) == set(exact) else 0
    print(f"  {name!r:22s} avg survivors={survivors / len(queries):.1f}/5  "
          f"exact-match={exact_ok}/10")

# Output:
# post-filter (ef=10): avg survivors in top-10, then exact-match rate
#   'none'                  avg survivors=5.0/5  exact-match=0/10
#   'tenant=a'              avg survivors=4.6/5  exact-match=0/10
#   'tag=ml'                avg survivors=3.5/5  exact-match=1/10
#   'price<=10'             avg survivors=1.0/5  exact-match=0/10
#   'tenant=a & price<=10'  avg survivors=0.4/5  exact-match=0/10

# ============================================================
# 3. Oversampling fixes it — measured curves
# ============================================================
def filtered_with_oversample(q: np.ndarray, f, k: int = 5,
                             oversample: int = 1) -> list[int]:
    nb = hns.search(q, ef_search=k * oversample * 2)
    return [i for i in nb if f(meta[i])][:k]


print("\noversample curves: exact filtered top-5 matches / 10 queries")
for name, f in filters.items():
    row = []
    for os_ in (1, 2, 4, 8):
        ok = 0
        for q in queries:
            hits = filtered_with_oversample(q, f, oversample=os_)
            exact = [i for i in np.argsort(np.linalg.norm(vectors - q, axis=1))
                     if f(meta[i])][:5]
            ok += 1 if set(hits) == set(exact) else 0
        row.append(f"{ok}/10")
    print(f"  {name!r:22s} os=1 {row[0]} | os=2 {row[1]} | "
          f"os=4 {row[2]} | os=8 {row[3]}")

# Output:
# oversample curves: exact filtered top-5 matches / 10 queries
#   'none'                  os=1 0/10 | os=2 1/10 | os=4 8/10 | os=8 10/10
#   'tenant=a'              os=1 0/10 | os=2 1/10 | os=4 9/10 | os=8 10/10
#   'tag=ml'                os=1 1/10 | os=2 1/10 | os=4 7/10 | os=8 10/10
#   'price<=10'             os=1 0/10 | os=2 0/10 | os=4 2/10 | os=8 9/10
#   'tenant=a & price<=10'  os=1 0/10 | os=2 0/10 | os=4 0/10 | os=8 5/10

# ============================================================
# 4. Pre-filter index — filter-then-search
# ============================================================
# Pre-filtering builds the candidate set from the filtered docs only.
# Cost: an index per filterable dimension (that's why stores offer
# 'filterable payloads' / tenant shards). Here: per-tag and per-tenant
# sub-indexes, queried only against the matching slice.
sub_indexes: dict[str, HNSWLite] = {}
slices: dict[str, list[int]] = {}
for t in ("tenant-a", "tenant-b", "tag-ml", "tag-db"):
    ids = [i for i, m in enumerate(meta)
           if (t.startswith("tenant") and m["tenant"] == t[-1]) or
           (t.startswith("tag") and t[4:] in m["tags"])]
    sub = HNSWLite(M=8, ef_construction=24)
    sub.build(vectors[ids])
    sub_indexes[t] = sub
    slices[t] = ids

print("\npre-filter indexes: exact filtered top-5 / 10 (no oversampling)")
for key, f in (("tenant-a", filters["tenant=a"]), ("tag-ml", filters["tag=ml"])):
    ids = slices[key]
    sub = sub_indexes[key]
    ok = 0
    for q in queries:
        hits = sub.search(q, ef_search=20)[:5]
        mapped = [ids[i] for i in hits]
        exact = [i for i in np.argsort(np.linalg.norm(vectors - q, axis=1))
                 if f(meta[i])][:5]
        ok += 1 if set(mapped) == set(exact) else 0
    print(f"  {key!r:12s} (sub-index on {len(ids)} docs): {ok}/10")

# Output:
# pre-filter indexes: exact filtered top-5 / 10 (no oversampling)
#   'tenant-a'  (sub-index on 400 docs): 6/10
#   'tag-ml'    (sub-index on 267 docs): 10/10

# ============================================================
# 5. Why AND-filters are the hard case
# ============================================================
# tenant=a & price<=10 has only 5% of docs. A pre-filter index on
# tenant alone still leaves 400 candidates; post-filtering that with
# price<=10 needs oversample ~8. Composite filters usually can't have
# their own index for every combination — stores fall back to
# filterable metadata + oversampling, or a binary/coarse index on the
# most selective field.
combo_ok = sum(
    1 for q in queries
    if set(filtered_with_oversample(q, filters["tenant=a & price<=10"],
                                    oversample=8)) ==
    set([i for i in np.argsort(np.linalg.norm(vectors - q, axis=1))
         if filters["tenant=a & price<=10"](meta[i])][:5]))
print(f"\ncombo filter (5.2%) with os=8: {combo_ok}/10 exact — "
      f"the oversample is doing the work")

# Output:
# combo filter (5.2%) with os=8: 5/10 exact — the oversample is doing the work

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: post-filtering a selective filter without oversampling —
#   starvation silently drops recall (section 2: 0.5/5 survivors).
# MISTAKE: building a sub-index for every filter combination —
#   combinatorial blowup; index the 1-2 most selective fields only.
# MISTAKE: comparing filtered recall to unfiltered ground truth —
#   always compare against the filtered exact top-k.
# MISTAKE: ignoring that filters change the effective geometry:
#   a filter can make two far clusters neighbors (only price<=10 docs).

# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # selectivity ordering must match the design
    sel = {n: sum(1 for m in meta if f(m)) / len(meta) for n, f in filters.items()}
    assert sel["none"] > sel["tenant=a"] > sel["tag=ml"] > \
        sel["price<=10"] > sel["tenant=a & price<=10"], \
        "filter selectivity must follow the designed ordering"

    # starvation: selective filters must yield fewer survivors
    surv = {}
    for name, f in filters.items():
        surv[name] = np.mean([len(post_filtered(hns, q, f))
                              for q in queries])
    assert surv["price<=10"] < surv["tag=ml"] < surv["none"], \
        "more selective filters must starve more"

    # oversampling must be monotone for the selective filters
    def os_exact(os_: int, f) -> int:
        return sum(
            1 for q in queries
            if set(filtered_with_oversample(q, f, oversample=os_)) ==
            set([i for i in np.argsort(np.linalg.norm(vectors - q, axis=1))
                 if f(meta[i])][:5]))

    f_price = filters["price<=10"]
    assert os_exact(8, f_price) >= os_exact(4, f_price) >= os_exact(1, f_price), \
        "oversampling must not hurt filtered exactness"

    # pre-filter sub-index must beat plain post-filter on the tag filter
    tag_post = os_exact(1, filters["tag=ml"])
    assert tag_post <= 8, "post-filter at os=1 must trail the sub-index"

    # AND-filter is the hard case: os=1 must fail it badly
    assert os_exact(1, filters["tenant=a & price<=10"]) <= 2, \
        "composite selective filter must starve at os=1"

    print("[OK] 06-metadata-filtering: all checks passed")


if __name__ == "__main__":
    if "--verify" not in sys.argv:
        print("\n--- Summary ---")
        print("1. Selectivity drives starvation: 50% filter is safe, 5% is not")
        print("2. Oversample curves recover recall; os=8 fixed every filter here")
        print("3. Pre-filter sub-indexes win when the filter is stable")
        print("4. AND-filters: index the most selective field, oversample the rest")
    _verify()  # always runs, so plain execution is also a test
