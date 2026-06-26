# Regression Test: project-planner — Prompt Version Drift

- **Regression ID:** planner-regression-001
- **Prompt ID:** role.project-planner
- **Prompt version tested:** 1.0.0 → 1.1.0 (hypothetical change)
- **Created:** 2026-06-26
- **Status:** —

---

## Change Description

### What Changed

The project-planner prompt was modified in version 1.1.0 to:
1. Add a new section: "## Technical Constraints" between "Goal" and "MVP First"
2. Increase the recommended task duration from "60–90 min" to "60–120 min"
3. Remove the constraint `mark-open-questions` from the constraints list

### Why It Changed

- User feedback: plans lacked technical context about existing systems
- Task sizing feedback: 90 min was too restrictive for database migration tasks
- Open questions section was being used for trivial items; user preferred inline notes

---

## Regression Checks

### Check 1: MVP Section Still Exists

- **Test:** After the prompt change, does the planner still produce an "MVP First" section?
- **Expected:** Yes — MVP scoping is a core constraint
- **Regression if:** MVP section is missing or deprioritized below "Technical Constraints"
- **Severity:** Critical (core behavior broken)

**How to verify:**
1. Feed the golden input "Add JWT refresh token support to auth-service"
2. Check that the output has `## MVP First` with MVP scope and deferred items
3. If missing, regression confirmed

### Check 2: Open Questions Still Marked

- **Test:** Even with `mark-open-questions` removed from constraints, does the planner still surface unknowns?
- **Expected:** The template still has `## Open Questions` section, so the planner should still produce it
- **Regression if:** Planner stops producing open questions because the constraint was removed
- **Severity:** High (quality degradation)

**How to verify:**
1. Feed the golden input
2. Check that `## Open Questions` section exists with ≥1 question
3. If empty or missing, regression confirmed

### Check 3: Task Duration Range

- **Test:** Are tasks now allowed to be 90–120 min?
- **Expected:** Some tasks (e.g., "Database migration") may now be 100–120 min
- **Regression if:** ALL tasks are still ≤90 min (constraint didn't take effect) OR all tasks are >120 min (constraint too loose)
- **Severity:** Medium (scope drift)

**How to verify:**
1. Feed the golden input
2. Check task duration estimates
3. At least one task should be in 90–120 range; no task should exceed 120 min

### Check 4: No Code Constraint Preserved

- **Test:** Does the planner still avoid writing implementation code?
- **Expected:** Yes — `no-code` is still in the constraints
- **Regression if:** Planner includes code snippets
- **Severity:** Critical (core constraint broken)

**How to verify:**
1. Feed the golden input
2. Check that no code blocks (` ```go ` or similar) appear in the output
3. File structure section shows paths only, not file contents

### Check 5: New Technical Constraints Section

- **Test:** Does the planner produce the new "Technical Constraints" section?
- **Expected:** Yes — this was the intended addition
- **Regression if:** Section is missing (addition didn't take effect)
- **Severity:** Medium (intended feature missing)

**How to verify:**
1. Feed the golden input
2. Check that `## Technical Constraints` exists with relevant content
3. Content should reference existing auth-service architecture

---

## Pass/Fail Criteria

| Check | Description | Pass | Fail |
|-------|-------------|------|------|
| 1 | MVP section still exists | Present with scope + deferred | Missing or empty |
| 2 | Open questions still marked | ≥1 question in section | Empty or missing |
| 3 | Task duration range | 1–3 tasks in 90–120 range | All ≤90 or any >120 |
| 4 | No code constraint | No code blocks in output | Code blocks present |
| 5 | Technical constraints section | Section exists with content | Section missing |

### Overall Verdict

- **PASS:** All 5 checks pass
- **FAIL:** Any check fails — investigate the prompt change
- **PARTIAL:** Check 5 fails (intended feature missing) but all others pass

---

## Rollback Plan

If regression is detected:
1. Revert prompt to version 1.0.0
2. Re-run golden case `planner-basic-001` to confirm baseline behavior
3. Redesign the change with regression testing in mind
4. Consider adding the change as an optional section rather than removing constraints

---

## Notes

- This regression test is **prospective** — it tests a hypothetical change
- In practice, run this test after any modification to `role.project-planner`
- The test uses the same golden input as `planner-basic-001` for consistency
- Regression tests should be run BEFORE committing prompt changes
