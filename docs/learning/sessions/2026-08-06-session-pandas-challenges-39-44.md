# Pandas Curriculum: Challenges 40-44 + Quizzes 39-44 + Two Inverted-Premise Discoveries

### Context

In projects/00-core-foundations/python (pandas curriculum), authored and verified challenges 40-44, quizzes 39-44, and synced lecture/glossary 44 after discovering two pandas behaviors that contradicted my initial assumptions.

### Explanation

Challenges 39-44 are now complete and verified: each has README (Bronze/Silver/Gold), starter.py, solution.py, test_challenge.py, with solution-passes/starter-fails confirmed. Challenge 41 (time series) teaches no-leak rolling means — the key insight is rolling(window).mean().shift(1) makes windows past-only; the test window arithmetic is mean(s.iloc[t-5:t]) for row t. Challenge 42 (groupby) reimplements split-apply-combine manually with a monkeypatched groupby guard, builds a (column, metric) MultiIndex via agg+concat (NOT sort_index — that breaks native column order), and a cohort retention matrix using month-position maps and nunique denominators. Challenge 43 (pandas for ML) revealed the OLS scale-invariance trap: LinearRegression predictions/RMSE are IDENTICAL whether the scaler was fit on train or pooled data; switched to Ridge(alpha=10) where clean RMSE 1.82 < leaky 3.51, and learned pandas .std() defaults to ddof=1 while sklearn uses population std. Challenge 44 (pitfalls) had the biggest discovery: pct_change() defaults to fill_method='pad', FILLING gaps before computing deltas — [10, NaN, 20] gives [NaN, 0.0, 1.0] (fabricated), and the honest version is pct_change(fill_method=None). The original premise (pandas stays NaN) was inverted; I rewrote the challenge, synced lecture 44 (added section 5, renumbered 5-9 to 6-10), and glossary 44 (added fill_method term). Quizzes 39-44 written in supplementary/quizzes/ with 20 questions each (6E/9M/5H), answer keys, and scoring guides. Exercises 39-44 re-verified [OK].

### Alternatives

1. For challenge 43: keep LinearRegression — rejected because OLS absorbs affine transforms into coefficients, making the scaling-leak demo produce identical RMSEs (probe confirmed clean == leaky exactly). KNN also failed (single-feature monotone scaling preserves neighbor order). Ridge with meaningful alpha was the only reliable demo. 2. For challenge 44: implement safe_pct_change as NaN-fill — rejected because the premise was false; the REAL pitfall is the ffill fabrication, so safe = fill_method=None. 3. For quiz style: followed the existing pandas-advanced-quiz.md format (## Question N [Difficulty], A-D, Correct Answer + Explanation, code blocks) rather than inventing a new layout.

### Rationale (Why this?)

Every challenge expectation was probed against pandas 2.2.3/numpy 2.4.1 before being committed to tests — the two memory entries (pct_change ffill, OLS scale-invariance) capture reusable cross-project facts. Test files always run starter (fails with NotImplementedError) by default and solution via CHALLENGE_USE_SOLUTION=1, matching the established challenge pattern. Lecture/glossary sync after a discovery is mandatory so learners never read content that contradicts the verified challenge.

### Exercises

1. Re-run each challenge with CHALLENGE_USE_SOLUTION=1 and confirm green: 39 (17), 40 (15), 41 (17), 42 (19), 43 (17), 44 (25). 2. Re-run the 6 exercises (39-44) and confirm [OK]. 3. Answer the 20-question quiz for each topic and score against the guide. 4. Write a cohort retention analysis on real data using challenge 42's matrix. 5. Refactor a real pipeline's pct_change calls to fill_method=None and verify no fabricated deltas.

### Next Steps

Run the targeted full pandas exercise loop (all verified files) and document remaining FAILED items if any; consider adding the pct_change pitfall to the quizzes README topic list; then report the full per-topic inventory (6 lectures, 6 glossaries, 6 exercises, 6 challenges, 6 quizzes) for topics 39-44.

---
