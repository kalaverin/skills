# business-audit

Agent skill for extracting business and domain knowledge from a repository's source code.

## What this skill does

`business-audit` defines the workflow, prompts, and memory routing that an agent follows to produce a business-domain view of a project. It does not run as a service and contains no executable code. Instead, it gives the root agent:

- A master workflow for commissioning business-domain analysis.
- A base prompt for business-domain subagents.
- Specialized subagent prompts for:
  - Entity catalog extraction.
  - Process map extraction.
  - Business rules extraction.
  - Integration points extraction.
  - Risk analysis.
- Writer instructions for assembling the final report.
- Memory routing rules that send findings to the correct Serena namespace.

## When to use it

Use this skill when the request involves:

- Business entity analysis or domain model extraction.
- Identifying business rules, invariants, actors, or domain events.
- Understanding what business a repository implements.
- Expanding an existing `project-audit` entity card with a business-domain view.

> **Prerequisite:** A technical entity card created by `project-audit` must already exist at `entities/<entity>`. This skill builds on top of that card.

## Repository layout

```text
business-audit/
├── references/           # Subagent prompts, writer instructions, memory routing
│   ├── 01_make_business_analysis.md
│   ├── 02_business_domain_base_prompt.md
│   ├── 03_entity_catalog_subagent.md
│   ├── 04_process_map_subagent.md
│   ├── 05_rules_subagent.md
│   ├── 06_integrations_subagent.md
│   ├── 07_risks_subagent.md
│   ├── 08_business_domain_writer.md
│   └── 09_domain_memory_routing.md
└── SKILL.md              # Skill entry point with lazy-load routing index
```

## How to use this skill

1. Confirm that `entities/<entity>` exists (created by `project-audit`).
2. Open `SKILL.md` and locate the routing index.
3. Load `references/01_make_business_analysis.md` for the master workflow.
4. Dispatch read-only subagents using the prompts in `references/02_*.md` through `references/07_*.md`.
5. Route findings according to `references/09_domain_memory_routing.md`:
   - Domain findings → `logic/<entity>/<topic>.md`
   - Non-domain findings → `notes/<entity>/<topic>.md`, `decisions/<entity>/<topic>.md`, or `bugs/<entity>/<topic>.md`
6. Assemble the final report with `references/08_business_domain_writer.md`.

## Reference index

| File | Purpose |
|------|---------|
| `references/01_make_business_analysis.md` | Master orchestration workflow |
| `references/02_business_domain_base_prompt.md` | Base prompt for business-domain subagents |
| `references/03_entity_catalog_subagent.md` | Extract business entities |
| `references/04_process_map_subagent.md` | Extract processes and flows (Mermaid diagrams required) |
| `references/05_rules_subagent.md` | Extract business rules and invariants |
| `references/06_integrations_subagent.md` | Extract integration points |
| `references/07_risks_subagent.md` | Risk analysis |
| `references/08_business_domain_writer.md` | Final report writer instructions |
| `references/09_domain_memory_routing.md` | Memory namespace routing and metadata rules |

## Conventions

- `SKILL.md` is the single entry point; reference sections use `[ref: #bda-<name>]` anchors.
- Business-domain findings are owned by the `logic/<entity>/...` namespace.
- Memory paths use `snake_case` with underscores and no hyphens.
- Mermaid diagrams are required for non-trivial flows and multi-actor interactions.
- All memory files must carry the standard Serena YAML frontmatter with UTC ISO 8601 timestamps.
