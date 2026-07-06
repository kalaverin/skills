# Common entity-card template (agent prompt)

[ref: #pe-common]

Use this skeleton for **every** entity card, regardless of type (`grpc-service`, `rest-gateway`, `workflow-worker`, `infrastructure`, `library`). Combine it with the type-specific template that describes the exported interface.

## Agent rules

[ref: #pe-common-agent-rules]

- Write in **English**.
- Do **not** include upstream consumers of this entity.
- Do **not** include Sentry, Prometheus, or other observability-only dependencies.
- Do **not** include entry points (how to run the entity).
- Do **not** include development meta: Makefile, tests, linters, CI, pre-commit hooks, coverage, or editor config.
- For the directory tree, use the `tree --gitignore --prune --condense --compress 3 --dirsfirst -vnx` command. Add a one-line responsibility comment for **meaningful** files/directories only. Skip empty `__init__.py`, entry-point files, and boilerplate.
- For environment variables, list only the **necessary/important** ones with their prefix. Do **not** write default values, example values, or secrets.
- For **Technology stack**, use categorical bullets with proper technology names; put libraries in parentheses with the version exactly as declared in `pyproject.toml`, `requirements/*.txt`, `uv.lock`, `package.json`, `go.mod`, or equivalent lockfiles. Do not normalize to `major.minor`, do not drop the patch, and do not invent versions.
- For **Standards and protocols**, state what is actually used in the entity, based on code evidence and authoritative sources (RFCs, vendor docs); use web search when necessary. Do not prescribe standards or guess.
- When you discover anomalies, TODOs, version drift, unused methods, ghost dependencies, important constraints, or other gotchas, **do not put them in the entity card**. Instead, write them to the appropriate Serena memory namespace as defined in `serena-protocol` `[ref: #serena-findings-traceability]`:
  - `bugs/<entity>/<topic>` — for bugs or broken/inconsistent behavior.
  - `notes/<entity>/<topic>` — for observations, surprising patterns, or important caveats.
  - `decisions/<entity>/<topic>` — for architectural decisions or trade-offs.
  - `style/<entity>/<topic>` — for project-specific style conventions.
  - `todo/<entity>/<topic>` — for TODOs or short actionable items from code/docs.
- All dates must be UTC ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`).
- Always record the current git branch and latest short commit hash in `Latest commit` with commit datetime.

## Common skeleton

[ref: #pe-common-skeleton]

```markdown
# <entity-name> entity card

## Purpose

3–7 sentences describing what this entity does in business terms.

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

Record the formal standards, protocols, or cryptographic schemes that are **actually used** by this entity, as evidenced by the code. This section is a statement of fact, not a recommendation. For each item, indicate where in the code it is used (file/function/flow), cite the authoritative source (RFC, PEP, ISO, vendor spec, official docs), and include the **current commit hash of the referenced file** (`git log -1 --format=%H -- <relative-path>`).

Examples of what to capture:

- OAuth 2.0 token introspection (RFC 6749, RFC 7662) — used in Zitadel auth flow; see `app/oauth/validator.py`.
- JWT signed with RS256 (RFC 7515, RFC 7519) — JWT generation; see `app/oauth/token.py`.
- RSA-PSS with SHA-256 (RFC 8017) — request/response signature verification; see `app/signature/rsa.py`.
- JSON Schema validation (draft-07, draft-2020-12, etc.) — requisites validation; see `app/requisites_validator/`.
- gRPC over HTTP/2.
- Temporal gRPC service protocol.
- OpenID Connect / Zitadel-specific flows.

## Directory structure

<entity-name>/
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

List every resource this entity **uses** or **requires** to run.

| Resource | Nature | Details |
|----------|--------|---------|
| `<entity>` | downstream gRPC | `ProtoService`: methods used |
| `<edge-api>` | external HTTP | endpoint + auth summary |
| `Temporal cluster` | orchestration | namespace, task queue, workflows/updates/signals used |
| `HashiCorp Vault` | secrets | what secrets are injected |
| `PostgreSQL` | database | tables owned, or `None` |
| `Redis` | cache / idempotency | usage summary, or `None` |

- Do **not** list upstream callers here.
- For databases, name the tables only if the entity owns them; otherwise treat DB as a required resource.

## Important environment variables

Prefix: `<ENTITY_NAME_>*`

- `<ENTITY_NAME>_DB_NAME` / `_DB_ADDR` / `_DB_DSN` / `_DB_CREDENTIALS`
- `<ENTITY_NAME>_TEMPORAL_NAMESPACE` / `_TEMPORAL_TASK_QUEUE` / `_TEMPORAL_CLUSTER_URL`
- `<ENTITY_NAME>_SERVICE_<DOWNSTREAM>_HOST` / `_PORT`
- `<ENTITY_NAME>_VAULTS`
- etc.

Rules:
- Include only variables required for operation.
- Do **not** write values, defaults, examples, or secrets.
- Each environment variable should have a short, consistent description: what it is, why it matters, and what behavior it controls.

## What is intentionally omitted from the common skeleton

The following are handled by the type-specific templates:

- **Resources provided / exported interface**
  - gRPC service: service name + method table.
  - REST gateway: endpoint table (method, path, auth/notes).
  - Worker: workflows + activities + signals/queries/cron/updates.
  - Infrastructure: list of deployed services and environments.
  - Library: public packages/modules and build conventions.
- **Business logic / state machines / status values** — add only when relevant to the type-specific template.
