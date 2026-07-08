# Root agent prompt: write an entity card

[ref: #pe-writer]

You are the **root agent**. Your job is to produce a final entity card in Serena memory. You do **not** explore the codebase yourself; you delegate that to a read-only subagent and then write the results.

Skip any information about AGENTS.md or Serena architecture. The card should be a concise, factual, business-focused document describing the entity, its technology, and its exported interface. Do not include any development meta (tests, linters, CI, Makefile), observability-only dependencies (Sentry, Prometheus), or entry points (how to run the entity).

## Input

The user gives you an entity name, e.g. `important-api`, `drinks-wf`, `production`.

## Step 1 — Load templates

Read these memories to understand the target format:
- `references/04_service_card_common.md`
- `references/05_grpc_service.md`
- `references/06_rest_gateway.md`
- `references/07_temporal_worker.md`
- `references/08_infrastructure_gitops.md`
- `references/09_library.md`

## Step 2 — Launch read-only exploration subagent

Create an `explore` subagent and give it the prompt from `references/03_service_card_explorer.md`. Provide:
- `entity_name`
- `entity_path` = `$PWD/<entity_name>`
- `existing_memory_context` = the contents of any existing `entities/<entity_name>` card and relevant `bugs/<entity_name>/...`, `notes/<entity_name>/...`, `decisions/<entity_name>/...`, `style/<entity_name>/...`, or `todo/<entity_name>/...` memories

Wait for the subagent to return a complete exploration report in the format defined in `references/03_service_card_explorer.md`.

The subagent is read-only and does not have access to Serena/MCP tools. It must not write to Serena, run mutating commands, or commit.

## Step 3 — Generate the directory tree

The root agent MUST generate the `## Directory structure` section itself. Use the exact command from `references/04_service_card_common.md`:

```bash
cd <entity_path>
tree --gitignore --prune --condense --compress 3 --dirsfirst -vnx
```

- Do not delegate this to the subagent.
- Add one-line responsibility comments for meaningful files/directories only.
- Skip `__init__.py`, entry points, `Dockerfile`, `Makefile`, test files, CI files, lint config, and boilerplate.
- Do **not** write the `tree` command itself into the final card.

## Step 4 — Validate the report

Check that the report contains all required sections and that the exported interface is exhaustive:
- REST: every endpoint listed.
- gRPC: every method, including declared-but-unimplemented.
- Worker: every workflow and activity.
- Infra: every HelmRelease per environment.
- Library: every public module/package and its purpose.

If anything is missing or unclear, ask the subagent follow-up questions until the report is complete.

## Step 5 — Resolve contradictions against existing memory

Before writing, compare every factual claim in the subagent report with existing Serena memories:

- Re-read `entities/<entity_name>` if it exists, plus any `bugs/<entity_name>/...`, `notes/<entity_name>/...`, `decisions/<entity_name>/...`, `style/<entity_name>/...`, or `todo/<entity_name>/...` memories.
- **Pay special attention to git branches and commit hashes.** Entity-specific metadata must come from the entity's own repository, not from `.serena`. Project-wide memories use `.serena`.
- If a contradiction is found:
  1. Compare recorded dates and commit hashes of the conflicting memories.
  2. If the newer memory explicitly overrides the older one, adopt the newer.
  3. If one source is `AGENTS.md` and the other is a session memory, `AGENTS.md` wins unless the session memory explicitly says it overrides `AGENTS.md`.
  4. If the contradiction is unresolved, STOP and report it to the user. Do not guess.
- Log every detected contradiction in `agent/contradictions`, even if resolved, including the conflicting memory names, dates/branches, and the resolution.

## Step 6 — Quality checklist

Before saving, verify the card against this checklist:

- **Completeness** — every required section from `references/04_service_card_common.md` and the matching type-specific template is present; exported interface is exhaustive.
- **Precision** — all versions are taken from lockfiles/manifests; all standards/protocols cite authoritative sources; no guesses.
- **Consistency** — metadata uses the entity's own git branch and latest commit; no contradictions with existing memory unless explicitly resolved.
- **Compressibility** — no fluff; one-line comments for directory entries; no duplicated information.
- **Traceability** — every finding cites file path, line, and current commit hash.

If any item fails, fix it before proceeding.

## Step 7 — Write the entity card

Convert the report into the final card format and save it to Serena memory:

**Target:** `entities/<entity_name>`

Use `write_memory`. The final card must follow the section order from `references/04_service_card_common.md` plus the type-specific sections from the matching type template.

Section order:

```markdown
# <entity-name> entity card

## Purpose

## Type

## Technology stack

## Standards and protocols

## Directory structure

## Required resources / suppliers

## Important environment variables

## <type-specific exported interface section(s)>
```

- Write versions exactly as declared in `pyproject.toml`, `requirements/*.txt`, `uv.lock`, `package.json`, `go.mod`, or equivalent lockfiles. Do not normalize to `major.minor` and do not invent versions.
- Do not include Sentry, Prometheus, tests, linters, CI, Makefile, Docker, or entry points.
- Do not write env var values or defaults.

## Step 8 — Write findings to separate memories

For every item in the report's `Findings for separate memory storage` section, write a focused Serena memory. Use the routing table from `serena-protocol` `[ref: #serena-findings-traceability]`:

- `bugs/<entity>/<topic>` — broken or inconsistent behavior.
- `notes/<entity>/<topic>` — observations and caveats.
- `decisions/<entity>/<topic>` — architectural decisions or trade-offs.
- `style/<entity>/<topic>` — project-specific style conventions.
- `todo/<entity>/<topic>` — TODOs or short actionable items from code/docs.

Keep each memory short and focused on one topic.

## Step 9 — Verify

1. Read back the saved entity card memory to verify it was written correctly.
2. Read back the saved finding memories to verify they were written correctly.

## Step 10 — Report summary

After verification, write a short summary to the user chat:

- Number of sections in the card.
- Number of findings written, grouped by severity and category.
- Any unresolved contradictions detected.
- Whether an existing `entities/<entity_name>` card was updated or a new one was created.

Then run `just serena-checkpoint` to persist the memory changes. Do not stop until the card and all findings are committed.

## Example output style

The final card should look like existing `entities/*` cards: concise, table-heavy, factual, and business-focused. See the example in `references/04_service_card_common.md`.
