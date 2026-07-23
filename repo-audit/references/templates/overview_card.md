---
subject: "Overview card templates; common skeleton, agent rules, table-heavy factual style, technology stack lockfile versions, standards protocols, directory tree, required resources, env prefixes, per-type sections, gRPC methods, REST endpoints, Temporal workflows activities, HelmRelease, library packages, `repos/<repo>/overview`."
index:
  - anchor: ra-tpl-overview-common
    what: "The common skeleton and agent rules every repo card follows regardless of type: purpose, type, stack, standards, tree, resources, env vars."
    problem: "Cards diverge between authors and eras; sections appear and vanish, versions get rounded, observability noise sneaks in; section roulette, version rounding, noise invasion, skeleton absence, style drift, format lottery, editorial chaos, uniformity decay."
    use_when: "Writing any repo overview card; reviewing card compliance; choosing what the common sections contain."
    avoid_when: "Type-specific interface sections — the five per-type anchors below; anomaly routing — `[ref: #entity-findings-traceability]`."
    expected: "Every card shares one concise, table-heavy, factual skeleton."
  - anchor: ra-tpl-overview-grpc
    what: "The gRPC-service section: exported services with method tables, declared-but-unimplemented methods, business logic."
    problem: "gRPC card lists methods loosely; unimplemented proto declarations vanish and consumers call into nowhere; incomplete tables, surface fog, phantom endpoints, contract erosion, declaration loss, consumer misdirection, coverage holes, inventory drift, stub fog."
    use_when: "Documenting a gRPC API service card; enumerating proto methods; marking aliases and unimplemented declarations."
    avoid_when: "Common sections — `ra-tpl-overview-common`; business-domain depth — business report templates."
    expected: "Complete method tables with protobuf message names and unimplemented declarations marked."
  - anchor: ra-tpl-overview-rest
    what: "The REST-gateway section: endpoint tables split by auth, authentication scheme."
    problem: "REST card piles routes without auth info; unauthenticated surface hides and security review misses exposure; auth fog, security blindness, endpoint sprawl, exposure blindness, route chaos, review failure, perimeter darkness, access confusion."
    use_when: "Documenting a REST API gateway card; grouping endpoints by router; recording auth per endpoint."
    avoid_when: "Full request/response schemas — method, path, auth, purpose only."
    expected: "Every route tabled with path, auth, and one-line purpose."
  - anchor: ra-tpl-overview-temporal
    what: "The Temporal-worker section: workflow and activity inventories, schedules, signals, business logic."
    problem: "Worker card names Python classes without Temporal semantics; signals and schedules stay hidden and operators cannot run system; class naming, hidden triggers, schedule blindness, operator fog, semantic loss, runtime opacity, platform ignorance, trigger fog."
    use_when: "Documenting a Temporal workflow worker card; mapping activities to downstreams; listing schedules and signals."
    avoid_when: "Retry policy internals — business logic section covers behavior-affecting rules only."
    expected: "Complete Temporal inventories with platform names and downstream mapping."
  - anchor: ra-tpl-overview-infra
    what: "The GitOps section: deployed services per environment, key files, infrastructure dependencies, conventions."
    problem: "Infra card degrades into directory dump; nobody can tell which releases run where with which images; release fog, environment confusion, deployment blindness, chart chaos, image fog, namespace drift, ops confusion."
    use_when: "Documenting an Infrastructure/GitOps card; grouping HelmReleases by namespace; recording charts and image tags."
    avoid_when: "Anomalies and gotchas — those route to findings namespaces per `[ref: #entity-findings-traceability]`."
    expected: "Every release tabled per environment with chart, image, and notes."
  - anchor: ra-tpl-overview-library
    what: "The library section: exported packages with public symbols, build/generation, conventions."
    problem: "Library card lists every generated message; public API surface drowns and consumers cannot find stable entry points; symbol flood, surface burial, consumer confusion, API fog, export sprawl, adoption friction, stability doubt, navigation pain."
    use_when: "Documenting a shared library card; grouping packages by domain; recording build and generation rules."
    avoid_when: "Generated internal helpers — omitted by design; runtime service sections — wrong type."
    expected: "Public packages tabled with purpose and important symbols."
---

# Overview Card Templates (repo-audit)

## Common skeleton and agent rules

[ref: #ra-tpl-overview-common]

Use this skeleton for **every** repo card, regardless of type (`grpc-service`, `rest-gateway`, `workflow-worker`, `infrastructure`, `library`). Combine it with the type-specific section below that describes the exported interface.

### Agent rules

- Write in **English**.
- The card MUST be concise, table-heavy, factual, and business-focused: use a table wherever a table can express the content; prose is allowed only where no table fits. No narrative essays, no filler, no restated code.
- Do **not** include upstream consumers of this repo.
- Do **not** include Sentry, Prometheus, or other observability-only dependencies.
- Do **not** include entry points (how to run the repo).
- Do **not** include development meta: Makefile, tests, linters, CI, pre-commit hooks, coverage, or editor config.
- For the directory tree: the ROOT agent generates it with the canonical command (`shell-protocol` `[ref: #tree-agent-rules]`; never delegated — `subagents-protocol` §13). Add a one-line responsibility comment for **meaningful** files/directories only. Skip empty `__init__.py`, `Makefile`, `Dockerfile`, `tests/`, CI files, entry-point files, and boilerplate.
- For environment variables, list only the **necessary/important** ones with their prefix. Do **not** write default values, example values, or secrets.
- For **Technology stack**, use categorical bullets with proper technology names; put libraries in parentheses with the version exactly as declared in `pyproject.toml`, `requirements/*.txt`, `uv.lock`, `package.json`, `go.mod`, or equivalent lockfiles. Do not normalize to `major.minor`, do not drop the patch, and do not invent versions.
- For **Standards and protocols**, state what is actually used in the repo, based on code evidence and authoritative sources (RFCs, vendor docs); use web search when necessary. Do not prescribe standards or guess.
- When you discover anomalies, TODOs, version drift, unused methods, ghost dependencies, important constraints, or other gotchas, **do not put them in the repo card**. Instead, write them to the appropriate Serena memory namespace as defined in `entity-protocol` `[ref: #entity-findings-traceability]`:
  - `bugs/<repo>/<topic>` — for bugs or broken/inconsistent behavior.
  - `notes/<repo>/<topic>` — for observations, surprising patterns, or important caveats.
  - `decisions/<repo>/<topic>` — for architectural decisions or trade-offs.
  - `style/<repo>/<topic>` — for project-specific style conventions.
  - `todo/<repo>/<topic>` — for TODOs or short actionable items from code/docs.
- All dates must be UTC ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`).
- Record git tracking metadata per the frontmatter-protocol tracking extension (`[ref: #tracking-fields]`, `[ref: #tracking-git-commands]`).

### Common skeleton

```markdown
# <repo-name> repo card

## Purpose

3–7 sentences describing what this repo does in business terms.

## Type

One of: `gRPC API service`, `REST API gateway`, `Temporal workflow worker`, `Infrastructure / GitOps`, `library`.

## Technology stack

Categorize every item. Use the proper technology/product name, and put the library/package in parentheses with the exact version as found in lockfiles/manifests. Do not round or normalize versions. Omit Sentry, Prometheus, lint, test, and CI tooling.

- **Language / runtime:** Python 3.12, asyncio.
- **API / web / workflow framework:** e.g. internal async gRPC server (`classic-grpc[async]` 0.1), FastAPI 0.10x, Temporal SDK (`temporalio` 1.x).
- **Database / storage:** e.g. PostgreSQL (SQLAlchemy 2.0, `psycopg[binary]` 3.1, Alembic 1.13), Google BigQuery 3.x, GCS, Redis, or `None`.
- **Config / secrets:** e.g. Pydantic Settings 2.x (`pydantic-settings` 2.x), `classic-vaults[async]` 1.0.
- **Orchestration (if used):** Temporal client/worker (`temporalio` 1.x) — namespace/task queue are listed in Required resources.
- **External business integrations:** e.g. TronGrid HTTP API, Zitadel OAuth2, SendGrid, Sumsub, FraudAverse, Coinbase API, OpenExchangeRates.
- **Explicitly not used:** state when there is no local DB, no REST framework, no message broker, etc.

**Do not list:** Sentry, Prometheus, pytest, ruff, black, mypy, bandit, Makefile, Docker, CI, pre-commit hooks.

## Standards and protocols

Record the formal standards, protocols, or cryptographic schemes that are **actually used** by this repo, as evidenced by the code. This section is a statement of fact, not a recommendation. For each item, indicate where in the code it is used (file/function/flow), cite the authoritative source (RFC, PEP, ISO, vendor spec, official docs), and include the **current commit hash of the referenced file** — stamped by the ROOT agent at synthesis per `entity-protocol` `[ref: #entity-findings-traceability]`; the exploration subagent supplies only `path:line` + symbol.

Examples of what to capture:

- OAuth 2.0 token introspection (RFC 6749, RFC 7662) — used in Zitadel auth flow; see `app/oauth/validator.py`.
- JWT signed with RS256 (RFC 7515, RFC 7519) — JWT generation; see `app/oauth/token.py`.
- RSA-PSS with SHA-256 (RFC 8017) — request/response signature verification; see `app/signature/rsa.py`.
- JSON Schema validation (draft-07, draft-2020-12, etc.) — requisites validation; see `app/requisites_validator/`.
- gRPC over HTTP/2.
- Temporal gRPC service protocol.
- OpenID Connect / Zitadel-specific flows.

## Directory structure

<repo-name>/
├── app/
│   ├── api/              # gRPC routing / REST routers / workflow glue
│   ├── core/             # business logic and domain services
│   ├── domain/           # dataclasses, enums, models
│   └── storages/         # DB/storage implementation
├── migrations/           # Alembic migrations (if any)
└── ...

- Add a brief comment only for directories/files that carry real responsibility.
- Skip `__init__.py`, `main.py`, `worker.py`, `entrypoint.sh`, `Dockerfile`, `Makefile`, `pyproject.toml`, test files, CI files, lint config, etc.

## Required resources / suppliers

List every resource this repo **uses** or **requires** to run.

| Resource | Nature | Details |
|----------|--------|---------|
| `<repo>` | downstream gRPC | `ProtoService`: methods used |
| `<edge_api>` | external HTTP | endpoint + auth summary |
| `Temporal cluster` | orchestration | namespace, task queue, workflows/updates/signals used |
| `HashiCorp Vault` | secrets | what secrets are injected |
| `PostgreSQL` | database | tables owned, or `None` |
| `Redis` | cache / idempotency | usage summary, or `None` |

- Do **not** list upstream callers here.
- For databases, name the tables only if the repo owns them; otherwise treat DB as a required resource.

## Important environment variables

Prefix: `<REPO_NAME_>*`

- `<REPO_NAME>_DB_NAME` / `_DB_ADDR` / `_DB_DSN` / `_DB_CREDENTIALS`
- `<REPO_NAME>_TEMPORAL_NAMESPACE` / `_TEMPORAL_TASK_QUEUE` / `_TEMPORAL_CLUSTER_URL`
- `<REPO_NAME>_SERVICE_<DOWNSTREAM>_HOST` / `_PORT`
- `<REPO_NAME>_VAULTS`
- etc.

Rules:
- Include only variables required for operation.
- Do **not** write values, defaults, examples, or secrets.
- Each environment variable should have a short, consistent description: what it is, why it matters, and what behavior it controls.

## What is intentionally omitted from the common skeleton

The following are handled by the type-specific sections:

- **Resources provided / exported interface**
  - gRPC service: service name + method table.
  - REST gateway: endpoint table (method, path, auth/notes).
  - Worker: workflows + activities + signals/queries/cron/updates.
  - Infrastructure: list of deployed services and environments.
  - Library: public packages/modules and build conventions.
- **Business logic / state machines / status values** — add only when relevant to the type-specific section.
```

## gRPC API service

[ref: #ra-tpl-overview-grpc]

Use the common skeleton and agent rules above (`[ref: #ra-tpl-overview-common]`) first. This section adds only the gRPC-specific sections.

### Type-specific additions

#### Exported gRPC service(s)

For every gRPC service exposed by the application, create a subsection.

```markdown
## Exported gRPC service: `<ServiceName>`

- **Proto package:** e.g. `classic.grpc.stubs.adverts`
- **Server framework:** internal async/sync gRPC server (`classic-grpc[async]` 0.1 / `classic-grpc[sync]` 0.1)
- **Platform servicers also exposed:** `HealthServicer`, `InjectableServicer`

#### Implemented / routed methods

| Method | Request | Response | Handler | Notes |
|--------|---------|----------|---------|-------|
| `CreateOrder` | `CreateOrderRequest` | `order_pb2.IdMessage` | `handlers.create_order` | — |
| ... | ... | ... | ... | ... |

#### Declared but not implemented

| Method | Reason / status |
|--------|-----------------|
| `UpdateNickname` | Mapped in routes but not declared in pinned proto; unreachable. |
| ... | ... |
```

Rules:
- Include both implemented and declared-but-unimplemented proto methods.
- Mark method aliases if the same handler answers multiple proto names.
- Keep request/response types as protobuf message names, not raw fields.

#### Business logic / state machines (if relevant)

Add only when the domain has explicit rules worth documenting:

```markdown
## Business logic

- Status workflow: `NEW → PROCESSING → RESOLVED / REJECTED`.
- `UpdateType` rejects changing type to `DISPUTE` for existing cases.
- `DeleteClientPaymentMethod` transitions status only from `ACTIVE` or `CLOSING`.
```

Do not duplicate the method table here; only domain rules, status values, and lifecycle constraints.

## REST API gateway

[ref: #ra-tpl-overview-rest]

Use the common skeleton and agent rules above (`[ref: #ra-tpl-overview-common]`) first. This section adds only the REST-gateway-specific sections.

### Type-specific additions

#### Exported REST API

Split into public/unauthenticated endpoints and authenticated `/api/v1` endpoints.

```markdown
## Exported REST API

#### Health / misc (unauthenticated)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/ping` | Liveness probe |
| GET | `/api/version` | Service version |
| GET | `/healthcheck` | Health check |
| GET | `/status` | Health + dependency status |
| POST | `/secret` | Vault injector callback |

#### `/api/v1/orders`

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| GET | `/api/v1/orders` | OAuth2 | List orders |
| GET | `/api/v1/orders/{order_id}` | OAuth2 | Get order |
| PATCH | `/api/v1/orders/{order_id}/status` | OAuth2 | Close order by bartender |
| ... | ... | ... | ... |
```

Rules:
- Group endpoints by router/domain.
- Include auth requirement per endpoint (e.g. `none`, `OAuth2`, `RSA-PSS`, `HMAC`).
- For path parameters, use `{param}` notation.
- Do not list full request/response schemas — only path, method, auth, and one-line purpose.

#### Authentication scheme (if relevant)

```markdown
## Authentication

- Zitadel OAuth2 bearer token introspection via `authlib`/`pyjwt` (RS256).
- RSA-PSS SHA-256 request/response signing for merchant endpoints.
- HMAC webhooks for KYC/KYT callbacks.
```

Add only the scheme that is actually used, with a reference to the code files where it is implemented.

## Temporal workflow worker

[ref: #ra-tpl-overview-temporal]

Use the common skeleton and agent rules above (`[ref: #ra-tpl-overview-common]`) first. This section adds only the worker-specific sections.

### Type-specific additions

#### Temporal workflows

```markdown
## Temporal workflows

| Temporal name | Class | Purpose | Signals | Updates | Queries | Cron / schedule |
|---------------|-------|---------|---------|---------|---------|-----------------|
| `payin` | `Payin` | Merchant pay-in processing | — | `accept_payin_order`, `reject_payin_order` | — | — |
| `exchange` | `Exchange` | P2P exchange lifecycle | — | `accept_order_by_user`, `confirm_order_by_buyer`, ... | — | — |
| ... | ... | ... | ... | ... | ... | ... |
```

Rules:
- Use the Temporal workflow name, not only the Python class name.
- List signals, updates, queries, and cron/schedule triggers if they exist.
- Mark placeholder/stub workflows explicitly.

#### Temporal activities

```markdown
## Temporal activities

| Activity name | Function | Downstream resource | Purpose |
|---------------|----------|---------------------|---------|
| `get_client_by_id` | `activities.important_api.get_client_by_id` | `important_api` (`ImportantService.GetClientById`) | Fetch client record |
| `create_order` | `activities.orders_api.create_order` | `orders_api` (`OrdersService.CreateOrder`) | Create payin order |
| ... | ... | ... | ... |
```

Rules:
- Use the Temporal activity name.
- Map each activity to the downstream service/method it calls.
- Group activities by downstream domain if there are many.
- Mark activities that are defined but not registered in the worker.

#### Schedules, signals, queries

```markdown
## Cron schedules

- `generate new pizza` — `@every 1m`
- `collect empty bottles` — `@every 5m`

## Signals

- `unlock_transfer` → `Clearing`
- `confirm_refund_start` → `Deposit`
```

#### Business logic / state machines (if relevant)

Add only explicit domain rules, e.g. order status flows, retry/timeout policies that affect behavior, or idempotency rules.

```markdown
## Business logic

- Idempotency key for deposits: `deposit:{tx_hash}:{log_index}`.
- `Clearing` calls `continue_as_new` on FAILED transfers.
```

## Infrastructure / GitOps

[ref: #ra-tpl-overview-infra]

Use the common skeleton and agent rules above (`[ref: #ra-tpl-overview-common]`) first. This section adds only the infrastructure-specific sections.

### Type-specific additions

#### Deployed services / environments

```markdown
## Deployed backend services

#### Namespace `important` (production)

| Release | Helm chart | Image tag | Notes |
|---------|------------|-----------|-------|
| `important-api` | `important-api` | 0.0.12 | — |
| `important-wf` | `temporal-worker` | 8.2.0 | Queue `default`, namespace `important-api` |
| ... | ... | ... | ... |

#### Frontends (namespace `frontend`)

| Release | Helm chart | Image | Ingress host |
|---------|------------|-------|--------------|
| `important-nginx` | `nginx` | `important-nginx` | `kalaver.in`, `www.kalaver.in` |
| ... | ... | ... | ... |
```

Rules:
- Group by namespace/environment.
- Include chart name and image tag.
- Add a short note for special configuration (queue, namespace, ingress gateway, etc.).

#### Key files / entry points

```markdown
## Key files

| File | Purpose |
|------|---------|
| `clusters/classic-prod/important-apps.yaml` | Root Flux Kustomization |
| `apps/classic-prod/important/kustomization.yaml` | Aggregates backend HelmReleases |
| `apps/base/important/<service>/release.yaml` | Per-service base HelmRelease |
```

#### Infrastructure dependencies

```markdown
## Infrastructure dependencies

| Component | Nature | Details |
|-----------|--------|---------|
| Flux CD | GitOps engine | `important-apps` Kustomization |
| Kubernetes | Runtime | `classic-prod` cluster |
| Helm | Packaging | `gar` HelmRepository in `flux-system` |
| Istio | Service mesh | Sidecars, VirtualServices, ingress gateways |
| HashiCorp Vault | Secrets | `vault-injector` |
| PostgreSQL | Database | `1.1.1.1:5432`; per-app DB names |
```

#### Conventions

```markdown
## Conventions

- Base + overlay GitOps pattern.
- One HelmRelease per app; `metadata.name` == `spec.releaseName`.
- Temporal workers use chart `temporal-worker` 0.6.2.
- Dedicated `important` nodegroup via taints/tolerations.
```

Do not list anomalies or gotchas here — route them to the appropriate repo-scoped namespace as defined in `entity-protocol` `[ref: #entity-findings-traceability]`.

## Shared library

[ref: #ra-tpl-overview-library]

Use the common skeleton and agent rules above (`[ref: #ra-tpl-overview-common]`) first. This section adds only the library-specific sections for shared code libraries (e.g., `modern-grpc`, `classic-grpc`) that do not expose a runtime service or worker.

### Type-specific additions

#### Exported packages / modules

Describe the public API surface of the library:

```markdown
## Exported packages

| Package / module | Purpose | Public symbols |
|------------------|---------|----------------|
| `modern.common.pizza.v1` | Billing domain protobuf messages and gRPC stubs | `PizzaServiceStub`, `PizzaServiceServicer`, `CreateOrderRequest`, ... |
| `modern.secure.pepsi.v1` | Wallet domain protobuf messages and gRPC stubs | `PepsiServiceStub`, `FantaServiceStub`, ... |
```

Rules:
- Group by domain or directory.
- List the most important public symbols (classes, functions, constants) that consumers rely on.
- Do not list generated internal helpers or every single message.

#### Build / generation (if relevant)

```markdown
## Build and generation

- Python stubs generated by `buf` with plugins `grpc/python` and `protocolbuffers/python`.
- Go stubs generated by `protoc-gen-go` and `protoc-gen-go-grpc`.
- Generated artifacts are committed under `gen/python/` and `gen/go/`.
```

#### Conventions

```markdown
## Conventions

- Proto files are the source of truth.
- Buf v2 workspace with `STANDARD` lint and `FILE` breaking-change detection.
- Python package uses PEP 420 implicit namespace packages.
- Version is declared in `pyproject.toml`; Go module version is tracked via git tags.
```

Do not list anomalies or gotchas here — route them to the appropriate repo-scoped namespace as defined in `entity-protocol` `[ref: #entity-findings-traceability]`.
