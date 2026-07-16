# serena-protocol

Defines the canonical rules for Serena memory, knowledge base, and symbolic code exploration.

## What it does

This skill is the rulebook for the Serena MCP ecosystem.
It governs memory namespaces and routing, naming conventions, mandatory YAML frontmatter metadata, the metadata contract, git source resolution, memory lifecycle, mutation protocol, entity-card workflow, deterministic type detection, root versus subagent responsibilities, contradiction resolution, findings traceability, and the Serena MCP tools reference.

## When it activates

No action needed — loaded automatically in every session.

## How to use it

You do not need to invoke this skill directly.
Whenever the agent reads or writes a memory, creates an entity card, or explores code through Serena MCP tools, it follows the rules in this skill.

Example prompts that rely on it:

- "Create an entity card for the payment service."
- "Record this bug in Serena memory."
- "Update the decision note for order-service."
- "List known issues for the user-api entity."

## What it produces

- Correctly routed and formatted memory entries.
- Valid entity cards with proper YAML frontmatter.
- Consistent metadata including `repo`, `branch`, `commit`, and `committed_at`.

## Repository layout

```text
serena-protocol/
├── references/           # Canonical rule set
│   └── rules.md
└── SKILL.md              # Agent entry point: manifest, triggers, and routing index
```

## Reference overview

| File | What it covers |
|------|----------------|
| `references/rules.md` | Overview of Serena memory, naming convention, namespaces and routing, entity analysis prerequisite, metadata header rules, metadata contract, lifecycle, mutation protocol, entity card workflow, type detection algorithm, agent segregation, quality checklist, interface exhaustiveness matrix, contradiction resolution, core tools, deprecations, findings traceability, forbidden actions, examples, memory freshness, common mistakes, and MCP tools reference. |

## Important conventions / gotchas

- Requires the `markdown-protocol` skill automatically.
- Every memory file must begin with strict YAML frontmatter followed immediately by an H1 title.
- Memory names use `snake_case` with underscores and no hyphens.
- Entity-scoped memories require an existing entity card at `.serena/memories/entities/<entity>`.
- The reconciliation workflow lives in `serena-audit`; entity card production lives in `project-audit`.
- After any memory mutation, the agent reads the memory back and runs the configured persistence command.
- All timestamps use UTC ISO 8601 format.
