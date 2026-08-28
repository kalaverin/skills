---
subject: "Repo-audit run gates; input acceptance, one repo per run, prerequisite card gate, run-mode selection FULL PARTIAL REFRESH, freshness gate, naming compliance, glossary seeds, memory path collection, `repos/<repo>/overview`, `project/dependencies`, hard stops, user decisions."
index:
  - anchor: ra-gates
    what: "The gate sequence every repo-audit run passes before any subagent launches, shared by all three run modes."
    problem: "Run launches subagents before checking repo, card, and memory state; wrong repo, missing card, stale memories rot every downstream artifact; premature fan-out, gate bypass, rework, output decay, wasted waves, rotten inputs, unchecked launch, downstream damage."
    use_when: "Starting any repo-audit run in any mode; reviewing why a run stopped early; adding a new gate."
    avoid_when: "Wave orchestration details — `references/analysis/` and `references/generators/` prompts; refresh detector mechanics — `[ref: #ra-refresh]`."
    expected: "Every run passes all gates or stops with a user-visible reason."
  - anchor: ra-gates-input
    what: "Input acceptance: `repo_name`/`repo_path` resolution, optional `business_context` capture, the one-repo-per-run rule and its project-index exception."
    problem: "Audit starts with ambiguous target or batch of repos; outputs merge contexts and cross-contaminate cards; mixed contexts, vague scope, contaminated output, cross-talk, identity mix, input fuzz, scope creep, handoff friction, intake failure."
    use_when: "Accepting user input for any run; request mentions several repos; optional business context present in prompt."
    avoid_when: "Project-level dependency index generation — inherently multi-repo per `[ref: #ra-tpl-deps-project]`."
    expected: "Exactly one repo resolved with snake_case name, absolute path, and captured context."
  - anchor: ra-gates-prerequisite
    what: "The prerequisite gate application: card existence at `repos/<repo>/overview` with STOP procedures and the meta-entity exemption."
    problem: "Analysis writes into repo-scoped namespaces without canonical card; identity and layout of every artifact lack anchor; missing card, implicit creation, name guessing, unanchored writes, gate violation, identity vacuum, layout chaos, downstream corruption."
    use_when: "Before any repo-scoped write or analysis run; `repos/` scope empty; target repo card missing."
    avoid_when: "Creating the card itself — that is the FULL audit run; meta-entity `project` writes are exempt per `[ref: #entity-namespace-registry]`."
    expected: "Run proceeds only with existing card or explicit user decision."
  - anchor: ra-gates-mode
    what: "The run-mode selection table: FULL, PARTIAL, REFRESH conditions."
    problem: "Wrong mode picked wastes waves on re-exploration or silently reuses rotten inputs; mode confusion, wasted subagents, stale reuse, redundant exploration, wrong strategy, budget burn, signal loss, decision paralysis, mode misfire, user surprise."
    use_when: "Choosing mode at run start; card exists but user asks one artifact; any input stale."
    avoid_when: "Mode internals — FULL pipeline lives in repo-audit/SKILL.md, REFRESH flow in `[ref: #ra-refresh]`."
    expected: "One mode selected deterministically from card existence and freshness."
  - anchor: ra-gates-freshness
    what: "The HARD freshness gate for PARTIAL mode: per-input commit vs HEAD comparison and the stale-input stop."
    problem: "PARTIAL run generates artifact from stale inputs; dependency card built on last month's truth misleads every consumer; outdated commits, consumer deception, freshness lapse, hidden drift, rotten reuse, watermark gap, verification skip, trust erosion."
    use_when: "PARTIAL mode before any generation; input memory commit differs from repo HEAD; consistency across inputs required."
    avoid_when: "FULL mode — pipeline produces fresh inputs itself; REFRESH flow — that is `[ref: #ra-refresh]`."
    expected: "Generation only from inputs whose commit equals repo HEAD."
  - anchor: ra-gates-naming
    what: "Naming compliance check: snake_case enforcement and immediate rename of non-compliant memory paths."
    problem: "Memory paths arrive with hyphens and spaces from legacy directories; every route and link into those memories silently breaks; invalid characters, non-compliant paths, broken links, naming drift, rename postponement, routing decay, anchor rot."
    use_when: "Any run touching memory paths for the repo; existing path violates convention."
    avoid_when: "Naming grammar itself — `serena-protocol` `[ref: #serena-naming]` owns it."
    expected: "Every path compliant before analysis starts."
  - anchor: ra-gates-glossary-seeds
    what: "Glossary seeding: create project and repo glossaries where missing before launching subagents."
    problem: "Domain subagents start work while glossary files do not exist; terminology lands in ad-hoc places and drifts apart; fragmented terminology, missing glossary, scattered terms, lost definitions, vocabulary drift, seed absence, onboarding friction, naming chaos."
    use_when: "Before analysis wave; `project/glossary` or `repos/<repo>/glossary` absent."
    avoid_when: "Glossary update mechanics — `references/templates/glossary_routing.md` owns them."
    expected: "Both glossaries exist as seeds before any subagent launches."
  - anchor: ra-gates-memory-paths
    what: "The memory path collection: absolute path list of all relevant `.serena/memories/` files passed to subagents without reading contents."
    problem: "Subagents launch with no memory context at all, or with full memory contents inlined into prompts; context flooding, missing context, prompt bloat, path absence, inline dumping, token waste, inventory gap, orchestration failure, context starvation."
    use_when: "Preparing any subagent launch; assembling repo-relevant memory inventory."
    avoid_when: "Reading memory contents — root never reads; subagents read paths themselves per `[ref: #ra-subagent-memory-reading]`."
    expected: "Complete path list covers cards, business, dependencies, glossary, and findings scopes."
---

# Shared Gates (repo-audit)

[ref: #ra-gates]

The gates every repo-audit run passes before any subagent launches. Applies to all three run modes (FULL / PARTIAL / REFRESH).

## 1. Input acceptance

[ref: #ra-gates-input]

- Obtain `repo_name` (snake_case) and `repo_path` (absolute) from the user. If unclear, ask before proceeding.
- Capture any business context or specific questions from the user's prompt and pass them to the domain subagents as the optional `business_context` input.
- **Exactly one repo per run.** If the request mentions multiple repos, STOP and ask the user to pick one. Do not batch repos.
- Exception: the project-level dependency index (`project/dependencies`) is inherently multi-repo and is generated only on explicit user request after every repo has a fresh `repos/<repo>/dependencies`.

## 2. Prerequisite gate

[ref: #ra-gates-prerequisite]

Apply `entity-protocol` `[ref: #entity-prerequisite]`:

- If `repos/` is empty, STOP and ask the user to create the first repo card via repo-audit.
- If the target repo has no card at `repos/<repo>/overview` and the request is anything other than creating that card, STOP and ask the user to create it first. Do not guess names.
- The meta-entity `project` is exempt (`[ref: #entity-namespace-registry]`).

## 3. Mode selection

[ref: #ra-gates-mode]

| Condition | Mode |
|---|---|
| No `repos/<repo>/overview` exists, or the user explicitly asks for a full audit | **FULL** |
| Card exists; user asks for one artifact (e.g. only dependencies, only business) | **PARTIAL** |
| Any required input memory is stale (`commit` ≠ repo HEAD), or the user reports stale cards | **REFRESH** — always ask the user first, presenting staleness metrics (`[ref: #ra-refresh]`) |

## 4. Freshness gate (HARD, PARTIAL mode)

[ref: #ra-gates-freshness]

Before generating a downstream artifact from existing memory:

1. Read the frontmatter `commit` of every required input (`repos/<repo>/overview`, `repos/<repo>/business`, plus task-specific inputs).
2. Compare with the repo HEAD (collect branch/commit/timestamp per `[ref: #tracking-git-commands]`, run inside `<repo_path>`).
3. All input memories must also be mutually consistent (same entity-repo commit generation).
4. If any input is stale, missing, or inconsistent → do NOT generate. Run the REFRESH-mode flow (`[ref: #ra-refresh]`): present staleness metrics and ask the user.

In FULL mode, inputs are produced fresh by the pipeline itself; the gate is trivially satisfied.

## 5. Naming compliance

[ref: #ra-gates-naming]

Verify every memory path for this repo complies with `serena-protocol` `[ref: #serena-naming]` (snake_case, no hyphens). Rename non-compliant paths immediately, before analysis.

## 6. Glossary seeds

[ref: #ra-gates-glossary-seeds]

Check whether `project/glossary` and `repos/<repo>/glossary` exist. Create seed glossaries where missing before launching subagents (contract: `references/templates/glossary_routing.md`).

## 7. Memory path collection

[ref: #ra-gates-memory-paths]

Build the absolute path list of all relevant `.serena/memories/` files for this repo: `repos/<repo>/...` (overview, business, split files, glossary, dependencies), `project/glossary`, findings (`bugs|notes|decisions|style|todo|plans|proposals|reports/<repo>/...`). The root agent does NOT read the contents itself — it passes only the path list to subagents.
