# repo-audit

Full repository audit pipeline for the Serena memory ecosystem. Merges the legacy `project-audit`, `business-audit`, and `dependencies-audit` skills into a single wave-based pipeline.

## What it produces

Per repo, under the unified `repos/` memory scope:

- `repos/<repo>/overview` — technical card (type, stack, interface, resources).
- `repos/<repo>/business` — business-domain report (single file or split model with `entities/`, `processes/`, `rules/`, `integrations/`, `risks/` subfiles).
- `repos/<repo>/glossary` — repo-specific business terms (alongside `project/glossary`).
- `repos/<repo>/dependencies` — exhaustive dependency card with a Mermaid diagram.
- `project/dependencies` — project-level index (only on explicit request, all cards fresh).

## How it works

Three run modes:

- **FULL** — wave pipeline: phase-0 gates, 5 parallel analysis subagents, 4 parallel generators subagents fed by `preanalysis_reports`, root synthesis (including the root-drawn dependency diagram).
- **PARTIAL** — single-artifact run from fresh memory with a HARD freshness gate.
- **REFRESH** — diff-driven surgical update of stale artifacts: staleness detector (lockfiles/generated/vendor/tests excluded), metrics to the user, always-ask, subagents read only the `.tmp/repo-audit/` diff.

The repo concept (prerequisite gate, type detection, freshness, memory layout, findings routing) lives in `entity-protocol`; memory mechanics live in `serena-protocol`; git tracking follows the frontmatter-protocol tracking extension.

## Layout

```text
repo-audit/
├── SKILL.md                  # orchestrator: modes, wave pipeline, routing index
├── README.md
└── references/
    ├── shared/               # subagent base prompt, gates, REFRESH, synthesis, conventions
    ├── analysis/             # wave 1: explorer + domain (4 anchors)
    ├── generators/           # wave 2: risks + dependencies (3 anchors)
    ├── templates/            # artifact templates (card, business, dependencies, glossary)
    └── checklists.md         # quality checklists for all modes
```

Status: `draft: true` until the transition cutover (see the repo-audit merge plan in Serena memory: `plans/project/repo_audit_implementation`).
