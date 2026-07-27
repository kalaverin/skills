---
subject: "Repo type detection and interface exhaustiveness; preset types plus `custom:<slug>` open labels, deterministic shell-probe algorithm, closed facet registry of interface surfaces (http-in, rpc-in, bot-handlers, llm-agent-tools, storage-schema, deployment-units, and more), per-facet exhaustive extraction rules, preset facet bundles, user-confirmation rule for custom vectors."
index:
  - anchor: repo-type-detection
    what: "The two-layer repo taxonomy: five preset types as named facet bundles plus open `custom:<slug>` labels, the deterministic probe algorithm, and the rule that custom types are confirmed with the user before the pipeline proceeds."
    problem: "Closed type lists break on real projects — standalone Telegram bot or any unusual shape forces undocumented deviations or wrong templates; taxonomy rigidity, deviation debt, wrong card sections, stalled pipelines, project diversity, classification gaps."
    use_when: "Phase 0 of any audit run — type and facet vector are determined once, at the very start; confirming a repo type; registering a custom label for an unusual project."
    avoid_when: "Per-facet extraction requirements — sibling anchor below; business-domain classification — domain subagents own that."
    expected: "Exactly one type label plus an explicit facet vector, confirmed with the user for custom types, before any wave launches."
  - anchor: repo-interface-exhaustiveness
    what: "The closed registry of interface facets — detection signals and exhaustive extraction rule per facet — plus the preset bundles mapping each named type to its facets; summarization is FORBIDDEN."
    problem: "Explorer summarizes instead of enumerating, or extraction rules tied to type names silently skip surfaces project actually has; incomplete interfaces, silent omissions, coverage gaps, surface blindness, downstream defects, exhaustiveness breach, template mismatch, validation failure."
    use_when: "Tech explorer extracting exported interfaces; dependency extractor listing surface; validating report completeness against the facet rules."
    avoid_when: "Type determination itself — sibling anchor above; business-domain extraction — `analysis/domain.md` prompts."
    expected: "Every surface present in the facet vector is enumerated completely — every route, method, handler, job, model, unit — with zero summarization."
---

# Repo Type Detection & Interface Facets

[ref: #repo-type-detection]

The type system has two layers: a **type label** (what the repo is called) and a **facet vector** (which interface surfaces it actually has). The label routes presentation; the facet vector drives exhaustiveness (next section).

**Preset types** (fixed display strings, backward compatible):

| Preset | Facet bundle |
|---|---|
| `gRPC API service` | `rpc-in` + `public-api-surface` |
| `REST API gateway` | `http-in` |
| `Temporal workflow worker` | `workflow-pipelines` + `outbound-integrations` |
| `library` | `public-api-surface` (+ build/generation rules) |
| `Infrastructure / GitOps` | `deployment-units` + `iac-config` |

**Custom types:** any project outside the presets gets `custom:<slug>` (kebab-case, e.g. `custom:telegram-bot`, `custom:chrome-extension`, `custom:cli-tool`) plus an explicit facet vector chosen from the registry below.

**Detection algorithm** (exact order, safe read-only shell probes only — `lsd`, `test -d`, `test -f`, no source reads):

1. `IF` directory contains `apps/base/` or `clusters/` AND NO `app/` source tree → **Infrastructure / GitOps**
2. `ELSE IF` directory contains `proto/` AND NO `app/` OR `worker.py` → **library**
3. `ELSE IF` directory contains `app/api/` (with FastAPI/Flask routers) OR `main.py`/`server.py` exposing HTTP → **REST API gateway**
4. `ELSE IF` directory contains `worker.py` OR `app/workflow/` with `@workflow.defn` → **Temporal workflow worker**
5. `ELSE IF` directory contains `app/` with gRPC servicers / runtime-served proto stubs → **gRPC API service**
6. `ELSE` → **custom**: detect facets by the registry's signal column, then STOP and confirm with the user (below).

**Custom-type confirmation rule (HARD):** for any custom type, halt before launching waves and present the user: the proposed `custom:<slug>`, the facets detected with their evidence, and the resulting facet vector. Ask the user to confirm, correct, or add facet groups to the custom bundle. Only after explicit user confirmation does the pipeline proceed. Never silently default a custom vector.

The type and facet vector are determined ONCE, at the very start of the pipeline (Phase 0), and passed downstream as `repo_type` and `interface_facets`; downstream subagents consume both values and never re-derive them.

## Interface Facet Registry

[ref: #repo-interface-exhaustiveness]

The exploring subagent MUST extract every interface of every facet in the vector, per the rules below. Summarization is FORBIDDEN. A facet absent from the vector is not explored; a facet present in the vector is exhausted completely.

### Inbound surfaces

| Facet | Detection signals | Exhaustive requirement |
|---|---|---|
| `http-in` | Routers, `@app.route`, controllers, OpenAPI | EVERY route; split unauthenticated vs authenticated; `{param}` notation; auth type per endpoint. |
| `rpc-in` | `.proto`, servicers, runtime stubs | EVERY method; separate table for methods declared but NOT implemented; message names, not field definitions. |
| `graphql-in` | Schemas, resolvers, federation config | EVERY query/mutation/subscription; auth per operation; sensitive fields marked. |
| `websocket-sse` | `ws://` handlers, channels, SSE endpoints | EVERY channel/stream: handshake auth, message types, lifecycle. |
| `bot-handlers` | Command/callback decorators, aiogram, telegraf, slack-bolt, discord.py | EVERY command/callback handler: trigger, auth/role checks, side effects. |
| `cli-commands` | `argparse`, `click`, `cobra`, `bin/` entry points | EVERY command/subcommand: args, side effects, privilege assumptions. |
| `queue-consumer` | Kafka/RabbitMQ/SQS/NATS/pub-sub consumers | EVERY consumer: topic/queue, payload schema, idempotency, DLQ handling. |
| `event-handlers` | Inbound webhooks, event callbacks | EVERY handler: source, signature verification, payload schema. |
| `cron-scheduler` | cron, `@scheduled`, celery beat, systemd timers | EVERY job: schedule, side effects, concurrency/overlap policy. |

### Execution model

| Facet | Detection signals | Exhaustive requirement |
|---|---|---|
| `workflow-pipelines` | Temporal workflows, Airflow DAGs, Celery chains, StepFunctions | EVERY workflow/pipeline: triggers, signals/queries/updates, activity map to downstream calls, cron schedules. |
| `llm-agent-tools` | Function/tool definitions, MCP servers, agent loops | EVERY tool: input schema, auth, side effects; agent entry points and loop bounds. |
| `ui-routes` | SPA page routing (React/Vue/Angular router) | EVERY route/page: data dependencies, auth guards. |
| `auth-flows` | JWT issuance/validation, OAuth flows, session management, password reset | EVERY flow: token types, storage, refresh/rotation, expiry. |

### Outbound and data

| Facet | Detection signals | Exhaustive requirement |
|---|---|---|
| `outbound-integrations` | Third-party HTTP clients, outbound webhooks, SDK calls | EVERY integration: endpoint, auth, data sent, retry/timeout policy. |
| `storage-schema` | ORM models, migrations, table schemas | EVERY model/table: sensitive fields marked (PII, credentials, tokens). |
| `cache-kv` | Redis/Memcached/in-memory caches | EVERY cache: keyspace, TTL, invalidation strategy. |
| `data-feeds` | CSV/XML/ETL import-export pipelines | EVERY feed: format, validation, schedule/trigger. |

### Public surface and deployment

| Facet | Detection signals | Exhaustive requirement |
|---|---|---|
| `public-api-surface` | Library exports, public modules, package index | EVERY public package/module; omit generated internal helpers; include build/generation rules (`buf`, `protoc-gen-go`). |
| `plugin-extension-points` | Plugin systems, hooks, codegen, KSP, script engines | EVERY extension point: contract, trust boundary, load path. |
| `deployment-units` | Helm charts, Dockerfiles, K8s manifests, serverless configs | EVERY unit grouped by environment/namespace (as `HelmRelease` for GitOps). |
| `iac-config` | Terraform, CloudFormation, Pulumi, ARM | EVERY module/stack: resources and security-relevant parameters. |

Facet registration is closed: a new facet is added only with explicit user approval, recorded as a change to this file.
