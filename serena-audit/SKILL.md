---
name: serena-audit
description: >
  Reconcile and update every Serena memory file against its source repository.
  Use when the user asks to reconcile memory.
triggers:
  all:
    files: ".serena/memories/"
    request: "reconcile memory, memory audit, audit memory, реконсиляция памяти"
requires:
  - serena-protocol
---

# SKILL: Serena Memory Reconciler

Keep the entire Serena memory store in sync with the repositories it describes.
This skill covers **all** memory scopes: `agent/`, `project/`, `meta/`,
`prompts/`, `templates/`, `entities/`, `bugs/`, `decisions/`, `notes/`,
`style/`, `plans/`, `proposals/`, `proposal/`, `reports/`, `todo/`, `logic/`,
`guide/`, `artifacts/`, and `playbook/`.

## Skill Boundary

- **This skill owns** the two-phase reconciliation workflow: scan every memory
  file, detect drift, produce an update plan, then execute per-memory updates.
- **This skill does NOT own** the rules that define how memories are named,
  routed, or formatted. Those live in `serena-protocol` and MUST be
  loaded automatically.
- **This skill does NOT own** entity-card creation. If an entity-scoped memory
  exists but `entities/<entity>` is missing, STOP and ask the user to create the
  card via `project-audit`.
- **This skill does NOT own** business-domain analysis. If a `logic/<entity>/...`
  memory needs domain-level refresh, delegate to the `business-audit`
  subagent prompt.

## Lazy-Load Protocol

Do not read every reference file. Use the Routing Index below to load only the
sections needed for the current sub-task.

### Routing Index

| Trigger | File | Anchor |
|---|---|---|
| Full phase-1 orchestration (scan, classify, plan) | `references/01_reconcile_and_plan.md` | `[ref: #smr-reconcile]` |
| Subagent prompt for the initial memory scan | `references/02_reconciliation_subagent_prompt.md` | `[ref: #smr-scan-prompt]` |
| Plan-memory format and routing | `references/03_plan_writer.md` | `[ref: #smr-plan]` |
| Full phase-2 orchestration (execute the plan) | `references/04_execute_update.md` | `[ref: #smr-execute]` |
| Subagent prompt for updating one memory | `references/05_per_memory_subagent_prompt.md` | `[ref: #smr-update-prompt]` |
| Validation checklist and edit rules | `references/06_validation_and_edits.md` | `[ref: #smr-validate]` |
| Header-validation script (stub) | `scripts/validate_memory_frontmatter.py` | `[ref: #smr-script]` |

Extract a reference section with `rg` (example):

```bash
rg -A 200 '^\[ref: #smr-scan-prompt\]' \
  serena-audit/references/02_reconciliation_subagent_prompt.md
```

Stop reading when you reach the next `[ref: #...]` marker or the end of the
relevant subsection.

## Master Execution Workflow

When the user asks to reconcile or update Serena memories, execute this
workflow. For full details, lazy-load the anchors above.

1. **Phase 1 — Reconcile and plan.**
   - Enumerate every `.md` file under `.serena/memories/`.
   - Immediately rename any file or directory whose name violates the
     `serena-protocol` naming rules (`[ref: #serena-naming]`).
   - Run the validation script stub (`scripts/validate_memory_frontmatter.py`)
     and review its output.
   - Launch a read-only `explore` subagent with the scan prompt
     (`[ref: #smr-scan-prompt]`). Give it absolute paths, not memory contents.
   - For each memory, determine the correct git source and current `HEAD`
     metadata (`[ref: #smr-git-source]`).
   - Classify every discrepancy (`stale_commit`, `stale_branch`, `stale_date`,
     `legacy_header`, `invalid_frontmatter`, `title_mismatch`, `source_missing`,
     `source_lines_changed`, `entity_card_missing`, `contradiction`,
     `naming_violation`).
   - Write the reconciliation plan to a `plans/...` memory
     (`[ref: #smr-plan]`).

2. **Phase 2 — Execute the plan.**
   - Read the plan and break it into per-memory to do list tasks.
   - For each task, launch a subagent with the per-memory update prompt
     (`[ref: #smr-update-prompt]`).
   - Validate the subagent's diff report (`[ref: #smr-validate]`).
   - Apply header-only refreshes directly at `.serena/memories/<path>.md`;
     apply content changes through Serena MCP tools with refreshed YAML
     frontmatter.
   - Keep every `write_memory` payload under **25 KB**. For large structured
     data, store the full artifact outside Serena memory (e.g.
     `/tmp/serena_audit_full.json`) and keep the memory entry compact.
   - After every mutation, read the memory back and run
     `just agent-memory-commit` from the project root.

## Determining the git source and `repo` value

[ref: #smr-git-source]

`repo` is a **logical** value; the git directory that supplies `branch`,
`commit`, and `committed_at` is chosen by what actually exists on disk.

A memory file lives under `.serena/memories/<scope>/...`. The first path
segment is the scope.

### Entity-scoped scopes

`entities/`, `bugs/`, `decisions/`, `notes/`, `style/`, `plans/`,
`proposals/`, `reports/`, `todo/`, `logic/`.

- If the path is `<scope>/<entity>/<topic>` (or `<scope>/<entity>` for
  `entities/`), treat it as entity-scoped.
- Map the memory-path entity segment to the git directory and to the canonical
  entity card name (`[ref: #smr-entity-mapping]`).
- Git source order: `<workspace-root>/<git-entity-dir>` → `<workspace-root>` →
  `<workspace-root>/.serena`.
- `repo` value: the canonical **snake_case** entity name when the entity
  directory is the source; otherwise `project` or `serena` matching the chosen
  directory.
- If the path is `<scope>/<topic>` (no entity segment), treat it as
  scope-level. Git source order: `<workspace-root>` → `<workspace-root>/.serena`;
  `repo` is `project` or `serena`.

### Project-wide scope

`project/`.

- Git source order: `<workspace-root>` → `<workspace-root>/.serena`.
- `repo` value: `project` regardless of which directory supplies the commit.
  (If the workspace root is not a git repo, the metadata still comes from
  `.serena`, but the memory logically belongs to the project.)

### Cross-entity / agent scopes

`agent/`, `meta/`, `prompts/`, `templates/`, `artifacts/`, `guide/`,
`playbook/`, and scope-level `proposal/`.

- Git source: `<workspace-root>/.serena`.
- `repo` value: `serena`.

### Project-specific scopes

Any other top-level scope (e.g. `text/`, `tools/`):

- Git source order: `<workspace-root>` → `<workspace-root>/.serena`.
- `repo` value: `project` or `serena` matching the chosen directory.

Collect current metadata with:

```bash
cd <selected-git-source>
git rev-parse --abbrev-ref HEAD         # branch
git rev-parse --short HEAD                # 7-char commit
git log -1 --format=%cd --date=iso-strict # commit timestamp, normalize to UTC Z
```

## Entity name mapping

[ref: #smr-entity-mapping]

Memory paths, entity cards, and git directories may use different forms.
Normalize using the rules in `[ref: #serena-naming]`. Common examples:

| Memory directory | Entity card | Git directory |
|---|---|---|
| `client_api` / `client-api` | `client_api` | `client-api` |
| `payment-method-api` | `payment_method_api` | `payment-method-api` |
| `risk-management-api` | `risk_management_api` | `risk-management-api` |
| `production` | `configs_production` | `production` |
| `staging` | `configs_staging` | `staging` |

Always verify that an entity-scoped memory maps to an existing
`entities/<entity>.md` card before editing.

## Scripts

[ref: #smr-script]

`scripts/validate_memory_frontmatter.py` is a stub. It will eventually scan all
memory files, parse YAML frontmatter, validate mandatory fields, check that the
title matches the first H1, enforce file/directory naming rules, and emit a JSON
report. The root agent and subagents may call it via shell.

## Do Not

- Do not edit memory contents as the root agent during phase 1.
- Do not create missing entity cards implicitly; route them to the user via
  `project-audit`.
- Do not pass full memory contents to subagents; pass absolute file paths.
- Do not write memory files larger than ~25 KB via `write_memory`; split or
  store large artifacts outside Serena memory.
- Do not leave non-compliant memory names in place; rename them immediately.
- Do not forget to refresh the YAML frontmatter on every content edit.
- Do not skip `just agent-memory-commit` after any memory mutation.
