---
subject: "Repo card production rules; root subagent workflow, responsibility segregation, tree fallback, quality checklist, content exclusions, hard fails, mistake avoidance, frontmatter header example, `repos/<repo>/overview`, explore timeout, follow-up loop, contradictions, persistence, canonical names."
index:
  - anchor: entity-card-workflow
    what: "The ten-step root-agent orchestration for producing or updating `repos/<repo>/overview` plus the HARD root-vs-subagent responsibility split, tool-degradation and tree-fallback rules."
    problem: "Card production without strict split lets subagents write memory, invent trees, or run git while root skips validation; hallucinated cards, restricted-shell failures, evidence forgery, unverified reports, delegation chaos, missing follow-ups, rework."
    use_when: "Producing or updating any repo card; launching exploration subagent for card data; validating subagent report before persist; handling blocked shell or missing `tree`."
    avoid_when: "Business or dependency artifacts — `repo-audit` pipeline owns those; per-type extraction rules — `[ref: #repo-interface-exhaustiveness]`."
    expected: "Complete validated card written by root with every duty executed at its designated layer."
  - anchor: entity-card-quality
    what: "The five-criterion pre-save gate: completeness, precision, consistency, compressibility, traceability."
    problem: "Cards saved with guessed versions, fluffy prose, contradictions against existing memory silently poison every downstream artifact; quality drift, version rounding, narrative essays, stale facts, unchecked saves, precision loss, inconsistency, bloat, rework."
    use_when: "Final check before writing any card; reviewing existing card for compliance; deciding whether section needs follow-up questions."
    avoid_when: "Workflow sequencing questions — `[ref: #entity-card-workflow]`; content allow-lists — `[ref: #entity-card-exclusions]`."
    expected: "Every saved card passes all five criteria with verbatim versions and zero fluff."
  - anchor: entity-card-exclusions
    what: "The closed list of content that never goes into a repo card: agent infrastructure, observability-only deps, development meta, entry points, env values, upstream consumers, anomalies."
    problem: "Cards bloat with Sentry, pytest configs, run instructions, and secrets until signal drowns and security review flags leaks; content bloat, credential leakage, dev-meta noise, scope creep, consumer confusion, observability clutter."
    use_when: "Drafting or reviewing any card section; deciding whether borderline item belongs; routing rejected content elsewhere."
    avoid_when: "Positive content requirements — templates in `repo-audit`; dependency-card consumers section — that artifact requires upstream consumers."
    expected: "Cards contain only technical overview; every rejected category routed to its proper home."
  - anchor: entity-card-hard-fails
    what: "The eight protocol-breaking conditions plus the mistake-avoidance rules for card production."
    problem: "Single careless move — hand-written tree, guessed name, `.serena` git metadata, rounded version — invalidates whole card run; protocol violations, voided runs, silent failure modes, repeated mistakes, rework loops, gate bypass, provenance forgery."
    use_when: "Self-checking during card production; reviewing why card run failed; teaching failure boundaries to subagents."
    avoid_when: "General skill prohibitions — SKILL.md Do Not section; quality polish — `[ref: #entity-card-quality]`."
    expected: "Zero hard-fail conditions triggered across the run; known mistakes caught by the avoidance rules."
  - anchor: entity-card-header-example
    what: "The concrete YAML frontmatter template for `repos/<repo>/overview` cards with all tracking fields."
    problem: "Card headers diverge in field sets and formats; readers and freshness checks cannot parse them uniformly; header drift, missing fields, malformed yaml, validation failures, metadata inconsistency, template mismatch, tracking gaps, uniformity loss."
    use_when: "Writing card frontmatter; refreshing stale card header; verifying field set completeness."
    avoid_when: "Field semantics — `[ref: #tracking-fields]` and `[ref: #entity-repo-field]` own meanings; non-card memories — standard memory header applies."
    expected: "Card headers match template exactly with valid tracking values."
---

# Card Production (entity-protocol reference)

Rules for producing and updating repo cards (`repos/<repo>/overview`). Loaded lazily via the routing index in `entity-protocol/SKILL.md`.

## Root/Subagent Workflow

[ref: #entity-card-workflow]

The root agent orchestrates; a read-only subagent explores.

**Root-agent procedure:**

1. Load templates and existing memory.
2. Apply the deprecations read-side duty (`[ref: #entity-deprecations]`) BEFORE writing anything; apply canonical names throughout, and append newly discovered deprecations/aliases to the appropriate level after the run.
3. Apply `[ref: #entity-prerequisite]`: confirm the target repo has a card at `repos/<repo>/overview`; if not, STOP and ask the user.
4. Determine the repo type per `[ref: #repo-type-detection]` (`repo-audit`).
5. Launch a read-only `explore` subagent (timeout 3595 seconds).
6. Generate the `## Directory structure` section locally — never delegated (see Tree generation below).
7. Validate the report against the exhaustiveness matrix (`[ref: #repo-interface-exhaustiveness]`): if any section is missing, thin, or contradicts the template, ask the subagent FOLLOW-UP questions (resume the same subagent instance) and repeat until the report is complete; if the follow-up loop stalls (no progress after two rounds), escalate to the user with the specific gaps.
8. Resolve contradictions, write the final card to `repos/<repo>/overview`.
9. Write findings to separate memories (routing per `[ref: #entity-namespace-registry]`, evidence per `[ref: #entity-findings-traceability]`).
10. Run the persistence command (`just serena-checkpoint`).

**Root vs subagent responsibilities (HARD):** to prevent hallucinations and restricted-shell failures, responsibilities are strictly segregated.

- **ROOT AGENT:** owns the prerequisite gate, type determination, tree generation, contradiction resolution, all memory writes, commit-hash stamping, and persistence.
- **EXPLORATION SUBAGENT (read-only):** timeout 3595 seconds. Has no MCP/Serena tools; browses memory via `tree --gitignore --prune <workspace-root>/.serena/memories` and reads listed files via `cat`; receives memory PATHS only, never pasted contents. Reads manifests/lockfiles, code, and proto files. Extracts exhaustive interfaces per `[ref: #repo-interface-exhaustiveness]`. Outputs a flat list of meaningful paths (never the directory tree) and findings with severity and `path:line` + symbol anchors; NEVER runs git — the ROOT agent stamps commit hashes when persisting findings; never writes to Serena, never runs mutating commands. If the Shell tool is blocked or absent, applies the degradation rules of `subagents-protocol` (§12 Subagent Tool Degradation): read-tool fallbacks, no retries, limitations stated in the report.

**Tree generation (root agent only):** per `subagents-protocol` §13 (directory trees belong to the root agent), the ROOT agent runs the canonical command from `shell-protocol` `[ref: #tree-agent-rules]` inside `<repo_path>`; the command is referenced from there, never restated, and never delegated to the subagent. Do NOT write the `tree` command itself into the card.

**Fallback when `tree` is unavailable or fails:** ask the exploration subagent for a flat list of meaningful paths (it can produce one without shell access, via its file-reading/listing tools), then the ROOT agent formats the tree-like structure manually from that list. This is the ONLY case where a hand-formatted tree is legal (see the carve-out in `[ref: #entity-card-hard-fails]`).

## Card Quality Checklist

[ref: #entity-card-quality]

Before saving a repo card, verify:

- **Completeness:** every required section present; exported interface exhaustive (every endpoint, gRPC method, workflow/activity, HelmRelease, public module).
- **Precision:** all versions come from lockfiles/manifests verbatim — no guessing, no normalization to `major.minor`; all standards/protocols cite authoritative sources (RFC or vendor spec).
- **Consistency:** metadata uses the repo's own git branch and latest commit; no contradictions with existing memory unless explicitly resolved and logged.
- **Compressibility:** no fluff; one-line comments for directory entries; no duplicated information; the card stays a technical overview — anomalies route to finding namespaces. Target shape: the arc42/C4 minimal per-service subset (C4 level-1 context, level-2 container/stack, key decisions as ADR-style findings, the primary runtime flow) — everything else routes out of the card.
- **Traceability:** every finding cites file path, line, and current commit hash (stamped by the ROOT agent at persistence).

## Card Content Exclusions

[ref: #entity-card-exclusions]

Never in a repo card: AGENTS.md content and Serena/agent infrastructure (`.serena/`, memory layouts, agent configuration); Sentry/Prometheus/observability-only dependencies; tests, linters, CI, Makefile, Docker, pre-commit, editor config ("development meta"); entry points (how to run); environment variable VALUES/defaults/examples/secrets (names and prefixes only); upstream consumers of the repo (they belong to the dependency card, not the overview card); anomalies/gotchas (those route to finding namespaces).

## Card Hard Fails

[ref: #entity-card-hard-fails]

If you do any of the following, you fail the protocol:

- **HARD FAIL:** Writing to a repo-scoped namespace when the target repo has no card at `repos/<repo>/overview` (the meta-entity `project` is exempt — see `[ref: #entity-namespace-registry]`).
- **HARD FAIL:** Implicitly creating a repo card outside the `repo-audit` skill.
- **HARD FAIL:** Guessing a repo name instead of asking the user.
- **HARD FAIL:** Hand-writing a directory tree instead of using the exact `tree` CLI command output — EXCEPT the documented fallback: `tree` is unavailable or failed AND the structure is formatted by the ROOT agent from the subagent's flat list of meaningful paths.
- **HARD FAIL:** Rounding or normalizing dependency versions (e.g., writing `FastAPI 0.10x` instead of reading the exact version from `uv.lock`).
- **HARD FAIL:** Using the `.serena` git repository to fill out the metadata header for a specific repo — always use the repo's own git.
- **HARD FAIL:** Including `Sentry`, `Prometheus`, `pytest`, `ruff`, or CI/CD pipelines in the `Technology stack` section of a repo card.
- **HARD FAIL:** Writing actual environment variable VALUES or SECRETS in memory. Write the PREFIX and description only.

**Mistake avoidance:** putting findings into the card is the most common residual mistake — route anomalies, TODOs, and style issues to the findings scopes per `[ref: #entity-namespace-registry]`; every other recurring mistake is already a HARD FAIL above.

## Card Header Example

[ref: #entity-card-header-example]

```yaml
---
title: example_api entity card
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
repo: example_api
branch: <branch>
commit: <7-char-short-hash>
committed_at: YYYY-MM-DDTHH:MM:SSZ
source: example_api
---

# example_api entity card

## Purpose
Example public-facing REST gateway for the platform...
```
