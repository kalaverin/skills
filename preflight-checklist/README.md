# preflight-checklist
[ref: #preflight-checklist]

Verifies that the Startup Gate completed successfully before the agent begins working.

## What it does
[ref: #preflight-checklist-purpose]

This skill is the closing ceremony of session initialization.
It audits the Startup Gate once per session, immediately after `bootstrap` finishes and before the first task output.
It checks for evidence that every Startup Gate step ran: mirror sync, forced import of the frontmatter protocol, skill discovery and evaluation, project activation, memory priming, MCP group declaration, and the think block.
It is not a per-action check; mid-session compliance is enforced by the individual skills at the moment of action.

## When it activates
[ref: #preflight-checklist-activation]

Always active.
It runs automatically once at session start, immediately after the Startup Gate.

## How to run / use it
[ref: #preflight-checklist-usage]

1. Start a session.
2. The agent executes the Startup Gate (`bootstrap`).
3. This skill runs automatically and prints a compact verdict table.
4. If any item fails, the agent fixes the cause, re-runs the affected check, and prints the corrected line.
5. Only when every item passes does the agent answer the first user request.

## What it produces
[ref: #preflight-checklist-artifacts]

- A single evidence-backed verdict table printed before the first task output.
- No persistent files or memory entries.
- Confidence that the agent has the correct skill set and MCP groups loaded.

## Dependencies and why they matter
[ref: #preflight-checklist-dependencies]

- `bootstrap` — provides the Startup Gate steps this skill audits.
- `just` (runtime tool) — mirror sync evidence comes from `just sync-skills-mirror` output (`SYNCED`, `INSYNC`, or `CREATED`).

## Strengths and trade-offs
[ref: #preflight-checklist-tradeoffs]

- Strong sides: catches initialization failures before any user work begins; requires evidence, not mental checkmarks; compact one-line-per-item format is easy to scan.
- Weak sides / limits: runs only once per session; it does not re-audit mid-session when new skills activate or when the workspace changes.
- Common pitfalls / gotchas: if `just sync-skills-mirror` reports `INSYNC` while uncommitted skill edits exist, apply the lag workaround and re-run; a missing think block or undeclared MCP group is a FAIL.

## Repository layout
[ref: #preflight-checklist-layout]

```text
preflight-checklist/
├── README.md   # Human overview (this file)
└── SKILL.md    # Agent entry point: checklist, verdict format, and timing rules
```

## Important conventions / gotchas
[ref: #preflight-checklist-gotchas]

- Runs exactly once per session, immediately after the Startup Gate.
- Every checklist item needs evidence: command output, tool result, or a file read in the current session.
- Any FAIL must be fixed and re-verified before user output.
- It augments, but does not replace, the Startup Gate defined in `AGENTS.md`.
