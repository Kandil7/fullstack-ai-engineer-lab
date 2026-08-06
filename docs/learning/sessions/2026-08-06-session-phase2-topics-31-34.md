# Phase 2 Topics 31-34: Concurrency, Metaprogramming, Security, Debugging

### Context

Session in fullstack-ai-engineer-lab/projects/00-core-foundations/python: authored Phase 2 Advanced Python topics 28-34 (7 topics x 5 artifacts = 35 files) per admin/mastery-plan/01-content-standards.md and 03-phase-2-advanced-python.md. Topics 28-30 were completed in earlier sessions; this session finished the pending Topic 30 artifacts (already existed from prior work) and created 31-34 fully.

### Explanation

Topics created this session: 31-concurrency-patterns (bounded queue backpressure = R1.1 fix, token bucket + circuit breaker + retry-with-jitter with injectable clocks, graceful shutdown, idempotency, bulkhead; lecture references the 04-queues.py R1.1 deadlock; exercise runs 0.45s, challenge 19/19), 32-metaprogramming (__init_subclass__ registry, __set_name__ descriptors, inspect.signature+get_type_hints -> JSON schema = the @tool pattern, importlib plugins, dispatch tables vs eval, ast, monkey-patching; caught the string-annotations trap), 33-security-essentials (secrets vs random, pbkdf2_hmac + compare_digest, parameterized SQL, subprocess arg lists, resolve+is_relative_to path containment, pickle/yaml RCE demos, ReDoS, redaction; fixed Windows echo->sys.executable, line-buffering for deterministic output), 34-debugging-techniques (traceback.format_exc shape, assertion-driven boundary debugging, leveled logging, seed freezing/PYTHONHASHSEED, faulthandler real-file dumps, scripted pdb via cmdqueue+do_p override, bisection, hypothesis method for silent RAG bugs). Key Python 3.13 traps hit: faulthandler.dump_traceback requires a real file (not StringIO), Pdb.run has no commands kwarg (use cmdqueue), pdb has built-in do_p so default() never intercepts, list.shuffle returns None, stable sort expectations in challenge tests.

### Alternatives

For schema generation: using get_type_hints to resolve string annotations (from __future__ import annotations) vs matching raw strings — get_type_hints is what real @tool implementations do. For password hashing: pbkdf2_hmac stdlib fallback since bcrypt/argon2 unavailable in env (documented in lecture as the production preference). For pdb demo: scripted cmdqueue session vs interactive breakpoint() — cmdqueue keeps CI deterministic.

### Rationale (Why this?)

Specs demanded: exercises with _verify() >=5 asserts, ASCII-only deterministic stdout, complexity annotations, AI-relevance docstrings, 12-section lectures with Output comments, challenges with README/starter/solution/test (pytest passes solution, fails starter), 20-question quizzes with 6E/9M/5H and >=8 code-output. Concurrency topic had a hard <30s budget (0.45s actual) and no wall-clock asserts. All 7 exercises verified exit 0 plain and --verify; 133/133 challenge tests pass in 1.86s.

### Exercises

1. Re-run the full sweep: python 02-advanced-python\{28..34}.py --verify and pytest challenges\{28..34}-* -q (133 tests). 2. Review 31's R1.1 worked example against 06-data-structures-algorithms/04-queues.py BoundedBuffer. 3. Extend 32's describe() to nested objects/arrays (dict[str, int]) and test. 4. Build a 5-step hypothesis drill for a deliberately broken RAG pipeline using 34's boundary-assert pattern. 5. Check the phase doc exit criteria: mypy --strict on new files.

### Next Steps

All 7 Phase 2 topics (28-34) are now complete: 35 artifacts. Next: update admin/mastery-plan checklists (03-phase-2-advanced-python.md deliverable counts), run the repo's run_smoke_tests.py to confirm the whole python directory passes, consider mypy --strict pass per exit criteria, and update docs/learning/00-INDEX.md if it tracks these topics.

---
