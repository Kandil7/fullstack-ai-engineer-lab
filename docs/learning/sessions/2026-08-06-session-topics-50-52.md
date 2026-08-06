# Topics 50–52 Content: Datetime, Serialization, Memory & Performance

### Context

Phase-1 core-Python curriculum at projects/00-core-foundations/python (fullstack-ai-engineer-lab). Session 2 of the topics 47–52 content campaign: completed topics 50 (datetime/timezones), 51 (serialization/persistence), 52 (memory/perf) — lecture, glossary, challenge (README/starter/solution/test), and quiz each, following the canonical templates from admin/mastery-plan/01-content-standards.md and the model quality of 42-pathlib. Topic 50's lecture had been written at the end of the previous session.

### Explanation

Produced 12 files: 50 lecture (456 lines) + glossary (380), 51 lecture (593) + glossary (449), 52 lecture (567) + glossary (425), challenge dirs 50/51/52 (README + starter + solution + test_challenge each), and quizzes 50/51/52 (20 questions, difficulty tags, answer keys). Verified: 124 challenge tests fail vs starter (NotImplementedError) and 124 pass vs solution (17+21+25+23+21+17). Key technical facts verified empirically before writing content: (1) Cairo 2026 DST: spring-forward gap at Apr 24 00:00 (00:00-00:59 doesn't exist), fall-back at local 03:00 on Oct 29 making 02:00-02:59 ambiguous (fold=0 gives +03:00, fold=1 +02:00) — NOT midnight as commonly assumed; (2) NY 2026: gap Mar 8 02:30 resolves via replace(tzinfo=ny) to pre-transition -05:00 (07:30Z), back-converts to 03:30 EDT; (3) pickle DEFAULT_PROTOCOL=4, HIGHEST=5 on 3.13; (4) sqlite3 `with conn:` commits/rolls back but does NOT close; Connection is immutable (cannot shadow execute on instance or class — must subclass via factory=, and executemany internally dispatches exactly one execute); (5) JSON emits non-standard NaN token by default; (6) CPython 3.13.11 sizes: list of 4 = 88B (stale exercise comments said 96), dict empty 64 / 4-key 184, int 2**62 36B, float 24B, 2-attr instance 48B both with and without dict — the __slots__ win is the ~264-296B dict itself; (7) join vs += measured ~11x at n=500k with list-based join (generator join is only ~2x — an honest benchmark needs the real pattern); (8) tracemalloc: 1M datetime schedule stream peaks 22 KiB vs ~56MB materialized; 1M floats ~32MB.

### Alternatives

(a) Keeping the pre-existing short lectures/glossaries (215-325 lines) and only adding missing pieces — rejected: they lacked the mandatory "Cheaper alternative" column and canonical 12-section structure. (b) Wall-clock performance guards in tests — rejected: flaky on CI; used op-counting (zoneinfo construction counter via fresh-import + patched zoneinfo.ZoneInfo; sqlite3 execute call counting via Connection subclass factory=; tracemalloc ceilings). (c) Instance-attribute monkeypatching for sqlite3 counting — impossible (C extension immutable); class-attribute patching also fails; documented subclass-with-factory is the correct mechanism. (d) 10^6-iteration memory test — 8.8s runtime; cut to 4e5 with a 15MiB ceiling (materialized ~22MB) for a 3.5s test. (e) pytest same-basename collision (all test_challenge.py in sibling dirs) — fixed globally with --import-mode=importlib in pytest.ini (recommended pytest 7+ mode).

### Rationale (Why this?)

The empirical verifications exist because the pre-existing exercise files contained stale Output comments (e.g., list of 4 = 96B, dict-instance + dict = 56B, "53x faster" join, Cairo transitions at wrong hours). Content correctness required measuring on the actual runtime (3.13.11). The tracemalloc/op-counting guards were chosen over wall-clock because challenge tests run on student machines; deterministic guards make pass/fail meaningful. The memory-test sizes were tuned so materialization (the bug being caught) exceeds the ceiling with margin while the streaming path stays 3 orders of magnitude under it. Revisit: the pytest.ini change is project-wide; if the repo later standardizes unique test basenames, --import-mode=importlib becomes unnecessary but remains harmless.

### Exercises

1. Run the full challenge suite both ways: pytest challenges dir (all 124 fail vs starter), then $env:CHALLENGE_USE_SOLUTION=1 (all 124 pass). 2. In the 50 test, delete the tracemalloc guard temporarily and materialize the stream — confirm the 15MiB/50MiB ceilings catch it, then restore. 3. In the 51 test, replace executemany with a per-row execute loop and confirm the CountingConn factory catches it (calls == 20_000). 4. Compute Cairo 2026 DST transition times with zoneinfo for a different year (2027) and note how the gap/ambiguous hours shift — the Oct 29 03:00 fall-back is a non-obvious fact worth re-deriving. 5. Re-run the join vs += benchmark with generator-join vs list-join and explain why the ratio differs (generator overhead dominates at small n).

### Next Steps

Topics 47–52 campaign is complete (12 lectures+glossaries, 6 challenge dirs, 6 quizzes, 124 verified tests). Next: (1) update docs/learning/00-INDEX.md coverage tracker if one exists for this repo; (2) run the same 4-part flow for any remaining Phase-1 topics or move to Phase-2 (advanced-python) linking exercises (03-context-managers, 04-async-await, 10-itertools, 11-collections, 19-logging already referenced); (3) consider a docs-drift-check pass over the old Output comments in exercise files 50-52 (some were stale and corrected in the lectures).

---
