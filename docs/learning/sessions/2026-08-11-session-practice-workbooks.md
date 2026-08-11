# Practice Workbooks for the AI Engineer Curriculum (83 topics, 4 modules)

### Context

Repo: fullstack-ai-engineer-lab (active track: 10-week AI Engineer, vehicle DevMate). The 4 curriculum lectures (docs/curriculum/lectures/01-04) had exercises and quizzes but no per-topic practice depth. User asked to "add practice for every section and for every topic in details and with real world problems" so an AI engineer can master every topic.

### Explanation

Built a practice workbook system at docs/curriculum/practice/: README.md (index + mastery protocol + per-topic template) plus 4 workbooks — 01-llm-fundamentals (15 topics), 02-rag-systems (20), 03-agents (24), 04-evaluation-observability (24) = 83 topics total. Every lecture section (1.1–4.9, 28 sections) opens with a concrete real-world problem (legal-tech token blow-up, e-commerce 429 storms, agent burning $400 in loops, silent prompt regressions, $30k/month bills, query drift in new markets). Every topic follows the template: Mastery = observable definition; Level 1 Drill (deterministic, assertable, 20–45 min); Level 2 Applied (real DevMate files + acceptance commands); Level 3 Stretch (production-grade, ADR-style justification); Verify (exact commands); Common failure modes (symptom→cause→fix tables); Interview (question + strong-answer structure). Workbooks are anchored to verified repo facts: real Makefile targets (make test/eval/ci/cli/up), real module paths (devmate/src/devmate/llm/client.py, ingest/chunker.py, obs/cost.py, mcp/server.py, etc.), real eval folders (evaluations/rag/datasets, reports, baselines), and planned deliverables (devmate-golden.jsonl, eval/run_ragas.py). Subagents (llm-ops, rag-optimization, agent-systems, ai-evaluation engineers) wrote one workbook each in parallel; M4 initially failed and was re-launched. Bonus findings baked into drills: FixedSizeChunker has an infinite loop when chunk_size <= overlap (blocks make test); tenacity policy retries only Timeout/NetworkError so 429s never retry; OpenAI streams get usage=0 without stream_options include_usage; RecursiveChunker descends to character level unlike LangChain; CRLF vs LF changes chunk boundaries; mcp/server.py has no __main__ entrypoint; LangGraphAgent falls back to ReAct. Lectures now link forward to their workbooks; README links back.

### Alternatives

(1) Add practice inline inside each lecture — rejected: lectures stay theory-only, workbooks stay depth-only, one change doesn't bloat the other. (2) One giant 4-module practice file — rejected: ~4000 lines unmanageable, per-module files match per-module lectures. (3) Code-file exercises like projects/04-ai-engineering/ai-automation/practice — rejected for the workbook layer because verification and interview dimensions are documentation, but Level-1 drills remain runnable as .py scratch scripts. (4) I write all four myself sequentially — rejected: parallel domain specialists (llm-ops, rag-optimization, agent-systems, ai-evaluation) produced deeper, verified content faster; orchestrator reviewed and integrated.

### Rationale (Why this?)

The track (ADR-0006) requires curriculum content to be production-focused and anchored to DevMate; each Applied level therefore maps to a real repo path and a command that proves completion, and each Stretch level ends in an ADR-style decision. Mastery protocol (Drill→Applied→Stretch, verify before moving on) replaces "feels understood" with runnable evidence — consistent with the track's definition-of-done culture (make eval prints a table, chunking ADR cites numbers). Revisit when: a topic's real repo path changes, the golden set (devmate-golden.jsonl) ships and drill numbers should be re-verified, or LangGraph/MCP modules land and 03's stubs become real code.

### Exercises

1. Run the M2 workbook's FixedSizeChunker drill: reproduce the infinite loop with chunk_size=100 overlap=10 on 200 words, add a regression test, fix, and log in mistakes.md. 2. Do M1 topic 1.3.b Level 2: wire per-request cost tracking into obs/cost.py and prove `make test` green with a $/query assertion. 3. Do M4 topic 4.6a Level 3: inject a prompt bug, prove the regression gate fails (baseline 0.91 faithfulness), revert, write the ADR. 4. Create evaluations/rag/datasets/devmate-golden.jsonl (25 questions, 40/40/20 difficulty) per M4 section 4.2, then build eval/run_ragas.py so `make eval` prints a table. 5. Do M3 topic 3.3c: write path-traversal tests for read_file (../, %2e%2e, absolute paths) and make them pass.

### Next Steps

Next: (1) execute workbook Level 2s in week order — they are the track's build list anyway; (2) when devmate-golden.jsonl and eval/run_ragas.py exist, re-verify M2/M4 drill numbers against real output; (3) consider adding a practice/README progress tracker (checkboxes per topic) once execution starts; (4) extend the same workbook pattern to the deferred ML sprint (07-machine-learning) if time allows.

---
