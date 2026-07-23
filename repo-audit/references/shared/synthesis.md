# Shared Synthesis Rules (repo-audit)

[ref: #ra-synthesis]

How the root agent combines subagent reports into final artifacts. Applies after every wave, in every run mode.

## 1. Contradiction resolution

Follow `serena-protocol` `[ref: #serena-contradictions]`. The hierarchy:

1. Compare recorded dates and commit hashes of the conflicting memories.
2. A newer memory explicitly overriding an older one wins.
3. `AGENTS.md` wins over session memory unless explicitly overridden.
4. The repo's own git metadata wins over `.serena` metadata for repo-specific facts.
5. An unresolved contradiction = STOP and report to the user; never proceed with an open conflict.

Log every contradiction (resolved and unresolved) in `agent/contradictions` with the conflicting memory names, dates/branches, and the resolution.

## 2. No raw dumps

Never route raw subagent output directly to memory. Synthesize, deduplicate, and edit the reports into the final artifact templates (`references/templates/`).

## 3. Single vs split business report

Decide the `business.md` shape:

- **Single file** if: ≤5 domain entities, ≤4 processes, ≤8 rules, AND the result fits under ~300 lines.
- **Split model** otherwise: executive summary at `repos/<repo>/business.md` plus focused files under `repos/<repo>/entities/`, `repos/<repo>/processes/`, `repos/<repo>/rules/`, `repos/<repo>/integrations/`, `repos/<repo>/risks/`. These are files, not directories; names MUST use snake_case.

## 4. Root-drawn dependency diagram

The root agent draws the dependency Mermaid diagram itself during synthesis of `repos/<repo>/dependencies` — from the three dependency extractor reports (interface, downstream, infra) PLUS the existing `repos/<repo>/dependencies` card if present. There is no diagram subagent. The diagram is ALL-ENCOMPASSING: every upstream consumer and every downstream target from the card's tables MUST appear as a node — omitting a node is a defect; if the diagram grows unwieldy, keep all nodes and improve layout (subgraphs, grouping) instead of dropping anything. Diagram rules: `[ref: #ra-conventions]`; validation checklist: `references/checklists.md`.

## 5. Verify and persist

Verify and persist per `serena-protocol` `[ref: #serena-memory-mutation]` (read-back + persistence command from the workspace root; the YAML frontmatter is refreshed on every mutation).

## 6. User summary format

Report to the user (in the user's language):

- Repo name and detected type.
- Mode run (FULL / PARTIAL / REFRESH) and artifact counts (sections, findings by severity and category).
- Subagent counts per wave and any follow-up questions asked.
- Resolved and unresolved contradictions.
- Created vs updated artifacts (paths).
