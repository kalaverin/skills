# entity-protocol
[ref: #entity-protocol]

The single normative source for the repo (entity) concept and for all Serena memory namespaces and scopes.

## What it does
[ref: #entity-protocol-purpose]

This skill defines what a repo is, how it is named, and where repo-scoped knowledge lives.
It owns:

- The repo concept and its prerequisite gate (a repo needs a card at `repos/<repo>/overview` before repo-scoped memory can be written).
- The single namespace registry for every Serena memory scope.
- Findings semantics and evidence rules for repo-scoped memories.
- The deprecation registry and canonical naming rules.
- The canonical `repos/` memory layout.

General memory mechanics (create, append, update, persist) live in `serena-protocol`; type detection and the audit pipeline that produces cards live in `repo-audit`.

## When it activates
[ref: #entity-protocol-activation]

Loaded at startup with header-only awareness (`runtime: true`) and activated whenever the conversation touches entities, repos, entity cards, repo cards, namespaces, the `repos/` layout, or the prerequisite gate.

Example prompts:

- "Create an entity card for the payment service."
- "What repos are in this project?"
- "Record a bug for order-service."
- "List the namespace registry."

## How to run / use it
[ref: #entity-protocol-usage]

1. To create the first repo card, use the `repo-audit` skill; do not invent repo names from directory names.
2. Before writing any repo-scoped memory (bugs, decisions, notes, style, todo, plans, proposals, reports, deprecations, or anything under `repos/<repo>/...`), verify that `repos/<repo>/overview` exists.
3. If the target repo has no card, stop the memory write and ask the user to create the card via `repo-audit` or to confirm the correct repo name.
4. Pick the right scope from the namespace registry: `agent/`, `project/`, `repos/<repo>/...`, findings scopes, etc.
5. For migration from legacy `entities/` or `logic/` scopes, follow the ordered `ruplacer` procedure in `references/memory_layout.md`.

## What it produces
[ref: #entity-protocol-artifacts]

- A stable repo concept and naming convention (`snake_case`, no hyphens).
- The single namespace registry used by every Serena memory write.
- Repo cards at `repos/<repo>/overview` and related analysis artifacts (`business`, `dependencies`, split-model subfiles, glossary).
- Repo-scoped findings with proper severity, `path:line`, and commit-hash evidence.

## Dependencies and why they matter
[ref: #entity-protocol-dependencies]

- `frontmatter-protocol` — provides the YAML envelope and tracking-field semantics for repo cards and tracked memories.
- `repo-audit` (runtime skill) — produces repo cards and business/dependency artifacts; this skill defines the layout those artifacts must follow.
- `git` (runtime tool) — supplies branch, short commit hash, and commit timestamp for freshness checks.
- `ruplacer` (runtime tool) — refreshes cross-memory links during migration from legacy scopes.

## Strengths and trade-offs
[ref: #entity-protocol-tradeoffs]

- Strong sides: one authoritative namespace registry prevents ad-hoc scope sprawl; the prerequisite gate stops repo-scoped writes before a repo is defined; separation of concerns keeps this skill focused on routing.
- Weak sides / limits: it does not create cards itself — `repo-audit` is required; it does not detect repo types or extract interfaces — that belongs to `repo-audit`.
- Common pitfalls / gotchas: never guess a repo name from a directory name; the meta-entity `project` is exempt from the prerequisite gate; `project/repos` is only a name registry, not a usability token; legacy values like `entities/` and `logic/` must be migrated in the exact order documented.

## Repository layout
[ref: #entity-protocol-layout]

```text
entity-protocol/
├── README.md                       # Human overview (this file)
├── SKILL.md                        # Core standard: repo concept, namespace registry, prerequisite gate, naming, freshness
└── references/
    ├── card_production.md          # Repo card workflow, quality gate, exclusions, hard fails, header template
    ├── memory_layout.md            # Canonical `repos/` layout and legacy migration procedure
    └── repo_memory.md              # `repo` field semantics, findings evidence format, deprecation registry
```

## Reference overview
[ref: #entity-protocol-references]

| File | What it covers |
|------|----------------|
| `references/card_production.md` | Root/subagent workflow for producing `repos/<repo>/overview`, the five-criterion quality gate, content exclusions, hard fails, and the card frontmatter template. |
| `references/memory_layout.md` | Canonical `repos/` directory layout and the ordered migration from legacy `entities/` + `logic/` scopes. |
| `references/repo_memory.md` | `repo` frontmatter field semantics, findings traceability format, and the two-level deprecation registry. |

## Important conventions / gotchas
[ref: #entity-protocol-gotchas]

- A repo is usable for repo-scoped memory only after its `repos/<repo>/overview` card exists.
- Exactly one repo is analyzed per run; do not batch repos.
- Repo identity metadata comes from the repo's own git, never from the `.serena` host project.
- Repo names are `snake_case` with underscores; directory dashes become underscores.
- The scope name `cards/` is reserved for future use.
