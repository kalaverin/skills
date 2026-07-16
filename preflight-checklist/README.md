# preflight-checklist

Verifies that core mandatory skills are active before the agent starts working.

## What it does

This skill augments the Startup Gate in the repository `AGENTS.md`.
It documents the check that the agent must perform before producing any user-facing output: confirming that `shell-protocol`, `serena-protocol`, and `read-for-comments` have been discovered and loaded.
You do not interact with it directly.

## When it activates

No action needed — loaded automatically in every session.

## How to use it

Nothing.
This skill is a compliance gate for the agent.

## What it produces

No files or reports for you.
It ensures the agent has the core protocol skills loaded before handling your request.

## Repository layout

```text
preflight-checklist/
└── SKILL.md              # Single-file skill with manifest and compliance checklist
```

## Reference overview

| File | What it covers |
|------|----------------|
| `SKILL.md` | Mandatory pre-flight checklist for the agent |

## Important conventions / gotchas

- Loaded unconditionally in every session.
- Does not replace the Startup Gate in `AGENTS.md`; it augments it.
- The skills it checks are `shell-protocol`, `serena-protocol`, and `read-for-comments`.
