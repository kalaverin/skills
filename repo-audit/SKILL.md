---
name: repo-audit
description: "MANDATORY skill for full repository audits: creates and maintains repo cards (`repos/<repo>/overview`), business-domain reports (`repos/<repo>/business`), dependency cards (`repos/<repo>/dependencies`), and the project-level index (`project/dependencies`). Three run modes: FULL (wave pipeline of parallel subagents), PARTIAL (single artifact from fresh memory), REFRESH (diff-driven update of stale artifacts). Use when the user asks to: create or study an entity card / repo card, explore or study a project/service/repository, run business or domain analysis, extract business rules, build a dependency card or dependency map, audit a repo, or refresh stale cards. Triggers on 'entity card', 'repo card', 'изучи проект/сервис/репозиторий', 'бизнес-анализ', 'доменная модель', 'карточка зависимостей', 'карта зависимостей', 'аудит репо'."
version: 0.1.0
triggers:
  request: "create entity card, create project card, create service card, create repository card, entity card, project card, service card, repository card, repo card, explore project, explore service, explore repository, study project, study service, study repository, изучи проект, изучи сервис, изучи репозиторий, создай карточку проекта, создай карточку сервиса, создай карточку репозитория, карточка репо, business entities, business expertise, domain analysis, domain events, бизнес-сущности, анализ бизнеса, business analysis, business domain analysis, analyze business domain, business logic analysis, business rules analysis, what business does, business purpose, business meaning, domain model analysis, бизнес-анализ, бизнес-логика, бизнес-смысл, доменная модель, бизнес-правила, зачем нужно приложение, бизнес-цель, dependency card, create dependency card, dependency map, create dependency map, architecture dependencies, service dependencies, what does it depend on, карточка зависимостей, создай карточку зависимостей, карта зависимостей, изучи зависимости, repo audit, аудит репо, аудит репозитория, полный аудит, обнови карточки, refresh cards, update stale cards"
requires:
  - entity-protocol
  - frontmatter-protocol
  - serena-protocol
  - subagents-protocol
---

# SKILL: repo-audit — Full Repository Audit Pipeline

One skill, three artifacts: the technical repo card (`repos/<repo>/overview`), the business-domain report (`repos/<repo>/business` + optional split files), and the dependency card (`repos/<repo>/dependencies` + optional `project/dependencies`). Replaces the legacy `project-audit` / `business-audit` / `dependencies-audit` trio.

## Skill Boundary

- **This skill owns** the audit pipeline: gates, wave orchestration, subagent prompts, artifact templates, synthesis, and quality checklists.
- **This skill does NOT own** the repo concept (definition, prerequisite gate, identity/freshness, `repos/` layout, findings routing, the namespace registry) — that is `entity-protocol`.
- **This skill OWNS** the type taxonomy/detection and per-type interface exhaustiveness as part of the audit pipeline: `references/analysis/type_detection.md` (`[ref: #repo-type-detection]`, `[ref: #repo-interface-exhaustiveness]`) — currently flagged REWORK-REQUIRED.
- **This skill does NOT own** general memory mechanics (metadata headers, mutation protocol, persistence) — that is `serena-protocol`. Tracking fields are stamped per the frontmatter-protocol tracking extension.
- **This skill does NOT own** memory reconciliation of unrelated scopes — load `serena-audit` for that.
- **This skill does NOT own** language-specific coding standards or protocol/schema design. When the audit task also involves editing code or designing/changing `.proto`/OpenAPI definitions, run a CONTEXTUAL RE-EVALUATION of the skill registry for that domain (per the frontmatter-protocol include extension: match the task against every skill's `request` triggers from memory) and load the matching skills before touching those files — `python-lang` for Python code, `protobuf-lang`/`api-design` for proto/OpenAPI design.

## Run Modes

| Mode | When | What runs |
|---|---|---|
| **FULL** | No `repos/<repo>/overview` exists, or the user asks for a full audit | Phase 0 gates → analysis wave (5 subagents) → generators wave (4 subagents) → root synthesis of all artifacts |
| **PARTIAL** | Card exists; user asks for one artifact (e.g. only dependencies, only business) | Phase 0 gates + HARD freshness gate → only the subagents producing that artifact, fed from fresh memory |
| **REFRESH** | Any required input is stale (`commit` ≠ HEAD), or the user reports stale cards | Staleness detector → ALWAYS ask the user with metrics → diff-driven surgical update via `.tmp/repo-audit/` |

Mode selection details and all gates: `references/shared/gates.md` (`[ref: #ra-gates]`). REFRESH flow: `references/shared/refresh.md` (`[ref: #ra-refresh]`).

## FULL Mode — Wave Pipeline

**Phase 0 (root, gates):** input acceptance (one repo per run) → prerequisite gate (`entity-protocol` `[ref: #entity-prerequisite]`) → naming compliance → type detection (`[ref: #repo-type-detection]`) → glossary seeds → memory path list.

**Analysis wave (5 read-only `explore` subagents in parallel, 3595 s each):**

1. Tech explorer (`analysis/explorer.md` `[ref: #ra-explorer]`).
2. Domain entities (`analysis/domain.md` `[ref: #ra-domain-entities]`).
3. Domain processes (`analysis/domain.md` `[ref: #ra-domain-processes]`).
4. Domain rules (`analysis/domain.md` `[ref: #ra-domain-rules]`).
5. Domain integrations (`analysis/domain.md` `[ref: #ra-domain-integrations]`).

Every subagent prompt = the common base prompt (`shared/subagent_base.md` `[ref: #ra-subagent-base]`) + its specialization section.

**Generators wave (4 read-only `explore` subagents in parallel, 3595 s each)** — each receives `preanalysis_reports` (the analysis-wave reports):

1. Domain risks (`generators/domain.md` `[ref: #ra-domain-risks]`).
2. Dependency interface extractor (`generators/dependencies.md` `[ref: #ra-deps-interface]`).
3. Dependency downstream mapper (`generators/dependencies.md` `[ref: #ra-deps-downstream]`).
4. Dependency infra & libs catalog (`generators/dependencies.md` `[ref: #ra-deps-infra]`).

**Root synthesis:** generate the directory tree yourself (never delegate) → write `repos/<repo>/overview` (template `templates/overview_card.md`) → write `repos/<repo>/business` (single or split per thresholds; template `templates/business_writer.md`) → write `repos/<repo>/dependencies` and draw the Mermaid diagram yourself (template `templates/dependencies_card.md`) → update both glossaries (`templates/glossary_routing.md`) → route findings (`entity-protocol` `[ref: #entity-namespace-registry]`) → verify read-backs → `just serena-checkpoint`. Synthesis rules: `shared/synthesis.md` (`[ref: #ra-synthesis]`). Conventions (mermaid, exclusions, evidence, dates): `shared/conventions.md` (`[ref: #ra-conventions]`).

In FULL mode the analysis-wave subagents explore the codebase; the generators wave works from `preanalysis_reports` plus targeted code reads. Code covered by a fresh input (`commit == HEAD`) is never re-read.

## PARTIAL Mode

Run the gates, then launch only the subagents that produce the requested artifact, feeding them from fresh memory instead of new exploration where the freshness rule allows. The freshness gate is HARD: stale inputs → switch to the REFRESH flow and ask the user.

## REFRESH Mode

Staleness detector per artifact → present metrics and ALWAYS ask the user (recommend REFRESH under 1000 lines / 10%, FULL over 5000 lines / 30%) → root prepares `.tmp/repo-audit/` (diff, numstat, impact.md) → one subagent per affected artifact reads only the diff → root applies updated sections, bumps tracking fields → deletes the scratch dir → persists. Full procedure: `references/shared/refresh.md` (`[ref: #ra-refresh]`).

## Lazy-Load Routing Index

Do not read every reference file. Extract only the anchors needed, per the frontmatter-protocol lazy-load mechanics. This corpus uses the `separate` marker placement form (markdown-protocol `marker_style`): exactly one blank line above and below every `[ref:]` marker.

| Trigger / situation | File | Anchor |
|---|---|---|
| Gates, mode selection, freshness gate | `references/shared/gates.md` | `[ref: #ra-gates]` |
| Type detection and per-type interface exhaustiveness (REWORK-REQUIRED) | `references/analysis/type_detection.md` | `[ref: #repo-type-detection]`, `[ref: #repo-interface-exhaustiveness]` |
| REFRESH mode: detector, impact map, scratch layout | `references/shared/refresh.md` | `[ref: #ra-refresh]` |
| Launching any subagent (base prompt) | `references/shared/subagent_base.md` | `[ref: #ra-subagent-base]` |
| Synthesis, single/split, persist, summary | `references/shared/synthesis.md` | `[ref: #ra-synthesis]` |
| Mermaid, exclusions, evidence, dates | `references/shared/conventions.md` | `[ref: #ra-conventions]` |
| Tech explorer subagent | `references/analysis/explorer.md` | `[ref: #ra-explorer]` |
| Domain subagents (entities, processes, rules, integrations) | `references/analysis/domain.md` | `[ref: #ra-domain-entities]`, `[ref: #ra-domain-processes]`, `[ref: #ra-domain-rules]`, `[ref: #ra-domain-integrations]` |
| Risks subagent (generators wave) | `references/generators/domain.md` | `[ref: #ra-domain-risks]` |
| Dependency subagents (interface, downstream, infra) | `references/generators/dependencies.md` | `[ref: #ra-deps-interface]`, `[ref: #ra-deps-downstream]`, `[ref: #ra-deps-infra]` |
| Repo card template (+ type sections) | `references/templates/overview_card.md` | `[ref: #ra-tpl-overview-common]`, `[ref: #ra-tpl-overview-grpc]`, `[ref: #ra-tpl-overview-rest]`, `[ref: #ra-tpl-overview-temporal]`, `[ref: #ra-tpl-overview-infra]`, `[ref: #ra-tpl-overview-library]` |
| Business report writer (single/split, anti-patterns) | `references/templates/business_writer.md` | `[ref: #ra-tpl-business-writer]` |
| Dependency card template (per-repo) | `references/templates/dependencies_card.md` | `[ref: #ra-tpl-deps-card]` |
| Project-level dependency index | `references/templates/dependencies_project.md` | `[ref: #ra-tpl-deps-project]` |
| Glossaries and memory routing | `references/templates/glossary_routing.md` | `[ref: #ra-tpl-glossary]` |
| Quality checklists (all modes) | `references/checklists.md` | `[ref: #ra-checklists]` |

Extract a section per the canonical loader mechanics in `frontmatter-protocol` `[ref: #lazy-load-routing]` (bounded extraction — never a blind `rg -A N` window; the exact command lives there, not here).

## Do Not

- Do not analyze more than one repo per run (except the project-level index, which requires all fresh per-repo cards).
- Do not launch a single "analyze everything" subagent; use the wave pipeline.
- Do not explore the codebase directly as the root agent; delegate to the read-only subagents (3595 s timeouts).
- Do not re-read code covered by a fresh input (`commit == HEAD`); work diff-driven when stale.
- Do not put git tracking metadata into subagent reports; the root stamps tracking fields per the frontmatter-protocol tracking extension.
- Do not generate from stale inputs without asking the user (REFRESH flow).
- Do not include Sentry, Prometheus, tests, linters, CI, Makefile, Docker, or entry points unless they are actual runtime dependencies.
- Do not write environment variable values, defaults, examples, or secrets.
- Do not dump raw subagent output into memory; synthesize first.
- Do not write business-domain findings into `repos/<repo>/overview` (the technical card) — and do not write technical/implementation detail into `repos/<repo>/business` either. The artifacts intersect, but they describe different things.
- Do not skip frontmatter refresh, read-back verification, or `just serena-checkpoint` after any memory mutation.

**Violation protocol:** if you violate a gate, the wave topology, the diff-driven rules, or the tracking ownership, halt immediately, discard the offending operation, reload the relevant anchor, and redo the step correctly.
