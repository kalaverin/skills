---
name: business-audit
description: >
  MANDATORY skill for extracting business/domain entities, processes, rules,
  invariants, actors, and integration points from a repository's source code.
  Use when the user asks for: business entity analysis, domain model extraction,
  business logic expertise, "what business does this repo do", "business
  rules", "domain events", or when expanding an existing `project-audit`
  entity card with a business-domain view. Triggers on keywords such as
  "business entities", "domain analysis", "business logic", "business
  expertise", "domain model", "what business does", "бизнес-сущности",
  "анализ бизнеса", "доменная модель", "бизнес-правила". Requires an existing
  entity card at `entities/<entity>` and a project glossary at
  `project/glossary` (created and maintained by this skill).
triggers:
  all:
    files: ".serena/memories/"
    request: "business analysis, business domain analysis, analyze business domain, business logic analysis, business rules analysis, what business does, business purpose, business meaning, domain model analysis, бизнес-анализ, бизнес-логика, бизнес-смысл, доменная модель, бизнес-правила, зачем нужно приложение, бизнес-цель"
requires:
  - project-audit
  - serena-protocol
---

# business-audit

Extract and document the business/domain layer hidden in a repository's code.
This skill produces business-domain reports and updates the project glossary.

## Skill Boundary

- **This skill owns** the business/domain analysis workflow: inputs,
  specialized subagent prompts, report synthesis, glossary maintenance, and
  `logic/<entity>/<topic>` memory routing.
- **This skill does NOT own** the technical entity card. That is the job of
  `project-audit`. This skill requires an existing card at `entities/<entity>`.
- **This skill does NOT own** general Serena memory rules (scopes, naming,
  YAML frontmatter, metadata, mutation, persistence). Those live in
  `serena-protocol`. Load it automatically whenever this skill is used.
- **This skill does NOT own** memory reconcilation or bulk header refreshes.
  Load `serena-audit` when the task is to update or audit existing
  business-domain memories.
- **This skill does NOT own** language-specific coding standards. Load
  `python-lang`, `protobuf-lang`, or `api-design` only if
  the analysis also involves editing code in those domains.

## Lazy-Load Protocol

Do not read every reference file. Use the Routing Index below to load only the
sections needed for the current sub-task.

### Routing Index

| Trigger | File | Anchor |
|---|---|---|
| Full workflow, inputs, constraints, single/split decision | `references/01_make_business_analysis.md` | `[ref: #bda-workflow]` |
| Common subagent rules (memory access, evidence, exclusions) | `references/02_business_domain_base_prompt.md` | `[ref: #bda-base-prompt]` |
| Subagent: entity catalog | `references/03_entity_catalog_subagent.md` | `[ref: #bda-entities]` |
| Subagent: process map and workflows | `references/04_process_map_subagent.md` | `[ref: #bda-processes]` |
| Subagent: business rules and invariants | `references/05_rules_subagent.md` | `[ref: #bda-rules]` |
| Subagent: actors and external integrations | `references/06_integrations_subagent.md` | `[ref: #bda-integrations]` |
| Subagent: risks, gaps, contradictions | `references/07_risks_subagent.md` | `[ref: #bda-risks]` |
| Synthesis templates and anti-patterns | `references/08_business_domain_writer.md` | `[ref: #bda-writer]` |
| Memory routing, glossary rules, metadata | `references/09_domain_memory_routing.md` | `[ref: #bda-memory]` |

Extract a reference section with `rg` (example):

```bash
rg -A 200 '^\[ref: #bda-processes\]' \
  business-audit/references/04_process_map_subagent.md
```

Stop reading when you reach the next `[ref: #...]` marker or the end of the
relevant subsection.

## Master Execution Workflow

When the user asks for a business/domain analysis, execute this workflow. For
full details, lazy-load the anchors above.

1. **Accept exactly one entity per run.**
   - Obtain `entity_name` (`snake_case`) and `entity_path` from the user.
   - If the request mentions multiple entities, STOP and ask the user to pick
     one. Do not batch entities.
2. **Verify entity card exists.** Apply `[ref: #serena-entity-prerequisite]`
   from `serena-protocol`. If `entities/<entity_name>` does not exist,
   STOP and ask the user to create it via `project-audit`.
3. **Ensure glossaries exist.** Check whether `project/glossary` and
   `logic/<entity_name>/glossary` exist. Create seed glossaries where missing.
4. **Collect relevant memory paths.** Build a list of absolute paths to all
   relevant `.serena/memories/` files for this entity:
   `entities/<entity_name>`, `logic/<entity_name>/...`, `bugs/<entity_name>/...`,
   `notes/<entity_name>/...`, `decisions/<entity_name>/...`,
   `project/glossary`, and `logic/<entity_name>/glossary`. Do not read the
   contents yourself; pass only the path list.
5. **Verify naming compliance.** Rename any non-compliant memory paths
   immediately per `[ref: #serena-naming]`.
6. **Launch parallel specialized subagents.** For the single target entity,
   create **five** read-only `explore` subagents in parallel, each with a
   narrow business task:
   - Entity catalog (`[ref: #bda-entities]`).
   - Process map and workflows (`[ref: #bda-processes]`).
   - Business rules and invariants (`[ref: #bda-rules]`).
   - Actors and external integrations (`[ref: #bda-integrations]`).
   - Risks, gaps, and contradictions (`[ref: #bda-risks]`).
   Each subagent receives the same memory path list and `entity_path`, plus
   the common base prompt (`[ref: #bda-base-prompt]`). Timeout per subagent:
   at least **1800 seconds** (30 minutes).
7. **Synthesize the report.** Use the templates from `[ref: #bda-writer]` to
   combine the five subagent reports into the final business-domain output.
   Resolve contradictions using the hierarchy in `serena-protocol`
   (`[ref: #serena-contradictions]`).
8. **Decide single vs split report.** Use the criteria in `[ref: #bda-workflow]`:
   - Single file if ≤5 domain entities, ≤4 processes, ≤8 rules, and the result
     fits under ~300 lines.
   - Split model otherwise: executive summary at
     `logic/<entity>/business_domain_report` plus focused files under
     `logic/<entity>/entities/`, `logic/<entity>/processes/`,
     `logic/<entity>/rules/`, `logic/<entity>/integrations/`, and
     `logic/<entity>/risks/`.
9. **Update the glossaries.** Add common/cross-entity terms to
   `project/glossary` and entity-specific terms to
   `logic/<entity_name>/glossary`. Refine definitions in both. Mark changes as
   `added`, `refined`, or `moved`.
10. **Write business-domain memories.** Save findings to `logic/<entity_name>/...`
    following the routing table in `[ref: #bda-memory]`. Route anomalies,
    ambiguities, and contradictions to `notes/<entity_name>/...` or
    `decisions/<entity_name>/...` per `serena-protocol`.
11. **Verify and persist.** Read back every saved memory to confirm it was
    written correctly, then run the configured persistence command (commonly
    `just serena-checkpoint`) from the project root.

## Glossary Contract

- Two glossaries are mandatory preconditions:
  - `project/glossary` — cross-cutting, product-wide business terms.
  - `logic/<entity_name>/glossary` — terms specific to this entity's business
    domain.
- If either glossary is missing, create a seed glossary before running the
  subagents.
- During analysis, the agent must actively add new business terms, remove
  obsolete ones, and refine definitions based on code evidence.
- Each glossary entry must include: term, concise definition, scope
  (`common` / `<entity_name>`), related entity tag(s), and a code anchor
  (file:line or symbol) when available.

## Do Not

- Do not analyze more than one entity in a single run.
- Do not launch a single "analyze everything" subagent; use parallel
  specialized subagents.
- Do not analyze a repository whose entity card does not exist.
- Do not write business-domain findings into `entities/<entity>`; that card is
  for the technical overview only.
- Do not explore the codebase directly as the root agent; delegate to the
  read-only subagents.
- Do not dump full memory contents into subagent prompts; pass only paths.
- Do not include Sentry, Prometheus, tests, linters, CI, Makefile, Docker, or
  entry points in the business-domain report unless they directly encode
  business rules.
- Do not write environment variable values, defaults, examples, or secrets.
- Do not skip YAML frontmatter refresh or `just serena-checkpoint` after any
  memory mutation.
