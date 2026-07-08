[ref: #dcc-overview]

# Dependency card creator: overview, inputs, and constraints

## Goal

Produce an exhaustive, evidence-based dependency card for a single project
entity. The card answers:

- What public surfaces does this entity expose? (methods, endpoints, workflows,
  activities, signals, queries, updates, library modules, GitOps artifacts.)
- What does this entity call or depend on? (services, databases, queues,
  external systems, libraries, infrastructure.)
- What are the exact names of those calls/workflows/methods?
- Who consumes this entity's surfaces?
- What databases, external integrations, libraries, and infrastructure does it
  use?
- What architectural observations, gaps, or TODOs are relevant?

Per-service cards are the default output. The project-level index is generated
only on explicit request and only after every entity has a fresh per-service
card.

## Inputs

| Input | Source | Required |
|---|---|---|
| `entity_name` | User | Yes |
| `entity_path` | User / entity card | Yes |
| Entity card | `entities/<entity>` | Yes |
| Business-domain report | `logic/<entity>/business_domain_report` | Yes |
| Integration memory | `logic/<entity>/integrations` | No |
| Process memory | `logic/<entity>/processes` | No |
| Existing findings | `bugs/<entity>/...`, `notes/<entity>/...`, `decisions/<entity>/...` | No |
| Existing dependency card | `logic/<entity>/dependencies` | No |

## Hard prerequisites

Before launching any subagent:

1. Accept **exactly one entity** per run. If the user mentions multiple
   entities, STOP and ask them to pick one.
2. `entities/<entity>` MUST exist. If not, STOP and ask the user to create it
   via `project-audit`.
3. `logic/<entity>/business_domain_report` SHOULD exist. If it is missing, the
   dependency card may be technically correct but lack business context.
4. Run the **freshness gate**: compare the `commit` field in the frontmatter of
   every input memory with the latest commit of the entity's own git repository.
   - `cd <entity_path>`
   - `git rev-parse --short HEAD`
   - `git rev-parse --abbrev-ref HEAD`
   - `git log -1 --format=%cd --date=iso-strict`
   If any input memory's `commit` does not match the repo HEAD, or if input
   memories for the same entity disagree on the commit, STOP. Report the exact
   mismatch and ask the user to reconcile via `serena-audit` or by
   refreshing the upstream skill (`project-audit` or
   `business-audit`).
5. Collect absolute paths to existing memories:
   - `entities/<entity>`
   - `logic/<entity>/business_domain_report`
   - `logic/<entity>/integrations`
   - `logic/<entity>/processes`
   - `logic/<entity>/rules`
   - `logic/<entity>/entities`
   - `bugs/<entity>/...`, `notes/<entity>/...`, `decisions/<entity>/...`,
     `style/<entity>/...`, `todo/<entity>/...`
6. Verify every memory path complies with Serena naming rules
   (`[ref: #serena-naming]`). Rename non-compliant paths before analysis.

## Constraints

- One entity per run. No batching.
- The analysis is read-only. No code changes.
- Evidence must be traceable to file, line, and commit hash.
- All output must be written in English (technical content) and stored in Serena
  memory with proper YAML frontmatter.
- User-facing chat remains in the user's language.
- Every memory mutation refreshes the YAML frontmatter and ends with
  `just serena-checkpoint`.
- Do not generate a project-level card unless explicitly asked and unless every
  entity in `entities/` has a fresh `logic/<entity>/dependencies` card.

## Reuse from sibling skills

### `serena-protocol`

Use as the single source of truth for:

- YAML frontmatter and metadata contract (`[ref: #serena-metadata]`,
  `[ref: #serena-metadata-contract]`).
- Naming convention (`[ref: #serena-naming]`).
- Entity prerequisite (`[ref: #serena-entity-prerequisite]`).
- Memory mutation and persistence (`[ref: #serena-memory-mutation]`).
- Routing findings (`[ref: #serena-findings-traceability]`).
- Contradiction resolution (`[ref: #serena-contradictions]`).

Do not duplicate these rules in this skill.

### `project-audit`

Reuse without duplicating:

- Entity existence check.
- Deterministic type detection algorithm
  (`[ref: #serena-algo-type-detection]`).
- Read-only exploration subagent pattern (no MCP, evidence with file:line and
  commit hash).
- The entity card itself as the primary source for exported interface.

Do not rewrite the entity card here.

### `business-audit`

Reuse as context, not as analysis:

- `logic/<entity>/business_domain_report` for meaningful descriptions.
- `logic/<entity>/integrations` for actors and external systems.
- `logic/<entity>/processes` for workflow-to-process mapping.
- Glossaries for consistent naming.

Do not re-run business-domain analysis. If these inputs are missing or stale,
STOP and ask the user to refresh them via `business-audit`.

## Subagent strategy

Do not launch a single "analyze everything" subagent. Launch **four** parallel
read-only `explore` subagents, each specialized on one dependency task:

1. **Interface extractor** — every exposed surface and its consumers.
2. **Downstream mapper** — every downstream call, exact method/workflow names,
   protocols, purposes.
3. **Infra & libs catalog** — databases, external systems, libraries,
   infrastructure.
4. **Diagram synthesizer** — Mermaid diagram covering every upstream consumer
   and downstream target.

Each subagent receives the same memory path list and `entity_path`, plus the
common base rules (`[ref: #dcc-subagents-base]`). Timeout per subagent: at least
**1800 seconds** (30 minutes).

The root agent synthesizes the four reports into the final dependency card.

## Output routing

- Final per-service card: `logic/<entity>/dependencies`.
- Optional project-level index: `project/dependencies`.
- Findings that are not dependency-specific (bugs, style issues, TODOs) route
  to the canonical namespaces per `[ref: #serena-findings-traceability]`.

## Pre-generation checklist

Confirm before writing:

- [ ] Exactly one entity is selected.
- [ ] `entities/<entity>` exists.
- [ ] Input memories (`entities/<entity>`, `logic/<entity>/business_domain_report`,
      `logic/<entity>/integrations`, `logic/<entity>/processes`) are fresh and
      share a consistent entity-repo commit.
- [ ] All memory path names are Serena-compliant.
- [ ] Existing `logic/<entity>/dependencies` was read (if present).
