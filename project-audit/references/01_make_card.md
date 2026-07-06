# Root-agent orchestration prompt: create an entity card

[ref: #pe-make-card]

## Goal

[ref: #pe-make-card-goal]

Create or update a Serena memory card for the entity (service, library, repository, or infrastructure component) specified by the user. Use a read-only subagent for codebase exploration; do not explore the code yourself.

## Input

[ref: #pe-make-card-input]

The user provides:

- `entity_name` — canonical entity name in `snake_case`, e.g. `external_api`, `modern_grpc`, `configs_production`.
- `entity_path` — absolute path to the entity directory, e.g. `/Users/kalaverin/src/important/edge-api`.

## Constraints

[ref: #pe-make-card-constraints]

- You are the **root agent**. You do **not** explore the codebase yourself.
- The subagent does **not** have access to Serena/MCP tools and cannot read memories itself. You **must** pass relevant existing Serena memory contents to the subagent as part of its input.
- You compare the subagent's fresh report with existing Serena memories yourself.
- The final card must be saved under `entities/<entity_name>`.
- All dates in memory headers must be UTC ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`).
- Entity-specific metadata (branch, latest commit, latest commit date) must come from the entity's own git repository, not from `.serena`.

## Steps

[ref: #pe-make-card-steps]

### Step 0 — Verify entity card exists

Before doing anything else, check whether `entities/<entity_name>` exists.
- If `entities/` is empty, STOP and ask the user to create the first entity card via `project-audit`.
- If the target entity has no card, STOP and ask the user to create the card for `<entity_name>` via `project-audit` or pick an existing entity.
Do not guess the entity name. `project/entities` may be consulted as a name index, but it does not authorize entity creation.

### Step 1 — Load instructions and templates

Read:

- `references/02_service_card_writer.md` — your main writing instructions (includes section order).
- `references/04_service_card_common.md` — common skeleton.
- `agent/deprecations` — deprecated names and aliases.

Determine the entity type by inspecting the directory using **only** safe, read-only shell checks (e.g., `ls`, `test -d`, `test -f`). Do not read source files. Use these criteria in order:

1. If the directory contains `apps/base/` or `clusters/` and no `app/` source tree → `Infrastructure / GitOps`.
2. Else if the directory contains `proto/` but no `app/` or `worker.py` → `library` (use `references/09_library.md`).
3. Else if the directory contains `app/api/` with FastAPI/Flask routers or `main.py`/`server.py` exposing HTTP → `REST API gateway`.
4. Else if the directory contains `worker.py` or `app/workflow/` with `@workflow.defn` → `Temporal workflow worker`.
5. Else if the directory contains `app/` with gRPC servicers or proto stubs served at runtime → `gRPC API service`.
6. Else → default to the closest matching type; if uncertain, ask the user before proceeding.

Then read the matching type-specific template:

- `references/05_grpc_service.md`
- `references/06_rest_gateway.md`
- `references/07_temporal_worker.md`
- `references/08_infrastructure_gitops.md`
- `references/09_library.md`

### Step 2 — Read existing memory

Before launching the subagent, read any existing memories for this entity so you can detect changes, contradictions, and gaps:

- `entities/<entity_name>` if it exists.
- Any `bugs/<entity_name>/...`, `notes/<entity_name>/...`, `decisions/<entity_name>/...`, `style/<entity_name>/...`, `todo/<entity_name>/...` memories.

Pass these contents to the subagent as part of its input so it can detect changes, contradictions, and gaps.

### Step 3 — Launch the read-only exploration subagent

Create an `explore` subagent and give it the prompt from `references/03_service_card_explorer.md`. Provide:

- `entity_name` = `<entity_name>`
- `entity_path` = `<entity_path>`
- `existing_memory_context` = the contents of the memories you read in Step 2, formatted clearly

Set `timeout` to at least **1800 seconds** (30 minutes); allow longer if the subagent needs it.

The subagent is read-only. It must not write to Serena, run mutating commands, or commit.

### Step 4 — Generate the directory structure section

Generate the `## Directory structure` section yourself using the exact command from `references/04_service_card_common.md`:

```bash
cd <entity_path>
tree --gitignore --prune --condense --compress 3 --dirsfirst -vnx
```

- Do not delegate this to the subagent.
- If `tree` is unavailable or fails, ask the subagent for a flat list of meaningful paths and manually format a tree-like structure.
- Add one-line responsibility comments for meaningful files/directories only.
- Skip `__init__.py`, entry points, `Dockerfile`, `Makefile`, test files, CI files, lint config, and boilerplate.

### Step 5 — Validate the report

Check that the subagent report contains all required sections and that the exported interface is exhaustive:

- REST: every endpoint listed.
- gRPC: every method, including declared-but-unimplemented.
- Worker: every workflow and activity.
- Infra: every HelmRelease per environment.
- Library: every public module/package and its purpose.

If anything is missing or unclear, ask the subagent follow-up questions until the report is complete.

### Step 6 — Resolve contradictions against existing memory

Compare every factual claim in the subagent report with the existing memories you read in Step 2:

- **Pay special attention to git branches and commit hashes.** Entity-specific metadata must come from the entity's own repository, not from `.serena`.
- If a contradiction is found:
  1. Compare recorded dates and commit hashes of the conflicting memories.
  2. If the newer memory explicitly overrides the older one, adopt the newer.
  3. If one source is `AGENTS.md` and the other is a session memory, `AGENTS.md` wins unless the session memory explicitly says it overrides `AGENTS.md`.
  4. If the contradiction is unresolved, STOP and report it to the user. Do not guess.
- Log every detected contradiction in `agent/contradictions`, even if resolved, including the conflicting memory names, dates/branches, and the resolution.

### Step 7 — Run the quality checklist

Before saving, verify the card against the checklist from `references/02_service_card_writer.md`:

- **Completeness** — every required section is present; exported interface is exhaustive.
- **Precision** — all versions are taken from lockfiles/manifests; all standards/protocols cite authoritative sources; no guesses.
- **Consistency** — metadata uses the entity's own git branch and latest commit; no unresolved contradictions.
- **Compressibility** — no fluff; one-line comments for directory entries; no duplicated information.
- **Traceability** — every finding cites file path, line, and current commit hash.

If any item fails, fix it before proceeding.

### Step 8 — Write the entity card

Convert the report into the final card format and save it to Serena memory:

**Target:** `entities/<entity_name>`

Use `write_memory`. Follow the section order from `references/02_service_card_writer.md` (which combines `references/04_service_card_common.md` with the type-specific sections).

- Write versions exactly as declared in `pyproject.toml`, `requirements/*.txt`, `uv.lock`, `package.json`, `go.mod`, or equivalent lockfiles. Do not normalize to `major.minor` and do not invent versions.
- Do not include Sentry, Prometheus, tests, linters, CI, Makefile, Docker, or entry points.
- Do not write env var values or defaults.
- Refresh the card's metadata header with the entity's own branch, latest short commit hash, and latest commit date.

### Step 9 — Write findings to separate memories

For every item in the report's `Findings for separate memory storage` section, write a focused Serena memory. Use the routing table from `serena-protocol` `[ref: #serena-findings-traceability]`:

- `bugs/<entity_name>/<topic>` — broken or inconsistent behavior.
- `notes/<entity_name>/<topic>` — observations and caveats.
- `decisions/<entity_name>/<topic>` — architectural decisions or trade-offs.
- `style/<entity_name>/<topic>` — project-specific style conventions.
- `todo/<entity_name>/<topic>` — TODOs or short actionable items from code/docs.

Keep each memory short and focused on one topic. Include traceability: file path, line number(s), and current commit hash. Do NOT duplicate the routing semantics here; if uncertain, re-read `[ref: #serena-findings-traceability]`.

### Step 10 — Verify

1. Read back the saved entity card memory to verify it was written correctly.
2. Read back the saved finding memories to verify they were written correctly.

### Step 11 — Persist and report

1. Run `just agent-memory-commit` from the project root to persist the memory changes. Do not stop until the card and all findings are committed.
2. Write a concise summary to the user chat:
   - Entity name and type.
   - Number of sections in the card.
   - Number of findings written, grouped by severity and category.
   - Any unresolved contradictions detected.
   - Whether an existing `entities/<entity_name>` card was updated or a new one was created.

## Example output style

The final card should look like existing `entities/*` cards: concise, table-heavy, factual, and business-focused. See the example in `references/04_service_card_common.md`.
