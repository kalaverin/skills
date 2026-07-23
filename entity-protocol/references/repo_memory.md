---
subject: "Repo-scoped memory model; `repo` frontmatter field domain axis, legal values, lazy normalization, git-anchor chain, findings evidence severity, location, commit hash, two-level deprecation registry, canonical names, read-side write-side duties, aliases, provenance."
index:
  - anchor: entity-repo-field
    what: "The `repo` frontmatter field as domain axis naming what the memory is about, with two legal value classes and the git-anchor chain supplying `branch`/`commit`/`committed_at`."
    problem: "Agent stamps memory headers and must pick domain value plus git source; wrong umbrella value or wrong git anchor falsifies freshness checks across workspace; header drift, legacy values, provenance confusion, stale watermark, bad commit, fallback ordering, normalization timing."
    use_when: "Stamping or validating any memory header; choosing between `<repo-name>` and `generic`; resolving which git repository anchors tracking fields; deciding whether normalization fires on this mutation."
    avoid_when: "Memory path naming conventions — `serena-protocol` `[ref: #serena-naming]` owns those; scope routing questions — `[ref: #entity-namespace-registry]` owns those."
    expected: "Every header carries one legal domain value and tracking fields stamped from the correct git anchor."
  - anchor: entity-findings-traceability
    what: "The evidence format every finding declares: severity taxonomy, `path:line` location, and commit hash stamped by the ROOT agent via `git log -1`."
    problem: "Findings land in memory without verifiable anchors; weeks later nobody can check whether claim still holds or where it came from; unverifiable claims, missing evidence, lost provenance, hallucination risk, audit failure, orphan notes."
    use_when: "Writing any finding memory (`bugs`, `notes`, `decisions`, `style`, `todo`, `plans`, `proposals`, `reports`); persisting subagent-reported findings; reviewing evidence quality of existing findings."
    avoid_when: "Choosing which scope receives the finding — routing lives in `[ref: #entity-namespace-registry]`; card production duties — `[ref: #entity-card-workflow]`."
    expected: "Every finding carries severity, exact `path:line`, and root-stamped commit hash."
  - anchor: entity-deprecations
    what: "The two-level deprecation registry (`agent/deprecations` project-wide plus `deprecations/<repo>/` repo-scoped) with mandatory read-side and write-side duties around card runs."
    problem: "Old names, aliases, renamed modules circulate in prompts and code; agent writes new memories under dead names and cards fork identity; naming drift, alias chaos, duplicate cards, legacy endpoints, renamed services, stale references."
    use_when: "Before producing or updating any card — read-side HARD duty; after run when newly deprecated names surfaced — write-side duty; encountering alias for known repo."
    avoid_when: "Findings about dead code inside one repo — those route to `notes/<repo>/` or `style/<repo>/`; physical legacy-scope migration — `[ref: #entity-migration-legacy]`."
    expected: "Canonical names applied throughout every run; newly found deprecations appended to the correct level."
---

# Repo-Scoped Memory Model (entity-protocol reference)

The `repo` frontmatter field, findings traceability, and the deprecation registry. The namespace registry lives in `entity-protocol/SKILL.md` (`[ref: #entity-namespace-registry]`). Loaded lazily via the routing index.

## The `repo` Field (Domain Axis and Git-Anchor Chain)

[ref: #entity-repo-field]

The `repo` field names the **domain entity the memory is about** (domain axis), not the git remote hosting the file. Two legal value classes:

1. `repo: <repo-name>` — the memory concerns a known entity (a service, a library, a game component such as a renderer or an input controller).
2. `repo: generic` — the memory concerns the whole project/workspace as a domain object, is cross-project, or the entity cannot be determined. `generic` is the ONLY legal umbrella value. Legacy values (`serena`, `project`, directory names) normalize to `generic` lazily — only on the next mutation of that memory; never batch-rewrite.

**Git-anchor chain (tracking axis).** The `branch`/`commit`/`committed_at` fields are stamped from the git repository that anchors the domain object named by `repo`:

1. Entity with its own `.git` → that git.
2. Entity-component without its own `.git` (e.g. a renderer inside the game repo) → the containing project git. Component and `generic` memories then carry identical commits — expected: the git is one.
3. `generic` → the **project root git** when it exists (the project git ALWAYS takes priority over the Serena meta-git); otherwise the `.serena/` meta-repository's own git (fallback for git-less monorepo workspaces); otherwise **HARD STOP** — the agent cannot version documents and must report to the user instead of writing.

## Findings Traceability

[ref: #entity-findings-traceability]

EVERY finding must be anchored to a specific file, line, AND the exact commit hash of that file at the moment of exploration.

**Division of labor (HARD):** the SUBAGENT never runs git — it anchors each finding to `path/to/file.py:line_num` plus the symbol name. The ROOT agent stamps the exact commit hash when persisting the finding memory, using:

```bash
git log -1 --format=%H -- <relative-file-path>
```

Each finding must declare:

- **Severity:** `critical` (breaks functionality, security, or data; money at risk), `warning` (inconsistency, tech debt, maintainability), `info` (observation, style, documentation gap).
- **Location:** `path/to/file.py:line_num`
- **Hash:** `(commit <hash>)` — stamped by the ROOT agent at persistence, never by the subagent.

## Deprecated Names and Aliases

[ref: #entity-deprecations]

Deprecations live at two levels:

1. **Project-wide** — a deprecation table in `agent/deprecations` (deprecated repo names, cross-repo aliases).
2. **Repo-scoped** — `deprecations/<repo>/<topic>` memories for names/aliases deprecated INSIDE one repo (old service endpoints, renamed modules, legacy workflow names).

Example table structure:

| Name | Status | Canonical / Replacement | Implications |
|------|--------|------------------------|--------------|
| `<old-name>` | Deprecated | `<new-name>` | Treat `<old-name>` as legacy; do not create new cards. |

Every project must document its own deprecated repo names and aliases. Cards and new memories must use canonical names.

**Read-side duty (HARD):** before producing or updating any card, the root agent MUST read BOTH levels — `agent/deprecations` AND `deprecations/<repo>/...` for the target repo — and apply the canonical names throughout the run. New deprecations or aliases discovered during the run are appended to the appropriate level after the run — write-side and read-side are both mandatory.
