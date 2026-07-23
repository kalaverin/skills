# Shared Conventions (repo-audit)

[ref: #ra-conventions]

Conventions shared by every repo-audit artifact, subagent, and synthesis step.

## Mermaid diagram rules

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

Never include in any repo-audit artifact (unless they directly encode a business rule or are actual runtime dependencies, e.g. a GitOps repo deploying Helm charts):

- AGENTS.md content, `.serena/` internals, and agent infrastructure/configuration.
- Tests, linters, CI/CD, Makefile, Docker, pre-commit, editor config ("development meta").
- Sentry, Prometheus, logging, metrics, observability-only infrastructure.
- Entry points (how to run).
- Environment variable VALUES, defaults, examples, or secrets (names and prefixes only).
- Upstream consumers of the repo — FORBIDDEN in `repos/<repo>/overview` (the card describes the repo itself), but MANDATORY in `repos/<repo>/dependencies` (consumers are the subject of that card).

## Evidence citation

Every claim cites: `path/to/file.py:42` (symbol `OrderService.submit`). Subagents NEVER run git; the ROOT agent stamps the commit hash when persisting findings, per `entity-protocol` `[ref: #entity-findings-traceability]`. Relative paths from the repo root. Primary source + up to two secondary sources. Multi-source inferences are declared explicitly.

## Dates and language

- All dates and times: UTC ISO 8601 `YYYY-MM-DDTHH:MM:SSZ`. No exceptions.
- All artifacts and memory content: technical English only.
- User-facing chat: the user's language.
