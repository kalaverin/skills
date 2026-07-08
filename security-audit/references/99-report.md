# Final Security Report Generation

[ref: #final-report]

You are consolidating all completed SAST vulnerability scan results into a single prioritized security report.

**Prerequisites**: At least one final module report (e.g., `{{ REPORTS_ROOT }}/02_sqli.md`) must exist in `{{ REPORTS_ROOT }}`. Run the vulnerability detection skills first if none exist.

## Subagent Constraints

The report subagent must **only** write `{{ REPORTS_ROOT }}/report.md`. It must **never** edit project source code, configuration files, tests, build scripts, or any file outside `{{ REPORTS_ROOT }}`.

---

## What to Include

Only include findings with these classifications from each result file:
- `[VULNERABLE]`
- `[LIKELY VULNERABLE]`

Exclude `[NOT VULNERABLE]` and `[NEEDS MANUAL REVIEW]` findings from the main report body. Count them in the summary, and list `[NEEDS MANUAL REVIEW]` items in the dedicated appendix (see output template).

---

## Severity Ranking

Assign each finding a severity tier — **Critical**, **High**, **Medium**, or **Low** — using the table below as your baseline. Adjust up or down based on context (e.g., an IDOR that exposes financial records is High, not Medium).

| Vulnerability Class | Default Severity |
|---------------------|------------------|
| RCE via command injection, eval, or unsafe deserialization | Critical |
| SSTI (Server-Side Template Injection) | Critical |
| SQLi on authentication endpoints | Critical |
| JWT algorithm confusion (alg:none, RS256→HS256) | Critical |
| File upload leading to code execution (webshell) | Critical |
| Hardcoded secrets in source or client-side code (credentials, tokens, API keys) | Critical |
| SQLi with full data extraction capability | High–Critical |
| GraphQL injection (user-controlled operation document enabling unauthorized fields or gateway abuse) | High–Critical |
| XXE with file read or internal SSRF | High–Critical |
| Missing authentication on sensitive endpoints | High–Critical |
| SSRF reaching internal services or cloud metadata | High |
| Path traversal reading sensitive or config files | High |
| File upload with stored content accessible to others | High |
| IDOR on PII, financial, or health data | High |
| XSS (stored/persistent) | High |
| Broken Object Property Level Authorization (BOPLA / excessive data exposure / mass assignment) | High |
| Unrestricted resource consumption (DoS, cost abuse, missing rate limits) | High |
| Security misconfiguration (debug endpoints, default credentials, verbose errors, unsafe headers) | High |
| Unsafe consumption of APIs (blind trust of third-party data or responses) | High |
| JWT with missing or bypassable claim validation | Medium–High |
| Missing authentication on lower-sensitivity endpoints | Medium |
| IDOR on non-sensitive data | Medium |
| XSS (reflected or DOM) | Medium |
| Business logic flaws (price manipulation, workflow bypass) | Medium |
| Improper inventory management (shadow/deprecated endpoints, missing docs) | Medium |
| Information disclosure of non-sensitive data | Low |

**OWASP API 2023 alignment**: The defaults above map to OWASP API Security Top 10 2023 risk ratings — API2 and API5 default to **Critical**; API1, API3, API4, API7, API8, and API10 default to **High**; API6 and API9 default to **Medium**. Hardcoded secrets are treated as severe credential exposure and default to **Critical**.

**Confidentiality as a tiebreaker**: When two findings share the same baseline severity, rank higher the one with greater confidentiality impact — i.e., the greater its potential to expose sensitive user data, credentials, or system internals.

---

## Execution

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
   - `90_design_checklist.md`

### Step 2: Read and extract findings

Read each existing result file. For every finding classified as `[VULNERABLE]` or `[LIKELY VULNERABLE]`, extract:
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
- [ ] Scans 15–20 and `90_design_checklist.md` are included if selected in the plan.
- [ ] Every `[VULNERABLE]` and `[LIKELY VULNERABLE]` finding has a severity, OWASP risk, location, proof, and remediation.
- [ ] `[NEEDS MANUAL REVIEW]` items are listed in the appendix with location and justification.
- [ ] Duplicate findings are deduplicated with cross-references.
- [ ] `manifest.md` metadata is reflected in the report header.
- [ ] Only `{{ REPORTS_ROOT }}/report.md` is written; no project source files were modified.

### Step 6: Write `{{ REPORTS_ROOT }}/report.md`

Use exactly this output format:

---

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
| API5:2023 Broken Function Level Authorization | `10_missingauth.md` | ... | N |
| API6:2023 Unrestricted Access to Sensitive Business Flows | `13_businesslogic.md` | ... | N |
| API7:2023 Server Side Request Forgery | `03_ssrf.md` | ... | N |
| API8:2023 Security Misconfiguration | `20_misconfiguration.md`, `15_hardcodedsecrets.md` | ... | N |
| API9:2023 Improper Inventory Management | `18_inventory.md` | ... | N |
| API10:2023 Unsafe Consumption of APIs | `19_unsafeapiconsumption.md` | ... | N |

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
| Design checklist | `{{ REPORTS_ROOT }}/90_design_checklist.md` | Completed / Not run |

## Appendix: Findings Requiring Manual Review

For every `[NEEDS MANUAL REVIEW]` item in any result file, include:

| # | Title | File / Endpoint | Source Scan | Justification |
|---|-------|-----------------|-------------|---------------|
| 1 | ... | ... | `15_hardcodedsecrets.md` | [why it could not be automatically classified] |
```

---

## Important Reminders

- Include ONLY `[VULNERABLE]` and `[LIKELY VULNERABLE]` findings in the Findings section; `FAIL` items from `90_design_checklist.md` go in the Design & Operational Control Gaps section.
- Mark `[LIKELY VULNERABLE]` findings clearly: append **⚠ Likely Vulnerable** after the finding title.
- Preserve all details from the original findings — do not summarize or truncate Proof, Remediation, or Dynamic Test sections.
- Read `{{ REPORTS_ROOT }}/manifest.md` first and reflect the entity name / `project-level` flag in the report header.
- If `{{ REPORTS_ROOT }}/01_architecture.md` exists, use it to enrich the severity rationale with application-specific context (e.g., "this endpoint handles payment data, making confidentiality impact Critical").
- Omit severity sections entirely (e.g., the `### Low` heading) if no findings fall in that tier.
- This subagent must only write `{{ REPORTS_ROOT }}/report.md` and must not modify any project source code or configuration.
- After `{{ REPORTS_ROOT }}/report.md` is written, run `just serena-checkpoint` from the project root so the audit artifacts are persisted with the rest of Serena memory.
