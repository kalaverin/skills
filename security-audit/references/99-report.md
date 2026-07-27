---
subject: "Final security report consolidation reference; single write target `{{ REPORTS_ROOT }}/report.md` with read-only scope constraint, per-module-family include/exclude classification tags `[VULNERABLE]`/`[CONFIRMED BACKDOOR]`/`[MALICIOUS OBFUSCATION]`/`[CONFIRMED THREAT]`, severity baseline table with confidentiality tiebreaker, six-step execution incl. dedup cross-references scoring completeness checklist, fenced output template with OWASP heatmap plus appendices, operational reminders."
index:
  - anchor: final-report
    what: "Final-report consolidation role merging every completed scan result (`02_sqli.md` through `24_jvm_anomalies.md` plus `90_design_checklist.md`) into one prioritized deliverable at `{{ REPORTS_ROOT }}/report.md` — gated on at least one finished module report."
    problem: "Dozens of module scan outputs sit scattered across `{{ REPORTS_ROOT }}` with mixed tag families, overlapping flaws, and no unified ranking, so stakeholders cannot grasp overall risk posture or remediation order; decision support, audit closure, risk visibility, triage basis, wrap-up synthesis, executive readout, portfolio view."
    use_when: "Every selected scan finished; at least one scan artifact present; final stakeholder-facing deliverable must be produced; `manifest.md` found in `{{ REPORTS_ROOT }}`."
    avoid_when: "Scan selection still open — `00-screener.md` owns it; recon or architecture context missing — `01-analysis.md` first; detection itself unfinished — module files 02–24 and `90-design-checklist.md` run first."
    expected: "One prioritized `{{ REPORTS_ROOT }}/report.md` produced, spanning every result file; nothing else written."
  - anchor: report-subagent-constraints
    what: "Write-scope confinement rule for the report subagent: only `{{ REPORTS_ROOT }}/report.md` may be written; everything outside `{{ REPORTS_ROOT }}` stays untouched."
    problem: "Consolidation agent with broad repo access may drift into editing production code, config files, tests, or build scripts while composing findings, corrupting audit integrity and leaving unauthorized modifications; read-only posture, side-effect containment, blast radius, scope discipline, stray writes, tamper risk, guardrail."
    use_when: "Briefing the consolidation subagent before dispatch; writing its constraint block; reviewing whether any file outside `{{ REPORTS_ROOT }}` was touched."
    avoid_when: "Detection-stage subagent limits are the topic — module files 02–24 carry their own rules; scan selection belongs to `00-screener.md`; recon belongs to `01-analysis.md`."
    expected: "Subagent writes exactly one file under `{{ REPORTS_ROOT }}` and leaves project tree unmodified."
  - anchor: report-what-to-include
    what: "Per-module-family inclusion and exclusion tag rules: standard family (modules 02–20, 24) takes `[VULNERABLE]` and `[LIKELY VULNERABLE]`, module 21 takes `[CONFIRMED BACKDOOR]`/`[LIKELY BACKDOOR]`, module 22 takes `[MALICIOUS OBFUSCATION]`/`[LIKELY MALICIOUS]`, module 23 takes `[CONFIRMED THREAT]`/`[LIKELY THREAT]`, while `[NOT VULNERABLE]`, `[SUSPICIOUS BUT LEGITIMATE]`, `[LEGITIMATE OBFUSCATION]`, `[LOW RISK]`, and `[NEEDS MANUAL REVIEW]` stay out of headline findings yet still count toward summary tallies."
    problem: "Mixed classification vocabularies across module families make naive merging pull benign, legitimate, or manual-review entries into confirmed findings, inflating totals and burying real threats; inclusion filter, exclusion set, tag canon, verdict hygiene, noise rejection, tally accuracy, count integrity."
    use_when: "Deciding which entries from each result file enter the final Findings section; routing `[NEEDS MANUAL REVIEW]` items toward the appendix; reconciling tallies with exclusions."
    avoid_when: "`FAIL` item handling from the design checklist belongs to its dedicated section under execution; original classification inside one scan belongs to module files 02–24; design-gap assessment belongs to `90-design-checklist.md`."
    expected: "Only family-appropriate confirmed and likely entries reach the main body; excluded tags appear solely as summary counts and appendix rows."
  - anchor: report-severity-ranking
    what: "Baseline severity table assigning Critical/High/Medium/Low per vulnerability class — RCE, SSTI, auth-endpoint SQLi, JWT algorithm confusion, webshell upload, hardcoded secrets, confirmed backdoors, and JVM deserialization/JNDI as Critical; SSRF reaching internal services, sensitive path traversal, stored XSS, BOPLA, resource consumption, misconfiguration as High; reflected XSS, business-logic flaws, inventory gaps as Medium — plus OWASP API 2023 default-risk alignment and confidentiality-impact tiebreaker."
    problem: "Findings arrive without comparable urgency labels, and flat or gut-feel scoring lets low-impact noise outrank credential exposure while equal-baseline items lack any ordering principle; severity canon, tier assignment, context adjustment, tiebreak rule, ranking fairness, triage signal, impact weighting."
    use_when: "Assigning tiers to confirmed findings during scoring; breaking same-tier deadlocks via sensitive-data weight; aligning verdicts with default risk ratings."
    avoid_when: "Module-level verdict tagging belongs to module files 02–24; design-gap `FAIL` severities follow the Low/Medium rule inside the output template; scan selection belongs to `00-screener.md`."
    expected: "Every finding carries one justified tier; tied items ordered consistently; list sorted Critical-first."
  - anchor: report-execution
    what: "Six-step in-session execution with no subagents: discover module outputs plus `manifest.md` and `01_architecture.md` context, extract per-family findings, deduplicate by file path/endpoint/sink keeping highest severity with `Cross-references` field, score and sort Critical-first by confidentiality, run completeness checklist against `00_plan.md`, then write the mandated fenced template — header, executive-summary severity counts, OWASP API 2023 coverage heatmap, top-three risk scores, remediation SLA timeline, vulnerability index, tiered finding blocks, design-gap section, scan-coverage and manual-review appendices."
    problem: "Consolidation attempted ad hoc skips result files, double-counts shared vulnerable locations, orders tiers inconsistently, and ships deliverables whose summary tallies disagree with detail rows or omit required appendices; workflow canon, step sequence, evidence gathering, cross-scan overlap, coverage audit, template fidelity, structural completeness."
    use_when: "Running the consolidation end to end after module scans complete; grouping same-location findings before scoring; validating deliverable completeness against the plan; writing or reviewing `{{ REPORTS_ROOT }}/report.md` structure."
    avoid_when: "Any module scan still pending — finish module files 02–24 or `90-design-checklist.md` first; scan selection belongs to `00-screener.md`; recon and architecture work belong to `01-analysis.md`; classification-tag rules alone wanted — see the inclusion card."
    expected: "`{{ REPORTS_ROOT }}/report.md` written with header metadata, heatmap, tiered findings, dedup cross-references, and both appendices present; checklist items all verified."
  - anchor: report-important-reminders
    what: "Closing operational reminders: family-correct tag enforcement with ⚠ likely markers preserved per family, original labels kept for modules 21–23 rather than re-labeled, full detail preservation without truncating Proof/Remediation/Dynamic Test, `manifest.md` header reflection, `01_architecture.md`-enriched severity rationale, empty-tier section omission, single-file write confinement, post-write memory persistence via `[ref: #serena-memory-mutation]`."
    problem: "Final pass without fixed wrap-up rules lets likely-verdict markers vanish, module-specific labels get flattened into generic tags, proof details get truncated, or stray writes touch project files; closing rules, quality floor, marker hygiene, exit discipline, audit closure, scope restraint, uniform endings."
    use_when: "Finalizing the consolidated deliverable; verifying tag fidelity and marker placement; confirming header metadata and rationale enrichment are applied."
    avoid_when: "Earlier consolidation steps still open — finish extraction, dedup, and scoring first; detection work belongs to module files 02–24; design-gap assessment belongs to `90-design-checklist.md`; scan selection belongs to `00-screener.md`."
    expected: "Deliverable closes with ⚠ markers attached, family labels intact, untruncated evidence, and nothing beyond the report file touched."
---

# Final Security Report Generation

[ref: #final-report]

You are consolidating all completed SAST vulnerability scan results into a single prioritized security report.

**Prerequisites**: At least one final module report (e.g., `{{ REPORTS_ROOT }}/02_sqli.md`) must exist in `{{ REPORTS_ROOT }}`. Run the vulnerability detection skills first if none exist.

## Subagent Constraints
[ref: #report-subagent-constraints]

The report subagent must **only** write `{{ REPORTS_ROOT }}/report.md`. It must **never** edit project source code, configuration files, tests, build scripts, or any file outside `{{ REPORTS_ROOT }}`.

***

## What to Include
[ref: #report-what-to-include]

Only include findings with the include tags of each result file's module family:
- Modules 02–20 and 24 (standard family): `[VULNERABLE]` and `[LIKELY VULNERABLE]`
- Module 21 (backdoors): `[CONFIRMED BACKDOOR]` and `[LIKELY BACKDOOR]`
- Module 22 (obfuscation): `[MALICIOUS OBFUSCATION]` and `[LIKELY MALICIOUS]`
- Module 23 (dependencies): `[CONFIRMED THREAT]` and `[LIKELY THREAT]`

Exclude the excluded tags of each family — `[NOT VULNERABLE]`, `[SUSPICIOUS BUT LEGITIMATE]`, `[LEGITIMATE OBFUSCATION]`, and `[LOW RISK]` — together with `[NEEDS MANUAL REVIEW]` from the main report body. Count them in the summary, and list `[NEEDS MANUAL REVIEW]` items in the dedicated appendix (see output template).

***

## Severity Ranking
[ref: #report-severity-ranking]

Assign each finding a severity tier — **Critical**, **High**, **Medium**, or **Low** — using the table below as your baseline. Adjust up or down based on context (e.g., an IDOR that exposes financial records is High, not Medium).

| Vulnerability Class | Default Severity |
|---------------------|------------------|
| RCE via command injection, eval, or unsafe deserialization | Critical |
| SSTI (Server-Side Template Injection) | Critical |
| SQLi on authentication endpoints | Critical |
| JWT algorithm confusion (alg:none, RS256→HS256) | Critical |
| File upload leading to code execution (webshell) | Critical |
| Hardcoded secrets in source or client-side code (credentials, tokens, API keys) | Critical |
| Confirmed backdoor or implant | Critical |
| JVM anomalies (unsafe deserialization, JNDI injection, unsigned ClassLoader) | Critical |
| SQLi with full data extraction capability | High–Critical |
| GraphQL injection (user-controlled operation document enabling unauthorized fields or gateway abuse) | High–Critical |
| XXE with file read or internal SSRF | High–Critical |
| Missing authentication on sensitive endpoints | High–Critical |
| Malicious obfuscation hiding payloads or C2 | High–Critical |
| Confirmed supply-chain threat (compromised/typosquatted dependency in runtime path) | High–Critical |
| SSRF reaching internal services or cloud metadata | High |
| Path traversal reading sensitive or config files | High |
| File upload with stored content accessible to others | High |
| IDOR on PII, financial, or health data | High |
| XSS (stored/persistent) | High |
| Broken Object Property Level Authorization (BOPLA / excessive data exposure / mass assignment) | High |
| Unrestricted resource consumption (DoS, cost abuse, missing rate limits) | High |
| Security misconfiguration (debug endpoints, default credentials, verbose errors, unsafe headers) | High |
| Unsafe consumption of APIs (blind trust of third-party data or responses) | High |
| Other JVM anomalies (reflection, scripting, RMI/JMX exposure) | High |
| JWT with missing or bypassable claim validation | Medium–High |
| Missing authentication on lower-sensitivity endpoints | Medium |
| IDOR on non-sensitive data | Medium |
| XSS (reflected or DOM) | Medium |
| Business logic flaws (price manipulation, workflow bypass) | Medium |
| Improper inventory management (shadow/deprecated endpoints, missing docs) | Medium |
| Information disclosure of non-sensitive data | Low |

**OWASP API 2023 alignment**: The defaults above map to OWASP API Security Top 10 2023 risk ratings — API2 and API5 default to **Critical**; API1, API3, API4, API7, API8, and API10 default to **High**; API6 and API9 default to **Medium**. Hardcoded secrets are treated as severe credential exposure and default to **Critical**. Modules 21–23 (backdoors, obfuscation, dependencies) map to API8:2023 and/or API10:2023, judged per finding; module 24 (JVM anomalies) maps to API5:2023, API8:2023, and/or API10:2023.

**Confidentiality as a tiebreaker**: When two findings share the same baseline severity, rank higher the one with greater confidentiality impact — i.e., the greater its potential to expose sensitive user data, credentials, or system internals.

***

## Execution
[ref: #report-execution]

Perform all steps in-session (no subagents needed).

### Step 1: Discover result files and context

1. Read `{{ REPORTS_ROOT }}/manifest.md`. Use the `entity` field (`project-level` or a specific entity name) in the report header.
2. Read `{{ REPORTS_ROOT }}/01_architecture.md` if it exists (use it for the project name, application context, and severity rationale).
3. Check which of these files exist in `{{ REPORTS_ROOT }}/`:
   - `02_sqli.md`
   - `03_ssrf.md`
   - `04_xss.md`
   - `05_rce.md`
   - `06_ssti.md`
   - `07_xxe.md`
   - `08_idor.md`
   - `09_jwt.md`
   - `10_missingauth.md`
   - `11_fileupload.md`
   - `12_pathtraversal.md`
   - `13_businesslogic.md`
   - `14_graphql.md`
   - `15_hardcodedsecrets.md`
   - `16_bopla.md`
   - `17_resourceconsumption.md`
   - `18_inventory.md`
   - `19_unsafeapiconsumption.md`
   - `20_misconfiguration.md`
   - `21_backdoors.md`
   - `22_obfuscation.md`
   - `23_dependencies.md`
   - `24_jvm_anomalies.md`
   - `90_design_checklist.md`

### Step 2: Read and extract findings

Read each existing result file. For every finding classified with an include tag from the file's tag family — `[VULNERABLE]`/`[LIKELY VULNERABLE]` (modules 02–20 and 24), `[CONFIRMED BACKDOOR]`/`[LIKELY BACKDOOR]` (`21_backdoors.md`), `[MALICIOUS OBFUSCATION]`/`[LIKELY MALICIOUS]` (`22_obfuscation.md`), `[CONFIRMED THREAT]`/`[LIKELY THREAT]` (`23_dependencies.md`) — extract:
- Finding title
- Vulnerability type (derived from the source file)
- OWASP API 2023 risk mapping (e.g., API1:2023 Broken Object Level Authorization)
- File / endpoint affected
- Issue description
- Impact description
- Proof / code path
- Remediation
- Dynamic test steps (if present)

For `90_design_checklist.md`, extract every `FAIL` item instead of `[VULNERABLE]`/`[LIKELY VULNERABLE]`. Capture:
- Finding title (from the checklist item)
- Checklist item reference
- Risk
- Evidence
- Remediation

Skip `PASS`, `NOT_APPLICABLE`, and `NEEDS_MANUAL_REVIEW` entries in the main report body, but count `NEEDS_MANUAL_REVIEW` in the summary.

### Step 3: Deduplicate and cross-reference

A single vulnerable location can appear in multiple scan reports (e.g., an IDOR object-access flaw that also enables a sensitive-business-flow bypass). Before scoring:

1. Group findings by file path, endpoint, and vulnerable code location / sink.
2. For each group, keep the highest severity among the contributing findings.
3. Use the OWASP API 2023 risk from the highest-severity contributor as the primary risk.
4. In the finding block, add a **Cross-references** field listing the other contributing scans and their OWASP risk mappings.
5. Preserve all distinct proof-of-concept payloads and remediation actions as sub-bullets under **Proof** and **Remediation**.

If a finding is unique, omit the **Cross-references** field.

### Step 4: Score and sort

Assign each finding a severity level (Critical / High / Medium / Low) using the table above. Sort all findings:

1. Critical first, then High, Medium, Low
2. Within each tier, sort by confidentiality impact (highest first)

### Step 5: Completeness validation checklist

Before finalizing `{{ REPORTS_ROOT }}/report.md`, verify:

- [ ] All scans selected in `{{ REPORTS_ROOT }}/00_plan.md` are represented in the report.
- [ ] Scans 15–24 and `90_design_checklist.md` are included if selected in the plan.
- [ ] Every finding uses its module's classification tags (backdoor, obfuscation, and threat tag families for modules 21–23).
- [ ] Every `[VULNERABLE]` and `[LIKELY VULNERABLE]` finding has a severity, OWASP risk, location, proof, and remediation.
- [ ] `[NEEDS MANUAL REVIEW]` items are listed in the appendix with location and justification.
- [ ] Duplicate findings are deduplicated with cross-references.
- [ ] `manifest.md` metadata is reflected in the report header.
- [ ] Only `{{ REPORTS_ROOT }}/report.md` is written; no project source files were modified.

### Step 6: Write `{{ REPORTS_ROOT }}/report.md`

Use exactly this output format:

***

```markdown
# Security Assessment Final Report

**Entity / Project**: [value from `manifest.md` `entity` field, or name from `01_architecture.md`, or infer from codebase]
**Generated**: [current date UTC ISO 8601]
**Scans completed**: [comma-separated list of scan types that had result files]
**Audit target**: [project-level or specific entity name from `manifest.md`]

---

## Executive Summary

| Severity | Count |
|----------|-------|
| Critical | N |
| High     | N |
| Medium   | N |
| Low      | N |
| **Total confirmed findings** | **N** |

Scans with no confirmed vulnerabilities: [list]
Findings requiring manual review: N ([see appendix](#appendix-findings-requiring-manual-review))
Design & operational control gaps: N (from `90_design_checklist.md`)

### OWASP API 2023 Coverage Heatmap

| OWASP API 2023 Risk | Applicable Scan Files | Status | Finding Count |
|---|---|---|---|
| API1:2023 Broken Object Level Authorization | `08_idor.md` | Scanned / Not selected / No findings | N |
| API2:2023 Broken Authentication | `09_jwt.md`, `10_missingauth.md` | ... | N |
| API3:2023 Broken Object Property Level Authorization | `16_bopla.md` | ... | N |
| API4:2023 Unrestricted Resource Consumption | `17_resourceconsumption.md` | ... | N |
| API5:2023 Broken Function Level Authorization | `10_missingauth.md`, `24_jvm_anomalies.md` | ... | N |
| API6:2023 Unrestricted Access to Sensitive Business Flows | `13_businesslogic.md` | ... | N |
| API7:2023 Server Side Request Forgery | `03_ssrf.md` | ... | N |
| API8:2023 Security Misconfiguration | `20_misconfiguration.md`, `15_hardcodedsecrets.md`, `21_backdoors.md`, `22_obfuscation.md`, `23_dependencies.md`, `24_jvm_anomalies.md` | ... | N |
| API9:2023 Improper Inventory Management | `18_inventory.md` | ... | N |
| API10:2023 Unsafe Consumption of APIs | `19_unsafeapiconsumption.md`, `21_backdoors.md`, `22_obfuscation.md`, `23_dependencies.md`, `24_jvm_anomalies.md` | ... | N |

### Top Risks

Rank the top three OWASP API 2023 risks by combined severity score (Critical=4, High=3, Medium=2, Low=1). For each, list the risk, its score, and a one-line rationale based on the findings.

1. **[Risk] — Score: N** — [rationale]
2. **[Risk] — Score: N** — [rationale]
3. **[Risk] — Score: N** — [rationale]

### Recommended Remediation Timeline

| Severity | Recommended SLA | Rationale |
|---|---|---|
| Critical | 24–72 hours | Severe technical impact, easy exploitation, common/widespread prevalence (e.g., API2, API5, hardcoded credentials). |
| High | 1–2 weeks | Moderate-to-severe impact, easy exploitation (e.g., API1, API3, API4, API7, API8, API10). |
| Medium | 2–4 weeks | Business-harm flows or inventory gaps with average detectability (e.g., API6, API9). |
| Low | 30–90 days | Best-practice gaps with limited immediate exploitability. |

---

## Vulnerability Index

| # | Title | Type | Severity | Endpoint / File |
|---|-------|------|----------|----------------|
| 1 | ... | RCE | Critical | `POST /api/exec` |
| 2 | ... | SQLi | High | `GET /api/users` |

---

## Findings

### Critical

#### [Finding Title] — [Vuln Type] ⚠ Likely Vulnerable

- **Source scan**: `{{ REPORTS_ROOT }}/N_NAME.md` (e.g., `02_sqli.md`)
- **Classification**: Vulnerable *(or "Likely Vulnerable")*
- **Endpoint / File**: ...
- **Risk rating**: [OWASP API 2023 risk, e.g., API1:2023 Broken Object Level Authorization]
- **Severity rationale**: [1–2 sentences explaining why this is Critical, with focus on confidentiality and integrity impact]
- **Issue**: ...
- **Impact**: ...
- **Proof**:
  ```
  [code path or evidence from original finding]
  ```
- **Remediation**: ...
- **Dynamic Test**:
  ```
  [curl command or step-by-step test instructions from original finding]
  ```
- **Cross-references**: [only when deduplicated — list other contributing scans and their OWASP risk mappings]

---

### High

[Same structure as Critical section]

---

### Medium

[Same structure]

---

### Low

[Same structure]

---

## Design & Operational Control Gaps

List each `FAIL` finding from `{{ REPORTS_ROOT }}/90_design_checklist.md` in this
section. Assign a severity of **Low** or **Medium** based on the described risk;
default to **Low** unless the missing control could directly enable
authentication bypass, data exposure, or service compromise.

#### [Finding Title] — Design Gap

- **Source scan**: `{{ REPORTS_ROOT }}/90_design_checklist.md`
- **Checklist item**: [section and item number]
- **Risk**: ...
- **Evidence**: ...
- **Remediation**: ...

[Repeat for each FAIL]

---

## Appendix: Scan Coverage

| Scan | Result File | Status |
|------|-------------|--------|
| SQLi | `{{ REPORTS_ROOT }}/02_sqli.md` | Completed / Not run |
| SSRF | `{{ REPORTS_ROOT }}/03_ssrf.md` | Completed / Not run |
| XSS | `{{ REPORTS_ROOT }}/04_xss.md` | Completed / Not run |
| RCE | `{{ REPORTS_ROOT }}/05_rce.md` | Completed / Not run |
| SSTI | `{{ REPORTS_ROOT }}/06_ssti.md` | Completed / Not run |
| XXE | `{{ REPORTS_ROOT }}/07_xxe.md` | Completed / Not run |
| IDOR | `{{ REPORTS_ROOT }}/08_idor.md` | Completed / Not run |
| JWT | `{{ REPORTS_ROOT }}/09_jwt.md` | Completed / Not run |
| Missing Auth | `{{ REPORTS_ROOT }}/10_missingauth.md` | Completed / Not run |
| File Upload | `{{ REPORTS_ROOT }}/11_fileupload.md` | Completed / Not run |
| Path Traversal | `{{ REPORTS_ROOT }}/12_pathtraversal.md` | Completed / Not run |
| Business Logic | `{{ REPORTS_ROOT }}/13_businesslogic.md` | Completed / Not run |
| GraphQL injection | `{{ REPORTS_ROOT }}/14_graphql.md` | Completed / Not run |
| Hardcoded Secrets | `{{ REPORTS_ROOT }}/15_hardcodedsecrets.md` | Completed / Not run |
| BOPLA | `{{ REPORTS_ROOT }}/16_bopla.md` | Completed / Not run |
| Resource Consumption | `{{ REPORTS_ROOT }}/17_resourceconsumption.md` | Completed / Not run |
| Inventory | `{{ REPORTS_ROOT }}/18_inventory.md` | Completed / Not run |
| Unsafe API Consumption | `{{ REPORTS_ROOT }}/19_unsafeapiconsumption.md` | Completed / Not run |
| Misconfiguration | `{{ REPORTS_ROOT }}/20_misconfiguration.md` | Completed / Not run |
| Backdoors | `{{ REPORTS_ROOT }}/21_backdoors.md` | Completed / Not run |
| Obfuscation | `{{ REPORTS_ROOT }}/22_obfuscation.md` | Completed / Not run |
| Dependencies | `{{ REPORTS_ROOT }}/23_dependencies.md` | Completed / Not run |
| JVM Anomalies | `{{ REPORTS_ROOT }}/24_jvm_anomalies.md` | Completed / Not run |
| Design checklist | `{{ REPORTS_ROOT }}/90_design_checklist.md` | Completed / Not run |

## Appendix: Findings Requiring Manual Review

For every `[NEEDS MANUAL REVIEW]` item in any result file, include:

| # | Title | File / Endpoint | Source Scan | Justification |
|---|-------|-----------------|-------------|---------------|
| 1 | ... | ... | `15_hardcodedsecrets.md` | [why it could not be automatically classified] |
```

***

## Important Reminders
[ref: #report-important-reminders]

- Include ONLY findings with their module family's include tags in the Findings section — `[VULNERABLE]`/`[LIKELY VULNERABLE]` (modules 02–20 and 24), `[CONFIRMED BACKDOOR]`/`[LIKELY BACKDOOR]` (21), `[MALICIOUS OBFUSCATION]`/`[LIKELY MALICIOUS]` (22), `[CONFIRMED THREAT]`/`[LIKELY THREAT]` (23); `FAIL` items from `90_design_checklist.md` go in the Design & Operational Control Gaps section.
- Mark the family-appropriate "likely" findings clearly: append **⚠ Likely Vulnerable** (or the family's likely label) after the finding title.
- Findings from modules 21–23 keep their original classification labels in the report — a `[CONFIRMED BACKDOOR]` is reported as such, not re-labeled `[VULNERABLE]`; the ⚠ marker applies to the family-appropriate "likely" tag (`[LIKELY VULNERABLE]`, `[LIKELY BACKDOOR]`, `[LIKELY MALICIOUS]`, `[LIKELY THREAT]`).
- Preserve all details from the original findings — do not summarize or truncate Proof, Remediation, or Dynamic Test sections.
- Read `{{ REPORTS_ROOT }}/manifest.md` first and reflect the entity name / `project-level` flag in the report header.
- If `{{ REPORTS_ROOT }}/01_architecture.md` exists, use it to enrich the severity rationale with application-specific context (e.g., "this endpoint handles payment data, making confidentiality impact Critical").
- Omit severity sections entirely (e.g., the `### Low` heading) if no findings fall in that tier.
- This subagent must only write `{{ REPORTS_ROOT }}/report.md` and must not modify any project source code or configuration.
- After `{{ REPORTS_ROOT }}/report.md` is written, the ROOT agent persists per `serena-protocol` `[ref: #serena-memory-mutation]` so the audit artifacts are persisted with the rest of Serena memory.
