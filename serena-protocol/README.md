# serena-protocol

Canonical rules for the Serena memory and MCP ecosystem.

## What this skill does

`serena-protocol` defines how agents organize, name, route, mutate, and persist memory entries under `.serena/memories/`. It is a documentation-only skill consumed by other skills and agents. It specifies:

- Memory namespaces and routing rules.
- Naming conventions (`snake_case` with underscores).
- Mandatory YAML frontmatter metadata headers.
- The metadata contract and git source resolution rules.
- Memory lifecycle and workflow.
- Memory mutation protocol (create, edit, verify, persist).
- Entity-card creation workflow.
- Deterministic type-detection algorithm.
- Root vs subagent responsibilities.
- Quality checklist for entity cards.
- Interface exhaustiveness matrix.
- Contradiction resolution.
- Findings and traceability rules.
- Forbidden actions and hard fails.
- Serena MCP tools reference.

## When to use it

This skill is loaded automatically (`triggers: always: true`) because memory and knowledge-base tools are used in every session. Explicitly consult it when:

- Reading or writing Serena memories.
- Creating or updating entity cards.
- Resolving contradictions in stored knowledge.
- Following memory metadata, naming, or routing conventions.

## Repository layout

```text
serena-protocol/
├── references/           # Canonical rule set
│   └── rules.md
└ SKILL.md                # Skill entry point, lazy-load routing index, and workflow
```

## How to use this skill

1. Open `SKILL.md` for the lazy-load routing index.
2. Match your task to a trigger in the index.
3. Extract only the relevant `[ref: #...]` section from `references/rules.md` using `rg`.
4. Apply the extracted rules strictly.
5. After any memory mutation, read the memory back to verify it and run the configured persistence command (commonly `just agent-memory-commit`).

## Reference index

| Anchor | Topic |
|--------|-------|
| `[ref: #serena-what-is]` | Overview of Serena memory and available scopes |
| `[ref: #serena-naming]` | Memory naming convention |
| `[ref: #serena-namespaces-routing]` | Memory namespaces and strict routing |
| `[ref: #serena-entity-prerequisite]` | Entity analysis prerequisite |
| `[ref: #serena-metadata]` | Metadata header rules |
| `[ref: #serena-metadata-contract]` | The strict metadata contract |
| `[ref: #serena-lifecycle]` | Memory lifecycle / workflow |
| `[ref: #serena-memory-mutation]` | Memory mutation protocol |
| `[ref: #serena-card-workflow]` | Entity card creation workflow |
| `[ref: #serena-algo-type-detection]` | Deterministic type detection algorithm |
| `[ref: #serena-agent-segregation]` | Root vs subagent responsibilities |
| `[ref: #serena-quality]` | Quality checklist for entity cards |
| `[ref: #serena-interface-exhaustiveness]` | Interface exhaustiveness matrix |
| `[ref: #serena-contradictions]` | Contradiction resolution overview |
| `[ref: #serena-contradiction-resolution]` | Strict contradiction resolution protocol |
| `[ref: #serena-core-tools]` | Core tools, git commands, and persistence command |
| `[ref: #serena-deprecations]` | Deprecated services and aliases |
| `[ref: #serena-findings-traceability]` | Findings and traceability rules |
| `[ref: #serena-forbidden-actions]` | Hard fails and forbidden actions |
| `[ref: #serena-examples]` | Examples of memory entries |
| `[ref: #serena-memory-freshness]` | Reading entity-specific memories |
| `[ref: #serena-mistakes]` | Common mistakes and gotchas |
| `[ref: #serena-mcp-tools]` | Serena MCP tools reference |

## Conventions

- `SKILL.md` is the single entry point.
- Agents must **not** read `references/rules.md` in full; they must use lazy extraction.
- Every memory file must begin with strict YAML frontmatter and an H1 title.
- Memory names use `snake_case` with underscores and no hyphens.
- Entity-scoped memories require an existing entity card at `entities/<entity>`.
- All timestamps use UTC ISO 8601 format.
- After any memory mutation, run the configured persistence command.
