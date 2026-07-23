---
name: security-audit
description: Security assessment / SAST workflow for a codebase aligned with the OWASP API Security Top 10 2023. Runs architecture reconnaissance, a mandatory screener that selects applicable vulnerability scans, then dispatches detection subagents for each selected scan class (IDOR/BOLA, SQLi, SSRF, XSS, RCE, XXE, SSTI, JWT, missing authentication, insecure file upload, path traversal, business logic flaws, GraphQL injection, hardcoded secrets, BOPLA, unrestricted resource consumption, improper inventory management, unsafe consumption of APIs, security misconfiguration). Validates findings and produces a consolidated final report stored under `.serena/memories/audit/`. Use when asked for a security audit, SAST scan, vulnerability assessment, code security review, penetration-test style source review, OWASP API 2023 coverage, or specific vulnerability class searches such as SQLi, XSS, IDOR, SSRF, JWT, BOLA, BOPLA, misconfiguration, etc.
triggers:
  request: "sast, security audit, vulnerability assessment, code security review, penetration test, pentest, security scan, аудит безопасности, поиск уязвимостей, сканирование уязвимостей, проверка безопасности, SQL injection, SQLi, XSS, IDOR, SSRF, RCE, XXE, SSTI, JWT, file upload, path traversal, missing auth, business logic, GraphQL injection, hardcoded secrets, BOLA, BOPLA, broken object level authorization, broken object property level authorization, resource consumption, rate limiting, inventory management, unsafe consumption of APIs, third-party API, security misconfiguration, OWASP API 2023, OWASP API Security Top 10"
requires:
  - project-audit
---

# SKILL: SAST Audit

This skill orchestrates a source-code security assessment. It does not perform
the detection itself; it dispatches specialized `coder` subagents, each reading
exactly one reference file, to perform reconnaissance, screening, detection,
validation, and reporting.

All audit artifacts live under a single `{{ REPORTS_ROOT }}` directory inside
`.serena/memories/audit/`. The root agent creates this directory at the start of
the audit and passes the concrete path to every subagent.

## Session initialization

Before dispatching any subagent, the root agent must:

1. **Capture the audit timestamp**
   - `AUDIT_DATETIME_UTC` — UTC ISO 8601, e.g. `2026-07-05T03:20:41Z`.
   - `AUDIT_DIR_SUFFIX` — compact directory suffix, e.g. `sast_2026_0705_0320`.
     This is only a filesystem label; all metadata uses `AUDIT_DATETIME_UTC`.

2. **Determine the audit target**
   - If the user explicitly names an entity (e.g., "audit entity `text`"),
     check whether a card exists at `.serena/memories/entities/<entity>/`.
     - If the card exists, set `ENTITY_NAME=<entity>`.
     - If the card does **not** exist, **halt immediately** and tell the user:
       "Entity `<entity>` has no card in `.serena/memories/entities/`. Create
       it via `project-audit` before running an entity-scoped audit."
   - If no entity is named, set `ENTITY_NAME=""` (project-level audit).

3. **Build `{{ REPORTS_ROOT }}`**
   - With entity:
     `.serena/memories/audit/<ENTITY_NAME>/<AUDIT_DIR_SUFFIX>/`
   - Without entity:
     `.serena/memories/audit/<AUDIT_DIR_SUFFIX>/`

4. **Create `{{ REPORTS_ROOT }}`** if it does not exist.

5. **Write a manifest** at `{{ REPORTS_ROOT }}/manifest.md`:

   ```markdown
   ---
   title: SAST Audit Manifest
   created_at: [AUDIT_DATETIME_UTC]
   entity: [ENTITY_NAME or "project-level"]
   reports_root: [{{ REPORTS_ROOT }}]
   source: [project root]
   ыtarted_at: [AUDIT_DATETIME_UTC]
   ---
   ```

6. **Pass `{{ REPORTS_ROOT }}`** to every subagent prompt. Subagents must treat any
   `{{ REPORTS_ROOT }}/` prefix they see in their assigned reference file as the
   concrete path they received.

## Master workflow

1. **Ensure architecture context**
   - If `{{ REPORTS_ROOT }}/01_architecture.md` does not exist, dispatch the **analysis**
     subagent with `references/01-analysis.md` and `{{ REPORTS_ROOT }}=<path>`.
   - Wait for it to finish.

2. **Run the screener**
   - Dispatch the **screener** subagent with `references/00-screener.md` and
     `{{ REPORTS_ROOT }}=<path>`.
   - The screener reads `{{ REPORTS_ROOT }}/01_architecture.md` and writes
     `{{ REPORTS_ROOT }}/00_plan.md`, which lists every detection scan to run and
     justifies each choice.
   - Wait for it to finish.

3. **Dispatch detection scans**
   - Read `{{ REPORTS_ROOT }}/00_plan.md`.
   - For each selected scan, queue a `coder` subagent with the corresponding
     numbered reference file from the activation table below and
     `{{ REPORTS_ROOT }}=<path>`.
   - Run up to **5 subagents in parallel**. When a slot frees, start the next
     queued scan.
   - Wait until all queued scans finish.

4. **Validate findings**
   - Read every final module report produced in `{{ REPORTS_ROOT }}`
     (e.g., `02_sqli.md`, `03_ssrf.md`, etc.).
   - Skip `90_design_checklist.md` during this validation; it uses `PASS`/`FAIL`
     classifications rather than `[VULNERABLE]`.
   - For each `[VULNERABLE]` and `[LIKELY VULNERABLE]` finding, perform an
     in-session spot check against the actual source code.
   - If a finding is clearly a false positive, downgrade or remove it and note
     the reason. If uncertain, keep the original classification and add a note.

5. **Run the design checklist**
   - If the screener selected `references/90-design-checklist.md`, dispatch a
     `coder` subagent with that reference and `{{ REPORTS_ROOT }}=<path>`.
   - It writes `{{ REPORTS_ROOT }}/90_design_checklist.md`.

6. **Generate final report**
   - Dispatch the **report** subagent with `references/99-report.md` and
     `{{ REPORTS_ROOT }}=<path>`.
   - It reads `{{ REPORTS_ROOT }}/01_architecture.md`, all validated final
     module reports from `{{ REPORTS_ROOT }}`, `90_design_checklist.md`, and
     writes `{{ REPORTS_ROOT }}/report.md`.

7. **Commit to Serena memory**
   - After the final report is written, persist per `serena-protocol`
     `[ref: #serena-memory-mutation]` — this persists the entire
     `{{ REPORTS_ROOT }}` tree in git via Serena's memory commit mechanism.

## Activation table

Load each referenced section per the canonical loader mechanics in `frontmatter-protocol` `[ref: #lazy-load-routing]` (bounded extraction — never read reference files in full).

| # | Reference | Anchor | Scan / purpose | Output file |
|---|---|---|---|---|
| 00 | `references/00-screener.md` | [ref: #screener] | Diagnostic — decides which scans apply | `{{ REPORTS_ROOT }}/00_plan.md` |
| 01 | `references/01-analysis.md` | [ref: #codebase-analysis] | Architecture reconnaissance | `{{ REPORTS_ROOT }}/01_architecture.md` |
| 02 | `references/02-sqli.md` | [ref: #sqli-detection] | SQL injection | `{{ REPORTS_ROOT }}/02_sqli.md` |
| 03 | `references/03-ssrf.md` | [ref: #ssrf-detection] | Server-side request forgery | `{{ REPORTS_ROOT }}/03_ssrf.md` |
| 04 | `references/04-xss.md` | [ref: #xss-detection] | Cross-site scripting | `{{ REPORTS_ROOT }}/04_xss.md` |
| 05 | `references/05-rce.md` | [ref: #rce-detection] | Remote code execution | `{{ REPORTS_ROOT }}/05_rce.md` |
| 06 | `references/06-ssti.md` | [ref: #ssti-detection] | Server-side template injection | `{{ REPORTS_ROOT }}/06_ssti.md` |
| 07 | `references/07-xxe.md` | [ref: #xxe-detection] | XML external entity | `{{ REPORTS_ROOT }}/07_xxe.md` |
| 08 | `references/08-idor.md` | [ref: #idor-detection] | Insecure direct object reference | `{{ REPORTS_ROOT }}/08_idor.md` |
| 09 | `references/09-jwt.md` | [ref: #jwt-detection] | JWT weaknesses | `{{ REPORTS_ROOT }}/09_jwt.md` |
| 10 | `references/10-missingauth.md` | [ref: #missingauth-detection] | Missing authentication / broken access control | `{{ REPORTS_ROOT }}/10_missingauth.md` |
| 11 | `references/11-fileupload.md` | [ref: #fileupload-detection] | Insecure file upload | `{{ REPORTS_ROOT }}/11_fileupload.md` |
| 12 | `references/12-pathtraversal.md` | [ref: #pathtraversal-detection] | Path traversal | `{{ REPORTS_ROOT }}/12_pathtraversal.md` |
| 13 | `references/13-businesslogic.md` | [ref: #businesslogic-detection] | Business logic flaws | `{{ REPORTS_ROOT }}/13_businesslogic.md` |
| 14 | `references/14-graphql.md` | [ref: #graphql-detection] | GraphQL injection | `{{ REPORTS_ROOT }}/14_graphql.md` |
| 15 | `references/15-hardcodedsecrets.md` | [ref: #hardcodedsecrets-detection] | Hardcoded secrets in public/client code | `{{ REPORTS_ROOT }}/15_hardcodedsecrets.md` |
| 16 | `references/16-bopla.md` | [ref: #bopla-detection] | Broken Object Property Level Authorization (BOPLA) | `{{ REPORTS_ROOT }}/16_bopla.md` |
| 17 | `references/17-resourceconsumption.md` | [ref: #resourceconsumption-detection] | Unrestricted resource consumption | `{{ REPORTS_ROOT }}/17_resourceconsumption.md` |
| 18 | `references/18-inventory.md` | [ref: #inventory-detection] | Improper inventory management | `{{ REPORTS_ROOT }}/18_inventory.md` |
| 19 | `references/19-unsafeapiconsumption.md` | [ref: #unsafeapiconsumption-detection] | Unsafe consumption of APIs | `{{ REPORTS_ROOT }}/19_unsafeapiconsumption.md` |
| 20 | `references/20-misconfiguration.md` | [ref: #misconfiguration-detection] | Security misconfiguration | `{{ REPORTS_ROOT }}/20_misconfiguration.md` |
| 21 | `references/21-backdoors.md` | [ref: #backdoors-detection] | Deliberate malicious code / backdoors / implants | `{{ REPORTS_ROOT }}/21_backdoors.md` |
| 22 | `references/22-obfuscation.md` | [ref: #obfuscation-detection] | Obfuscated code that may hide malicious behavior | `{{ REPORTS_ROOT }}/22_obfuscation.md` |
| 23 | `references/23-dependencies.md` | [ref: #dependencies-detection] | Supply chain / dependency risks | `{{ REPORTS_ROOT }}/23_dependencies.md` |
| 24 | `references/24-jvm-anomalies.md` | [ref: #jvm-anomalies-detection] | Kotlin/Java JVM-specific anomalies (deserialization, JNDI, reflection, ClassLoaders, JNI, KSP, etc.) | `{{ REPORTS_ROOT }}/24_jvm_anomalies.md` |
| 90 | `references/90-design-checklist.md` | [ref: #design-checklist] | API Security design checklist assessment | `{{ REPORTS_ROOT }}/90_design_checklist.md` |
| 99 | `references/99-report.md` | [ref: #final-report] | Consolidated final report | `{{ REPORTS_ROOT }}/report.md` |

## Lazy-load protocol

Only load the reference files required for the current step:

- Before dispatching a subagent, read the single reference file named in the
  activation table.
- Do not load detection references until the screener has selected them.
- Keep `SKILL.md` and the activation table loaded at all times.

## Subagent dispatch rules

- Use `coder` subagents for all SAST tasks. Their role is investigative; they
  must write only files under `{{ REPORTS_ROOT }}/` and must not modify project
  source code.
- Pass each subagent exactly one reference file path to read and the concrete
  `{{ REPORTS_ROOT }}` value.
- Do not inline reference content into subagent prompts.
- Detection scans run in parallel batches of up to **5**. Start the next queued
  scan as soon as a slot frees.
- The screener and report subagents run alone because later steps depend on
  their output.

## Validation gate

Detection subagents are instructed to collect as many suspicions as possible
and to annotate likely false positives. The root agent must:

1. Read every report from `{{ REPORTS_ROOT }}`.
2. Skip `90_design_checklist.md`; its `PASS`/`FAIL` classifications are validated during the design-checklist step, not by spot-check.
3. Spot-check `[VULNERABLE]` and `[LIKELY VULNERABLE]` findings against source.
4. Downgrade or remove confirmed false positives, adding a note.
5. Keep `[NEEDS MANUAL REVIEW]` entries unchanged.
6. After validation, update result files if any changes were made.

## Final report

After validation, dispatch the report subagent with `references/99-report.md`
and `{{ REPORTS_ROOT }}=<path>`. It produces `{{ REPORTS_ROOT }}/report.md` ranked
by severity and confidentiality impact.

## Important reminders

- Never skip the screener. If a scan is not in `{{ REPORTS_ROOT }}/00_plan.md`, do
  not run it unless the user explicitly requests it.
- If the user asks for a specific vulnerability class (e.g., "find SQLi"), still
  run the screener first; the screener may add complementary scans based on the
  architecture.
- Preserve all intermediate `{{ REPORTS_ROOT }}/*_recon.md` and
  `{{ REPORTS_ROOT }}/*_batch_*.md` files until the final report is written;
  detection references tell subagents when to delete them.
- All metadata timestamps use UTC ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`). The
  compact `sast_YYYY_MMDD_HHMM` suffix is only a directory label.
- Always persist after the final report is written, per `serena-protocol` `[ref: #serena-memory-mutation]`, so
  the audit artifacts are persisted with the rest of Serena memory.
