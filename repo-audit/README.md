# repo-audit
[ref: #ra-intro]

Full repository audit pipeline that creates and maintains repo cards, business-domain reports, and dependency cards in Serena memory.

## What it does
[ref: #ra-what]

This skill produces a complete picture of a repository and stores it in Serena memory. It runs a wave-based pipeline of read-only subagents that explore the codebase, extract domain entities, processes, rules, and integrations, then generate risk, dependency interface, downstream, and infrastructure catalog reports. The root agent synthesizes the results into three canonical artifacts: a technical repo card, a business-domain report, and a dependency card with a Mermaid diagram. Three run modes let you create cards from scratch, produce a single artifact, or surgically refresh stale cards from a diff.

## When it activates
[ref: #ra-when]

Activates when you ask to create or study a repo card, explore a project or service, run business or domain analysis, build a dependency card or map, audit a repo, or refresh stale cards in English or Russian.

Examples:

- "Create a repo card for the payment service."
- "Изучи проект order-service."
- "Build a dependency map for the platform."
- "Refresh stale cards."

## How to run / use it
[ref: #ra-how]

Tell the agent which repository or service you want audited.
The skill handles one repo per run; it runs prerequisite gates, detects the repo type, and chooses the run mode automatically.
In FULL mode it launches a wave of analysis subagents followed by a wave of generator subagents.
In PARTIAL mode it produces only the requested artifact.
In REFRESH mode it detects stale inputs, asks you for confirmation, and applies a diff-driven update.
You do not need to prepare any files; the agent reads the codebase and existing memory.

## What it produces
[ref: #ra-produces]

- `repos/<repo>/overview` — technical card covering type, stack, interface, and resources.
- `repos/<repo>/business` — business-domain report (single file or split model with `entities/`, `processes/`, `rules/`, `integrations/`, `risks/` subfiles).
- `repos/<repo>/dependencies` — exhaustive dependency card with a Mermaid diagram drawn by the root agent.
- `repos/<repo>/glossary` — repo-specific business terms alongside the project glossary.
- `project/dependencies` — project-level dependency index (only on explicit request when all per-repo cards are fresh).
- `project/repos` — updated registry row mapping repo, type, language, and skills.

## Dependencies and why they matter
[ref: #ra-deps]

- `entity-protocol` — owns the repo concept, prerequisite gate, identity and freshness rules, namespace registry, and canonical `repos/` memory layout.
- `frontmatter-protocol` — provides tracking fields and lazy-load routing for reference files.
- `serena-protocol` — governs memory mutation, persistence, and read-back verification.
- `subagents-protocol` — defines the dispatch rules, timeouts, and deliverable expectations for the analysis and generator waves.

## Strengths and trade-offs
[ref: #ra-tradeoffs]

### Strong sides
[ref: #ra-strong]

- Produces a reusable, structured memory corpus rather than a one-off report.
- Wave pipeline keeps subagents focused and parallelizable.
- Diff-driven REFRESH mode avoids re-reading code that is already fresh.
- Dependency diagram is drawn by the root agent from synthesized data, not inferred blindly.

### Weak sides / limits
[ref: #ra-weak]

- Higher initial cost than a shallow README summary because of the multi-wave subagent pipeline.
- Requires an existing understanding of the repo concept from `entity-protocol`.
- Audits one repo per run; cross-repo project indexes require every per-repo card to be fresh.
- Stale inputs force a user confirmation before proceeding.

### Common pitfalls / gotchas
[ref: #ra-pitfalls]

- Do not ask the agent to analyze more than one repo in a single run.
- The root agent should not explore the codebase directly; exploration is delegated to read-only subagents.
- Generated findings must be synthesized before writing to memory; raw subagent output is never dumped.
- Technical findings go into `overview`; business findings go into `business`; keep the two separate.

## Repository layout
[ref: #ra-layout]

```text
repo-audit/
├── references/           # Subagent prompts, templates, and shared conventions
│   ├── analysis/         # Wave 1: explorer + domain subagents
│   │   ├── domain.md
│   │   ├── explorer.md
│   │   └── type_detection.md
│   ├── generators/       # Wave 2: risks + dependency subagents
│   │   ├── dependencies.md
│   │   └── domain.md
│   ├── shared/           # Gates, synthesis, conventions, subagent base prompt
│   │   ├── conventions.md
│   │   ├── gates.md
│   │   ├── refresh.md
│   │   ├── subagent_base.md
│   │   └── synthesis.md
│   ├── templates/        # Artifact templates
│   │   ├── business_writer.md
│   │   ├── dependencies_card.md
│   │   ├── dependencies_project.md
│   │   ├── glossary_routing.md
│   │   └── overview_card.md
│   └── checklists.md     # Quality checklists for all modes
├── SKILL.md              # Agent entry point: modes, wave pipeline, routing index
└── README.md
```

## Reference overview
[ref: #ra-refs]

| File | What it covers |
|------|----------------|
| `references/analysis/domain.md` | Domain subagents: entities, processes, rules, integrations |
| `references/analysis/explorer.md` | Technical explorer subagent |
| `references/analysis/type_detection.md` | Repository type detection and routing |
| `references/generators/dependencies.md` | Dependency interface, downstream, and infra catalog subagents |
| `references/generators/domain.md` | Domain risks subagent |
| `references/shared/conventions.md` | Mermaid, exclusions, evidence, and date conventions |
| `references/shared/gates.md` | Input, prerequisite, mode, freshness, naming, and memory-path gates |
| `references/shared/refresh.md` | Staleness detector and diff-driven refresh flow |
| `references/shared/subagent_base.md` | Common base prompt for all subagents |
| `references/shared/synthesis.md` | Synthesis rules for root agent artifact generation |
| `references/templates/business_writer.md` | Business report writer template |
| `references/templates/dependencies_card.md` | Per-repo dependency card template |
| `references/templates/dependencies_project.md` | Project-level dependency index template |
| `references/templates/glossary_routing.md` | Glossaries and memory routing templates |
| `references/templates/overview_card.md` | Repo card template with type-specific sections |
| `references/checklists.md` | Quality checklists for all run modes |

## Important conventions / gotchas
[ref: #ra-conventions]

- One repo per run; the project-level dependency index is the only exception and requires fresh per-repo cards.
- Use the wave pipeline; do not launch a single "analyze everything" subagent.
- Do not re-read code covered by a fresh input (`commit == HEAD`); work diff-driven when stale.
- Do not include Sentry, Prometheus, tests, linters, CI, Makefile, Docker, or entry points unless they are actual runtime dependencies.
- Do not write environment variable values, defaults, examples, or secrets into memory.
- Always run frontmatter refresh, read-back verification, and `just serena-checkpoint` after any memory mutation.
