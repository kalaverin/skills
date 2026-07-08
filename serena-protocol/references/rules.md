# Universal Serena Memory Protocol

A project-agnostic reference for organizing, populating, and maintaining Serena memory, and for creating entity cards.

---

## 1. What Serena memory is
[ref: #serena-what-is]

| Aspect | Rule |
|--------|------|
| **On-disk location** | `.serena/memories/` under the workspace root (`<workspace-root>/.serena/memories/`). |
| **Relationship to `AGENTS.md`** | `AGENTS.md` is the project-level source of truth for agent behavior. Serena memory stores operational facts (entity cards, bugs, decisions, notes, templates, prompts). |
| **Authoritative index** | `agent/rules` defines where to look first for authoritative knowledge. |
| **Scope** | Workspace-wide. The parent workspace owns `.serena/`; individual entity directories usually do not contain their own `.serena/`. |
| **Content language** | Technical English only. |

**Available namespaces/scopes:**

| Scope | Structure | Purpose |
|-------|-----------|---------|
| `agent/` | `agent/<topic>` | Agent behavior rules, deprecations, contradictions, known issues, user preferences. |
| `project/` | `project/<topic>` | Project-wide information: glossary, dependency graph, tech stack, entity registry. |
| `meta/` | `meta/<topic>` | Meta-information about conventions (e.g., how to name memories, skill structure). |
| `prompts/` | `prompts/<topic>` | Orchestration prompts for root/subagent workflows. |
| `templates/` | `templates/<topic>` | Entity-card templates. |
| `entities/` | `entities/<entity>` | Canonical entity cards (services, libraries, configs, infrastructure, components). No findings. |
| `bugs/` | `bugs/<entity>/<topic>` | Broken or inconsistent behavior. |
| `decisions/` | `decisions/<entity>/<topic>` | Architectural decisions and trade-offs. |
| `notes/` | `notes/<entity>/<topic>` | Observations, caveats, surprising patterns, hardcoded constants, missing docs. |
| `style/` | `style/<entity>/<topic>` | Project/entity-specific style conventions and technical-debt notes. |
| `plans/` | `plans/<entity>/<topic>` | Complex multi-step plans or investigations. |
| `proposals/` | `proposals/<entity>/<topic>` | Results of a session: proposed changes, alternative solutions, code snippets to revisit. |
| `reports/` | `reports/<entity>/<topic>` | Agent reports (reviews, incident investigations, feature research). |
| `todo/` | `todo/<entity>/<topic>` | TODOs from code and docs; short actionable one-shots so nothing is forgotten. |

---

## 2. Memory naming convention
[ref: #serena-naming]

- **Format:** `snake_case` with underscores (`_`) as word separators.
- **Allowed characters:** Latin letters (`a-zA-Z`), digits (`0-9`), and underscore (`_`) ONLY.
- **No hyphens, dashes, minus signs, spaces, or any other special characters** in memory names or directory names.
- **No leading, trailing, or consecutive underscores** (e.g. `_name`, `name_`, `name__part`).
- **Pattern:** `<domain>/<topic>` for cross-cutting scopes; `<domain>/<entity>/<topic>` for entity-scoped scopes. Topics may be nested (e.g. `guide/onboarding_glossary/chapter_01`).

### Hard rename rule

If an existing memory file or directory under `.serena/memories/` violates the
character rules above, the agent MUST rename it to a compliant name
immediately, before reading or editing its contents. Do not wait for a separate
batch and do not leave non-compliant names in place.

**Normalization recipe:**
1. Replace hyphens, dashes, en-dashes, em-dashes, spaces, and any other
   separator with `_`.
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

---

## 3. Memory namespaces & routing
[ref: #serena-namespaces-routing]

Memory names MUST use `snake_case` with underscores. NO hyphens.
Pattern: `<domain>/<topic>` or `<domain>/<entity>/<topic>`. Directory dashes become underscores (e.g., `client-api` → `client_api`).

### Entity analysis prerequisite (HARD RULE)
[ref: #serena-entity-prerequisite]

Before creating any entity-scoped memory (`bugs/<entity>/...`, `decisions/<entity>/...`, `notes/<entity>/...`, `style/<entity>/...`, `plans/<entity>/...`, `proposals/<entity>/...`, `proposal/<entity>/...`, `reports/<entity>/...`, `todo/<entity>/...`, `logic/<entity>/...`, or `entities/<entity>`), the agent MUST verify that the target entity already has a card at `entities/<entity>`.

`project/entities` is the curated registry of entity names. It groups recognized entities, but an entity is only considered usable after its card has been created via the `project-audit` skill.

**If no entity cards exist yet (`entities/` scope is empty):**
1. STOP all entity-scoped memory writes.
2. Ask the user to create the first entity card using the `project-audit` skill.
3. Do NOT guess, infer, or default to a name based on directory names.

**If the target `<entity>` does not have a card in `entities/`:**
1. STOP all memory writes for that entity.
2. Ask the user to create the entity card via `project-audit` or confirm the correct entity name from existing cards.
3. Do NOT create the entity card implicitly and do NOT guess.

Examples of valid entity registries:
- Monorepo with services, libraries, configs: `client_api`, `billing_wf`, `payment_lib`, `production`.
- Game project: `engine`, `renderer`, `physics`, `audio`, `ui`.
- Personal dotfiles: `dotbot`, `dotbot_git`, `shell`, `text`, `scripts`.

### Strict Routing Rules

- `agent/rules`: Contains the `## Contradictions log`.
- `agent/deprecations`: Source of truth for legacy aliases (e.g., `billing-api` is external).
- `project/entities`: Canonical registry of entities recognized in this workspace.
- `project/<topic>`: Project-wide knowledge (glossary, dependency graph, tech stack).
- `bugs/<entity>/<topic>`: Broken behavior, Sentry exceptions, contract mismatches.
- `decisions/<entity>/<topic>`: Architectural choices (e.g., "intentionally stateless").
- `notes/<entity>/<topic>`: Hardcoded constants, surprising patterns, missing docs.
- `entities/<entity>`: Canonical entity card ONLY. No findings here.
- `plans/<entity>/<topic>`: Complex multi-step plans or investigations.
- `proposals/<entity>/<topic>`: Proposed code changes, alternative solutions, session results.
- `proposal/<topic>` or `proposal/<entity>/<topic>`: Agent proposals that are not yet accepted but are kept for future consideration.
- `reports/<entity>/<topic>`: Agent reports (reviews, incident investigations, feature research).
- `style/<entity>/<topic>`: Technical debt, deprecated library usage, naming inconsistencies.
- `todo/<entity>/<topic>`: TODOs from code/docs for humans and agents.
- `logic/<entity>/<topic>`: Business-domain analysis output (owned by the `business-audit` skill).
- `guide/<topic>`: Manuals, onboarding docs, and reference literature for users.
- `artifacts/<topic>`: Artifacts produced during agent work (diagrams, exported data, intermediate dumps).
- `playbook/<topic>`: Agent-facing instructions, scripts, and repeatable procedures.

---

## 4. Metadata header rules
[ref: #serena-metadata]

Every memory entry MUST begin with a YAML frontmatter block enclosed in `---`, followed immediately by a Markdown H1 header (`# <Title>`). Do NOT put metadata as plain text below the header. On every `write_memory` or `edit_memory`, refresh the entire header.

### Header template
```yaml
---
title: <String; must match the H1 title below>
created_at: <UTC ISO 8601, e.g., 2026-06-16T20:00:53Z>
updated_at: <UTC ISO 8601; refresh on every edit>
repo: <String; "serena", "project", or <repo-name>>
branch: <String; current git branch>
commit: <String; 7-char short hash>
committed_at: <UTC ISO 8601; timestamp of the commit referenced by `commit`>
source: <String; project-relative path with optional line range>
---

# <Title>
```

### Field semantics
| Field | Meaning | Source |
|-------|---------|--------|
| `title` | Exact duplicate of the H1 title below the frontmatter. | The `# <Title>` line. |
| `created_at` | Timestamp when the memory was first created. | Current UTC time at first `write_memory`. |
| `updated_at` | Timestamp of the most recent content change. | Current UTC time at every `write_memory`/`edit_memory`. |
| `repo` | Git repository context: `serena` for cross-entity/agent memories, `project` for project-wide memories, or the entity/repo name (e.g., `merchant-api`) for entity-specific memories. | See Repository selection rules below. |
| `branch` | Current git branch of the selected repository. | `git rev-parse --abbrev-ref HEAD` |
| `commit` | Short hash of the latest commit in the selected repository. | `git rev-parse --short HEAD` |
| `committed_at` | Timestamp of the commit referenced by `commit`. | `git log -1 --format=%cd --date=iso-strict`, normalized to UTC `Z`. |
| `source` | Project-relative path to the relevant file or entity directory, with optional line range (`path:lineno..lineno`). | The file/directory the memory describes. |

### Optional tags

Agents MAY add additional YAML fields (tags) to the frontmatter when they provide useful metadata for filtering, routing, or context. Optional tags MUST:

- Be valid YAML scalar or list values.
- Not duplicate or contradict the mandatory fields.
- Be relevant to the memory type and content.

Common optional tags include:

| Tag | Useful for | Example |
|-----|------------|---------|
| `status` | Bugs, proposals, plans, TODOs | `status: diagnosed, fix pending` |
| `severity` | Findings, bugs | `severity: critical` |
| `priority` | TODOs, plans, proposals | `priority: high` |
| `owner` | Reports, proposals, decisions | `owner: platform-team` |
| `due_date` | TODOs, plans | `due_date: 2026-07-10T00:00:00Z` |

Agents should add tags based on the memory's nature and project conventions, not invent tags without purpose.

### Repository selection rules
| Memory type | Git source | `repo` value |
|-------------|------------|--------------|
| Entity-specific (`bugs/<entity>/...`, `entities/<entity>`) | The entity's own repository (`cd <workspace-root>/<entity-name>`). | The entity/repo name (e.g., `merchant-api`). |
| Project-wide (`project/...`) | The main project repository (`cd <workspace-root>`). | `project` |
| Cross-entity / agent (`agent/...`, `meta/...`, `prompts/...`, `templates/...`) | The Serena repository (`cd <workspace-root>/.serena`). | `serena` |

### Commands to collect metadata
```bash
cd <selected-repo>
git rev-parse --abbrev-ref HEAD         # branch
git rev-parse --short HEAD                # latest commit hash
git log -1 --format=%cd --date=iso-strict # latest commit date (ISO 8601)
```
The latest commit date must be normalized to UTC with a `Z` suffix (e.g., `2026-06-17T08:39:38Z`).

---

## 5. The metadata contract
[ref: #serena-metadata-contract]

Every memory entry MUST begin with the exact YAML frontmatter block below.
On EVERY `write_memory` or `edit_memory`, you MUST refresh this header.

```yaml
---
title: <String; must match the H1 title below>
created_at: <UTC ISO 8601>
updated_at: <UTC ISO 8601>
repo: <String; "serena", "project", or <repo-name>>
branch: <String>
commit: <7-char-short-hash>
committed_at: <UTC ISO 8601>
source: <String; project-relative path with optional line range>
---

# <Title>
```

Additional optional tags MAY appear after the mandatory fields. They do not relax the requirement to refresh the header on every mutation.

**Git Source Resolution Rule:**
- **Entity-specific memory** (`bugs/`, `entities/`, etc.): Execute git commands INSIDE the entity's own repository (`cd <workspace-root>/<entity-name>`). Set `repo` to the entity/repo name (e.g., `merchant-api`).
- **Project-wide memory** (`project/`): Execute git commands INSIDE the main project repository (`cd <workspace-root>`). Set `repo` to `project`.
- **Meta/Cross-entity memory** (`agent/`, `meta/`, `prompts/`, `templates/`): Execute git commands INSIDE the `.serena` directory (`cd <workspace-root>/.serena`). Set `repo` to `serena`.

**Mandatory Git Retrieval Commands:**
```bash
git rev-parse --abbrev-ref HEAD
git rev-parse --short HEAD
git log -1 --format=%cd --date=iso-strict
```
*(Ensure timezone is converted/appended as UTC `Z`).*

---

## 6. Memory lifecycle / workflow
[ref: #serena-lifecycle]

Agents must proactively populate Serena memory without being reminded.

### Before writing any entity-scoped memory
1. Apply `[ref: #serena-entity-prerequisite]`: verify the target entity has a card at `entities/<entity>`.
2. If `entities/` is empty, STOP and ask the user to create the first entity card via `project-audit`.
3. If the target entity has no card, STOP and ask the user to create it via `project-audit` or pick an existing entity.
4. Only then proceed to the routing table below.

### When to record
| Trigger | Target namespace |
|---------|------------------|
| Confirmed bug | `bugs/<entity>/<topic>` |
| Architectural decision or trade-off | `decisions/<entity>/<topic>` |
| Strange pattern, caveat, observation | `notes/<entity>/<topic>` |
| Coding style convention or technical debt | `style/<entity>/<topic>` |
| Agent behavior bug or workaround | `agent/<topic>` |
| Proposed change/refactoring/alternative solution | `proposals/<entity>/<topic>` |
| Short actionable item from code/docs | `todo/<entity>/<topic>` |
| Complex multi-step plan or investigation | `plans/<entity>/<topic>` |
| Agent report | `reports/<entity>/<topic>` |
| Project-wide knowledge or entity registry | `project/<topic>` |

### Verification and persistence
1. After any `write_memory` or `edit_memory`, **read the memory back** to verify it was saved correctly.
2. Run the configured persistence command (e.g., `just serena-checkpoint`) from the workspace root. Do not stop until everything is persisted.

### When reading entity-specific memories
[ref: #serena-memory-freshness]

Before trusting the contents of an entity-specific memory (where `repo` is neither `serena` nor `project`), verify that the memory still reflects the current state of the entity's repository.

1. Locate the entity repository (`<workspace-root>/<repo>`).
2. Compare the memory's `commit` and `committed_at` against the repository's current HEAD:
   ```bash
   cd <workspace-root>/<repo>
   git rev-parse --short HEAD
   git log -1 --format=%cd --date=iso-strict
   ```
3. If the memory's `commit` differs from HEAD, treat the memory as potentially stale. Then:
   - Run `git diff <memory-commit>..HEAD` to see all changes in the repository since the memory was recorded.
   - Reconcile the memory's claims against the diff. Update the memory if the changes invalidate it, or append a note describing the divergence.
   - If you cannot reconcile automatically, inform the user that the memory may be stale and ask how to proceed.

This freshness check does NOT apply to memories where `repo` is `serena` or `project`.

---

## 7. Memory mutation protocol
[ref: #serena-memory-mutation]

**CRITICAL:** `write_memory` completely overwrites a file. You MUST NEVER use it to append to an existing memory.

**To CREATE a new memory:**
1. Call `list_memories` to ensure the name does not exist.
2. Call `write_memory`.

**To APPEND to an existing memory:**
Call `edit_memory` with the following EXACT JSON payload:
```json
{
  "mode": "regex",
  "needle": "\\Z",
  "repl": "\n\n## <New Section>\n<new content>"
}
```

**To UPDATE specific lines:**
Use `edit_memory` with a highly specific `regex` targeting only the outdated paragraph/table row.

---

## 8. Entity card creation workflow
[ref: #serena-card-workflow]

The root agent orchestrates; a read-only subagent explores.

### Root-agent responsibilities
1. Load templates and existing memory.
2. Apply `[ref: #serena-entity-prerequisite]`: confirm the target entity has a card at `entities/<entity>`; if not, STOP and ask the user.
3. Determine entity type via safe, read-only shell checks.
4. Launch a read-only `explore` subagent.
5. Generate the `## Directory structure` section using the exact `tree` command.
6. Validate the report, resolve contradictions, write the final card to `entities/<entity>`.
7. Write findings to separate memories (bugs, notes, decisions, style, todo).
8. Run the persistence command.

### Subagent responsibilities
- Read existing memories and templates.
- Explore the codebase thoroughly.
- Do **not** generate the directory tree.
- Do **not** write to Serena or run mutating commands.
- Return a structured markdown report.

### Directory tree command (Root Agent Only)
```bash
cd <entity_path>
tree --gitignore --prune --condense --compress 3 --dirsfirst -vnx
```
- Add one-line responsibility comments for meaningful files/directories only.
- Do **not** write the `tree` command itself into the final card.

---

## 9. Deterministic type detection algorithm
[ref: #serena-algo-type-detection]

When analyzing a repository to create an `entities/` card, you MUST apply this logic in exact order:

1. `IF` directory contains `apps/base/` or `clusters/` AND NO `app/` source tree:
   ➔ Type is **`Infrastructure / GitOps`**
2. `ELSE IF` directory contains `proto/` AND NO `app/` OR `worker.py`:
   ➔ Type is **`library`**
3. `ELSE IF` directory contains `app/api/` (with FastAPI/Flask routers) OR `main.py`/`server.py` exposing HTTP:
   ➔ Type is **`REST API gateway`**
4. `ELSE IF` directory contains `worker.py` OR `app/workflow/` with `@workflow.defn`:
   ➔ Type is **`Temporal workflow worker`**
5. `ELSE IF` directory contains `app/` with gRPC servicers:
   ➔ Type is **`gRPC API service`**
6. `ELSE`:
   ➔ Default to closest match or STOP and ask user.

---

## 10. Card creation segregation (Root vs Subagent)
[ref: #serena-agent-segregation]

To prevent hallucinations and restricted-shell failures, responsibilities are strictly segregated.

**ROOT AGENT (You):**
- Applies `[ref: #serena-entity-prerequisite]`: confirms the entity has a card at `entities/<entity>`; if not, STOP and ask.
- Determines the entity type using the algorithm above.
- Generates the `## Directory structure` locally (Subagent MUST NOT do this).
- Reads existing memories to prepare for contradiction checks.
- Launches the Subagent.
- Resolves contradictions, writes the final card to `entities/`, and writes findings to `bugs/`, `notes/`, etc.
- Runs `just serena-checkpoint`.

**EXPLORATION SUBAGENT (Read-only):**
- Has a `timeout` of at least `1800` seconds.
- Reads `pyproject.toml`, `uv.lock`, code, and proto files.
- Extracts exhaustive interfaces (see Matrix below).
- Outputs a flat list of meaningful paths (so Root Agent knows what to annotate in the tree).
- Outputs findings with severity and exact Git hashes.

**Mandatory Tree Command (Run by ROOT AGENT):**
```bash
cd <entity_path>
tree --gitignore --prune --condense --compress 3 --dirsfirst -vnx
```
*Rule: Do NOT include `__init__.py`, `Makefile`, `Dockerfile`, `tests/`, `CI` files, or entry points in the final annotated tree.*

---

## 11. Quality checklist
[ref: #serena-quality]

Before saving an entity card, verify:
- **Completeness:** Every required section is present; exported interface is exhaustive (every endpoint, every gRPC method, every workflow/activity).
- **Precision:** All versions come from lockfiles/manifests; do not guess.
- **Consistency:** Metadata uses the entity's own git branch and latest commit.
- **Traceability:** Every finding cites file path, line, and current commit hash.

---

## 12. Interface exhaustiveness matrix
[ref: #serena-interface-exhaustiveness]

The Subagent MUST extract interfaces according to these strict rules. Summarization is FORBIDDEN.

| Type | Exhaustive Requirements |
|---|---|
| **gRPC API** | MUST extract EVERY method. MUST create a separate table for methods declared in `.proto` but NOT implemented in code. Use Protobuf message names (e.g., `CreateAdvertRequest`), not field definitions. |
| **REST API** | MUST extract EVERY route. MUST split into unauthenticated (misc/health) vs authenticated (`/api/v1`). Path parameters MUST use `{param}` notation. MUST specify Auth type (e.g., `OAuth2`, `RSA-PSS`, `none`). |
| **Temporal Worker** | MUST extract EVERY `@workflow.defn` and `@activity.defn`. MUST list all signals, queries, updates, and cron schedules. Activities MUST map to their downstream service calls. |
| **Library** | MUST list EVERY public package/module. Omit generated internal helpers. MUST include build/generation rules (e.g., `buf`, `protoc-gen-go`). |
| **Infra** | MUST extract EVERY `HelmRelease` grouped by environment/namespace. |

---

## 13. Contradiction resolution
[ref: #serena-contradictions]

1. Compare the recorded dates and commit hashes of the conflicting memories.
2. Newer memory explicitly overriding older memory wins.
3. `AGENTS.md` wins over session memory unless explicitly stated otherwise.
4. If unresolved, **STOP and report it to the user**. Do not guess.

Log detected contradictions in `agent/rules ## Contradictions log`.

---

## 14. Contradiction resolution protocol
[ref: #serena-contradiction-resolution]

When creating a card, compare the Subagent's fresh report against existing Serena memories.

1. **Compare Dates/Hashes:** Check the header of the conflicting memories.
2. **Explicit Override:** If the newer memory explicitly states it overrides the older one, adopt the newer.
3. **Hierarchy Rule:** If one source is `AGENTS.md` and the other is a session memory, **`AGENTS.md` WINS** unless the session memory explicitly overrides `AGENTS.md` by name.
4. **Failure State:** If the contradiction is unresolved, you MUST STOP and report it to the user. DO NOT GUESS.
5. **Logging:** You MUST log every detected contradiction (even if resolved) by appending to `agent/rules` under the `## Contradictions log` header using `edit_memory`.

---

## 15. Core tools and commands
[ref: #serena-core-tools]

### Serena memory tools
- `write_memory` **overwrites** the entire file. Never use it to append.
- To create a new memory, first call `list_memories` to ensure the name does not exist.
- To add to an existing memory, use `edit_memory` with:
```json
{
  "mode": "regex",
  "needle": "\\Z",
  "repl": "\n\n<new content>"
}
```

### Git metadata commands
```bash
cd <entity-repo>
git rev-parse --abbrev-ref HEAD
git rev-parse --short HEAD
git log -1 --format=%cd --date=iso-strict
```

### Persistence command
```bash
<memory-commit-command>
```
Run from the workspace root after every memory write/edit. Replace with the command configured for the project (commonly `just serena-checkpoint`).

### Working directory for Serena operations
Every Serena operation that touches `.serena/` — including `write_memory`, `edit_memory`, `list_memories`, `delete_memory`, `rename_memory`, and the persistence command — MUST be executed from the workspace root (`cd <workspace-root>`). Before running the command, verify that the target `.serena/` directory is the workspace-root `.serena/` and not a nested instance inside a subdirectory. Never run Serena commands from within an entity directory or any other nested project that may contain its own `.serena/`.

---

## 16. Deprecated services and aliases
[ref: #serena-deprecations]

Maintain a deprecation table in `agent/deprecations` for the project. Example structure:
| Name | Status | Canonical / Replacement | Implications |
|------|--------|------------------------|--------------|
| `<old-name>` | Deprecated | `<new-name>` | Treat `<old-name>` as legacy; do not create new cards. |

Every project must document its own deprecated names and aliases. Cards must use canonical names.

---

## 17. Findings & traceability
[ref: #serena-findings-traceability]

Findings (bugs, anomalies, missing configs, TODOs, style issues) MUST NEVER be placed in the `entities/<entity>` card. They MUST be routed to `bugs/`, `notes/`, `decisions/`, `style/`, or `todo/`.

**Traceability Requirement:**
EVERY finding must be anchored to a specific file, line, AND the exact commit hash of that file at the moment of exploration.

**Subagent Command for Traceability:**
```bash
git log -1 --format=%H -- <relative-file-path>
```

Each finding must declare:
- **Severity:** `critical` (breaks functionality), `warning` (tech debt/inconsistency), `info` (observation).
- **Location:** `path/to/file.py:line_num`
- **Hash:** `(commit <extracted-hash>)`

---

## 18. Hard fails & forbidden actions
[ref: #serena-forbidden-actions]

If you do any of the following, you fail the protocol:
- **HARD FAIL:** Hand-writing a directory tree instead of using the exact `tree` CLI command output.
- **HARD FAIL:** Rounding or normalizing dependency versions (e.g., writing `FastAPI 0.10x` instead of reading the exact version from `uv.lock`).
- **HARD FAIL:** Using the `.serena` git repository to fill out the metadata header for a specific entity like `client-api`.
- **HARD FAIL:** Including `Sentry`, `Prometheus`, `pytest`, `ruff`, or CI/CD pipelines in the `Technology stack` section of an entity card.
- **HARD FAIL:** Writing actual environment variable VALUES or SECRETS in memory. Write the PREFIX and description only.
- **HARD FAIL:** Forgetting to run `just serena-checkpoint` (or equivalent persistence command) after writing/editing memories.
- **HARD FAIL:** Writing to an entity-scoped namespace when the target entity has no card at `entities/<entity>`.
- **HARD FAIL:** Implicitly creating an entity card outside the `project-audit` skill.
- **HARD FAIL:** Guessing an entity name instead of asking the user.
- **HARD FAIL:** Executing any Serena memory operation or persistence command from anywhere other than the workspace root when a nested `.serena/` could be affected.

---

## 19. Examples of memory entries
[ref: #serena-examples]

### `bugs/<entity>/<topic>`
```yaml
---
title: Example validation error not translated (EXAMPLE-API-E1)
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
repo: example-api
branch: <branch>
commit: <7-char-short-hash>
committed_at: YYYY-MM-DDTHH:MM:SSZ
source: example-api/src/handlers/example.py:42..45
status: diagnosed, fix pending
---

# Example validation error not translated (EXAMPLE-API-E1)

**Entity:** example-api → downstream-api

## Problem
`POST /api/v1/example` triggers Sentry event `EXAMPLE-API-E1`:
`ValidationError: Invalid input`.
```

### `entities/<entity>` card header
```yaml
---
title: example-api entity card
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
repo: example-api
branch: <branch>
commit: <7-char-short-hash>
committed_at: YYYY-MM-DDTHH:MM:SSZ
source: example-api
---

# example-api entity card

## Purpose
Example public-facing REST gateway for the platform...
```

---

## 20. Common mistakes and gotchas
[ref: #serena-mistakes]

| Mistake | How to avoid |
|---------|--------------|
| **Hand-written directory trees** | Always run `tree --gitignore --prune --condense --compress 3 --dirsfirst -vnx` |
| **Stale metadata headers** | Refresh the header on every `write_memory`/`edit_memory`. |
| **Using `.serena` repo for entity metadata** | Use the entity's own git repository for entity cards/findings. Use `.serena` only for cross-entity meta. |
| **Forgetting the persistence command** | Run the configured memory-commit command after every write/edit cycle. |
| **Using `write_memory` to append** | Use `edit_memory` with `mode: "regex"`, `needle: "\\Z"` to append. |
| **Putting findings in the entity card** | Route anomalies, TODOs, style issues to `bugs/`, `notes/`, `decisions/`, `style/`, or `todo/` memories. |
| **Including development meta in cards** | Omit Sentry, Prometheus, tests, linters, CI, Makefile, Docker. |
| **Writing env var values** | List only important env var prefixes and names; never values, examples, or secrets. |
| **Guessing entity names** | Apply `[ref: #serena-entity-prerequisite]`; if the entity has no card, STOP and ask the user. |

---

## 21. Serena MCP tools reference
[ref: #serena-mcp-tools]

Serena exposes powerful MCP tools. Prefer them over raw file reads, manual grep, or direct edits.

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

### Agent guidelines for Serena tools
- **Prefer symbolic tools over raw reads.** Do not read a whole file if `get_symbols_overview` or `find_symbol` can give you the answer.
- **Line numbers are 0-based** in Serena tool results.
- **Verify edits.** After symbolic edits, use `get_diagnostics_for_file` to confirm the change.
