# business-audit

Extracts the business domain hidden in your repository's code.

## What it does

This skill produces a business-domain view of a project entity.
It identifies business entities, processes, rules, invariants, actors, external integrations, and risks, then writes the findings into Serena memory and updates the project glossary.
Use it when you need to understand what business a service or library actually implements.

## When it activates

Activates when you ask about business analysis, domain modeling, business rules, business logic, or what a repository does in business terms.
Examples:
- "What business does this service implement?"
- "Analyze the business domain of the billing service"
- "Extract business rules from this repo"
- "Build a domain model for user subscriptions"

## How to use it

Ask the agent to analyze the business domain of one entity.
The entity must already have a technical card created by the `project-audit` skill at `entities/<entity>`.
The agent will run read-only subagents in parallel, synthesize a report, save business-domain memories, and update `project/glossary` and `logic/<entity>/glossary`.
You do not need to prepare any files beyond the existing entity card and project memory layout.

## What it produces

- A business-domain report, either as a single file or a split model depending on complexity.
- Business-domain memories under `logic/<entity>/` for entities, processes, rules, integrations, and risks.
- Updated `project/glossary` and `logic/<entity>/glossary` with business terms, definitions, scopes, and code anchors.

## Repository layout

```text
business-audit/
├── references/           # Subagent prompts, writer instructions, and memory routing
│   ├── 01_make_business_analysis.md
│   ├── 02_business_domain_base_prompt.md
│   ├── 03_entity_catalog_subagent.md
│   ├── 04_process_map_subagent.md
│   ├── 05_rules_subagent.md
│   ├── 06_integrations_subagent.md
│   ├── 07_risks_subagent.md
│   ├── 08_business_domain_writer.md
│   └── 09_domain_memory_routing.md
└── SKILL.md              # Agent entry point: manifest, triggers, and routing index
```

## Reference overview

| File | What it covers |
|------|----------------|
| `references/01_make_business_analysis.md` | Master orchestration workflow |
| `references/02_business_domain_base_prompt.md` | Base prompt for business-domain subagents |
| `references/03_entity_catalog_subagent.md` | Extract business entities |
| `references/04_process_map_subagent.md` | Extract processes and workflows |
| `references/05_rules_subagent.md` | Extract business rules and invariants |
| `references/06_integrations_subagent.md` | Extract actors and external integrations |
| `references/07_risks_subagent.md` | Risk register and gap analysis |
| `references/08_business_domain_writer.md` | Final report writer instructions |
| `references/09_domain_memory_routing.md` | Memory namespace routing and glossary rules |

## Important conventions / gotchas

- Requires an existing entity card at `entities/<entity>` created by `project-audit`.
- Also requires `serena-protocol` for memory rules.
- The agent analyzes exactly one entity per run.
- Mermaid diagrams are required for non-trivial flows and multi-actor interactions.
- Memory paths and entity names use `snake_case` with underscores and no hyphens.
