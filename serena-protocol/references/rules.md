---
subject: "Serena memory protocol rules; `.serena/memories` location, AGENTS.md relationship, snake_case naming, rename normalization, YAML frontmatter metadata contract, proactive lifecycle, when-to-record, contradiction resolution, override hierarchy, worked findings examples, symbolic MCP tools, diagnostics."
index:
  - anchor: serena-what-is
    what: "The orientation table defining what Serena memory is: on-disk location, relationship to `AGENTS.md`, authoritative index, workspace-wide scope, content language."
    problem: "Agent starts memory work without knowing where store lives on disk or how it differs from AGENTS.md; wrong root assumed, wrong tongue used; store confusion, location mistakes, scope misunderstanding, speech drift, orientation failure."
    use_when: "First contact with Serena ecosystem in session; deciding where memories physically live; weighing AGENTS.md against memory as source of truth."
    avoid_when: "Concrete write/edit recipes — `#serena-memory-mutation`; scope routing — `[ref: #entity-namespace-registry]`."
    expected: "Agent orients correctly: right directory, right language, right truth source."
  - anchor: serena-naming
    what: "The `snake_case` grammar for memory names plus the hard rename rule and five-step normalization recipe with worked examples."
    problem: "Memory paths arrive with hyphens, spaces, leading underscores; left unfixed they break routing and linking across workspace; invalid characters, non-compliant paths, broken links, rename hesitation, batch postponement, character drift, regex mismatch."
    use_when: "Creating any memory file or directory; encountering non-compliant existing path; normalizing entity directory names into memory segments."
    avoid_when: "Choosing which scope receives content — `[ref: #entity-namespace-registry]`; header fields — `#serena-metadata`."
    expected: "Every memory path matches grammar; violations renamed immediately before edits."
  - anchor: serena-metadata
    what: "The metadata header contract: mandatory YAML frontmatter with immediate H1, refresh-on-mutation, and the ownership map to tracking extension and `repo` field rules."
    problem: "Memories written with plain-text metadata or stale headers become unparseable and falsify freshness checks; header drift, missing frontmatter, stale timestamps, contract violations, parse failures, refresh neglect, uniformity loss, downstream distrust, audit noise."
    use_when: "Writing or editing any memory; refreshing outdated headers; verifying field set after mutation."
    avoid_when: "Field-by-field semantics — `[ref: #tracking-field-semantics]`; `repo` value choice — `[ref: #entity-repo-field]`."
    expected: "Every memory carries valid refreshed frontmatter with matching H1."
  - anchor: serena-lifecycle
    what: "The proactive-population mandate and the cross-cutting when-to-record routing for `agent/` and `project/` scopes."
    problem: "Agent finishes sessions leaving discoveries unrecorded; knowledge evaporates between sessions and bugs get rediscovered; forgotten findings, silent sessions, knowledge loss, repeated mistakes, recording hesitation, evaporation, rediscovery cycles, memory amnesia, reminder dependence."
    use_when: "Ending any task or session; deciding whether discovery warrants memory; routing agent-behavior or project-wide knowledge."
    avoid_when: "Repo-scoped findings routing — `[ref: #entity-namespace-registry]`; mutation mechanics — `#serena-memory-mutation`."
    expected: "Every discovery recorded in correct scope without reminders."
  - anchor: serena-contradictions
    what: "The five-step resolution protocol for conflicting memories: date/hash comparison, explicit override, `AGENTS.md` hierarchy, stop-and-report, mandatory logging."
    problem: "Two memories state opposite facts; agent picks one arbitrarily or averages them, corrupting downstream decisions; conflicting facts, stale duplicates, arbitrary resolution, silent divergence, unresolved clashes, guesswork, trust erosion, flip-flopping, evidence neglect."
    use_when: "Fresh report contradicts stored memory; two memories disagree; reviewing flagged contradictions log entries."
    avoid_when: "Stale-vs-fresh commit checks — tracking extension `[ref: #tracking-staleness]`; naming conflicts — `#serena-naming`."
    expected: "Every contradiction resolved by protocol or escalated; all logged."
  - anchor: serena-examples
    what: "Worked body examples for all nine findings domains from `bugs/` through `deprecations/`."
    problem: "Agent writes first finding of some domain and invents structure ad hoc; inconsistent formats across domains confuse later readers; format guessing, structure drift, missing severity, inconsistent evidence, template absence, ad-hoc bodies, format chaos."
    use_when: "Drafting memory in any findings domain; checking expected body shape; calibrating severity and evidence placement."
    avoid_when: "Header assembly — `[ref: #tracking-fields]`; scope selection — `[ref: #entity-namespace-registry]`."
    expected: "Findings follow uniform per-domain shapes with complete evidence."
  - anchor: serena-mcp-tools
    what: "The Serena MCP tool catalog: symbolic search, exploration, and editing tools with usage guidelines."
    problem: "Agent greps whole files or edits textually when symbolic tools would answer precisely; context floods, imprecise edits, broken symbols; raw reads, context bloat, blind edits, rename hazards, tool ignorance, textual hacks."
    use_when: "Exploring code structure; finding symbols or references; renaming or replacing symbol bodies; verifying edits via diagnostics."
    avoid_when: "Memory operations — `#serena-memory-mutation`; web search — kagi tools per kagi-search skill."
    expected: "Code operations use symbolic tools; textual fallback reserved for gaps."
---

# Universal Serena Memory Protocol

The canonical rule set for organizing, populating, and maintaining Serena memory. The mutation & persistence protocol lives in `serena-protocol/SKILL.md` §1 (`[ref: #serena-memory-mutation]`). Namespaces/scopes, the repo concept, and findings routing live in `entity-protocol`.

## What Serena Memory Is

[ref: #serena-what-is]

| Aspect | Rule |
|--------|------|
| **On-disk location** | `.serena/memories/` under the workspace root (`<workspace-root>/.serena/memories/`). |
| **Relationship to `AGENTS.md`** | `AGENTS.md` is the project-level source of truth for agent behavior. Serena memory stores operational facts (entity cards, bugs, decisions, notes, templates, prompts). |
| **Authoritative index** | `agent/rules` defines where to look first for authoritative knowledge. |
| **Scope** | Workspace-wide. The parent workspace owns `.serena/`; individual entity directories usually do not contain their own `.serena/`. |
| **Content language** | Technical English only. |

All namespaces/scopes and their routing rules: `entity-protocol` `[ref: #entity-namespace-registry]` — the single place defining all topics, repos, domains, and namespaces.

## Memory Naming Convention

[ref: #serena-naming]

- **Format:** `snake_case` with underscores (`_`) as word separators.
- **Allowed characters:** Latin letters (`a-zA-Z`), digits (`0-9`), and underscore (`_`) ONLY.
- **No hyphens, dashes, minus signs, spaces, or any other special characters** in memory names or directory names.
- **No leading, trailing, or consecutive underscores** (e.g. `_name`, `name_`, `name__part`).
- **Pattern:** `<domain>/<topic>` for cross-cutting scopes; `<domain>/<repo>/<topic>` for repo-scoped scopes. Topics may be nested (e.g. `guide/onboarding_glossary/chapter_01`).

### Hard rename rule

If an existing memory file or directory under `.serena/memories/` violates the character rules above, the agent MUST rename it to a compliant name immediately, before reading or editing its contents. Do not wait for a separate batch and do not leave non-compliant names in place.

**Normalization recipe:**

1. Replace hyphens, dashes, en-dashes, em-dashes, spaces, and any other separator with `_`.
2. Remove every character that is not a Latin letter, digit, or `_`.
3. Strip leading and trailing underscores.
4. Collapse any sequence of two or more underscores into a single `_`.
5. Ensure the result is non-empty and starts with a letter or digit.

**Examples:**

| Invalid original | Normalized |
|---|---|
| `payment-method-api` | `payment_method_api` |
| `risk-management-api` | `risk_management_api` |
| `classic-grpc` | `classic_grpc` |
| `_legacy_name_` | `legacy_name` |
| `double__underscore` | `double_underscore` |

Additional rules:

- One memory = one focused topic; keep files short and specialized.
- For entity-scoped memories, replace directory dashes with underscores: `my-service` → `my_service`.

## Metadata Header Rules

[ref: #serena-metadata]

Every memory entry MUST begin with a YAML frontmatter block enclosed in `---`, followed immediately by a Markdown H1 header (`# <Title>`). Do NOT put metadata as plain text below the header.

**The contract:**

- The header template and the required field set are owned by the tracking extension — `[ref: #tracking-fields]`.
- Per-field semantics and optional tags are owned by the tracking extension — `[ref: #tracking-field-semantics]`; `repo` value semantics (domain axis, legal values, git-anchor chain) are owned by `entity-protocol` `[ref: #entity-repo-field]`.
- On EVERY mutation the entire header is refreshed per the tracking extension (`[ref: #tracking-refresh]`, `[ref: #tracking-timestamps]`) — including the header refresh caused by the mutation itself.
- Optional tags MAY appear after the mandatory fields; they do not relax the refresh-on-mutation requirement.
- Git metadata commands, validation timing, and the staleness protocol (`stale_since`) are owned by the tracking extension (`frontmatter-protocol/references/tracking.md`) — apply it here in full.

## Memory Lifecycle / Workflow

[ref: #serena-lifecycle]

Agents MUST proactively populate Serena memory without being reminded — every session, every task, every discovery.

**Memory-operation triggers (HARD):** any instruction mentioning "memory", "память", "knowledge base", or "база знаний" for read/write/edit/list/delete/rename MUST trigger the Serena memory tools — never raw file operations. The ONLY raw-file exception: refreshing an outdated memory header in place at `.serena/memories/<path>.md`, preserving all content below the header (per `serena-protocol/SKILL.md` §4 Master Execution Workflow).

**Decision cards (MANDATORY after the user answers presented options):** record ONE self-contained memory in `decisions/<repo-or-project>/<topic>` containing, in order: (1) **Global context** — the overarching task/goal and why it matters; (2) **Local scope** — the specific sub-task(s) that led to the question(s); (3) **Questions & options** — each question posed, the options presented for it, and the user's chosen answer; (4) **Decision summary** — the consolidated decision(s) and the concrete consequences / next steps. A reader opening only this card MUST understand the full picture without consulting any other source.

**Before writing any repo-scoped memory:** apply `entity-protocol` `[ref: #entity-prerequisite]` (verification, STOP procedures, meta-entity exemption). Repo-scoped findings routing (which findings domain receives what): `entity-protocol` `[ref: #entity-namespace-registry]`.

**When to record (cross-cutting scopes):**

| Trigger | Target namespace |
|---------|------------------|
| Agent behavior bug or workaround | `agent/<topic>` |
| Project-wide knowledge or repo registry | `project/<topic>` |

**After any write/edit:** verify and persist per `[ref: #serena-memory-mutation]` (read-back + persistence command from the workspace root).

**When reading repo-specific memories:** apply the freshness rule of `entity-protocol` `[ref: #entity-freshness]`.

## Contradiction Resolution

[ref: #serena-contradictions]

Applies whenever stored knowledge conflicts — between memories, or between a fresh report (e.g. a card-creation subagent report) and existing memories.

1. **Compare dates/hashes:** check the headers of the conflicting memories.
2. **Explicit override:** if the newer memory explicitly states it overrides the older one, the newer wins.
3. **Hierarchy rule:** if one source is `AGENTS.md` and the other is a session memory, `AGENTS.md` WINS unless the session memory explicitly overrides `AGENTS.md` by name.
4. **Failure state:** if the contradiction is unresolved, STOP and report it to the user. Do NOT guess.
5. **Logging:** log EVERY detected contradiction (even if resolved) by appending to `agent/rules` under the `## Contradictions log` header via `edit_memory` (`[ref: #serena-memory-mutation]`).

## Examples of Memory Entries

[ref: #serena-examples]

One worked body example per findings domain. Headers are NOT restated: assemble them per `[ref: #tracking-fields]`, with `repo` per `[ref: #entity-repo-field]` and evidence (`path:line` + commit hash) per `[ref: #entity-findings-traceability]`. Scope semantics: `[ref: #entity-namespace-registry]`.

### `bugs/<repo>/<topic>`

```markdown
# Example validation error not translated (EXAMPLE-API-E1)

**Severity:** critical — `example-api/src/handlers/example.py:42` (commit abc1234)

## Problem
`POST /api/v1/example` triggers Sentry event `EXAMPLE-API-E1`: `ValidationError: Invalid input`.

## Root cause
The handler raises before the translation layer runs.
```

### `decisions/<repo>/<topic>`

```markdown
# Sessions intentionally stateless in example-api

Decided 2026-07-23 with the user. `example-api/src/auth/session.py:18` (commit abc1234)

## Decision
All session state lives in Redis; the service holds no in-process session cache.

## Rationale
Horizontal scaling behind the balancer requires any instance to serve any request.

## Consequences
Every request pays one Redis round-trip; local caching is forbidden.
```

### `notes/<repo>/<topic>`

```markdown
# Retry budget hardcoded at 3 in example-api client

`example-api/src/clients/downstream.py:77` (commit abc1234)

The downstream client hardcodes `MAX_RETRIES = 3` with no config override. Surprising during incident drills: longer outages cannot be tuned without a deploy.
```

### `style/<repo>/<topic>`

```markdown
# Repository pattern naming in example-api

`example-api/src/db/` (commit abc1234)

Repositories are named `<entity>_repo.py` and expose only async methods. Sync helpers are tech debt scheduled for removal; do not add new ones.
```

### `todo/<repo>/<topic>`

```markdown
# TODO: backfill idempotency keys on payment retries

Source: `example-api/src/handlers/payments.py:133` TODO comment (commit abc1234)

Priority: high. Retry path re-charges on timeout until the key backfill lands.
```

### `plans/<repo>/<topic>`

```markdown
# Plan: migrate example-api webhooks to outbox pattern

Status: in progress. Context: webhook delivery lost on deploy rollbacks.

- [x] 1. Add outbox table and writer
- [ ] 2. Dual-write from handlers
- [ ] 3. Relay worker with retries
- [ ] 4. Cut over and drop direct sends
```

### `proposals/<repo>/<topic>`

```markdown
# Proposal: replace hand-rolled retry with tenacity in example-api

Status: not yet accepted. `example-api/src/clients/downstream.py:70..90` (commit abc1234)

## Proposal
Adopt `tenacity` with jittered backoff; delete the custom loop.

## Trade-offs
+ Battle-tested, less code. − New dependency; behavior change in backoff curve.
```

### `reports/<repo>/<topic>`

```markdown
# Report: auth latency investigation in example-api

Date: 2026-07-23. Trigger: p99 auth latency alert.

## Findings
1. RSA verify dominates (62% of span). 2. Key fetched per request — no cache.

## Recommendation
Cache the JWKS for 5 minutes; expected p99 drop ~40%.
```

### `deprecations/<repo>/<topic>`

```markdown
# Deprecated: legacy_charge endpoint in example-api

| Name | Status | Canonical / Replacement | Implications |
|------|--------|------------------------|--------------|
| `POST /api/v1/legacy_charge` | Deprecated | `POST /api/v1/charges` | Do not add new callers; removal planned 2026-09. |
```

## Serena MCP Tools Reference

[ref: #serena-mcp-tools]

Serena exposes powerful MCP tools. Prefer them over raw file reads, manual grep, or direct edits.

**Protocol context.** The Model Context Protocol defines three server primitives — Resources, Prompts, and Tools (spec 2025-11-25; Roots and Sampling are deprecated per SEP-2577 over prompt-injection and exfiltration concerns). Serena exposes every operation below as a Tool; the tables group them by domain.

### Symbolic search and exploration

| Tool | Use it for |
|------|------------|
| `get_symbols_overview` | High-level view of symbols in a file. Best first step when opening a new file. |
| `find_symbol` | Locate a specific symbol by `name_path` pattern (e.g., `MyClass/my_method`). |
| `search_for_pattern` | Flexible regex search across files. |
| `find_referencing_symbols` | Find all symbols that reference a given symbol (impact analysis). |
| `find_implementations` | Find implementations of an interface/abstract symbol. |
| `find_declaration` | Resolve the declaration of a symbol from a usage site. |
| `get_diagnostics_for_file` | Retrieve LSP diagnostics (errors, warnings) for a file. |

### Symbolic editing

| Tool | Use it for |
|------|------------|
| `replace_symbol_body` | Replace the entire body of a function, method, or class. |
| `insert_after_symbol` | Add new code immediately after a class/method/function definition. |
| `insert_before_symbol` | Add new code immediately before a symbol definition (e.g. imports). |
| `rename_symbol` | Rename a symbol across the entire codebase. |
| `safe_delete_symbol` | Delete a symbol if it has no references. |

### Memory operations

| Tool | Use it for |
|------|------------|
| `write_memory` | Create or fully overwrite a memory file. NEVER use to append (`[ref: #serena-memory-mutation]`). |
| `read_memory` | Read a memory by name. |
| `edit_memory` | Edit in place (`literal` or `regex` mode) — the append/update tool (`[ref: #serena-memory-mutation]`). |
| `list_memories` | List memories, optionally filtered by topic; mandatory pre-create check. |
| `delete_memory` | Delete a memory — only on explicit instruction or granted permission. |
| `rename_memory` | Rename/move a memory; use `/` for scope organization. |

### Project and session management

| Tool | Use it for |
|------|------------|
| `activate_project` | Activate a project by name or path before any symbolic or memory work. |
| `get_current_config` | Print the active configuration: projects, tools, contexts, modes. |
| `onboarding` | Perform first-time onboarding for a project (at most once per conversation). |
| `initial_instructions` | Read the Serena Instructions Manual — mandatory if not yet read. |

### Agent guidelines for Serena tools

- **Prefer symbolic tools over raw reads.** Do not read a whole file if `get_symbols_overview` or `find_symbol` can give you the answer.
- **Line numbers are 0-based** in Serena tool results.
- **Verify edits.** After symbolic edits, use `get_diagnostics_for_file` to confirm the change.
