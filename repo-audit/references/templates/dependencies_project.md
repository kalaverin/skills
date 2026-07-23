---
subject: "Project-level dependency card template; generation conditions, fresh per-service cards, `project/dependencies`, `repo: generic`, mandatory sections, edge types, service taxonomy, external inventory, consumer provider matrix, cross-domain summary, key observations, quality rules, aggregate overview."
index:
  - anchor: ra-tpl-deps-project
    what: "The project-level dependency card template: exact layout for `project/dependencies.md`."
    problem: "Project overview assembles ad hoc; sections mismatch per-service cards and aggregate picture contradicts details; ad-hoc assembly, clashing picture, layout absence, aggregate drift, level confusion, coherence failure, map inconsistency, synthesis fog, trust decay."
    use_when: "Writing the project-level dependency overview; reviewing its structure."
    avoid_when: "Per-service details — those live in `repos/<repo>/dependencies.md` by design."
    expected: "One consistent project overview derived from per-service cards."
  - anchor: ra-tpl-deps-project-when
    what: "The generation conditions: explicit user request plus every per-service card fresh at HEAD."
    problem: "Overview generated from stale per-service cards; aggregate teaches last month's architecture with full confidence; stale inputs, confident staleness, premature generation, freshness neglect, garbage aggregate, rotted summary, trust abuse, input decay, assembly sin."
    use_when: "Before creating or updating the project overview; checking preconditions; deciding to STOP."
    avoid_when: "Generating anyway with a warning — conditions are HARD, stop and report instead."
    expected: "Overview only from explicit request and fully fresh inputs."
  - anchor: ra-tpl-deps-project-frontmatter
    what: "The project overview header: `repo: generic` with project-root git tracking."
    problem: "Overview stamped with random service git; provenance points at wrong repository and freshness checks fire falsely; provenance mismatch, value confusion, stamp error, lineage fog, tracking decay, verification noise, anchor drift, root confusion."
    use_when: "Stamping the overview header; choosing the repo value and git source."
    avoid_when: "Field semantics — `[ref: #entity-repo-field]` owns the `generic` rule."
    expected: "Header carries `generic` anchored to project-root git."
  - anchor: ra-tpl-deps-project-sections
    what: "The mandatory eight sections: scope, aliases, edge types, taxonomy, external inventory, matrix, cross-domain summary, observations."
    problem: "Overview sections get reordered or dropped; readers expect canonical map and lose orientation; reordering, orientation loss, canonical drift, map chaos, section lottery, reader confusion, structure decay, sequence fog, outline rot, navigation pain."
    use_when: "Structuring the project overview; reviewing section completeness."
    avoid_when: "Section content details — the fill instructions below."
    expected: "All eight sections present in canonical order."
  - anchor: ra-tpl-deps-project-fill
    what: "The fill instructions: scope method, alias table, edge-type legend, taxonomy rows, inventories, matrix, summary, mandatory observation themes."
    problem: "Sections filled vaguely; edge types invented, repos skipped silently, observations generic; fill drift, matrix gaps, legend invention, coverage holes, theme neglect, spec neglect, content shallowness, row fog, precision loss, observation fog."
    use_when: "Filling any overview section; choosing edge types; writing key observations."
    avoid_when: "Method-level details — those belong to per-service cards, never here."
    expected: "Every section concrete with only real edge types and all repos accounted."
  - anchor: ra-tpl-deps-project-quality
    what: "The quality rules: no method details, no per-service graphs, every repo accounted, UTC dates."
    problem: "Overview smuggles method details and skips repos quietly; level mixing, detail leakage, rule drift, completeness doubt, discipline breach, boundary erosion, audit failure, coverage lies, level confusion, repo omission, standard decay."
    use_when: "Final review before saving the overview; checking level discipline."
    avoid_when: "Per-service card quality — `references/checklists.md` owns that."
    expected: "Overview passes all four quality rules."
---

# Project-Level Dependency Card Template (repo-audit)

[ref: #ra-tpl-deps-project]

This file defines the exact layout and fill-instructions for
`project/dependencies.md`.

## When to create or update

[ref: #ra-tpl-deps-project-when]

Generate or refresh `project/dependencies.md` **only** when:

1. The user explicitly asks for the project-level dependency overview.
2. Every repo in `repos/` has a fresh `repos/<repo>/dependencies.md`
   card whose frontmatter commit matches the repo's repository HEAD.

If either condition is not met, STOP and tell the user what is missing.

## YAML frontmatter

[ref: #ra-tpl-deps-project-frontmatter]

Use the current YAML frontmatter standard from `[ref: #serena-metadata]`;
collect the git tracking fields per the frontmatter-protocol tracking extension
(`[ref: #tracking-fields]`, `[ref: #tracking-git-commands]`).

```yaml
---
title: <Project name> service dependencies
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
repo: generic
branch: <branch>
commit: <7-char-short-hash>
committed_at: YYYY-MM-DDTHH:MM:SSZ
source: .serena/memories/project/dependencies.md
---
```

`repo` is `generic` because this is a project-wide memory — the whole project
as the domain object (legacy `serena`/`project` values normalize to `generic`);
`.serena`, per `[ref: #entity-repo-field]`.

## Mandatory section order

[ref: #ra-tpl-deps-project-sections]

```markdown
# <Project name> service dependencies

**Scope:** project-level overview of services, their taxonomy, dependency edge
 types, external/infrastructure inventory, consumer/provider matrix, and
 cross-domain summary. Method-level details live in `repos/<repo>/dependencies.md`.

## 1. Scope and method

## 2. Canonical aliases and deprecation notes

## 3. Edge types

## 4. Service taxonomy

## 5. External / infrastructure systems inventory

## 6. Consumer/provider matrix

## 7. External / cross-domain dependency summary

## 8. Key observations
```

## Section fill-instructions

[ref: #ra-tpl-deps-project-fill]

### 1. Scope and method

- State that this is the project-level dependency overview.
- Point to `repos/<repo>/dependencies.md` for method/endpoint/workflow details.
- Explain that the overview is derived from `repos/<repo>/overview` cards and
  `repos/<repo>/dependencies.md`.
- Include the update methodology: update per-service cards first; update the
  project overview only when the aggregate picture changes.

### 2. Canonical aliases and deprecation notes

Use a table:

| Alias / deprecated name | Canonical repo card | Notes |
|---|---|---|
| `old-billing-api` | *(none — external)* | Deprecated in-project service. Active billing is the external `billing` monolith. |
| `case-management` | `repos/dispute_api/overview` | Proto package `classic.case_management`. |

### 3. Edge types

Legend table. The agent selects the edge types actually used in the project.
Common values:

| Edge type | Meaning |
|-----------|---------|
| `grpc:downstream` | Service calls another gRPC service |
| `grpc:upstream` | Service exposes gRPC methods consumed by others |
| `http:downstream` | Service makes HTTP calls to another service/API |
| `http:upstream` | Service exposes HTTP/REST consumed by others |
| `temporal:downstream` | Service starts/signals/queries workflows in another namespace |
| `temporal:upstream` | Service exposes Temporal workflows started by others |
| `temporal:worker` | Service is a Temporal worker |
| `db` | Service owns a database |
| `external` | Calls a third-party/external system |
| `infra` | Uses shared infrastructure (secrets, cache, observability, mesh, etc.) |
| `library` | Consumes a shared library/SDK |
| `gitops` | Deployment manifests managed by this GitOps repository |
| `message_queue` | Produces/consumes messages from a message broker |
| `event_stream` | Produces/consumes events from an event stream |

Only include types that actually appear in the project.

### 4. Service taxonomy

Columns: `repos/ card`, `Directory`, `Type`, `Runtime role`, `Dependency card`.

Example row:

| `repos/` card | Directory | Type | Runtime role | Dependency card |
|---|---|---|---|---|
| `wallet_wf` | `wallet-wf/` | Temporal workflow worker | Deposit / topup / withdrawal / clearing | `repos/wallet_wf/dependencies.md` |

Every repo in `repos/` should appear here unless explicitly skipped and
noted in Key observations.

### 5. External / infrastructure systems inventory

Columns: `System`, `Category`, `Consumers`, `Notes`.

Example row:

| System | Category | Consumers | Notes |
|---|---|---|---|
| HashiCorp Vault | Secrets | All runtime services | AppRole/KV v1/v2; injected via sidecar. |
| PostgreSQL | Database | `order_service`, `inventory_service` | Accessed via SQLAlchemy 2.0 async. |

### 6. Consumer/provider matrix

Columns: `Provider`, `Consumers`, `Primary interaction`.

Example row:

| Provider | Consumers | Primary interaction |
|---|---|---|
| `wallet_api` | `backoffice_api`, `external_api`, `wallet_wf` | gRPC upstream (`WalletService`) |

### 7. External / cross-domain dependency summary

Columns: `External system`, `In-project consumers`, `Protocol / integration point`.

Example row:

| External system | In-project consumers | Protocol / integration point |
|---|---|---|
| `billing` monolith | `billing_wf`, `external_api` | gRPC `modern.common.billing.v1`; external to this repo |

### 8. Key observations

Bulleted architectural takeaways. Mandatory recurring themes to cover:

- Deprecated services and their replacements.
- Aliased services.
- Services with the broadest fan-out.
- Shared libraries with high blast radius.
- Central infrastructure (orchestration, identity, observability).
- Any database-naming drift or shared-cluster legacy.
- Stub/non-functional repos.
- Method-level details live in `repos/<repo>/dependencies.md`.

## Quality rules

[ref: #ra-tpl-deps-project-quality]

- No method-level details outside the per-service cards.
- No "Dependency graph by service" section — that belongs in each
  `repos/<repo>/dependencies.md`.
- Every repo in `repos/` is either in the taxonomy or explicitly skipped
  with a reason.
- All timestamps are UTC ISO 8601 with a `Z` suffix.
