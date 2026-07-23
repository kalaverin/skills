# Subagent prompt: risks, gaps, and contradictions

[ref: #ra-domain-risks]

**Task:** Find risks, gaps, inconsistencies, and contradictions in the
business-domain layer of **one** service. You receive `preanalysis_reports` —
the reports of the analysis-wave subagents (entities, processes, rules,
integrations). You MUST base your risk analysis on them to identify what is
missing, ambiguous, or wrong, and read the code directly only in a targeted
way where evidence is missing.

## Required inputs (MUST read)

- `preanalysis_reports` — your primary source (all four analysis-wave reports).
- `repos/<repo>/overview`, `project/glossary`, `repos/<repo>/glossary`.
- Existing `repos/<repo>/business.md` and split files (if present).
- Targeted code reads ONLY to verify or fill gaps left by the reports.

## What to explore

1. **Missing documentation** — business rules without anchors, processes without triggers, entities without definitions.
2. **Inconsistent business rules** — same rule implemented differently in two places.
3. **Hardcoded values** — thresholds, currencies, provider URLs that should be configurable.
4. **Gaps between code and domain language** — overloaded terms, naming mismatches.
5. **Contradictions** — between existing memories, repo card, and code.
6. **Security / money / data-loss risks** — anything that could break core flows or leak assets.

## Output structure

```markdown
# <Repo> — risks and gaps

## Existing memory summary
...

## Risk register

### CRITICAL: <Risk title>
- **Description:** ...
- **Impact:** ...
- **Code anchor:** `file.py:line`.
- **Recommended action:** ...

### WARNING: ...
### INFO: ...

## Contradictions

| Source A | Source B | Conflict | Proposed resolution |
|---|---|---|---|
| ... | ... | ... | ... |

## Gaps

| Gap | Severity | Details | Recommended action |
|---|---|---|---|
| ... | critical / warning / info | ... | ... |

## Uncertainties and open questions
...
```

## Severity definitions

- `critical` — data loss, security breach, broken core flow, money at risk.
- `warning` — inconsistent behavior, missing validation, maintainability issue.
- `info` — documentation gap, naming mismatch, observed TODO.

## Rules

- Every risk MUST have a code anchor or a reference to a missing anchor.
- Distinguish confirmed risks from inferred gaps.
- Log contradictions between memories using the hierarchy in
  `serena-protocol` (`[ref: #serena-contradictions]`).
- Do not invent risks without evidence.
