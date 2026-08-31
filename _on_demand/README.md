# _on_demand
[ref: #ondemand-readme-intro]

> Human overview of the on-demand skill directory. The machine layer is the `ondemand:` manifest in `_on_demand/SKILL.md`; this file explains it, never duplicates it.

## What on-demand skills are
[ref: #ondemand-readme-what]

On-demand skills are rarely used capabilities stored outside the always-loaded skill set: they are discovered from the compressed manifest and loaded only when their triggers match the current request.

- Each skill lives in its own directory under `_on_demand/<skill>/`.
- The manifest keeps startup cheap: headers only, never full skill bodies.

## How the manifest is used
[ref: #ondemand-readme-usage]

- At bootstrap, the `_on_demand/SKILL.md` frontmatter is batch-extracted like any skill header.
- Entries with `runtime: true` re-evaluate after every new user message or path touch; the rest evaluate once at bootstrap.
- On a match, the agent reads `_on_demand/<skill>/SKILL.md` in full and resolves its `requires`.

## On-demand skill index
[ref: #ondemand-readme-index]

Every skill lives at `_on_demand/<skill>/`.

| Skill | Runtime | Short description |
|---|---|---|
| `atlassian-skill` | yes | Read-only Atlassian Jira and Confluence access via MCP. |
| `bobplus-api` | yes | Bobplus Payments API integration knowledge for Africa payments. |
| `code-review` | yes | Language-agnostic diff-based and full-project code review. |
| `feature-archival` | yes | Archive a completed feature's memory footprint into `archive/<feature>/`. |
| `loki-skill` | yes | Grafana Loki log investigation through `logcli`. |
| `protobuf-lang` | yes | Buf Protobuf lint and schema style. |
| `pytest-design` | yes | Python unit, integration, and pytest suite work. |
| `pytest-planner` | no | Repository-specific pytest enablement and coverage plans. |
| `repo-audit` | no | Full repository audits, entity cards, and dependency maps. |
| `security-audit` | no | OWASP API Security Top 10 aligned SAST workflow. |
| `service-layout` | yes | Company Python service layout standard, ruling ids L/I/D/M/P/E/S/T/Y/O. |
| `session-inspector` | yes | Token-cheap inspection of Kimi Code CLI session files. |
| `temporal-lang` | yes | Temporal workflows, activities, workers, and operations. |

## How to add a new on-demand skill
[ref: #ondemand-readme-add]

1. Create `_on_demand/<skill>/SKILL.md` with a valid header; add `runtime: true` if it must re-evaluate mid-session.
2. Harvest headers: `uv run --no-project --with pyyaml python _on_demand/scripts/harvest_manifest.py`, then compress the raw manifest into `.tmp/_on_demand/.manifest.compressed.yaml` (subagent task) per the trigger-compression convention (`mem:decisions/project/ondemand_trigger_compression`) and review it.
3. Apply the manifest: `uv run --no-project --with pyyaml python _on_demand/scripts/apply_manifest.py` — it rewrites `_on_demand/SKILL.md`, so never edit that file by hand.
4. Add a row to the index above.

## Repository layout
[ref: #ondemand-readme-layout]

> **DEPRECATED 2026-08-31T20:08:13Z:** the tree duplicated the index's paths and descriptions and had drifted stale (it missed `feature-archival`). The index table is the single layout view. See [ref: #ondemand-readme-index]

## Dependencies
[ref: #ondemand-readme-deps]

- `frontmatter-protocol` — owns the header schema, trigger grammar, and discovery algorithm that consume this manifest.
