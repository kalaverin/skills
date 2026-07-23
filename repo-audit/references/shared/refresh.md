# REFRESH Mode — Diff-Driven Update (repo-audit)

[ref: #ra-refresh]

The update mode for stale artifacts. Entry points: the freshness gate detected stale inputs, the user reports stale cards, or the agent itself notices staleness (`[ref: #entity-freshness]`). The goal: update the affected artifacts surgically from the git diff instead of re-running the full pipeline.

## 1. Staleness detector

Run per artifact (`repos/<repo>/overview`, `repos/<repo>/business`, `repos/<repo>/dependencies`), using the artifact's own frontmatter `commit` as the base:

```bash
cd <repo_path>
git rev-list --count <card_commit>..HEAD                     # commits behind
git diff --shortstat <card_commit>..HEAD -- . ':(exclude)*lock*' ':(exclude)**/gen/**' ':(exclude)**/vendor/**' ':(exclude)**/tests/**' ':(exclude)**/test/**'
git diff --name-only <card_commit>..HEAD -- . ':(exclude)*lock*' ':(exclude)**/gen/**' ':(exclude)**/vendor/**' ':(exclude)**/tests/**' ':(exclude)**/test/**' | wc -l
git ls-files -- . ':(exclude)*lock*' ':(exclude)**/gen/**' ':(exclude)**/vendor/**' ':(exclude)**/tests/**' ':(exclude)**/test/**' | wc -l
git ls-files -- . ':(exclude)*lock*' ':(exclude)**/gen/**' ':(exclude)**/vendor/**' ':(exclude)**/tests/**' ':(exclude)**/test/**' | xargs wc -l | tail -1
```

Noise exclusions are MANDATORY: lockfiles (`*lock*`), generated code (`**/gen/**`), vendored code (`**/vendor/**`), and tests (`**/tests/**`, `**/test/**`) never count toward staleness.

## 2. Present metrics and ALWAYS ask the user

Per stale artifact, present:

```text
<artifact>: <N> commits behind; <M> files changed of <F> (<P>%); +<X>/−<Y> lines (<L> total, <Q>% of codebase)
```

Then ALWAYS ask the user which mode to run — never auto-decide. Recommendation rule:

- `< 1000` changed lines AND `< 10%` of the codebase → recommend **REFRESH** (surgical update is cheap).
- `> 5000` changed lines OR `> 30%` → recommend **FULL** (surgery costs more than a rebuild).
- In between → no recommendation; the user decides.

## 3. Prepare the scratch diff (root agent only)

```text
.tmp/repo-audit/
├── diff-<card_commit>..HEAD.patch      # full diff (with the same exclusions)
├── numstat.txt                         # per-file change statistics
└── impact.md                           # root's analysis: which artifacts/sections are affected
```

`impact.md` maps the changed paths to artifacts via the impact map below and lists the exact memory files each refresh subagent must read.

## 4. Diff → artifact impact map

| What changed in the diff | Artifacts to update |
|---|---|
| `proto/`, `app/api/`, servicers/routers | `overview` (interface sections) → `dependencies` (provided interface, diagram) |
| `app/workflow/`, `worker.py`, signals/cron | `overview` → `business` (processes) → `dependencies` |
| Models/schemas/migrations, status enums | `business` (entities, rules) |
| External-system clients, webhooks | `business` (integrations) → `dependencies` (downstream) |
| `pyproject.toml`, `uv.lock`, `go.mod`, `package.json` | `overview` (tech stack) → `dependencies` (infra & libs) |
| Behavior-driving constants/config | `business` (rules) |
| `apps/base/`, `clusters/`, HelmRelease | `overview` (infra sections) → `dependencies` |

The cascade runs left to right: an interface change also refreshes `dependencies`. Each affected artifact's `commit` is bumped to HEAD after its update.

## 5. Refresh subagents

Launch **one read-only `explore` subagent per affected artifact** (maximum 3: overview / business / dependencies), timeout 3595 s. Each subagent receives:

- `diff_dir` = `.tmp/repo-audit/` (reads ONLY the diff + `impact.md`),
- the path list of the stale cards for its artifact,
- the common base prompt (`[ref: #ra-subagent-base]`) and its specialized prompt (`analysis/` or `generators/` per artifact).

Subagents return the UPDATED SECTIONS for their artifact. They never re-read the whole codebase.

## 6. Apply and finalize (root agent)

1. Apply the returned sections to the artifacts (`edit_memory`; never `write_memory` to append).
2. Bump each touched artifact's frontmatter: `commit` → HEAD, `branch`, `committed_at`, `updated_at`.
3. If `business` changed, update the glossaries with the delta (`added` / `refined` / `moved` markers).
4. Delete `.tmp/repo-audit/` (pytest-planner scratch convention).
5. Verify and persist per `serena-protocol` `[ref: #serena-memory-mutation]` (read-back + persistence command from the workspace root).
