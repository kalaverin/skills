---
name: project-audit
description: >
  MANDATORY skill for creating, updating, or studying a Serena entity card
  for a service, library, repository, infrastructure component, or any other
  project entity. Load this skill when the user asks to create a card, study
  an entity, explore a project/service/library/repository, or gather
  information for an entity card. The skill orchestrates a read-only exploration
  subagent and writes the final card to `entities/<entity>` plus focused
  finding memories.
triggers:
  request: "create entity card, create project card, create service card, create repository card, entity card, project card, service card, repository card, explore project, explore service, explore repository, study project, study service, study repository, изучи проект, изучи сервис, изучи репозиторий, создай карточку проекта, создай карточку сервиса, создай карточку репозитория"
requires:
  - serena-protocol
---

# project-audit

Create and maintain Serena entity cards via a read-only exploration subagent.
This skill handles services, libraries, repositories, and infrastructure/GitOps
entities.

## Skill Boundary

- **This skill owns** the operational workflow for producing an entity card:
  root-agent orchestration, subagent exploration prompt, writing instructions,
  common skeleton, and type-specific templates.
- **This skill does NOT own** general Serena memory rules (scopes, routing,
  naming, metadata, mutation, verify/persist). Those live in
  `serena-protocol`. Load it automatically whenever this skill is used.
- **This skill does NOT own** language-specific coding standards. Load
  `python-lang` when the entity is a Python project and the task also requires
  editing Python code.
- **This skill does NOT own** protocol/schema design. Load
  `protobuf-lang` or `api-design` when the card work also
  involves designing or changing `.proto`/OpenAPI definitions.

## Lazy-Load Protocol

Do not read every reference file. Use the Routing Index below to load only the
sections needed for the current sub-task.

### Routing Index

| Trigger | File | Anchor |
|---|---|---|
| Full root-agent orchestration | `references/01_make_card.md` | `[ref: #pe-make-card]` |
| Card goal / input / constraints only | `references/01_make_card.md` | `[ref: #pe-make-card-goal]`, `[ref: #pe-make-card-input]`, `[ref: #pe-make-card-constraints]` |
| Step-by-step orchestration only | `references/01_make_card.md` | `[ref: #pe-make-card-steps]` |
| Final writing instructions and section order | `references/02_service_card_writer.md` | `[ref: #pe-writer]` |
| Read-only exploration subagent prompt | `references/03_service_card_explorer.md` | `[ref: #pe-explorer]` |
| Common skeleton and agent rules | `references/04_service_card_common.md` | `[ref: #pe-common]`, `[ref: #pe-common-agent-rules]`, `[ref: #pe-common-skeleton]` |
| gRPC service type | `references/05_grpc_service.md` | `[ref: #pe-grpc]` |
| REST API gateway type | `references/06_rest_gateway.md` | `[ref: #pe-rest]` |
| Temporal workflow worker type | `references/07_temporal_worker.md` | `[ref: #pe-temporal]` |
| Infrastructure / GitOps type | `references/08_infrastructure_gitops.md` | `[ref: #pe-infra]` |
| Library type | `references/09_library.md` | `[ref: #pe-library]` |

Extract a reference section with `rg` (example):

```bash
rg -A 200 '^\[ref: #pe-explorer\]' \
  project-audit/references/03_service_card_explorer.md
```

Stop reading when you reach the next `[ref: #...]` marker or the end of the
relevant subsection.

## Master Execution Workflow

When the user asks to create/study an entity card, execute this workflow. For
full details, lazy-load the anchors above.

1. **Identify the entity.** Obtain `entity_name` (`snake_case`) and `entity_path`
   from the user. If unclear, ask before proceeding.
2. **Verify entity card exists.** Check whether `entities/<entity_name>` exists.
   - If no cards exist in `entities/` at all, STOP and ask the user to create
     the first entity card via this skill.
   - If the target entity has no card, STOP and ask the user to create the card
     for `<entity_name>` via this skill or confirm an existing entity name.
   Do not guess.
3. **Load instructions.** Read `references/01_make_card.md`
   (`[ref: #pe-make-card]`) and `references/02_service_card_writer.md`
   (`[ref: #pe-writer]`).
4. **Determine the type.** Use only safe read-only shell checks (`ls`, `test -d`,
   `test -f`) on `entity_path`. Map to one of:
   `gRPC API service`, `REST API gateway`, `Temporal workflow worker`,
   `Infrastructure / GitOps`, `library`. Load the matching type reference
   (`[ref: #pe-grpc]`, `[ref: #pe-rest]`, `[ref: #pe-temporal]`,
   `[ref: #pe-infra]`, `[ref: #pe-library]`).
5. **Collect relevant memory paths.** Build a list of absolute paths to all
   relevant `.serena/memories/` files for this entity:
   `entities/<entity_name>`, `bugs/<entity_name>/...`, `notes/<entity_name>/...`,
   `decisions/<entity_name>/...`, `style/<entity_name>/...`,
   `todo/<entity_name>/...`. Do not read the contents yourself; pass only the
   path list.
6. **Launch read-only exploration subagent.** Create an `explore` subagent with
   the prompt from `references/03_service_card_explorer.md`
   (`[ref: #pe-explorer]`). Provide `entity_name`, `entity_path`, and
   `memory_path_list`. The subagent does not have Serena MCP tools, but it can
   browse the memory tree with `tree --gitignore --prune
   <workspace-root>/.serena/memories` and read the listed markdown files
   directly via shell. Timeout: at least **1800 seconds** (30 minutes); allow
   longer if the subagent needs it.
7. **Generate the directory tree yourself.** Use the exact command from
   `references/04_service_card_common.md` (`[ref: #pe-common-skeleton]`). Do not
   delegate this to the subagent.
8. **Validate the report.** Ensure the exported interface is exhaustive (every
   endpoint, method, workflow/activity, HelmRelease, or public module). Ask
   follow-up questions if anything is missing.
9. **Resolve contradictions.** Compare fresh findings with existing Serena
   memories. Prefer newer memories, `AGENTS.md` over session memory, and the
   entity's own git metadata over `.serena` project metadata. Log resolved and
   unresolved contradictions in `agent/contradictions`.
10. **Write outputs.**
    - Save the final card to `entities/<entity_name>` following the skeleton in
      `references/04_service_card_common.md` (`[ref: #pe-common-skeleton]`) plus
      the type-specific sections.
    - For each finding, write a focused memory to the appropriate namespace as
      defined in `serena-protocol` `[ref: #serena-findings-traceability]`.
11. **Verify and persist.** Read back every saved memory to confirm it was
    written correctly, then run the configured persistence command (commonly
    `just agent-memory-commit`) from the project root before reporting completion.

## Do Not

- Do not explore the codebase directly as the root agent; delegate to the
  read-only subagent.
- Do not pass existing Serena memory contents to the subagent.
- Do not include Sentry, Prometheus, tests, linters, CI, Makefile, Docker, or
  entry points in the final card.
- Do not write environment variable values, defaults, examples, or secrets.
- Do not proceed with an unresolved contradiction; report it to the user."
"
