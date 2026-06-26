---
id: task.source-extractor
layer: task
version: 1.0.0
status: active
owner: workspace
pairs_with_roles: [source-learning-agent]
constraints: [source-grounded, separate-confirmed-vs-inferred, one-exercise, repo-first]
---

# Task: Source Extractor

Extract a structured lesson from a single source.

## Steps

1. Identify source type → pick the matching template.
2. Pull confirmed key concepts (stated by the source).
3. List your inferences separately and label them.
4. Keep minimal example code worth retaining.
5. Produce exactly **one** practical exercise tied to a project task.
6. Flag low-confidence areas.

## Constraints

- Do not exceed what the source supports without labeling it inference.
- Must link to a real `projects/...` task.
- Include the Arabic summary section.
