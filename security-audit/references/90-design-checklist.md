---
subject: "Design-level API security checklist assessment reference; single-subagent `PASS`/`FAIL`/`NOT_APPLICABLE`/`NEEDS_MANUAL_REVIEW` prompt, scope routing versus technical scans 02–24, OWASP API 2023 alignment table, Shieldfy items spanning authentication, access, OAuth incl. `PKCE`/`DPoP`, input, processing, output, CI/CD, monitoring, AI/LLM controls, execution classification, output template, reminders, references."
index:
  - anchor: design-checklist
    what: "Design-level, cross-cutting security assessment role based on the Shieldfy API Security Checklist — one read-only subagent evaluates policy, architecture, and process controls untied to single code locations, supplementing technical scans 02–24 — gated on the architecture report."
    problem: "API may pass every code-level scan while lacking documented rate-limit policy, secret-rotation process, or monitoring design, and piecemeal review of forty-plus controls without one orchestrated sweep leaves governance blind spots until audit; cross-cutting coverage, checklist inventory, evidence hunt, architecture context, readiness, operational discipline, organizational posture."
    use_when: "Design-checklist scan selected by the screener; `{{ REPORTS_ROOT }}/01_architecture.md` exists; full policy-level assessment must run end to end."
    avoid_when: "Architecture report missing — run analysis first; only conceptual Shieldfy knowledge is needed, not execution."
    expected: "Every checklist item classified, with governance findings written into one consolidated design report."
  - anchor: design-checklist-scope-routing
    what: "Boundary table routing code-level gaps — rate limiting, CORS, headers, hardcoded secrets, missing authentication, injection classes, business logic, third-party trust — to technical references 02–24, reserving `FAIL` here for controls with no evidence anywhere."
    problem: "Design reviewer flags code-level weaknesses already owned by technical modules, so identical flaw surfaces twice in final reports and policy-only gaps drown in duplicated noise; routing boundaries, scan ownership, overlap discipline, channel separation, report hygiene, misrouted findings, policy-versus-code split."
    use_when: "A gap candidate emerges during design assessment; verdict needed on whether this file reports it or another scan owns it; triaging overlap between policy absence and implementation weakness."
    avoid_when: "Scan selection itself — `00-screener.md` owns that; recon and architecture work belong to `01-analysis.md`; code-level gap hunting belongs to sibling scan modules 02–24."
    expected: "Each candidate lands in exactly one report — policy absences stay here, code weaknesses route outward."
  - anchor: design-checklist-owasp-alignment
    what: "Alignment table mapping each checklist area — authentication, access, authorization/OAuth, input, processing, output, CI/CD, monitoring, advanced — to its primary OWASP API 2023 risk (`API1:2023` through `API10:2023`) for `FAIL` findings."
    problem: "Every failed control needs root-cause risk labeling, yet reviewers guess between authorization, resource-consumption, and misconfiguration framings or skip labeling entirely, weakening consolidated audit output; threat attribution, taxonomy tagging, mapping choice, framing consistency, report compliance, label discipline, crosswalk table."
    use_when: "Assigning risk labels to confirmed `FAIL` findings; checking which primary threat a given control area maps to; keeping taxonomy consistent across sibling reports."
    avoid_when: "CWE identifier selection — this table covers OWASP risk framing only; scan applicability decisions belong to `00-screener.md`."
    expected: "Each `FAIL` finding carries exactly one aligned OWASP tag."
  - anchor: design-checklist-mapping
    what: "Full 40-plus-item Shieldfy checklist — authentication, access, authorization/OAuth incl. `PKCE` and `DPoP`, input, processing, output, CI/CD incl. SBOM/provenance, monitoring, advanced topics incl. GraphQL, zero trust, AI/LLM controls — each with evidence definition plus file patterns and keywords."
    problem: "Policy assessment without concrete item catalog devolves into vague impressions, so obscure controls like sender-constrained tokens, entity expansion, or MCP endpoint authentication never get checked and coverage stays unverifiable; checklist canon, evidence types, keyword index, breadth guarantee, hunt list, granular probing, overlooked corners, systematic questioning."
    use_when: "Assessor needs the concrete item list with evidence pointers; searching repo and docs for policy, configuration, CI/CD, or runbook traces per control; building per-area hunt queries from keyword columns."
    avoid_when: "Routing overlaps to technical modules — see scope card; verdict definitions belong to execution card; code-level weakness hunting belongs to technical modules 02–24."
    expected: "All nine areas probed item by item with documented evidence searched for every control."
  - anchor: design-checklist-execution
    what: "Single-`coder`-subagent execution: read-only constraints, architecture context passed in, per-item evidence search, four-status classification (`PASS`, `FAIL`, `NOT_APPLICABLE`, `NEEDS_MANUAL_REVIEW`) with partial-evidence bias toward manual review, overlap dedup against technical scans, and finding write-up obligations."
    problem: "Assessment dispatched without crisp verdict rules produces inconsistent statuses, duplicated findings, and overconfident failures where proof sits outside repo reach; classification canon, ambiguity handling, evidence thresholds, subagent briefing, read-only discipline, judgment calibration, dispatch clarity, uncertainty bias."
    use_when: "Dispatching the design-assessment subagent; writing its goal, constraints, and step instructions; calibrating borderline verdicts between `FAIL` and `NEEDS_MANUAL_REVIEW`."
    avoid_when: "Scan selection belongs to `00-screener.md`; recon and architecture-report generation belong to `01-analysis.md`; item catalog lookup belongs to the mapping card."
    expected: "Subagent finishes with every item statused under consistent definitions and each `FAIL` fully argued."
  - anchor: design-checklist-output-template
    what: "Mandatory report skeleton for `{{ REPORTS_ROOT }}/90_design_checklist.md`: executive-summary status counts, per-item status table, `FAIL` finding blocks with risk/evidence/remediation, Appendix A manual-review items with uncertainty, Appendix B not-applicable items with rationale."
    problem: "Free-form reporting yields inconsistent deliverables where summary counts disagree with detail tables, manual-review items vanish without trace, and downstream consolidation cannot compare scans; report shape, tally reconciliation, template fidelity, appendix coverage, traceable uncertainty, uniform output, structural canon."
    use_when: "Writing or reviewing the final `90_design_checklist.md`; assembling summary tallies, per-item rows, verdict write-ups, and both appendices; checking deliverable completeness before closing."
    avoid_when: "Classification rules themselves — see execution card; item content belongs to mapping card; technical scan output formats live in modules 02–24."
    expected: "Deliverable matches the template exactly — counts agree with detail rows, verdict sections complete, both appendices present."
  - anchor: design-checklist-important-reminders
    what: "Closing operational reminders: read architecture report first, policy-versus-code boundary against scans 02–24, `FAIL` reserved for absent controls rather than imperfect implementations, `NEEDS_MANUAL_REVIEW` bias under doubt, write-only-to-report subagent confinement."
    problem: "Final pass without fixed wrap-up rules lets imperfect implementations get marked failed, architecture context skipped, or stray writes touch project source; closing rules, quality floor, exit discipline, audit closure, judgment restraint, scope confinement, uniform endings."
    use_when: "Finalizing the design report; double-checking status conservatism, scope restraint, and context obligations before closing the assessment."
    avoid_when: "Earlier work still open — finish classification and writing first; scan selection belongs to `00-screener.md`; technical-module routing rules live in scope card."
    expected: "Assessment closes with all reminders honored — context consumed, conservative statuses, no project files touched."
  - anchor: design-checklist-references
    what: "External link list: Shieldfy API Security Checklist repository, OWASP API Security Top 10 2023 edition page, OWASP Cheat Sheet Series, NIST `SP 800-207` Zero Trust Architecture."
    problem: "Findings and remediation advice need authoritative follow-up sources beyond distilled checklist content when deeper control detail, cheat-sheet recipes, or canonical citation is required; further reading, external canon, primary material, cited works, source integrity, zero-trust background."
    use_when: "Findings need links to canonical advisories or standards; reader wants primary checklist, OWASP, or NIST material behind summarized controls."
    avoid_when: "Assessment procedure or verdict rules — this list is follow-up reading, not procedure; routing questions belong to scope card."
    expected: "Reader reaches canonical external material for every topic this file condenses."
---

# API Security Design Checklist Assessment

[ref: #design-checklist]

You are performing a **design-level, cross-cutting** security assessment based on the [Shieldfy API Security Checklist](https://github.com/shieldfy/API-Security-Checklist). This scan looks for policy, architecture, and process gaps that are not tied to a single code location. It supplements the technical scans 02–24; it does not replace them.

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

***

## Scope and relationship to other scans
[ref: #design-checklist-scope-routing]

This checklist evaluates whether the API's **design, build, and operational policies** address common countermeasures. Do **not** duplicate findings that are better handled by the technical scans:

| If the gap is... | Route it to... |
|---|---|
| Missing or flawed code-level rate limiting, quota, or resource-consumption controls | `17_resourceconsumption.md` |
| CORS misconfiguration, missing security headers, debug mode, verbose errors, TLS issues | `20_misconfiguration.md` |
| Hardcoded secrets, API keys, or credentials in source/client code | `15_hardcodedsecrets.md` |
| Missing authentication on an endpoint or broken access control | `10_missingauth.md` |
| SQL/NoSQL injection, XSS, SSRF, RCE, XXE, SSTI, IDOR, file upload, path traversal | The corresponding `02–14` reference |
| Business-logic abuse, workflow bypass, price manipulation | `13_businesslogic.md` |
| Unsafe trust of third-party API responses | `19_unsafeapiconsumption.md` |

Report a **FAIL** in this design checklist **only** when there is **no evidence at all** that the control is addressed by policy, architecture, configuration, or process. Code-level weaknesses that already have some control in place should be left to the technical scans.

***

## OWASP API 2023 alignment
[ref: #design-checklist-owasp-alignment]

This checklist spans multiple OWASP API Security Top 10 2023 risks. Map each FAIL to the most relevant risk:

| Checklist area | Primary OWASP API 2023 risk |
|---|---|
| Authentication | API2:2023 Broken Authentication |
| Access controls, rate limiting | API4:2023 Unrestricted Resource Consumption / API5:2023 Broken Function Level Authorization |
| Authorization / OAuth | API1:2023 Broken Object Level Authorization / API5:2023 Broken Function Level Authorization |
| Input validation | API6:2023 Unrestricted Access to Sensitive Business Flows; injection risks (02–07, 14) |
| Processing | API1:2023 Broken Object Level Authorization / API3:2023 Broken Object Property Level Authorization |
| Output / headers / TLS | API8:2023 Security Misconfiguration |
| CI/CD and secrets | API8:2023 Security Misconfiguration / API10:2023 Unsafe Consumption of APIs |
| Monitoring | API8:2023 Security Misconfiguration / API9:2023 Improper Inventory Management |
| Advanced topics | API1:2023, API4:2023, API8:2023 |

Use the primary risk in the `FAIL` findings when appropriate.

***

## Checklist mapping
[ref: #design-checklist-mapping]

Evaluate every item below. For each item, look for **documented policy**, **architectural decision**, **configuration**, or **process evidence** in the repository and its docs.

### What counts as evidence

Accept any of the following as evidence of a control:

- A documented policy, decision record, or runbook.
- Configuration in code or infrastructure-as-code.
- A CI/CD job, test, or automated check.
- A clearly scoped "not applicable" rationale in docs or issues.

### 1. Authentication

| # | Checklist item | Evidence to look for | File patterns / keywords |
|---|---|---|---|
| 1.1 | Don't use Basic Auth; use standard authentication | Auth scheme declarations, middleware, docs | `Basic`, `Authorization: Basic`, `HTTPBasic`, `basic-auth` |
| 1.2 | Don't reinvent authentication, token generation, or password storage | Custom crypto/hash code, token issuance, password fields | `password_hash`, `bcrypt`, `argon2`, `scrypt`, `jwt.encode`, custom signing |
| 1.3 | Use max-retry and jail/lockout features on login | Rate-limit or lockout config, login throttling | `max_retry`, `lockout`, `throttle`, `login_attempts`, `jail` |
| 1.4 | Encrypt all sensitive data at rest and in transit | Encryption configs, TLS, database encryption flags | `TLS`, `SSL`, `encrypt`, `AES`, `at_rest`, `in_transit`, `ENCRYPTION_KEY` |

### 2. Access

| # | Checklist item | Evidence to look for | File patterns / keywords |
|---|---|---|---|
| 2.1 | Limit requests/throttling to avoid DDoS and brute-force | Gateway rate limits, WAF rules, throttling middleware | `throttle`, `rate_limit`, `Quota`, `Spike Arrest`, `429` |
| 2.2 | Use HTTPS on server side with TLS 1.2+ and secure ciphers | TLS configuration, cipher suites, certificate setup | `ssl_protocols`, `TLSv1.2`, `TLSv1.3`, `SSLCipherSuite`, `cert.pem` |
| 2.3 | Send HSTS header with SSL | HSTS config in app or reverse proxy | `Strict-Transport-Security`, `HSTS`, `max-age` |
| 2.4 | Turn off directory listings | Web server directory index settings | `autoindex`, `directory_listing`, `Indexes`, `Options Indexes` |
| 2.5 | For private APIs, allow access only from safelisted IPs/hosts | IP allowlists, network policies, ingress rules | `allow_list`, `whitelist`, `ip_allowlist`, `NetworkPolicy`, `security group` |

### 3. Authorization / OAuth

| # | Checklist item | Evidence to look for | File patterns / keywords |
|---|---|---|---|
| 3.1 | Validate `redirect_uri` server-side against an allowlist | OAuth authorization handler, redirect validation | `redirect_uri`, `redirect_uris`, `allowed_redirect_uris` |
| 3.2 | Exchange authorization codes, not tokens (`response_type=token` disallowed) | OAuth flow config, response_type handling | `response_type=code`, `response_type=token`, `implicit grant` |
| 3.3 | Use random `state` parameter to prevent CSRF in OAuth | State generation/validation in OAuth flow | `state`, `state_param`, `generate_state` |
| 3.4 | Define default scope and validate scope per application | Scope definitions, scope validation logic | `scope`, `default_scope`, `allowed_scopes`, `validate_scope` |
| 3.5 | Require PKCE for every OAuth client (OAuth 2.1 direction; implicit grant removed) | Authorization-code flow config, PKCE parameters | `code_challenge`, `code_verifier`, `code_challenge_method=S256`, OAuth 2.1 notes |
| 3.6 | Prefer sender-constrained tokens for high-value APIs (DPoP, RFC 9449) | Token binding config, DPoP proofs | `DPoP`, `dpop_jkt`, `cnf`, sender-constrained |

### 4. Input

| # | Checklist item | Evidence to look for | File patterns / keywords |
|---|---|---|---|
| 4.1 | Use proper HTTP methods; return `405` for inappropriate methods | Route definitions, method handlers, method filtering | `@app.route`, `methods=[`, `405`, `Method Not Allowed` |
| 4.2 | Validate `Accept`/`content-type`; return `406` for unsupported formats | Content negotiation middleware, accepted types | `Accept`, `application/json`, `406`, `Not Acceptable` |
| 4.3 | Validate `content-type` of posted data | Body parser configuration, content-type checks | `content-type`, `multipart/form-data`, `application/json` |
| 4.4 | Validate user input to avoid XSS, SQLi, RCE, etc. | Input validation framework, sanitization, parameterized queries | `validate`, `sanitize`, `param`, `schema`, `pydantic`, `validator` |
| 4.5 | Don't put credentials, passwords, tokens, or API keys in URLs | Route patterns, query parameters, logs | `password=`, `token=`, `api_key=`, `credentials` in URL paths |
| 4.6 | Use only server-side encryption | Encryption operations in client vs server code | `crypto.subtle` in frontend, `window.crypto`, server-side `encrypt` |
| 4.7 | Use an API gateway for caching, rate limiting, and dynamic deployment | Gateway configuration, deployment docs | `api-gateway`, `kong`, `nginx`, `apigee`, `aws apigateway`, `cache` |

### 5. Processing

| # | Checklist item | Evidence to look for | File patterns / keywords |
|---|---|---|---|
| 5.1 | All endpoints protected behind authentication | Global auth middleware, route guards, public-exceptions list | `authenticate`, `require_auth`, `@login_required`, `public_routes` |
| 5.2 | Avoid user-owned resource IDs; prefer `/me/orders` | Resource ID patterns in routes | `/user/{id}`, `/users/{id}/orders`, `/me/`, `current_user` |
| 5.3 | Don't auto-increment IDs; use UUID | ID generation strategy, schema definitions | `auto_increment`, `serial`, `uuid`, `UUID`, `bigint` |
| 5.4 | If parsing XML, disable entity parsing to avoid XXE | XML parser configuration | `xml.etree`, `lxml`, `resolve_entities`, `no_network`, `XXE` |
| 5.5 | If parsing XML/YAML with anchors/refs, disable entity expansion | YAML/XML loader settings | `yaml.safe_load`, `Loader`, `entity_expansion`, `Billion Laughs` |
| 5.6 | Use a CDN for file uploads | Upload architecture docs, CDN references | `cdn`, `s3`, `cloudfront`, `file_upload`, `blob storage` |
| 5.7 | Use workers/queues for heavy data processing | Background task configuration | `celery`, `rq`, `bull`, `sidekiq`, `worker`, `queue`, `async job` |
| 5.8 | Turn DEBUG mode OFF in production | Environment configs, debug flags | `DEBUG=True`, `debug=True`, `NODE_ENV=development`, `APP_ENV` |
| 5.9 | Use non-executable stacks when available | Compiler/linker flags, runtime settings | `NX bit`, `DEP`, `noexecstack`, `stack_canary`, `ASLR` |

### 6. Output

| # | Checklist item | Evidence to look for | File patterns / keywords |
|---|---|---|---|
| 6.1 | Send `X-Content-Type-Options: nosniff` | Security header middleware/proxy config | `X-Content-Type-Options`, `nosniff` |
| 6.2 | Send `X-Frame-Options: deny` | Frame options header | `X-Frame-Options`, `DENY`, `SAMEORIGIN` |
| 6.3 | Send `Content-Security-Policy: default-src 'none'` | CSP header or config | `Content-Security-Policy`, `default-src` |
| 6.4 | Remove fingerprinting headers (`X-Powered-By`, `Server`, etc.) | Header stripping config | `X-Powered-By`, `Server`, `X-AspNet-Version`, `server_tokens` |
| 6.5 | Force `content-type` on responses | Response serialization config | `content-type`, `JSONResponse`, `Response(media_type=)` |
| 6.6 | Don't return overly specific error messages to clients | Error handler policy, exception response shape | `traceback`, `stack`, `Internal server error`, `error handler` |
| 6.7 | Don't return credentials, passwords, or security tokens | Response schemas, DTOs, serialization rules | `password`, `token`, `secret`, `api_key` in responses |
| 6.8 | Return proper HTTP status codes | Status code usage in handlers | `200`, `201`, `400`, `401`, `403`, `404`, `405`, `500` |

### 7. CI/CD

| # | Checklist item | Evidence to look for | File patterns / keywords |
|---|---|---|---|
| 7.1 | Audit design/implementation with unit/integration test coverage | Test config, coverage thresholds | `pytest`, `jest`, `coverage`, `codecov`, `.github/workflows` |
| 7.2 | Use code review process and disregard self-approval | Branch protection, review policy | `CODEOWNERS`, `require review`, `branch protection`, `pull_request` |
| 7.3 | Statically scan all components (including dependencies) before production | AV/SAST pipeline steps | `snyk`, `trivy`, `clamav`, `virus`, `static scan` |
| 7.4 | Continuously run security tests (SAST/DAST) | CI security job definitions | `sast`, `dast`, `security scan`, `codeql`, `semgrep` |
| 7.5 | Check dependencies and OS for known vulnerabilities | Dependency scanning, SBOM | `npm audit`, `pip audit`, `dependabot`, `renovate`, `CVE` |
| 7.6 | Design a rollback solution for deployments | Deployment docs, rollback procedures | `rollback`, `blue-green`, `canary`, `deployment strategy` |
| 7.7 | Generate an SBOM and verify dependency provenance (SLSA, Sigstore, trusted publishing) | SBOM artifacts, provenance verification jobs, publish pipeline auth | `sbom`, `cyclonedx`, `spdx`, `slsa`, `cosign`, `npm audit signatures`, trusted publishing |

### 8. Monitoring

| # | Checklist item | Evidence to look for | File patterns / keywords |
|---|---|---|---|
| 8.1 | Use centralized logging for all services/components | Logging architecture, log aggregation | `elk`, `fluentd`, `cloudwatch`, `splunk`, `centralized logging` |
| 8.2 | Use agents to monitor traffic, errors, requests, and responses | APM agents, tracing, monitoring config | `apm`, `datadog`, `newrelic`, `opentelemetry`, `agent` |
| 8.3 | Use alerts for SMS, Slack, email, Telegram, Kibana, CloudWatch, etc. | Alerting rules, notification channels | `alertmanager`, `pagerduty`, `slack webhook`, `sns`, `alert` |
| 8.4 | Ensure sensitive data is not logged | Log filtering/masking policy | `mask`, `redact`, `sanitize logs`, `PII`, `credit card`, `password` |
| 8.5 | Use IDS/IPS to monitor API requests and instances | Network security controls | `IDS`, `IPS`, `waf`, `intrusion detection`, `firewall` |

### 9. Advanced topics

#### 9.1 Rate limiting and abuse prevention

| # | Checklist item | Evidence to look for | File patterns / keywords |
|---|---|---|---|
| 9.1.1 | Implement sliding-window rate limiting per API key and IP | Rate-limit policy, sliding window config | `sliding window`, `rate limit`, `per ip`, `per api key` |
| 9.1.2 | Use exponential backoff for repeated failed authentication | Backoff policy on auth failures | `exponential backoff`, `retry-after`, `auth failure` |
| 9.1.3 | Implement CAPTCHA or proof-of-work after suspicious activity | Anti-automation controls | `captcha`, `recaptcha`, `proof of work`, `challenge` |
| 9.1.4 | Monitor and alert on unusual API usage patterns | Anomaly detection, usage alerts | `anomaly`, `usage pattern`, `baseline`, `alert on spikes` |

#### 9.2 GraphQL-specific security

| # | Checklist item | Evidence to look for | File patterns / keywords |
|---|---|---|---|
| 9.2.1 | Disable introspection in production | GraphQL server config | `introspection`, `graphql`, `apollo`, `graphene`, `disable introspection` |
| 9.2.2 | Implement query depth limiting | Query depth config | `max_depth`, `query depth`, `depth limit` |
| 9.2.3 | Use query cost analysis to prevent resource exhaustion | Cost analysis middleware | `query cost`, `complexity`, `cost analysis` |
| 9.2.4 | Whitelist allowed queries in production when possible | Persisted queries, allowlist | `persisted queries`, `query whitelist`, `allowed_queries` |

#### 9.3 Secrets management

| # | Checklist item | Evidence to look for | File patterns / keywords |
|---|---|---|---|
| 9.3.1 | Rotate API keys and secrets on a regular schedule | Key rotation policy/process | `rotate`, `rotation policy`, `key rotation`, `secret rotation` |
| 9.3.2 | Use HSM for signing operations | Signing infrastructure docs | `HSM`, `kms`, `cloudhsm`, `signing key` |
| 9.3.3 | Implement secret scanning in CI/CD pipelines | Secret scanning job | `secret scanning`, `gitleaks`, `trufflehog`, `detect-secrets` |
| 9.3.4 | Never commit secrets; use environment variables or secret managers | Secret storage pattern | `.env`, `secrets manager`, `vault`, `aws secretsmanager`, `process.env` |

#### 9.4 Zero trust architecture

| # | Checklist item | Evidence to look for | File patterns / keywords |
|---|---|---|---|
| 9.4.1 | Implement mTLS for service-to-service communication | mTLS config, client certificates | `mTLS`, `client_cert`, `mutual TLS`, `service mesh` |
| 9.4.2 | Validate all requests, even from internal services | Internal auth policy | `internal auth`, `service account`, `inter-service`, `zero trust` |
| 9.4.3 | Use short-lived tokens with automatic refresh | Token TTL/refresh policy | `TTL`, `RTTL`, `refresh token`, `short-lived` |
| 9.4.4 | Implement request signing for sensitive operations | Request signature config | `request signing`, `signature`, `HMAC`, `signed request` |

#### 9.5 AI / LLM API controls

| # | Checklist item | Evidence to look for | File patterns / keywords |
|---|---|---|---|
| 9.5.1 | Enforce per-user quotas and cost caps on LLM-backed endpoints (OWASP LLM10:2025) | Quota/rate config on AI endpoints, spend alerts | `max_tokens`, `quota`, `spend alert`, LLM10, `rate_limit` on completion routes |
| 9.5.2 | Treat model output as untrusted input in downstream design (OWASP LLM05:2025) | Output-validation contract, schema checks before sinks | `model_validate`, output schema, LLM05, prompt-injection notes |
| 9.5.3 | Inventory MCP servers and agent tooling; no unauthenticated MCP endpoints (OWASP MCP09:2025) | MCP config inventory, auth on `/sse` and `/mcp` transports | `.mcp.json`, `mcp.json`, `mcpServers`, MCP09 |

***

## Execution
[ref: #design-checklist-execution]

Perform this assessment with a single `coder` subagent. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` as context.

> **Subagent constraints**: Investigate only. Do not modify project source code, configuration files, tests, or build scripts. Do not open pull requests or run destructive commands. Write only under `{{ REPORTS_ROOT }}/`.

Give the subagent these instructions:

> **Goal**: Evaluate the API against the Shieldfy API Security Checklist and write the results to `{{ REPORTS_ROOT }}/90_design_checklist.md`.
>
> **Constraint**: Read-only. Do not modify source code, commit changes, or open pull requests. Write only under `{{ REPORTS_ROOT }}/`.
>
> **Context**: Read `{{ REPORTS_ROOT }}/01_architecture.md` first to understand the tech stack, frameworks, deployment topology, and existing controls.
>
> **Steps**:
>
> 1. For each checklist item in sections 1–9, determine whether there is **policy, architectural, configuration, or process evidence** that the control is addressed.
>
> 2. Assign one of the following statuses:
>    - `PASS` — Evidence exists that the control is addressed by design or process.
>    - `FAIL` — No evidence exists that the control is addressed at all.
>    - `NOT_APPLICABLE` — The control does not apply to this API (explain why).
>    - `NEEDS_MANUAL_REVIEW` — Evidence is incomplete or ambiguous; a human must decide.
>
> 3. If a `FAIL` overlaps with a technical scan (02–24), do **not** duplicate it here unless the gap is purely at the policy/design level. For example:
>    - A missing rate-limit policy → report here as `FAIL`.
>    - A flawed code-level rate limit → leave to `17_resourceconsumption.md`.
>    - A missing CORS policy → report here as `FAIL`.
>    - A CORS misconfiguration in code → leave to `20_misconfiguration.md`.
>    - Hardcoded secrets in source → leave to `15_hardcodedsecrets.md`.
>    - Missing endpoint authentication → leave to `10_missingauth.md`.
>
> 4. For every `FAIL`, write a short finding with:
>    - **Risk**: Why the missing control matters.
>    - **Evidence**: What you searched and what you did not find.
>    - **Remediation**: Concrete design, process, or configuration change.
>
> 5. Write the final report to `{{ REPORTS_ROOT }}/90_design_checklist.md` using the exact output template below.

### Classification guidance

Use these definitions consistently:

- `PASS` — Policy, configuration, or process evidence exists. The control is addressed at the design level even if the implementation could be improved.
- `FAIL` — No evidence of the control exists anywhere in architecture docs, configuration, source, CI/CD, or runbooks.
- `NOT_APPLICABLE` — The API type, deployment model, or tech stack makes the item irrelevant (e.g., no OAuth flows, no GraphQL surface, no file uploads).
- `NEEDS_MANUAL_REVIEW` — Evidence is partial, split across repositories, or controlled by an external system (e.g., a corporate WAF or cloud account policy) that cannot be verified from this repo alone.

When evidence is partial, prefer `NEEDS_MANUAL_REVIEW` over `FAIL` unless the gap is clearly complete.

***

## Output template
[ref: #design-checklist-output-template]

Write `{{ REPORTS_ROOT }}/90_design_checklist.md` using exactly this structure:

```markdown
# API Security Design Checklist Results: [Project Name]

## Executive Summary

| Status | Count |
|---|---|
| PASS | N |
| FAIL | N |
| NOT_APPLICABLE | N |
| NEEDS_MANUAL_REVIEW | N |
| **Total items assessed** | **N** |

## Design Checklist Results

| Section | Item | Status | Evidence / Notes |
|---|---|---|---|
| 1. Authentication | 1.1 Don't use Basic Auth | PASS / FAIL / NOT_APPLICABLE / NEEDS_MANUAL_REVIEW | [file/links or reason] |
| 1. Authentication | 1.2 Use standard auth/token/password libraries | ... | ... |
| ... | ... | ... | ... |

## Findings

### [FAIL] [Short finding title]

- **Checklist item**: [section number and title]
- **Risk**: [Why the missing control matters]
- **Evidence**: [What was searched and what was not found]
- **Remediation**: [Concrete design/process/configuration change]

[Repeat for every FAIL]

## Appendix A: Items Requiring Manual Review

| # | Section | Item | Uncertainty | Suggested review |
|---|---|---|---|---|
| 1 | ... | ... | ... | ... |

## Appendix B: Not Applicable Items

| # | Section | Item | Rationale |
|---|---|---|---|
| 1 | ... | ... | ... |
```

***

## Important reminders
[ref: #design-checklist-important-reminders]

- Read `{{ REPORTS_ROOT }}/01_architecture.md` before assessing any item.
- This is a **policy/design** scan. Do not re-report code-level vulnerabilities already covered by scans 02–24.
- `FAIL` items should reflect absent controls, not imperfect implementations.
- When in doubt, classify as `NEEDS_MANUAL_REVIEW` rather than `FAIL` or `PASS`.
- The subagent must only write `{{ REPORTS_ROOT }}/90_design_checklist.md` and must not modify any project source code or configuration.

***

## References
[ref: #design-checklist-references]

- Shieldfy API Security Checklist: https://github.com/shieldfy/API-Security-Checklist
- OWASP API Security Top 10 2023: https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/
- NIST SP 800-207 Zero Trust Architecture: https://csrc.nist.gov/publications/detail/sp/800-207/final
