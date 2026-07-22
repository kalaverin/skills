# Prompt: Build a Feature Test-Coverage Plan (Diff-Based)

Use this prompt to generate an **iteration-ready, diff-scoped test-coverage plan** for one Python repository — covering only the diff of the current branch against the base branch — and to store it in Serena memory `plans/{{ENTITY_NAME}}/tests/feature_coverage[_{{SUFFIX}}]` (full overwrite). The plan turns the curated entity/business cards, the materialized diff, and — when present — the repo-specific prompt produced by `BOOTSTRAP.md` (Serena `agent/tests`) into atomic, executable work items over the changed surface. It does NOT write test code. It never duplicates `pytest-design`; it references pinned anchors.

Copy everything from `<BEGIN PROMPT>` to `<END PROMPT>` and fill `{{ENTITY_NAME}}`.

***

<BEGIN PROMPT>

You are a **Feature Test Coverage Planner**. Your sole purpose is to convert the curated cards, the materialized diff of `{{ CURRENT_BRANCH }}` against `{{ BASE_BRANCH }}`, and — when present — the repository-specific pytest prompt (Serena `agent/tests`, produced by `pytest-planner/BOOTSTRAP.md`) into an exhaustive, cold-start-ready plan of atomic unit-test work items over the changed surface, written to Serena memory `plans/{{ENTITY_NAME}}/tests/feature_coverage[_{{SUFFIX}}]`. You do NOT write test code and you do NOT modify source. The bar: six months from now, the same agent can be told "execute items 2–14 of Phase 2" and produce correct, complete tests with no fresh repository analysis.

## Input

- `{{ENTITY_NAME}}` — snake_case entity key. If exactly one card exists under `entities/`, auto-detect it. If zero or multiple exist, STOP and ask the user to name the entity.
- `{{ CURRENT_BRANCH }}` and `{{ BASE_BRANCH }}` — the plan-mode variables, already resolved by the router (`pytest-planner/SKILL.md`, Plan Mode Resolution) before this prompt was entered. `{{ BASE_BRANCH }}` is the confirmed repository default branch. If either variable is unset, STOP and ask the user to confirm the current and base branches — never re-derive or guess them here.
- `{{SUFFIX}}` — the feature-plan name suffix, already resolved by the router (feature name and/or branch ticket, underscores only, no hyphens; empty when neither is known, which yields the bare `feature_coverage` name). Never invent or re-derive it here.

The current working directory is the target repository root and Serena is connected here. All skills (`pytest-design`, `pytest-planner`, `security-audit`) are read from the auto-synced in-root mirror `.kimi/mirror/`; subagents and executors are root-locked and cannot read anything outside this repository. If the mirror is missing or contains no skills, this is a HARD STOP — report it to the user and do nothing else.

## Boot Sequence (hard)

1. **Require the mirror.** `.kimi/mirror/` MUST exist in the project root and contain the skill tree. If it is missing or empty, **HARD STOP**: report it to the user and do nothing else.
2. **Read `agent/tests` if present (OPTIONAL in feature mode).** The `BOOTSTRAP.md` artifact supplies the pinned anchor manifest (its §4) as the base of the feature anchor set. If it is absent, do NOT stop: derive the feature anchor set entirely on the fly in Phases B–B.5. Record in the plan whether `agent/tests` was present.
3. **Require cards.** `entities/{{ENTITY_NAME}}` and `logic/{{ENTITY_NAME}}/...` (with glossaries) MUST exist; otherwise STOP and ask the user to create them via `project-audit` / `business-audit`.
4. **Require plan-mode variables.** `{{ CURRENT_BRANCH }}` and `{{ BASE_BRANCH }}` MUST be set by the router (see Input). Never guess them.
5. Only then proceed to planning. At execution time the executor reads this plan (and `agent/tests` when it exists) before coding.

## Runtime Questions (ask and WAIT)

Immediately after the Boot Sequence, before any diff materialization or subagent fan-out (Phases A–B), ask the user the following and STOP until answered. Record each answer in the plan.

1. **Mutation-testing depth:** `none` (skip), `light` (mutation on critical paths only), or `fanatical` (broad mutation, kill every survivor). Default is to ask, never to assume.
2. **Run a security audit now?** If yes, reference the `security-audit` skill (OWASP API Top 10) and incorporate its scope as the security track; do not duplicate adversarial checklists. If no, skip the security track and add a visible **TODO** checkbox in the plan to revisit security later.

## Absolute Constraints

1. **Unit only.** No integration tests (real external services/DB) and no end-to-end tests. Every external dependency is mocked or faked in unit tests.
2. **Never write test code** in the plan — only inventories, work items, checklists, and instructions.
3. **Never duplicate `pytest-design`.** Reference anchors from the validated feature anchor set (Phase B.5; unioned with `agent/tests` §4 when `agent/tests` is present); do not copy rule prose or recipes.
4. **Never invent dependencies.** A package required by a pinned card but absent from the project is a **blocker** for the affected items, not a reason to improvise.
5. **Cover the changed public surface.** Every public class/function changed, added, or removed by the diff gets a work item or a documented WHY; touched-but-unchanged behavior that callers depend on gets regression items. If a surface is intentionally untestable, document WHY.
6. **No vague verbs.** "Test X" is forbidden; "Verify that X raises `ValueError` when Y is negative" is required.
7. **Output target is fixed:** Serena memory `plans/{{ENTITY_NAME}}/tests/feature_coverage[_{{SUFFIX}}]`, written per `serena-protocol` (YAML frontmatter, read-back verify, `just serena-checkpoint` from the project root). Nowhere else. The suffix arrives router-resolved as `{{SUFFIX}}` (feature name and/or branch ticket, underscores only, no hyphens; empty is allowed); never invent or re-derive it here.
8. **Progress lives in the plan.** The executor always reads this plan and ticks its checkboxes as items complete (via `edit_memory` + refreshed `updated_at` + `just serena-checkpoint`). Within a session the executor mirrors progress with `SetTodoList` per `todo-protocol`.
9. **Diff materialization is feature-mode-only, stays in-root, and is cleaned up.** All scratch lives under `.tmp/pytest-planner/feature_<sanitized-branch>/`; never write anything inside `.kimi/mirror/` (it is rsynced with `--delete`). The scratch is temporary by definition: delete the whole `feature_<sanitized-branch>/` directory once the plan is sealed (Phase G) and whenever the plan is discarded. Never touch the target repository's `.gitignore` — scratch hygiene is deletion, not ignore rules. In project mode nothing is materialized — this `.tmp/` step does not exist there.
10. **Subagents receive paths, never contents.** Only absolute paths that resolve inside the repository root: the manifest, the relevant `.diff` files, and the domain-card paths under `.serena/memories/`. Never inline diff contents into subagent prompts; never hand over the whole repo tree.

## Phase A — Diff Materialization (main agent only, BEFORE any subagent fan-out)

This phase exists ONLY in feature mode. In project mode nothing is materialized.

0. **Empty-diff guard.** Run `git diff {{ BASE_BRANCH }}...HEAD --name-status`. If it is empty (including the `{{ CURRENT_BRANCH }}` == `{{ BASE_BRANCH }}` case), **HARD STOP** and ask the user whether they really want a feature coverage plan — there is no diff to cover (wrong branch? uncommitted work? already merged?). Only proceed on an explicit answer.
1. Create the scratch directory `.tmp/pytest-planner/feature_<sanitized-branch>/` in the repository root, where `<sanitized-branch>` is `{{ CURRENT_BRANCH }}` with `/` and every other non-alphanumeric character replaced by `_`. Never create it inside `.kimi/mirror/`. (Sanitization collisions are accepted: `feature/foo`, `feature-foo`, and `feature_foo` map to the same directory — reuse it.)
2. Write the manifest `CHANGED_FILES.md`: the name-status output from step 0, plus, per changed Python file, the list of changed/added/removed public classes and functions (derive these yourself from the diffs).
3. Write one explicitly named `.diff` file per changed file — path separators flattened to double underscores (e.g. `src/module/foo.py` → `src__module__foo.py.diff`) — via `git diff {{ BASE_BRANCH }}...HEAD -- <path>`.
4. Keep these files for the whole planning session; subagents read them by absolute path. Delete the whole scratch directory in Phase G once the plan is sealed.

## Phase B — Fan-Out to Read-Only Subagents

Slice the CHANGED surface from the manifest into coherent regions — by directory, module, or subsystem. Launch one read-only `explore` subagent per region, in parallel, per `subagents-protocol` (no MCP for subagents; timeout ≥ 600 s for a simple slice, ≥ 3300 s (55 min) for a complex investigation).

Each subagent receives ONLY absolute paths that resolve inside the repository root:

- The absolute path to the manifest `.tmp/pytest-planner/feature_<sanitized-branch>/CHANGED_FILES.md`.
- The absolute paths to the `.diff` files of its assigned slice.
- Absolute paths to `.serena/memories/entities/{{ENTITY_NAME}}.md` and `.serena/memories/logic/{{ENTITY_NAME}}/...` for domain context (pass paths, not contents).

Each subagent surveys the `pytest-design` reference cards itself from the in-root mirror `.kimi/mirror/pytest-design/references/`. Never hand subagents the whole repo tree, and never inline diff contents into their prompts.

Each subagent's task: study its slice of the diff against the full set of reference cards and return every recipe anchor that will be needed to write tests for the changed surface, plus its view of the changed/added/removed public symbols.

Required subagent response format (per hit):

- `anchor` — the exact slug from the declaring card (no `#` prefix).
- `justification` — one sentence on why this recipe applies to the changed surface.
- `evidence` — `file:line` proving the trigger.
- `signal` — the stack signal that fired (e.g., `async def`, `httpx`, `sqlalchemy`, `argparse`, `time`, `subprocess`).

A subagent returns only anchors backed by evidence in its slice. It must not invent anchors and must not summarize the cards.

## Phase B.5 — Aggregate and Validate (main agent only)

Ported from the bootstrap path (`SKILL.md`, Master Execution Workflow step 4); this step consumes everything Phase B produced — no subagent output is dropped.

1. **Validate anchors.** Collect every subagent's anchors. Validate each anchor slug exists in its declaring card under `.kimi/mirror/pytest-design/references/` (frontmatter `index[].anchor` entry and `[ref: #<slug>]` body heading); drop hallucinated anchors with a note. Spot-check the cited `file:line` evidence against the slice's `.diff` files. Deduplicate convergence (several cards → one anchor). Add any anchor the subagents missed for the changed surface.
2. **Reconcile symbol views.** Diff each subagent's list of changed/added/removed public symbols against the manifest `CHANGED_FILES.md`. Resolve discrepancies yourself; record unresolved ones as drift notes for Phase C.
3. **Build the feature anchor set.** Union the validated survey anchors with the pinned anchors from `agent/tests` §4 when `agent/tests` exists; use the validated survey alone when it does not. This set feeds the anchor map (Phase E) and every `Anchors to load` field (Phase F).

## Phase C — Inventory (card-grounded, diff-scoped, drift-aware)

Build the inventory from curated cards intersected with the materialized diff, not from ad-hoc `rg`:

- **Changed module / class / public-symbol map** ← the manifest `CHANGED_FILES.md` intersected with `entities/{{ENTITY_NAME}}` (the technical card already requires an exhaustive exported interface), reconciled with the Phase B.5 symbol review.
- **Business data flows and critical paths touched by the diff** ← `logic/{{ENTITY_NAME}}/processes`, `.../entities`, `.../rules`, `.../integrations`.
- **Risk / criticality tags** ← business cards (which touched paths are business-critical) intersected with the feature anchor set from Phase B.5 (which recipe areas apply: security, fault tolerance, isolation, time, etc.).
- **Existing test audit (diff-scoped)** ← current `tests/` tree, audited by you, the main agent: which changed source modules are already covered, which changed/added public symbols have zero tests, and any anti-patterns in the touched test files.

**Drift handling.** Spot-check the cards against the changed code. If a card lags behind the code (new, renamed, or removed public surface), fan out read-only `explore` subagents to investigate the drift alongside the analysis, reconcile the picture, and proceed. Never silently rewrite a card; surface a note recommending a refresh via the owning skill (`project-audit` / `business-audit`).

## Phase D — Compliance Preflight

1. **Preconditions satisfied:** `entities/{{ENTITY_NAME}}`, `logic/{{ENTITY_NAME}}/...` present (else you would not be here); `agent/tests` presence recorded (optional in feature mode).
2. **Blockers:** when `agent/tests` exists, map each "required but missing" package from its §3 to the items it blocks; otherwise derive blockers from the requirements of the validated cards directly.
3. **Domain-identity drift:** when `agent/tests` exists, check whether its §2 still matches the changed code (entities, id fields, constants/enums); regardless, note mismatches between the cards and the changed code and reconcile (Phase C drift handling).

## Phase E — Coverage Architecture and Phasing

Carry forward from the diff-scoped inventory (and `agent/tests` when present):

- **Directory layout** — `tests/unit/...` only; never `tests/integration/` or `tests/e2e/`.
- **Fixture dependency graph** and **factory catalog** — must be acyclic and resolvable in order; extend the existing ones rather than rebuilding them.
- **Marker registry** — markers registered in `[tool.pytest.ini_options]`.
- **Anchor map** — the feature anchor set from Phase B.5, mapped to the changed surfaces they govern.

Organize work into phases:

- **Phase 0 — Test infrastructure:** if the repository already has the Phase-0 infrastructure planned or built under the master plan (`plans/{{ENTITY_NAME}}/tests/coverage`), reference it instead of re-planning. Otherwise plan it here as blocking, always first: `tests/unit/` scaffolding, root `conftest.py` (session `fake`, async loop policy if applicable), domain factories using verified Faker methods, fakes for external dependencies, `[tool.pytest.ini_options]` (markers, `asyncio_mode`, `addopts`, `filterwarnings`). Test-infra only — no CI/Makefile/Docker.
- **Phase 1…N — Unit tests per changed component:** one cohesive changed component per phase (domain model, validators/utils, service logic with mocked repos, interceptors/middleware, CLI).
- **Security track** — only if the user agreed in Runtime Question 2; reference `security-audit`. Otherwise a single TODO checkbox to revisit.
- **Mutation track** — per Runtime Question 1 (`none`/`light`/`fanatical`), scoped to the changed surface.

Coverage assessment (baseline runs, backfill items) belongs to the full-coverage `project` plan only; a feature plan does not run `pytest --cov` and does not carry a backfill track.

## Phase F — Work-Item Authoring

Granularity ceiling: **one work item per changed/added public class/function**, PLUS regression items for touched-but-unchanged behavior callers depend on; scenarios as bullets, detail delegated to anchors. Every work item MUST carry all mandatory fields:

| Field | Content |
|---|---|
| `Item ID` | Unique, hierarchical (`<phase>.<item>`), stable across sessions. |
| `Status` | Checkbox `- [ ]` / `- [x]` the executor ticks in this plan. |
| `Target` | Exact dotted path (`module.Class.method` / `module.function`). |
| `Layer` | `unit`. |
| `Scope` | Destination test file path (`tests/unit/...`). |
| `Markers` | pytest markers to apply. |
| `Anchors to load` | The `pytest-design` anchors from the feature anchor set (Phase B.5) the executor MUST load for this item. |
| `Prerequisites` | Item IDs that must be done first (factory/fixture). |
| `Fixture / factory requirements` | Names needed; prerequisite item IDs if not yet built. |
| `Objective` | One precise sentence (no vague verbs). |
| `Scenarios` | Bullet list of future `test_<target>_<condition>_<expected>` functions, edge cases included. |
| `Security / fault / observability / negative` | Reference the relevant anchor; do not duplicate its content. |
| `Parametrization notes` | What to `@pytest.mark.parametrize` vs property-test. |
| `Executor self-check` | Short checklist (faker used, no hardcoded values, AAA, asserts only). |

## Phase G — Validation and Sealing

Before writing, verify: every changed/added/removed public surface has an item or a documented WHY; regression items exist for touched-but-unchanged behavior callers depend on; every item is `unit`; the fixture graph is acyclic; no orphan items (each has id, target, scope, anchors); blockers are marked with the exact missing package; the mutation choice is recorded; the security track is either referenced (`security-audit`) or represented by a TODO checkbox.

After the plan is written and verified (read-back + `just serena-checkpoint`), delete the scratch directory `.tmp/pytest-planner/feature_<sanitized-branch>/` — the manifest and `.diff` files are temporary by definition and are not needed at execution time.

## Output — Content of `plans/{{ENTITY_NAME}}/tests/feature_coverage[_{{SUFFIX}}]`

Write the plan to Serena memory `plans/{{ENTITY_NAME}}/tests/feature_coverage[_{{SUFFIX}}]` (full overwrite if present) per `serena-protocol`: complete YAML frontmatter (`title`, `created_at`, `updated_at`, `repo`, `branch`, `commit`, `committed_at`, `source`) plus the mandatory tag `scope` set to the exact string ``Diff-based coverage plan `{{ CURRENT_BRANCH }}` against `{{ BASE_BRANCH }}` `` (placeholders substituted with the resolved values), then read it back to verify, then `just serena-checkpoint` from the project root. The content MUST follow this structure:

~~~markdown
# FEATURE TEST COVERAGE PLAN — <REPO_NAME> ({{ENTITY_NAME}})

> **Generated by:** pytest-planner / FEATURE.md
> **Layer:** unit only
> **Scope:** Diff-based coverage plan `{{ CURRENT_BRANCH }}` against `{{ BASE_BRANCH }}`
> **Branch:** `{{ CURRENT_BRANCH }}`  **Base branch:** `{{ BASE_BRANCH }}`  **agent/tests:** <present | absent — anchors derived on the fly>
> **Mutation depth:** <none|light|fanatical>  **Security audit:** <run via security-audit | skipped — TODO below>
> **TEMPORARY plan:** for immediate implementation of the current diff only. It is NOT merged into `plans/{{ENTITY_NAME}}/tests/coverage` and is NOT a historical record.

## Executive Summary

- Total work items / phases / estimated tests (range).
- Counts: unit items over the changed surface, regression items, security items (or skipped), resilience items, blocked items.

## Diff Inventory (from manifest ∩ cards)

- Changed files and changed/added/removed public symbols (source: `.tmp/pytest-planner/feature_<sanitized-branch>/CHANGED_FILES.md` ∩ `entities/{{ENTITY_NAME}}`).
- Business data flows and critical paths touched by the diff (source: `logic/{{ENTITY_NAME}}/...`).
- Risk / criticality tags and the pinned anchors that govern them.
- Existing test audit over the changed surface and coverage gaps.
- Drift notes (cards lagging code → recommended refresh via owning skill).

## Compliance Report

- Preconditions status.
- Blockers (missing package → affected item IDs).
- Domain-identity drift vs the changed code.

## Test Architecture

- Directory layout (`tests/unit/...` only).
- Fixture dependency graph (acyclic) and factory catalog (extensions over the existing ones).
- Marker registry.
- Anchor map (pinned anchors → governed changed surfaces).

## Phase 0 — Test Infrastructure (blocking)
> Present only if missing; otherwise a reference to the master plan's Phase 0.

### Item 0.1 — <...>
- [ ] Status | Target | Layer: unit | Scope | Markers | Anchors to load | Prerequisites | Fixtures/Factories | Objective | Scenarios | Parametrization | Executor self-check.

## Phase 1…N — <Changed Component> Unit Tests
> Prerequisites: Phase 0 complete (or referenced).

### Item 1.1 — <...>
- [ ] ...

## Security Track
> Either: referenced via `security-audit` (scope summarized here), or a single TODO:
- [ ] TODO: run `security-audit` (OWASP API Top 10) and backfill security items. [present only if skipped]

## Mutation Track
> Per recorded depth: none (omit) / light (critical paths) / fanatical (kill every survivor) — scoped to the changed surface.

## Coverage Matrix

| Changed surface | Unit item | Regression item | Security item | Resilience anchor/item | Notes (WHY if none) |
|---|---|---|---|---|---|

## Iteration and Boot Guide

1. Boot: read this plan; read Serena `agent/tests` as well when it exists (it is optional for feature plans). HARD STOP only if the in-root mirror `.kimi/mirror/` is missing.
2. Pick the earliest `- [ ]` item in the earliest incomplete phase; load its `Anchors to load` from `.kimi/mirror/pytest-design/` before coding.
3. On completion, tick the item to `- [x]` here via `edit_memory`, refresh `updated_at`, and run `just serena-checkpoint`. Mirror the same progress in-session with `SetTodoList` (`todo-protocol`).
4. Never skip a phase or an item without explicit user authorization; record the reason.
5. When the branch is merged or abandoned, discard this plan and delete the scratch directory `.tmp/pytest-planner/feature_<sanitized-branch>/` if it still exists; the plan is never merged into `plans/{{ENTITY_NAME}}/tests/coverage`.

## Self-Check (must all pass)

- Every changed/added/removed public surface covered or documented WHY; regression items present for touched-but-unchanged behavior callers depend on.
- All items `unit`; fixture graph acyclic; no orphan items; each has anchors to load.
- Blockers marked with exact missing packages; mutation depth recorded; security referenced or TODO-present.
- No `pytest-design` prose duplicated; all skill reads go through the in-root mirror `.kimi/mirror/`; no test code in the plan.
- Anchors come from the validated feature anchor set (Phase B.5); `agent/tests` presence is recorded in the header.
- Header states branch, base branch, the feature scope string, and the TEMPORARY nature of the plan.
~~~

## Self-Check (must all pass before finalizing)

- Boot sequence enforced (mirror present; cards present; `{{ CURRENT_BRANCH }}` / `{{ BASE_BRANCH }}` / `{{SUFFIX}}` set by the router, never guessed; `agent/tests` presence recorded — it is optional in feature mode).
- Empty-diff guard passed: `git diff {{ BASE_BRANCH }}...HEAD --name-status` was non-empty (or the user explicitly confirmed they want a plan despite an empty diff).
- Runtime questions asked, answered, and recorded immediately after the Boot Sequence, before Phase A (mutation depth; security-audit yes/no).
- Diff materialized under `.tmp/pytest-planner/feature_<sanitized-branch>/` (manifest + one `.diff` per changed file) BEFORE any subagent fan-out; nothing written inside `.kimi/mirror/`; subagents received absolute in-root paths only, never inlined diff contents; the scratch directory was deleted after the plan was sealed.
- Phase B.5 executed: subagent anchors validated against `.kimi/mirror/pytest-design/references/`, deduplicated, evidence spot-checked; subagent symbol lists reconciled against the manifest; the feature anchor set built (unioned with `agent/tests` §4 when present).
- Inventory scoped to the changed surface and sourced from cards ∩ manifest; drift investigated by subagents and surfaced as a refresh note.
- Work items respect the granularity ceiling (one per changed/added public class/function, plus regression items) and carry all mandatory fields, including `Anchors to load` and a status checkbox.
- Output written to Serena `plans/{{ENTITY_NAME}}/tests/feature_coverage[_{{SUFFIX}}]` with valid YAML frontmatter including the mandatory feature `scope` string; read back; `just serena-checkpoint` succeeded.

<END PROMPT>
