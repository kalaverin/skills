---
name: pytest-planner
description: "MANDATORY skill for producing repository-specific pytest enablement artifacts for a Python project: a per-repo test-authoring and research prompt that pins the exact `pytest-design` reference anchors the downstream agent must always lazy-load, and an iteration-ready unit-test coverage plan of atomic work items — whole-entity (`project` mode) or diff-scoped over the current branch (`feature` mode)."
version: 0.2.0
triggers:
  all:
    files: ".serena/memories/"
    request: "pytest bootstrap, bootstrap tests, generate test prompt, test agent prompt, pytest-planner, test planning bootstrap, master test plan, план покрытия, бутстрап тестов, сгенерируй промпт тестов, промпт для тестов, промпт pytest, планирование тестов, feature coverage plan, coverage plan, diff coverage plan, feature test plan, branch coverage plan, feature testing, branch coverage, план покрытия фичи, покрытие фичи, план покрытия ветки, покрытие диффа, тестирование фичи, покрытие ветки"
requires:
  - business-audit
  - project-audit
  - pytest-design
  - serena-protocol
  - subagents-protocol
  - todo-protocol
---

# pytest-planner

Generate a repository-specific pytest test-authoring and research prompt and store it in Serena memory `agent/tests`.
The prompt pins the exact `pytest-design` reference anchors a downstream test agent must always lazy-load for the target repository, and carries the repository's domain identity sourced from the curated entity and business cards.

## Skill Boundary

- **This skill owns** the bootstrap workflow: preconditions, feature discovery from `pytest-design`, fan-out to read-only exploration subagents, anchor aggregation/validation, and writing the final prompt to `agent/tests`.
- **This skill does NOT own** the test rules, fixtures, or HOW. Those live in `pytest-design` and are always loaded alongside. Never duplicate them here or in the generated prompt.
- **This skill does NOT own** the technical entity card (`project-audit`) or the business-domain cards (`business-audit`). They are mandatory inputs.
- **This skill does NOT own** general Serena memory rules (frontmatter, naming, mutation, verify/persist). Those live in `serena-protocol`.

## Inputs and Preconditions

- `{{ENTITY_NAME}}` (snake_case) is the only free input. It keys `entities/<ENTITY_NAME>`, `logic/<ENTITY_NAME>/...`, and the glossaries.
  - If exactly one card exists under `entities/`, auto-detect the name.
  - If zero or multiple exist, STOP and ask the user to name the entity.
- **Hard preconditions** (verify before any work):
  - `.kimi/mirror/` in the project root MUST exist and contain the skill tree (at minimum `pytest-design/` and `pytest-planner/`). Subagents are root-locked: they can read only files inside the project repository, and `.kimi/skills` is a symlink they cannot rely on, so the auto-synced mirror is their only way to read skills. If `.kimi/mirror/` is missing or contains no skills, this is a HARD STOP — report it to the user and do not proceed (the main agent's startup gate keeps the mirror fresh).
  - `entities/<ENTITY_NAME>` — technical card (create via `project-audit`). If missing, STOP and ask the user to create it via the named skill.
  - `logic/<ENTITY_NAME>/...` plus `project/glossary` and `logic/<ENTITY_NAME>/glossary` — business cards (create via `business-audit`). If missing, STOP and ask the user to create it via the named skill.

## Request Routing

Pick exactly one artifact to produce based on the user's phrasing, then read the matching prompt in `prompts/` in full (each is a `<BEGIN PROMPT>` … `<END PROMPT>` generator):

- **Bootstrap** — when the user asks to add or create a **prompt for tests** ("создай/добавь промпт для тестов", "test prompt", "bootstrap tests", "бутстрап тестов"): read `prompts/BOOTSTRAP.md` and write Serena `agent/tests` (domain identity + stack profile + pinned `pytest-design` anchor manifest + minimal repo rules).
- **Planning** — when the user asks to create a **test plan / coverage plan / test development plan** ("план тестирования", "план покрытия", "план разработки тестов", "coverage plan"): first resolve the plan mode per **Plan Mode Resolution (HARD STOP)** below, then read the matching generator — `project` → `prompts/PLANNING.md` → Serena `plans/<entity>/tests/coverage` (atomic unit-test work items over the whole entity); `feature` → `prompts/FEATURE.md` → Serena `plans/<entity>/tests/feature_coverage[_<suffix>]` (atomic unit-test work items over the diff of `{{ CURRENT_BRANCH }}` against `{{ BASE_BRANCH }}`).

Bootstrap dependency depends on the plan mode. In `project` mode Serena `agent/tests` is a hard precondition: if it is absent, do not plan — hard-stop and demand that the user generate it first via `prompts/BOOTSTRAP.md`. In `feature` mode `agent/tests` is optional: the feature anchor set is surveyed and validated on the fly (`prompts/FEATURE.md`, Phases B–B.5) and unioned with `agent/tests` §4 when present.
If the request is ambiguous between the two, STOP and ask which artifact to produce; do not guess.
Read `pytest-design` only through the in-root mirror at `.kimi/mirror/pytest-design/`; only its frontmatter is harvested into a temporary frontmatter-harvest file during BOOTSTRAP Phase 1.

## Plan Mode Resolution (HARD STOP)

This fork applies ONLY to the **planning** branch of routing; bootstrap is repo-level and branch-independent and is never affected by it.

Read `{{ CURRENT_BRANCH }}` from git first. Then apply this logic:

1. If `{{ CURRENT_BRANCH }}` is `main` or `master`, default the plan mode to `project` (the existing `prompts/PLANNING.md` path). No question is asked.
2. If `{{ CURRENT_BRANCH }}` is any other branch and the user has not explicitly stated the mode, STOP and demand an explicit mode.
3. If the user explicitly states the mode (e.g. "план покрытия фичи", "feature coverage plan"), use it without asking.

You MUST NOT guess or assume the plan mode outside the `main`/`master` → `project` default.

When stopping, return this message to the user verbatim:

> Ты не на главной ветке. Укажи режим плана покрытия:
> - `feature` — план покрытия diff'а текущей ветки относительно главной (`main`/`master`);
> - `project` — полный план покрытия всего entity.

Only proceed once the user supplies the mode.

For `feature` mode, resolve `{{ BASE_BRANCH }}` next: auto-detect the repository's default branch; if it is not `main` or `master`, STOP and ask the user to confirm it. If the diff `{{ BASE_BRANCH }}`...`{{ CURRENT_BRANCH }}` is empty (including the `{{ CURRENT_BRANCH }}` == `{{ BASE_BRANCH }}` case), STOP and ask the user whether they really want a feature coverage plan — there is no diff to cover.

### Plan Modes and Artifact Naming

| Mode | Prompt | Output (Serena memory) | Scope metadata string |
|---|---|---|---|
| `project` | `prompts/PLANNING.md` | `plans/<entity>/tests/coverage` | `Full project coverage plan (not diff-based)` |
| `feature` | `prompts/FEATURE.md` | `plans/<entity>/tests/feature_coverage[_<suffix>]` | ``Diff-based coverage plan `{{ CURRENT_BRANCH }}` against `{{ BASE_BRANCH }}` `` |

Feature artifact naming: `plans/<entity>/tests/feature_coverage`, optionally suffixed (bare `feature_coverage` is allowed when neither is known) with the feature name and/or branch ticket joined by underscores — e.g. `feature_coverage_trading_statistics_CRYPTO5238` (feature name + ticket) or `feature_coverage_BINDER1341` when the feature name is unknown. The ticket is sanitized code-review style: the internal separator is removed (`CRYPTO-5238` → `CRYPTO5238`). Underscores only, no hyphens. If the suffix is unclear, STOP and ask the user for it; do not guess. The router resolves the suffix and hands it to the generator as `{{SUFFIX}}`. On a re-run, list existing `plans/<entity>/tests/feature_coverage*` memories first; if any exist, STOP and ask the user what to do (which one to overwrite, or create a new suffixed plan).

## Master Execution Workflow

This is the **bootstrap** path (→ Serena `agent/tests`); for the **planning** path, resolve the plan mode first (Plan Mode Resolution above — NEVER guess it outside the `main`/`master` → `project` default), then follow `prompts/PLANNING.md` (`project`) or `prompts/FEATURE.md` (`feature`).

1. **Preconditions.** Resolve `{{ENTITY_NAME}}`; verify the hard preconditions above. STOP on failure.
2. **Frontmatter harvest (main agent only).** Run the frontmatter harvest from the in-root mirror `.kimi/mirror/pytest-design/` into a temporary file (path is the agent's choice, but never inside `.kimi/mirror/`, which is rsynced with `--delete`). The frontmatter-harvest file is a main-agent working inventory and is never handed to subagents:

```bash
fd -t f . references/ 2>/dev/null | sort -u \
    | xargs -I{} sh -c 'printf "\n### {}\n"; awk "/^---$/{c++; if(c==2) exit; next} c==1{print}" "{}"' | grep -v 'expected:' \
    > <HARVEST_FILE>
```

3. **Fan-out.** Slice the **codebase** into coherent regions (directory / module / subsystem), including the tests that belong to each region. Launch parallel read-only `explore` subagents — one per region. Subagents are root-locked and survey the `pytest-design` cards themselves from the in-root mirror `.kimi/mirror/pytest-design/references/`; each receives only its region path and the domain-card paths under `.serena/memories/` (paths, not contents). Follow `subagents-protocol`: no MCP for subagents; timeout ≥ 600 s for a simple region, ≥ 3300 s (55 min) for a complex investigation. Per-subagent contract is in `prompts/BOOTSTRAP.md`.
4. **Aggregate and validate (main agent).** Collect every subagent's anchors. Validate each anchor slug exists in its declaring card under `.kimi/mirror/pytest-design/references/` (frontmatter `index[].anchor` entry and `[ref: #<slug>]` body heading); drop hallucinated anchors. Spot-check the cited `file:line` evidence. Ensure the stack is covered (async/sync, HTTP, DB, time, CLI, frameworks, isolation). Deduplicate convergence (several cards → one anchor). Add any anchor the subagents missed.
5. **Write output.** Produce the repository-specific prompt and write it to Serena memory `agent/tests` (full overwrite) per `serena-protocol`: YAML frontmatter, read-back verify, then `just serena-checkpoint` from the project root. The required contents of `agent/tests` are defined in `prompts/BOOTSTRAP.md` (Phase 4).

## Output Contract (what lands in `agent/tests`)

The generated prompt MUST contain, in order:

1. **Header** — repository, `{{ENTITY_NAME}}`, Python baseline, generator id, UTC timestamp, git branch + short commit.
2. **Domain identity** — real entities, primary id fields, services, business rules/invariants, constants/`Enum`s to import, and naming conventions, sourced from `entities/<ENTITY_NAME>` + `logic/<ENTITY_NAME>/...` + glossaries. This re-contextualizes downstream examples without duplicating rules.
3. **Stack profile** — test framework and plugins present, async/sync ratio, frameworks, external I/O, time handling, CLI, each with `file:line` evidence.
4. **Pinned anchor manifest** — the exhaustive, deduplicated list of `pytest-design` anchors (slugs grouped by declaring card file) the downstream agent MUST always lazy-load from the in-root mirror `.kimi/mirror/pytest-design/` (hard stop if the mirror is missing), plus the exact extraction commands against the mirror.
5. **Minimal repo-specific rules** — only what is NOT already covered by the pinned cards (the universal floor lives in `pytest-design`).
6. **Usage note** — how to use the prompt both for research and for authoring.

For the **coverage-plan** outputs, the required structure and mandatory work-item fields are defined in the Output sections of the two planning generators; do not duplicate them here:

- `prompts/PLANNING.md` — `project` mode → `plans/<entity>/tests/coverage`, scope metadata string `Full project coverage plan (not diff-based)`.
- `prompts/FEATURE.md` — `feature` mode → `plans/<entity>/tests/feature_coverage[_<suffix>]`, scope metadata string ``Diff-based coverage plan `{{ CURRENT_BRANCH }}` against `{{ BASE_BRANCH }}` ``.

## Do Not

- Do not duplicate `pytest-design` rule prose into the generated prompt.
- Do not start without the technical and business cards in place.
- Do not pass Serena memory contents to subagents — pass file paths only.
- Do not hand subagents any path outside the project repository (the skills repo, `/tmp`, the symlinked `.kimi/skills`); subagents read skills only from the in-root mirror `.kimi/mirror/`.
- Do not write anything inside `.kimi/mirror/` — it is rsynced with `--delete` and foreign files are wiped.
- Do not trust subagent anchor lists blindly; validate and extend them.
- Do not write the output anywhere other than Serena memory (`agent/tests` for bootstrap, `plans/<entity>/tests/coverage` for a project plan, `plans/<entity>/tests/feature_coverage[_<suffix>]` for a feature plan).
- Do not guess or assume the plan mode outside the `main`/`master` → `project` default; on any other branch without an explicitly stated mode, STOP and ask (the verbatim question in Plan Mode Resolution).
- Do not plan a feature over an empty diff; if the diff `{{ BASE_BRANCH }}`...`{{ CURRENT_BRANCH }}` is empty, STOP and ask the user whether they really want a feature coverage plan.
- Do not treat `agent/tests` as a precondition for feature-mode planning; it is a hard precondition only for `project` mode.
- Do not modify the target repository's `.gitignore`; feature-mode scratch under `.tmp/pytest-planner/` is temporary by definition — delete it once the plan is sealed and whenever the plan is discarded.
- Do not merge a feature plan back into `plans/<entity>/tests/coverage`; the feature plan is a TEMPORARY artifact for immediate implementation of the current diff, not a historical record.
