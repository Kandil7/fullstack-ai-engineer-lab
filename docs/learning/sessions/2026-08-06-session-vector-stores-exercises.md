# Vector Stores sub-project: 8 verified exercises + corpus fixes

### Context

Fullstack AI Engineer Lab, phase-4 databases. Building the vector-stores topic set (8 exercises) inside projects/00-core-foundations/python/04-databases/vector-stores/, per the mastery plan 05-phase-4-databases.md and content standards. Environment: numpy only (no faiss at runtime), deterministic seeds, no wall-clock asserts.

### Explanation

Completed and verified all 8 vector-store exercises: 01-vector-search-fundamentals, 02-ann-algorithms (HNSW-lite, IVF, PQ, LSH implemented in numpy), 03-exact-knn (argpartition vs sort, L2 vs cosine), 04-indexing-strategies (M/ef sweeps, memory ladder, quantization ladder, pre/post-filter, drift), 05-hybrid-search (BM25 vs dense, RRF, min-max blending, alpha sweep), 06-metadata-filtering (selectivity, starvation, oversample curves, sub-indexes), 07-chunking-retrieval (recall@1 vs recall@3, seams, size sweep), 08-cosine-similarity (magnitude-blindness, unit identity, concentration curse). Every file ends with a _verify() of >=5 asserts, prints exactly [OK] NN-name: all checks passed, exit 0.

Key engineering lessons learned while building:
1. Synthetic corpus metadata must NOT align with cluster structure: tenant = i%2 and tags = (i*7+len(t))%3 are constant within each cluster (i%6), making filters degenerate (all-or-nothing per cluster). Fixed: tenant = (i//2)%2, tags = (i%3 + i//6 + len(t))%3.
2. Single-layer HNSW-lite with fixed entry point (node 0) strands the beam in the first cluster; landmark entry points (nearest of 64 anchors, multi-start at 2) fix multi-cluster recall.
3. Dense graphs (high M) need bigger ef budgets; at fixed moderate ef, low-M graphs can out-recall high-M graphs — the sweep lesson: hold M fixed, sweep ef; then sweep M at generous ef (shows saturation at small n).
4. Bag-of-words hash embeddings make sparse and dense arms agree almost always; genuine disagreement needs idf-vs-count design (rare token 'e503' vs common 'cache'). 'e503 cache latency' and 'error latency' split the arms cleanly.
5. Retrieval eval must be number-aware: checking for the phrase 'requests per minute' in the top chunk passes when ANY chunk contains it; must check for the unique answer token. recall@3 (top-k, what the LLM sees) is the honest RAG metric; recall@1 is strict.
6. Fixed-size chunking without overlap cuts sentences; overlap or sentence/recursive chunking recovers seam answers. Chunk-size sweep shows fragmentation (too small) vs dilution (too big).

### Alternatives

1. Use faiss/sklearn at runtime instead of numpy stand-ins — rejected: no server/GPU deps, must run anywhere, and implementing HNSW/IVF/PQ in numpy is itself the pedagogy. 2. Keep one shared HNSW implementation in a module vs copying per exercise — copied compactly per file so each exercise runs standalone (imports only vector_utils). 3. Fix the tag/tenant formulas vs building filters in exercises from scratch — fixing in vector_utils keeps all exercises consistent.

### Rationale (Why this?)

The corpus fixes matter beyond this sub-project: any future exercise using make_corpus metadata (filters, tenants, tags) now gets within-cluster variation, which is the only regime where filtering demos are meaningful. The metric lesson (number-aware, recall@3) applies to any retrieval eval.

### Exercises

1. Run `python 08-cosine-similarity.py --verify` and explain why L2(a,c)=33.67 while cosine=1.00. 2. In 04, change HNSWLite M to 32 and re-run the ef sweep — explain why the curve shape changes. 3. In 06, add a filter 'price>=90' and predict its oversample curve before running. 4. In 05, add a query with a brand-new rare token and predict which arm wins. 5. In 07, switch the sweep to sentence chunking and compare pick sizes.

### Next Steps

Next: write Redis lectures + glossaries + challenges (8 topics), MongoDB _verify() retrofit + 12-mongo-vs-sql, vector-store lectures/glossaries/challenges, then the 3 quizzes, then full pytest run of all challenge directories.

---
