---
name: service-layout
description: "MANDATORY normative standard for how a company Python service MUST look: canonical package layout, import borders, domain models, mappings, ports/DI, errors, settings/secrets, persistence/UoW, lifecycle, observability — ruling ids L/I/D/M/P/E/S/T/Y/O. Use when designing a new service, scaffolding greenfield code, or reviewing an existing service. On activation the FULL standard applies in every scenario; every violation is reported by ruling id."
triggers:
  request: "service layout, service structure, структура сервиса, лейаут сервиса, как должен выглядеть сервис, новый сервис, создай сервис, создаём сервис, проектируем сервис, спроектируй сервис, проектирование сервиса, каркас сервиса, service scaffold, scaffolding, greenfield service, service design, company service standard, service standard, ревью сервиса, проверь сервис, service review, layout review, composition root, порты и адаптеры, hexagonal service"
  reason: "Design, greenfield development, and review of company services must conform to the Company Service Layout Standard."
runtime: true
version: 0.1.0
---

# SKILL: Company Service Layout Standard

Normative standard for how every company service MUST look: layout, layering, domain models, mappings, ports/DI, errors, settings, persistence, lifecycle, observability.
Ruling ids: one letter per dimension plus a number — **L** layout, **I** imports, **D** domain models, **M** mappings, **P** ports/DI, **E** errors, **S** settings, **T** persistence/storage, **Y** lifecycle, **O** observability.
Normative keywords (`MUST`, `SHOULD`, `MAY`) follow RFC 2119 / RFC 8174 (by `read-for-comments`).

## Skill Boundary

[ref: #sly-boundary]

- This skill owns the normative STRUCTURE of a service: package layout, import direction and borders, domain model shapes, mapping rules, ports and DI, error taxonomy, settings and secrets, persistence and UoW, entrypoint and lifecycle, observability wiring.
- This skill does NOT own Python code style (→ `python-lang`), the review workflow and report format (→ `code-review`), API resource design (→ `api-design`), or protobuf schema style (→ `protobuf-lang`). Those load alongside via their own triggers.
- The standard is anchored to Python services (gRPC and FastAPI). For another language, apply the structural rulings and ask the user about idiomatic mapping.

## Activation Scenarios

[ref: #sly-scenarios]

- On activation the ENTIRE standard is in force. Selective application is FORBIDDEN: in every scenario you check ALL rulings (L/I/D/M/P/E/S/T/Y/O; profile-conditional ones per the detected profile) and the WHOLE anti-pattern registry, and you MUST detect and report EVERY violation found, each cited by its ruling id.
- **Design:** propose service skeletons only per the canonical layout; every proposed element cites the ruling ids it satisfies.
- **Greenfield development:** scaffold per the profile tree; the Conformance Checklist is the definition of done.
- **Code review:** check the changeset or service against every ruling and the registry; findings cite ruling ids; the Conformance Checklist is the final gate.
- The scenario changes ONLY the output shape (proposal, scaffold plan, findings list) — never the set of rules applied.

## Profile Detection

[ref: #sly-profiles]

- Before applying profile-conditional rulings, classify the service at hand. The profile is the decision criterion for what applies — you make this classification yourself.
- **Profile A — gRPC resource service (stateful):** owns a Postgres DB, serves gRPC.
- **Profile B — REST gateway / BFF (stateless):** FastAPI over downstream gRPC/HTTP/Temporal, no local DB.
- The primary classification signal is DB ownership: the service owns a Postgres DB (`migrations/` + `storages/`) → A; no local DB, FastAPI over downstream gRPC/HTTP/Temporal → B. Upstream clients under `services/` appear in both profiles and never decide alone; serving REST alongside gRPC does not change A while the service owns its DB.
- Legacy non-conformant services exist (3-tier with ORM-as-domain, bespoke adapters without `core/`/`storages/`); the migration target is Profile A — never invent a third profile (L5).
- Profile-conditional rulings: L4, T1, P4, M4, and the layout trees; L5 applies only to legacy services. Every other ruling applies unconditionally to both profiles.
- On ambiguous classification, ask the user — never guess the profile.
- Out of scope of this standard: Temporal workers, shared libraries, GitOps configs.

## Canonical Layout

[ref: #sly-layout]

- The layout exists to keep `domain/` and `core/` unit-testable without infrastructure: ports accept fake implementations, so tests never touch network or DB.

### Package roots

[ref: #sly-package-roots]

- `app/` — the application code (L1, MUST).
- `src/<module>/` — isolated project-specific component packages (e.g. a client module for some API), at project root. One-way isolation: `app/` MAY import from `src/`; `src/` MUST NEVER import from `app/` (enforced, I4).
- `sdk/<provider>/` — general, extractable third-party/provider toolkits, at project root (L3). `sdk/` imports nothing project-side. The split: `src/` is project-specific, `sdk/` is general/reusable.

### Profile A tree

[ref: #sly-profile-a-tree]

```text
<service>/
├── app/
│   ├── domain/                 # pure: frozen dataclasses + StrEnum, stdlib imports only
│   ├── core/                   # use cases + ports (the hexagon)
│   │   ├── <aggregate>.py      #   business logic over ports
│   │   ├── repo.py             #   @runtime_checkable Protocol repos (one per aggregate)
│   │   ├── storage.py          #   Storage Protocol aggregating the repos
│   │   └── transaction_manager.py  # TransactionManager Protocol (UoW)
│   ├── storages/<backend>/     # persistence adapters (postgres/, object storage, ...); skip if stateless
│   ├── services/               # outbound adapters: grpc/<upstream>/, http/<thirdparty>/ (only if used)
│   ├── api/                    # the ONLY delivery package
│   │   ├── errors/             # edge concerns defined ONCE, shared by all transports
│   │   ├── health/
│   │   ├── auth/
│   │   ├── grpc/<entity>/      # servicers.py (thin) + models.py (view assembly) + views.py (pb2 serializers)
│   │   │   └── interceptors/   # logging, exception mapping
│   │   └── http/               # only when the service truly serves REST too
│   ├── bootstrap.py            # composition root: build_provider(config)
│   ├── server.py               # entrypoint: sentry, settings, secrets, bootstrap, serve; owns shutdown
│   ├── settings.py             # pydantic-settings; grows into settings/ package per concern
│   ├── secrets.py              # vault resolution, fail-fast at startup
│   ├── errors.py               # ApplicationError hierarchy
│   └── version.py              # single version source
├── src/<module>/               # isolated project-specific modules (optional)
├── sdk/<provider>/             # general provider toolkits (optional)
├── migrations/                 # alembic (only when the service owns a DB)
├── tests/
└── etc/                        # lint configs
```

### Profile B tree

[ref: #sly-profile-b-tree]

Same skeleton minus `storages/` and `migrations/` (stateless, T1); `app/services/grpc|http/<upstream>/` is MANDATORY and carries the anti-corruption mappers (`mappers.py` next to the client code); delivery is `app/api/http/v1/<domain>/{handlers,schemas,models}.py` — handlers thin, `schemas.py` = input contracts, `models.py` = output contracts. Note: `models.py` is per-transport vocabulary — view assembly in Profile A gRPC, the output contract in Profile B REST.

### Naming rulings

[ref: #sly-naming-rulings]

- `api/` is the only legal delivery package; a top-level `grpc_api/` is FORBIDDEN (L2, MUST NOT) — `<service>/grpc_api/` at the repository root is the canonical violation.
- Transports are siblings inside `api/`: `api/grpc/`, `api/http/`; shared edge concerns live once at the `api/` root (L2).
- One backend = one technology-named adapter package (`storages/postgres/`, never ORM-named) (L3, T1).
- Profile B keeps the Profile A skeleton minus `storages/` (stateless); `services/grpc|http/<upstream>/` is obligatory for upstream calls (L4, MUST).
- Legacy non-conformant services migrate toward Profile A; a third profile is MUST NOT (L5).

## Rulings

[ref: #sly-rulings]

### Import direction and borders (I1–I4)

[ref: #sly-ruling-imports]

- **I1 (MUST)** Import direction: `api/ → core/ → domain/`; adapters (`storages/`, `services/`) import `core/` ports and `domain/` models; `domain/` imports stdlib ONLY. `app/ → src/` is one-way; `sdk/` imports nothing project-side.
- **I2 (MUST)** Anti-corruption: pb2 / ORM / HTTP-client types live and convert only at their own boundary — pb2 in `api/grpc/<entity>/views.py` and `services/grpc/<upstream>/mappers.py`, ORM in `storages/<backend>/`, HTTP types in `services/http/`. A pb2 import inside `domain/` is a blocking defect.
- **I3 (MUST NOT)** Reverse imports: `services/` never imports `api/`; `core/` never imports adapters.
- **I4 (MUST)** Enforcement: import-linter in `pyproject.toml` `[tool.importlinter]` — `root_packages`, an exhaustive layered contract (a forgotten package = hard failure), `forbidden` contracts (`src ⇏ app`, `sdk ⇏ app, src`), `independence` contracts, forbidden external modules per layer; Ruff TID251 bans configured named imports (layer direction stays with import-linter); a pre-commit hook runs `lint-imports`. Reference shape:

```toml
[tool.importlinter]
root_packages = ["app", "src", "sdk"]
include_external_packages = true

[[tool.importlinter.contracts]]
name = "Layered: delivery and adapters over core over domain"
type = "layers"
layers = ["api | storages | services", "core", "domain"]
containers = ["app"]
exhaustive = true
exhaustive_ignores = ["bootstrap", "server", "settings", "secrets", "errors", "version"]

[[tool.importlinter.contracts]]
name = "adapters are independent"
type = "independence"
modules = ["app.storages", "app.services"]

[[tool.importlinter.contracts]]
name = "src never imports app"
type = "forbidden"
source_modules = ["src"]
forbidden_modules = ["app"]

[[tool.importlinter.contracts]]
name = "sdk imports nothing project-side"
type = "forbidden"
source_modules = ["sdk"]
forbidden_modules = ["app", "src"]

[[tool.importlinter.contracts]]
name = "domain imports stdlib only"
type = "forbidden"
source_modules = ["app.domain"]
forbidden_modules = ["grpc", "sqlalchemy", "httpx", "fastapi", "pydantic"]
```

### Domain models and enums (D1–D4)

[ref: #sly-ruling-domain-models]

- **D1 (MUST)** Domain models are `@dataclass(frozen=True, slots=True)` — frozen AND slots by default, always. Mutability is a strict exception with a documented reason in the docstring; the exception covers data-carrier shapes only — business-state transitions still follow D3.
- **D2 (MUST)** Text constants → `StrEnum`, numeric → `IntEnum`, members ALWAYS via `auto()`. Plain `str` statuses and plain `Enum` are MUST NOT.
- **D3 (MUST)** State transitions are domain-object methods returning new instances (`dataclasses.replace`); external mutation from the service layer is MUST NOT. No `**` kwargs wiring in model conversions — field-by-field slot-to-slot only.
- **D4 (MUST)** Three model families stay separate forever: ORM models (persistence) ≠ domain models (business) ≠ HTTP/pydantic IO schemas (REST validation). ORM-as-domain is MUST NOT.

### Mappings (M1–M5)

[ref: #sly-ruling-mappings]

- **M1 (MUST)** Inbound pb2→domain: mapper functions in the transport layer build domain objects field-by-field. `from_pb2` ON domain models is MUST NOT (violates I2).
- **M2 (MUST)** Outbound domain→pb2: `to_pb2`/`views.py` helpers in the transport layer; handlers never build pb2 inline; the dict-splat response pattern is MUST NOT.
- **M3 (MUST)** ORM↔domain: explicit mapper functions (`orm_to_domain` / `domain_to_orm`) in a mapper module inside `storages/<backend>/`; `to_domain()` on the ORM model is MUST NOT — the dependency stays one-directional and visible.
- **M4 (MUST)** Profile B: `schemas.py` (input) validates and converts to domain via an explicit api-layer mapper; `models.py` (output) is built from domain field-by-field; domain objects are NEVER returned to FastAPI directly; `response_model` is always an IO model.
- **M5 (MUST NOT)** `**`-unpacking in any conversion; `model_dump()` is legal only for wire serialization at the boundary itself. Automated mapping libraries (introspection-based, mapstruct-style) are MUST NOT: they break silently on field renames, while explicit field-by-field mapping is caught by mypy and IDE refactoring.

### Ports and DI (P1–P4)

[ref: #sly-ruling-ports-di]

- **P1 (MUST)** Ports are `typing.Protocol` with `@runtime_checkable`. ABC ports are MUST NOT.
- **P2 (MUST)** Composition root: `app/bootstrap.py` builds a `Provider` (storage + clients + sdks) at startup and threads it into servicers/handlers via constructors. Module-level singletons (factory globals, stub registries, service-locator globals) are MUST NOT. The only sanctioned global is the read-only `config`. DI containers/frameworks (`punq`, `dependency-injector`) are MUST NOT without explicit user approval — manual constructor injection is the default.
- **P3 (MUST NOT)** Per-request service instantiation. Services are built once in bootstrap.
- **P4 (MUST)** Profile B: the `Provider` is built in the FastAPI lifespan, stored on `app.state`, threaded via `Depends` factories. `Depends` factories live in one `dependencies.py` module per transport package — never inside routes or bootstrap — to avoid circular imports.
- **P5 (MUST)** Injected dependencies live at least as long as their consumers: singletons (config, connection pools, stateless services) NEVER receive per-request objects (DB sessions, transactions). A short-lived object captured by a long-lived one is a captive dependency and a blocking defect.

### Errors (E1–E4)

[ref: #sly-ruling-errors]

- **E1 (MUST)** One hierarchy in `app/errors.py`: `ApplicationError` root → `ClientError`/`ServerError`; class names end with `Error`. Per-service custom roots are MUST NOT. Few types; a new class exists only with differentiated handling.
- **E2 (MUST)** One central mapping place: gRPC interceptor / FastAPI exception handler with an EXHAUSTIVE `ERROR_MAP`; an unmapped error is a bug. Local try/except only where behavior genuinely differs. The mapping distinguishes transient from permanent failures: a permanent failure gets a precise status code so the client knows NOT to retry.
- **E3 (MUST)** Errors carry a reason enum serialized in exactly one place; stringly-typed matching and parsing `grpc.detail()` strings are MUST NOT. On the wire the reason travels as gRPC Rich Error Details (`ErrorInfo`), never packed into the message string.
- **E4 (MUST)** Crash-loud at startup: config/secrets/connections fail loudly; no cleanup theater before the process starts.

### Settings and secrets (S1–S4)

[ref: #sly-ruling-settings]

- **S1 (MUST)** pydantic-settings, one root `Settings` object; config is formed once at initialization from a single source. Swappable infra flavors are DISCRIMINATED UNIONS selected by a `type` discriminant. Flat `os.getenv` modules are MUST NOT. The root settings declare `SettingsConfigDict(env_prefix="<SERVICE>_", extra="ignore")`: one env namespace per service, and unknown env vars are TOLERATED — orchestrators inject their own variables, `extra="forbid"` would break deploys. Reference shape:

```python
class VaultEnvConfig(BaseSettings):
    type: Literal["env"]  # every variant declares its discriminant
    # fields...

VaultConfig = Annotated[
    VaultEnvConfig | VaultKubernetesConfig | VaultTokenConfig | VaultJWTConfig,  # Python ≥3.10 union syntax
    Field(discriminator="type"),
]
```

- **S2 (MUST)** No defaults for secrets/passwords/tokens, ever; required vars crash at startup naming the variable. Hardcoded vault tokens / encryption keys are MUST NOT. Secret-typed fields use `pydantic.SecretStr` so values stay masked in logs and tracebacks.
- **S3 (MUST)** `secrets.py` resolves vault secrets at startup BEFORE any client connects; failure = the process does not start.
- **S4 (MUST)** `.env.example` is committed and documents every variable; the service boots locally without infrastructure (literals / no-op implementations); dev opt-in is always explicit.

### Persistence and UoW (T1–T4)

[ref: #sly-ruling-persistence]

- **T1 (MUST)** A stateful Profile-A service has alembic migrations + `storages/postgres/`; a stateless service MUST NOT grow a local DB. Multi-backend is legal — one package per backend.
- **T2 (MUST)** UoW via the `TransactionManager` Protocol (`async with tm.transaction() as storage:`) WITH mandatory per-aggregate repository Protocols (`core/repo.py`). Handler-passed sessions are MUST NOT. A single `AsyncEngine` is created once at startup; the session factory is scoped per transaction; the UoW context manager MUST guarantee session closure even on exceptions.
- **T3 (MUST NOT)** Manual `rollback()`/`commit()` inside the `with session.begin():` context manager — the context manager owns commit/rollback.
- **T4 (MUST)** The migration version check is ACTIVE at startup and fails fast BEFORE serving traffic — the DB revision (`alembic.runtime.migration.MigrationContext.get_current_revision()`) is compared with the alembic head revision (`ScriptDirectory.get_current_head()`), and any mismatch aborts startup (a commented-out check is MUST NOT). On shutdown the engine is disposed (`await engine.dispose()`) so pooled idle connections do not leak.

### Entrypoint and lifecycle (Y1–Y5)

[ref: #sly-ruling-lifecycle]

- **Y1 (MUST)** `main.py` is a thin entry, no CLI magic; `docker-entrypoint.sh` help text tells the truth — a help/case mismatch is MUST NOT.
- **Y2 (MUST)** Symmetric lifecycle: every `connect_*` has a paired close registered in `shutdown()`; shutdown is total and awaited (engine, channels, Temporal clients, HTTP sessions) and drains in-flight work with an explicit grace period (`server.stop(grace=N)`) before force-terminating. Long-running background `asyncio` tasks MUST receive cancellation (`asyncio.Event` / `task.cancel()`) during shutdown and MUST be awaited there. No-op shutdown is MUST NOT.
- **Y3 (MUST)** Single teardown owner: shutdown lives once in `server.py`/lifespan; servicer `on_exit` teardown hooks are MUST NOT.
- **Y4 (MUST)** Startup order: sentry → settings → secrets (vault) → bootstrap (`build_provider`) → serve; any failure before serve = the process does not start.
- **Y5 (MUST)** Signal propagation: the container entrypoint uses the `exec` form (`ENTRYPOINT ["python", "-m", "app.main"]`) so the Python process receives `SIGTERM` directly — a shell-wrapped entrypoint swallows signals and the container dies by kill timeout, which is MUST NOT; an init shim (`tini`) is REQUIRED when the app is not PID 1.

### Observability (O1–O7)

[ref: #sly-ruling-observability]

- **O1 (MUST)** Sentry is initialized at startup before clients connect (see Y4); DSN comes from settings with no hardcoded default. An empty DSN is ALLOWED for development, but startup MUST log a warning that Sentry is not initialized; silent disable is MUST NOT.
- **O2 (MUST)** Sentry integrations match the transport: async gRPC services use `AsyncioIntegration` + `LoggingIntegration` + `GRPCIntegration`; REST services use `FastApiIntegration` + `LoggingIntegration`. PII is off globally (`send_default_pii=False` — no IPs, cookies, or POST bodies) AND `before_send` is a shared scrubber from a shared library; hand-copied per-service `sentry.py` filters are MUST NOT.
- **O3 (MUST)** Logging goes through one shared configuration (from the org's shared logging library): plain + JSON formatters, level and format from settings, static fields (`service`, `version`, `environment`, k8s metadata) with the correct service name. Dumping the full config to logs at startup is MUST NOT. Copy-pasted logging config with a foreign env prefix or wrong service name is MUST NOT.
- **O4 (SHOULD)** Request/correlation IDs propagated across gRPC metadata / HTTP headers when a flow needs cross-service tracing — the W3C `traceparent` header is the canonical carrier; extraction/injection happens in transport middleware (FastAPI middleware, gRPC client/server interceptors), never in business logic.
- **O5 (SHOULD)** Prometheus metrics endpoint — optional but desirable. When present, metric names follow `namespace_subsystem_name_unit` (e.g. `grpc_server_duration_seconds`) and label values MUST be cardinality-bounded (`endpoint`, `method`, `status_code`); unbounded label values (`user_id`, full URLs, request parameters) are MUST NOT — high cardinality degrades Prometheus itself.
- **O6 (out of scope)** Distributed tracing is not regulated by this standard; it is a separate per-team decision.
- **O7 (out of scope)** Health-probe semantics are governed outside this standard; this standard only requires that the endpoints exist (gRPC services expose `startup`/`readiness`/`liveness` via grpc_health.v1, REST services `/livez` + `/readyz`); dependency-check depth is a per-team decision — with one hard warning: liveness MUST stay shallow (process alive only), because a deep liveness check turns a transient dependency outage into an orchestrator restart loop; dependency depth belongs to readiness.

Rationale: observability scaffolding is the most copy-pasted code in a service fleet; the fixes are cheap and uniform, while tracing and probe depth are separate per-team activities.

## Anti-Pattern Registry

[ref: #sly-anti-patterns]

Banned patterns, each with the ruling that forbids it:

1. Module-global mutable factories/registries as DI (factory singletons, stub registries, service-locator globals) → composition root (P2).
2. Per-request service instantiation → P3.
3. Asymmetric/no-op shutdown → Y2.
4. Servicer `on_exit` teardown → Y3.
5. pb2 imports in `domain/` → I2.
6. Reverse imports `services/` → `api/` → I3.
7. SQLAlchemy in business modules → I2.
8. Mutable domain dataclasses as default → D1.
9. Plain `str`/plain `Enum` statuses → D2.
10. Domain mutation in the service layer → D3.
11. `from_pb2` on domain models → M1.
12. Dict-splat pb2 responses → M2.
13. Domain objects as FastAPI responses → M4.
14. `**`-unpacking in conversions → M5.
15. ABC ports → P1.
16. Per-service custom error roots → E1.
17. Unmapped errors (missing `ERROR_MAP` entries, `ServerError` falling through to INTERNAL) → E2.
18. Stringly-typed error matching → E3.
19. Flat `os.getenv` settings → S1.
20. Hardcoded secret defaults → S2.
21. Missing `.env.example` → S4.
22. Manual rollback/commit inside `session.begin()` → T3.
23. Commented-out migration version check → T4.
24. `docker-entrypoint.sh` help/case mismatch → Y1.
25. Copy-paste residue: foreign service names in settings/configs, wrong `pyproject.toml` name, template READMEs, placeholder test scaffolding (a misnamed `tests/contest.py` instead of `conftest.py`, `test_fake.py`, missing test env configuration) → forbidden outright.
26. Silent Sentry disable on empty DSN → O1.
27. Transport-mismatched Sentry integrations (gRPC service without `GRPCIntegration`, REST service without transport coverage) → O2.
28. Hand-copied `sentry.py` noisy-filter without PII scrubbing → O2.
29. Wrong service name / foreign env prefix in logging config → O3.
30. Full config dump to startup logs → O3.
31. Shell-form Docker entrypoint swallowing SIGTERM → Y5.
32. Background `asyncio` tasks left uncancelled at shutdown → Y2.
33. Unbounded Prometheus label values (`user_id`, full URLs) → O5.

## Reference Implementations

[ref: #sly-references]

Canonical patterns to imitate when unsure (anonymized; find services in your fleet that exhibit them):

- **Symmetric lifecycle (Y2):** every `connect_*` paired with a close in one `shutdown()`, engine disposed, all upstream clients awaited closed.
- **Composition root (P2/P4):** `bootstrap.py` `build_provider` for gRPC; lifespan-built `Provider` on `app.state` with `Depends` factories for FastAPI.
- **Settings discipline (S1/S4):** pydantic-settings with nested groups, discriminated-union infra flavors, committed `.env.example`.
- **Observability wiring (O1–O3):** Sentry init before clients with transport-matched integrations and a shared `before_send` scrubber; shared logging config with the correct service name; readiness probes that actually check dependencies.

## Conformance Checklist

[ref: #sly-conformance]

A service conforms when ALL of the following hold:

1. Layout: `app/` root; delivery only under `api/` (`api/grpc/`, `api/http/`); no top-level `grpc_api/`; isolated modules in `src/`, general toolkits in root `sdk/`.
2. Imports: import-linter contracts green in CI; `domain/` imports stdlib only; no pb2/ORM/HTTP types across boundaries; no reverse imports.
3. Domain: `@dataclass(frozen=True, slots=True)`; `StrEnum`/`IntEnum` with `auto()`; behavior as model methods; ORM ≠ domain ≠ IO schemas.
4. Mappings: transport-layer mappers field-by-field; no `from_pb2` on domain; no dict-splat responses; no `**` conversion; FastAPI `response_model` is an IO model.
5. DI: Protocol ports; `bootstrap.py` composition root; no module-level factory singletons; no per-request service instantiation.
6. Errors: `ApplicationError` hierarchy in `app/errors.py`; one central exhaustive mapping; no stringly-typed matching.
7. Settings: pydantic-settings root object; discriminated-union infra flavors; no secret defaults; `.env.example` committed; local boot without infra.
8. Persistence: alembic + UoW + repository ports (stateful) or provably stateless; no manual rollback/commit inside `session.begin()`; active migration version check.
9. Lifecycle: thin `main.py`; truthful `docker-entrypoint.sh`; exec-form entrypoint that propagates SIGTERM (Y5); symmetric total awaited shutdown with an explicit grace period and cancelled background tasks, owned once; fail-fast startup order (sentry → settings → secrets → bootstrap → serve, E4, Y4); engine disposed on shutdown (T4).
10. Observability: Sentry init before clients with transport-matched integrations and a shared `before_send` scrubber; empty DSN logs a startup warning; logging via shared config with the correct service name; no config dumps to logs (O1–O3). Correlation IDs and metrics per O4/O5; tracing and probe depth per O6/O7.

## Violation Protocol

[ref: #sly-violations]

If you design, scaffold, or review a service while violating these rulings — or you detect a violation and stay silent — halt immediately, discard the offending output, reload the violated section by its `sly-` anchor, and redo the work correctly. Every detected violation is reported to the user with its ruling id, even when the task's scope is narrower. Repeated bypasses are recorded in Serena memory under `bugs/project/service_layout_bypass`.
