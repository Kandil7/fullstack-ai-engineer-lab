---
id: repair.fix-output-format
layer: repair
version: 1.0.0
status: active
owner: workspace
trigger: invalid-output-shape
---

# Repair: Fix Output Format

Use when output did not match the required template/shape.

## Steps

1. Identify the correct template in `templates/` for this artifact.
2. Map the existing content onto the template's required sections.
3. Fill any missing required section (e.g. ADR Consequences, review Severity, plan Open Questions).
4. Preserve the substance; only restructure.

## Output

The same content, correctly shaped to the template, with no required section empty.
