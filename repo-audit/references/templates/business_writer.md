---
subject: "Business-domain report synthesis; five subagent reports, contradiction hierarchy, glossary delta, single-report template, split-report structure, executive summary, entity process rule integration risk files, metadata header, anti-patterns, `repos/<repo>/business`, Mermaid flows, thresholds, header refresh."
index:
  - anchor: ra-tpl-business-writer
    what: "The business-report synthesis contract: five domain reports become the final memory output without re-exploring code."
    problem: "Root receives five domain reports; re-exploring code burns budget while shapeless assembly loses business picture; meaning evaporation, report neglect, synthesis confusion, re-exploration temptation, resource drain, assembly drift, effort duplication, coherence failure."
    use_when: "Synthesizing the business report from domain-wave reports; reviewing the five-input contract."
    avoid_when: "Wave prompts themselves — `analysis/domain.md` and `generators/domain.md`; technical card writing — overview templates."
    expected: "One coherent business artifact set from five reports, zero code re-reads."
  - anchor: ra-tpl-business-synthesis
    what: "The synthesis steps: cross-report comparison, conflict hierarchy, terminology delta, single-vs-split decision, frontmatter refresh."
    problem: "Reports conflict with each other and with glossary terms; careless merging imports contradictions into canonical memory; conflict smuggling, glossary drift, step skipping, canonical pollution, precedence doubt, import accidents, haste damage."
    use_when: "Merging domain reports; resolving factual conflicts; building the glossary delta; deciding report shape."
    avoid_when: "The hierarchy rules themselves — `serena-protocol` `[ref: #serena-contradictions]` owns them."
    expected: "Conflicts resolved by precedence, terminology delta unified, shape decided, headers fresh."
  - anchor: ra-tpl-business-single
    what: "The single-report template for compact domains (≤5 entities, ≤4 processes, ≤8 rules, ≤300 lines)."
    problem: "Compact domain gets fragmented into split files; reader chases five memories for one small picture; fragmentation, navigation chase, split overhead, small-picture scatter, template confusion, file hopping, context switching, overview loss."
    use_when: "Domain under the thresholds; writing `repos/<repo>/business.md` as one file; choosing section order."
    avoid_when: "Complex domains — the split structure below; metadata rules — `[ref: #tracking-fields]`."
    expected: "One complete business.md with all sections in order."
  - anchor: ra-tpl-business-split
    what: "The split-report structure: executive summary plus focused files per entity, process, rule, integration, risk."
    problem: "Complex domain crammed into one file; readers sink in mega-report and cannot find their slice; bloat, slice fog, cramming, navigation failure, structure absence, reader fatigue, content overflow, discovery stall, orientation loss."
    use_when: "Domain exceeds thresholds; creating split files; structuring the executive summary."
    avoid_when: "Compact domains — single template; the decision itself — `[ref: #ra-synthesis-single-vs-split]`."
    expected: "Executive summary links to complete focused files."
  - anchor: ra-tpl-business-split-guidance
    what: "The split guidance: summary-only business.md, shared metadata header per split file."
    problem: "Split files diverge in headers or repeat summary content verbatim; divergence, header drift, guidance absence, consistency decay, content echo, template fork, metadata chaos, duplication spiral, shape rot, copy drift, uniformity loss, split drift."
    use_when: "Writing any split file; deciding what stays in the summary; stamping split headers."
    avoid_when: "The file templates themselves — the split structure above."
    expected: "Summary stays executive; every split file carries fresh identical header shape."
  - anchor: ra-tpl-business-antipatterns
    what: "The eight anti-patterns with bad/good pairs: card copying, vague entities, triggerless processes, missing Mermaid, unanchored rules, unanchored risks, infra plumbing, mega-subagent."
    problem: "Business reports degrade into tech-card copies and vague inventories; business meaning vanishes and reviewers bounce reports; degradation, meaning loss, anti-pattern drift, quality erosion, shallowness, copycat decay, reviewer rejection, formlessness, focus collapse."
    use_when: "Reviewing a business report before saving; learning what business-focused means concretely; rejecting shallow output."
    avoid_when: "Positive templates — the single and split structures above."
    expected: "Reports avoided all eight failure shapes."
---

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

[ref: #ra-tpl-business-synthesis]

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

[ref: #ra-tpl-business-single]

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

[ref: #ra-tpl-business-split]

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

[ref: #ra-tpl-business-split-guidance]

If the report is long, split it per `## Split-report structure` above: `repos/<repo>/business.md` carries the executive summary only; the focused files (`entities/`, `processes/`, `rules/`, `integrations/`, `risks/` subdirs) are templated there. The single-vs-split decision itself is owned by `references/shared/synthesis.md` (`[ref: #ra-synthesis-single-vs-split]`).

Each split memory must include the same metadata header with fresh git context.

## Anti-patterns

[ref: #ra-tpl-business-antipatterns]

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
