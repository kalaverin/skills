# serena-audit

Reconciles Serena memory files against their source repositories to keep knowledge fresh and metadata accurate.

## What it does

This skill detects drift between Serena memory entries and the code they describe.
It runs in two phases: first it scans every memory file, classifies discrepancies, and writes a reconciliation plan; then it executes the plan by updating each memory in turn.
It also resolves git source directories, maps entity names between memory paths and git directories, and validates memory frontmatter.

## When it activates

Activates when the project contains a `.serena/memories/` directory and you ask to reconcile or audit Serena memory.

Example prompts:

- "Reconcile Serena memory with the source repos."
- "Audit memory freshness."
- "Update stale memory headers."
- "Реконсиляция памяти проекта."

## How to use it

Ask the agent to reconcile or audit memory.
The agent enumerates all memories, checks their YAML frontmatter and git metadata, classifies discrepancies, and produces a plan.
After you approve or the agent continues per policy, it updates each memory with refreshed content and metadata.
You do not need to edit memory files manually.

## What it produces

- A reconciliation plan saved as a Serena memory under `.serena/memories/plans/...`.
- Updated memory files with refreshed YAML frontmatter and corrected content.
- Output from the frontmatter validation script.

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
└── SKILL.md              # Agent entry point: manifest, triggers, and routing index
```

## Reference overview

| File | What it covers |
|------|----------------|
| `references/01_reconcile_and_plan.md` | Phase 1: scan every memory, classify discrepancies, and write a reconciliation plan. |
| `references/02_reconciliation_subagent_prompt.md` | Read-only scan subagent prompt. |
| `references/03_plan_writer.md` | Plan-memory format and routing. |
| `references/04_execute_update.md` | Phase 2: execute the update plan. |
| `references/05_per_memory_subagent_prompt.md` | Per-memory update subagent prompt. |
| `references/06_validation_and_edits.md` | Validation checklist and edit rules. |
| `scripts/validate_memory_frontmatter.py` | Stub frontmatter validator. |

## Important conventions / gotchas

- Requires the `serena-protocol` skill automatically.
- Missing entity cards must be created via `project-audit` before entity-scoped memories can be reconciled.
- Memory paths and entity names use `snake_case` with underscores and no hyphens.
- Every memory file must start with strict YAML frontmatter followed immediately by an H1 title.
- Keep each `write_memory` payload under 25 KB; store large artifacts outside Serena memory.
- All timestamps use UTC ISO 8601 format.
