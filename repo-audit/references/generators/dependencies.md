# Dependency Subagent Prompts (repo-audit)

## Goal of the dependency analysis

Produce an exhaustive, evidence-based dependency card for the repo. The combined output of the three extractors in this file MUST answer:

1. What public surfaces does this repo expose? (methods, endpoints, workflows, activities, signals, queries, updates, library modules, GitOps artifacts.)
2. Who consumes those surfaces? (exact upstream callers and audiences.)
3. What does this repo call or depend on? (services, databases, queues, external systems, libraries, infrastructure.)
4. What are the exact names of those calls, workflows, and methods?
5. What databases, external integrations, libraries, and infrastructure does it use — with exact versions from lockfiles?
6. What architectural observations, gaps, or TODOs are relevant?

Completeness is the contract: an omitted surface, consumer, or downstream is a defect of the card, not a stylistic choice. Each extractor answers ONLY its slice; anything outside it goes to `## Uncertainties and open questions`.

## Interface extractor

[ref: #ra-deps-interface]

### Role

Identify every public surface this repo exposes and who consumes it.

### Required inputs (MUST read)

- `repos/<repo>/overview` (technical card) — primary source for the exported interface.
- `repos/<repo>/business.md` (+ `repos/<repo>/integrations/` split files, if present).
- Existing `repos/<repo>/dependencies` (if present).
- `preanalysis_reports` (FULL mode): the explorer and integrations reports — reuse them instead of re-deriving the interface from scratch; verify with targeted code reads only.

### What to extract

For the `repo_type` input — determined once in Phase 0 per `[ref: #repo-type-detection]` and passed to this subagent as an input (never re-derived here):

- **gRPC API service:** every service and method, including
  declared-but-unimplemented methods. Note streaming kind.
- **REST API gateway:** every route in every router (method, path, auth).
- **Temporal workflow worker:** every workflow, activity, signal, query,
  update, cron/schedule.
- **Infrastructure / GitOps:** every HelmRelease, Kustomization, namespace, and
  environment.
- **library:** every public package/module, important classes/functions,
  exported symbols.

### Output

A markdown table:

```markdown
| Method / endpoint / workflow | Type | Description | Consumers |
|---|---|---|---|
```

Rules:

- Use exact names.
- `Type` must reflect the actual surface (the agent chooses from the semantic
  types, not from a fixed enum).
- `Description` is one concise sentence with business meaning.
- `Consumers` names exact upstream callers or audiences.
- Include unused/unimplemented surfaces and mark them.

## Downstream mapper

[ref: #ra-deps-downstream]

### Role

Identify every downstream call, dependency, and integration this repo makes.

### Required inputs (MUST read)

- `repos/<repo>/overview` (technical card) — the Required resources / suppliers section.
- `repos/<repo>/business.md` (+ `repos/<repo>/integrations/`, `repos/<repo>/processes/` split files, if present).
- Existing `repos/<repo>/dependencies` (if present).
- `preanalysis_reports` (FULL mode): the integrations and processes reports — reuse them instead of re-mapping downstreams from scratch; verify with targeted code reads only.

### What to extract

- Calls to other gRPC services (service + exact methods).
- Calls to REST/HTTP services (endpoint + method).
- Temporal workflow starts/signals/queries/updates (target namespace/workflow).
- Database ownership and table usage.
- Cache usage (Redis, etc.).
- Message broker / event stream usage.
- External/third-party integrations.
- Shared libraries consumed.
- Identity provider usage.
- Secret store usage.

### Output

A markdown table:

```markdown
| Target | Direction | Methods / workflows used | Protocol | Purpose |
|---|---|---|---|---|
```

Rules:

- `Direction` format: `<repo> -> <direction>`.
- `Methods / workflows used` must list exact names. Use `—` for infrastructure
  connections without specific methods.
- `Protocol` is concrete and precise.
- `Purpose` is one line.
- Do not omit "obvious" dependencies (DB, cache, identity, secrets).

## Infra & libs catalog

[ref: #ra-deps-infra]

### Role

Catalog databases, external integrations, libraries, and infrastructure.

### Required inputs (MUST read)

- `repos/<repo>/overview` (technical card) — technology stack and required resources.
- `repos/<repo>/business.md` (+ split files, if present).
- Existing `repos/<repo>/dependencies` (if present).
- `preanalysis_reports` (FULL mode): the explorer report (manifests, lockfiles) — reuse it; verify with targeted code reads only.

### What to extract

- **Databases:** engine, tables owned, ORM/driver.
- **External integrations:** third-party APIs, identity providers, SaaS, cloud services.
- **Libraries:** shared libraries/SDKs consumed with versions from lockfiles.
- **Infrastructure:** secrets store, orchestrator, cache, observability, service mesh, load balancers.

### Output

A bullet list:

```markdown
- **Databases:** ...
- **External integrations:** ...
- **Libraries:** ...
- **Infrastructure:** ...
```

Rules:

- If a category is not applicable, state `None` with a brief reason.
- Use exact versions from lockfiles/manifests (`pyproject.toml`, `uv.lock`,
  `go.mod`, `package.json`).
- Do not include test/CI/observability-only tools unless they are runtime
  dependencies.
