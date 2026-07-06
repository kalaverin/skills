[ref: #bda-workflow]

# Business-domain analysis: goal, inputs, and constraints

## Goal

Produce a structured, evidence-based description of the business layer encoded
in a repository's source code. The output answers:

- What business problem does this code solve?
- What are the core business entities, value objects, and aggregates?
- What business processes, state machines, and events exist?
- What business rules and invariants are enforced?
- Who are the actors and external systems?
- What domain language is used, and how should the glossary be updated?

## Inputs

| Input | Source | Required |
|---|---|---|
| `entity_name` | User | Yes |
| `entity_path` | User / entity card | Yes |
| Entity card | `entities/<entity>` | Yes |
| Project glossary | `project/glossary` | Yes |
| Entity glossary | `logic/<entity>/glossary` | Yes |
| Existing findings | `bugs/<entity>/...`, `notes/<entity>/...`, `decisions/<entity>/...` | No |
| Existing business-domain memory | `logic/<entity>/...` | No |
| Business context / questions | User prompt | No |

## Hard prerequisites

Before launching any subagent:

1. Accept **exactly one entity** per run. If the user mentions multiple
   entities, STOP and ask them to pick one.
2. `entities/<entity>` MUST exist. If not, STOP and ask the user to create it
   via `project-audit`.
3. `project/glossary` MUST exist. Create a seed glossary if it is missing.
4. `logic/<entity>/glossary` MUST exist. Create a seed glossary if it is missing.
5. Collect absolute paths to existing memories:
   - `entities/<entity>`
   - `logic/<entity>/...`
   - `bugs/<entity>/...`
   - `notes/<entity>/...`
   - `decisions/<entity>/...`
   - `project/glossary`
   - `logic/<entity>/glossary`
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
  `just agent-memory-commit`.

## Subagent strategy

Do not launch a single "analyze everything" subagent. Instead, launch **five**
parallel read-only `explore` subagents, each specialized on one business task:

1. **Entity catalog** (`[ref: #bda-entities]`) — domain entities, value objects,
   aggregates, enums, events.
2. **Process map** (`[ref: #bda-processes]`) — workflows, business processes,
   state machines.
3. **Business rules** (`[ref: #bda-rules]`) — validation, invariants,
   authorization, calculations.
4. **Actors and integrations** (`[ref: #bda-integrations]`) — human/system
   actors and external systems.
5. **Risks and gaps** (`[ref: #bda-risks]`) — contradictions, risks, missing
   docs, inconsistencies.

Each subagent receives the same memory path list and `entity_path`, plus the
common base prompt (`[ref: #bda-base-prompt]`). Timeout per subagent: at least
**1800 seconds** (30 minutes).

The root agent synthesizes the five detailed reports into the final
business-domain output.

## Single-report vs split-report decision

Use the **single-file** report when **all** of the following are true:

- ≤ 5 domain entities.
- ≤ 4 business processes.
- ≤ 8 business rules.
- The final report fits comfortably under ~300 lines.

Otherwise use the **split model**:

- Executive summary at `logic/<entity>/business_domain_report`.
- Focused files under:
  - `logic/<entity>/entities/<business_entity>`
  - `logic/<entity>/processes/<process_name>`
  - `logic/<entity>/rules/<topic>`
  - `logic/<entity>/integrations/<topic>`
  - `logic/<entity>/risks/<topic>`

These are files, not directories. Names MUST use `snake_case` with underscores
only (`[ref: #serena-naming]`).

## Pre-analysis checklist

Confirm before writing:

- [ ] Exactly one entity is selected.
- [ ] `entities/<entity>` exists.
- [ ] `project/glossary` and `logic/<entity>/glossary` exist.
- [ ] Existing `logic/<entity>/business_domain_report` was read (if present).
- [ ] Existing `bugs/<entity>/...`, `notes/<entity>/...`, `decisions/<entity>/...`
      were skimmed for business context.
- [ ] All memory path names are Serena-compliant.
