# Phase 1: reconcile and plan

[ref: #smr-reconcile]

## Goal

Audit every Serena memory file, compare its recorded metadata and content
against the current state of its source repository, and produce a compact
reconciliation plan.

## Input

- Workspace root path (`$PWD`).
- `.serena/memories/` directory.
- `project/entities` registry (if it exists).

## Steps

### Step 0 — Enumerate memory files

Run a recursive listing of all markdown memories. Do not read contents yet.

```bash
tree --gitignore --prune <workspace-root>/.serena/memories
```

### Step 0.5 — Rename non-compliant paths

Before reading any content, inspect every path segment. If a directory or file
name contains hyphens, spaces, or any character outside `[a-zA-Z0-9_]`, rename
it immediately using the Serena MCP `rename_memory` tool (or the normalization
recipe from `[ref: #serena-naming]`). Do not wait for a separate batch.

### Step 1 — Run the validation script

Execute the stub script to get a baseline JSON report:

```bash
python serena-audit/scripts/validate_memory_frontmatter.py --memories-dir .serena/memories
```

Review the output. The script currently is a placeholder; treat its results as
advisory until it is implemented.

### Step 2 — Generate the machine-readable audit dump

Write a full JSON audit to a location outside Serena memory, e.g.:

```bash
/tmp/serena_audit_full.json
/tmp/serena_reconciliation_plan.json
```

This dump contains every per-file classification and is the source of truth for
phase 2. Keep the Serena plan memory small.

### Step 3 — Launch the read-only scan subagent

Create an `explore` subagent with the prompt from
`references/02_reconciliation_subagent_prompt.md` (`[ref: #smr-scan-prompt]`).
Provide:

- `workspace_root` — absolute path.
- `memories_dir` — absolute path to `.serena/memories`.
- `validation_report_path` — path to the script output (if generated).
- `entity_registry_path` — path to `.serena/memories/project/entities.md` (if it exists).

Timeout: at least **1800 seconds** (30 minutes).

### Step 4 — Determine the correct git source for every memory

For each memory path, apply the rules from `SKILL.md` `[ref: #smr-git-source]`:

- Entity-scoped → entity git dir → workspace root → `.serena`.
- Project-wide → workspace root → `.serena` (`repo: project`).
- Cross-entity/agent → `.serena` (`repo: serena`).
- Project-specific → workspace root → `.serena`.

Use `[ref: #smr-entity-mapping]` to map memory-path names to git directories
and canonical entity cards.

Record the chosen `repo`, `branch`, `commit`, and `committed_at`.

### Step 5 — Classify issues

For each memory, produce one or more of these classifications:

| Class | Meaning |
|---|---|
| `ok` | Header matches current git metadata and source exists. |
| `stale_commit` | Recorded commit differs from `HEAD`. |
| `stale_branch` | Recorded branch differs from current branch. |
| `stale_date` | Recorded `committed_at` does not match `HEAD` commit timestamp. |
| `legacy_header` | File has plain-text metadata instead of YAML frontmatter. |
| `invalid_frontmatter` | YAML frontmatter is missing or malformed. |
| `title_mismatch` | `title` field does not match the first H1. |
| `source_missing` | The `source` path does not exist. |
| `source_lines_changed` | The `source` line range is out of bounds. |
| `entity_card_missing` | Entity-scoped memory exists but `entities/<entity>` does not. |
| `contradiction` | Same fact is recorded differently in another memory. |
| `naming_violation` | Path contains hyphens or other invalid characters. |
| `no_h1` | File has no Markdown H1 heading. |

### Step 6 — Write the reconciliation plan

Use the format from `references/03_plan_writer.md` (`[ref: #smr-plan]`).

Target memory name:

- If the plan covers a single entity → `plans/<entity>/serena_reconciliation_plan`.
- If the plan covers multiple entities or the whole workspace → `plans/project/serena_reconciliation_plan`.

The git source for the plan is:

- workspace root if it is a git repo (`repo: project`);
- else `.serena` (`repo: serena`).

Keep the plan compact. Reference the full JSON dump in the notes.

### Step 7 — Verify and persist

Read the plan back to confirm it was written correctly, then run:

```bash
just serena-checkpoint
```

## Output

A compact `plans/.../serena_reconciliation_plan` memory plus a full
machine-readable audit in `/tmp/serena_audit_full.json`.
