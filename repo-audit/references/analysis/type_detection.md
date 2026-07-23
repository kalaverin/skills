---
subject: "Repo type detection and per-type interface exhaustiveness (REWORK-REQUIRED); five-type taxonomy, deterministic shell-probe algorithm, `gRPC API service`, `REST API gateway`, `Temporal workflow worker`, `Infrastructure / GitOps`, `library`, exhaustive extraction matrix, streaming kinds, cron schedules, HelmRelease, public modules."
index:
  - anchor: repo-type-detection
    what: "The five-type repo taxonomy with fixed display strings and the deterministic six-branch detection algorithm using only safe read-only shell probes."
    problem: "Pipeline needs repo classification before templates and extraction rules fork; guessed or drifting outcome renders wrong card sections and broken dependency surface; type confusion, template mismatch, branching errors, probe inconsistency, taxonomy drift."
    use_when: "Phase 0 of any audit run — type is determined once, at the very start; tech explorer confirming repo type; anywhere canonical display string is required."
    avoid_when: "Per-type extraction requirements — sibling anchor below; business-domain classification — domain subagents own that."
    expected: "Exactly one canonical type string determined deterministically before any wave launches."
  - anchor: repo-interface-exhaustiveness
    what: "The per-type matrix of interfaces the exploring subagent MUST extract exhaustively, with summarization forbidden."
    problem: "Explorer summarizes instead of enumerating; methods, routes, workflows silently drop from cards and dependency artifacts; incomplete interfaces, silent omissions, summary shortcuts, coverage gaps, downstream defects, endpoint loss, validation failure, exhaustiveness breach."
    use_when: "Tech explorer extracting exported interface; dependency interface extractor listing surface; validating report completeness against matrix."
    avoid_when: "Type determination itself — sibling anchor above; business-domain extraction — `analysis/domain.md` prompts."
    expected: "Every method, route, workflow, module, HelmRelease enumerated per repo type with zero summarization."
---

# Type Detection and Interface Exhaustiveness (repo-audit reference)

> **REWORK-REQUIRED.** This fragment was moved verbatim from `entity-protocol` (2026-07-23). The user has flagged the type fork as critically important and requiring a dedicated rework: the five-type taxonomy and the detection algorithm drive the card-rendering templates (`templates/overview_card.md` per-type sections, `generators/dependencies.md` per-type surface, `analysis/explorer.md`). Known rework items: the per-type list in `generators/dependencies.md` overlaps this matrix (dedup candidate); `analysis/explorer.md` restates the type strings inline (should cite this file). Do not treat the current text as final.

## Type Taxonomy and Deterministic Type Detection

[ref: #repo-type-detection]

Exactly five types with fixed display strings: `gRPC API service`, `REST API gateway`, `Temporal workflow worker`, `Infrastructure / GitOps`, `library`.

Apply this algorithm in exact order, using only safe read-only shell checks (`lsd`, `test -d`, `test -f`), no source reads:

1. `IF` directory contains `apps/base/` or `clusters/` AND NO `app/` source tree → **Infrastructure / GitOps**
2. `ELSE IF` directory contains `proto/` AND NO `app/` OR `worker.py` → **library**
3. `ELSE IF` directory contains `app/api/` (with FastAPI/Flask routers) OR `main.py`/`server.py` exposing HTTP → **REST API gateway**
4. `ELSE IF` directory contains `worker.py` OR `app/workflow/` with `@workflow.defn` → **Temporal workflow worker**
5. `ELSE IF` directory contains `app/` with gRPC servicers / runtime-served proto stubs → **gRPC API service**
6. `ELSE` → default to closest match or STOP and ask the user.

The type is determined ONCE, at the very start of the pipeline (Phase 0), and passed downstream as the `repo_type` input; downstream subagents consume the value and never re-derive it.

## Interface Exhaustiveness Matrix

[ref: #repo-interface-exhaustiveness]

The exploring subagent MUST extract interfaces according to these strict rules. Summarization is FORBIDDEN.

| Type | Exhaustive requirements |
|---|---|
| `gRPC API service` | EVERY method. Separate table for methods declared in `.proto` but NOT implemented in code. Protobuf message names (e.g. `CreateAdvertRequest`), not field definitions. |
| `REST API gateway` | EVERY route. Split unauthenticated (misc/health) vs authenticated (`/api/v1`). Path parameters use `{param}` notation. Auth type per endpoint (`OAuth2`, `RSA-PSS`, `none`). |
| `Temporal workflow worker` | EVERY `@workflow.defn` and `@activity.defn`. All signals, queries, updates, cron schedules. Activities map to downstream service calls. |
| `library` | EVERY public package/module. Omit generated internal helpers. Include build/generation rules (`buf`, `protoc-gen-go`). |
| `Infrastructure / GitOps` | EVERY `HelmRelease` grouped by environment/namespace. |
