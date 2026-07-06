# preflight-checklist

Mandatory pre-flight compliance skill loaded in every agent session.

## What this skill does

`preflight-checklist` is a runtime protocol skill that augments the Startup Gate defined in the repository `AGENTS.md`. It verifies that the two core mandatory skills have been discovered and loaded before any user-facing output is produced:

- `shell-protocol`
- `serena-protocol`

The skill is a single-file Markdown document with a short checklist. It does not implement runtime logic itself; it documents the verification step that every agent must perform.

## When to use it

This skill is loaded unconditionally (`triggers: always: true`). It runs as part of the startup sequence for every task.

## Repository layout

```text
preflight-checklist/
└── SKILL.md              # Single-file skill with compliance checklist
```

## How to use this skill

Before producing output for any user request, confirm:

- [ ] `shell-protocol` was discovered during Skill Discovery and its `SKILL.md` is loaded.
- [ ] `serena-protocol` was discovered during Skill Discovery and its `SKILL.md` is loaded.

If either skill is missing, halt, load it, and restart the Startup Gate.

## Conventions

- `SKILL.md` begins with a YAML frontmatter block declaring `name`, `description`, and `triggers: always: true`.
- This skill augments, but does not replace, the Startup Gate in `AGENTS.md`.
