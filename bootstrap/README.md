# bootstrap
[ref: #bootstrap]

Canonical session boot and skill-loading orchestrator.

## What it does
[ref: #bootstrap-purpose]

This skill is the agent's Startup Gate.
It makes every session begin with the same ordered ritual: skill-mirror sync, forced import of the frontmatter protocol, discovery of all skill headers, evaluation of their triggers, project activation, memory priming, MCP inventory, and a think-block proof of work.
The concrete mechanics of skill headers, trigger grammar, discovery, and evaluation live in `frontmatter-protocol` (include extension), which this skill requires.

## When it activates
[ref: #bootstrap-activation]

Always active.
It runs automatically at the beginning of every session before the agent produces any user-facing output.

## How to run / use it
[ref: #bootstrap-usage]

1. Place skills in the runtime skill directories the harness expects, such as `.kimi/skills/` or `.agents/skills/`.
2. Give every `SKILL.md` a valid frontmatter with `name`, `description`, and `triggers`.
3. If `just` is installed, run `just sync-skills-mirror` from the workspace root before the session starts.
4. The agent then executes the Startup Gate automatically:
   - syncs the skill mirror,
   - loads `frontmatter-protocol/SKILL.md` and its boot-mandatory `references/include.md`,
   - batch-extracts every `SKILL.md` header,
   - evaluates triggers and resolves `requires` dependencies transitively,
   - activates the project,
   - primes `agent/rules` and relevant memories,
   - declares the MCP groups the task needs,
   - emits a think block listing the applied skills and MCP groups.

## What it produces
[ref: #bootstrap-artifacts]

- A deterministic, correctly closed skill set for the session.
- Transitive loading of every skill declared in `requires` lists.
- Header-only awareness for `runtime: true` skills that may activate later in the session.
- The Startup Gate think block used as evidence by `preflight-checklist`.

## Dependencies and why they matter
[ref: #bootstrap-dependencies]

- `frontmatter-protocol` — provides the YAML envelope rules, the closed skill-header schema, the trigger grammar, discovery/evaluation algorithms, and the boot contract.
- `just` (runtime tool) — executes `just sync-skills-mirror` to keep `.kimi/mirror/` in sync with the live skill tree.

## Strengths and trade-offs
[ref: #bootstrap-tradeoffs]

- Strong sides: deterministic startup; no guesswork about which skills are active; trigger override prevents agents from skipping relevant skills; `runtime: true` support keeps mid-session activation cheap.
- Weak sides / limits: assumes a working skill mirror and a valid skill directory layout; cannot repair malformed `SKILL.md` headers automatically.
- Common pitfalls / gotchas: the gate must complete before any user-facing output; `draft: true` skills are invisible; a failed mirror sync blocks the whole session; `runtime: true` skills are known by header only until they trigger.

## Repository layout
[ref: #bootstrap-layout]

```text
bootstrap/
├── README.md   # Human overview (this file)
└── SKILL.md    # Agent entry point: Startup Gate mandate and verification
```

## Important conventions / gotchas
[ref: #bootstrap-gotchas]

- Always loaded first; no user action triggers it manually.
- The loading mechanics are delegated to `frontmatter-protocol`; never hand-roll header extraction or trigger evaluation.
- A matching trigger forces loading even when the agent believes the skill is unnecessary.
- `requires` is resolved transitively; cycles are non-conformant and must be reported, not walked.
