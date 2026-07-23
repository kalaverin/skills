---
subject: "Skill header evaluation extension; SKILL.md frontmatter schema, closed trigger grammar, always any all conditions, files shell exit zero, request semantic matching, runtime bootstrap awareness read and re-evaluation, requires transitive closure, draft skip, version policy, skill discovery, boot contract, batch extraction, deterministic evaluation pipeline, skill-creator override."
index:
  - anchor: include-skill-header-schema
    what: "The closed key schema every `SKILL.md` header MUST satisfy: `name`, `description`, `triggers`, optional `requires`, `runtime`, `version`, `draft`."
    problem: "Agent loads skills whose headers drift in shape — unknown keys, missing triggers, undeclared flags — so evaluation becomes guesswork and loaders break on surprises; schema drift, silent keys, loader crashes, inconsistent headers, validation gaps, key sprawl, undocumented flags, brittle discovery."
    use_when: "Authoring or editing any `SKILL.md` header; reviewing a skill for conformance; wiring a new skill into the registry."
    avoid_when: "Reference-file card frontmatter — that schema lives in the lazyload extension; Serena memory headers — tracking extension plus serena-protocol."
    expected: "Every skill header parses against one closed schema; stray keys fail validation loudly."
  - anchor: include-trigger-grammar
    what: "The closed grammar for the `triggers` block: recursive nodes of `always` / `files` / `request` conditions, `any:` (OR) and `all:` (AND) combinators, nesting depth 0..N, `reason` annotation legal at every level."
    problem: "Trigger blocks grow ad-hoc shapes across skills — nested maps, invented keys, ambiguous combinations — and two loaders read identical blocks differently; condition sprawl, divergent loaders, unpredictable activation, boolean semantics, declarative gating, load decision."
    use_when: "Defining when a skill activates; converting prose activation rules into declarative conditions; choosing between `any` and `all` semantics."
    avoid_when: "Runtime behavior after activation — triggers only gate loading; per-task routing inside a loaded skill belongs to that skill's own routing."
    expected: "One grammar covers every skill; identical trigger blocks evaluate identically everywhere."
  - anchor: include-trigger-evaluation
    what: "Evaluation semantics: `always: true` loads unconditionally; bare sibling conditions are OR-ed; `files` runs as shell probe at bootstrap only, exit 0 means match, bare `fd` forbidden (`fd ... --max-results 1 | wc -l | grep -q 1` is the canonical existence probe); `request` matches semantically against the user message and project context."
    problem: "Agent faces one trigger block and must decide load-or-skip right now; misreading OR as AND or substring-matching requests skips needed skills or floods context with wrong ones; boolean confusion, keyword trap, semantic matching, shell exit codes, load mistakes, context glut."
    use_when: "Evaluating one skill's header during discovery; deciding load-or-skip for a concrete user request; implementing a loader."
    avoid_when: "Designing new condition kinds — the grammar is closed; evaluation covers only existing kinds."
    expected: "Each trigger block yields one deterministic load-or-skip decision per request and workspace."
  - anchor: include-runtime-reevaluation
    what: "The `runtime: true` opt-in: at bootstrap the loader reads the skill's `SKILL.md` in full and remembers its feature set as available-on-demand capabilities; `files` gates freeze at bootstrap; after every new message the agent matches the `request` conditions and described domain from memory and activates the skill when the conversation reaches them."
    problem: "Session starts without some skill, then mid-session user messages mention its domain — delegation, review, search; startup-only evaluation misses that shift and agent answers unguarded; late triggers, stale skill set, shifting topics, dynamic loading, session drift, domain emergence."
    use_when: "Meta/orchestration skills whose relevance appears mid-session; skills gated on user vocabulary that may surface later."
    avoid_when: "Stable domain skills where startup evaluation suffices; attaching re-evaluation universally wastes cycles."
    expected: "Bootstrap yields full feature awareness for every runtime skill; activation happens mid-session exactly when the trigger first matches; no re-reads of unchanged files."
  - anchor: include-requires-resolution
    what: "Transitive closure of the `requires` list: loading a skill loads every listed skill, recursively, until no new skills are added."
    problem: "Skill declares dependencies on peers, agent loads only top one and misses mandated companions — protocols, languages, checklists — producing partial rule sets; missing dependencies, transitive gaps, broken chains, incomplete closure, orphaned companions, dependency blindness."
    use_when: "Loading any skill with a `requires` list; authoring dependencies between skills; diagnosing why a companion skill never activated."
    avoid_when: "Circular dependency traversal — cycles are non-conformant and must be reported, not walked."
    expected: "The loaded set is closed under `requires`; every mandated companion is active."
  - anchor: include-skill-discovery
    what: "The discovery algorithm: search skill directories in priority order, batch-extract every `SKILL.md` header in one shell command, skip `draft: true` headers entirely."
    problem: "Agent needs full skill inventory before evaluation; ad-hoc directory listing misses scopes, double-loads mirrors, or loads half-finished drafts; incomplete inventory, scope blindness, duplicate mirrors, draft leakage, manual listing, search order, wasted cycles."
    use_when: "Session startup before any task; after skill directories change; verifying the registry contents."
    avoid_when: "Evaluating individual headers — discovery yields raw headers; evaluation is the separate next step."
    expected: "One batch command yields every non-draft skill header across all scopes, ordered by priority."
  - anchor: include-boot-contract
    what: "The boot contract: the system prompt force-loads `frontmatter-protocol`; its SKILL.md boot section obliges reading this file whole; only then does header evaluation begin."
    problem: "Agent must evaluate skill headers before knowing evaluation rules — chicken-and-egg; without fixed boot chain each session invents its own loading order; bootstrap paradox, ordering chaos, unevaluated rules, forced preload, startup sequence, hard gate."
    use_when: "Boot-time initialization; writing or changing the system prompt's startup gate; debugging why headers were evaluated loosely."
    avoid_when: "Mid-session operation — the contract binds startup only; later loads follow ordinary lazy rules."
    expected: "Every session evaluates headers with identical rules in identical order, starting from this file."
  - anchor: include-version-policy
    what: "Version policy: `version` is mandatory in the schema; an absent value reads as `0.0.0`; agents ignore missing versions during the transition."
    problem: "Some skills carry versions, most do not; strict loaders demanding versions block twenty skills, lenient ones lose compat metadata entirely; version gaps, transition period, gradual adoption, default zero, semver policy, compat tracking."
    use_when: "Validating headers during the transition; deciding whether a missing `version` is an error; planning version rollout."
    avoid_when: "Enforcing presence today — rollout is manual and gradual; gaps are tolerated meanwhile."
    expected: "Headers validate with or without `version`; absence reads as `0.0.0`."
  - anchor: include-evaluation-pipeline
    what: "The deterministic trigger pipeline: fixed gate sequence (draft, then always, then files, then request), OR short-circuit, AND fail-fast, requires closure with cycle reporting, runtime re-check from memory with `files` gates frozen at bootstrap."
    problem: "Identical header sets meet different sessions and yield divergent load decisions because gate order, short-circuit points, and cycle handling were never pinned down; nondeterminism, evaluation drift, divergent outcomes, order ambiguity, cycle hangs, reproducibility gap, unpredictable activation."
    use_when: "Evaluating any discovered header during the boot sweep; implementing or auditing a loader; debugging why two sessions loaded different skill sets."
    avoid_when: "Designing new condition kinds — the grammar stays closed and this pipeline only sequences existing kinds."
    expected: "Identical headers, workspace, and request produce one identical load set per session; cycles surface as reported errors instead of silent walks."
  - anchor: include-skill-creator-override
    what: "The override ruling: built-in `skill-creator` mandates minimal two-key headers and rejects auxiliary docs; this schema supersedes it inside the project while keeping its process guidance."
    problem: "Agent reads built-in `skill-creator` mandating bare minimal headers and no README files, then hesitates or strips extended keys when authoring skills in this repository; conflicting standards, hesitation, built-in pressure, schema clash, authority question, dual rulebooks."
    use_when: "Authoring or editing any SKILL.md header for project skills; `skill-creator` instructions collide with project rules; judging whether extended keys are legitimate."
    avoid_when: "Generic skill authoring beyond this workspace — built-in defaults govern there."
    expected: "Extended headers carrying `triggers`, `requires`, `runtime`, `version`, `draft` stand as the single legal form; README documents stay conventional."
---

# Reference: include — Skill Header Evaluation (frontmatter-protocol extension)

Boot-mandatory extension of `frontmatter-protocol`: read this file WHOLE at the boot gate (core §1), then apply it to every skill header you evaluate.

## SKILL.md Header Schema

[ref: #include-skill-header-schema]

Every skill entry point is `<skill-dir>/SKILL.md` carrying a core-conformant frontmatter with this **closed** key set:

| Key | Required | Content |
|---|---|---|
| `name` | yes | Skill identifier, kebab-case, MUST equal the directory name. |
| `description` | yes | What the skill governs; prose, any YAML string style. |
| `triggers` | yes | Activation rules per the trigger grammar (next section). |
| `requires` | no | List of skill names to load transitively (see Requires Resolution). |
| `runtime` | no | Boolean; `true` opts into bootstrap awareness read plus per-message re-evaluation (see Runtime Re-Evaluation). |
| `version` | yes* | Semver string. \*Mandatory in the schema, but absence reads as `0.0.0` (see Version Policy). |
| `draft` | no | Boolean; `draft: true` marks a skill purely in development — loaders MUST ignore it entirely. |

No other top-level keys are allowed. `reason` is NOT a top-level key: it lives inside `triggers` at any nesting level as an evaluation-transparent annotation (see Trigger Grammar). A header with `draft: true` is treated as nonexistent during discovery and evaluation: it is not listed, not triggered, not loaded, and its `requires` entries resolve to nothing.

## Trigger Grammar

[ref: #include-trigger-grammar]

The `triggers` block is a **recursive node grammar**: a node is a YAML mapping whose entries are conditions, combinators, and annotations, nested to any depth (0..N).

- **Condition kinds (closed):** `always` (constant-true condition), `files` (shell probe), `request` (semantic match). No other condition kinds exist.
- **Combinators (closed):** `any:` — a child node whose entries combine by **OR**; `all:` — a child node whose entries combine by **AND**. Entries inside a combinator may themselves be conditions or nested combinators, recursively.
- **Default combination:** sibling conditions at one level without a combinator combine by **OR** (any match activates).
- **Annotation:** `reason` — a free-text explanation of what the node or condition activates and why; legal at **every** level, as a sibling of any condition or combinator. Evaluation MUST ignore `reason` entirely: it documents the trigger for lexical reading and never changes the outcome. A root-level `always: true` MUST carry a sibling `reason`.

```yaml
triggers:                                 # unconditional load
  always: true
  reason: "<why always active>"

triggers:                                 # flat conditions (OR)
  files: "<shell probe>"
  request: "<keywords and phrases>"

triggers:                                 # explicit OR
  any:
    files: "<shell probe>"
    request: "<keywords and phrases>"

triggers:                                 # explicit AND, annotated
  all:
    files: "test -d .serena/memories"
    reason: "precondition: memory corpus exists"
    request: "<keywords and phrases>"

triggers:                                 # nested 0..N — legal at any depth
  any:
    all:
      files: "<shell probe>"
      request: "<keywords>"
    request: "<other keywords>"
    reason: "why this whole branch exists"
```

Evaluation of a node: collect the results of every non-`reason` entry (conditions evaluate directly, `any:`/`all:` recurse), then combine them by the node's mode — OR for plain nodes and `any:` children, AND for `all:` children.

## Trigger Evaluation

[ref: #include-trigger-evaluation]

Evaluate a header's conditions against the current user message plus project context. This section owns ONLY the semantics of each condition kind; condition COMBINATION is owned by the Trigger Grammar, and the ORDER, short-circuit, and load procedure are owned by the Evaluation Pipeline.

1. `always: true` — the condition is constant-true: it loads the skill unconditionally, for every task.
2. `files: "<shell command>"` — run the command in the workspace root **at bootstrap only**; **exit code 0 means match**. **Probe law:** the command MUST exit non-zero when the target is absent. Bare `fd` is FORBIDDEN as a probe — `fd` exits 0 even with zero matches. Canonical existence probe: `fd -e py --max-results 1 | wc -l | grep -q 1` (cap `fd` at one hit, count it, gate through `grep -q`). Content probes use `rg` (exits 1 on no match); directory probes use `test -d`. **Prefer STRUCTURAL probes** (extension, directory, exact config filename) over content greps: a content probe matches prose as readily as code — observed live in this workspace, `rg -i 'temporal'` matched the skills repository's own documentation and force-loaded `temporal-lang` for a whole session. If a content probe is unavoidable, anchor it to code-shaped markers (decorators, import statements), never to bare words.
3. `request: "<keywords>"` — **semantic** match against the user's request and the inferred session work, never naive substring matching.

## Runtime Re-Evaluation

[ref: #include-runtime-reevaluation]

Skills opt into mid-session activation with `runtime: true`. This section owns the opt-in mechanics (bootstrap awareness read, frozen `files` gates, memory-based re-check, activation semantics); where these mechanics sit in the evaluation order is owned by the Evaluation Pipeline.

1. **Bootstrap awareness read.** When a `runtime: true` skill's triggers do NOT fire at bootstrap, the loader still reads the skill's `SKILL.md` in full right then — purely for awareness: the agent learns the skill's feature set, its `request` conditions, and the domain its `description` names, and keeps them in mind as capabilities it can connect on demand. Awareness is NOT activation: the skill's rules do not apply yet, its `requires` are not resolved, and its reference corpus is not routed.
2. By default triggers evaluate once, at session start. **`files` gates run ONLY at bootstrap** — they are never re-executed mid-session.
3. After **every new user message**, for each `runtime: true` skill not yet activated, the agent re-evaluates **from memory**: it matches the message against the `request` conditions and the domain remembered from the bootstrap read, and notices when the conversation reaches anything described there. Do NOT re-read the `SKILL.md` for this check; do NOT re-run shell probes.
4. On a match, ACTIVATE the skill: the `SKILL.md` body is already in context from the bootstrap read, so activation means applying its rules to all subsequent actions, resolving `requires` transitively, and routing its reference corpus per the skill's own lazy-load protocol.
5. Skills without `runtime:` (or `runtime: false`) are never read at bootstrap "just in case" and never re-evaluated mid-session.

## Requires Resolution

[ref: #include-requires-resolution]

1. When a skill is marked for loading, mark every skill in its `requires` list as well.
2. Repeat transitively until no new skills are added; the loaded set is the **closure** under `requires`.
3. A `requires` entry pointing at a `draft: true` or missing skill resolves to nothing (with a warning to the user when noticed).
4. Cycles are non-conformant: report them to the user instead of walking them.

## Skill Discovery

[ref: #include-skill-discovery]

A skill directory is any directory containing a `SKILL.md` entry point. Discover candidates in this priority order:

1. `.kimi/skills/` in the project root.
2. `.agents/skills/` in the project root.
3. Any other directories exposed by the environment (e.g. `~/.config/kimi/skills`, harness built-ins).

Batch-extract every header in one command (core §6, Form 2 applied to discovery):

```bash
fd -t f SKILL.md .kimi/skills .agents/skills <other-dirs> 2>/dev/null | LC_ALL=C sort -u | while IFS= read -r f; do printf '\n### %s\n' "$f"; awk '/^---[ \t]*$/{c++; if(c==2) exit; next} c==1{print}' "$f"; done
```

Then: drop every header carrying `draft: true`, and evaluate the rest per Trigger Evaluation. Subagents never use the `.kimi/skills` symlink; they read skills from the `.kimi/mirror/` copy.

## Boot Contract

[ref: #include-boot-contract]

The fixed startup chain that resolves the chicken-and-egg of header evaluation:

1. The **system prompt** instructs the agent to execute the Startup Gate owned by the `bootstrap` skill.
2. The gate's **forced import** reads `frontmatter-protocol/SKILL.md` in full; that file's **boot hard gate** (core §1) obliges the agent to read THIS file whole and apply it.
3. Only then does the agent run Skill Discovery and the Evaluation Pipeline over all other skills' headers.
4. `bootstrap` declares `requires: [frontmatter-protocol]`, so any bootstrap-driven session inherits this chain.

Until steps 1–2 complete, no skill header may be evaluated: the rules for evaluation live here.

## Version Policy

[ref: #include-version-policy]

- `version` is part of the schema: a semver string (`MAJOR.MINOR.PATCH`).
- During the transition, many skills carry no `version`: treat absence as `0.0.0` and do NOT report it as an error. Version rollout is owned manually; agents ignore the gaps.
- When present, `version` is informational metadata for compatibility reasoning; it does not affect trigger evaluation.

## Evaluation Pipeline

[ref: #include-evaluation-pipeline]

Trigger evaluation MUST run as a fixed pipeline, in this exact order, for every discovered header:

1. **Draft gate.** The header carries `draft: true` → SKIP entirely: not listed, not triggered, its `requires` entries resolve to nothing.
2. **Always gate.** `always: true` → LOAD unconditionally; condition evaluation is skipped.
3. **Condition evaluation.** Otherwise evaluate the `triggers` conditions:
   - `files` conditions run FIRST (cheap, deterministic shell commands; exit 0 means match), `request` conditions LAST (semantic match).
   - Flat conditions and `any:` (OR): short-circuit — stop at the first match → LOAD.
   - `all:` (AND): fail-fast — stop at the first non-match → SKIP.
4. **Load.** On a positive decision, read the skill's `SKILL.md` in full (trigger override: load even when the topic feels familiar), then resolve `requires`.
5. **Requires closure.** Walk `requires` with a visited set until no new skills are added (semantics: Requires Resolution). An edge pointing back into the current dependency chain is a CYCLE: report it to the user and drop the edge — never walk cycles.
6. **Runtime bootstrap read.** For each `runtime: true` skill whose triggers did not fire in steps 1–3, apply the bootstrap awareness read from Runtime Re-Evaluation.
7. **Runtime re-evaluation.** After every new user message, apply the re-check-from-memory mechanics from Runtime Re-Evaluation; on a match, activate and run step 5 (`requires` closure).

Determinism contract: identical header set + identical workspace + identical request MUST yield an identical load decision. The only non-mechanical step is `request` semantic matching; every other gate is byte- or exit-code-exact.

## Built-in skill-creator Override

[ref: #include-skill-creator-override]

The built-in `skill-creator` skill mandates a two-key frontmatter (`name` + `description` only) and discourages auxiliary files such as `README.md`. In THIS project those rulings are overridden:

**External alignment.** The public Agent Skills specification (agentskills.io, Anthropic platform docs) defines exactly two required fields — `name` (≤64 chars, lowercase kebab) and `description` (≤1024 chars); everything else is implementation-specific. This project's schema is a deliberate SUPERSET of that public baseline: `triggers`, `requires`, `runtime`, `version`, `draft` are project extensions owned by this extension; `name` and `description` stay compatible with the public spec.

1. The closed schema of this extension (with `triggers`, `requires`, `runtime`, `reason`, `version`, `draft`) is the single legal header form; the two-key rule does not apply.
2. `README.md` files are a repository convention and remain welcome for humans.
3. Everything else in `skill-creator` (concise bodies, progressive disclosure, bundled resources, the iteration workflow) remains valid process guidance. On any conflict, THIS standard wins.
