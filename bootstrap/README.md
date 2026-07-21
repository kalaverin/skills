# bootstrap

Automatically discovers and loads the right skills for every agent session.

## What it does

This skill is the canonical skill loader.
It discovers skill directories, reads the YAML frontmatter in each `SKILL.md`, evaluates triggers, resolves transitive dependencies, and decides which skills the agent should use for your request.
It also supports runtime re-evaluation for skills that need to activate mid-session.

## When it activates

No action needed — loaded automatically in every session.

## How to use it

You do not need to do anything.
Place your skills in the directories the execution harness expects, such as `.kimi/skills/` or `.agents/skills/`.
The agent uses this skill at startup to figure out which other skills are relevant.

## What it produces

- A correctly loaded skill set for the current session.
- Triggered skills, plus any skills they declare as dependencies.

## Repository layout

```text
bootstrap/
├── prompts/
│   └── REFERENCE_MIGRATION_PROMPT.md  # Six-phase orchestration prompt for standardizing a skill's reference corpus
├── references/
│   └── REFERENCE_STANDARD.md          # Normative cross-skill standard for reference files, frontmatter cards, and anchors
└── SKILL.md                           # Agent entry point: manifest and full loading protocol
```

## Reference overview

| Reference | Purpose |
|---|---|
| `references/REFERENCE_STANDARD.md` | Normative standard for every skill's reference files that use `[ref: #anchor]` lazy-load routing: frontmatter card schema, anchor mechanics, loader funnel, conformance checklist. Load when authoring, migrating, or validating reference corpora. |

## Important conventions / gotchas

- This skill is always loaded before any other work happens.
- It can only load skills that are present in the discovered skill directories.
- A matching trigger overrides any internal assumption the agent might have.
- Runtime re-evaluation applies only to skills that opt in with `runtime: true`.
