# Shared Gates (repo-audit)

[ref: #ra-gates]

The gates every repo-audit run passes before any subagent launches. Applies to all three run modes (FULL / PARTIAL / REFRESH).

## 1. Input acceptance

- Obtain `repo_name` (snake_case) and `repo_path` (absolute) from the user. If unclear, ask before proceeding.
- Capture any business context or specific questions from the user's prompt and pass them to the domain subagents as the optional `business_context` input.
- **Exactly one repo per run.** If the request mentions multiple repos, STOP and ask the user to pick one. Do not batch repos.
- Exception: the project-level dependency index (`project/dependencies`) is inherently multi-repo and is generated only on explicit user request after every repo has a fresh `repos/<repo>/dependencies`.

## 2. Prerequisite gate

Apply `entity-protocol` `[ref: #entity-prerequisite]`:

- If `repos/` is empty, STOP and ask the user to create the first repo card via repo-audit.
- If the target repo has no card at `repos/<repo>/overview` and the request is anything other than creating that card, STOP and ask the user to create it first. Do not guess names.
- The meta-entity `project` is exempt (`[ref: #entity-namespace-registry]`).

## 3. Mode selection

| Condition | Mode |
|---|---|
| No `repos/<repo>/overview` exists, or the user explicitly asks for a full audit | **FULL** |
| Card exists; user asks for one artifact (e.g. only dependencies, only business) | **PARTIAL** |
| Any required input memory is stale (`commit` ≠ repo HEAD), or the user reports stale cards | **REFRESH** — always ask the user first, presenting staleness metrics (`[ref: #ra-refresh]`) |

## 4. Freshness gate (HARD, PARTIAL mode)

Before generating a downstream artifact from existing memory:

1. Read the frontmatter `commit` of every required input (`repos/<repo>/overview`, `repos/<repo>/business`, plus task-specific inputs).
2. Compare with the repo HEAD (collect branch/commit/timestamp per `[ref: #tracking-git-commands]`, run inside `<repo_path>`).
3. All input memories must also be mutually consistent (same entity-repo commit generation).
4. If any input is stale, missing, or inconsistent → do NOT generate. Run the REFRESH-mode flow (`[ref: #ra-refresh]`): present staleness metrics and ask the user.

In FULL mode, inputs are produced fresh by the pipeline itself; the gate is trivially satisfied.

## 5. Naming compliance

Verify every memory path for this repo complies with `serena-protocol` `[ref: #serena-naming]` (snake_case, no hyphens). Rename non-compliant paths immediately, before analysis.

## 6. Glossary seeds

Check whether `project/glossary` and `repos/<repo>/glossary` exist. Create seed glossaries where missing before launching subagents (contract: `references/templates/glossary_routing.md`).

## 7. Memory path collection

Build the absolute path list of all relevant `.serena/memories/` files for this repo: `repos/<repo>/...` (overview, business, split files, glossary, dependencies), `project/glossary`, findings (`bugs|notes|decisions|style|todo|plans|proposals|reports/<repo>/...`). The root agent does NOT read the contents itself — it passes only the path list to subagents.
