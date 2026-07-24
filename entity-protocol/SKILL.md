---
name: entity-protocol
description: "MANDATORY core standard for the repo (entity) concept and the SINGLE namespace registry for all Serena memory scopes: repo definition, naming, the prerequisite gate, one-repo-per-run, identity/provenance/freshness rules, and the canonical repos/ memory layout summary. Type detection and the audit pipeline live in repo-audit; general memory mechanics live in serena-protocol."
runtime: true
triggers:
  request: "entity, repo, сущность, репо, entity card, repo card, карточка репо, карточка сущности, prerequisite gate, repos/, namespace registry, неймспейсы, репозиторий"
requires:
  - frontmatter-protocol
version: 0.2.0
---

# SKILL: Entity Protocol (Repo Concept & Namespace Standard)

This skill is the single normative source for the **repo** concept and for **all Serena memory namespaces/scopes**. Terminology migration: `entity` and `repo` are full synonyms; `repo` (рус. «репо») is the new canonical term.

**Skill boundary.** This skill owns: the repo CONCEPT (definition, naming, gates, identity, freshness), the SINGLE namespace registry (every scope, its semantics, and its routing rules), repo-scoped findings semantics and evidence rules, the deprecation registry, card production rules, and the canonical `repos/` memory layout. It does NOT own general memory mechanics (metadata headers, mutation protocol, persistence) — those live in `serena-protocol`. It does NOT own type detection, per-type interface extraction rules, or the audit pipeline that PRODUCES the artifacts — those live in `repo-audit`.

## 1. What a Repo (Entity) Is

[ref: #entity-definition]

- A repo (legacy: entity) is a service, library, repository, infrastructure/GitOps component, or any other project component that owns a canonical card at `repos/<repo>/overview` in Serena memory.
- The card is the **usability token**: a repo is usable for repo-scoped memory only after its card exists. `project/repos` (legacy: `project/entities`) is a curated **name registry only** — it groups recognized names but does NOT authorize memory writes or card creation.
- The card at `repos/<repo>/overview` holds the **technical overview only**. Business-domain knowledge lives at `repos/<repo>/business` (+ split files); dependency knowledge at `repos/<repo>/dependencies`; findings live under the findings scopes — semantics in §5. No findings inside the card.
- Examples of valid registries: monorepo (`client_api`, `billing_wf`, `payment_lib`, `production`); game project (`engine`, `renderer`, `physics`, `audio`, `ui`); dotfiles (`dotbot`, `dotbot_git`, `shell`, `text`, `scripts`).

## 2. Naming

[ref: #entity-naming]

- Canonical repo name: `snake_case` with underscores, NO hyphens. Directory dashes convert to underscores (`my-service` → `my_service`).
- The agent renames non-compliant memory paths immediately per `serena-protocol` `[ref: #serena-naming]` before any analysis.

## 3. The Prerequisite Gate (HARD RULE)

[ref: #entity-prerequisite]

Before creating any repo-scoped memory (`bugs/<repo>/...`, `decisions/<repo>/...`, `notes/<repo>/...`, `style/<repo>/...`, `plans/<repo>/...`, `proposals/<repo>/...`, `proposal/<repo>/...`, `reports/<repo>/...`, `todo/<repo>/...`, `deprecations/<repo>/...`, or anything under `repos/<repo>/...`), the agent MUST verify that the target repo already has a card at `repos/<repo>/overview`.

**If no repo cards exist yet (`repos/` scope is empty):**

1. STOP all repo-scoped memory writes.
2. Ask the user to create the first repo card using the `repo-audit` skill.
3. Do NOT guess, infer, or default to a name based on directory names.

**If the target `<repo>` does not have a card:**

1. STOP all memory writes for that repo.
2. Ask the user to create the repo card via `repo-audit` or confirm the correct repo name from existing cards.
3. Do NOT create the repo card implicitly and do NOT guess.

## 4. One Repo Per Run

[ref: #entity-one-repo-per-run]

- Every analysis run accepts exactly ONE repo. If the request mentions multiple repos, STOP and ask the user to pick one. Do not batch repos.
- Exception: the project-level dependency index (`project/dependencies`) is inherently multi-repo and is generated only on explicit user request after every repo has a fresh `repos/<repo>/dependencies`.

## 5. The Namespace Registry (SINGLE SOURCE)

[ref: #entity-namespace-registry]

All Serena memory namespaces/scopes are defined HERE — the single normative source for the entire skills repository. No other file may define, restate, or own a scope.

**Scope creation (HARD, no deviations, no agent skips):** any new scope is born ONLY with explicit user approval. The agent that believes a new scope is needed MUST STOP, present the case and the options to the user, and wait for an explicit decision. Two approved forms exist: (1) **registered scopes** — durable, cross-project; this registry itself is amended (the user approves the edit); (2) **session scopes** — workspace-local, approved in conversation and recorded in `agent/rules` (a compressed note: scope exists, what it holds, when to read it at minimum); session scopes are NEVER added to this registry. Writing to a scope that is neither registered nor user-approved is a HARD FAIL.

| Scope | Structure | Purpose |
|-------|-----------|---------|
| `agent/` | `agent/<topic>` | Agent behavior rules, deprecations, contradictions, known issues, user preferences. |
| `project/` | `project/<topic>` | Project-wide information: glossary, dependency graph, tech stack, repo registry. |
| `meta/` | `meta/<topic>` | Meta-information about conventions (e.g., how to name memories, skill structure). |
| `prompts/` | `prompts/<topic>` | Orchestration prompts for root/subagent workflows. |
| `templates/` | `templates/<topic>` | Repo-card templates. |
| `repos/` | `repos/<repo>/...` | Canonical repo cards (`overview`) and repo analysis (`business`, `dependencies`, `glossary`, split-model subdirs). No findings. |
| `standard/` | `standard/<family>/<family>_<id>.md` | Fetch-once archive of authoritative standards (full raw bodies). Families: `rfc`, `std`, `bcp`, `pep`, `aip`, `owasp`, `w3c`, `whatwg`, `zmpc`, `cwe`. |
| Findings scopes | `<domain>/<repo>/<topic>` | Repo-scoped findings (`bugs`, `decisions`, `notes`, `style`, `todo`, `plans`, `proposals`, `reports`, `deprecations`) — semantics in the subsection below. |

**Strict routing rules:**

- `agent/rules`: Contains the `## Contradictions log`.
- `agent/deprecations`: Project-wide deprecation registry; per-repo deprecations live in `deprecations/<repo>/` — semantics in `[ref: #entity-deprecations]`.
- `project/repos`: Canonical registry of repos recognized in this workspace.
- `project/<topic>`: Project-wide knowledge (glossary, dependency graph, tech stack).
- `repos/<repo>/overview`: Canonical repo card ONLY. No findings here. Layout contract: `[ref: #entity-memory-layout]`.
- `repos/<repo>/...`: Repo analysis output (`business`, `entities/`, `processes/`, `rules/`, `integrations/`, `risks/`, `glossary`, `dependencies`) — produced by the `repo-audit` skill. Layout contract: `[ref: #entity-memory-layout]`.
- `guide/<topic>`: Manuals, onboarding docs, and reference literature for users.
- `artifacts/<topic>`: Artifacts produced during agent work (diagrams, exported data, intermediate dumps).
- `playbook/<topic>`: Agent-facing instructions, scripts, and repeatable procedures.
- `standard/<family>/<family>_<id>.md`: Fetch-once archive of authoritative standards — written ONLY by the archival pipeline owned by the `read-for-comments` skill (families and fetch URLs live there). Project-wide (`repo: generic`), exempt from the prerequisite gate. Raw bodies stay untouched below the synthetic H1.

### Findings scopes: semantics and when to record

Findings are repo-scoped memories about a repo (or the meta-entity). They MUST NEVER be placed inside the `repos/<repo>/overview` card.

**Scope semantics:**

- `bugs/<repo>/<topic>`: broken behavior, Sentry exceptions, contract mismatches.
- `decisions/<repo>/<topic>`: architectural choices (e.g., "intentionally stateless"); follows the ADR discipline (Architecture Decision Records, Michael Nygard 2011 — context, decision, consequences; lifecycle statuses proposed/accepted/deprecated/superseded map to optional tags).
- `notes/<repo>/<topic>`: observations, caveats, hardcoded constants, surprising patterns, missing docs.
- `style/<repo>/<topic>`: project/repo-specific style conventions, technical debt, deprecated library usage, naming inconsistencies.
- `todo/<repo>/<topic>`: TODOs from code/docs for humans and agents.
- `plans/<repo>/<topic>`: complex multi-step plans or investigations.
- `proposals/<repo>/<topic>`: proposed code changes, alternative solutions, session results; `proposal/<topic>` or `proposal/<repo>/<topic>` for not-yet-accepted agent proposals.
- `reports/<repo>/<topic>`: agent reports (reviews, incident investigations, feature research).
- `deprecations/<repo>/<topic>`: deprecated repo-local names, aliases, and their canonical replacements.

**Granularity (HARD):** keep each finding memory short and focused on ONE topic. A report item that mixes two topics becomes two memories. Never append unrelated findings to an existing memory.

**When to record:**

| Trigger | Target namespace |
|---------|------------------|
| Confirmed bug | `bugs/<repo>/<topic>` |
| Architectural decision or trade-off | `decisions/<repo>/<topic>` |
| Strange pattern, caveat, observation | `notes/<repo>/<topic>` |
| Coding style convention or technical debt | `style/<repo>/<topic>` |
| Proposed change/refactoring/alternative solution | `proposals/<repo>/<topic>` |
| Short actionable item from code/docs | `todo/<repo>/<topic>` |
| Complex multi-step plan or investigation | `plans/<repo>/<topic>` |
| Agent report | `reports/<repo>/<topic>` |
| Deprecated name/alias of the repo | `deprecations/<repo>/<topic>` |

### The meta-entity `project`

The name `project` is a RESERVED meta-entity representing the whole project. The repo-scoped grammar is uniform:

```text
<domain>/<repo>/<topic>,  where <repo> is a concrete repo OR the meta-entity `project`
```

Rules:

- The meta-entity exists by definition — the project always exists. It is EXEMPT from the prerequisite gate (`[ref: #entity-prerequisite]`): no card is required to write `bugs/project/...`, `decisions/project/...`, `notes/project/...`, `plans/project/...`, `reports/project/...`, etc.
- Use the meta-entity for knowledge that concerns the project as a whole rather than any single repo.
- No name collision: `project/<topic>` (cross-cutting scope of project-wide knowledge) and `<domain>/project/<topic>` (findings about the meta-entity) are distinct, valid roles of the same name.

Legacy scope mapping and the physical migration procedure: `[ref: #entity-migration-legacy]` in `references/memory_layout.md`.

## 6. Identity, Provenance, and Freshness

[ref: #entity-freshness]

- A repo's identity includes its own git branch, latest short commit hash (7 chars), and commit datetime (UTC ISO 8601). These are ALWAYS sourced from the repo's own git repository, NEVER from the `.serena` host project.
- The `repo` field (domain axis, legal values `<repo-name>` / `generic`, lazy legacy normalization, and the git-anchor chain) is owned by `[ref: #entity-repo-field]` in `references/repo_memory.md`. Tracking field mechanics (field set, git commands, timestamps, refresh-on-mutation) are owned by the frontmatter-protocol tracking extension.
- **Freshness rule:** before trusting a repo-specific memory (where `repo` is not `generic`), compare its `commit`/`committed_at` against the repo's current HEAD. On mismatch the memory is potentially stale: run `git diff <memory-commit>..HEAD`, reconcile claims against the diff, update or append a divergence note; if reconciliation is impossible, inform the user and ask how to proceed. The check does NOT apply to memories with `repo: generic` (including legacy `serena`/`project` values pending lazy normalization).
- **Freshness gate (analysis-time, HARD):** before generating downstream artifacts (dependency cards), every input memory's frontmatter `commit` must match the repo HEAD and all input memories must be mutually consistent. Any stale/missing/inconsistent input → STOP, report the exact mismatch, and offer the REFRESH mode of `repo-audit` (or reconciliation via `serena-audit`).
- **Exploration by mode:** a FULL audit ALWAYS explores the codebase — existing memory is context, never a substitute. In PARTIAL mode, fresh inputs (`commit == HEAD`) are consumed from memory without re-reading code. In REFRESH mode, work is strictly diff-driven: `git diff <card-commit>..HEAD` per card, for ANY diff size — the codebase is never re-read wholesale.

## 7. Canonical Memory Layout

The canonical `repos/` memory layout contract and the legacy migration procedure live in `references/memory_layout.md` (`[ref: #entity-memory-layout]`, `[ref: #entity-migration-legacy]`).

## 8. Lazy-Load Routing Index

Do not read every reference file. Extract only the sections needed, per the frontmatter-protocol lazy-load mechanics.

| Trigger / situation | File | Anchor |
|---|---|---|
| Producing or updating a repo card: root/subagent workflow, constraints, tree fallback | `references/card_production.md` | `[ref: #entity-card-workflow]` |
| Card quality gate before saving | `references/card_production.md` | `[ref: #entity-card-quality]` |
| Card content exclusions (what never goes into a card) | `references/card_production.md` | `[ref: #entity-card-exclusions]` |
| Card hard fails and mistake avoidance | `references/card_production.md` | `[ref: #entity-card-hard-fails]` |
| Card frontmatter header example | `references/card_production.md` | `[ref: #entity-card-header-example]` |
| The `repos/` layout contract, all paths and decisions | `references/memory_layout.md` | `[ref: #entity-memory-layout]` |
| Migrating legacy `entities/`, `logic/`, `project/entities` memories | `references/memory_layout.md` | `[ref: #entity-migration-legacy]` |
| The `repo` field: domain axis, legal values, git-anchor chain | `references/repo_memory.md` | `[ref: #entity-repo-field]` |
| Findings severity/location/hash evidence format | `references/repo_memory.md` | `[ref: #entity-findings-traceability]` |
| Deprecated repo names and aliases registry | `references/repo_memory.md` | `[ref: #entity-deprecations]` |
| Type detection and per-type interface exhaustiveness (REWORK-REQUIRED) | `repo-audit/references/analysis/type_detection.md` | `[ref: #repo-type-detection]`, `[ref: #repo-interface-exhaustiveness]` |

Extract a section per the canonical loader mechanics in `frontmatter-protocol` `[ref: #lazy-load-routing]` (bounded extraction — never a blind `rg -A N` window; the exact command lives there, not here).

## Do Not

- Do NOT write repo-scoped memory before the prerequisite gate passes (§3).
- Do NOT guess repo names from directory names; ask the user.
- Do NOT source repo identity metadata from the `.serena` host project — always from the repo's own git.
- Do NOT re-read code covered by a fresh card (`commit == HEAD`); work diff-driven when stale.
- Do NOT define, restate, or own a memory scope anywhere outside §5 — the registry is single.
- Do NOT use the reserved scope name `cards/`.

**Violation protocol:** if you write repo-scoped memory in violation of the gate, naming, provenance, or freshness rules, halt immediately, discard the offending operation, reload the violated section, and redo the operation correctly.
