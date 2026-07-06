[ref: #bda-risks]

# Subagent prompt: risks, gaps, and contradictions

**Task:** Find risks, gaps, inconsistencies, and contradictions in the
business-domain layer of **one** service. Use the other subagent reports (or
your own reading) to identify what is missing, ambiguous, or wrong.

## What to explore

1. **Missing documentation** — business rules without anchors, processes
   without triggers, entities without definitions.
2. **Inconsistent business rules** — same rule implemented differently in two
   places.
3. **Hardcoded values** — thresholds, currencies, provider URLs that should be
   configurable.
4. **Gaps between code and domain language** — overloaded terms, naming
   mismatches.
5. **Contradictions** — between existing memories, entity card, and code.
6. **Security / money / data-loss risks** — anything that could break core
   flows or leak assets.

## Output structure

```markdown
# <Entity> — risks and gaps

## Scope
...

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
