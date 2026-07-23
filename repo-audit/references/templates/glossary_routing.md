# Memory Routing, Glossary Rules, and Metadata (repo-audit)

[ref: #ra-tpl-glossary]

## Dedicated business-domain namespace

This skill introduces and owns the `repos/<repo>/<topic>` namespace.
`repos/` memories are repo-scoped, so the repo card prerequisite from
`entity-protocol` (`[ref: #entity-prerequisite]`) applies.

| Memory | Purpose |
|---|---|
| `repos/<repo>/business.md` | Executive summary and full report (or split point) |
| `repos/<repo>/entities/<business_entity>.md` | Detailed entity/value object/aggregate description |
| `repos/<repo>/processes/<process_name>.md` | Business process flow and state transitions |
| `repos/<repo>/rules/<topic>.md` | Business rules and invariants |
| `repos/<repo>/integrations/<topic>.md` | External actors and systems |
| `repos/<repo>/risks/<topic>.md` | Domain risks, gaps, contradictions |
| `repos/<repo>/glossary` | Repo-specific business terms |

Findings that are not domain-specific (e.g., implementation quirks, naming
inconsistencies, missing docs) should be routed to the canonical namespaces:

- `notes/<repo>/<topic>` — observations and ambiguities.
- `decisions/<repo>/<topic>` — business-driven architectural choices.
- `bugs/<repo>/<topic>` — confirmed incorrect business behavior.

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
  `repos/<repo>/business.md`.
- Keep the **detailed risk register** in `repos/<repo>/risks/<topic>.md`.
- If a finding is severe enough to be tracked as a bug, route it to
  `bugs/<repo>/<topic>` instead of `repos/<repo>/risks/`.

## Project glossary

The glossary is project-wide knowledge and lives at `project/glossary`.

### Reading the glossary

Before every analysis, read `project/glossary`. If it does not exist, create it.

### Creating the glossary

Use `write_memory` with a project-wide metadata header. Git source is
`.serena`; collect the tracking fields per the frontmatter-protocol tracking
extension (`[ref: #tracking-fields]`, `[ref: #tracking-git-commands]`).

Initial content:

```markdown
---
title: Project glossary
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
repo: generic
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

The glossary is a living contract: actively ADD new terms, REMOVE obsolete ones (no longer backed by code evidence), and REFINE definitions as the code evolves — a stale term is worse than a missing one.

Mutate the glossary per `serena-protocol` `[ref: #serena-memory-mutation]` (append via `edit_memory`; verify and persist as prescribed there).

For each new or refined term, add a row:

```markdown
| Order | A customer's request to purchase goods | order_service | `orders/model.py:23` |
```

When refining an existing term, use `edit_memory` to update only that row.

Mark changes in the report:

- `added` — new term.
- `refined` — definition improved.
- `moved` — term relocated between `project/glossary` and
  `repos/<repo>/glossary`.
- `removed` — term deleted as obsolete (no code evidence).

## Repo glossary

Repo-specific terms live at `repos/<repo>/glossary`. This is a
repo-scoped memory, so the repo card prerequisite applies
(`[ref: #entity-prerequisite]`).

### Creating the repo glossary

Use `write_memory` with a repo-scoped metadata header. Git source is the
repo's own repository; collect the tracking fields per the
frontmatter-protocol tracking extension (`[ref: #tracking-fields]`, `[ref: #tracking-git-commands]`).

Initial content:

```markdown
---
title: <Repo> glossary
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
repo: <repo-name>
branch: <branch>
commit: <7-char-short-hash>
committed_at: YYYY-MM-DDTHH:MM:SSZ
source: <repo-path>
---

# <Repo> glossary

## Terms

| Term | Definition | Related entities | Source |
|---|---|---|---|
```

### Updating the repo glossary

Mutate per `serena-protocol` `[ref: #serena-memory-mutation]` (append via `edit_memory`; verify and persist as prescribed there). The same add/remove-obsolete/refine duty as for the project glossary applies here.

When a term should move between `project/glossary` and
`repos/<repo>/glossary`, remove it from the old location and add it to the
new one, noting the move in the report.

## Naming rules

- Memory names use `snake_case` with underscores. No hyphens.
- Directory dashes in repo names become underscores (`my-service` →
  `my_service`).
- One memory = one focused topic.
- If an existing path violates the naming convention, rename it immediately
  per `[ref: #serena-naming]` before editing.

## Metadata headers

### For `repos/<repo>/...` memories

Git source: the repo's own repository; collect the tracking fields per the
frontmatter-protocol tracking extension (`[ref: #tracking-fields]`, `[ref: #tracking-git-commands]`).

Use the current YAML frontmatter standard from `[ref: #serena-metadata]`:

```yaml
---
title: <Title matching H1>
created_at: <UTC ISO 8601>
updated_at: <UTC ISO 8601; refresh on every edit>
repo: <repo-name>
branch: <branch>
commit: <7-char-short-hash>
committed_at: <UTC ISO 8601>
source: <project-relative path with optional line range>
---

# <Title>
```

### For `project/glossary`

Git source: the project root git (or the `.serena` meta-repository when no project git exists). `repo: generic`.
