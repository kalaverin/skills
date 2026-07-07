# security-audit

Source-code security assessment (SAST) skill aligned with the OWASP API Security Top 10 2023.

## What this skill does

`security-audit` orchestrates a security assessment workflow. It does not perform detection itself; instead, it provides a mandatory screener, architecture reconnaissance instructions, and 24 focused detection playbooks that are consumed by `coder` subagents. The skill defines:

- Where audit artifacts are written (`.serena/memories/audit/`).
- How the final consolidated report is produced and persisted.
- Severity ranking and coverage heat mapping against OWASP API Security Top 10 2023.

## When to use it

Use this skill when the request involves:

- Security audit, SAST scan, vulnerability assessment, or code security review.
- Penetration-test style source review.
- OWASP API 2023 coverage.
- Specific vulnerability-class searches such as SQLi, XSS, IDOR, SSRF, JWT, BOLA, BOPLA, misconfiguration, etc.

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
│   ├── 90-design-checklist.md      # Shieldfy design checklist assessment
│   └── 99-report.md                # Final consolidated report generation
└ SKILL.md                          # Skill entry point, triggers, activation table, workflow
```

## How to use this skill

1. Open `SKILL.md` for the master workflow and activation table.
2. Run the mandatory screener (`references/00-screener.md`) to decide which detection playbooks apply.
3. Perform architecture reconnaissance (`references/01-analysis.md`).
4. Dispatch up to five `coder` subagents in parallel with the selected detection playbooks (`references/02-*.md` through `references/24-*.md`).
5. Run the design checklist assessment (`references/90-design-checklist.md`).
6. Consolidate findings into the final report (`references/99-report.md`).
7. Write the report under `.serena/memories/audit/` and persist with `just agent-memory-commit`.

## Reference index

| File | Vulnerability / Topic |
|------|-----------------------|
| `references/00-screener.md` | Scan selection and coverage decision matrix |
| `references/01-analysis.md` | Architecture reconnaissance |
| `references/02-sqli.md` | SQL / NoSQL injection |
| `references/03-ssrf.md` | Server-side request forgery |
| `references/04-xss.md` | Cross-site scripting |
| `references/05-rce.md` | Remote code execution |
| `references/06-ssti.md` | Server-side template injection |
| `references/07-xxe.md` | XML external entity |
| `references/08-idor.md` | IDOR / BOLA |
| `references/09-jwt.md` | JWT weakness |
| `references/10-missingauth.md` | Missing authentication / BFLA |
| `references/11-fileupload.md` | Insecure file upload |
| `references/12-pathtraversal.md` | Path traversal |
| `references/13-businesslogic.md` | Business-logic flaws |
| `references/14-graphql.md` | GraphQL injection |
| `references/15-hardcodedsecrets.md` | Hardcoded secrets |
| `references/16-bopla.md` | Broken object property level authorization |
| `references/17-resourceconsumption.md` | Unrestricted resource consumption |
| `references/18-inventory.md` | Improper inventory management |
| `references/19-unsafeapiconsumption.md` | Unsafe consumption of APIs |
| `references/20-misconfiguration.md` | Security misconfiguration |
| `references/21-backdoors.md` | Deliberate malicious code / backdoors |
| `references/22-obfuscation.md` | Obfuscated code |
| `references/23-dependencies.md` | Supply chain / dependency risks |
| `references/24-jvm-anomalies.md` | Kotlin/Java JVM-specific anomalies |
| `references/90-design-checklist.md` | Shieldfy design checklist |
| `references/99-report.md` | Final consolidated report |

## Conventions

- `SKILL.md` is the single entry point.
- The mandatory screener decides which of the 24 detection playbooks apply.
- Detection subagents are `coder` type and run in parallel batches of up to 5.
- Final reports are written under `.serena/memories/audit/`.
- Reports must be persisted with `just agent-memory-commit`.
- Risk framework: OWASP API Security Top 10 2023.
