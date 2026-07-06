# Plan-memory format and routing

[ref: #smr-plan]

## Goal

Produce a compact, auditable reconciliation plan. Large structured data lives
outside Serena memory; the plan only contains summary tables and action items.

## Target memory name

Choose one:

- Single-entity reconciliation: `plans/<entity>/serena_reconciliation_plan`
- Multi-entity or workspace-wide reconciliation:
  `plans/project/serena_reconciliation_plan`

If the target name already exists, overwrite it with `write_memory`.

## Size constraint

The plan memory MUST be under **25 KB**. If the full action-item list is too
large, keep only grouped counts in the plan and store the per-item list in
`/tmp/serena_reconciliation_plan.json`.

## Metadata header

Use the current git source for the plan:

- workspace root if it is a git repo → `repo: project`;
- else `.serena` → `repo: serena`.

Refresh all header fields.

## Section order

```markdown
# Serena memory reconciliation plan

**Recorded:** YYYY-MM-DDTHH:MM:SSZ
**Git branch:** <branch>
**Latest commit:** <short-hash>
**Latest commit datetime:** YYYY-MM-DDTHH:MM:SSZ
**Location:** <workspace-root>

## Scope

- Workspace root: `<workspace-root>`
- Memories directory: `.serena/memories/`
- Entities covered: `<list>`
- Cross-entity/agent scopes included: yes / no
- Full audit dump: `/tmp/serena_audit_full.json`

## Summary

| Status | Count |
|---|---|
| ok | N |
| stale_commit | N |
| stale_branch | N |
| stale_date | N |
| legacy_header | N |
| invalid_frontmatter | N |
| title_mismatch | N |
| source_missing | N |
| source_lines_changed | N |
| entity_card_missing | N |
| naming_violation | N |
| no_header | N |
| no_h1 | N |
| contradiction | N |

## High priority action items

| # | Memory path | Scope | Entity | Issue(s) | Current HEAD | Recorded commit | Recommended action | Priority |
|---|---|---|---|---|---|---|---|---|
| 1 | ... | ... | ... | ... | ... | ... | ... | high |

## Medium priority action items

| Issue | Count | Affected scopes/entities | Recommended action |
|---|---|---|---|
| legacy_header | N | ... | Refresh to YAML frontmatter |

## Low priority action items

| Issue | Count | Details | Recommended action |
|---|---|---|---|
| no_header | N | ... | Add YAML frontmatter |
| no_h1 | N | ... | Add generated H1 |

## Blockers

List any items that require user input before proceeding:

- Missing entity card for `<entity>` — create via `project-audit` first.
- Unresolved contradiction between `<memory-A>` and `<memory-B>`.
- Missing git repository for `<entity>` / workspace root / `.serena`.

## Execution order

1. Rename non-compliant paths (`naming_violation`).
2. Fix invalid frontmatter (`invalid_frontmatter`, including `commited_at` typo).
3. Refresh legacy headers (`legacy_header`).
4. Add missing headers (`no_header`) and H1 titles (`no_h1`).
5. Sync stale metadata (`stale_commit`, `stale_branch`, `stale_date`) where content is still valid.
6. Update source-anchored content (`source_missing`, `source_lines_changed`).
7. Update entity cards (`entities/<entity>`) and business-domain reports (`logic/<entity>/...`).
8. Route new findings to `bugs/`, `notes/`, `decisions/`, `style/`, `todo/`.
```

## Priority rules

- `high` — `source_missing`, `entity_card_missing`, unresolved contradiction,
  `invalid_frontmatter` that breaks parsing, `naming_violation`.
- `medium` — `stale_commit` / `stale_branch` / `stale_date`, `legacy_header`,
  `title_mismatch`.
- `low` — `no_header`, `no_h1`, cosmetic issues, missing optional tags.

## Writing the plan

Use `write_memory`. Because the plan is a multi-line structured document, write
it in one call. Do not append. If it exceeds 25 KB, move the per-item table to
`/tmp/serena_reconciliation_plan.json` and keep only grouped counts in Serena.
