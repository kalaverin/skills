# serena-protocol
[ref: #serena-protocol]

Defines the canonical rules for Serena memory, knowledge base, and symbolic code exploration.

## What it does
[ref: #serena-protocol-purpose]

This skill is the rulebook for the Serena MCP ecosystem.
It governs the memory mutation and persistence protocol, naming conventions, mandatory YAML frontmatter metadata, memory lifecycle, contradiction resolution, worked examples per findings domain, and the Serena MCP tools reference.
Memory namespaces and routing, the repo concept, findings semantics, and card production live in `entity-protocol`; tracking fields and timestamps live in the `frontmatter-protocol` tracking extension.

## When it activates
[ref: #serena-protocol-activation]

Always active.
It applies whenever the agent reads or writes a memory, creates or updates an entity card, or explores code through Serena MCP tools.

## How to run / use it
[ref: #serena-protocol-usage]

1. Ask the agent to record a finding, create a repo card, list known issues, or explore code symbolically.
2. The agent routes the request through the memory mutation protocol:
   - For new memories, call `list_memories` first to avoid collisions, then `write_memory` with the complete frontmatter and body.
   - For appends, use `edit_memory` in regex mode with needle `\\Z`.
   - For updates, use `edit_memory` with a specific regex or literal replacement.
3. The agent refreshes tracking fields (`updated_at`, and `branch`/`commit`/`committed_at` when git state changed).
4. The agent reads the memory back to verify it, then runs the configured persistence command (commonly `just serena-checkpoint`) from the workspace root.

Example prompts:

- "Create an entity card for the payment service."
- "Record this bug in Serena memory."
- "Update the decision note for order-service."
- "List known issues for the user-api entity."

## What it produces
[ref: #serena-protocol-artifacts]

- Correctly routed and formatted memory entries under `.serena/memories/`.
- Valid repo cards with proper YAML frontmatter.
- Consistent metadata including `repo`, `branch`, `commit`, and `committed_at`.
- Symbolic code exploration and edits via Serena MCP tools.

## Dependencies and why they matter
[ref: #serena-protocol-dependencies]

- `entity-protocol` — provides the repo concept, the single namespace registry, findings routing, and card production rules.
- `frontmatter-protocol` — provides the YAML envelope rules and the tracking extension for git-bound memory headers.
- `markdown-protocol` — provides the Markdown authoring rules and headings-as-API standard every memory file must follow.
- `just` (runtime tool) — commonly runs the persistence command `just serena-checkpoint` after memory mutations.

## Strengths and trade-offs
[ref: #serena-protocol-tradeoffs]

- Strong sides: separates routing (`entity-protocol`) from mechanics (`serena-protocol`) for clear ownership; every mutation is verified and persisted; symbolic tools reduce blind text edits.
- Weak sides / limits: the workspace must contain a `.serena/` directory; all memory operations must run from the workspace root; forgetting the persistence command leaves changes uncommitted.
- Common pitfalls / gotchas: `write_memory` completely overwrites a file — never use it to append; memory names must use `snake_case` with no hyphens; all timestamps use UTC ISO 8601 with a `Z` suffix; working from inside a nested repo directory can accidentally target the wrong `.serena/`.

## Repository layout
[ref: #serena-protocol-layout]

```text
serena-protocol/
├── README.md              # Human overview (this file)
├── SKILL.md               # Agent entry point: manifest, triggers, and routing index
└── references/
    └── rules.md           # Canonical rule set: naming, metadata, lifecycle, contradictions, examples, MCP tools
```

## Reference overview
[ref: #serena-protocol-references]

| File | What it covers |
|------|----------------|
| `references/rules.md` | Overview of Serena memory, naming convention, metadata header rules, memory lifecycle, contradiction resolution, worked examples per findings domain, and the MCP tools reference. The mutation and persistence protocol lives in `SKILL.md` §1. |

## Important conventions / gotchas
[ref: #serena-protocol-gotchas]

- Every memory file must begin with strict YAML frontmatter followed immediately by an H1 title.
- Memory names use `snake_case` with underscores and no hyphens.
- After any memory mutation, the agent reads the memory back and runs the configured persistence command.
- All Serena memory operations that touch `.serena/` must execute from the workspace root.
- The reconciliation workflow for stale memories lives in `serena-audit`.
