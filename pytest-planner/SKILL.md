---
name: pytest-planner
description: "MANDATORY skill for producing repository-specific pytest enablement artifacts for a Python project: a per-repo test-authoring and research prompt that pins the exact `pytest-design` reference anchors the downstream agent must always lazy-load, and an iteration-ready unit-test coverage plan of atomic work items."
triggers:
  all:
    files: ".serena/memories/"
    request: "pytest bootstrap, bootstrap tests, generate test prompt, test agent prompt, pytest-planner, test planning bootstrap, master test plan, план покрытия, бутстрап тестов, сгенерируй промпт тестов, промпт для тестов, промпт pytest, планирование тестов"
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
- **Planning** — when the user asks to create a **test plan / coverage plan / test development plan** ("план тестирования", "план покрытия", "план разработки тестов", "coverage plan"): read `prompts/PLANNING.md` and write Serena `plans/<entity>/tests/coverage` (atomic unit-test work items).

Planning depends on bootstrap: if Serena `agent/tests` is absent, do not plan — run bootstrap first (or hard-stop and demand it), per the boot sequence in `prompts/PLANNING.md`.
If the request is ambiguous between the two, STOP and ask which artifact to produce; do not guess.
Read `pytest-design` only through the in-root mirror at `.kimi/mirror/pytest-design/`; only its frontmatter is harvested into a temporary feature file during BOOTSTRAP Phase 1.

## Master Execution Workflow

This is the **bootstrap** path (→ Serena `agent/tests`); for the **planning** path, follow `prompts/PLANNING.md`.

1. **Preconditions.** Resolve `{{ENTITY_NAME}}`; verify the hard preconditions above. STOP on failure.
2. **Feature discovery (main agent only).** Run the frontmatter harvest from the in-root mirror `.kimi/mirror/pytest-design/` into a temporary file (path is the agent's choice, but never inside `.kimi/mirror/`, which is rsynced with `--delete`). The feature file is a main-agent working inventory and is never handed to subagents:

```bash
fd -t f . references/ 2>/dev/null | sort -u \
    | xargs -I{} sh -c 'printf "\n### {}\n"; awk "/^---$/{c++; if(c==2) exit; next} c==1{print}" "{}"' | grep -v 'expected:' \
    > <FEATURE_FILE>
```

3. **Fan-out.** Slice the **codebase** into coherent regions (directory / module / subsystem), including the tests that belong to each region. Launch parallel read-only `explore` subagents — one per region. Subagents are root-locked and survey the `pytest-design` cards themselves from the in-root mirror `.kimi/mirror/pytest-design/references/`; each receives only its region path and the domain-card paths under `.serena/memories/` (paths, not contents). Follow `subagents-protocol`: no MCP for subagents, timeout ≥ 30–55 min. Per-subagent contract is in `prompts/BOOTSTRAP.md`.
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

For the **coverage-plan** output (`plans/<entity>/tests/coverage`), the required structure and mandatory work-item fields are defined in `prompts/PLANNING.md` (Output section); do not duplicate them here.

## Do Not

- Do not duplicate `pytest-design` rule prose into the generated prompt.
- Do not start without the technical and business cards in place.
- Do not pass Serena memory contents to subagents — pass file paths only.
- Do not hand subagents any path outside the project repository (the skills repo, `/tmp`, the symlinked `.kimi/skills`); subagents read skills only from the in-root mirror `.kimi/mirror/`.
- Do not write anything inside `.kimi/mirror/` — it is rsynced with `--delete` and foreign files are wiped.
- Do not trust subagent anchor lists blindly; validate and extend them.
- Do not write the output anywhere other than Serena memory `agent/tests`.
