# Phase 2 Topics 21-27: Concurrency Comparison, Asyncio Advanced, Typing, Memory/GC, Profiling, Patterns, Packaging — REPORT

### Context

Session in fullstack-ai-engineer-lab/projects/00-core-foundations/python: completed Phase 2 Advanced Python topics 21-27 (7 topics x 5 artifacts = 35 files) per admin/mastery-plan/01-content-standards.md and 03-phase-2-advanced-python.md. The 7 exercise scripts (21-27) already existed and passed; this session wrote the remaining 28 files: 7 lectures, 7 glossaries, 7 challenge sets (README/starter/solution/test), 7 quizzes, fixed one quiz defect, and indexed everything in both section READMEs.

### Explanation

Per-topic artifacts delivered (all in projects/00-core-foundations/python/):

- 21-concurrency-comparison (marked highest value): exercise measures FIO seq 0.517s / threads 0.074s / processes 0.401s / async 0.014s at 50x0.01s and CPU 24M seq 1.660s / threads 1.576s / processes 0.750s; lecture reuses these numbers so text and code match exactly. Challenge tiers: Bronze choose_model (I/O vs CPU + GIL), Silver run_io_overlap (ThreadPoolExecutor), Gold run_cpu_parallel with module-level _cpu_worker (Windows spawn-safe).
- 22-asyncio-advanced: Bronze run_limited (Semaphore peak), Silver bounded-queue pipeline, Gold TaskGroup fail_counts with STAGGERED delays (i<fail_at 0.005s, i==fail_at 0.02s, i>fail_at 5s) so cancellation is deterministic. Glossary: asyncio.timeout, CancelledError, shield, TaskGroup, to_thread, backpressure.
- 23-typing-advanced: Bronze build_schema via get_type_hints (resolves string annotations), Silver signature_matches (inspect.signature), Gold Retriever Protocol + verify_retriever + safe_search + Result (runtime_checkable for isinstance; Qdrant/Chroma/WrongSignature fakes).
- 24-memory-and-gc: Bronze collect_cycle (index-based loop so the loop variable does not keep the last node alive), Silver slots_ratio (__dict__ counted in non-slots size), Gold weak_cache_trap + sum_materialized/sum_streamed tracemalloc peaks (495 KB vs 90 KB).
- 25-profiling-and-optimization: Bronze dedup_chunks (set-based O(n) vs naive O(n^2) shown in comments), Silver hash_join (40k rows, ~1810x), Gold fib_stats (iterative 27 calls, 0.3s vs naive 242,785 calls, 19s).
- 26-design-patterns-advanced: Bronze __init_subclass__ Tool registry (no-op starter so test collection works) + registry_dispatch with source-check for manual registration (literal registry[" keys), Silver Editor undo/redo (_Insert/_Delete snapshots), Gold LLMClient Protocol with @runtime_checkable + Summarizer constructor injection (fake prefix "FAKE:summa:" = first 5 chars).
- 27-packaging-and-distribution: Bronze parse_version (tuple-padded), Silver compare_versions + matches_requirement (pip-style: pre-releases excluded unless spec mentions rc/a/b/dev/post, so 2.0.0rc1 must NOT satisfy <2), Gold latest_compatible + pyproject_info via tomllib (no external libs).

Quizzes: 20 questions each (6 Easy / 9 Medium / 5 Hard, >=8 code-output), Answer Key with distractor analysis. Glossaries: 15-17 terms each (>=15 requirement), flat alphabetical ### Term with Definition/Example/output/Related. Lectures: 12-section shape (numbered sections, Common Mistakes, Best Practices, Complexity and Cost, AI Engineering Relevance table, 6 Practice Exercises, Summary, Quick Reference, Next Steps). READMEs updated: 02-advanced-python/README.md topics table now 01-27 + companion-material pointer; lectures/README.md table extended to 11-27 + Phase 4 study path.

Final validation (this session): exercises 21-27 pass plain AND --verify (also confirmed 20, 28, 29 still green). Challenge suites: solution passes 11/12/17/12/15/16/23 (total 106); starter fails in every suite (10/1, 12/0, 17/0, 12/0, 15/0, 13/3, 23/0 — topic 26's 3 starter passes are the DI signature tests the starter already satisfies structurally). Quiz question counts verified by grep: exactly 20 per file (21-27, and 28-29 for completeness).

### Alternatives

Challenge design choices vs alternatives: 21 Gold could have used ratio asserts on wall-clock (rejected: Windows scheduler noise; used call-count/peak/task-order asserts only); 22 Gold used identical 0.01s delays first (rejected: cancellation nondeterministic — staggered 5s tail makes fail-fast provable); 24 collect_cycle initially used enumerate() (rejected after diagnosing the loop-variable reachability bug); 26 registry could use a metaclass (rejected: __init_subclass__ is the modern idiom and matches the lecture); 27 could use packaging.Requirement (rejected: not guaranteed in the env — hand-rolled PEP 440 comparison with explicit pre-release rule, matching pip default behavior). Quiz 22 Q17 originally had placeholder lines (print("cannot run: q undefined")) — replaced with clean runnable asyncio.run(main()) snippet keeping the no-sentinel-hang teaching point.

### Rationale (Why this?)

Specs from 01-content-standards.md drove everything: deterministic ASCII-only stdout, no network/pip, ratio/growth asserts instead of wall-clock, Windows spawn-safe module-level workers, runtimes under 15-30s, complexity annotations, AI-relevance docstrings, 12-section lectures with Output comments, challenges with README/starter/solution/test where pytest passes solution and fails starter, quizzes 20Q with 6E/9M/5H and >=8 code-output, glossaries >=15 terms. Calibration numbers were measured on this machine (Python 3.13.11, pytest 9.0.2) and baked into lectures/glossaries so every stated number is reproducible. Revisit if: environment Python major changes (GIL work, TaskGroup semantics), or packaging ecosystem introduces pip-visible pre-release default changes.

### Exercises

1. Re-run the full sweep: cd projects/00-core-foundations/python; foreach file in 02-advanced-python\{21..27}.py run plain then --verify (all must exit 0); then pytest 02-advanced-python/challenges/2[1-7]-*/test_challenge.py with $env:CHALLENGE_MODULE='solution' (106 passed) and 'starter' (all fail). 2. Read 22's Gold challenge and explain WHY the staggered 5s delays make the TaskGroup fail-fast provable — derive the timeline by hand. 3. Extend 23's build_schema to nested generics (dict[str, list[int]]) and make signature_matches handle **kwargs. 4. Run mypy --strict on 02-advanced-python\{21..27}.py per the phase exit criteria and log findings. 5. Do a hand-timed reproduction of one calibration number (e.g., fib(25) call counts) and confirm it matches the lecture/glossary.

### Next Steps

Update admin/mastery-plan/03-phase-2-advanced-python.md deliverable checklists (topics 21-27 now 5/5). Run the repo's run_smoke_tests.py to confirm the whole python directory passes. Check docs/learning/00-INDEX.md to see if it tracks these topics and add entries if so. Verify topics 28-34 completeness claim from the prior session log (28-30 quizzes already exist). Optional: a second QA pass re-reading one lecture (21) line-count/style against content-standards §3.

---
