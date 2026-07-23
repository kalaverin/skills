---
name: serena-audit
description: Reconcile and update every Serena memory file against its source repository. Use when the user asks to reconcile memory.
triggers:
  all:
    files: "test -d .serena/memories"
    request: "reconcile memory, memory audit, audit memory, реконсиляция памяти"
draft: true
requires:
  - serena-protocol
---

# SKILL: Serena Memory Reconciler

Keep the entire Serena memory store in sync with the repositories it describes.
This skill covers **all** memory scopes — the single normative registry of scopes and routing rules is `entity-protocol` `[ref: #entity-namespace-registry]`.

## Skill Boundary

- **This skill owns** the two-phase reconciliation workflow: scan every memory
  file, detect drift, produce an update plan, then execute per-memory updates.
- **This skill does NOT own** the rules that define how memories are named,
  routed, or formatted. Those live in `serena-protocol` and MUST be
  loaded automatically.
- **This skill does NOT own** repo-card creation. If a repo-scoped memory
  exists but `repos/<repo>/overview` is missing, STOP and ask the user to create the
  card via `repo-audit`.
- **This skill does NOT own** business-domain analysis. If a `repos/<repo>/...`
  memory needs domain-level refresh, delegate to the `repo-audit`
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

Extract ONLY the relevant section per the canonical loader mechanics in `frontmatter-protocol` `[ref: #lazy-load-routing]` (bounded extraction — never a blind `rg -A N` window; the exact command lives there, not here).

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
   - After every mutation, verify and persist per `serena-protocol`
     `[ref: #serena-memory-mutation]`.

## Determining the git source and `repo` value

[ref: #smr-git-source]

`repo` is a **logical** value; the git directory that supplies `branch`,
`commit`, and `committed_at` is chosen by what actually exists on disk.

A memory file lives under `.serena/memories/<scope>/...`. The first path
segment is the scope. Scope definitions and routing are owned by `entity-protocol`
`[ref: #entity-namespace-registry]`; the classification below only maps scope
groups to git sources.

### Repo-scoped scopes

`repos/`, `bugs/`, `decisions/`, `notes/`, `style/`, `plans/`,
`proposals/`, `reports/`, `todo/`, `deprecations/`.

- If the path is `<scope>/<repo>/<topic>` (or `repos/<repo>/...`), treat it as
  repo-scoped.
- Map the memory-path entity segment to the git directory and to the canonical
  repo card name (`[ref: #smr-entity-mapping]`).
- Git source order: `<workspace-root>/<git-entity-dir>` → `<workspace-root>` →
  `<workspace-root>/.serena`.
- `repo` value: the canonical **snake_case** entity name when the entity
  directory is the source; otherwise `generic` (legacy `project`/`serena`
  normalize lazily per `entity-protocol` `[ref: #entity-repo-field]`).
- If the path is `<scope>/<topic>` (no entity segment), treat it as
  scope-level. Git source order: `<workspace-root>` → `<workspace-root>/.serena`;
  `repo` is `generic`.

### Project-wide scope

`project/`.

- Git source order: `<workspace-root>` → `<workspace-root>/.serena`.
- `repo` value: `generic` regardless of which directory supplies the commit.
  (If the workspace root is not a git repo, the metadata still comes from
  `.serena`, but the memory logically belongs to the project.)

### Cross-entity / agent scopes

`agent/`, `meta/`, `prompts/`, `templates/`, `artifacts/`, `guide/`,
`playbook/`, and scope-level `proposal/`.

- Git source: `<workspace-root>/.serena`.
- `repo` value: `generic`.

### Project-specific scopes

Any other top-level scope (e.g. `text/`, `tools/`):

- Git source order: `<workspace-root>` → `<workspace-root>/.serena`.
- `repo` value: `generic`.

Collect current metadata per the canonical git triplet — `[ref: #tracking-git-commands]` — run inside `<selected-git-source>`.

## Entity name mapping

[ref: #smr-entity-mapping]

Memory paths, repo cards, and git directories may use different forms.
Normalize using the rules in `[ref: #serena-naming]`. Common examples:

| Memory directory | Entity card | Git directory |
|---|---|---|
| `client_api` / `client-api` | `client_api` | `client-api` |
| `payment-method-api` | `payment_method_api` | `payment-method-api` |
| `risk-management-api` | `risk_management_api` | `risk-management-api` |
| `production` | `configs_production` | `production` |
| `staging` | `configs_staging` | `staging` |

Always verify that a repo-scoped memory maps to an existing
`repos/<repo>/overview` card before editing.

## Scripts

[ref: #smr-script]

`scripts/validate_memory_frontmatter.py` is a stub. It will eventually scan all
memory files, parse YAML frontmatter, validate mandatory fields, check that the
title matches the first H1, enforce file/directory naming rules, and emit a JSON
report. The root agent and subagents may call it via shell.

## Do Not

- Do not edit memory contents as the root agent during phase 1.
- Do not create missing repo cards implicitly; route them to the user via
  `repo-audit`.
- Do not pass full memory contents to subagents; pass absolute file paths.
- Do not write memory files larger than ~25 KB via `write_memory`; split or
  store large artifacts outside Serena memory.
- Do not leave non-compliant memory names in place; rename them immediately.
- Do not forget to refresh the YAML frontmatter on every content edit.
- Do not skip `just serena-checkpoint` after any memory mutation.
