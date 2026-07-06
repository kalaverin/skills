[ref: #bda-rules]

# Subagent prompt: business rules and invariants

**Task:** Extract and document the business rules, invariants, validation
logic, authorization checks, and calculation logic for **one** service. Do not
explore processes or integrations in depth; focus on the rules themselves.

## What to explore

1. **Validation functions** — `validate_*`, `check_*`, `ensure_*`, `can_*`.
2. **Invariants** — conditions that must always hold for an entity or process.
3. **Authorization rules** — role/permission checks, actor-specific guards.
4. **Calculation logic** — pricing, fees, limits, thresholds, currency
   conversions.
5. **Configuration constants** — thresholds, currencies, blockchains, time
   windows that drive behavior.

## Output structure

```markdown
# <Entity> — business rules

## Scope
...

## Existing memory summary
...

## Rule catalog

### R1: <Concise rule statement>
- **Type:** validation / invariant / authorization / calculation.
- **Enforcement:** `path/file.py:line` (`symbol_name`).
- **Violation consequence:** what happens when the rule is broken.
- **Related entities:** `EntityA`, `EntityB`.
- **Hardcoded values:** thresholds, currencies, time windows (if any).
- **Notes:** edge cases or inconsistencies.

### R2: ...

## Invariants summary

| Invariant | Entity/Process | Enforcement location | Code anchor |
|---|---|---|---|
| ... | ... | ... | ... |

## Authorization rules

| Rule | Actor | Condition | Code anchor |
|---|---|---|---|
| ... | ... | ... | ... |

## Calculation rules

| Rule | Formula / Logic | Code anchor |
|---|---|---|
| ... | ... | ... |

## Uncertainties and open questions
...
```

## Rules

- Every rule MUST have an enforcement location.
- State hardcoded values explicitly; do not hide them in prose.
- Distinguish validation (input rejected) from invariant (state illegal).
- Include edge cases and contradictions if the same rule appears in multiple
  places.
