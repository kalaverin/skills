# dependencies-audit

Maps what each project entity exposes and depends on.

## What it does

This skill creates and maintains dependency cards for project entities.
A dependency card documents every surface an entity exposes, every downstream call it makes, every database, external system, library, and infrastructure component it touches, plus a visual dependency diagram.
It can also build a project-level dependency index when all per-service cards are up to date.

## When it activates

Activates when you ask for a dependency card, dependency map, service dependencies, or architecture dependencies.
Examples:
- "Create a dependency card for the payment service"
- "What does the auth service depend on?"
- "Build a dependency map for this project"
- "List all downstream calls from the order service"

## How to use it

Ask the agent to create a dependency card for one entity.
The entity must already have a technical card at `entities/<entity>` and up-to-date business-domain memories under `logic/<entity>/` from `business-audit`.
The agent will check memory freshness, run specialized read-only subagents, synthesize the card, and save it to `logic/<entity>/dependencies.md`.
For a project-level index, ask explicitly after every entity has a fresh per-service card.

## What it produces

- A per-service dependency card at `logic/<entity>/dependencies.md` with a Mermaid diagram.
- A project-level dependency index at `project/dependencies.md`, only on explicit request and when every per-service card is fresh.

## Repository layout

```text
dependencies-audit/
├── references/           # Templates, subagent prompts, and quality checks
│   ├── 01_overview_and_boundary.md
│   ├── 02_per_service_template.md
│   ├── 03_project_template.md
│   ├── 04_subagent_prompts.md
│   └── 05_quality_checks.md
└── SKILL.md              # Agent entry point: manifest, triggers, and routing index
```

## Reference overview

| File | What it covers |
|------|----------------|
| `references/01_overview_and_boundary.md` | Inputs, constraints, freshness gate, and memory path list |
| `references/02_per_service_template.md` | Per-service dependency card template with Mermaid diagram rules |
| `references/03_project_template.md` | Project-level dependency index template |
| `references/04_subagent_prompts.md` | Specialized subagent prompts for interface, downstream, infra, and diagram tasks |
| `references/05_quality_checks.md` | Pre-generation, per-service, project-level, and persistence checks |

## Important conventions / gotchas

- Requires an existing entity card from `project-audit` and up-to-date business-domain memories from `business-audit`.
- Also requires `serena-protocol` for memory rules.
- The agent handles exactly one entity per per-service run.
- Stale input memories stop the workflow until you reconcile them.
- Per-service cards use Mermaid diagrams and standard Serena YAML frontmatter.
