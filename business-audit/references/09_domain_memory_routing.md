[ref: #bda-memory]

# Memory routing, glossary rules, and metadata

## Dedicated business-domain namespace

This skill introduces and owns the `logic/<entity>/<topic>` namespace.
`logic/` memories are entity-scoped, so the entity card prerequisite from
`serena-protocol` applies.

| Memory | Purpose |
|---|---|
| `logic/<entity>/business_domain_report` | Executive summary and full report (or split point) |
| `logic/<entity>/entities/<business_entity>` | Detailed entity/value object/aggregate description |
| `logic/<entity>/processes/<process_name>` | Business process flow and state transitions |
| `logic/<entity>/rules/<topic>` | Business rules and invariants |
| `logic/<entity>/integrations/<topic>` | External actors and systems |
| `logic/<entity>/risks/<topic>` | Domain risks, gaps, contradictions |
| `logic/<entity>/glossary` | Entity-specific business terms |

Findings that are not domain-specific (e.g., implementation quirks, naming
inconsistencies, missing docs) should be routed to the canonical namespaces:

- `notes/<entity>/<topic>` — observations and ambiguities.
- `decisions/<entity>/<topic>` — business-driven architectural choices.
- `bugs/<entity>/<topic>` — confirmed incorrect business behavior.

## Synthesis from subagent reports

The root agent receives five specialized subagent reports (entities, processes,
rules, integrations, risks). It MUST:

1. Resolve contradictions using `[ref: #serena-contradictions]`.
2. Build a unified glossary delta.
3. Decide single vs split report.
4. Write final memories with refreshed YAML frontmatter.

Do not route raw subagent output directly to memory. Synthesize and edit for
consistency.

## Risk register routing

- Keep a **summary** of risks (3–8 bullets with severity and anchor) inside
  `logic/<entity>/business_domain_report`.
- Keep the **detailed risk register** in `logic/<entity>/risks/<topic>`.
- If a finding is severe enough to be tracked as a bug, route it to
  `bugs/<entity>/<topic>` instead of `logic/<entity>/risks/`.

## Project glossary

The glossary is project-wide knowledge and lives at `project/glossary`.

### Reading the glossary

Before every analysis, read `project/glossary`. If it does not exist, create it.

### Creating the glossary

Use `write_memory` with a project-wide metadata header. Git source is
`.serena`:

```bash
cd <workspace-root>/.serena
git rev-parse --abbrev-ref HEAD
git rev-parse --short HEAD
git log -1 --format=%cd --date=iso-strict
```

Initial content:

```markdown
---
title: Project glossary
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
repo: serena
branch: <branch>
commit: <7-char-short-hash>
committed_at: YYYY-MM-DDTHH:MM:SSZ
source: .serena
---

# Project glossary

## Terms

| Term | Definition | Scope | Related entities | Source |
|---|---|---|---|---|
```

### Updating the glossary

Use `edit_memory` with `mode: "regex"`, `needle: "\\Z"` to append new terms or
sections. Do NOT use `write_memory` unless you are replacing the entire file.

For each new or refined term, add a row:

```markdown
| Order | A customer's request to purchase goods | order_service | `orders/model.py:23` |
```

When refining an existing term, use `edit_memory` to update only that row.

Mark changes in the report:

- `added` — new term.
- `refined` — definition improved.
- `moved` — term relocated between `project/glossary` and
  `logic/<entity>/glossary`.

## Entity glossary

Entity-specific terms live at `logic/<entity>/glossary`. This is an
entity-scoped memory, so the entity card prerequisite applies.

### Creating the entity glossary

Use `write_memory` with an entity-scoped metadata header. Git source is the
entity's own repository:

```bash
cd <workspace-root>/<entity>
git rev-parse --abbrev-ref HEAD
git rev-parse --short HEAD
git log -1 --format=%cd --date=iso-strict
```

Initial content:

```markdown
---
title: <Entity> glossary
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
repo: <entity-name>
branch: <branch>
commit: <7-char-short-hash>
committed_at: YYYY-MM-DDTHH:MM:SSZ
source: <entity-path>
---

# <Entity> glossary

## Terms

| Term | Definition | Related entities | Source |
|---|---|---|---|
```

### Updating the entity glossary

Use `edit_memory` with `mode: "regex"`, `needle: "\\Z"` to append new terms.
Do NOT use `write_memory` unless you are replacing the entire file.

When a term should move between `project/glossary` and
`logic/<entity>/glossary`, remove it from the old location and add it to the
new one, noting the move in the report.

## Naming rules

- Memory names use `snake_case` with underscores. No hyphens.
- Directory dashes in entity names become underscores (`my-service` →
  `my_service`).
- One memory = one focused topic.
- If an existing path violates the naming convention, rename it immediately
  per `[ref: #serena-naming]` before editing.

## Metadata headers

### For `logic/<entity>/...` memories

Git source: the entity's own repository.

```bash
cd <workspace-root>/<entity>
git rev-parse --abbrev-ref HEAD
git rev-parse --short HEAD
git log -1 --format=%cd --date=iso-strict
```

Use the current YAML frontmatter standard from `[ref: #serena-metadata]`:

```yaml
---
title: <Title matching H1>
created_at: <UTC ISO 8601>
updated_at: <UTC ISO 8601; refresh on every edit>
repo: <entity-name>
branch: <branch>
commit: <7-char-short-hash>
committed_at: <UTC ISO 8601>
source: <project-relative path with optional line range>
---

# <Title>
```

### For `project/glossary`

Git source: `.serena`. `repo: serena`.

## Verification and persistence

1. After every `write_memory` or `edit_memory`, read the memory back to verify
   it.
2. Run the configured persistence command (commonly `just agent-memory-commit`)
   from the workspace root.
3. Do not skip persistence after any mutation.
