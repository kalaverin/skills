---
subject: "Git document tracking extension; repo branch commit committed_at fields, stale_since marker, git triplet commands, validation timing, first invalidating commit, field update matrix, refresh on mutation, reconciliation ladder, presumed stale, scope limits, created_at updated_at timestamp semantics, field semantics table, optional tags rules."
index:
  - anchor: tracking-fields
    what: "The git-tracking key set `{repo, branch, commit, committed_at}` plus the `stale_since` marker — the fields that bind a document to a repository state."
    problem: "Document describes repository truth but carries no binding to that truth's revision; reader cannot tell whether content reflects current code or last year's; unbound documents, silent staleness, missing provenance, trust gap, freshness signal, version skew."
    use_when: "Stamping any document that mirrors repository state — Serena memories, audit reports, generated manifests; designing new tracked document kinds."
    avoid_when: "Files that ARE the versioned truth — skill files, references, source code never carry tracking fields."
    expected: "Every tracked document names its repository and exact verified revision; untracked drift becomes detectable."
  - anchor: tracking-git-commands
    what: "The canonical command triplet that fills the fields: abbreviated branch, short HEAD hash, strict-ISO commit date normalized to UTC `Z`."
    problem: "Agents hand-roll git calls with divergent flags — full hashes, local timezones, wrong fields — and downstream comparisons break on format mismatches; flag divergence, timezone bugs, hash length, inconsistent stamps, manual git calls, parsing pain."
    use_when: "Filling or refreshing `branch`/`commit`/`committed_at`; scripting freshness checks; teaching agents the exact invocations."
    avoid_when: "Repositories in broken ref states — verify ref consistency first; HEAD/reflog mismatches have bitten before."
    expected: "Every tracked document carries stamps from identical invocations, comparable byte-for-byte."
  - anchor: tracking-validation-timing
    what: "When validation happens: lazily — before tracked content influences a decision or work — and eagerly at every write of the document."
    problem: "Eager validation on every read taxes each lookup with three git calls; never validating lets stale content silently drive decisions; validation cost, lazy checks, write-time verification, decision gate, timing balance, git overhead."
    use_when: "Reading a tracked document to USE it; writing or mutating one; designing workflows over tracked corpora."
    avoid_when: "Casual browsing with no decision at stake — validation on mere reads is wasted work."
    expected: "Git checks run exactly at decision points and writes, never on passive reads."
  - anchor: tracking-staleness
    what: "Staleness protocol: compare recorded `commit` against HEAD; on drift annotate the frontmatter with `stale_since` pointing at first drift commit — WITHOUT bumping `commit`."
    problem: "Repository moved on after document verification; content may be wrong and nobody knows; silently bumping recorded hash would erase last-verified watermark and hide drift; revision drift, lost watermark, hidden changes, silent corruption, annotation duty, invalidating commit."
    use_when: "Detected drift between recorded and current HEAD; annotating a document whose verification lapsed; scanning corpora for stale entries."
    avoid_when: "First-time stamping — no drift exists before the initial verified write."
    expected: "Stale documents self-declare with `stale_since`; the last-verified watermark survives until reconciliation."
  - anchor: tracking-reconciliation
    what: "Reconciliation ladder: diff `commit..HEAD` against `source`; genuinely harmless churn clears `stale_since` silently and bumps the watermark; anything else asks the user."
    problem: "Drift detected, agent must decide: harmless churn or real invalidation; guessing wrong either nags users over cosmetics or blesses rotten content; reconciliation judgment, nag fatigue, diff review, user confirmation, clean diff, content update."
    use_when: "`stale_since` is set and the content is needed; clearing markers after review; escalating uncertain diffs."
    avoid_when: "Untracked documents — there is no watermark to diff against."
    expected: "Clean churn clears silently; real invalidation reaches the user with the diff summary."
  - anchor: tracking-refresh
    what: "Refresh-on-mutation: every document mutation MUST refresh the tracking fields to current repository state — except `commit`/`committed_at`, which move only on verification."
    problem: "Edit after edit, fields fossilize at ancient values while content evolves; readers trust stamps that stopped describing reality months ago; stale metadata, edit drift, trust erosion, refresh duty, mutation hook, watermark decay."
    use_when: "Any write or edit of a tracked document; wiring refresh into save flows; auditing why fields lag content."
    avoid_when: "The stale-annotation mutation itself — it refreshes `branch` only and MUST NOT bump `commit`."
    expected: "Fields describe present repository state after every verified mutation."
  - anchor: tracking-timestamps
    what: "The document timestamps `created_at` / `updated_at`: creation stamp immutable, update stamp refreshed on every content mutation, UTC ISO 8601 with `Z`."
    problem: "Timestamps fossilize at creation while content mutates under them; readers cannot tell fresh edits from ancient text, ordering and freshness reasoning collapse; frozen updated_at, forgotten refresh, edit invisibility, chronological drift, trust in stale dates."
    use_when: "Creating or mutating any frontmatter-carrying document; auditing why updated_at lags content; designing save flows that stamp dates."
    avoid_when: "Date fields that are domain data (due_date, event time) — those describe content, not document history."
    expected: "updated_at equals the last mutation moment after every edit; created_at never moves."
  - anchor: tracking-field-semantics
    what: "The strict per-field semantics table of the tracked-document header (meaning + authoritative source of every field) plus the optional-tags rules."
    problem: "Agents guess field meanings and invent ad-hoc tags; identical fields get divergent interpretations across documents, optional keys sprawl without purpose; semantic drift, tag pollution, undocumented keys, contradictory field usage, schema guessing."
    use_when: "Writing or reviewing any tracked-document header; deciding whether an extra tag is legitimate; teaching agents what each field means."
    avoid_when: "Domain-specific field additions — those are declared by the owning skill per core §9, not here."
    expected: "Every field carries one canonical meaning traced to its owning extension; tags appear only with purpose."
  - anchor: tracking-scope
    what: "Scope boundary: tracking applies to documents OUTSIDE the versioned source of truth — Serena memories, user markdowns — never to skill files, references, or code."
    problem: "Stamping versioned files duplicates what git already knows and creates two competing truths; skipping stamps on external documents leaves them unverifiable; git redundancy, scope confusion, boundary rules, applicability, memory corpus, user documents."
    use_when: "Deciding whether a new document kind gets tracking fields; reviewing corpora for misplaced or missing stamps."
    avoid_when: "Source repositories themselves — their files' truth IS git; stamps there are noise."
    expected: "Exactly the external documents carry tracking; versioned files stay stamp-free."
---

# Reference: tracking — Git Document Tracking (frontmatter-protocol extension)

Extension of `frontmatter-protocol` (core §9): activated implicitly by any of the keys `repo`, `branch`, `commit`, `committed_at`, `stale_since` in a frontmatter.
It binds a document to the git revision its content was verified against, and defines how drift is detected, annotated, and reconciled.

## Tracking Fields

[ref: #tracking-fields]

| Key | Required | Content |
|---|---|---|
| `repo` | yes | Repository identifier per `entity-protocol` `[ref: #entity-repo-field]`: an entity/location name with its own git, or `generic`. |
| `branch` | yes | Current branch of the resolved repository at last refresh. |
| `commit` | yes | 7-char short hash of the last **verified** revision — the watermark. Moves only on verification, never on edits. |
| `committed_at` | yes | UTC ISO 8601 timestamp (`Z` suffix) of the commit referenced by `commit`. |
| `stale_since` | only when stale | 7-char hash of the **first invalidating commit**, or `unknown` when it cannot be determined. Presence means: content is presumed stale. |

A document carrying any of these keys MUST carry the full required set (`--expect-extension tracking`).

The canonical assembled header of a tracked document (the `title`/H1 pairing is owned by `markdown-protocol` §6; `source` names the file the document describes; timestamps per `[ref: #tracking-timestamps]`):

```yaml
---
title: <String; must match the H1 title below>
created_at: <UTC ISO 8601>
updated_at: <UTC ISO 8601; refresh on every edit>
repo: <String; "generic" or <repo-name>>
branch: <String; current git branch>
commit: <String; 7-char short hash>
committed_at: <UTC ISO 8601; timestamp of the commit referenced by `commit`>
source: <String; project-relative path with optional line range>
---

# <Title>
```

## Repo Resolution

Owned by `entity-protocol` `[ref: #entity-repo-field]` — the legal `repo` values (`<repo-name>` / `generic`, lazy legacy normalization on mutation, never by backfill) and the git-anchor chain (entity git → containing project git → project root git, always preferred → `.serena` meta-git fallback → HARD STOP) live there. This extension only CONSUMES the resolved location: every command and check below runs inside the repository that recipe resolves.

## Git Metadata Commands

[ref: #tracking-git-commands]

Fill the fields with exactly this triplet, run inside the resolved repository:

```bash
git rev-parse --abbrev-ref HEAD           # branch
git rev-parse --short HEAD                # commit (7 chars)
git log -1 --format=%cd --date=iso-strict # committed_at; normalize to UTC with a `Z` suffix
```

- The commit hash is always the **short** form (7 chars) — never the full hash.
- `committed_at` MUST end in `Z` (convert timezones; e.g. `2026-06-17T08:39:38Z`).
- Broken ref states exist in the wild (observed HEAD/reflog mismatches): when results look impossible, verify ref consistency before stamping.

## Validation Timing

[ref: #tracking-validation-timing]

Validation (re-running the triplet and comparing against recorded fields) happens at exactly two moments:

1. **On decision impact** — before tracked content is about to influence a decision, a plan, or any work product.
2. **On write** — at every creation or mutation of the document.

Passive browsing (reading without using) does NOT trigger validation; the git tax is paid only where staleness could cause harm.

## Staleness Protocol

[ref: #tracking-staleness]

1. Compare recorded `commit` with the resolved repository's current HEAD.
2. On drift, find the **first invalidating commit**:
   - the document has a `source` field: `git log --reverse --format=%h <commit>..HEAD -- <source-path>` (first hit);
   - no `source`: `git log --reverse --format=%h <commit>..HEAD | head -1` (first commit after the watermark — precision honestly degrades without `source`);
   - repository unavailable/unresolvable: use `unknown`.
3. Annotate the frontmatter: `stale_since: <hash|unknown>`. This annotation MUST NOT bump `commit`/`committed_at` — the watermark is the last *verified* state and survives until reconciliation.
4. Treat the content as **presumed stale**: readable, but unusable for decisions until reconciled; disclose the marker when quoting the document.

Field-update matrix:

| Event | `commit` / `committed_at` | `branch` | `stale_since` |
|---|---|---|---|
| Verified content write/edit | bump to HEAD | refresh | clear if present |
| Staleness annotation | **unchanged** | refresh | set |
| Reconciliation, clean diff | bump to HEAD | refresh | clear (silently) |
| Reconciliation, content updated | bump to HEAD | refresh | clear (after user confirms) |
| Repository unavailable | unchanged | unchanged | `unknown` |

## Reconciliation Ladder

[ref: #tracking-reconciliation]

When presumed-stale content is needed:

**Design lineage.** This ladder is the "last verified commit" watermark pattern with stale-while-revalidate semantics: content stays readable while flagged presumed-stale, and revalidation happens through this ladder rather than blocking access. Churn-based freshness scoring and PR-level doc linting were evaluated and intentionally not adopted — the watermark plus explicit `stale_since` gives a byte-exact, zero-noise signal.

1. Diff the watermark against HEAD: `git log --oneline <commit>..HEAD` and `git diff --stat <commit>..HEAD -- <source>` (when `source` exists).
2. **Truly clean diff** (cosmetics only, nothing invalidating): clear `stale_since` and bump the watermark **silently** — but only when the diff is genuinely clean.
3. **Anything else**: show the user the diff summary and ASK — update the content or confirm it still holds; then clear the marker and bump.
4. **Repository unavailable**: set `stale_since: unknown` and warn the user; do not guess.

## Refresh on Mutation

[ref: #tracking-refresh]

Every mutation of a tracked document MUST refresh the tracking fields to the current repository state, with one exception carved out by the staleness protocol: `commit`/`committed_at` move only on verification, never on edits or annotations.

Domain-level timestamp obligations inherit from this rule: e.g. serena-protocol's `updated_at` refresh on every memory mutation is the serena-face of this protocol obligation.

## Document Timestamps

[ref: #tracking-timestamps]

| Key | Required | Content |
|---|---|---|
| `created_at` | yes | UTC ISO 8601 (`Z` suffix) of the document's creation. Immutable — set once at the first write, never touched again. |
| `updated_at` | yes | UTC ISO 8601 (`Z` suffix) of the most recent content mutation. Refreshed on EVERY write/edit of the document. |

Refresh-on-mutation applies here in full (`[ref: #tracking-refresh]`): an edit that changes content without bumping `updated_at` is non-conformant. These stamps are document history, not domain data — event times, deadlines, and schedules belong to optional tags (e.g. `due_date`), never to `created_at`/`updated_at`.

## Field Semantics and Optional Tags

[ref: #tracking-field-semantics]

Every field of the tracked-document header carries exactly one canonical meaning, traced to its owning extension:

| Field | Meaning | Source |
|-------|---------|--------|
| `title` | Exact duplicate of the H1 title below the frontmatter. | The `# <Title>` line; pairing owned by `markdown-protocol` §6. |
| `created_at` | Creation timestamp (immutable). | `[ref: #tracking-timestamps]`. |
| `updated_at` | Last-mutation timestamp, refreshed on every edit. | `[ref: #tracking-timestamps]`. |
| `repo` | Domain entity the document is about: `<repo-name>` or `generic`. | Semantics owned by `entity-protocol` `[ref: #entity-repo-field]`. |
| `branch` | Current git branch of the resolved repository. | `[ref: #tracking-git-commands]`. |
| `commit` | Short hash (7 chars) of the last verified revision. | `[ref: #tracking-git-commands]`. |
| `committed_at` | Timestamp of the commit referenced by `commit`, UTC ISO 8601 with `Z`. | `[ref: #tracking-git-commands]`. |
| `source` | Project-relative path to the relevant file or entity directory, with optional line range (`path:lineno..lineno`). | The file/directory the document describes (domain-defined). |

**Optional tags.** Agents MAY add additional YAML fields (tags) to the frontmatter when they provide useful metadata for filtering, routing, or context. Optional tags MUST:

- Be valid YAML scalar or list values.
- Not duplicate or contradict the mandatory fields.
- Be relevant to the memory type and content.

Common optional tags:

| Tag | Useful for | Example |
|-----|------------|---------|
| `status` | Bugs, proposals, plans, TODOs | `status: diagnosed, fix pending` |
| `severity` | Findings, bugs | `severity: critical` |
| `priority` | TODOs, plans, proposals | `priority: high` |
| `owner` | Reports, proposals, decisions | `owner: platform-team` |
| `due_date` | TODOs, plans | `due_date: 2026-07-10T00:00:00Z` |

Agents add tags based on the document's nature and project conventions, never inventing tags without purpose.

## Scope

[ref: #tracking-scope]

- **Applies to:** documents living OUTSIDE the versioned source of truth — Serena memories, user-owned markdowns, generated manifests stored as documents.
- **Does NOT apply to:** skill files, `references/`, source code, or any file whose truth is its own git history. Stamping those duplicates git and creates two competing truths.
