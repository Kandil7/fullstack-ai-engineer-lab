<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# 1) Executive Summary

- سيتم بناء **AI Engineering Workspace / Learning OS** على شكل monorepo عملي يجمع بين: التعلم بالمشاريع، AI workflows، prompts versioned، architecture reviews، code reviews، debugging logs، وcapstone projects ضمن repo واحد منظم.[^1]
- الهدف ليس مجرد repo تعليمي، بل **operating system هندسي** يساعد المستخدم على التعلم، التنفيذ، المراجعة، والتطور من Full-Stack AI Engineer إلى مستوى إنتاجي أعلى.[^1]
- التصميم المناسب هنا هو **hybrid architecture**: content/documentation-centric repo أولًا، مع طبقة workflows وprompts وtemplates واضحة، بدل البدء بمنصة برمجية ضخمة فيها orchestration runtime معقد من اليوم الأول.[^1]
- النظام الحالي المستنتج من الخطة يركز على Go backend، Flutter frontend، FastAPI لخدمات AI، PostgreSQL وRedis وQdrant، إضافة إلى AI workflows داخل `99-ai-workflow/` أو ما يعادله.[^1]
- سيتم فصل المكونات إلى: learning content، project workspaces، reusable prompts، review artifacts، decision records، evaluation assets، وworkflow templates.[^1]
- سيتم اعتماد **prompt architecture modular** بدل prompt واحد عملاق: teacher, planner, reviewer, debugger, architect, feature-builder, source-learning.[^1]
- لن يتم اقتراح agents runtime كثيرة بلا داعٍ؛ في MVP ستكون معظم “agents” **prompted operating modes** داخل workspace، وليس distributed autonomous agents. هذا أبسط وأكثر توافقًا مع الهدف الحالي.[^1]
- سيتم اعتبار prompts، templates، ADRs، وreview outputs كـ **engineering artifacts** يجب versioning لها، اختبارها، ومراجعتها.[^1]
- سيتم دعم source-driven learning من الكتب، repos، notebooks، والوثائق الرسمية عبر workflows مخصصة لكل نوع مصدر.[^1]
- حدود النطاق الحالية: النظام هو **repo-centric implementation system** يدعم التنفيذ البشري وAI-assisted workflows؛ ليس مطلوبًا الآن بناء SaaS متعددة المستخدمين لإدارة هذه العمليات.[^1]


# 2) Problem Framing

النظام يحل مشكلة أن خطط التعلم والمشاريع والـ prompts والمراجعات غالبًا تكون مشتتة بين ملفات، chats، notebooks، وأدوات متفرقة، مما يجعل التطور غير منظم وغير قابل للقياس.[^1]

المستخدم الأساسي هو مهندس يريد أن يصبح Full-Stack AI Engineer بمستوى إنتاجي، مع ربط التعلم بالمشاريع العملية في backend، frontend، AI engineering، system design، وdevops. كما أن النظام يجب أن يناسب مشاريع فعلية مثل Athar وBaligh ذات الطابع RAG/LLM-heavy.[^1]

المدخلات الأساسية تشمل:

- roadmap/plan
- source materials مثل docs/books/repos/notebooks
- feature ideas
- code under review
- bugs/errors
- architectural questions
- AI project artifacts[^1]

المخرجات المتوقعة تشمل:

- project plans
- implementation workflows
- code reviews
- architecture reviews
- debugging sessions
- source-learning notes
- ADRs
- evaluation artifacts
- capstone project structure[^1]

قيود المجال الحالية:

- يجب أن يبقى النظام عمليًا وقابلًا للتنفيذ الفردي.
- يجب تجنب over-engineering في طبقة agent runtime.
- يجب أن تكون البنية قابلة للتوسع لاحقًا لتخدم مشاريع AI production مثل RAG systems وagentic apps.[^1]


# 3) Scope Definition

## In Scope

- Monorepo منظم للتعلم والتنفيذ والمراجعة.[^1]
- Project folders للمسارات: foundations, backend, frontend, databases, AI engineering, system design, devops, capstone.[^1]
- Prompt system modular ومقسم حسب الوظيفة.[^1]
- Workflows للتخطيط، البناء، المراجعة، التصحيح، والتعلم من المصادر.[^1]
- Documentation system: README, roadmap, ADRs, learning notes, review logs.[^1]
- Source-learning system من books/repos/notebooks/official docs.[^1]
- Evaluation folders وتقارير أولية للمشاريع AI-heavy.[^1]


## Out of Scope

- SaaS multi-user product لإدارة هذه العمليات.
- autonomous multi-agent runtime orchestrator يعمل في الإنتاج.
- full UI لإدارة الـ repo workflows.
- enterprise-grade secret management platform.
- automatic code execution engine داخل النظام نفسه.[^1]


## Future Scope

- dashboard لتتبع التقدم.
- CLI لتوليد templates والـ ADRs والـ review files.
- local retrieval layer للبحث داخل docs والقرارات والـ prompts.
- evaluation harness أكثر صرامة لمشاريع Athar/Baligh.
- integration مع GitHub Actions لفحوص prompts والوثائق والملفات.[^1]


# 4) System Architecture

## High-level architecture

المعمارية المقترحة هي **Repo-Centric Agentic Workspace**:

1. **Content Layer**
يحتوي roadmap، docs، learning paths، deep dives، source materials، وdecision records.[^1]
2. **Project Layer**
يحتوي المشاريع التطبيقية الفعلية: auth-service، chat-service، rag-system، ai-assistant، capstone.[^1]
3. **Workflow Layer**
يحتوي step-by-step workflows للتخطيط، البناء، المراجعة، debugging، والتعلم من المصادر.[^1]
4. **Prompt Layer**
يحتوي prompts modular تستخدم كـ operating modes: mentor, planner, architect, reviewer, debugger, interviewer, source-learning.[^1]
5. **Template Layer**
يحتوي templates موحدة للـ plans, reviews, ADRs, bug reports, daily logs, source summaries.[^1]
6. **Evaluation Layer**
يحتوي golden cases، review outputs، eval reports، release gates للمشاريع AI.[^1]
7. **Project Delivery Layer**
يحتوي infra, docker, scripts, app structure للمشاريع الكاملة لاحقًا، خاصة monorepo Go + FastAPI + Flutter + Next.js.[^1]

## Core services/modules

| Module | Why exists | Responsibility | Inputs | Outputs | Relation |
| :-- | :-- | :-- | :-- | :-- | :-- |
| `docs/` | حفظ المعرفة والقرارات | توثيق architecture, learning, product, ADRs | plans, decisions, learnings | structured docs | يخدم كل الطبقات |
| `templates/` | توحيد المخرجات | قوالب ثابتة للخطط والمراجعات | task or source context | filled artifact | تستخدمه workflows |
| `prompts/` أو `.ai/prompts/` | modular prompt system | تشغيل أدوار AI المختلفة | user task + context | constrained AI output | مرتبط بالworkflows |
| `workflows/` أو `.ai/workflows/` | تنظيم التنفيذ | تسلسل الخطوات لكل نوع عمل | entry task | next action + artifacts | يستدعي prompts/templates |
| `projects/` أو phase folders | تنفيذ المشاريع | code + project docs | features, tasks | working software | يعتمد على docs/workflows |
| `evaluations/` | ضبط الجودة | tests, golden cases, AI evals | outputs/models/retrieval | quality evidence | للمراجعة والإطلاق |
| `learning-sources/` | source-driven learning | تنظيم مصادر التعلم | books/repos/docs/notebooks | structured lessons | يغذي docs/learning |

## Orchestration layer

لا يوجد orchestrator runtime منفصل في MVP. orchestration هنا **human-led + workflow-driven** عبر ملفات workflows وprompts. هذا أبسط لأنه يحقق الهدف الحالي دون بناء agent platform كاملة.[^1]

## Agent layer

الـ “agents” هنا هي **logical roles** وليست processes مستقلة:

- Learning Coach
- Project Planner
- System Architect
- Pair Programmer
- Code Reviewer
- Debugging Specialist
- Source Learning Agent
- System Designer/Principal Engineer mode[^1]


## Skill layer

الـ skills هي reusable capabilities مثل:

- architecture decomposition
- code review
- bug triage
- source extraction
- implementation planning
- RAG evaluation planning


## Prompt layer

مقسمة حسب الوظيفة والملكية والاستخدام، وليس prompt monolith واحد.[^1]

## Memory/context layer

- short-term: current task context + selected source + current file paths
- long-term: docs, ADRs, review logs, learning notes, evaluations داخل repo
- no hidden opaque memory required في MVP


## Integration/tool layer

- Git/GitHub
- Docker/Compose
- optional CI
- project runtime stacks: Go, FastAPI, Flutter, Next.js, PostgreSQL, Redis, Qdrant.[^1]


## Storage/config layer

- Markdown docs
- YAML/JSON config for registries
- code repos and project folders
- env files للمشاريع الفعلية


## Request lifecycle

مثال feature lifecycle:
START → feature request → planner prompt → plan artifact → architect prompt → architecture review → implementation in project folder → code review → fixes → reflection/learning log → END.[^1]

## Control flow

- Entry from one of: new feature, new bug, new source, new design question.
- Workflow selects template + prompt + target folder.
- Human executes/edits artifacts.
- Output stored in repo in deterministic path.
- Reviews feed into fixes أو ADRs أو learning notes.[^1]


## Failure points

- prompts واسعة أكثر من اللازم.
- duplication بين docs وproject notes.
- turning every capability into an “agent”.
- lack of naming conventions.
- reviews دون follow-up.
- source learning without project linkage.[^1]


## Fallback paths

- downgrade multi-agent concept إلى single workflow + prompt.
- إذا لم توجد معلومات كافية: create `open-questions.md`.
- إذا كان task صغيرًا: استخدم pair-programmer أو reviewer فقط.
- إذا كان design غير ناضج: اكتب ADR draft بدل implementation.[^1]


# 5) Project Structure

```text
fullstack-ai-engineer-lab/
  README.md
  ROADMAP.md
  MAKEFILE.md
  .gitignore

  docs/
    architecture/
      overview.md
      monorepo-structure.md
      ai-workspace-architecture.md
    decisions/
      README.md
      0001-repo-centric-workspace.md
      0002-prompt-modularization.md
      0003-hybrid-stack-go-fastapi.md
    learning/
      paths/
        go-backend.md
        fastapi-ai-services.md
        flutter-client.md
        nextjs-web.md
        rag-qdrant.md
        system-design.md
      deep-dives/
        auth-service-deep-dive.md
        rag-system-deep-dive.md
        athar-retrieval-deep-dive.md
        baligh-training-deep-dive.md
      notes/
        weekly/
        monthly/
      source-summaries/
    product/
      workspace-goals.md
      scope-definition.md
      feature-priorities.md
    cheat-sheets/
      git.md
      docker.md
      postgres.md
      qdrant.md
      prompt-design.md

  templates/
    adr.template.md
    project-plan.template.md
    feature-spec.template.md
    architecture-review.template.md
    code-review.template.md
    bug-report.template.md
    debugging-session.template.md
    daily-log.template.md
    weekly-review.template.md
    monthly-review.template.md
    source-doc.template.md
    source-repo.template.md
    source-book.template.md
    source-notebook.template.md
    evaluation-report.template.md

  .ai/
    prompts/
      system/
        workspace-governor.md
        output-format-rules.md
      roles/
        learning-coach.md
        project-planner.md
        system-architect.md
        pair-programmer.md
        code-reviewer.md
        debugging-specialist.md
        source-learning-agent.md
        principal-system-designer.md
      tasks/
        feature-builder.md
        adr-writer.md
        source-extractor.md
        implementation-planner.md
        review-summarizer.md
      critics/
        architecture-validator.md
        code-quality-validator.md
        prompt-auditor.md
      repair/
        retry-with-missing-context.md
        simplify-overengineered-plan.md
        fix-output-format.md
    workflows/
      feature/
        01-plan.md
        02-design.md
        03-build.md
        04-review.md
        05-fix.md
        06-reflect.md
      debugging/
        01-symptom-capture.md
        02-hypothesis-ranking.md
        03-diagnostics.md
        04-fix-verification.md
      learning/
        learn-from-docs.md
        learn-from-repo.md
        learn-from-book.md
        learn-from-notebook.md
        source-to-exercise.md
      architecture/
        propose-decision.md
        record-adr.md
        review-architecture.md
      evaluation/
        ai-feature-eval.md
        prompt-regression.md
        rag-quality-check.md

  registries/
    prompt-registry.yaml
    workflow-registry.yaml
    template-registry.yaml
    decision-log.yaml
    skills-registry.yaml

  learning-sources/
    source-index.md
    books/
    repos/
    notebooks/
    official-docs/

  evaluations/
    prompts/
      golden-cases/
      regressions/
    rag/
      datasets/
      reports/
      baselines/
    projects/
      auth-service/
      rag-system/
      capstone/

  projects/
    00-core-foundations/
      go/
      git-linux/
      ds-algo/
    01-backend-go/
      01-auth-service/
        README.md
        plan.md
        notes.md
        ai-review.md
        mistakes.md
        src/
        tests/
      02-user-service/
      03-chat-service/
    02-frontend/
      flutter-app/
      nextjs-web/
    03-databases/
      postgres-design/
      redis-cache/
      qdrant-rag/
    04-ai-engineering/
      prompt-engineering/
      embeddings/
      rag-system/
      agents/
    05-system-design/
      chatgpt-clone-design.md
      saas-architecture.md
    06-devops/
      docker/
      ci-cd/
      deployment/
    07-capstone/
      thanaweyagpt/
        backend/
        frontend/
        ai/
        infra/
        docs/

  infra/
    docker/
      docker-compose.yml
      postgres/
      redis/
      qdrant/
    scripts/
      setup.sh
      dev-run.sh
      seed-db.sh
      new-adr.sh
      new-review.sh
      new-source-note.sh

  tests/
    prompts/
    workflows/
    templates/
    repo-structure/
```


## Key files

| File path | Purpose | Why it exists | Key contents |
| :-- | :-- | :-- | :-- |
| `README.md` | repo entry | يشرح الهدف والقواعد والبنية | overview, stack, workflow rules [^1] |
| `ROADMAP.md` | learning progression | يربط phases بالمشاريع | phases, milestones [^1] |
| `docs/decisions/README.md` | ADR index | يمنع ضياع القرارات | ADR table, statuses |
| `.ai/prompts/roles/project-planner.md` | feature planning prompt | توحيد التخطيط | scope, tasks, MVP-first [^1] |
| `.ai/workflows/feature/01-plan.md` | plan workflow entry | بداية أي feature | inputs, artifacts, exit criteria |
| `templates/adr.template.md` | ADR standard | اتساق القرارات | context, decision, consequences |
| `registries/prompt-registry.yaml` | prompt inventory | versioning وownership | prompt id, owner, scope, status |
| `learning-sources/source-index.md` | source map | تنظيم المصادر | source type, topic, status |
| `evaluations/rag/reports/` | AI quality evidence | لأن RAG يحتاج قياس | eval reports, failure cases |
| `infra/scripts/new-adr.sh` | automation helper | تقليل friction | generate numbered ADR |

# 6) Agents Design

## Agents table

| Agent Name | Role | Responsibilities | Inputs | Outputs | Tools Access | Skills Used | Prompt Used | Invocation Trigger | Failure Handling | Notes |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Learning Coach | mentor mode | شرح، تحديات، active recall، gap detection | topic, current level, source | lesson, exercise, gaps | repo docs only | teaching, questioning, evaluation | `roles/learning-coach.md` | عند طلب تعلم موضوع | إذا context ناقص: يطلب open questions داخل artifact | أساسي للمستخدم [^1] |
| Project Planner | planning mode | تفكيك feature إلى tasks وMVP | feature request, constraints | plan.md | templates, docs | scoping, decomposition | `roles/project-planner.md` | بداية أي feature | output to `open-questions` if scope unclear | موجود صراحة في الخطة [^1] |
| System Architect | architecture mode | تصميم عالي المستوى، مكونات، مخاطر، tradeoffs | feature/system idea | architecture review/doc | docs, ADR templates | architecture design | `roles/system-architect.md` | features الكبيرة أو services | إذا over-engineered: pass to simplifier | صريح في الخطة [^1] |
| Pair Programmer | guided implementation | تقسيم التنفيذ لخطوات صغيرة | code task, current code | next steps, partial guidance | project code | implementation sequencing | `roles/pair-programmer.md` | أثناء البناء | إذا task ambiguous: send to planner | ليس autonomous coder [^1] |
| Code Reviewer | review mode | readability, maintainability, security, performance | code diff/files | ai-review.md | code files, templates | code review | `roles/code-reviewer.md` | بعد implementation | flags severity, no rewrite by default | صريح [^1] |
| Debugging Specialist | bug triage mode | root causes, hypotheses, diagnostics, investigation steps | bug report, logs, code context | debugging session doc | logs/code | debugging, ranking | `roles/debugging-specialist.md` | عند bug/error | if insufficient evidence: request diagnostics | صريح [^1] |
| Source Learning Agent | source extraction | تحويل doc/repo/book/notebook إلى structured lesson | source file/link/notes | source summary + exercises | learning sources | extraction, synthesis | `roles/source-learning-agent.md` | عند دراسة مصدر | if source weak: mark low-confidence sections | موجود في v2 scaffold [^1] |
| Principal System Designer | senior design mode | system design, scale, bottlenecks, data flow | system problem | design doc | docs | system design | `roles/principal-system-designer.md` | capstone/large systems | degrade to architect if scope smaller | صريح كsystem designer prompt [^1] |

## لماذا هذا التقسيم الأنسب

هذا التقسيم يغطي الاحتياجات المؤكدة في الخطة: التعلم، التخطيط، التصميم، التنفيذ الموجّه، المراجعة، debugging، وsystem design. لا توجد حاجة حاليًا إلى runtime agents إضافية مثل security/devops/product managers ككيانات مستقلة داخل repo لأن نفس الوظائف يمكن تمثيلها مؤقتًا كprompts/task modes أو review templates.[^1]

## Single-agent vs multi-agent

- استخدم **single-agent mode** في:
    - شرح موضوع
    - code review
    - bug triage
    - small feature planning
- استخدم **multi-step/multi-role flow** في:
    - feature كبير
    - architecture-heavy change
    - capstone planning
    - RAG system design[^1]


## ما الذي لا يجب أن يكون agent

- template rendering
- ADR numbering
- file scaffolding
- prompt registry lookups
- repo structure validation
هذه يجب أن تكون scripts أو services بسيطة، لا agents.


# 7) Skills Design

| Skill Name | Purpose | Reusable by which agents | Inputs | Outputs | Internal logic summary | Dependencies | Failure modes | Test strategy |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Scope Decomposition | تفكيك feature/tasks | Planner, Architect, Pair Programmer | feature description | task tree | identify MVP, dependencies, blockers | templates | vague scope | golden planning cases |
| Architecture Framing | تصميم الأنظمة | Architect, Principal Designer | requirements | components, risks, tradeoffs | components, data flow, failure points | ADR templates | over-design | architecture fixtures |
| Guided Teaching | تعلم موجّه | Learning Coach, Source Agent | topic/source | explanation + challenge | explain, example, exercise, recall | source docs | too much solutioning | output rubric |
| Code Review Analysis | مراجعة الكود | Code Reviewer | code/diff | findings/severity | inspect architecture, security, maintainability | review template | vague findings | review snapshots |
| Debugging Triage | تشخيص الأعطال | Debugger | symptoms/logs | ranked hypotheses | symptom → hypothesis → diagnostics | bug template | premature conclusion | seeded bug cases |
| Source Extraction | استخلاص المعرفة | Source Agent | source material | summary, concepts, exercise | detect source type, extract key ideas | source templates | shallow extraction | source-based goldens |
| Evaluation Planning | تخطيط التقييم | Architect, Reviewer | feature/system context | eval plan | define metrics, cases, risks | eval template | missing measurable criteria | metric presence checks |
| ADR Writing | توثيق القرارات | Architect, Planner | design decision | ADR doc | context, options, decision, consequences | ADR template | weak rationale | ADR rubric |

## الفرق بين agent وskill وtool وservice وworkflow step

- **Agent**: دور منطقي يملك responsibility وحدود output واضحة.
- **Skill**: capability قابلة لإعادة الاستخدام داخل أكثر من agent.
- **Tool**: interface خارجي أو utility، مثل script أو DB أو API.
- **Service**: component برمجي ثابت يقدم وظيفة مستقلة.
- **Workflow step**: خطوة إجرائية داخل تسلسل تنفيذ.

مثال:
`Code Reviewer` = agent، `Code Review Analysis` = skill، `new-review.sh` = tool/script، `review storage in docs` = service-like capability داخل repo، `04-review.md` = workflow step.

# 8) Prompt Architecture

## Structure

### System prompts

- `system/workspace-governor.md`
- `system/output-format-rules.md`


### Role prompts

- `roles/learning-coach.md`
- `roles/project-planner.md`
- `roles/system-architect.md`
- `roles/pair-programmer.md`
- `roles/code-reviewer.md`
- `roles/debugging-specialist.md`
- `roles/source-learning-agent.md`
- `roles/principal-system-designer.md`


### Task prompts

- `tasks/feature-builder.md`
- `tasks/adr-writer.md`
- `tasks/source-extractor.md`
- `tasks/implementation-planner.md`
- `tasks/review-summarizer.md`


### Critic / validator prompts

- `critics/architecture-validator.md`
- `critics/code-quality-validator.md`
- `critics/prompt-auditor.md`


### Retry / repair prompts

- `repair/retry-with-missing-context.md`
- `repair/simplify-overengineered-plan.md`
- `repair/fix-output-format.md`


## Prompt files

| File name | Scope | When used | Owner component | Expected output shape | Constraints | Anti-hallucination rules |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| `workspace-governor.md` | global operating rules | prepend to most runs | prompt runtime policy | bounded markdown | repo-first, no invented scope | rely only on given repo context |
| `project-planner.md` | feature planning | start of feature | planner agent | task list + artifacts | MVP-first | mark open questions |
| `system-architect.md` | architecture design | pre-implementation | architect agent | system breakdown | no code | no unstated infra assumptions |
| `code-reviewer.md` | code review | after coding | reviewer | findings, severity, fixes | no rewrite unless asked | cite exact files/areas |
| `debugging-specialist.md` | bug investigation | on error | debugger | ranked hypotheses | no jumping to conclusion | require evidence |
| `source-learning-agent.md` | source summarization | on source study | source agent | concepts, examples, exercise | source-grounded | separate confirmed vs inferred |
| `prompt-auditor.md` | prompt QA | before adopting prompt | critic | findings + risks | focus on scope/constraints | identify prompt sprawl |
| `simplify-overengineered-plan.md` | reduce complexity | if architecture bloats | repair | simplified plan | preserve scope | remove unjustified agents/layers |

## Prompt layering strategy

1. Global governor
2. Role prompt
3. Task prompt
4. Output format rules
5. Optional critic/repair pass

## Versioning strategy

`prompt-registry.yaml` stores:

- id
- path
- owner
- version
- status
- last-reviewed
- used-by workflows


## Evaluation strategy

- golden inputs for each prompt
- regression snapshots
- manual rubric on specificity, constraint adherence, and non-invention
- fail if output adds unjustified components


## Guardrails

- source-constrained behavior
- explicit missing inputs section
- no monolithic prompts unless justified
- no code generation in architecture/review modes unless task explicitly requires it


# 9) Workflow Design

## A. Sequential execution flow

### Feature workflow

START
→ `feature/01-plan.md`
→ produce `plan.md`
→ `feature/02-design.md`
→ produce `architecture-review.md` or ADR draft
→ `feature/03-build.md`
→ code in project folder
→ `feature/04-review.md`
→ produce `ai-review.md`
→ `feature/05-fix.md`
→ update code + `mistakes.md`
→ `feature/06-reflect.md`
→ update learning notes
→ END[^1]

### Debugging workflow

START
→ symptom capture
→ hypotheses ranking
→ diagnostics steps
→ fix verification
→ document root cause
→ END

### Learning workflow

START
→ choose source type
→ source-specific workflow
→ source summary artifact
→ practical exercise
→ review understanding
→ link to project task
→ END

## B. Agentic decision flow

START
→ classify request:

- learning
- feature
- bug
- architecture
- review

If learning
→ Source Learning Agent or Learning Coach
→ exercise generation
→ checkpoint

If feature
→ Project Planner
→ System Architect if needed
→ Pair Programmer
→ Code Reviewer

If bug
→ Debugging Specialist
→ diagnostics
→ fix verification

If architecture-heavy
→ Principal System Designer
→ ADR Writer
→ Architecture Validator

END

## Entry points

- new feature request
- bug report
- new learning topic
- source to study
- architecture decision candidate
- code ready for review


## Branching logic

- If feature touches system boundaries → architecture step mandatory.
- If source is repo/notebook/docs/book → use matching learning workflow.
- If bug reproducible → diagnostics first; else improve evidence capture.
- If output includes major tech choice → ADR candidate.


## Approval checkpoints

- plan approved before build
- architecture approved before large implementation
- review complete before marking feature done
- ADR accepted before irreversible architectural change


## Retry logic

- missing context → `retry-with-missing-context.md`
- too much complexity → `simplify-overengineered-plan.md`
- invalid output shape → `fix-output-format.md`


## Fallback flow

إذا planner غير كافٍ، escalate إلى architect.
إذا architect overbuilds، run simplifier.
إذا reviewer findings كثيرة، return to build/fix loop.

## Human-in-the-loop moments

- accept scope
- approve architecture
- decide on unresolved tradeoffs
- validate exercises/learning gaps
- approve ADR status


## Stop conditions

- required artifact generated
- review findings addressed or explicitly deferred
- acceptance criteria met
- open questions documented if blocking


## Success criteria

- deterministic file outputs
- no undocumented architectural decisions
- every feature has plan + review + reflection
- every studied source yields actionable artifact


# 10) Data Contracts and Schemas

## `AgentState`

- purpose: تتبع تنفيذ دور منطقي في workflow
- fields:
    - `agent_name: string`
    - `task_id: string`
    - `input_refs: string[]`
    - `status: enum[pending,running,blocked,done]`
    - `output_refs: string[]`
    - `notes: string[]`
- required: all except `notes`
- validation: `agent_name` must exist in registry

Example:

```json
{
  "agent_name": "Project Planner",
  "task_id": "feat-auth-refresh",
  "input_refs": ["projects/01-backend-go/01-auth-service/feature-spec.md"],
  "status": "done",
  "output_refs": ["projects/01-backend-go/01-auth-service/plan.md"],
  "notes": ["MVP chosen over OAuth2"]
}
```


## `TaskState`

- purpose: track workflow task
- fields:
    - `task_id: string`
    - `type: enum[feature,bug,learning,review,decision]`
    - `owner_role: string`
    - `project_path: string`
    - `phase: string`
    - `status: enum[todo,doing,blocked,done]`
    - `acceptance_criteria: string[]`
    - `blocking_questions: string[]`
- required: all except `blocking_questions`


## `MemoryRecord`

- purpose: long-term repo memory entry
- fields:
    - `id: string`
    - `kind: enum[lesson,decision,review,bug,eval]`
    - `title: string`
    - `source_path: string`
    - `tags: string[]`
    - `summary: string`
    - `freshness_date: string`
- validation: source path must exist


## `PromptRegistryEntry`

- fields:
    - `id`
    - `path`
    - `owner`
    - `version`
    - `status`
    - `used_by`
    - `last_reviewed`
    - `constraints`


## `WorkflowExecutionLog`

- fields:
    - `workflow_id`
    - `run_date`
    - `entry_point`
    - `steps_completed`
    - `artifacts_created`
    - `failures`
    - `next_action`


## `ToolRequestResponse`

for scripts:

- request:
    - `script_name`
    - `args`
    - `cwd`
- response:
    - `exit_code`
    - `stdout_path`
    - `stderr_path`
    - `generated_files`


## `EvaluationResult`

- fields:
    - `system_name`
    - `eval_type`
    - `dataset_name`
    - `metrics`
    - `failures`
    - `accepted`
    - `report_path`


# 11) Tooling and Integrations

## Git / GitHub

- purpose: versioning, PR workflow, review traceability
- interface style: git CLI + GitHub PRs
- request contract: branch, commit, PR description referencing artifacts
- response contract: commit history, PR discussion
- auth/config: Git credentials
- timeout/retry: n/a
- failure handling: branch sync + rebase policy
- observability: commit messages, PR links


## Docker / Docker Compose

- purpose: local infra for projects
- interface style: CLI
- request contract: compose file + env
- response contract: running services, logs
- auth/config: env files
- timeout/retry: service startup retries
- failure handling: health checks + logs
- observability: container logs, health status


## PostgreSQL

- purpose: relational persistence for backend projects
- interface style: SQL / ORM / migrations
- request contract: schema, queries
- response contract: rows, transactions
- auth/config: DB URL, credentials
- timeout/retry: app-level retries only where safe
- failure handling: migration rollback strategy
- observability: slow query logs


## Redis

- purpose: cache/session/pub-sub as needed
- interface style: key-value commands
- request contract: key patterns, TTL expectations
- response contract: value, cache hit/miss
- auth/config: connection URL
- failure handling: fallback to primary store
- observability: hit rate, latency


## Qdrant

- purpose: vector storage for RAG projects
- interface style: HTTP/gRPC API
- request contract: collection name, vectors, metadata filters
- response contract: matches with scores
- auth/config: host, API key if configured
- timeout/retry: bounded query retries
- failure handling: fallback to lexical/hybrid strategy if implemented
- observability: query latency, recall-oriented eval reports


## FastAPI AI Service

- purpose: AI/RAG endpoints in monorepo target architecture
- interface style: HTTP REST
- request contract:
    - `/ai/chat`
    - `/ai/embeddings`
    - `/ai/rag/query`
    - `/ai/agents/run`
- response contract: JSON outputs with status/error
- auth/config: API gateway/internal auth
- failure handling: timeout budget, degraded response
- observability: latency, token cost, failures[^1]


## Go API Gateway

- purpose: auth/users/routing/billing/rate limits/core backend
- interface style: REST
- request contract:
    - `/auth/register`
    - `/auth/login`
    - `/user/profile`
    - `/chat`
    - `/rag/query`
    - `/admin/metrics`
- response contract: JSON
- auth/config: JWT config, DB URL, Redis
- failure handling: standard error envelopes
- observability: access logs, error rate[^1]


# 12) Memory and Context Strategy

## Short-term context

يشمل:

- current task description
- current workflow step
- relevant source artifact
- current project folder
- active prompt constraints

هذا ضروري فقط لتنفيذ الخطوة الحالية بشكل صحيح.

## Long-term memory

يخزن داخل repo كـ explicit artifacts:

- ADRs
- review files
- debugging sessions
- learning notes
- source summaries
- eval reports
- mistakes logs[^1]


## ما لا يجب تخزينه

- raw secrets
- transient copied chats بلا تلخيص
- duplicated notes without source linkage
- speculative conclusions without markingها assumptions


## Retrieval strategy

- lookup by path and registry first
- then by folder convention (`docs/decisions`, `evaluations`, `projects/...`)
- optionally future local search index


## Context assembly strategy

For each task:

1. load workflow step
2. load target template
3. load owning prompt
4. load nearest project docs
5. load linked ADR/review if available

## Deduplication / ranking / freshness logic

- latest accepted ADR overrides older proposed drafts
- latest review supersedes older review for same feature revision
- source summaries ranked by direct relevance to current path
- weekly/monthly notes are secondary context only


## Memory safety boundaries

- repo artifacts are trusted only if explicitly accepted/committed
- retrieved source content should not override system/workflow constraints
- external content from books/docs/repos is informational, not executable instruction


# 13) Implementation Phases

## Phase 0: Foundations

- goal: establish repo skeleton and governance
- deliverables:
    - root structure
    - README
    - ROADMAP
    - templates
    - prompt registry
    - workflow registry
    - ADR directory
- dependencies: none
- acceptance criteria:
    - deterministic folder structure exists
    - first templates available
    - first prompts available
- risks:
    - naming inconsistency
    - prompt sprawl


## Phase 1: Core MVP

- goal: make one end-to-end feature workflow operational
- deliverables:
    - feature workflow
    - planner prompt
    - architect prompt
    - reviewer prompt
    - debugger prompt
    - one sample project (`auth-service`)
    - one complete artifact chain: spec → plan → build → review → fix
- dependencies: Phase 0
- acceptance criteria:
    - at least one feature completed with all artifacts
    - no missing template in path
- risks:
    - too many prompts before proving flow


## Phase 2: Reliability

- goal: stabilize outputs and learning loops
- deliverables:
    - learning workflows for docs/repo/book/notebook
    - source templates
    - prompt audits
    - tests for prompts/workflows/templates
- dependencies: Phase 1
- acceptance criteria:
    - source-learning path works for 2–3 real sources
    - prompt registry updated
- risks:
    - shallow source extraction
    - too much manual inconsistency


## Phase 3: Scale / Optimization

- goal: support larger multi-project use
- deliverables:
    - scripts for scaffolding
    - repo validation tests
    - evaluation folders
    - improved registries
    - project-level deep dives
- dependencies: Phase 2
- acceptance criteria:
    - new project/service can be scaffolded rapidly
    - reviews and ADRs indexed automatically
- risks:
    - automation drift from actual workflow


## Phase 4: Advanced Features

- goal: AI-production readiness for Athar/Baligh/capstone
- deliverables:
    - RAG eval harness folders
    - project-specific templates
    - advanced architecture docs
    - CI hooks
    - optional local retrieval/search
- dependencies: Phase 3
- acceptance criteria:
    - RAG project has eval reports + ADRs + design docs
    - capstone structure executable
- risks:
    - premature platformization
    - mixing generic lab concerns with product-specific constraints


# 14) Testing and Evaluation

## Unit tests

- scripts like `new-adr.sh`
- template generation correctness
- registry schema validation


## Integration tests

- feature workflow produces expected files
- learning workflow maps source → summary → exercise
- review workflow links to project correctly


## Workflow tests

- ensure each workflow has:
    - entry
    - artifacts
    - exit criteria
- fail if required files are omitted


## Prompt regression tests

- golden prompts with fixed inputs
- verify:
    - no invented requirements
    - bounded structure
    - correct section coverage


## Agent behavior tests

- planner should output MVP-first
- reviewer should not rewrite code by default
- debugger should rank hypotheses before fix
- source agent should separate confirmed vs inferred


## Golden test cases

- feature request for auth refresh token
- bug report for JWT expiry issue
- source-learning from a Go doc
- architecture question for RAG baseline


## Hallucination / failure tests

- ambiguous feature with missing constraints
- incomplete source
- conflicting notes
- over-engineered architecture response


## Latency / cost checks

لأن النظام repo-centric وليس runtime LLM platform، القياس هنا يكون على:

- prompt verbosity
- number of required passes
- artifact completeness per run
وفي المشاريع AI الفعلية لاحقًا:
- token usage
- eval runtime
- retrieval latency


## ماذا سنقيس

- completeness
- specificity
- adherence to file conventions
- ability to start implementation without guessing
- output repeatability
- presence of explicit assumptions


## كيف نحدد النجاح

النجاح يعني أن مهندس backend/AI يستطيع أخذ artifact ناتج من workflow وبدء التنفيذ أو المراجعة مباشرة دون سؤال إضافي كبير.

## الحالات الحرجة

- plan without file structure
- architecture with unnecessary agents
- review without severity
- learning note without project linkage
- ADR without consequences


# 15) Risks, Assumptions, and Open Questions

## Assumptions

- المستخدم يريد repo-centric implementation system وليس منصة SaaS مستقلة الآن.[^1]
- prompt roles الحالية تمثل operating modes أكثر من كونها distributed agents.[^1]
- stack المستهدف للمشاريع الكبيرة هو Go + FastAPI + Flutter + Next.js + Postgres + Redis + Qdrant.[^1]
- Athar/Baligh سيحتاجان لاحقًا eval-heavy AI architecture داخل نفس ecosystem.[^1]


## Risks

- تحويل كل capability إلى agent يزيد التعقيد بلا فائدة.
- تضخم عدد prompts بدون ownership واضح.
- تكرار المعرفة بين learning notes وproject notes وdocs.
- غياب automated validation للهيكل يؤدي إلى drift.
- مزج generic learning system مع product-specific architecture مبكرًا.


## Open Questions

- هل سيكون الجذر النهائي `99-ai-workflow/` أم `.ai/` أم كلاهما مع طبقة توافق؟
- هل مشاريع frontend الأساسية ستكون Flutter أولًا أم Next.js أولًا في التنفيذ اليومي؟
- هل نريد CLI generator فعلي في Phase 1 أو نؤجله إلى Phase 3؟
- ما مستوى الصرامة المطلوب في prompt tests: snapshot فقط أم rubric + linting؟
- هل source-learning outputs يجب أن تكون English-first مع Arabic summaries دائمًا؟


## Decision Log Candidates

- repo namespace: `.ai/` vs `99-ai-workflow/`
- canonical project layout under `projects/` vs flat phase folders
- whether reviews live next to project or centrally indexed
- whether prompt registries are YAML only or YAML + JSON schema
- whether capstone remains ThanaweyaGPT as canonical final project[^1]


# 16) Immediate Build Checklist

- إنشاء:
    - `README.md`
    - `ROADMAP.md`
    - `docs/decisions/README.md`
    - `templates/adr.template.md`
    - `templates/project-plan.template.md`
    - `templates/code-review.template.md`
    - `templates/debugging-session.template.md`
    - `templates/source-*.template.md`
- كتابة أول prompts:
    - `roles/project-planner.md`
    - `roles/system-architect.md`
    - `roles/code-reviewer.md`
    - `roles/debugging-specialist.md`
    - `roles/source-learning-agent.md`
    - `roles/learning-coach.md`
- تنفيذ أول agents منطقيًا:
    - Project Planner
    - Code Reviewer
    - Debugging Specialist
    - Source Learning Agent
- تشغيل أول workflow end-to-end:
    - `feature/01-plan.md` إلى `feature/06-reflect.md` على `projects/01-backend-go/01-auth-service/`
- بناء أول tests:
    - prompt regression for planner/reviewer/debugger
    - template existence test
    - workflow completeness test
- ما يمكن تأجيله:
    - CLI scaffolding
    - local semantic search
    - CI integration
    - advanced RAG eval harness
    - dashboard UI


# 17) Final Deliverable View

## Architecture snapshot

النظام النهائي هو **Production-Grade AI Engineering Workspace** داخل repo واحد، يجمع:

- learning system
- project execution system
- modular prompts
- structured workflows
- review/evaluation artifacts
- ADR-based architectural memory
- project scaffolds للمسار الكامل من foundations إلى capstone.[^1]


## Minimal viable implementation path

1. Build repo skeleton
2. Add templates
3. Add 5 core role prompts
4. Add feature + debugging + learning workflows
5. Run first end-to-end on auth-service
6. Add ADRs and review artifacts
7. Expand to RAG system and capstone

## Recommended first milestone

**Milestone 1: Operational MVP Workspace**
يعتبر منجزًا عندما يتم تنفيذ feature واحد كامل داخل `auth-service` مع:

- feature spec
- plan
- architecture note or ADR
- implementation notes
- code review
- bug/debug doc if needed
- reflection/learning note[^1]


## Definition of done for MVP

- repo structure ثابت ومفهوم
- prompts الأساسية موجودة ومفهرسة
- workflows الأساسية موجودة وتنتج artifacts واضحة
- one backend project completed through the full lifecycle
- ADR system يعمل
- source-learning workflow يعمل على مصدر حقيقي واحد على الأقل
- no major folder or artifact remains ambiguous or unnamed

<div align="center">⁂</div>

[^1]: 7-Day-Full-Stack-AI-Plan.md

