# security-audit
[ref: #sa-intro]

Runs a source-code security assessment aligned with the OWASP API Security Top 10 2023.

## What it does
[ref: #sa-what]

This skill orchestrates a SAST-style security audit of your codebase. The core agent acts as a thin dispatcher: it captures metadata, runs a screener, launches focused detection subagents for each vulnerability class, validates findings against source code, adjudicates doubtful items, and consolidates everything into a final report. Twenty-three detection modules cover injection, broken access control, secrets, misconfiguration, dependency risks, and JVM-specific anomalies, plus meta modules for screener, architecture, design checklist, validation, and report generation. A design checklist runs in parallel to catch API-security flaws that static detection alone can miss.

## When it activates
[ref: #sa-when]

Activates when you ask for a security audit, SAST scan, vulnerability assessment, code security review, penetration-test style review, OWASP API 2023 coverage, or a specific vulnerability class in English or Russian.

Examples:

- "Run a security audit on the payment service."
- "Scan this repo for SQL injection and SSRF."
- "Do an OWASP API Top 10 assessment."
- "Аудит безопасности сервиса заказов."

## How to run / use it
[ref: #sa-how]

Tell the agent what you want audited.
You can scope the audit to a single entity that already has a repo card, or run a project-level audit.
The agent creates a timestamped report directory, runs architecture reconnaissance, runs the screener, launches the selected scans in parallel batches, independently validates the results, and writes the final report.
You do not need to pick individual scans yourself.
All timestamps are recorded in UTC.

## What it produces
[ref: #sa-produces]

- An audit manifest under `.serena/memories/audit/<entity_or_project>/<suffix>/manifest.md`.
- Architecture reconnaissance notes at `01_architecture.md`.
- A scan plan at `00_plan.md` listing the selected vulnerability checks.
- Per-scan module reports, for example `02_sqli.md`, `03_ssrf.md`, `08_idor.md`.
- An independent validation ledger at `98_validation.md` with per-finding verdicts.
- A design checklist assessment at `90_design_checklist.md`.
- A consolidated final report at `report.md` ranked by severity and impact.

## Dependencies and why they matter
[ref: #sa-deps]

- `entity-protocol` — defines the repo concept, prerequisite gate, namespace registry, and memory routing rules.
- `frontmatter-protocol` — provides the canonical frontmatter extraction and tracking-field semantics used by every artifact.
- `serena-protocol` — governs memory mutation and persistence for the audit report tree.

## Strengths and trade-offs
[ref: #sa-tradeoffs]

### Strong sides
[ref: #sa-strong]

- Modular scan registry makes it easy to add or update individual checks.
- Parallel detection and independent validation reduce false positives before they reach the final report.
- Core adjudication step gives human-like judgment on ambiguous findings.
- Design checklist covers API-security design flaws that pure static analysis misses.

### Weak sides / limits
[ref: #sa-weak]

- Higher cost than a single-pass scan because of the multi-stage pipeline.
- The skill reports findings; it does not patch source code itself.
- Entity-scoped audits require a pre-existing repo card.
- Some findings may be flagged as `[NEEDS MANUAL REVIEW]` when evidence is ambiguous.

### Common pitfalls / gotchas
[ref: #sa-pitfalls]

- The screener always runs first, even when you ask for a specific vulnerability class.
- Detection scans run with a concurrency limit of six subagents across all stages.
- If a subagent fails to write its artifact, the core will re-dispatch once and fall back to inline text.
- Conditional scans from the plan are included by default unless you explicitly opt out.

## Repository layout
[ref: #sa-layout]

```text
security-audit/
├── references/           # Lazy-loaded subagent prompt library
│   ├── 00-screener.md              # Scan selection / coverage decision matrix
│   ├── 01-analysis.md              # Architecture reconnaissance
│   ├── 02-sqli.md                  # SQL / NoSQL injection
│   ├── 03-ssrf.md                  # Server-side request forgery
│   ├── 04-xss.md                   # Cross-site scripting
│   ├── 05-rce.md                   # Remote code execution
│   ├── 06-ssti.md                  # Server-side template injection
│   ├── 07-xxe.md                   # XML external entity
│   ├── 08-idor.md                  # IDOR / BOLA
│   ├── 09-jwt.md                   # JWT weakness
│   ├── 10-missingauth.md           # Missing authentication / BFLA
│   ├── 11-fileupload.md            # Insecure file upload
│   ├── 12-pathtraversal.md         # Path traversal
│   ├── 13-businesslogic.md         # Business-logic flaws
│   ├── 14-graphql.md               # GraphQL injection
│   ├── 15-hardcodedsecrets.md      # Hardcoded secrets
│   ├── 16-bopla.md                 # Broken object property level authorization
│   ├── 17-resourceconsumption.md   # Unrestricted resource consumption
│   ├── 18-inventory.md             # Improper inventory management
│   ├── 19-unsafeapiconsumption.md  # Unsafe consumption of APIs
│   ├── 20-misconfiguration.md      # Security misconfiguration
│   ├── 21-backdoors.md             # Deliberate malicious code / backdoors
│   ├── 22-obfuscation.md           # Obfuscated code
│   ├── 23-dependencies.md          # Supply chain / dependency risks
│   ├── 24-jvm-anomalies.md         # Kotlin/Java JVM-specific anomalies
│   ├── 90-design-checklist.md      # API Security design checklist assessment
│   ├── 98-validator.md             # Independent finding validation
│   ├── 99-report.md                # Final consolidated report generation
│   ├── execution-protocol.md       # Detection dispatch playbook
│   └── registry.md                 # Single scan registry (meta + detection layers)
├── README.md                # Human overview (this file)
└── SKILL.md              # Agent entry point: thin-core orchestration
```

## Reference overview
[ref: #sa-refs]

| File | What it covers |
|------|----------------|
| `references/00-screener.md` | Diagnostic screener that decides which scans apply |
| `references/01-analysis.md` | Architecture reconnaissance |
| `references/02-sqli.md` | SQL / NoSQL injection detection |
| `references/03-ssrf.md` | Server-side request forgery detection |
| `references/04-xss.md` | Cross-site scripting detection |
| `references/05-rce.md` | Remote code execution detection |
| `references/06-ssti.md` | Server-side template injection detection |
| `references/07-xxe.md` | XML external entity detection |
| `references/08-idor.md` | Insecure direct object reference / BOLA detection |
| `references/09-jwt.md` | JWT weakness detection |
| `references/10-missingauth.md` | Missing authentication / broken access control detection |
| `references/11-fileupload.md` | Insecure file upload detection |
| `references/12-pathtraversal.md` | Path traversal detection |
| `references/13-businesslogic.md` | Business-logic flaw detection |
| `references/14-graphql.md` | GraphQL injection detection |
| `references/15-hardcodedsecrets.md` | Hardcoded secret detection |
| `references/16-bopla.md` | Broken object property level authorization detection |
| `references/17-resourceconsumption.md` | Unrestricted resource consumption detection |
| `references/18-inventory.md` | Improper inventory management detection |
| `references/19-unsafeapiconsumption.md` | Unsafe consumption of APIs detection |
| `references/20-misconfiguration.md` | Security misconfiguration detection |
| `references/21-backdoors.md` | Deliberate malicious code / backdoor detection |
| `references/22-obfuscation.md` | Obfuscated code detection |
| `references/23-dependencies.md` | Supply chain / dependency risk detection |
| `references/24-jvm-anomalies.md` | Kotlin/Java JVM-specific anomaly detection |
| `references/90-design-checklist.md` | API Security design checklist assessment |
| `references/98-validator.md` | Independent validation of findings against source |
| `references/99-report.md` | Consolidated final report generation |
| `references/execution-protocol.md` | Detection dispatch playbook |
| `references/registry.md` | Single scan registry: layers, OWASP mapping, applicability, tag families |

## Important conventions / gotchas
[ref: #sa-conventions]

- An entity-scoped audit needs an existing card at `.serena/memories/repos/<entity>/overview` (create it via `repo-audit` first).
- This skill reports findings; it does not patch source code itself.
- The screener always runs first, even when you ask for a specific vulnerability class.
- Detection scans run in parallel batches of up to six subagents across all stages; the design checklist runs alongside them.
- Every finding is independently validated; the core agent personally re-checks doubtful ones.
- All audit artifacts are persisted with `just serena-checkpoint`.
- All timestamps use UTC ISO 8601 format.
