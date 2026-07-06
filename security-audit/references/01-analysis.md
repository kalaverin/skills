# Codebase Analysis

[ref: #codebase-analysis]

You are performing the first phase of a security assessment. Your goal is to deeply understand the codebase. You are NOT looking for specific vulnerabilities yet. This is pure reconnaissance.

Create the `{{ REPORTS_ROOT }}/` folder in the project root if it does not already exist. This phase produces exactly one output file inside it:

`{{ REPORTS_ROOT }}/01_architecture.md` — technology stack, architecture, entry points, data flows

## Scope and mission

The `01_architecture.md` report is the single source of truth for every later phase of this audit: the screener, all detection scan references, and the final report. A detection subagent must be able to read `01_architecture.md` and immediately know where to look, what technologies to expect, and which OWASP API Security Top 10 2023 risks are relevant. Be maximally complete. Do not assume a later phase will re-explore the codebase to fill gaps.

This phase must:

- Identify every technology, framework, and library that affects security behavior.
- Map every entry point that accepts untrusted input.
- Trace the lifecycle of user input through the system.
- Inventory roles, permissions, authentication mechanisms, and sensitive data.
- Record resource limits, security configuration, API inventory, and deployment details.
- Map each finding to the OWASP API Security Top 10 2023 risks it enables.

This phase must NOT:

- Report specific vulnerabilities such as "line 42 has SQL injection".
- Modify project source code or configuration files.
- Run exploits, scanners, or tests that alter state.
- Make risk ratings or business-impact judgments.

## Table of contents

- [Phase 1: Technology Reconnaissance](#phase-1-technology-reconnaissance)
- [Phase 2: Architecture Mapping](#phase-2-architecture-mapping)
- [Data items required by downstream references](#data-items-required-by-downstream-references)
- [OWASP API Security Top 10 2023 mapping](#owasp-api-security-top-10-2023-mapping)
- [Output template](#output-template)
- [Important reminders](#important-reminders)

## Phase 1: Technology Reconnaissance

Start by reading dependency manifests, project configs, and directory structure. Then drill into source code to confirm findings. If the codebase is large, prioritize entry points, configuration, and security-sensitive flows rather than exhaustive line-by-line review.

For each category below, record concrete values: names, versions, file paths, and configuration files. When a value is ambiguous, state the ambiguity explicitly and list the evidence.

### Languages

- All programming languages used and their versions if specified.
- Version sources: `.python-version`, `pyproject.toml`, `package.json` `engines`, `go.mod`, `pom.xml`, `Cargo.toml`, `Gemfile`, `Dockerfile` base images, CI matrixes.
- Note any polyglot boundaries where data crosses between languages or runtimes.

### Frameworks

- Web frameworks (e.g., FastAPI, Django, Flask, Express, NestJS, Spring Boot, ASP.NET Core, Ruby on Rails, Gin).
- ORM layers (e.g., SQLAlchemy, Django ORM, Hibernate, Prisma, GORM, Entity Framework).
- Template engines (e.g., Jinja2, Thymeleaf, EJS, Handlebars).
- Task queues and background workers (e.g., Celery, Sidekiq, Bull, RQ, Temporal).
- Testing frameworks and mock servers that may expose debug endpoints.

### Serialization and data binding

- Generic serializers (e.g., Pydantic, Marshmallow, Django REST Framework serializers, Jackson, Gson).
- Auto-binding and mass-assignment libraries.
- PATCH, partial-update, or merge handlers.
- GraphQL resolver patterns and field-level access controls.
- Form parsers, multipart handlers, JSON/XML/YAML parsers, and their strictness settings.
- DTO/Request/Command classes and where they are defined.

### Package managers and dependencies

- Lock files and dependency manifests: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `requirements.txt`, `requirements.lock`, `uv.lock`, `poetry.lock`, `go.mod`, `go.sum`, `Gemfile.lock`, `pom.xml`, `Cargo.lock`, `composer.lock`, etc.
- Direct and transitive dependencies with known security relevance: authentication libraries, HTTP clients, template engines, XML parsers, PDF/image processors, cryptography libraries.
- Dependency-update cadence and whether automated scanning is configured.

### Infrastructure hints

- Dockerfiles, docker-compose files, Kubernetes manifests, Helm charts, Terraform, Pulumi, CI/CD configs.
- Base images, exposed ports, runtime users, capabilities, read-only filesystem settings.
- Service mesh, reverse proxy, load balancer, WAF, or API gateway presence.
- Cloud provider services and IAM roles.

### Databases and storage

- SQL databases (e.g., PostgreSQL, MySQL, SQL Server, SQLite).
- NoSQL databases (e.g., MongoDB, DynamoDB, Redis, Cassandra, Elasticsearch).
- Cache layers and message brokers (e.g., Redis, Memcached, RabbitMQ, Kafka, SQS).
- Connection strings, ORM models, migration files, query builders, raw SQL files.
- File storage backends (local filesystem, S3, GCS, Azure Blob, MinIO).

### Authentication and authorization

- Auth libraries, middleware, and decorators (e.g., OAuth2, OIDC, JWT, session cookies, API keys, HMAC, mTLS).
- Token issuance, validation, refresh, revocation, and expiry configuration.
- Session configs: store, cookie flags (`HttpOnly`, `Secure`, `SameSite`), TTL.
- Role/permission models, access-control lists, attribute-based access control, policy engines.
- Admin panel presence and how admin privileges are granted.
- Public, authenticated, and internal-only endpoints.

### External integrations

- Third-party APIs, payment processors, email services, SMS gateways, cloud SDKs.
- Webhook handlers and signature verification methods.
- Outbound HTTP clients and destinations (e.g., `requests`, `httpx`, `axios`, `fetch`, `RestTemplate`, `HttpClient`).
- Service-to-service authentication and trust assumptions.

### Entry points

- HTTP routes and route tables.
- GraphQL schemas, queries, mutations, subscriptions.
- gRPC service definitions and proto files.
- CLI commands and their arguments.
- WebSocket handlers and message formats.
- Scheduled jobs, cron expressions, and message consumers.
- Serverless functions, event triggers, and hooks.

For each entry point, record: path/pattern, HTTP method or message type, whether authentication is required, and whether it accepts user-supplied object IDs or slugs.

### Resource limits and rate limiting

- Framework-level rate limits per route, user, IP, or global.
- Pagination parameters and maximum page sizes.
- Max body/payload sizes.
- Max upload sizes.
- Execution timeouts per request, job, or query.
- Memory, CPU, process, connection, and queue-size limits.
- Quotas for paid resources such as SMS, email, or biometric checks.

### Security configuration

- HTTPS/TLS setup and minimum TLS version.
- Security headers (`HSTS`, `X-Frame-Options`, `CSP`, `X-Content-Type-Options`, etc.).
- CORS policy: allowed origins, methods, headers, credentials.
- Debug mode, stack-trace exposure, and verbose error pages.
- Framework hardening settings (e.g., `DEBUG`, `SECRET_KEY`, CSRF protection, clickjacking protection).
- Cloud/container IAM roles and network policies.
- Logging configuration: what is logged, where, retention, and whether PII is included.

### API inventory and environments

- API versions and version negotiation strategy.
- OpenAPI, AsyncAPI, GraphQL schemas, and whether they are generated from code or maintained manually.
- Debug endpoints, health checks, metrics, and admin interfaces.
- Production, staging, development, and review-app hosts.
- Documentation freshness and divergence from code.
- Deprecated endpoints that remain deployed.

## Phase 2: Architecture Mapping

Based on Phase 1, build a mental model and document the following.

### Service boundaries

- Is this a monolith, modular monolith, microservices, serverless, or hybrid?
- What are the major components, services, or modules?
- What talks to what, and over which protocols?

### Data flow

- How does user input enter the system, get processed, get stored, and get returned?
- Trace primary flows such as registration, login, password reset, core business actions, file upload, payment, and admin operations.
- Identify where input is parsed, validated, transformed, and serialized.

### Trust boundaries

- Where does the system transition between trusted and untrusted contexts?
  - User input to backend.
  - Backend to database.
  - Service to service.
  - Server to client.
  - Internal network to external API.
- What authentication, validation, or encryption applies at each boundary?

### Privilege levels

- What roles, permissions, groups, tenants, or organizations exist?
- How are they enforced? Middleware, decorators, explicit checks, policy engines?
- Is there an admin panel, superuser role, or impersonation feature?
- Are privilege checks centralized or duplicated across handlers?

### Sensitive data inventory

- PII, credentials, tokens, financial data, health records, secrets, session identifiers.
- Where each type is stored, how it is accessed, and what protection is applied at rest and in transit.
- Whether sensitive data appears in logs, URLs, query parameters, or error messages.

### Secret management

- Where API keys, database credentials, signing keys, certificates, and encryption keys are stored.
- Distinguish between env vars, secret managers (e.g., Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager), source code, config files, and CI variables.
- Note rotation policy hints and key derivation practices.

### Logging and monitoring

- Which security events are logged: authentication success/failure, authorization failures, input-validation failures, rate-limit hits, file uploads, sensitive data access.
- Whether logs include PII, tokens, or passwords.
- Whether failed auth, access-control, or input-validation events trigger alerts.
- Log aggregation, SIEM, or observability tooling.

### CI/CD and deployment

- Build pipelines and their stages.
- Infrastructure-as-Code and environment separation.
- Container hardening, image scanning, and runtime security.
- Dependency-update cadence and automated security scanning.
- Deployment approvals, secrets injection, and rollback procedures.

## Data items required by downstream references

The table below links each architecture data item to the detection references that consume it. If a data item is missing, downstream detection may miss vulnerabilities.

| Data item | Required by | Why it matters |
|---|---|---|
| Object-ID access patterns in entry points | `08-idor.md`, `00-screener.md` | BOLA exists when functions accept object IDs without per-object authorization. |
| Auth endpoints, session/token mechanisms, role model | `10-missingauth.md`, `09-jwt.md`, `00-screener.md` | Weak or missing auth allows account takeover and privilege escalation. |
| Serializers / auto-binding / mass-assignment frameworks | `16-bopla.md`, `00-screener.md` | Unrestricted data binding leaks or mutates sensitive object properties. |
| Rate limits, pagination, payload size, resource budgets | `17-resourceconsumption.md`, `10-missingauth.md` | Missing limits enable resource exhaustion and brute force. |
| Role/permission model and admin endpoint inventory | `08-idor.md`, `10-missingauth.md`, `00-screener.md` | Complex roles without clear separation lead to horizontal/vertical privilege escalation. |
| Sensitive business flow endpoints | `13-businesslogic.md`, `00-screener.md` | Automated abuse of flows harms business without being an implementation bug. |
| Outbound HTTP clients and third-party integrations | `03-ssrf.md`, `19-unsafeapiconsumption.md`, `00-screener.md` | Unvalidated outbound URIs and over-trusted third-party data enable SSRF and supply-chain attacks. |
| Security configuration (TLS, headers, CORS, debug mode) | `20-misconfiguration.md`, `00-screener.md` | Default/verbose configurations expose the API to multiple attack classes. |
| API versions, specs, debug endpoints, non-prod hosts | `18-inventory.md`, `20-misconfiguration.md`, `00-screener.md` | Undocumented or deprecated endpoints bypass security controls and monitoring. |
| File upload handling and storage patterns | `11-fileupload.md`, `12-pathtraversal.md`, `17-resourceconsumption.md`, `00-screener.md` | Insecure upload handling leads to code execution, path traversal, and resource abuse. |
| Secret management and hardcoded credentials | `15-hardcodedsecrets.md`, `09-jwt.md`, `00-screener.md` | Exposed secrets enable authentication bypass and data decryption. |
| Logging and monitoring | `20-misconfiguration.md`, `99-report.md` | Incomplete logging hides attacks and complicates incident response. |
| Input validation and query building patterns | `02-sqli.md`, `04-xss.md`, `12-pathtraversal.md`, `00-screener.md` | Validation gaps and unsafe query construction enable injection attacks. |
| CI/CD and deployment practices | `20-misconfiguration.md`, `15-hardcodedsecrets.md` | Pipeline weaknesses introduce supply-chain and configuration risks. |

## OWASP API Security Top 10 2023 mapping

The architecture data items below are the single source of truth for the screener and all detection references. Map each item to the OWASP API 2023 risks it enables.

| Architecture data item | OWASP API 2023 risk(s) | Why it matters |
|---|---|---|
| Object-ID access patterns in entry points | API1:2023 Broken Object Level Authorization | BOLA exists because functions accept object IDs without per-object authorization checks. |
| Auth endpoints, session/token mechanisms, role model | API2:2023 Broken Authentication, API5:2023 Broken Function Level Authorization | Weak auth or missing function-level checks allow account takeover and privilege escalation. |
| Serializers / auto-binding / mass-assignment frameworks | API3:2023 Broken Object Property Level Authorization | Unrestricted data binding leaks or mutates sensitive object properties. |
| Rate limits, pagination, payload size, resource budgets | API4:2023 Unrestricted Resource Consumption | Missing limits let attackers exhaust resources or run up costs. |
| Role/permission model and admin endpoint inventory | API5:2023 Broken Function Level Authorization | Complex roles without clear separation lead to horizontal/vertical privilege escalation. |
| Sensitive business flow endpoints (purchase, post, book) | API6:2023 Unrestricted Access to Sensitive Business Flows | Automated abuse of flows harms business without being an implementation bug. |
| Outbound HTTP clients and third-party integrations | API7:2023 Server Side Request Forgery, API10:2023 Unsafe Consumption of APIs | Unvalidated outbound URIs and over-trusted third-party data enable SSRF and supply-chain attacks. |
| Security configuration (TLS, headers, CORS, debug mode) | API8:2023 Security Misconfiguration | Default/verbose configurations expose the API to multiple attack classes. |
| API versions, specs, debug endpoints, non-prod hosts | API9:2023 Improper Inventory Management | Undocumented or deprecated endpoints bypass security controls and monitoring. |

## Output template

Write the results of Phase 1 and Phase 2 to `{{ REPORTS_ROOT }}/01_architecture.md` using exactly this format. Replace bracketed placeholders with concrete findings. If a field is not applicable, write "N/A" and briefly explain why. If a field is unknown, write "Unknown" and describe what evidence is missing.

```markdown
# Architecture: [Project Name]

## Technology Stack

| Category | Details |
|---|---|
| Languages | ... |
| Frameworks | ... |
| Databases | ... |
| Auth mechanism | ... |
| Infrastructure | ... |
| External services | ... |
| Serialization & data binding | ... |

## Architecture Overview

[Describe the architecture: monolith vs microservices, how components interact,
main modules and their responsibilities. Mention any API gateway, reverse proxy,
load balancer, or service mesh.]

## Data Flow

[Trace how user input enters the system, gets processed, stored, and returned.
Cover the primary flows such as registration, login, password reset, core
business actions, file upload, payment, and admin operations. Identify parsing,
validation, transformation, and serialization steps.]

## Entry Points

| Entry Point | Type | Auth Required | User-Supplied Object IDs/Slugs | Description |
|---|---|---|---|---|
| ... | HTTP/GraphQL/WS/etc. | Yes/No | Yes/No — field name | ... |

## Authentication Endpoints

| Endpoint | Type | Purpose | Notes |
|---|---|---|---|
| ... | ... | login/register/reset/2FA/etc. | ... |

## Role & Permission Model

[Roles, permissions, how they are enforced, admin panel presence, and any
role hierarchy or group/tenant separation. List admin, internal, or privileged
endpoints separately if applicable.]

## Trust Boundaries

[List each trust boundary and what crosses it: user input to backend,
backend to database, service to service, server to client, internal to external
API. Include the authentication/validation/encryption applied at each.]

## Sensitive Data Inventory

| Data Type | Where Stored | How Accessed | Protection |
|---|---|---|---|
| ... | ... | ... | ... |

## Resource Limits & Rate Limiting

| Limit Type | Framework/Config | Value/Behavior | Notes |
|---|---|---|---|
| Rate limiting | ... | ... | ... |
| Pagination max | ... | ... | ... |
| Max payload/body | ... | ... | ... |
| Max upload size | ... | ... | ... |
| Execution timeout | ... | ... | ... |
| Memory/CPU/process limits | ... | ... | ... |

## Security Configuration

| Topic | Current State | Notes |
|---|---|---|
| HTTPS/TLS | ... | ... |
| Security headers | ... | ... |
| CORS policy | ... | ... |
| Debug mode | ... | ... |
| Framework hardening | ... | ... |
| Cloud/container IAM | ... | ... |
| Logging/monitoring | ... | ... |

## API Inventory & Environments

| Item | Details |
|---|---|
| API versions | ... |
| OpenAPI/AsyncAPI/GraphQL schemas | ... |
| Debug endpoints | ... |
| Production hosts | ... |
| Staging/dev/review hosts | ... |
| Documentation freshness | ... |

## File Upload Handling

| Aspect | Details |
|---|---|
| Upload endpoints | ... |
| Storage backend | ... |
| File-type/size validation | ... |
| Path construction | ... |

## Secret Management

| Secret Type | Storage Location | Rotation/Notes |
|---|---|---|
| API keys | ... | ... |
| DB credentials | ... | ... |
| Signing keys / certificates | ... | ... |

## CI/CD & Deployment

[Build pipelines, Infrastructure-as-Code, container hardening, dependency-update
cadence, deployment approvals, secrets injection, and rollback procedures.]

## Open Questions and Ambiguities

[List any architectural details that could not be determined, the evidence you
examined, and what a later phase should verify.]
```

## Important reminders

- Do NOT report specific vulnerabilities (like "line 42 has SQL injection"). That comes in later phases.
- Do NOT modify project source code. Write only to `{{ REPORTS_ROOT }}/01_architecture.md`.
- Be thorough in exploration. Read actual source code, not just config files. Look at how auth middleware is applied, how queries are built, how file uploads are handled, and how outbound requests are constructed.
- If the codebase is large, prioritize security-sensitive areas: auth, payment, data access, file handling, admin functionality.
- Record concrete file paths, configuration keys, and versions whenever possible. Vague statements such as "uses JWT" are insufficient; specify the library, configuration file, and token handling flow.
- Mark unknowns explicitly. Do not invent details to make the report look complete.
- Preserve the placeholder `{{ REPORTS_ROOT }}` exactly as written; do not substitute it with a literal path in this reference.
