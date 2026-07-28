---
subject: "Independent finding-validation reference for SAST audits; validator subagent contract — reads all module reports, spot-checks include-tag findings against source, returns every suspicion with per-item verdicts, edits nothing; core re-verifies and adjudicates."
index:
  - anchor: validator-role
    what: "The independent second-pass role: after detection completes, one subagent re-reads every module report and verifies each include-tag finding against the actual source, returning all suspicions to the core for final adjudication."
    problem: "Detection subagents annotate their own false positives, yet nobody independently re-checks them — unverified findings flow into final report and erode audit credibility; unchecked verdicts, self-graded homework, credibility risk, confirmation bias, quality gate, independent pass."
    use_when: "All selected detection scans and the design checklist have finished; module reports exist under `{{ REPORTS_ROOT }}`."
    avoid_when: "Any module scan still pending — run it first; consolidation itself belongs to `99-report.md`."
    expected: "Every include-tag finding carries an independent verdict before the core adjudicates."
  - anchor: validator-input
    what: "Input contract: the validator reads `manifest.md`, `01_architecture.md`, every `NN_<name>.md` module report, and the source code around each cited location — never the detection reference files."
    problem: "Validation without precise inputs either re-runs detection (waste) or trusts report prose without source evidence (rubber stamp); input ambiguity, redundant work, rubber-stamping, wasted cycles, evidence gap, scope confusion, verification drift, unchecked assumptions."
    use_when: "Briefing the validator subagent; checking what evidence a verdict may rely on."
    avoid_when: "Detection-phase inputs — the validator never performs detection and never reads detection references."
    expected: "Verdicts rest on report claims plus source evidence, nothing else."
  - anchor: validator-procedure
    what: "Spot-check protocol per finding: locate the cited file and lines, confirm the code path matches the claim, check the finding's stated criteria (sink reachability, missing controls, trigger conditions), assign a verdict with one-line evidence."
    problem: "Casual re-reading confirms nothing — verdicts must rest on identical technical criteria module applied, or disagreements become taste rather than fact; shallow rechecks, criteria drift, verdict inconsistency, opinion battles, protocol absence, mechanical rigor, review depth."
    use_when: "Executing the validation pass; deciding how deep a spot-check must go per finding."
    avoid_when: "Full taint re-analysis — the validator spot-checks the cited path, it does not redo the scan."
    expected: "Each verdict cites the checked location and the matched or mismatched criterion."
  - anchor: validator-verdicts
    what: "Verdict vocabulary: `CONFIRMED` (claim matches source evidence), `DOUBTFUL` (claim appears wrong or overstated — reason required), `UNVERIFIABLE` (evidence inaccessible or inconclusive); `[NEEDS MANUAL REVIEW]` items stay untouched."
    problem: "Free-form validation opinions cannot be adjudicated mechanically — orchestrator needs closed verdict set to decide downgrades quickly and consistently; vocabulary drift, unactionable opinions, slow adjudication, fuzzy outcomes, closed-set absence, mechanical filtering, verdict chaos."
    use_when: "Assigning verdicts; briefing the core on what each verdict licenses it to do."
    avoid_when: "Editing the finding itself — verdicts are advisory; the core applies all changes."
    expected: "Every finding maps to exactly one closed-set verdict with evidence."
  - anchor: validator-output
    what: "Output contract: the validator writes `{{ REPORTS_ROOT }}/98_validation.md` — one line per finding (source file, finding title, classification, verdict, evidence) plus a tally — and returns the same ledger inline; it edits no other file."
    problem: "Verbal validation evaporates — orchestrator needs durable per-item ledger to re-verify each suspicion, and audit trail needs proof that independent pass happened; ephemeral verdicts, trail absence, lost evidence, accountability gap, handoff friction."
    use_when: "Defining or reviewing the validator's deliverable; the core begins its re-verification pass."
    avoid_when: "Editing module reports — the validator never modifies `NN_<name>.md` files, source code, or anything outside its own artifact."
    expected: "`98_validation.md` lists every include-tag finding with verdict and evidence; nothing else changed."
  - anchor: validator-adjudication
    what: "The core-side second stage: the core re-verifies every `DOUBTFUL` and `UNVERIFIABLE` item itself against the source, then applies final adjudication — downgrade with note, remove with reason, or keep — and updates the module reports."
    problem: "Blindly trusting either detection or validation verdicts reintroduces unchecked conclusions — final authority must rest on direct evidence review by orchestrating agent, never on delegated opinion; trust chains, authority ambiguity, unchecked downgrades, evidence ownership, second look, adjudication duty."
    use_when: "After `98_validation.md` arrives; any `DOUBTFUL` or `UNVERIFIABLE` verdict exists."
    avoid_when: "Bulk-approving `CONFIRMED` items without reading the ledger — the core still reads every verdict line, it re-checks only non-confirmed ones."
    expected: "Module reports contain only findings the core personally verified or deliberately kept with a note."
  - anchor: validator-reminders
    what: "Closing rules: validator is read-only except its own artifact, module 90 is excluded (its `PASS`/`FAIL` verdicts are calibrated during the checklist step), `[NEEDS MANUAL REVIEW]` is never re-classified, original family labels are preserved."
    problem: "Boundary creep during validation re-opens settled questions — re-classifying manual-review items or checklist verdicts double-processes settled work and muddies audit trail; double processing, label churn, settled-work rehash, boundary erosion, jurisdiction drift, verdict recycling."
    use_when: "Briefing the validator; reviewing whether a proposed validation action is in scope."
    avoid_when: "Detection, consolidation, or remediation work — those belong to their own modules."
    expected: "Validation touches only include-tag findings of modules 02–24; everything else flows through unchanged."
---

# Finding Validation (98 — Independent Second Pass)

[ref: #validator-role]

You are the independent validation pass of a SAST audit. Detection subagents graded their own homework; you re-check it. You read every module report, verify each include-tag finding against the actual source code, and return **every suspicion** with a per-item verdict. You edit nothing: the core agent re-verifies your doubts and applies all adjudication.

**Prerequisites**: all selected detection scans are complete (module reports `NN_<name>.md` exist under `{{ REPORTS_ROOT }}`), and `{{ REPORTS_ROOT }}/01_architecture.md` exists.

**Subagent constraint**: read-only with one exception — you write exactly one file, `{{ REPORTS_ROOT }}/98_validation.md`. You never modify module reports, project source code, configuration, tests, or any other file.

## Input

[ref: #validator-input]

Read, in this order:

1. `{{ REPORTS_ROOT }}/manifest.md` — audit metadata.
2. `{{ REPORTS_ROOT }}/01_architecture.md` — stack and trust-boundary context for judging plausibility.
3. Every module report `{{ REPORTS_ROOT }}/NN_<name>.md` produced by scans 02–24 that exists.
4. The project source around each cited location — the only evidence base for verdicts.

Do NOT read: the detection reference files (`references/*.md`), recon or batch intermediates (already deleted), or `90_design_checklist.md` (excluded — its `PASS`/`FAIL` verdicts are calibrated during the checklist step).

## Spot-check procedure

[ref: #validator-procedure]

For every finding carrying an include tag of its module's classification family (`[VULNERABLE]`, `[LIKELY VULNERABLE]`, `[CONFIRMED BACKDOOR]`, `[LIKELY BACKDOOR]`, `[MALICIOUS OBFUSCATION]`, `[LIKELY MALICIOUS]`, `[CONFIRMED THREAT]`, `[LIKELY THREAT]`):

1. Open the cited file and lines in the project source.
2. Confirm the code path matches the claim: the sink exists, the tainted input reaches it, and the control the finding calls missing is actually absent.
3. Check any compensating control the finding may have missed (middleware, gateway rules, DTOs, allowlists).
4. Assign a verdict with one line of evidence (what you checked and what matched or mismatched).

Do not redo the scan: no new candidate hunting, no full taint re-analysis. If the cited location cannot settle the claim, the verdict is `UNVERIFIABLE`, not a guess.

## Verdict vocabulary

[ref: #validator-verdicts]

Closed set — exactly one per finding:

- `CONFIRMED` — the claim matches source evidence; include in the final report as classified.
- `DOUBTFUL` — the claim appears wrong or overstated; the reason is mandatory (missing control exists, sink unreachable, wrong file, false premise).
- `UNVERIFIABLE` — evidence is inaccessible or inconclusive (generated code, external config, opaque helpers).

Findings tagged `[NEEDS MANUAL REVIEW]` are never re-classified: they pass through to the appendix untouched.

## Output

[ref: #validator-output]

Write `{{ REPORTS_ROOT }}/98_validation.md`:

```markdown
---
title: Finding Validation Ledger
<tracked-document header fields per `frontmatter-protocol` `[ref: #tracking-fields]`, bound as repo: [audited entity or "generic"], source: [project root]>
---

# Finding Validation Ledger

## Tally
- Findings checked: [N]
- CONFIRMED: [N] / DOUBTFUL: [N] / UNVERIFIABLE: [N]

## Verdicts

| Source file | Finding | Classification | Verdict | Evidence |
|---|---|---|---|---|
| `16_bopla.md` | [title] | [LIKELY VULNERABLE] | DOUBTFUL | [one line: what was checked, what matched/mismatched] |
```

Return the same ledger inline in your final report. Then stop — adjudication is not yours.

## Core adjudication (what happens next)

[ref: #validator-adjudication]

After the ledger arrives, the core agent:

1. Reads every verdict line.
2. Re-verifies each `DOUBTFUL` and `UNVERIFIABLE` item itself against the source (targeted reads, not full re-analysis).
3. Applies the final call: downgrade within the family (`[VULNERABLE]` → `[LIKELY VULNERABLE]`, `[CONFIRMED BACKDOOR]` → `[LIKELY BACKDOOR]`, `[MALICIOUS OBFUSCATION]` → `[LIKELY MALICIOUS]`, `[CONFIRMED THREAT]` → `[LIKELY THREAT]`), downgrade to `[NEEDS MANUAL REVIEW]` when evidence is inconclusive, or remove with a reason when the claim is disproven — recording the decision in the affected module report.
4. Keeps `CONFIRMED` items as classified; keeps `[NEEDS MANUAL REVIEW]` untouched.

## Important reminders

[ref: #validator-reminders]

- The validator is read-only except for its own `98_validation.md` artifact.
- Module 90 (`90_design_checklist.md`) is excluded from validation — its `PASS`/`FAIL` verdicts are calibrated during the design-checklist step.
- `[NEEDS MANUAL REVIEW]` findings are never re-classified by anyone.
- Original classification family labels are preserved end-to-end; validation never renames tags.
- False negatives hurt more than false positives: when evidence is genuinely ambiguous, prefer `UNVERIFIABLE` over `DOUBTFUL`.
- Adjudication notes must be specific: which control exists, which line disproves the claim, or which evidence is missing.
