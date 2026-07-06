# SAST Scan Screener

[ref: #screener]

You are the entry-point diagnostic for a SAST audit. Your job is to study the
target codebase and decide which of the available vulnerability scans must run.
Do not perform the scans yourself; produce a rigorous, justified plan.

## Table of contents

- [Input](#input)
- [Coverage decision matrix](#coverage-decision-matrix)
- [OWASP API Security Top 10 2023 mapping](#owasp-api-security-top-10-2023-mapping)
- [Cross-mapped injection coverage](#cross-mapped-injection-coverage)
- [Per-risk trigger expansion](#per-risk-trigger-expansion)
- [Procedure](#procedure)
- [Output](#output)
- [Important reminders](#important-reminders)

## Input

Read `{{ REPORTS_ROOT }}/01_architecture.md`. If it does not exist, read
`references/01-analysis.md` and run the analysis phase first to create it, then
continue.

## Coverage decision matrix

Use the architecture findings to map the technology stack to scans. The default
rule is: **if the corresponding technology or feature is present, the scan is
mandatory.** Do not omit a scan unless you can explicitly justify why the
project has zero exposure.

| Scan | Reference | Trigger condition |
|---|---|---|
| Codebase analysis | `references/01-analysis.md` | Always required first if `{{ REPORTS_ROOT }}/01_architecture.md` is missing |
| SQL injection | `references/02-sqli.md` | Relational database usage; raw SQL / ORM raw methods; query builders with string concatenation; stored procedures with dynamic SQL; any SQL sink reachable from request or third-party data |
| SSRF | `references/03-ssrf.md` | Outbound HTTP/TCP/DNS/subprocess network calls, especially fetching remote resources from user-supplied URLs; webhooks; file fetch from URL; URL preview; custom SSO; cloud/Kubernetes/Docker metadata access |
| XSS | `references/04-xss.md` | Web frontend, server-side templates, DOM rendering, or any rendered output that includes user/ third-party data; reflected, stored, or DOM-based contexts; rich-text rendering |
| RCE | `references/05-rce.md` | OS command execution, `eval`/`exec`, deserialization, dynamic loading, unsafe serialization (pickle/yaml/XML/JSON), or code-generation from user/ third-party input |
| SSTI | `references/06-ssti.md` | Server-side template engine in use, especially when user/ third-party input reaches template rendering |
| XXE | `references/07-xxe.md` | XML parsing anywhere in the project, including SOAP, SAML, Office documents, SVG, RSS, configuration files, or dependency-mediated XML processing |
| IDOR / BOLA | `references/08-idor.md` | Authenticated endpoints that access objects by user-supplied IDs, UUIDs, slugs, keys, VINs, document keys, or any object reference; includes GraphQL mutations and bulk/batch object operations |
| JWT | `references/09-jwt.md` | JWT tokens used for authentication or authorization; custom token parsing; JWK/JWKS handling; token refresh/validation logic; `alg=none` or weak-signature risks |
| Missing auth / BFLA | `references/10-missingauth.md` | Authentication endpoints exist (login, register, forgot/reset password, token refresh); JWT/session/API-key auth is used; role-based or authenticated endpoints exist; admin/sensitive functions are present; mixed regular/admin path prefixes |
| File upload | `references/11-fileupload.md` | File receive/upload endpoints; image/document/video processing; archive extraction; MIME-type validation or path traversal around uploads |
| Path traversal | `references/12-pathtraversal.md` | File-system reads/writes with dynamic paths; archive extraction; static file serving; path concatenation without normalization |
| Business logic | `references/13-businesslogic.md` | Domain workflows with financial, entitlement, state-machine, posting/voting/booking/purchase, limited-stock, auction, transfer, withdrawal, referral/loyalty, or any flow whose automated abuse could harm the business |
| GraphQL injection | `references/14-graphql.md` | GraphQL server, GraphQL forwarding/proxy code, schema stitching, federation, or GraphQL batching |
| Hardcoded secrets | `references/15-hardcodedsecrets.md` | Client-side code, mobile apps, frontend bundles, public config, source repositories, CI/CD files, or infrastructure-as-code with embedded credentials |
| Broken Object Property Level Authorization (BOPLA) | `references/16-bopla.md` | Object serialization, auto-binding, mass-assignment, PATCH/partial updates, request fields that override read-only/sensitive properties, or generic serializers returning whole objects |
| Unrestricted Resource Consumption | `references/17-resourceconsumption.md` | Missing rate limits; unbounded pagination/array/string/payload params; file uploads without size limits; no execution timeouts / memory / CPU / process / file-descriptor limits; paid third-party integrations (SMS/email/phone/biometrics); GraphQL batching; expensive-operation throttling missing; serverless/container without resource limits |
| Improper Inventory Management | `references/18-inventory.md` | Multiple API versions; undocumented endpoints; debug endpoints; non-production hosts; missing/outdated OpenAPI/GraphQL schemas; microservices/serverless functions; unmonitored third-party integrations; feature flags gating admin/endpoints; production data in non-production deployments |
| Unsafe Consumption of APIs | `references/19-unsafeapiconsumption.md` | Outbound third-party HTTP/API consumption, webhooks, package-manager/registry calls, disabled TLS validation, blind redirect following, or no timeouts/limits on external calls |
| Security Misconfiguration | `references/20-misconfiguration.md` | Missing security headers, CORS issues, TLS gaps, verbose errors, insecure defaults, debug mode, unnecessary HTTP verbs, cloud/container/IaC configs, outdated components, logging with placeholder expansion/JNDI, default credentials, or inconsistent HTTP-chain request handling |
| Backdoors / deliberate malicious code | `references/21-backdoors.md` | Dynamic loading, reflective invocation, runtime string decryption, environment triggers, time bombs, dead-code activation, anti-debug checks, DGA patterns, beaconing/C2 callbacks, or any deliberate-implant indicators |
| Obfuscated code | `references/22-obfuscation.md` | Base64/hex concatenation, control-flow flattening, opaque predicates, string decryption loops, encrypted payloads, identifier mangling with dynamic access, or other obfuscation hiding behavior |
| Supply chain / dependencies | `references/23-dependencies.md` | Third-party dependencies; package manifests; lockfiles; registry configuration; dependency-update cadence; typosquatting, dependency confusion, known CVEs, abandoned packages, suspicious maintainer changes, or compromised registry packages |
| API Security design checklist | `references/90-design-checklist.md` | Any API, web service, or backend with HTTP interfaces; evaluates policy, architecture, and process controls from the Shieldfy API Security Checklist |

## OWASP API Security Top 10 2023 mapping

The table below maps each OWASP API Security Top 10 2023 risk to the primary
scan(s) that cover it and the concrete indicators that should select those
scans. Select the scan if **any** indicator in the row is true.

| OWASP 2023 risk | Primary scan(s) | Trigger indicators (select scan if any are true) |
| --- | --- | --- |
| API1:2023 Broken Object Level Authorization | `08-idor.md` | Any endpoint accepts an object identifier (ID, UUID, slug, VIN, document key, sequential integer, or generic string) from the client in path, query, header, or payload and accesses a data source; GraphQL mutations or batch operations acting on object IDs; server relies on client-supplied IDs because it does not fully track client state. |
| API2:2023 Broken Authentication | `09-jwt.md`, `10-missingauth.md` | Authentication endpoints exist (login, register, forgot/reset password, token refresh); JWT/session/API-key/tokens are used; password reset/recovery flows exist; MFA is optional or absent; microservices call each other; brute-force/lockout/CAPTCHA/weak-password protections are missing; sensitive operations lack re-authentication; tokens sent in URLs or stored insecurely; unsigned/weakly signed JWTs accepted; JWT expiration not validated; plain-text or weakly hashed passwords; weak encryption keys. |
| API3:2023 Broken Object Property Level Authorization | `16-bopla.md` | Generic serializers (`to_json`, `model_to_dict`, `to_string`) returning whole objects; request bodies bound to internal objects or variables (mass assignment); PATCH/partial updates; GraphQL resolvers returning whole objects; schema-based response validation missing; API exposes sensitive properties or allows changing/adding/deleting sensitive properties the user should not access. |
| API4:2023 Unrestricted Resource Consumption | `17-resourceconsumption.md` | No rate limits; unbounded pagination/array/string/payload params; file uploads without max size; missing execution timeouts, max allocable memory, max file descriptors, max processes; third-party API integrations charged per request (SMS/email/phone/biometrics) without spending limit or billing alert; GraphQL batching or multiple operations in a single client request; serverless/container without resource limits; expensive operations without throttling. |
| API5:2023 Broken Function Level Authorization | `10-missingauth.md` | Role/permission model exists; admin endpoints exist; endpoints with mixed regular/admin functions under the same path prefix; HTTP method switching possible (`GET` → `DELETE`/`PUT`/`PATCH`); guessed admin URLs or cross-group endpoint guessing (e.g. `/api/users/export_all`); complex user hierarchies, groups, or sub-users; deny-by-default not enforced. |
| API6:2023 Unrestricted Access to Sensitive Business Flows | `13-businesslogic.md` | Sensitive flows: purchase/shop (scalping/hoarding), post/comment/vote (spam), book/reserve (slot blocking), referral/loyalty (automated farming), limited-stock, auction, transfer, withdrawal, ticket purchasing, reservation cancellation; any flow whose excessive automated use could harm the business; machine-consumed or B2B APIs lacking anti-automation controls. |
| API7:2023 Server Side Request Forgery | `03-ssrf.md` | API fetches remote resources from user-supplied URLs; webhooks; file fetch from URL; URL preview; custom SSO; image/document processing from remote URLs; cloud/Kubernetes/Docker metadata services reachable; blind or reflected SSRF possible; outbound traffic allowed to internal destinations. |
| API8:2023 Security Misconfiguration | `20-misconfiguration.md`, `21-backdoors.md`, `22-obfuscation.md` plus cross-mapped injection scans | Missing hardening across any API stack layer; improperly configured cloud permissions (IAM, S3 ACLs, security groups); missing security patches or outdated components; unnecessary features enabled (HTTP verbs, logging); inconsistent request processing in HTTP server chain; missing TLS; missing/improper CORS; missing security/cache-control headers; verbose errors/stack traces/default credentials; logging with placeholder expansion/JNDI; debug mode enabled; deliberate malicious code or obfuscation hiding backdoors/C2. |
| API9:2023 Improper Inventory Management | `18-inventory.md` | Multiple API versions without retirement plan; microservices/serverless functions; undocumented endpoints; debug/beta/non-production hosts; missing/outdated OpenAPI/GraphQL schemas; third-party integrations without inventory, business justification, or sensitivity classification; feature flags gating admin/endpoints; production data in non-production deployments; host environment or network access scope undocumented. |
| API10:2023 Unsafe Consumption of APIs | `19-unsafeapiconsumption.md`, `23-dependencies.md` plus cross-mapped injection scans | Outbound HTTP clients; third-party webhooks; package-manager/registry calls; disabled TLS certificate validation; blind redirect following; no timeouts/resource limits on external calls; third-party data reaches SQL/template/eval/deserialization sinks without validation; trust placed in data from integrated APIs without validation; typosquatting, dependency confusion, compromised packages, or vulnerable dependencies. |

## Cross-mapped injection coverage

Some OWASP API 2023 risks are not covered by a single dedicated scan. When the
risks below are selected, also run the indicated injection scans because the
vulnerable pattern crosses category boundaries.

| OWASP 2023 risk | Why injection scans matter | Additional scans to consider |
| --- | --- | --- |
| API8:2023 Security Misconfiguration | Verbose errors, unnecessary HTTP verbs, insecure defaults, and logging misconfigurations can create or expose injection sinks (e.g., JNDI/placeholder expansion in logs). | `02-sqli.md`, `04-xss.md`, `05-rce.md`, `06-ssti.md`, `07-xxe.md` if the corresponding technology is present. |
| API10:2023 Unsafe Consumption of APIs | Data from third-party APIs is trusted and passed to SQL/template/eval/deserialization sinks without validation. | `02-sqli.md`, `04-xss.md`, `05-rce.md`, `06-ssti.md`, `07-xxe.md`, `03-ssrf.md` when third-party responses drive outbound requests. |

When writing `00_plan.md`, flag cross-mapped scans as **cross-mapped** in the
rationale and note the dependency on the primary scan (e.g.,
`19-unsafeapiconsumption.md` may feed payloads into `02-sqli.md`).

## Per-risk trigger expansion

When a scan row above is selected, use the following OWASP-derived details to
justify the choice in `00_plan.md`.

**API1 — Broken Object Level Authorization**

- Every endpoint that receives an object ID and performs any action on it must implement object-level authorization.
- Object IDs can be sequential integers, UUIDs, slugs, VINs, document keys, or any generic string.
- IDs may appear in the request target (path/query), headers, or request payload, including GraphQL variables.
- The server often does not fully track client state and relies on client-supplied IDs.
- Comparing the session user ID (e.g., from a JWT) with the ID parameter is insufficient for most cases.
- If the attacker accesses an endpoint they should not reach at all, classify that under API5 (BFLA), not API1.

**API2 — Broken Authentication**

- Credential stuffing / brute-force possible on login or password-reset endpoints.
- No account lockout, CAPTCHA, or weak-password checks.
- GraphQL query batching used to bypass request-level rate limiting on authentication.
- Forgot-password / reset-password endpoints treated with the same protections as login.
- Sensitive operations (email change, password change, 2FA/MFA update) without re-authentication or password confirmation.
- Tokens sent in URLs or stored insecurely.
- Unsigned/weakly signed JWTs accepted (`{"alg":"none"}`); JWT expiration not validated.
- Plain-text, non-encrypted, or weakly hashed passwords; weak encryption keys.
- Microservices accessed without authentication or with weak/predictable tokens.
- API keys used for user authentication instead of client authentication.

**API3 — Broken Object Property Level Authorization**

- API exposes object properties considered sensitive (formerly Excessive Data Exposure).
- API allows changing, adding, or deleting sensitive properties the user should not access (formerly Mass Assignment).
- Generic serialization methods (`to_json()`, `to_string()`, `model_to_dict()`) return whole objects.
- Functions automatically bind client input into code variables, internal objects, or object properties.
- PATCH/partial-update endpoints or GraphQL resolvers return whole objects without schema-based response validation.
- Returned data structures are not kept to the bare minimum required by the endpoint.

**API4 — Unrestricted Resource Consumption**

- Missing execution timeouts, max allocable memory, max file descriptors, max processes.
- Missing max upload file size or max payload size.
- Missing max length for strings or max number of elements in arrays.
- Multiple operations in a single client request (GraphQL batching, array params).
- Unbounded records per page or unbounded string/array inputs.
- Third-party provider charged per request (SMS, email, phone, biometrics) without spending limit or billing alert.
- Serverless/container workloads without resource limits.
- Expensive operations without throttling (e.g., OTP validation, password recovery).

**API5 — Broken Function Level Authorization**

- Regular users potentially reaching admin endpoints.
- Sensitive actions exposed by HTTP method switching (`GET` → `DELETE`/`PUT`/`PATCH`).
- Cross-group endpoint guessing (`/api/users/export_all`).
- Administrative endpoints mixed with regular endpoints under the same path prefix (e.g., `/api/users` contains admin functions).
- Complex roles, groups, sub-users, or hierarchies without a consistent authorization module.
- No deny-by-default enforcement; access granted implicitly rather than explicitly.

**API6 — Unrestricted Access to Sensitive Business Flows**

- Purchasing products (scalping/hoarding).
- Creating comments/posts (spam).
- Making reservations (slot blocking).
- Referral/loyalty programs (automated farming).
- Limited-stock releases, auctions, ticket sales, transfers, withdrawals.
- Any flow whose excessive automated use could harm the business.
- Machine-consumed or B2B APIs that lack anti-automation controls (device fingerprinting, CAPTCHA, non-human pattern detection).

**API7 — Server Side Request Forgery**

- API fetches remote resources from user-supplied URLs.
- Common vectors: webhooks, file fetching from URL, custom SSO, URL previews, image/document processing.
- Modern cloud/Kubernetes/Docker expose management channels over HTTP on predictable paths.
- Blind SSRF (no response returned) and reflected SSRF (response returned) both matter.
- Can lead to internal service enumeration, port scanning, metadata credential theft, or DoS.

**API8 — Security Misconfiguration**

- Network/transport: TLS version/cipher issues, HSTS, certificate pinning, cleartext transmission.
- Infrastructure: cloud IAM, S3 ACLs, security groups, container privileged mode, outdated patches.
- API gateway: CORS policy missing or improper, security headers missing, method restrictions missing.
- Application: debug mode, verbose errors/stack traces, unnecessary features, default credentials, inconsistent HTTP-chain request handling.
- Logging: JNDI/placeholder expansion (e.g., Log4j-style lookups), request-body logging, sensitive data in logs.
- Deliberate malicious code: dynamic loading, reflective invocation, runtime decryption, environment/time triggers, anti-debug, DGA, beaconing/C2.
- Obfuscated code: base64/hex concatenation, control-flow flattening, opaque predicates, string decryption loops, encrypted payloads used to hide behavior.
- Missing hardening process, configuration review, or automated configuration assessment across environments.

**API9 — Improper Inventory Management**

- Host environment not documented (production/staging/test/dev unclear).
- Network access scope unclear (public/internal/partners).
- API version undocumented, outdated, or lacking a retirement plan.
- Host inventory missing or outdated.
- Third-party data flows without business justification, inventory, or sensitivity classification.
- Serverless function URLs or API gateway routes not inventoried.
- Feature flags gating admin/endpoints without documentation.
- Production data used in non-production deployments.

**API10 — Unsafe Consumption of APIs**

- Interactions over unencrypted channels.
- Disabled certificate validation on outbound HTTPS clients.
- Blind redirect following.
- No resource/time limits on third-party responses.
- No timeouts on third-party calls.
- Third-party data reaches SQL/template/eval/deserialization sinks without validation/sanitization.
- Trust placed in data from well-known third-party APIs.
- Package-manager/registry calls whose outputs are used unsafely.
- Typosquatting, dependency confusion, abandoned packages, suspicious maintainer changes, or compromised registry packages.
- Known CVEs in runtime dependencies reachable from application code.

## Procedure

1. Read `{{ REPORTS_ROOT }}/01_architecture.md`.
2. For each row in the matrix, decide **Run**, **Skip**, or **Conditional**.
   - **Run**: the trigger condition is clearly met.
   - **Skip**: the technology is explicitly absent and no indirect exposure
     exists. Provide a one-sentence justification.
   - **Conditional**: the trigger might be met through indirect paths (e.g.,
     shared library, microservice boundary, third-party integration, or
     dependency-mediated exposure). Recommend running the scan and explain the
     doubt.
3. If the user requested a specific vulnerability class, mark it **Run**
   regardless of architecture, but still evaluate the rest of the matrix.
4. Identify the primary language/framework and note it in the plan; this helps
   detection subagents select relevant examples from their references.
5. List any scans that should be prioritized (e.g., web app with relational DB:
   SQLi, XSS, IDOR, missing auth first).
6. For API8 and API10, check the [cross-mapped injection coverage](#cross-mapped-injection-coverage) section and add the relevant injection scans when the technology is present.

## Output

Write the plan to `{{ REPORTS_ROOT }}/00_plan.md` using exactly this format:

```markdown
# SAST Scan Plan

**Project**: [name from architecture.md]
**Generated**: [UTC ISO 8601 timestamp]

## Selected scans

| # | Scan | Reference | Rationale |
|---|---|---|---|
| 02 | SQL injection | `references/02-sqli.md` | Project uses PostgreSQL + SQLAlchemy raw queries |
| ... | ... | ... | ... |

## Skipped scans

| # | Scan | Reference | Justification |
|---|---|---|---|
| 07 | XXE | `references/07-xxe.md` | No XML parsing libraries or XML inputs found |

## Execution order

1. Run selected technical scans (02–23) in parallel batches of up to 5.
2. If selected, run `references/90-design-checklist.md` after the technical
   scans complete.
3. Finally, run `references/99-report.md`.

## Notes

[Any conditional scans, prioritization, or special instructions for the orchestrator]
```

For each selected scan, include in the rationale:

1. The OWASP API 2023 risk(s) it addresses.
2. The concrete trigger indicator observed in `01_architecture.md`.
3. Whether the scan is **primary** or **cross-mapped**.
4. Any dependency on another scan (e.g., `19-unsafeapiconsumption.md` may need
   results from `03-ssrf.md`, and cross-mapped injection scans may need
   results from `19-unsafeapiconsumption.md`).

## Important reminders

- Be conservative: when in doubt, mark a scan **Run** or **Conditional**.
- The skipped list is for explicit absences only; do not use it to save time.
- Do not perform the actual vulnerability detection in this phase.
- Do not modify project source code; write only to `{{ REPORTS_ROOT }}/00_plan.md`.
- Cross-mapped scans are not duplicates; they look at the same data from a different angle (e.g., untrusted third-party data passed to SQL sinks).
