# Full-Stack AI Engineer Lab — task runner
#
# Works in Git Bash on Windows and on Linux CI. PowerShell-only operations stay in
# infra/scripts/*.ps1; see MAKEFILE.md for the full command reference.
#
# Primary target: `make ci` — the same gates GitHub Actions runs.

DEVMATE   := projects/04-ai-engineering/devmate
COMPOSE   := docker compose -f infra/docker/docker-compose.yml
PY        := poetry run

.DEFAULT_GOAL := help
.PHONY: help ci lint fmt fmt-check types test test-int eval run cli \
        up up-tools down reset ps logs validate docs-check fresh-check clean

## ---------------------------------------------------------------- help

help:  ## Show available targets
	@grep -hE '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

## ---------------------------------------------------------------- quality

ci: lint fmt-check types test docs-check fresh-check  ## Everything CI runs
	@echo "CI passed."

lint:  ## Lint DevMate (ruff)
	cd $(DEVMATE) && $(PY) ruff check .

fmt:  ## Format DevMate in place
	cd $(DEVMATE) && $(PY) ruff format .

fmt-check:  ## Verify formatting without writing
	cd $(DEVMATE) && $(PY) ruff format --check .

types:  ## Type-check DevMate (mypy)
	cd $(DEVMATE) && $(PY) mypy src/

test:  ## Unit tests with coverage
	cd $(DEVMATE) && $(PY) pytest -q --cov=devmate --cov-report=term-missing

test-int:  ## Integration tests (needs `make up`)
	cd $(DEVMATE) && $(PY) pytest -q -m integration

## ---------------------------------------------------------------- devmate

eval:  ## Run the RAG evaluation harness (week 2+)
	cd $(DEVMATE) && $(PY) python eval/run_ragas.py

run:  ## Serve the DevMate API locally
	cd $(DEVMATE) && $(PY) uvicorn devmate.api.main:app --reload

cli:  ## Run the DevMate CLI — make cli ARGS="stats ."
	cd $(DEVMATE) && $(PY) devmate $(ARGS)

## ---------------------------------------------------------------- infra

up:  ## Start Postgres, Redis, Qdrant
	$(COMPOSE) up -d

up-tools:  ## Start infra plus PgAdmin / Redis Commander
	$(COMPOSE) --profile dev-tools up -d

down:  ## Stop containers, keep volumes
	$(COMPOSE) down

reset:  ## Stop containers AND delete all data
	$(COMPOSE) down -v

ps:  ## Container status
	$(COMPOSE) ps

logs:  ## Follow logs — make logs SVC=qdrant
	$(COMPOSE) logs -f $(SVC)

## ---------------------------------------------------------------- workspace

validate:  ## Pester suites (Windows/PowerShell only)
	pwsh -NoProfile -Command "Invoke-Pester tests/"

docs-check:  ## Find broken relative links in docs/
	@fail=0; \
	for f in $$(find docs -name '*.md' -not -path 'docs/plan/archive/*'); do \
	  d=$$(dirname "$$f"); \
	  for l in $$(grep -oE '\]\([^)#][^)]*\.md[^)]*\)' "$$f" 2>/dev/null \
	      | sed -E 's/^\]\(//; s/\)$$//; s/#.*$$//'); do \
	    case "$$l" in http*) continue ;; esac; \
	    [ -f "$$d/$$l" ] || { echo "BROKEN  $$f -> $$l"; fail=1; }; \
	  done; \
	done; \
	[ $$fail -eq 0 ] && echo "docs links OK" || exit 1

fresh-check:  ## Fail if current-focus.md is older than 8 days
	@f=docs/tracking/current-focus.md; \
	s=$$(grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' "$$f" | head -1); \
	a=$$(( ( $$(date +%s) - $$(date -d "$$s" +%s) ) / 86400 )); \
	echo "current-focus.md: $$a day(s) old (stamped $$s)"; \
	[ $$a -le 8 ] || { echo "STALE — update it (weekly review)"; exit 1; }

clean:  ## Remove caches and build artifacts
	find . -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -prune -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -prune -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -prune -exec rm -rf {} + 2>/dev/null || true
	@echo "cleaned."
