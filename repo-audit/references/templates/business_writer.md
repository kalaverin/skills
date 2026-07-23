# Business-Domain Report Synthesis (repo-audit)

[ref: #ra-tpl-business-writer]

The root agent receives five detailed subagent reports:

1. `entities` — entity catalog.
2. `processes` — process map and workflows.
3. `rules` — business rules and invariants.
4. `integrations` — actors and external systems.
5. `risks` — risks, gaps, contradictions.

The root agent's job is to synthesize them into the final Serena memory output.
Do not explore the code again; rely on the subagent reports and resolve any
contradictions between them.

## Synthesis steps

1. Read all five subagent reports.
2. Compare factual claims across reports. If sources conflict, apply the
   hierarchy in `[ref: #serena-contradictions]`:
   - Newer memory overrides older memory.
   - `AGENTS.md` wins over session memory unless explicitly overridden.
   - Repo git metadata wins over `.serena` metadata for repo-specific facts.
3. Build a unified glossary delta:
   - Terms to add/refine/move in `project/glossary`.
   - Terms to add/refine/move in `repos/<repo>/glossary`.
4. Decide single vs split report using the criteria in `references/shared/synthesis.md` (`[ref: #ra-synthesis]`).
5. Write the final memory/memories with refreshed YAML frontmatter.

## Single-report template

Use when the domain is compact (≤5 entities, ≤4 processes, ≤8 rules, ≤300
lines). Save as `repos/<repo>/business.md`.

### Metadata header

Use the repo's own git repository for metadata (`repo: <repo-name>`), per the
frontmatter-protocol tracking extension (`[ref: #tracking-fields]`, `[ref: #tracking-git-commands]`).

```yaml
---
title: <Repo> business domain report
created_at: <UTC ISO 8601>
updated_at: <UTC ISO 8601>
repo: <repo-name>
branch: <branch>
commit: <7-char-short-hash>
committed_at: <UTC ISO 8601>
source: <repo-path>
---
```

### Section order

```markdown
# <Repo> business domain report

## Business purpose
1–2 paragraphs describing the business problem the service solves and the value
it delivers. Mention primary actor(s) and the core transaction or lifecycle.

## Key domain entities
- **EntityName** — one-line business definition.
- **EntityName** — one-line business definition.

## Key business processes
- **Process name** — trigger, actor, and one-line outcome.
- **Process name** — trigger, actor, and one-line outcome.

### <Process name>
**Trigger:** ...
**Actors:** ...
**Flow:**
1. ...
2. ...

```mermaid
flowchart TD
    A[...] --> B[...]
```

**Code anchors:** ...

## Key business rules

### R1: <Rule statement>
- **Enforcement:** `path/file.py:line` (`symbol`)
- **Violation consequence:** ...
- **Related entities:** ...

## Key external integrations
- **System/Service** — role and interaction pattern.

## Risks and gaps
- `critical` / `warning` / `info` summary items with code anchors.
```

## Split-report structure

Use for complex domains. Save the executive summary as
`repos/<repo>/business.md` and focused files as described below.

### Executive summary (`repos/<repo>/business.md`)

```markdown
# <Repo> business domain report

## Business purpose
## Key domain entities (bullet list)
## Key business processes (bullet list)
## Key external integrations (bullet list)
## Risks and gaps (summary)

See `repos/<repo>/entities/*`, `repos/<repo>/processes/*`,
`repos/<repo>/rules/*`, `repos/<repo>/integrations/*`, and
`repos/<repo>/risks/*` for details.
```

### Entity files (`repos/<repo>/entities/<name>.md`)

```markdown
# <Repo> — <Business entity>

## Definition
## Type
## Key attributes
## Lifecycle / state machine
## Relationships
## Invariants
## Code anchors
## Glossary terms
```

### Process files (`repos/<repo>/processes/<name>.md`)

```markdown
# <Repo> — <Process name>

## Trigger
## Actors
## Step-by-step flow
## Mermaid diagram
## Events, signals, side effects
## Error and timeout paths
## Code anchors
```

### Rule files (`repos/<repo>/rules/<topic>.md`)

```markdown
# <Repo> — <Topic> rules

## R1: <Rule statement>
- **Enforcement:** `file.py:line` (`symbol`)
- **Violation consequence:** ...
- **Related entities:** ...

## R2: ...
```

### Integration files (`repos/<repo>/integrations/<topic>.md`)

```markdown
# <Repo> — <Integration> integration

## System role
## Interaction pattern
## Request/response semantics
## Failure modes
## Code anchors
```

### Risk files (`repos/<repo>/risks/<topic>.md`)

```markdown
# <Repo> — <Topic> risks

## CRITICAL: <Risk title>
- **Description:** ...
- **Impact:** ...
- **Code anchor:** ...

## WARNING: ...
## INFO: ...
```

## Memory split guidance

If the report is long, split it into focused memories:

- `repos/<repo>/business.md` — executive summary only.
- `repos/<repo>/entities/<business_entity>.md` — one per significant entity.
- `repos/<repo>/processes/<process_name>.md` — one per process.
- `repos/<repo>/rules/<topic>.md` — grouped rules.
- `repos/<repo>/integrations/<topic>.md` — external actors/systems.
- `repos/<repo>/risks/<topic>.md` — risks and gaps.

Each split memory must include the same metadata header with fresh git context.

## Anti-patterns

### Copying the technical repo card
Bad:
```markdown
## Technology stack
- Python 3.11, Temporal SDK 1.18, PostgreSQL.
```
Good: stack belongs in `repos/<repo>/overview`. The business report answers *what
business* the code does.

### Vague entity list
Bad:
```markdown
## Key domain entities
- Wallet
- Transfer
- Order
```
Good:
```markdown
## Key domain entities
- **Wallet** — deposit address with lifecycle states and types.
- **Transfer** — on-chain movement classified as deposit, withdrawal, top-up,
  or internal movement.
- **Order** — billing order created for deposits and top-ups.
```

### Process without trigger or final state
Bad:
```markdown
## Key business processes
- Deposit processing.
```
Good:
```markdown
## Key business processes
- **Deposit processing** — triggered by inbound transfer detection; ends with
  accepted clearing or rejected refund.
```

### Missing Mermaid for non-trivial flows
Bad: a multi-step process described only in prose.
Good: prose + `flowchart TD` showing branches, errors, and final states.

### Rules without enforcement location
Bad:
```markdown
## Key business rules
- Deposits below 0.01 USDT are ignored.
```
Good:
```markdown
## Key business rules
- **R1: Deposits below 0.01 USDT are ignored** — enforced in
  `app/workflow/trc_20.py:88` (`process_transfer`).
```

### Risks without anchors or severity
Bad:
```markdown
## Risks and gaps
- Hardcoded thresholds.
```
Good:
```markdown
## Risks and gaps
- `warning` Deposit threshold `0.01` USDT is hardcoded in
  `app/workflow/trc_20.py:91`.
```

### Including infrastructure plumbing
Bad:
```markdown
## Key external integrations
- Prometheus Pushgateway for resource metrics.
```
Good: include Prometheus only if a metric directly drives a business decision;
otherwise omit.

### Launching one subagent for everything
Bad: a single "analyze the business domain" subagent that returns a shallow,
overloaded report.
Good: five parallel specialized subagents, each reporting in depth on one
aspect, then root-agent synthesis.
