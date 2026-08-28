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
    what: "Two-stage map-reduce consolidation: parallel extractor subagents normalize each module report into compact `NN_findings.yaml` cards, then one consolidator dedups by location keeping highest severity with `Cross-references`, scores and sorts Critical-first by confidentiality, validates completeness against `00_plan.md`, writes the mandated fenced template — header, severity counts, OWASP heatmap, top-three risks, SLA timeline, vulnerability index, tiered findings, design gaps, both appendices — and deletes the cards."
    problem: "Single-context consolidation forces one agent to ingest every module report verbatim with no truncation allowed, while ad hoc merging skips files, double-counts shared locations, and breaks tally consistency; context ceiling, workflow canon, evidence gathering, cross-scan overlap, coverage audit, template fidelity, staged extraction."
    use_when: "Running consolidation after all module scans complete; grouping same-location findings before scoring; validating completeness against the plan; writing or reviewing `{{ REPORTS_ROOT }}/report.md` structure."
    avoid_when: "Any module scan still pending — finish module files 02–24 or `90-design-checklist.md` first; scan selection belongs to `00-screener.md`; recon and architecture work belong to `01-analysis.md`; classification-tag rules alone wanted — see the inclusion card."
    expected: "`{{ REPORTS_ROOT }}/report.md` written with header metadata, heatmap, tiered findings, dedup cross-references, and both appendices present; no `NN_findings.yaml` left behind."
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

The report subagent writes only `{{ REPORTS_ROOT }}/report.md` and deletes the `NN_findings.yaml` cards after the report is written. It must **never** edit project source code, configuration files, tests, build scripts, or any file outside `{{ REPORTS_ROOT }}`.

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

Consolidation runs in two map-reduce stages — no single context ever reads every module report at once.

### Stage 1: Extract finding cards (parallel subagents)

For each existing module report (`NN_<name>.md` for scans 02–24, and `90_design_checklist.md`), dispatch one `coder` subagent with: this reference file's path, that module report's path, and `{{ REPORTS_ROOT }}`. It writes `{{ REPORTS_ROOT }}/NN_findings.yaml`:

- For scans 02–24: one card per finding carrying an include tag of the module's classification family (see What to Include). Excluded tags are skipped; `[NEEDS MANUAL REVIEW]` items go to a separate `manual_review:` list.
- For module 90: one card per `FAIL` item; `NEEDS_MANUAL_REVIEW` items go to `manual_review:`.

Card format (one YAML list item per finding):

```yaml
- id: "16-3"                      # scan id + finding number in source order
  source_scan: "16_bopla"
  classification: "[LIKELY VULNERABLE]"
  title: "Booking PATCH accepts total_stay_price"
  owasp_risk: "API3:2023 Broken Object Property Level Authorization"
  location: "api/bookings.py:88-104"
  endpoint: "PATCH /api/bookings/{id}"
  dedup_key: "api/bookings.py::BookingViewSet.partial_update"
  severity_hint: "High"           # per the Severity Ranking baseline
  summary: "Update serializer accepts any writable model field; price overwrite confirmed."
  evidence_ref: "16_bopla.md: finding block 3"
manual_review:
  - title: "..."
    location: "..."
    justification: "..."
```

The extractor never re-analyzes code and never re-judges verdicts: it normalizes the module report's own text into cards.

Extraction rules:

- The extractor ALWAYS writes `NN_findings.yaml`, even with zero include-tag findings: an empty findings list plus `scanned: true` and the module id — a clean scan must stay distinguishable from a not-run scan.
- For module 90: `classification: FAIL`, `endpoint: null`, `owasp_risk` from the checklist's own OWASP alignment table, no `severity_hint` (the consolidator assigns Low/Medium to design gaps), no `dedup_key` (design gaps never participate in dedup), and the card carries the `PASS`/`FAIL`/`NOT_APPLICABLE`/`NEEDS_MANUAL_REVIEW` tallies for the Design & Operational Control Gaps section header.
- If a finding block lacks an OWASP risk, the extractor falls back to the module's registry-row mapping in `references/registry.md`.

### Stage 2: Consolidate (one subagent)

Dispatch one `coder` subagent with this reference file's path and `{{ REPORTS_ROOT }}`. It:

1. Reads `manifest.md`, `01_architecture.md` (context for severity rationale), and every `NN_findings.yaml` — never the module reports at this step. Cards cross-referenced against `00_plan.md` determine each scan's coverage status: `Scanned` (ran with at least one surviving finding) / `No findings` / `Not selected`.
2. **Deduplicates** by `dedup_key` (plus file/endpoint/sink equivalence): groups cards, keeps the highest severity per group, takes the OWASP risk of the highest-severity contributor as primary, and records the other contributors in a **Cross-references** field; distinct PoC payloads and remediations are preserved as sub-bullets. Unique findings omit the field.
3. **Scores and sorts** per the Severity Ranking table: baseline + context adjustment; Critical → High → Medium → Low; within a tier, higher confidentiality impact first.
4. **Pulls full detail** for each surviving finding from its source module report — issue, impact, proof, remediation, dynamic test — preserved verbatim, never summarized or truncated.
5. **Validates completeness** against `00_plan.md`: every selected scan is represented (or its clean result is noted); `90_design_checklist.md` is included when selected; every surviving finding has severity, OWASP risk, location, proof, and remediation; every finding uses its module's classification tags; manual-review items land in the appendix with location and justification; duplicates carry cross-references; `manifest.md` metadata appears in the header; no project source files were modified.
6. Writes `{{ REPORTS_ROOT }}/report.md` using exactly this output format, then **deletes all `NN_findings.yaml` cards**.

***

```markdown
---
title: Security Assessment Final Report
<tracked-document header fields per `frontmatter-protocol` `[ref: #tracking-fields]`, bound as repo: [audited entity or "generic"], source: [project root]>
---

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

- **Source scan**: `{{ REPORTS_ROOT }}/NN_<name>.md` (e.g., `02_sqli.md`)
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

Checklist tallies from the module-90 card: PASS: N / FAIL: N / NOT_APPLICABLE: N / NEEDS_MANUAL_REVIEW: N.

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
- Read `{{ REPORTS_ROOT }}/manifest.md` first and reflect the `entity` value (`project-level` or a specific name) in the report header.
- If `{{ REPORTS_ROOT }}/01_architecture.md` exists, use it to enrich the severity rationale with application-specific context (e.g., "this endpoint handles payment data, making confidentiality impact Critical").
- Omit severity sections entirely (e.g., the `### Low` heading) if no findings fall in that tier.
- This subagent writes only `{{ REPORTS_ROOT }}/report.md` (deleting the `NN_findings.yaml` cards afterward) and must not modify any project source code or configuration.
- After `{{ REPORTS_ROOT }}/report.md` is written, the ROOT agent persists per `serena-protocol` `[ref: #serena-memory-mutation]` so the audit artifacts are persisted with the rest of Serena memory.
