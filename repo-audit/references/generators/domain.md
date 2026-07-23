---
subject: "Risks generator subagent prompt; preanalysis reports, business risks, gaps, contradictions, missing documentation, inconsistent rules, hardcoded values, security money data-loss, risk register, severity definitions, code anchors, `preanalysis_reports`, targeted verification, triage calibration."
index:
  - anchor: ra-domain-risks
    what: "The risks-generator prompt: find what is missing, ambiguous, or wrong in the business layer from the analysis-wave reports."
    problem: "Analysis wave reports describe what exists; nobody hunts what breaks business until production incident does it; unhunted risks, production surprises, gap blindness, contradiction drift, risk neglect, incident discovery, hunt absence, exposure buildup."
    use_when: "Launching the generators-wave risks subagent; reviewing risk register completeness."
    avoid_when: "Extraction of entities/processes/rules/integrations — `analysis/domain.md` prompts."
    expected: "Risk register covering missing docs, inconsistencies, hardcoded values, and money/security risks."
  - anchor: ra-domain-risks-inputs
    what: "The risks input contract: `preanalysis_reports` as primary source plus cards and targeted code reads."
    problem: "Risks subagent re-explores codebase from scratch duplicating analysis wave, or judges without evidence; duplicated exploration, evidence-free judgment, input confusion, re-read waste, source blindness, effort doubling, baseless claims, report blindness, verification skip."
    use_when: "Preparing risks subagent launch; deciding what feeds risk analysis."
    avoid_when: "Wholesale code re-exploration — reports are primary; targeted verification reads only."
    expected: "Risk analysis built on all four reports with gap-filling targeted reads."
  - anchor: ra-domain-risks-explore
    what: "The risk hunting grounds: missing documentation, inconsistent rules, hardcoded values, language gaps, contradictions, security/money/data-loss."
    problem: "Risk categories get skimmed; register fills with trivia while money-losing defects hide; skimming, trivia flood, concealed defects, category blindness, hunt shallowness, priority inversion, surface scratching, criticality fog, focus loss, coverage debt."
    use_when: "Hunting risks in reports and code; prioritizing what to flag; classifying findings."
    avoid_when: "Inventing risks without evidence — every entry anchors per the rules section."
    expected: "All six hunting grounds covered with evidence-anchored findings."
  - anchor: ra-domain-risks-output
    what: "The risks output structure: risk register, contradictions table, gaps table, uncertainties."
    problem: "Risks return as shapeless narrative; root cannot route them into business report or findings; unroutable findings, register absence, format chaos, synthesis friction, routing failure, structure vacuum, consumption stall, assembly stall, table absence."
    use_when: "Formatting the risks report; root consuming the register."
    avoid_when: "Severity semantics — defined in the sibling severity section."
    expected: "Structured register with contradictions and gaps tables."
  - anchor: ra-domain-risks-severity
    what: "The severity definitions: critical (data loss, security, money), warning (inconsistency, maintainability), info (docs, naming)."
    problem: "Every finding lands as critical or everything reads as info; triage impossible and money risks sink in noise; severity inflation, triage failure, calibration absence, priority noise, signal burial, ranking chaos, attention misallocation, triage collapse."
    use_when: "Assigning severity to any finding; calibrating the register; root routing findings to memory."
    avoid_when: "Domain-specific impact analysis — that is the register's own content."
    expected: "Severity calibrated consistently across all findings."
  - anchor: ra-domain-risks-rules
    what: "The risks evidence rules: anchors mandatory, confirmed vs inferred distinction, contradiction logging, no invention."
    problem: "Register fills with speculation lacking anchors; user cannot tell confirmed defects from guesses; speculation flood, anchor absence, confirmation fog, evidence-free entries, guess pollution, trust decay, invention spiral, fabrication risk, entry inflation, proof void."
    use_when: "Writing any risk entry; reviewing register quality; logging memory contradictions."
    avoid_when: "Contradiction protocol details — `serena-protocol` `[ref: #serena-contradictions]` owns them."
    expected: "Every entry anchored, typed as confirmed or inferred, zero inventions."
---

# Subagent prompt: risks, gaps, and contradictions

[ref: #ra-domain-risks]

**Task:** Find risks, gaps, inconsistencies, and contradictions in the
business-domain layer of **one** service. You receive `preanalysis_reports` —
the reports of the analysis-wave subagents (entities, processes, rules,
integrations). You MUST base your risk analysis on them to identify what is
missing, ambiguous, or wrong, and read the code directly only in a targeted
way where evidence is missing.

## Required inputs (MUST read)

[ref: #ra-domain-risks-inputs]

- `preanalysis_reports` — your primary source (all four analysis-wave reports).
- `repos/<repo>/overview`, `project/glossary`, `repos/<repo>/glossary`.
- Existing `repos/<repo>/business.md` and split files (if present).
- Targeted code reads ONLY to verify or fill gaps left by the reports.

## What to explore

[ref: #ra-domain-risks-explore]

1. **Missing documentation** — business rules without anchors, processes without triggers, entities without definitions.
2. **Inconsistent business rules** — same rule implemented differently in two places.
3. **Hardcoded values** — thresholds, currencies, provider URLs that should be configurable.
4. **Gaps between code and domain language** — overloaded terms, naming mismatches.
5. **Contradictions** — between existing memories, repo card, and code.
6. **Security / money / data-loss risks** — anything that could break core flows or leak assets.

## Output structure

[ref: #ra-domain-risks-output]

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

[ref: #ra-domain-risks-severity]

- `critical` — data loss, security breach, broken core flow, money at risk.
- `warning` — inconsistent behavior, missing validation, maintainability issue.
- `info` — documentation gap, naming mismatch, observed TODO.

## Rules

[ref: #ra-domain-risks-rules]

- Every risk MUST have a code anchor or a reference to a missing anchor.
- Distinguish confirmed risks from inferred gaps.
- Log contradictions between memories using the hierarchy in
  `serena-protocol` (`[ref: #serena-contradictions]`).
- Do not invent risks without evidence.
