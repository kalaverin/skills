---
subject: "Single scan registry for SAST audits; master table of all modules — id, reference file, purpose, OWASP API 2023 mapping, applicability predicate, classification tag family, output artifact; dispatch, screener selection, and consolidation derive from here."
index:
  - anchor: registry-master-table
    what: "The single authoritative enumeration of every audit module — meta references (00 screener, 01 analysis, 90 design-checklist, 98 validator, 99 report) and detection scans (02–24) — with file path, layer, purpose, OWASP risk mapping, applicability predicate, classification tag family, and output artifact name."
    problem: "Scan list lives in fifteen places at once — SKILL.md table, screener matrix, report heatmap, coverage appendix, skill description — so adding or renaming one scan demands synchronized edits everywhere and drift is guaranteed; registry duplication, enumeration drift, lockstep edits, stale lists, missing modules, ownership gap, single source."
    use_when: "Adding, renaming, or removing a scan; checking which file, output artifact, OWASP risks, or tag family a module owns; deriving dispatch or coverage lists."
    avoid_when: "Selection logic for a concrete project — that is `00-screener.md`; consolidation mechanics — `99-report.md`."
    expected: "Every consumer cites this table; enumerations elsewhere (SKILL.md `description`, screener coverage matrix, report coverage tables) are sanctioned derived copies synced in the same edit as any registry change."
  - anchor: registry-tag-families
    what: "The classification tag families per module group: standard `[VULNERABLE]`/`[LIKELY VULNERABLE]` for 02–20 and 24, `[CONFIRMED BACKDOOR]`/`[LIKELY BACKDOOR]` for 21, `[MALICIOUS OBFUSCATION]`/`[LIKELY MALICIOUS]` for 22, `[CONFIRMED THREAT]`/`[LIKELY THREAT]` for 23, plus excluded tags and the `FAIL` vocabulary of module 90."
    problem: "Consolidation silently drops findings when module verdict labels differ from standard pair — backdoor, obfuscation, and threat findings vanish from final output; label mismatch, family confusion, silent data loss, consolidation gap, extraction rules, mapping table."
    use_when: "Writing or reviewing extraction, validation, or consolidation logic; adding a module with a non-standard verdict vocabulary."
    avoid_when: "Per-finding adjudication rules — those live in the detection modules themselves."
    expected: "Every module's verdict labels map to exactly one family; consolidation loses no finding to a tag mismatch."
  - anchor: registry-applicability
    what: "Applicability predicates per scan: technology or feature conditions that make a scan mandatory (SQL/ORM for 02, GraphQL for 14, JVM runtime for 24, third-party dependencies for 23) and the near-unconditional scans (10, 17, 18, 20, 21, 22)."
    problem: "Screener must decide run-or-skip per project without guessing — JVM-only scan fired against Go service burns slots, while skipped implant scan hides compromise; applicability guesswork, false skips, language gating, exposure judgment, selection errors, resource waste."
    use_when: "Reviewing or extending the screener's coverage decision matrix; checking whether a scan is unconditional or technology-gated."
    avoid_when: "Concrete verdicts for one project — the screener applies these predicates; this section only owns their canonical form."
    expected: "Each scan's applicability is declared once here; the screener matrix cites predicates instead of restating them."
---

# Scan Registry (security-audit)

[ref: #registry-master-table]

Single source of truth for the audit module suite. SKILL.md dispatch, the screener's coverage matrix, and the final report's coverage sections derive from this table — nothing else may enumerate the scan suite.

| ID | Layer | Reference file | Purpose | OWASP API 2023 | Applicability predicate | Tag family | Output artifact |
|---|---|---|---|---|---|---|---|
| 00 | meta | `references/00-screener.md` | Diagnostic — decides which scans run | — | Always (after 01) | — | `00_plan.md` |
| 01 | meta | `references/01-analysis.md` | Architecture reconnaissance | — | Always (first) | — | `01_architecture.md` |
| 02 | detection | `references/02-sqli.md` | SQL injection | API8/API10 (cross-mapped) | SQL database or ORM present | standard | `02_sqli.md` |
| 03 | detection | `references/03-ssrf.md` | Server-side request forgery | API7 | Outbound HTTP/URL fetching present | standard | `03_ssrf.md` |
| 04 | detection | `references/04-xss.md` | Cross-site scripting | API8 (cross-mapped) | HTML rendering, templates, or frontend present | standard | `04_xss.md` |
| 05 | detection | `references/05-rce.md` | Remote code execution | API8/API10 (cross-mapped) | Command exec, eval, deserialization, or plugin loading present | standard | `05_rce.md` |
| 06 | detection | `references/06-ssti.md` | Server-side template injection | API8 (cross-mapped) | Server-side template engine present | standard | `06_ssti.md` |
| 07 | detection | `references/07-xxe.md` | XML external entity | API8 (cross-mapped) | XML parsing present | standard | `07_xxe.md` |
| 08 | detection | `references/08-idor.md` | Insecure direct object reference (BOLA) | API1 | Object IDs/slugs in routes or parameters | standard | `08_idor.md` |
| 09 | detection | `references/09-jwt.md` | JWT weaknesses | API2 | JWT issuance or validation present | standard | `09_jwt.md` |
| 10 | detection | `references/10-missingauth.md` | Missing authentication / BFLA | API2, API5 | Any API endpoints | standard | `10_missingauth.md` |
| 11 | detection | `references/11-fileupload.md` | Insecure file upload | API8 (cross-mapped) | File upload handlers present | standard | `11_fileupload.md` |
| 12 | detection | `references/12-pathtraversal.md` | Path traversal | API8 (cross-mapped) | Filesystem access from user input | standard | `12_pathtraversal.md` |
| 13 | detection | `references/13-businesslogic.md` | Business logic flaws | API6 | State-changing business flows | standard | `13_businesslogic.md` |
| 14 | detection | `references/14-graphql.md` | GraphQL injection | API8/API10 (cross-mapped) | GraphQL endpoint present | standard | `14_graphql.md` |
| 15 | detection | `references/15-hardcodedsecrets.md` | Hardcoded secrets in public/client code | API8 | Public or client-distributed code | standard | `15_hardcodedsecrets.md` |
| 16 | detection | `references/16-bopla.md` | Broken Object Property Level Authorization | API3 | Serializers, DTO binding, or update endpoints | standard | `16_bopla.md` |
| 17 | detection | `references/17-resourceconsumption.md` | Unrestricted resource consumption | API4 | Any API (near-unconditional) | standard | `17_resourceconsumption.md` |
| 18 | detection | `references/18-inventory.md` | Improper inventory management | API9 | Any project (near-unconditional) | standard | `18_inventory.md` |
| 19 | detection | `references/19-unsafeapiconsumption.md` | Unsafe consumption of APIs | API10 | Third-party API integrations present | standard | `19_unsafeapiconsumption.md` |
| 20 | detection | `references/20-misconfiguration.md` | Security misconfiguration | API8 | Any project (near-unconditional) | standard | `20_misconfiguration.md` |
| 21 | detection | `references/21-backdoors.md` | Deliberate malicious code / implants | API8, API10 | Near-unconditional (implant indicators) | backdoor | `21_backdoors.md` |
| 22 | detection | `references/22-obfuscation.md` | Malicious obfuscation | API8, API10 | Near-unconditional (implant indicators) | obfuscation | `22_obfuscation.md` |
| 23 | detection | `references/23-dependencies.md` | Supply chain / dependency risks | API8, API10 | Third-party dependencies present | threat | `23_dependencies.md` |
| 24 | detection | `references/24-jvm-anomalies.md` | JVM-specific anomalies | API5, API8, API10 | JVM runtime (Java/Kotlin) — language-gated | standard | `24_jvm_anomalies.md` |
| EP | protocol | `references/execution-protocol.md` | Shared three-stage detection pipeline (recon+split, verify, merge) | — | Every detection scan 02–24 | — | (mechanics only, no artifact) |
| 90 | meta | `references/90-design-checklist.md` | API security design checklist (PASS/FAIL) | Multi (see its alignment table) | Any API | checklist (`FAIL`) | `90_design_checklist.md` |
| 98 | meta | `references/98-validator.md` | Independent finding validation | — | Always (after detection) | — | `98_validation.md` |
| 99 | meta | `references/99-report.md` | Consolidated final report | — | Always (last) | — | `report.md` |

## Classification tag families

[ref: #registry-tag-families]

Every detection module emits findings under one of these families. Consolidation (`99-report.md`) and validation (`98-validator.md`) MUST key on families, never on a flat `[VULNERABLE]` assumption.

| Family | Include in report | Excluded (counted; NMR to appendix) | Modules |
|---|---|---|---|
| standard | `[VULNERABLE]`, `[LIKELY VULNERABLE]` | `[NOT VULNERABLE]`, `[SUSPICIOUS BUT LEGITIMATE]`, `[NEEDS MANUAL REVIEW]` | 02–20, 24 |
| backdoor | `[CONFIRMED BACKDOOR]`, `[LIKELY BACKDOOR]` | `[SUSPICIOUS BUT LEGITIMATE]`, `[NEEDS MANUAL REVIEW]` | 21 |
| obfuscation | `[MALICIOUS OBFUSCATION]`, `[LIKELY MALICIOUS]` | `[LEGITIMATE OBFUSCATION]`, `[NEEDS MANUAL REVIEW]` | 22 |
| threat | `[CONFIRMED THREAT]`, `[LIKELY THREAT]` | `[LOW RISK]`, `[NEEDS MANUAL REVIEW]` | 23 |
| checklist | `FAIL` (to the design-gaps section) | `PASS`, `NOT_APPLICABLE`, `NEEDS_MANUAL_REVIEW` | 90 |

Original labels are preserved end-to-end: a `[CONFIRMED BACKDOOR]` is never re-labeled `[VULNERABLE]`; the ⚠ marker attaches to the family-appropriate "likely" tag.

## Applicability predicates

[ref: #registry-applicability]

Canonical form of each scan's applicability, cited by the screener's coverage matrix instead of being restated there.

- **Technology-gated:** 02 (SQL/ORM), 03 (outbound HTTP), 04 (HTML/templates/frontend), 05 (exec/eval/deserialization), 06 (template engines), 07 (XML), 08 (object IDs in routes), 09 (JWT), 11 (uploads), 12 (filesystem from input), 13 (business flows), 14 (GraphQL), 15 (client/public code), 16 (serializers/binding), 19 (third-party APIs), 23 (dependencies).
- **Language-gated:** 24 — JVM only (Java/Kotlin). Never select for non-JVM stacks.
- **Near-unconditional:** 10, 17, 18, 20 — every API project; 21, 22 — implant indicators are rare on recon, so the conservative default is Run unless the user excludes them; 90 — any API.
- **Infrastructure (meta layer):** 01 always first, 00 always after 01, 90 in parallel with detection, 98 after detection, 99 always last.
