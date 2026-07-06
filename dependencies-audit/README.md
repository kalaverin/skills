# dependencies-audit

Agent skill for creating and maintaining exhaustive dependency cards for project entities.

## What this skill does

`dependencies-audit` orchestrates the production of dependency documentation. It consumes:

- An existing technical entity card at `entities/<entity>`.
- Up-to-date business-domain memories at `logic/<entity>/business_domain_report`, `logic/<entity>/integrations`, and `logic/<entity>/processes`.

It produces:

- A per-service dependency card at `logic/<entity>/dependencies.md`.
- Optionally, a project-level dependency index at `project/dependencies.md` when explicitly requested and every entity has a fresh card.

The skill contains templates, subagent prompts, and quality checks, but no executable code or runtime service.

## When to use it

Use this skill when the request involves:

- Creating a dependency card or dependency map for a service.
- Listing what a service depends on.
- Building a project-level architecture dependency index.

> **Prerequisite:** The target entity must have a card at `entities/<entity>` and up-to-date business-domain memories at `logic/<entity>/`.

## Repository layout

```text
dependencies-audit/
├── references/           # Templates and subagent prompts
│   ├── 01_overview_and_boundary.md
│   ├── 02_per_service_template.md
│   ├── 03_project_template.md
│   ├── 04_subagent_prompts.md
│   └── 05_quality_checks.md
└── SKILL.md              # Skill entry point and master workflow
```

## How to use this skill

1. Verify the entity card exists and the business-domain memories are fresh.
2. Open `SKILL.md` for the 11-step master workflow.
3. Use `references/01_overview_and_boundary.md` to confirm inputs, constraints, and reuse maps.
4. Generate the per-service card with `references/02_per_service_template.md`.
5. Generate the project-level index with `references/03_project_template.md` only when explicitly requested.
6. Dispatch read-only subagents using the prompts in `references/04_subagent_prompts.md`.
7. Apply the quality checks in `references/05_quality_checks.md`.

## Reference index

| File | Purpose |
|------|---------|
| `references/01_overview_and_boundary.md` | Inputs, constraints, freshness gate, memory path list |
| `references/02_per_service_template.md` | Per-service dependency card template with Mermaid diagram rules |
| `references/03_project_template.md` | Project-level dependency index template |
| `references/04_subagent_prompts.md` | Specialized subagent prompts for interface extraction and diagram synthesis |
| `references/05_quality_checks.md` | Pre-generation, per-service, project-level, and persistence checks |

## Conventions

- `SKILL.md` is the single entry point.
- Dependency cards are Markdown documents with mandatory Mermaid diagrams.
- Memory paths use `snake_case` with underscores.
- Per-service cards live at `logic/<entity>/dependencies.md`.
- Project-level index lives at `project/dependencies.md` and is generated only on explicit request.
- All produced memory files must include the standard Serena YAML frontmatter.
