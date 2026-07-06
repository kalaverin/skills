# Improper Inventory Management Detection

[ref: #inventory-detection]

You are performing a focused security assessment to find **Improper Inventory Management** vulnerabilities in a codebase and its deployments. This skill uses a three-phase approach with subagents: **recon** (discover API hosts, versions, routes, docs, debug endpoints, serverless functions, feature flags, API gateways, and third-party integrations), **batched verify** (check reachability, spec accuracy, and data exposure in parallel batches of 3), and **merge** (consolidate results).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

---

## API9:2023 Improper Inventory Management

OWASP API Security Top 10 2023 calls this risk **API9:2023 – Improper Inventory Management**. It covers any situation where an organization lacks accurate visibility into its API assets, versions, hosts, data flows, and deployment paths. Without an up-to-date inventory, security controls are inconsistently applied, deprecated or debug endpoints remain exposed, serverless functions and gateway routes become shadow APIs, and incident response is slowed.

### OWASP Risk Summary

| Factor | Rating |
|--------|--------|
| Exploitability | Easy |
| Prevalence | Widespread |
| Detectability | Average |
| Technical impact | Moderate |

The risk stems from outdated documentation, missing asset inventory, lack of retirement strategies, and unmonitored data flows.

### Documentation and Data-Flow Blindspots

OWASP defines two blindspots that drive this risk:

**Documentation blindspot** — a host's purpose is unclear and the following are unanswered:
- Which environment is the API running in?
- Who should have network access?
- Which API version is running?
- Is there up-to-date documentation and a retirement plan?
- Is the host inventory current?

**Data-flow blindspot** — sensitive data is shared with a third party and:
- There is no business justification or approval.
- There is no inventory or visibility of the flow.
- There is no clear view of what type of sensitive data is shared.

### OWASP Example Attack Scenarios

1. **Beta API host bypass** — `beta.api.example.org` runs the same API as production but lacks the rate-limiting component, allowing brute-force of reset tokens.
2. **Third-party data sharing** — a malicious app gains consent from many users and accesses friends' private information because the data flow is not restrictive or monitored.

These examples justify the audit findings about serverless/function URLs, API gateways, and feature flags: any unmonitored deployment path can become a blindspot.

### What This Scan Covers

- **Undocumented endpoints** — routes that exist in code but are not listed in OpenAPI/Swagger, API docs, or the inventory.
- **Deprecated API versions** — old versions (`/api/v1/`, `/v2/`) still deployed without a retirement plan or with weaker controls.
- **Excessive active API versions** — multiple major versions supported simultaneously without documented backport or sunset rationale, increasing attack surface and control drift.
- **Debug endpoints** — development, diagnostic, or admin routes left enabled in production (`/debug`, `/api/dev`, `/swagger-ui.html`, `/actuator`, `debug=True`).
- **Non-production hosts** — staging, beta, dev, or test deployments exposed to unauthorized networks or containing production data.
- **Missing or outdated API documentation** — no OpenAPI spec, stale specs, or specs that do not match implemented routes.
- **Shadow APIs** — endpoints deployed outside the official CI/CD pipeline or known only to a single team.
- **Serverless function URLs** — AWS Lambda function URLs, Azure Function Apps, Google Cloud Functions, and serverless framework configs (`serverless.yml`, `serverless.yaml`, `template.yml`, `functions/`) that expose routes not tracked in the main API inventory.
- **Feature-flag-gated routes** — endpoints, admin panels, or beta routes enabled by LaunchDarkly, Split, Unleash, or custom flag checks that may unintentionally expose functionality in production.
- **API gateway route inventory gaps** — route definitions in Kong, AWS API Gateway, Azure API Management, NGINX ingress, Ambassador, or Istio that are not reflected in code specs or inventory.
- **Unmonitored third-party integrations** — data flows to external services without inventory, business justification, or visibility.
- **Production data in non-production deployments** — real customer data in dev/staging/test environments.

### What This Scan Does NOT Cover

Do not flag these under this scan:

- **Missing authentication on a known endpoint** → that's "Unauthenticated Access".
- **Broken object-level authorization** → that's IDOR/BOLA.
- **Sensitive data exposure in responses** → that's "Excessive Data Exposure".
- **Weak access control on a documented admin endpoint** → that's BFLA or Access Control.

---

## Vulnerable vs. Secure Examples

### Debug Mode Enabled

```python
# VULNERABLE: debug mode enabled in production
DEBUG = True

# SECURE: debug controlled by environment
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
```

```java
// VULNERABLE: Spring Boot debug enabled unconditionally
spring.boot.devtools.restart.enabled=true
spring.output.ansi.enabled=always

// SECURE: debug/devtools disabled or profile-gated
spring.devtools.restart.enabled=false
# active profile controls debug behavior
```

```javascript
// VULNERABLE: Express debug mode on by default
const app = express();
app.set("env", "development");
app.use(errorhandler({ dumpExceptions: true, showStack: true }));

// SECURE: environment-driven debug
const isDev = process.env.NODE_ENV === "development";
if (isDev) app.use(errorhandler());
```

### Deprecated API Version Still Exposed

```python
# VULNERABLE: old version mounted without retirement plan or equal controls
app.register_blueprint(v1_api, url_prefix="/api/v1")
app.register_blueprint(v2_api, url_prefix="/api/v2")  # v1 still active

# SECURE: deprecated version removed or protected at the same level
app.register_blueprint(v2_api, url_prefix="/api/v2")
# v1 returns 410 Gone or is behind identical auth/rate-limit controls
```

```java
// VULNERABLE: deprecated version still exposed without EOL date
@RestController
@RequestMapping("/api/v1")
public class OrderControllerV1 { ... }

// SECURE: deprecated version gated or removed; current version documented
// application.properties: api.versions.active=v3
// api.v1.sunset-date=2024-12-31
// api.v1.return-410=true
@RestController
@RequestMapping("/api/v3")
public class OrderControllerV3 { ... }
```

```javascript
// VULNERABLE: multiple active versions without sunset plan
app.use("/api/v1", v1Router);
app.use("/api/v2", v2Router);
app.use("/api/v3", v3Router);

// SECURE: unsupported versions return 410 or redirect; active versions inventoried
app.use("/api/v3", v3Router);
app.use("/api/v2", sunsetRouter); // returns 410 Gone with Sunset header
```

```go
// VULNERABLE: deprecated routes mounted alongside current
mux.Handle("/api/v1/orders", v1OrderHandler)
mux.Handle("/api/v2/orders", v2OrderHandler)

// SECURE: only current version exposed; deprecated path returns 410
mux.Handle("/api/v2/orders", v2OrderHandler)
mux.Handle("/api/v1/orders", goneHandler)
```

```csharp
// VULNERABLE: old API version still mapped
app.MapControllers();
[ApiVersion("1.0")]
[Route("api/v{version:apiVersion}/orders")]
public class OrdersController : ControllerBase { ... }

// SECURE: deprecated versions report 410 with sunset policy
[ApiVersion("3.0")]
[Route("api/v{version:apiVersion}/orders")]
public class OrdersControllerV3 : ControllerBase { ... }
```

### Debug/Admin Routes in Production

```python
# VULNERABLE: development routes registered unconditionally
if True:
    app.register_blueprint(debug_routes)

# SECURE: debug routes only in non-production environments
if os.environ.get("ENV") in ("dev", "test"):
    app.register_blueprint(debug_routes)
```

```java
// VULNERABLE: Spring Boot Actuator exposed without restriction
management.endpoints.web.exposure.include=*

// SECURE: actuator limited and protected
management.endpoints.web.exposure.include=health,info
management.endpoint.health.show-details=when_authorized
```

```javascript
// VULNERABLE: admin/debug routes registered unconditionally
app.use("/admin", adminRouter);
app.use("/debug", debugRouter);

// SECURE: admin routes gated by environment and role
if (process.env.NODE_ENV !== "production") {
  app.use("/debug", debugRouter);
}
app.use("/admin", requireRole("admin"), adminRouter);
```

```go
// VULNERABLE: pprof debug handlers mounted in production
import _ "net/http/pprof"

// SECURE: pprof only bound on localhost/internal admin listener
if env == "dev" || env == "test" {
    mux.Handle("/debug/pprof/", http.HandlerFunc(pprof.Index))
}
```

```csharp
// VULNERABLE: developer exception page in production
if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage(); // wrong branch or missing env check
}

// SECURE: environment-appropriate error handling
if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
}
else
{
    app.UseExceptionHandler("/error");
    app.UseHsts();
}
```

### Missing OpenAPI / API Documentation

```yaml
# VULNERABLE: no OpenAPI spec or manual spec never updated
# No openapi.yaml, no Swagger, no generated docs

# SECURE: spec generated from code and verified in CI
# openapi.yaml generated by FastAPI / flask-smorest / springdoc / swashbuckle / etc.
# CI fails if spec drifts from implementation
```

```java
// SECURE: Springdoc generates OpenAPI from controllers
@Configuration
public class OpenApiConfig {
    @Bean
    public OpenAPI customOpenAPI() { ... }
}
```

```javascript
// SECURE: swagger-jsdoc or tsoa generates spec from code
const swaggerJsdoc = require("swagger-jsdoc");
const options = {
  definition: { openapi: "3.0.0", info: { title: "API", version: "1.0.0" } },
  apis: ["./routes/*.js"],
};
const specs = swaggerJsdoc(options);
```

### No CI/CD Spec Generation

```yaml
# VULNERABLE: documentation manually maintained
# openapi.yml updated by hand, often stale

# SECURE: spec generated in CI/CD pipeline
- name: Generate OpenAPI spec
  run: python -m scripts.generate_openapi > openapi.yaml
- name: Check spec is up to date
  run: git diff --exit-code openapi.yaml
```

```yaml
# SECURE: Java/Spring spec generation and drift check
- name: Generate OpenAPI with springdoc
  run: ./mvnw springdoc-openapi:generate
- name: Fail on spec drift
  run: git diff --exit-code openapi.yaml
```

### Non-Production Host with Production Data

```yaml
# VULNERABLE: staging uses production database
STAGING_DATABASE_URL: postgres://prod-db.example.com/app

# SECURE: staging isolated with synthetic/anonymized data
STAGING_DATABASE_URL: postgres://staging-db.example.com/app
DATA_CLASSIFICATION: synthetic
```

```csharp
// VULNERABLE: dev config points to production storage
"ConnectionStrings": {
  "DefaultConnection": "Server=prod-sql.example.com;Database=app;"
}

// SECURE: environment-specific connection strings and synthetic data
"ConnectionStrings": {
  "DefaultConnection": "Server=staging-sql.example.com;Database=app_staging;"
},
"DataClassification": "synthetic"
```

### Third-Party Integration Without Inventory

```python
# VULNERABLE: data sent to external service with no inventory entry
requests.post("https://third-party.example.com/sync", json=user_data)

# SECURE: integration listed in inventory with data-flow classification
# Inventory entry: partner-sync-service, PII flow, approved 2024-01, owner=security@example.com
```

```java
// VULNERABLE: outbound call to external API without inventory entry
webClient.post()
  .uri("https://analytics.example.com/events")
  .bodyValue(userEvent)
  .retrieve()
  .toBodilessEntity();

// SECURE: external integration declared in approved inventory
// Inventory: analytics-events-service, behavioral events, approved, owner=data@example.com
```

```javascript
// VULNERABLE: external data sharing not inventoried
await fetch("https://partner.example.com/leads", {
  method: "POST",
  body: JSON.stringify(customerData),
});

// SECURE: integration catalogued with data-flow classification
// Inventory entry: partner-leads-service, PII/lead data, approved 2024-06, owner=legal@example.com
```

### Serverless Function URLs

```yaml
# VULNERABLE: Lambda function URL exposed without inventory entry
functions:
  processOrder:
    handler: handlers.processOrder
    url: true  # AWS Lambda Function URL enabled

# SECURE: function URL inventoried, auth required, and route reflected in docs
functions:
  processOrder:
    handler: handlers.processOrder
    url:
      authorizer: aws_iam
      cors: false
# Inventory entry: processOrder, AWS Lambda Function URL, internal-only, owner=sre@example.com
```

```json
// VULNERABLE: Azure Function App HTTP trigger not in API inventory
{
  "bindings": [
    {
      "authLevel": "anonymous",
      "type": "httpTrigger",
      "direction": "in",
      "name": "req",
      "methods": ["post"]
    }
  ]
}

// SECURE: function trigger inventoried and auth level appropriate
{
  "bindings": [
    {
      "authLevel": "function",
      "type": "httpTrigger",
      "direction": "in",
      "name": "req",
      "methods": ["post"]
    }
  ]
}
```

### Feature-Flag-Gated Routes

```python
# VULNERABLE: admin route enabled by a feature flag without environment safeguards
if launchdarkly_client.variation("admin-billing-route", user, False):
    app.register_blueprint(billing_admin)

# SECURE: flag defaults to off in production; route still inventoried and access-controlled
# Inventory entry: billing-admin route, gated by LaunchDarkly flag "admin-billing-route", owner=finance@example.com
if is_prod():
    enabled = False
else:
    enabled = launchdarkly_client.variation("admin-billing-route", user, False)
if enabled:
    app.register_blueprint(billing_admin)
```

```javascript
// VULNERABLE: beta endpoint exposed through Split flag with no inventory
if (splitClient.getTreatment("beta-reports") === "on") {
  app.use("/api/beta/reports", betaReportsRouter);
}

// SECURE: flag state logged; endpoint in inventory and restricted
// Inventory entry: /api/beta/reports, Split flag "beta-reports", beta group only
const treatment = splitClient.getTreatment("beta-reports");
if (treatment === "on" && user.isBetaTester) {
  app.use("/api/beta/reports", requireBetaUser, betaReportsRouter);
}
```

### API Gateway Route Inventory

```yaml
# VULNERABLE: Kong route declared but not reflected in OpenAPI or inventory
services:
- name: billing-service
  url: http://billing:8080
  routes:
  - name: billing-admin
    paths:
    - /billing/admin

# SECURE: gateway route inventoried and access-controlled
# Inventory entry: /billing/admin, Kong route "billing-admin", admin-only
routes:
- name: billing-admin
  paths:
  - /billing/admin
  plugins:
  - name: key-auth
  - name: acl
    config:
      allow:
      - admin
```

```yaml
# VULNERABLE: NGINX ingress exposes internal route publicly
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: internal-api
spec:
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /internal
        pathType: Prefix
        backend:
          service:
            name: internal-service
            port:
              number: 80

# SECURE: internal route restricted by ingress annotation or separate internal host
metadata:
  annotations:
    nginx.ingress.kubernetes.io/whitelist-source-range: "10.0.0.0/8"
```

---

## Execution

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

> **Subagent constraints reminder**: All subagents used in this skill are **read-only**. They must never modify project source code, configuration files, CI/CD pipelines, or deployment manifests. Subagents only analyze, classify, and report.

### Phase 1: Recon — Discover API Assets

Launch a subagent with the following instructions:

> **Goal**: Discover all API hosts, versions, routes, documentation, debug endpoints, serverless functions, feature flags, API gateway routes, and third-party integrations. Write results to `{{ REPORTS_ROOT }}/18_recon.md`.
>
> **Context**: You will be given the project's architecture summary. Use it to understand the tech stack, frameworks, route definitions, deployment model, and known environments.
>
> **What to search for**:
>
> 1. **API hosts and environments**
>    - Configuration files: `.env`, `config.py`, `settings.yaml`, Terraform, Helm, Docker Compose
>    - Hostnames, base URLs, environment variables (`API_HOST`, `BASE_URL`, `ALLOWED_HOSTS`)
>    - Distinguish production, staging, dev, test, beta, demo
>
> 2. **API versions**
>    - URL prefixes: `/api/v1/`, `/v2/`, `/api/v1beta1/`
>    - Version headers or content negotiation
>    - Retirement plans or deprecation notices
>
> 3. **Route definitions**
>    - All framework routes, controllers, handlers, resource definitions
>    - GraphQL schemas and resolver maps
>    - gRPC `.proto` services
>
> 4. **Documentation and specs**
>    - `openapi.yaml`, `swagger.json`, `schema.graphql`, proto files
>    - Inline documentation tools (FastAPI, Springdoc, Swashbuckle, NSwag, etc.)
>    - CI steps that generate or validate specs
>
> 5. **Debug / diagnostic / development endpoints**
>    - `/debug`, `/dev`, `/test`, `/swagger-ui`, `/actuator`, `/_debug`, GraphQL introspection
>    - `DEBUG = True`, `app.debug`, `ENV=development`
>    - Health checks that leak debug info
>
> 6. **Serverless function URLs**
>    - AWS Lambda function URLs (`url: true` or `url.authorizer` in `serverless.yml`/`template.yml`)
>    - Azure Function Apps HTTP triggers (`function.json`)
>    - Google Cloud Functions (`main.py` + `functions-framework`, `gcloud functions deploy`)
>    - Serverless framework config files (`serverless.yml`, `serverless.yaml`, `serverless.json`)
>
> 7. **Feature flags gating routes or endpoints**
>    - LaunchDarkly (`launchdarkly-client`, `ldclient`)
>    - Split (`splitio`, `@splitsoftware/splitio`)
>    - Unleash (`unleash-client`)
>    - Custom flag checks (`isFeatureEnabled`, `feature_flag`, `FLAGS.*`, `config.*_enabled`)
>    - Flags that enable admin, beta, partner, or internal routes
>
> 8. **API gateway route definitions**
>    - Kong (`kong.yml`, `kong.yaml`, declarative config)
>    - AWS API Gateway (`AWS::ApiGateway::Resource`, `AWS::ApiGatewayV2::Route`, `api.yaml`)
>    - Azure API Management (`apim.json`, `api-management` resources)
>    - NGINX ingress (`Ingress` resources, `nginx.conf`)
>    - Ambassador (`Mapping` resources)
>    - Istio (`VirtualService`, `Gateway` resources)
>
> 9. **Third-party integrations and data flows**
>    - Outgoing HTTP clients, SDKs, webhooks
>    - External API keys, service tokens
>    - Data classification or sharing statements
>
> **Output format** — write to `{{ REPORTS_ROOT }}/18_recon.md`:
>
> ```markdown
> # Improper Inventory Management Recon: [Project Name]
>
> ## Summary
> Discovered [N] API hosts, [N] versions, [N] routes, [N] docs/specs, [N] debug endpoints, [N] serverless functions, [N] feature flags, [N] gateway routes, [N] third-party integrations.
>
> ## API Hosts
>
> ### 1. [environment] [hostname/base URL]
> - **Source**: `path/to/file` (lines X-Y)
> - **Environment**: [production / staging / dev / beta / unknown]
> - **Network access**: [public / internal / partner-only / unknown]
> - **Notes**: [any known details]
>
> ## API Versions
>
> ### 1. [version prefix or header]
> - **Source**: `path/to/file` (lines X-Y)
> - **Status**: [current / deprecated / beta / unknown]
> - **Retirement plan**: [yes / no / unknown]
>
> ## Routes
>
> ### 1. [METHOD /path]
> - **Source**: `path/to/file` (lines X-Y)
> - **Version**: [v1 / v2 / unversioned]
> - **Auth required**: [yes / no / unknown]
> - **Notes**: [public / admin / debug / etc.]
>
> ## Documentation / Specs
>
> ### 1. [spec name]
> - **Source**: `path/to/file` (lines X-Y)
> - **Type**: [OpenAPI / Swagger / GraphQL schema / proto / README]
> - **Generated automatically**: [yes / no / unknown]
> - **Last updated / CI check**: [yes / no / unknown]
>
> ## Debug / Dev Endpoints
>
> ### 1. [endpoint or config]
> - **Source**: `path/to/file` (lines X-Y)
> - **Type**: [debug route / admin panel / swagger-ui / actuator / introspection]
> - **Enabled in production**: [yes / no / conditional / unknown]
>
> ## Serverless Function URLs
>
> ### 1. [function / URL name]
> - **Source**: `path/to/file` (lines X-Y)
> - **Provider**: [AWS Lambda / Azure Function / Google Cloud Function]
> - **Auth level**: [public / IAM / function key / anonymous]
> - **Inventory entry found**: [yes / no / unknown]
>
> ## Feature Flags Gating Routes
>
> ### 1. [flag name]
> - **Source**: `path/to/file` (lines X-Y)
> - **Provider**: [LaunchDarkly / Split / Unleash / custom]
> - **Gated route(s)**: [list]
> - **Default in production**: [on / off / unknown]
>
> ## API Gateway Routes
>
> ### 1. [route name / path]
> - **Source**: `path/to/file` (lines X-Y)
> - **Gateway**: [Kong / AWS API Gateway / Azure APIM / NGINX / Ambassador / Istio]
> - **Reflected in OpenAPI/inventory**: [yes / no / unknown]
>
> ## Third-Party Integrations
>
> ### 1. [service name]
> - **Source**: `path/to/file` (lines X-Y)
> - **Role**: [analytics / payment / notification / etc.]
> - **Data exchanged**: [PII / financial / logs / unknown]
> - **Inventory entry found**: [yes / no / unknown]
> ```

### Phase 2: Verify — Validate Inventory Gaps (Batched)

After Phase 1 completes, read `{{ REPORTS_ROOT }}/18_recon.md` and split the discovered items into **batches of up to 3 items each**. Launch **one subagent per batch in parallel**. Each subagent verifies only its assigned items and writes results to its own batch file.

**Batching procedure** (you, the orchestrator, do this — not a subagent):

1. Read `{{ REPORTS_ROOT }}/18_recon.md` and count the numbered sections across all categories.
2. Divide them into batches of up to 3. For example, 8 items → 3 batches (1-3, 4-6, 7-8).
3. For each batch, extract the full text of those sections from the recon file.
4. Launch all batch subagents **in parallel**, passing each one only its assigned items.
5. Each subagent writes to `{{ REPORTS_ROOT }}/18_batch_N.md` where N is the 1-based batch number.

Give each batch subagent the following instructions (substitute the batch-specific values):

> **Goal**: Verify the following inventory management findings and determine whether undocumented/debug/deprecated/assets, serverless functions, feature-flag-gated routes, or API gateway routes are reachable, specs are accurate, or non-production hosts expose production data. Write results to `{{ REPORTS_ROOT }}/18_batch_[N].md`.
>
> **Your assigned items** (from the recon phase):
>
> [Paste the full text of the assigned sections here, preserving the original numbering]
>
> **Context**: You will be given the project's architecture summary. Use it to understand deployment, routing, and environment handling.
>
> **Improper Inventory Management Reference — What to look for**:
>
> Focus on visibility and control gaps:
> - Assets that exist in code or deployments but are not documented or inventoried
> - Deprecated versions or debug endpoints reachable without the same security controls as production
> - OpenAPI/specs that are missing, manually maintained, or out of sync with code
> - Non-production hosts that use production data or are exposed to unauthorized networks
> - Third-party data flows that lack inventory, approval, or monitoring
> - Serverless function URLs, feature-flag-gated routes, and API gateway routes not reflected in inventory
>
> **Classification**:
> - **Vulnerable**: An undocumented/deprecated/debug endpoint is reachable, a spec is missing or inaccurate, a non-production host exposes production data, a third-party integration lacks inventory/approval, or a serverless/gateway/flag-gated route is exposed without inventory.
> - **Likely Vulnerable**: A strong indicator exists but reachability or data classification cannot be confirmed from code alone.
> - **Not Vulnerable**: Asset is documented, version is current/retired, debug endpoints disabled in production, specs are generated and accurate, non-prod hosts are isolated.
> - **Needs Manual Review**: Cannot determine with confidence (e.g., deployment configuration is external, host reachability must be tested live, data classification is not in code).
>
> **For each assigned item, check**:
>
> 1. **Is the asset documented in an inventory, OpenAPI spec, or runbook?**
> 2. **If it is a deprecated version or debug endpoint, is it disabled or protected in production?**
> 3. **If it is a non-production host, does it use production data or production credentials?**
> 4. **If documentation/spec exists, does it match the implemented routes?**
> 5. **Is there CI/CD automation that generates or validates the spec?**
> 6. **For third-party integrations, is there evidence of approval, data-flow inventory, or monitoring?**
> 7. **For serverless functions, feature flags, or gateway routes, are they listed in the API inventory and protected appropriately?**
>
> **Output format** — write to `{{ REPORTS_ROOT }}/18_batch_[N].md`:
>
> ```markdown
> # Improper Inventory Management Batch [N] Results
>
> ## Findings
>
> ### [VULNERABLE] Finding name
> - **File/Location**: `path/to/file` (lines X-Y) or `[deployment/external]`
> - **Issue**: [Clear description of the inventory gap]
> - **Impact**: [What an attacker or incident can cause — access via deprecated endpoint, data leak from staging, etc.]
> - **Proof**: [Show the code, config, or deployment evidence]
> - **Remediation**: [Specific fix — remove/disable, add to inventory, generate docs, isolate data, etc.]
> - **Dynamic Test**:
>   ```
>   [curl command, nmap command, DNS lookup, or step-by-step instructions to confirm this finding.
>    Include exact host/endpoint, headers, and expected evidence.
>    Use placeholders like <HOST>, <TOKEN>.]
>   ```
>
> ### [LIKELY VULNERABLE] Finding name
> - **File/Location**: `path/to/file` (lines X-Y) or `[deployment/external]`
> - **Issue**: [What indicator was found]
> - **Impact**: [Probable consequence]
> - **Proof**: [Evidence found]
> - **Remediation**: [Specific fix]
> - **Dynamic Test**:
>   ```
>   [Step-by-step or command to confirm]
>   ```
>
> ### [NOT VULNERABLE] Asset name
> - **File/Location**: `path/to/file` (lines X-Y) or `[deployment/external]`
> - **Protection**: [Why it is properly managed]
>
> ### [NEEDS MANUAL REVIEW] Asset name
> - **File/Location**: `path/to/file` (lines X-Y) or `[deployment/external]`
> - **Uncertainty**: [Why automated analysis couldn't determine the status]
> - **Suggestion**: [What to check manually]
> ```

### Phase 3: Merge — Consolidate Batch Results

After **all** Phase 2 batch subagents complete, read every `{{ REPORTS_ROOT }}/18_batch_*.md` file and merge them into a single `{{ REPORTS_ROOT }}/18_inventory.md`. You (the orchestrator) do this directly — no subagent needed.

**Merge procedure**:

1. Read all `{{ REPORTS_ROOT }}/18_batch_1.md`, `{{ REPORTS_ROOT }}/18_batch_2.md`, ... files.
2. Collect all findings from each batch file and combine them into one list, preserving the original classification and all detail fields.
3. Count totals across all batches for the executive summary.
4. Write the merged report to `{{ REPORTS_ROOT }}/18_inventory.md` using this format:

```markdown
# Improper Inventory Management Results: [Project Name]

## Executive Summary
- Assets analyzed: [total across all batches]
- Vulnerable: [N]
- Likely Vulnerable: [N]
- Not Vulnerable: [N]
- Needs Manual Review: [N]

## Findings

[All findings from all batches, grouped by classification:
 VULNERABLE first, then LIKELY VULNERABLE, then NEEDS MANUAL REVIEW, then NOT VULNERABLE.
 Preserve every field from the batch results exactly as written.]
```

5. After writing `{{ REPORTS_ROOT }}/18_inventory.md`, **delete all intermediate batch files** (`{{ REPORTS_ROOT }}/18_batch_*.md`).

---

## Prevention Guidance

- **Maintain an inventory of all API hosts**, including environment (production, staging, dev, test), intended network access (public, internal, partner), and running API version.
- **Inventory integrated services and data flows**, documenting role, exchanged data types, sensitivity, owner, and approval.
- **Document all API aspects**: authentication, errors, redirects, rate limiting, CORS policy, endpoints, parameters, requests, and responses.
- **Generate API documentation automatically** using open standards (OpenAPI/Swagger, AsyncAPI, GraphQL introspection). Include the documentation build in your CI/CD pipeline and fail builds on drift.
- **Restrict API documentation access** to authorized consumers; do not expose specs or Swagger UI to the public internet unless required.
- **Apply security controls to all exposed API versions**, not just the current production version. Deprecated versions must be retired or protected at the same level.
- **Establish a sunset / end-of-life (EOL) process** for deprecated API versions. Publish sunset dates, communicate them to consumers, monitor usage, and eventually return `410 Gone` or decommission the version. Do not leave deprecated versions active indefinitely.
- **Avoid using production data in non-production deployments**. If unavoidable, apply the same security controls as production and clearly mark the environment.
- **Perform risk analysis** when newer versions include security improvements, and backport or retire older versions accordingly.
- **Include serverless functions, feature flags, and API gateway routes** in the API inventory and documentation. Treat function URLs and gateway-declared paths as first-class API assets.

---

## References

- OWASP API Security Top 10 2023 — **API9:2023 Improper Inventory Management**: https://owasp.org/API-Security/editions/2023/en/0xa9-improper-inventory-management/
- [CWE-1059: Incomplete Documentation](https://cwe.mitre.org/data/definitions/1059.html)
- [CWE-1057: Data Access Operations Outside of Expected Data Manager Component](https://cwe.mitre.org/data/definitions/1057.html)

---

## Important Reminders

- Read `{{ REPORTS_ROOT }}/01_architecture.md` and pass its content to all subagents as context.
- Phase 2 must run AFTER Phase 1 completes — it depends on the recon output.
- Phase 3 must run AFTER all Phase 2 batches complete — it depends on all batch outputs.
- Batch size is **3 items per subagent**. If there are 1–3 items total, use a single subagent. If there are 10, use 4 subagents (3+3+3+1).
- Launch all batch subagents **in parallel** — do not run them sequentially.
- Each batch subagent receives only its assigned items' text from the recon file, not the entire recon file. This keeps each batch subagent's context small and focused.
- **All subagents are read-only**. They must never modify project source code, configuration, CI/CD pipelines, deployment manifests, or any other file in the repository.
- Inventory management is a **discovery-oriented** assessment. False negatives are common when assets are outside the codebase (CDNs, partner gateways, serverless functions). Mark external or unclear assets as "Needs Manual Review".
- When in doubt, classify as "Needs Manual Review" rather than "Not Vulnerable". Missing assets are harder to prove than present ones.
- Clean up intermediate files: delete `{{ REPORTS_ROOT }}/18_recon.md` and all `{{ REPORTS_ROOT }}/18_batch_*.md` files after the final `{{ REPORTS_ROOT }}/18_inventory.md` is written.
