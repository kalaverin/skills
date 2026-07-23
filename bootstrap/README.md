# bootstrap

Orchestrates loading the right skills for every agent session.

## What it does

This skill is the canonical skill loading orchestrator.
It owns the operational mandate that every session discovers and loads the correct skill set.
The mechanics — skill header schema, trigger grammar, evaluation semantics, discovery algorithm — live in `frontmatter-protocol` (include extension), which bootstrap requires.

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
├── README.md   # This file
└── SKILL.md    # Agent entry point: loading mandate and verification
```

## Important conventions / gotchas

- This skill is always loaded before any other work happens.
- Header evaluation mechanics come from `frontmatter-protocol` (boot contract: core → include extension).
- Skill headers with `draft: true` are ignored — they are purely in development.
- A matching trigger overrides any internal assumption the agent might have.
- Runtime re-evaluation applies only to skills that opt in with `runtime: true`.
