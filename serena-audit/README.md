# serena-audit

Skill that keeps the Serena memory store in sync with the source repositories it describes.

## What this skill does

`serena-audit` defines a two-phase reconciliation workflow:

1. **Plan phase** — scan every memory file under `.serena/memories/`, classify discrepancies, and write a compact reconciliation plan.
2. **Execute phase** — run the plan by delegating per-memory updates to subagents.

The skill also ships a stub Python validator that checks YAML frontmatter and naming compliance.

## When to use it

Use this skill when the request involves:

- Reconciling Serena memory against source repositories.
- Auditing memory freshness, metadata, or naming compliance.
- Running a memory audit or reconciliation pass.

## Repository layout

```text
serena-audit/
├── references/           # Reconciliation workflow sections
│   ├── 01_reconcile_and_plan.md
│   ├── 02_reconciliation_subagent_prompt.md
│   ├── 03_plan_writer.md
│   ├── 04_execute_update.md
│   ├── 05_per_memory_subagent_prompt.md
│   └── 06_validation_and_edits.md
├── scripts/              # Stub memory frontmatter validator
│   └── validate_memory_frontmatter.py
└ SKILL.md                # Skill entry point and master workflow
```

## How to use this skill

1. Open `SKILL.md` for the master workflow.
2. Load `references/01_reconcile_and_plan.md` for the scan and plan steps.
3. Use `references/02_reconciliation_subagent_prompt.md` to delegate the scan.
4. Use `references/03_plan_writer.md` to assemble the reconciliation plan.
5. Use `references/04_execute_update.md` to run the plan.
6. Use `references/05_per_memory_subagent_prompt.md` for per-memory updates.
7. Use `references/06_validation_and_edits.md` for validation, git source resolution, and entity mapping.
8. Invoke the stub validator directly:
   ```bash
   python serena-audit/scripts/validate_memory_frontmatter.py --memories-dir .serena/memories
   ```
9. After every memory mutation, run `just serena-checkpoint` from the project root.

## Reference index

| File | Purpose |
|------|---------|
| `references/01_reconcile_and_plan.md` | Reconciliation planning |
| `references/02_reconciliation_subagent_prompt.md` | Scan subagent prompt |
| `references/03_plan_writer.md` | Plan writer instructions |
| `references/04_execute_update.md` | Plan execution workflow |
| `references/05_per_memory_subagent_prompt.md` | Per-memory update subagent prompt |
| `references/06_validation_and_edits.md` | Validation, git source resolution, entity mapping |

## Conventions

- `SKILL.md` is the single entry point.
- Reconciliation runs in two phases: plan and execute.
- The scan subagent classifies discrepancies without modifying files.
- Per-memory updates are delegated to subagents.
- Memory frontmatter must include `title`, `created_at`, `updated_at`, `repo`, `branch`, `commit`, `committed_at`, and `source`.
- All timestamps use UTC ISO 8601 format.
- Memory paths and entity names use `snake_case` with underscores.
