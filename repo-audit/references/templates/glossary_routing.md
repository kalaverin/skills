---
subject: "Glossary and memory routing; `repos/<repo>/` namespace, business memories, synthesis from five reports, risk register routing, project glossary, repo glossary, living contract, add refine remove markers, naming rules, metadata headers, `project/glossary`, mutation protocol."
index:
  - anchor: ra-tpl-glossary
    what: "The glossary and routing contract for repo-audit: namespaces, synthesis, risk routing, two-tier glossaries, naming, metadata."
    problem: "Glossary and routing rules scatter across template files; agents guess where terms and risks belong; term misplacement, risk fog, routing confusion, contract absence, placement doubt, knowledge scatter, ownership fog, guesswork spiral."
    use_when: "Working with glossaries or business-memory routing in any run; reviewing placement decisions."
    avoid_when: "Card and report templates — sibling template files; the global namespace registry — `[ref: #entity-namespace-registry]`."
    expected: "Every term and risk lands at its canonical place."
  - anchor: ra-tpl-glossary-namespace
    what: "The `repos/<repo>/` namespace contract: business memory types and non-domain findings routing."
    problem: "Business artifacts land in findings scopes and findings land in business memories; scope mixing, misplaced artifacts, routing errors, namespace confusion, boundary blur, destination chaos, category errors, domain fog, scope bleed, scope drift, placement chaos."
    use_when: "Placing any business memory; routing non-domain findings; checking the prerequisite."
    avoid_when: "The full scope registry — `entity-protocol` `[ref: #entity-namespace-registry]` owns it."
    expected: "Business content in `repos/`, findings in findings scopes, always."
  - anchor: ra-tpl-glossary-synthesis
    what: "The glossary synthesis duties: contradiction resolution, unified delta, shape decision, curated-only writes."
    problem: "Root pastes raw subagent output into glossaries; deltas fragment and contradictions import; paste temptation, delta chaos, synthesis skip, curated loss, error smuggling, assembly shortcuts, quality decay, dump noise, freshness neglect."
    use_when: "Building the glossary delta from the five reports; deciding single vs split; refreshing headers."
    avoid_when: "Synthesis rules for cards — `references/shared/synthesis.md` owns those."
    expected: "Unified curated glossary delta, zero raw dumps."
  - anchor: ra-tpl-glossary-risk-routing
    what: "The risk routing: summary in business.md, detailed register in risks/, bug-severe findings to bugs/."
    problem: "Risks duplicate fully in both places or severe bugs hide inside risk lists; duplication, concealed bugs, routing confusion, summary bloat, register absence, double recording, placement fog, severity blur, tracker confusion, split brain."
    use_when: "Placing any risk finding; deciding bug vs risk; sizing the summary."
    avoid_when: "Severity definitions — `generators/domain.md` owns those."
    expected: "Summary stays brief, register stays detailed, bugs route to bugs/."
  - anchor: ra-tpl-glossary-project
    what: "The project glossary: project-wide terms, read-before-analysis duty, creation with `repo: generic`."
    problem: "Analysis starts without project terminology; terms get redefined per repo and cross-repo meaning splits; terminology absence, redefinition, seed neglect, project confusion, vocabulary forks, shared-language decay, context drift, team misalignment, definition roulette."
    use_when: "Before any analysis; creating `project/glossary`; stamping its header."
    avoid_when: "Repo-local terms — those belong to the repo glossary below."
    expected: "Project glossary exists, read, and correctly stamped."
  - anchor: ra-tpl-glossary-repo
    what: "The repo glossary: repo-local terms with the living-contract duties (add, refine, remove)."
    problem: "Repo terms fossilize over releases; obsolete definitions linger and mislead every future run; misleading language, contract decay, stale vocabulary, definition rot, term senility, lexicon drift, reader deception, upkeep failure, maintenance debt."
    use_when: "Maintaining `repos/<repo>/glossary`; marking term changes; removing obsolete terms."
    avoid_when: "Project-spanning terms — project glossary above."
    expected: "Repo glossary stays alive: added, refined, removed as code evolves."
  - anchor: ra-tpl-glossary-naming
    what: "The glossary naming rules: snake_case, dash conversion, one-topic focus, immediate rename."
    problem: "Glossary paths violate naming grammar; links and routing break without anyone noticing; naming breach, path drift, rename postponement, silent linkrot, address decay, routing cracks, compliance lapse, hygiene debt, format sin."
    use_when: "Creating or renaming glossary memories; fixing non-compliant paths."
    avoid_when: "The naming grammar itself — `serena-protocol` `[ref: #serena-naming]` owns it."
    expected: "Every glossary path compliant."
  - anchor: ra-tpl-glossary-metadata
    what: "The glossary metadata headers: tracking fields per tier (repo git for repo glossary, project root for project glossary)."
    problem: "Glossary headers stamped from wrong git; freshness checks fire on wrong axis; axis confusion, false freshness, stamp error, tier mixing, anchor fog, verification noise, trust decay, source muddle, hierarchy mixup, git confusion."
    use_when: "Stamping any glossary header; choosing the git source per tier."
    avoid_when: "Field semantics — `[ref: #tracking-fields]` owns them."
    expected: "Each glossary tier stamped from its correct git."
---

# Memory Routing, Glossary Rules, and Metadata (repo-audit)

[ref: #ra-tpl-glossary]

## Dedicated business-domain namespace

[ref: #ra-tpl-glossary-namespace]

This skill introduces and owns the `repos/<repo>/<topic>` namespace.
`repos/` memories are repo-scoped, so the repo card prerequisite from
`entity-protocol` (`[ref: #entity-prerequisite]`) applies.

| Memory | Purpose |
|---|---|
| `repos/<repo>/business.md` | Executive summary and full report (or split point) |
| `repos/<repo>/entities/<business_entity>.md` | Detailed entity/value object/aggregate description |
| `repos/<repo>/processes/<process_name>.md` | Business process flow and state transitions |
| `repos/<repo>/rules/<topic>.md` | Business rules and invariants |
| `repos/<repo>/integrations/<topic>.md` | External actors and systems |
| `repos/<repo>/risks/<topic>.md` | Domain risks, gaps, contradictions |
| `repos/<repo>/glossary` | Repo-specific business terms |

Findings that are not domain-specific (e.g., implementation quirks, naming
inconsistencies, missing docs) should be routed to the canonical namespaces:

- `notes/<repo>/<topic>` — observations and ambiguities.
- `decisions/<repo>/<topic>` — business-driven architectural choices.
- `bugs/<repo>/<topic>` — confirmed incorrect business behavior.

## Synthesis from subagent reports

[ref: #ra-tpl-glossary-synthesis]

The root agent receives five specialized subagent reports (entities, processes,
rules, integrations, risks). It MUST:

1. Resolve contradictions using `[ref: #serena-contradictions]`.
2. Build a unified glossary delta.
3. Decide single vs split report.
4. Write final memories with refreshed YAML frontmatter.

Do not route raw subagent output directly to memory. Synthesize and edit for
consistency.

## Risk register routing

[ref: #ra-tpl-glossary-risk-routing]

- Keep a **summary** of risks (3–8 bullets with severity and anchor) inside
  `repos/<repo>/business.md`.
- Keep the **detailed risk register** in `repos/<repo>/risks/<topic>.md`.
- If a finding is severe enough to be tracked as a bug, route it to
  `bugs/<repo>/<topic>` instead of `repos/<repo>/risks/`.

## Project glossary

[ref: #ra-tpl-glossary-project]

The glossary is project-wide knowledge and lives at `project/glossary`.

### Reading the glossary

Before every analysis, read `project/glossary`. If it does not exist, create it.

### Creating the glossary

Use `write_memory` with a project-wide metadata header. Git source is
`.serena`; collect the tracking fields per the frontmatter-protocol tracking
extension (`[ref: #tracking-fields]`, `[ref: #tracking-git-commands]`).

Initial content:

```markdown
---
title: Project glossary
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
repo: generic
branch: <branch>
commit: <7-char-short-hash>
committed_at: YYYY-MM-DDTHH:MM:SSZ
source: .serena
---

# Project glossary

## Terms

| Term | Definition | Scope | Related entities | Source |
|---|---|---|---|---|
```

### Updating the glossary

The glossary is a living contract: actively ADD new terms, REMOVE obsolete ones (no longer backed by code evidence), and REFINE definitions as the code evolves — a stale term is worse than a missing one. Ubiquitous-language discipline: meanings are bounded by context — the repo glossary owns repo-local meanings, the project glossary only terms that genuinely span repos; code mirrors the language (class/method names should match glossary terms).

Mutate the glossary per `serena-protocol` `[ref: #serena-memory-mutation]` (append via `edit_memory`; verify and persist as prescribed there).

For each new or refined term, add a row:

```markdown
| Order | A customer's request to purchase goods | order_service | `orders/model.py:23` |
```

When refining an existing term, use `edit_memory` to update only that row.

Mark changes in the report:

- `added` — new term.
- `refined` — definition improved.
- `moved` — term relocated between `project/glossary` and
  `repos/<repo>/glossary`.
- `removed` — term deleted as obsolete (no code evidence).

## Repo glossary

[ref: #ra-tpl-glossary-repo]

Repo-specific terms live at `repos/<repo>/glossary`. This is a
repo-scoped memory, so the repo card prerequisite applies
(`[ref: #entity-prerequisite]`).

### Creating the repo glossary

Use `write_memory` with a repo-scoped metadata header. Git source is the
repo's own repository; collect the tracking fields per the
frontmatter-protocol tracking extension (`[ref: #tracking-fields]`, `[ref: #tracking-git-commands]`).

Initial content:

```markdown
---
title: <Repo> glossary
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
repo: <repo-name>
branch: <branch>
commit: <7-char-short-hash>
committed_at: YYYY-MM-DDTHH:MM:SSZ
source: <repo-path>
---

# <Repo> glossary

## Terms

| Term | Definition | Related entities | Source |
|---|---|---|---|
```

### Updating the repo glossary

Mutate per `serena-protocol` `[ref: #serena-memory-mutation]` (append via `edit_memory`; verify and persist as prescribed there). The same add/remove-obsolete/refine duty as for the project glossary applies here.

When a term should move between `project/glossary` and
`repos/<repo>/glossary`, remove it from the old location and add it to the
new one, noting the move in the report.

## Naming rules

[ref: #ra-tpl-glossary-naming]

- Memory names use `snake_case` with underscores. No hyphens.
- Directory dashes in repo names become underscores (`my-service` →
  `my_service`).
- One memory = one focused topic.
- If an existing path violates the naming convention, rename it immediately
  per `[ref: #serena-naming]` before editing.

## Metadata headers

[ref: #ra-tpl-glossary-metadata]

### For `repos/<repo>/...` memories

Git source: the repo's own repository; collect the tracking fields per the
frontmatter-protocol tracking extension (`[ref: #tracking-fields]`, `[ref: #tracking-git-commands]`).

Use the current YAML frontmatter standard from `[ref: #serena-metadata]`:

```yaml
---
title: <Title matching H1>
created_at: <UTC ISO 8601>
updated_at: <UTC ISO 8601; refresh on every edit>
repo: <repo-name>
branch: <branch>
commit: <7-char-short-hash>
committed_at: <UTC ISO 8601>
source: <project-relative path with optional line range>
---

# <Title>
```

### For `project/glossary`

Git source: the project root git (or the `.serena` meta-repository when no project git exists). `repo: generic`.
