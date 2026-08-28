---
subject: "Shared conventions; Mermaid diagram rules, mandatory cases, exclusion list, observability dev-meta, evidence citation, root-stamped hashes, UTC ISO 8601 dates, technical English, consumer placement, uniform style, validation, source limits, runtime dependencies, artifact hygiene."
index:
  - anchor: ra-conventions
    what: "The cross-cutting conventions for repo-audit artifacts: mermaid, exclusions, evidence, dates."
    problem: "Artifacts diverge in diagram style, exclusion scope, evidence shape, and date formats across teams; format chaos, convention absence, uniform decay, review friction, template guessing, cross-file inconsistency, style entropy, onboarding confusion, style roulette."
    use_when: "Writing or reviewing any artifact; settling format questions; onboarding new artifact types."
    avoid_when: "Per-template content rules — those live in `references/templates/`."
    expected: "Uniform diagrams, filtering, citations, and timestamps across artifacts."
  - anchor: ra-conventions-mermaid
    what: "The Mermaid diagram rules: when diagrams are mandatory, syntax, and validation."
    problem: "Complex flows and state machines receive prose-only descriptions nobody can follow, or diagrams whose syntax fails to render; missing visuals, prose walls, display collapse, flow blindness, reader fatigue, syntax errors, documentation decay."
    use_when: "Documenting any non-trivial flow or state machine; validating diagram syntax; reviewing artifacts."
    avoid_when: "Trivial linear steps — prose suffices; diagram content — the owning template."
    expected: "Every non-trivial flow has a valid Mermaid diagram."
  - anchor: ra-conventions-exclusions
    what: "The exclusion list: what never enters artifacts (observability, dev-meta, entry points, env values, consumer placement)."
    problem: "Artifacts bloat with monitoring config and framework boilerplate until architectural signal drowns completely; noise invasion, dev-meta creep, observability clutter, signal burial, review fatigue, relevance decay, clutter accumulation, scope erosion, reader abandonment."
    use_when: "Drafting or reviewing any artifact section; borderline inclusion judgment; consumer placement (overview vs dependencies)."
    avoid_when: "Runtime dependencies — included by definition; per-card exclusions — `[ref: #entity-card-exclusions]` for the overview card."
    expected: "Artifacts contain only architectural signal."
  - anchor: ra-conventions-evidence
    what: "The evidence citation convention: `path:line` + symbol, root-stamped hashes, source limits."
    problem: "Artifact claims arrive without anchors; reviewers verify nothing and confidence erodes silently; unverifiable statements, anchor absence, trust erosion, source sprawl, citation drift, credibility decay, audit friction, proof gap, verification failure."
    use_when: "Writing claims into artifacts; reviewing citation quality; stamping hashes at persistence."
    avoid_when: "Subagent-side evidence rules — `[ref: #ra-subagent-evidence]` owns those."
    expected: "Every claim anchored with controlled source counts."
  - anchor: ra-conventions-dates-language
    what: "The date and language convention: UTC ISO 8601 `Z` everywhere, technical English only."
    problem: "Artifacts mix timezones and natural languages across files; comparisons break and readers stumble over formats; timezone drift, locale chaos, comparison failure, language mixing, format inconsistency, reader friction, uniform decay, parsing pain."
    use_when: "Writing any date or prose into artifacts; reviewing format compliance."
    avoid_when: "User-facing chat — that follows the user's language, per project preferences."
    expected: "All dates UTC `Z`, all content technical English."
---

# Shared Conventions (repo-audit)

[ref: #ra-conventions]

Conventions shared by every repo-audit artifact, subagent, and synthesis step.

## Mermaid diagram rules

[ref: #ra-conventions-mermaid]

Mermaid is a first-class output format.

Add a diagram for:

- Any entity lifecycle or state machine with ≥ 2 states and non-trivial transitions.
- Any Temporal workflow or long-running process.
- Any process with branching, loops, timeouts, retries, or side effects.
- Any multi-actor interaction where sequence matters.

Use Mermaid whenever a diagram makes the domain easier to read — the mandatory cases are a floor, not a ceiling.

Preferred diagram types:

- **State machines:** `stateDiagram-v2`.
- **Workflows and business flows:** `flowchart TD` or `flowchart LR`.
- **Multi-actor interactions:** `sequenceDiagram`.
- **Dependency diagrams:** `graph LR` / `graph TB` / `flowchart`.

Quality rules:

- Name nodes with business terms, not raw function names.
- Label edges with the event/command (business flows) or the protocol/purpose (dependency diagrams).
- Include error/timeout branches, not just the happy path.
- Dependency diagrams: one node per repo/system; subgraphs only when they improve readability; never omit nodes for size — use a high-level diagram plus a note instead.
- Validate syntax before writing.

## Exclusion list

[ref: #ra-conventions-exclusions]

Never include in any repo-audit artifact (unless they directly encode a business rule or are actual runtime dependencies, e.g. a GitOps repo deploying Helm charts):

- AGENTS.md content, `.serena/` internals, and agent infrastructure/configuration.
- Tests, linters, CI/CD, Makefile, Docker, pre-commit, editor config ("development meta").
- Sentry, Prometheus, logging, metrics, observability-only infrastructure.
- Entry points (how to run).
- Environment variable VALUES, defaults, examples, or secrets (names and prefixes only).
- Upstream consumers of the repo — FORBIDDEN in `repos/<repo>/overview` (the card describes the repo itself), but MANDATORY in `repos/<repo>/dependencies` (consumers are the subject of that card).

## Evidence citation

[ref: #ra-conventions-evidence]

Every claim cites: `path/to/file.py:42` (symbol `OrderService.submit`). Subagents NEVER run git; the ROOT agent stamps the commit hash when persisting findings, per `entity-protocol` `[ref: #entity-findings-traceability]`. Relative paths from the repo root. Primary source + up to two secondary sources. Multi-source inferences are declared explicitly.

## Dates and language

[ref: #ra-conventions-dates-language]

- All dates and times: UTC ISO 8601 `YYYY-MM-DDTHH:MM:SSZ`. No exceptions.
- All artifacts and memory content: technical English only.
- User-facing chat: the user's language.
