# Monorepo Structure

```text
fullstack-ai-engineer-lab/
  README.md  ROADMAP.md  MAKEFILE.md  .gitignore  .editorconfig  .gitattributes

  .ai/
    prompts/   system/ roles/ tasks/ critics/ repair/
    workflows/ feature/ debugging/ learning/ architecture/ evaluation/

  templates/            # 15 artifact templates

  registries/           # prompt / workflow / template / decision / skills YAML

  docs/
    architecture/       # overview, monorepo-structure, ai-workspace-architecture
    decisions/          # ADR index + numbered ADRs
    learning/           # paths/ deep-dives/ notes/{weekly,monthly}/ source-summaries/
    product/            # workspace-goals, scope-definition, feature-priorities
    cheat-sheets/       # git, docker, postgres, qdrant, prompt-design

  learning-sources/     # source-index + books/ repos/ notebooks/ official-docs/

  evaluations/
    prompts/  golden-cases/ regressions/
    rag/      datasets/ reports/ baselines/
    projects/ auth-service/ rag-system/ capstone/

  projects/
    00-core-foundations/  go/ git-linux/ ds-algo/
    01-backend-go/        01-auth-service/ 02-user-service/ 03-chat-service/
    02-frontend/          flutter-app/ nextjs-web/
    03-databases/         postgres-design/ redis-cache/ qdrant-rag/
    04-ai-engineering/    prompt-engineering/ embeddings/ rag-system/ agents/
    05-system-design/
    06-devops/            docker/ ci-cd/ deployment/
    07-capstone/          thanaweyagpt/ backend/ frontend/ ai/ infra/ docs/

  infra/
    docker/   docker-compose.yml + postgres/ redis/ qdrant/
    scripts/  setup.ps1 dev-run.ps1 seed-db.ps1 new-adr.ps1 new-review.ps1 new-source-note.ps1

  tests/
    repo-structure/ templates/ workflows/ prompts/
```

## Naming Conventions

- ADRs: `NNNN-kebab-title.md` (4-digit, zero-padded).
- Source summaries: `<type>-<slug>.md` under `docs/learning/source-summaries/`.
- Project artifacts: `feature-spec.md`, `plan.md`, `architecture-review.md`, `ai-review.md`,
  `notes.md`, `mistakes.md` inside each project folder.
- Prompts: `<layer>.<name>` ids; workflows: `<group>/<NN-step>` ids.

## Why `.ai/` (not `99-ai-workflow/`)

See [ADR-0002](../decisions/0002-prompt-modularization.md). `.ai/` is concise, sorts to the top,
and signals "machine/AI workspace" distinct from human docs in `docs/`.
