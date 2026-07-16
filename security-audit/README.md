# security-audit

Runs a source-code security assessment aligned with the OWASP API Security Top 10 2023.

## What it does

This skill orchestrates a SAST-style audit of your codebase.
It starts with architecture reconnaissance and a screener that decides which vulnerability scans are relevant.
Then it dispatches focused detection subagents for up to twenty-four vulnerability classes.
Findings are validated against source code, a design checklist is run, and everything is consolidated into a final report stored in Serena memory.

## When it activates

Activates when you ask for a security audit, SAST scan, vulnerability assessment, code security review, penetration-test style review, OWASP API 2023 coverage, or a specific vulnerability class.

Example prompts:

- "Run a security audit on the payment service."
- "Scan this repo for SQL injection and SSRF."
- "Do an OWASP API Top 10 assessment."
- "Аудит безопасности сервиса заказов."

## How to use it

Tell the agent what you want audited.
You can scope the audit to a single entity that already has an entity card, or run a project-level audit.
The agent creates a report directory, runs the screener, launches the selected scans in parallel, validates the results, and writes the final report.
You do not need to pick individual scans yourself.

## What it produces

- An audit manifest under `.serena/memories/audit/<entity_or_project>/<suffix>/manifest.md`.
- Architecture reconnaissance notes.
- A scan plan listing the selected vulnerability checks.
- Per-scan module reports, for example `02_sqli.md`, `03_ssrf.md`, `08_idor.md`.
- A design checklist assessment.
- A consolidated final report at `report.md` ranked by severity and impact.

## Repository layout

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
│   └── 99-report.md                # Final consolidated report generation
└── SKILL.md              # Agent entry point: manifest, triggers, and routing index
```

## Reference overview

| File | What it covers |
|------|----------------|
| `references/00-screener.md` | Diagnostic screener that decides which scans apply. |
| `references/01-analysis.md` | Architecture reconnaissance. |
| `references/02-sqli.md` | SQL / NoSQL injection detection. |
| `references/03-ssrf.md` | Server-side request forgery detection. |
| `references/04-xss.md` | Cross-site scripting detection. |
| `references/05-rce.md` | Remote code execution detection. |
| `references/06-ssti.md` | Server-side template injection detection. |
| `references/07-xxe.md` | XML external entity detection. |
| `references/08-idor.md` | Insecure direct object reference / BOLA detection. |
| `references/09-jwt.md` | JWT weakness detection. |
| `references/10-missingauth.md` | Missing authentication / broken access control detection. |
| `references/11-fileupload.md` | Insecure file upload detection. |
| `references/12-pathtraversal.md` | Path traversal detection. |
| `references/13-businesslogic.md` | Business-logic flaw detection. |
| `references/14-graphql.md` | GraphQL injection detection. |
| `references/15-hardcodedsecrets.md` | Hardcoded secret detection. |
| `references/16-bopla.md` | Broken object property level authorization detection. |
| `references/17-resourceconsumption.md` | Unrestricted resource consumption detection. |
| `references/18-inventory.md` | Improper inventory management detection. |
| `references/19-unsafeapiconsumption.md` | Unsafe consumption of APIs detection. |
| `references/20-misconfiguration.md` | Security misconfiguration detection. |
| `references/21-backdoors.md` | Deliberate malicious code / backdoor detection. |
| `references/22-obfuscation.md` | Obfuscated code detection. |
| `references/23-dependencies.md` | Supply chain / dependency risk detection. |
| `references/24-jvm-anomalies.md` | Kotlin/Java JVM-specific anomaly detection. |
| `references/90-design-checklist.md` | API Security design checklist assessment. |
| `references/99-report.md` | Consolidated final report generation. |

## Important conventions / gotchas

- Requires the `project-audit` skill automatically.
- An entity-scoped audit needs an existing card at `.serena/memories/entities/<entity>`.
- This skill reports findings; it does not patch source code itself.
- The screener always runs first, even when you ask for a specific vulnerability class.
- Detection scans run in parallel batches of up to five.
- All audit artifacts are persisted with `just serena-checkpoint`.
- All timestamps use UTC ISO 8601 format.
