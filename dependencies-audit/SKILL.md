---
name: dependencies-audit
description: >
  MANDATORY skill for creating and maintaining exhaustive dependency cards for
  project entities. Produces per-service `logic/<entity>/dependencies.md` and,
  on explicit user request, the project-level `project/dependencies.md`. Use when
  the user asks for dependency cards, service dependencies, dependency map,
  architecture dependencies, or "what does X depend on". Requires an existing
  entity card at `entities/<entity>` and up-to-date business-domain memories at
  `logic/<entity>/`.
triggers:
  all:
    files: ".serena/memories/"
    request: "dependency card, create dependency card, dependency map, create dependency map, architecture dependencies, service dependencies, what does it depend on, карточка зависимостей, создай карточку зависимостей, карта зависимостей, изучи зависимости"
requires:
  - project-audit
  - business-audit
  - serena-protocol
---

# dependencies-audit

Create and maintain exhaustive, source-of-truth dependency cards for every
project entity. A dependency card documents every surface the entity exposes,
every downstream call it makes, every database, external system, library, and
infrastructure component it touches, plus a visual dependency diagram.

## Skill Boundary

- **This skill owns** the dependency-card workflow: inputs, freshness checks,
  specialized subagent prompts, per-service and project-level templates,
  edge-type taxonomy, exhaustiveness rules, and quality checks.
- **This skill does NOT own** the technical entity card. That belongs to
  `project-audit`. This skill requires an existing card at `entities/<entity>`.
- **This skill does NOT own** the business-domain analysis. That belongs to
  `business-audit`. It reuses `logic/<entity>/business_domain_report`,
  `logic/<entity>/processes`, `logic/<entity>/integrations`, and glossaries as
  inputs.
- **This skill does NOT own** general Serena memory rules (scopes, naming,
  YAML frontmatter, metadata, mutation, persistence). Those live in
  `serena-protocol`. Load it automatically whenever this skill is used.
- **This skill does NOT own** memory reconciliation. If existing dependency
  cards or input memories are stale, STOP and ask the user to reconcile via
  `serena-audit` or to refresh the upstream cards first.

## Lazy-Load Protocol

Do not read every reference file. Use the Routing Index below to load only the
sections needed for the current sub-task.

### Routing Index

| Trigger | File | Anchor |
|---|---|---|
| Goal, inputs, constraints, freshness gate, reuse map | `references/01_overview_and_boundary.md` | `[ref: #dcc-overview]` |
| Per-service card template and fill-instructions | `references/02_per_service_template.md` | `[ref: #dcc-per-service-template]` |
| Project-level card template and fill-instructions | `references/03_project_template.md` | `[ref: #dcc-project-template]` |
| Specialized subagent prompts | `references/04_subagent_prompts.md` | `[ref: #dcc-subagents]` |
| Quality checks and exhaustiveness rules | `references/05_quality_checks.md` | `[ref: #dcc-quality]` |

Extract a reference section with `rg` (example):

```bash
rg -A 200 '^\[ref: #dcc-per-service-template\]' \
  dependencies-audit/references/02_per_service_template.md
```

Stop reading when you reach the next `[ref: #...]` marker or the end of the
relevant subsection.

## Master Execution Workflow

When the user asks for a dependency card, execute this workflow. For full
details, lazy-load the anchors above.

1. **Accept exactly one entity per run.**
   - Obtain `entity_name` (`snake_case`) and `entity_path` from the user.
   - If the request mentions multiple entities, STOP and ask the user to pick
     one. Do not batch entities.
   - For a project-level request, see step 10.

2. **Verify the entity card exists.** Apply `[ref: #serena-entity-prerequisite]`
   from `serena-protocol`. If `entities/<entity_name>` does not exist,
   STOP and ask the user to create it via `project-audit`.

3. **Run the freshness gate (HARD).**
   - Read `entities/<entity_name>`, `logic/<entity_name>/business_domain_report`,
     `logic/<entity_name>/integrations`, and `logic/<entity_name>/processes` if
     they exist.
   - For each input memory, compare its frontmatter `commit` with the latest
     commit of the entity's own git repository (`git rev-parse --short HEAD` at
     `entity_path`).
   - Also compare the `commit` values across the input memories for the same
     entity. They should reflect a consistent, recent state of the entity repo.
   - If any input is stale, missing, or inconsistent with the entity repo,
     STOP. Report the exact mismatch to the user and demand reconciliation via
     `serena-audit` or by re-running `project-audit` /
     `business-audit` before proceeding.
   - Do NOT generate a dependency card from stale or unsynchronized inputs.

4. **Ensure naming compliance.** Rename any non-compliant memory paths
   immediately per `[ref: #serena-naming]`.

5. **Collect relevant memory paths.** Build a list of absolute paths to all
   relevant `.serena/memories/` files for this entity:
   - `entities/<entity_name>`
   - `logic/<entity_name>/business_domain_report`
   - `logic/<entity_name>/integrations`
   - `logic/<entity_name>/processes`
   - `logic/<entity_name>/rules`
   - `logic/<entity_name>/entities`
   - `bugs/<entity_name>/...`, `notes/<entity_name>/...`,
     `decisions/<entity_name>/...`, `style/<entity_name>/...`,
     `todo/<entity_name>/...`
   Do not read the contents yourself; pass only the path list.

6. **Determine the entity type.** Reuse the deterministic type-detection
   algorithm from `project-audit` (`[ref: #serena-algo-type-detection]`):
   gRPC API service, REST API gateway, Temporal workflow worker,
   Infrastructure / GitOps, or library.

7. **Launch parallel specialized subagents.** For the single target entity,
   create **four** read-only `explore` subagents in parallel:
   - Interface extractor (`[ref: #dcc-subagents-interface]`).
   - Downstream mapper (`[ref: #dcc-subagents-downstream]`).
   - Infra & libs catalog (`[ref: #dcc-subagents-infra]`).
   - Diagram synthesizer (`[ref: #dcc-subagents-diagram]`).
   Each subagent receives the same memory path list and `entity_path`, plus the
   common base rules (`[ref: #dcc-subagents-base]`). Timeout per subagent: at
   least **1800 seconds** (30 minutes).

8. **Synthesize the dependency card.** Combine the four subagent reports into
   the final `logic/<entity_name>/dependencies.md` using the template from
   `[ref: #dcc-per-service-template]`. Resolve contradictions using
   `[ref: #serena-contradictions]`.

9. **Write the per-service dependency card.**
   - Target: `logic/<entity_name>/dependencies`.
   - Use `write_memory` if new, `edit_memory` if updating.
   - Refresh YAML frontmatter with the entity's own branch, latest short commit
     hash, and latest commit date. `repo` must be the entity's repository name
     (logical name of the source repo), matching `[ref: #serena-metadata-contract]`.
   - `source` should point to the entity's directory and relevant memory files,
     e.g. `<entity-name>/`, `entities/<entity_name>.md`,
     `logic/<entity_name>/business_domain_report.md`.

10. **Project-level card (only on explicit request).**
    - Verify that a `logic/<entity_name>/dependencies` card exists and is fresh
      for **every** entity in `entities/`.
    - If any per-service card is missing or stale, STOP. List the gaps and ask
      the user to create or refresh them first.
    - Read all per-service dependency cards and synthesize `project/dependencies`
      using the template from `[ref: #dcc-project-template]`.
    - `repo` for `project/dependencies` is `serena` because the source of truth
      is the `.serena` memory repository, per `[ref: #serena-metadata-contract]`.

11. **Verify and persist.** Read back every saved memory to confirm it was
    written correctly, then run the configured persistence command (commonly
    `just serena-checkpoint`) from the project root.

## Do Not

- Do not analyze more than one entity in a single per-service run.
- Do not create dependency cards for entities whose `entities/<entity>` card
  does not exist.
- Do not generate from stale input memories. If frontmatter commits do not
  match the entity repo, STOP.
- Do not generate `project/dependencies` unless every entity has a fresh
  per-service dependency card.
- Do not launch a single "analyze everything" subagent; use parallel
  specialized subagents.
- Do not include Sentry, Prometheus, tests, linters, CI, Makefile, Docker, or
  entry points unless they are actual runtime dependencies (e.g., a GitOps repo
  deploying Helm charts).
- Do not write environment variable values, defaults, examples, or secrets.
- Do not skip YAML frontmatter refresh or `just serena-checkpoint` after any
  memory mutation.
