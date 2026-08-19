# Phase 2: execute the reconciliation plan

[ref: #smr-execute]

## Goal

Carry out the reconciliation plan produced in phase 1 by delegating each
per-memory update to a subagent and applying validated edits.

## Input

- `plans/<entity>/serena_reconciliation_plan` or
  `plans/project/serena_reconciliation_plan`.
- Full audit dump (`/tmp/serena_audit_full.json`) if available.
- Access to the relevant git repositories (workspace root, entity dirs,
  `.serena`).

## Steps

### Step 0 — Load the plan

Read the plan memory. If it contains blockers that require user input, STOP
and ask the user before proceeding.

### Step 1 — Rename non-compliant paths first

Before editing any content, process every `naming_violation` item:

1. Compute the normalized name using the recipe from `[ref: #serena-naming]`.
2. Use the Serena MCP `rename_memory` tool to move the file.
3. Update the plan and audit dump to reflect the new path.

Do not use raw filesystem `mv`; this is a memory operation and MUST go through
Serena MCP tools.

### Step 2 — Group action items

Group items by:

- Header-only refreshes.
- Content updates per entity.
- Business-domain reports (`repos/<repo>/...`).
- New findings to route to `bugs/`, `notes/`, `decisions/`, `style/`, `todo/`.

### Step 3 — Process header-only refreshes in batches

For each memory with `legacy_header`, `invalid_frontmatter`, `title_mismatch`,
`stale_branch`, `stale_date`, or `stale_commit` where the content itself is
still correct:

1. Determine the correct git source (`[ref: #smr-git-source]`).
2. Build a fresh YAML frontmatter block.
3. Replace the old header directly at `.serena/memories/<path>.md`, preserving
   all content below the first H1.
4. Process in batches of 20–40 files using a Python script or direct edits.
5. After each batch, run `git diff --stat`, review a sample, and persist per `serena-protocol` `[ref: #serena-memory-mutation]`.

### Step 4 — Launch per-memory update subagents

For each remaining content update:

1. Determine the correct git source and current `HEAD` metadata.
2. Create an `explore` or `coder` subagent with the prompt from
   `references/05_per_memory_subagent_prompt.md` (`[ref: #smr-update-prompt]`).
   Provide:
   - `memory_path` — absolute path.
   - `entity_path` — absolute path to the entity/repo (or workspace root).
   - `current_branch`, `current_commit`, `current_committed_at`.
   - `issue_type` — from the plan.
3. Set timeout to at least **1800 seconds** (30 minutes).

### Step 5 — Validate subagent reports

Apply the checklist from `references/06_validation_and_edits.md`
(`[ref: #smr-validate]`):

- Every cited commit hash exists.
- Every cited source file exists and line ranges are in bounds.
- No contradiction with newer memories remains unresolved.
- `AGENTS.md` wins over session memory unless explicitly overridden.

### Step 6 — Apply edits

- Content rewrites, appends, and partial updates → per `serena-protocol` `[ref: #serena-memory-mutation]` (`write_memory` with refreshed YAML frontmatter, `edit_memory` `\Z` append, precise-regex update). Keep `write_memory` payloads under **25 KB**.
- For large structured outputs, write the full artifact outside Serena memory
  and keep the memory entry compact.

### Step 7 — Route new findings

For each new finding reported by a subagent, create a focused memory in the
appropriate namespace per `entity-protocol` `[ref: #entity-namespace-registry]`
(scope semantics and when-to-record table: `bugs/`, `notes/`, `decisions/`,
`style/`, `todo/`, `plans/`, `proposals/`, `reports/`, `deprecations/`).

Before writing any repo-scoped finding, verify `repos/<repo>/overview` exists.

### Step 8 — Verify and persist

Verify and persist per `serena-protocol` `[ref: #serena-memory-mutation]` (read-back + persistence command from the workspace root).

The agent always persists automatically. Manual user review before commit is
not required.

### Step 9 — Report

Write a concise summary to the user:

- Number of memories scanned.
- Number of naming violations renamed.
- Number of header refreshes applied.
- Number of content updates applied.
- Number of new findings written, grouped by namespace.
- Any unresolved blockers or contradictions.
