---
name: security-audit
description: Security assessment / SAST workflow for a codebase aligned with the OWASP API Security Top 10 2023. Thin-core orchestration over an artifact-driven pipeline — architecture reconnaissance, a mandatory screener that emits a machine-readable plan, parallel detection subagents per scan class (IDOR/BOLA, SQLi, SSRF, XSS, RCE, XXE, SSTI, JWT, missing authentication, insecure file upload, path traversal, business logic flaws, GraphQL injection, hardcoded secrets, BOPLA, unrestricted resource consumption, improper inventory management, unsafe consumption of APIs, security misconfiguration, backdoors, obfuscation, dependency risks, JVM anomalies), an independent validation pass with core adjudication, and a consolidated final report under `.serena/memories/audit/`. Use when asked for a security audit, SAST scan, vulnerability assessment, code security review, penetration-test style source review, OWASP API 2023 coverage, or specific vulnerability class searches such as SQLi, XSS, IDOR, SSRF, JWT, BOLA, BOPLA, misconfiguration, etc.
triggers:
  request: "sast, security audit, vulnerability assessment, code security review, penetration test, pentest, security scan, аудит безопасности, поиск уязвимостей, сканирование уязвимостей, проверка безопасности, SQL injection, SQLi, XSS, IDOR, SSRF, RCE, XXE, SSTI, JWT, file upload, path traversal, missing auth, business logic, GraphQL injection, hardcoded secrets, BOLA, BOPLA, broken object level authorization, broken object property level authorization, resource consumption, rate limiting, inventory management, unsafe consumption of APIs, third-party API, security misconfiguration, OWASP API 2023, OWASP API Security Top 10"
requires:
  - entity-protocol
  - frontmatter-protocol
  - serena-protocol
version: 0.1.0
---

# SKILL: SAST Audit (Thin-Core Orchestration)
[ref: #sa-sast-audit]

This skill orchestrates a source-code security assessment. The core agent NEVER performs detection, validation passes, or consolidation reading itself; it dispatches subagents against `references/` contracts and moves small artifacts between them. Detection, validation intake, and report consolidation all happen inside subagents.

## 1. Core context discipline (HARD)
[ref: #sa-core-context-discipline]

The core agent holds ONLY:

- This `SKILL.md`.
- `references/registry.md` — the single scan registry (read it fully at session start).
- `references/execution-protocol.md` — the detection dispatch playbook (read it fully at session start; it is mechanics, not a domain reference, so the no-body rule below does not apply to it).
- The YAML frontmatter of `{{ REPORTS_ROOT }}/00_plan.md` (never the prose tables) and of any scan file (02–24) or meta file (00, 01, 90, 98, 99) it is about to dispatch (never the body).
- Verdict ledgers returned by subagents.

The core MUST NOT read: scan/meta reference bodies (a dispatched subagent reads its own reference), module reports `NN_<name>.md` (the validator reads them), recon/batch intermediates. The single exception is the adjudication pass (§4.6): targeted reads of the affected module-report sections and of source for re-verifying doubtful findings.

Frontmatter reading uses the canonical extraction primitives of `frontmatter-protocol` (`[ref: #fm-read-primitive]`); nothing else is loaded for dispatch.

## 2. Session initialization
[ref: #sa-session-init]

1. **Capture the audit timestamp** — `AUDIT_DATETIME_UTC` (UTC ISO 8601, e.g. `2026-07-05T03:20:41Z`) and `AUDIT_DIR_SUFFIX` (compact label, e.g. `sast_2026_0705_0320`). Also capture the audited repository's git identity (`GIT_BRANCH`, `GIT_COMMIT`, `GIT_COMMITTED_AT`) with the canonical triplet of `frontmatter-protocol` `[ref: #tracking-git-commands]`, run inside the audited repository — every artifact header needs it.
2. **Determine the audit target** — if the user names an entity, verify a card exists at `.serena/memories/repos/<entity>/overview.md`. If missing, halt and tell the user to create it via `repo-audit` first (legacy `entities/` cards: migrate per `entity-protocol` `[ref: #entity-migration-legacy]`). If no entity is named, run a project-level audit (`ENTITY_NAME=""`).
3. **Build and create `{{ REPORTS_ROOT }}`** — `.serena/memories/audit/<ENTITY_NAME>/<AUDIT_DIR_SUFFIX>/` or `.serena/memories/audit/<AUDIT_DIR_SUFFIX>/`.
4. **Write `{{ REPORTS_ROOT }}/manifest.md`** — it opens with the tracked-document header exactly per `frontmatter-protocol` `[ref: #tracking-fields]` (field semantics: `[ref: #tracking-field-semantics]`), bound as `title: SAST Audit Manifest`, `repo: <ENTITY_NAME>` (`generic` for a project-level audit), `source: <project root>`, and followed by the H1 `# SAST Audit Manifest`. The manifest adds skill-declared extras after the header fields: `entity: <ENTITY_NAME or "project-level">`, `reports_root: <REPORTS_ROOT path>`, `started_at: <AUDIT_DATETIME_UTC>`.

5. Pass the concrete `{{ REPORTS_ROOT }}` path to every subagent prompt.

## 3. The scan registry
[ref: #sa-scan-registry]

`references/registry.md` is the ONLY enumeration of the audit suite. It defines, per module: layer (meta / detection), reference file, OWASP mapping, applicability predicate, classification tag family, and output artifact. Dispatch derives from it. The screener's coverage matrix, the final report's coverage tables, and this skill's `description` are sanctioned derived copies — when a scan is added or renamed, update the registry first, then sync every derived copy in the same edit (drift-check rule).

## 4. Pipeline
[ref: #sa-pipeline]

### 4.1 Architecture analysis (subagent, blocking)

If `{{ REPORTS_ROOT }}/01_architecture.md` does not exist, dispatch a `coder` subagent with `references/01-analysis.md` and `{{ REPORTS_ROOT }}`. Wait for completion.

### 4.2 Screener (subagent, blocking)

If `{{ REPORTS_ROOT }}/00_plan.md` does not exist, dispatch a `coder` subagent with `references/00-screener.md` and `{{ REPORTS_ROOT }}`. It writes `{{ REPORTS_ROOT }}/00_plan.md` whose YAML frontmatter is the machine-readable plan. Never skip the screener: if the user asks for one vulnerability class, the screener still runs and may add complementary scans.

### 4.3 Plan parsing (core, cheap)

Read ONLY the YAML frontmatter of `00_plan.md` (canonical frontmatter extraction). The dispatch queue is `selected` + `cross_mapped` + `conditional` — conditional scans are included by default and listed to the user in the pre-dispatch summary (excluded only on explicit user opt-out); `design_checklist` gates module 90. Do not parse the prose tables.

### 4.4 Detection dispatch (per-stage, flat, up to 6 concurrent)

For each detection scan in the queue, the core runs the three stages of `references/execution-protocol.md`, tracking state through artifact filenames only (never reading recon, batch, or verify files):

1. **Recon+split** — dispatch a `coder` subagent with the scan's reference file, the protocol file, and `{{ REPORTS_ROOT }}` → produces `NN_recon.md` + `NN_batch_*.md` (≤3 candidates each), or the final `NN_<name>.md` directly on zero candidates.
2. **Verify** — for each `NN_batch_N.md`, dispatch a `coder` subagent with the scan's reference file and that batch file → `NN_verify_N.md`.
3. **Merge** — when all verify files of a scan exist, dispatch a `coder` subagent with the scan's reference file → final `NN_<name>.md`; the merge subagent deletes the intermediates.

Run at most **6 subagents concurrently across all stages and scans**; stages of different scans are independent, so free slots are filled from any pending stage. If `design_checklist: true`, dispatch `references/90-design-checklist.md` alongside detection — it needs only `01_architecture.md`.

Before the first dispatch of a scan, the core MAY read the scan file's frontmatter (subject + cards) to brief itself on the contract — and nothing more. Never inline reference content into subagent prompts; pass paths, not contents.

### 4.5 Validation (subagent, blocking)

After all module reports exist, dispatch a `coder` subagent with `references/98-validator.md` and `{{ REPORTS_ROOT }}`. It spot-checks every include-tag finding against source and writes `{{ REPORTS_ROOT }}/98_validation.md` plus returns the verdict ledger inline. It edits nothing else.

### 4.6 Core adjudication (core, the one judgment pass)

Read `98_validation.md`. For every `DOUBTFUL` and `UNVERIFIABLE` item, re-verify against the source with targeted reads, then apply the final call in the affected module report: downgrade with note, remove with reason, or keep. `CONFIRMED` items stand; `[NEEDS MANUAL REVIEW]` items stay untouched; original family labels are preserved.

### 4.7 Consolidation (map-reduce)

1. **Extract** — for each existing detection module report (scans 02–24) and, if run, `90_design_checklist.md`, dispatch a `coder` extractor subagent with `references/99-report.md` and that report's path (parallel within the 6-slot limit) → `NN_findings.yaml` cards.
2. **Consolidate (blocking)** — dispatch one `coder` subagent with `references/99-report.md` and `{{ REPORTS_ROOT }}` → it dedups the cards, scores severity, pulls full detail only for surviving findings, writes `{{ REPORTS_ROOT }}/report.md`, and deletes the cards.

### 4.8 Persistence (core)

Persist per `serena-protocol` `[ref: #serena-memory-mutation]` — the whole `{{ REPORTS_ROOT }}` tree is committed with the rest of Serena memory.

## 5. Subagent dispatch rules
[ref: #sa-dispatch-rules]

- `coder` subagents for all stages; each receives the reference file path(s) it needs (scan file, and for recon also `references/execution-protocol.md`), plus the concrete `{{ REPORTS_ROOT }}`.
- Subagents are read-only on the project: they write only their own artifacts under `{{ REPORTS_ROOT }}/`, never project source, tests, or configuration.
- Pass paths, never inline reference content.
- Detection stages and the design checklist run concurrently within the 6-slot limit; analysis, screener, validation, and consolidation each run alone because later stages depend on their artifacts.
- **Failure policy:** if a stage subagent completes but its expected artifact is absent, re-dispatch once with the error noted and the instruction: *if you cannot write the artifact, return its complete text inline instead*. If the artifact is still absent, the core writes it from the returned inline text at the expected path under `{{ REPORTS_ROOT }}`. Never proceed to a later stage over a silently missing artifact.
- **Deliverable-in-report (always):** every dispatch prompt includes the instruction that a subagent whose write tools are blocked returns the complete deliverable text in its final report (`subagents-protocol` §12.4). The core then writes the artifact itself.
- **Cleanup miss:** if the final module report exists but intermediates remain (`NN_recon.md`, `NN_batch_*.md`, `NN_verify_*.md`), the core deletes the intermediates itself — filenames only, no reads.

## 6. Artifact lifecycle
[ref: #sa-artifact-lifecycle]

- `01_architecture.md`, `00_plan.md`, `manifest.md` — persist to the end.
- `NN_findings.yaml` — born at the consolidation extract stage, deleted by the consolidator after `report.md` is written.
- Detection intermediates (`NN_recon.md`, `NN_batch_N.md`, `NN_verify_N.md`) — lifecycle owned by `execution-protocol.md` `[ref: #protocol-artifacts]`.
- `NN_<name>.md`, `90_design_checklist.md`, `98_validation.md`, `report.md` — persist; `report.md` is the only deliverable the user reads.

## 7. Important reminders
[ref: #sa-reminders]

- Never skip the screener. If a scan is not in the `00_plan.md` frontmatter, do not run it unless the user explicitly requests it.
- All metadata timestamps use UTC ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`); the `sast_YYYY_MMDD_HHMM` suffix is only a directory label.
- When evidence is ambiguous, prefer `[NEEDS MANUAL REVIEW]` over dismissing a finding — false negatives are worse than false positives.
- The core's only large-context moment is adjudication (§4.6); keep it targeted.
