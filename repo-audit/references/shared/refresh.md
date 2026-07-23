---
subject: "REFRESH mode diff-driven update; staleness detector, thresholds, user metrics prompt, `.tmp/repo-audit/` scratch, diff artifact impact map, refresh subagents, root finalize, `git diff`, numstat, tracking bump, per-artifact patches, glossary delta, persistence, exclusions."
index:
  - anchor: ra-refresh
    what: "The REFRESH-mode pipeline: diff-driven surgical update of stale artifacts instead of re-running the full audit."
    problem: "Cards lag behind code and user asks update; full re-audit burns waves on mostly-unchanged repo while ignoring drift rots trust; stale cards, update request, drift accumulation, full-rerun cost, precision editing, trust decay, mode selection."
    use_when: "Any required input stale (`commit` ≠ HEAD); user reports outdated cards; REFRESH selected by the mode gate."
    avoid_when: "No card exists or user wants complete re-audit — FULL mode; single artifact with fresh inputs — PARTIAL mode."
    expected: "Stale artifacts updated strictly from the diff with user-approved strategy."
  - anchor: ra-refresh-detector
    what: "The staleness detector: changed-lines and percentage metrics computed from `git diff` with lockfile/generated/vendor/test exclusions."
    problem: "Agent cannot say how stale cards are; recommendation without metrics is guesswork and user decides blind; staleness unknown, metric absence, drift unmeasured, decision vacuum, inflated counts, exclusion neglect, hunch-driven advice, evidence-free guidance."
    use_when: "Starting any REFRESH evaluation; computing how much code changed since the recorded commit; preparing the user prompt."
    avoid_when: "Exclusion-free raw diffs — lockfiles, generated code, vendor code, and tests are always excluded from the metrics."
    expected: "Absolute and percentage staleness numbers ready for the user prompt."
  - anchor: ra-refresh-metrics-ask
    what: "The mandatory user prompt with staleness metrics and the threshold-based recommendation (<1000 lines & <10% → REFRESH; >5000 lines or >30% → FULL)."
    problem: "Agent auto-decides refresh strategy and silently rewrites cards; user loses control over expensive operations that reshape canonical knowledge; self-decision, consent absence, threshold breach, strategy hijack, blind approval, control loss, unapproved mutation."
    use_when: "Every REFRESH run before any scratch preparation; presenting metrics; thresholds shape the recommendation only."
    avoid_when: "Treating thresholds as hard rules — they shape only the recommendation; the user ALWAYS decides."
    expected: "User explicitly approves the strategy after seeing staleness metrics."
  - anchor: ra-refresh-scratch
    what: "The `.tmp/repo-audit/` scratch directory: diff patches, numstat, and `impact.md` prepared by the root agent."
    problem: "Refresh subagents need diff input but have zero git access; missing scratch forces codebase re-reads and voids mode purpose; workspace gap, git-less workers, wholesale fallback, goal collapse, per-run hygiene, preparation lapse."
    use_when: "After user approves REFRESH; preparing subagent inputs; computing per-artifact diffs."
    avoid_when: "Sharing scratch across runs — it is per-run and deleted at finalize; never place it inside `.serena/`."
    expected: "Scratch contains per-artifact patches, numstat, and the impact map."
  - anchor: ra-refresh-impact-map
    what: "The diff→artifact impact map: which changed paths invalidate which card sections."
    problem: "Root stares at diff output without knowing which artifacts it invalidates; updating everything burns effort, updating blindly loses sections; impact unknown, unseen impact, section loss, mapping gap, scope confusion, touch analysis, attribution failure."
    use_when: "Building `impact.md` from the diff; deciding which artifacts need refresh subagents; scoping per-artifact work."
    avoid_when: "Using the map to re-read code — it scopes which artifacts update, never what to read."
    expected: "Every changed path assigned to affected artifacts or explicitly ignored."
  - anchor: ra-refresh-subagents
    what: "One refresh subagent per affected artifact (max 3) reading only the diff and the stale cards."
    problem: "One giant subagent updates all artifacts and cross-contaminates sections, or re-reads whole codebase anyway; oversized scope, cross-contamination, wholesale reading, boundary blur, parallel confusion, context mixing, isolation loss, fan-out waste, mission creep, diff bypass."
    use_when: "Dispatching refresh work after scratch preparation; one artifact stale; all three stale."
    avoid_when: "More than three artifacts — the set is bounded to overview, business, dependencies."
    expected: "Each affected artifact gets exactly one diff-scoped subagent."
  - anchor: ra-refresh-finalize
    what: "Root finalization: apply returned sections, bump tracking fields, update glossaries on business delta, delete scratch, verify and persist."
    problem: "Run ends with applied edits but stale headers and leftover scratch; freshness metadata lies and next run mis-detects staleness; persist skip, finalize lapse, false drift, header decay, debris accumulation, verification gap."
    use_when: "After refresh subagents return; applying updated sections; closing the run."
    avoid_when: "Partial application without header bump — header fields move together per `[ref: #tracking-fields]`."
    expected: "Artifacts updated, headers bumped to HEAD, scratch deleted, persistence verified."
---

# REFRESH Mode — Diff-Driven Update (repo-audit)

[ref: #ra-refresh]

The update mode for stale artifacts. Entry points: the freshness gate detected stale inputs, the user reports stale cards, or the agent itself notices staleness (`[ref: #entity-freshness]`). The goal: update the affected artifacts surgically from the git diff instead of re-running the full pipeline.

## 1. Staleness detector

[ref: #ra-refresh-detector]

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

[ref: #ra-refresh-metrics-ask]

Per stale artifact, present:

```text
<artifact>: <N> commits behind; <M> files changed of <F> (<P>%); +<X>/−<Y> lines (<L> total, <Q>% of codebase)
```

Then ALWAYS ask the user which mode to run — never auto-decide. Recommendation rule:

- `< 1000` changed lines AND `< 10%` of the codebase → recommend **REFRESH** (surgical update is cheap).
- `> 5000` changed lines OR `> 30%` → recommend **FULL** (surgery costs more than a rebuild).
- In between → no recommendation; the user decides.

## 3. Prepare the scratch diff (root agent only)

[ref: #ra-refresh-scratch]

```text
.tmp/repo-audit/
├── diff-<card_commit>..HEAD.patch      # full diff (with the same exclusions)
├── numstat.txt                         # per-file change statistics
└── impact.md                           # root's analysis: which artifacts/sections are affected
```

`impact.md` maps the changed paths to artifacts via the impact map below and lists the exact memory files each refresh subagent must read.

## 4. Diff → artifact impact map

[ref: #ra-refresh-impact-map]

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

[ref: #ra-refresh-subagents]

Launch **one read-only `explore` subagent per affected artifact** (maximum 3: overview / business / dependencies), timeout 3595 s. Each subagent receives:

- `diff_dir` = `.tmp/repo-audit/` (reads ONLY the diff + `impact.md`),
- the path list of the stale cards for its artifact,
- the common base prompt (`[ref: #ra-subagent-base]`) and its specialized prompt (`analysis/` or `generators/` per artifact).

Subagents return the UPDATED SECTIONS for their artifact. They never re-read the whole codebase.

## 6. Apply and finalize (root agent)

[ref: #ra-refresh-finalize]

1. Apply the returned sections to the artifacts (`edit_memory`; never `write_memory` to append).
2. Bump each touched artifact's frontmatter: `commit` → HEAD, `branch`, `committed_at`, `updated_at`.
3. If `business` changed, update the glossaries with the delta (`added` / `refined` / `moved` markers).
4. Delete `.tmp/repo-audit/` (pytest-planner scratch convention).
5. Verify and persist per `serena-protocol` `[ref: #serena-memory-mutation]` (read-back + persistence command from the workspace root).
