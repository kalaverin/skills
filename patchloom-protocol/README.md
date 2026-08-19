# patchloom-protocol
[ref: #patchloom-protocol]

Parser-backed structured editing and atomic multi-operation plans for files the agent modifies.

## What it does
[ref: #patchloom-what-it-does]

This skill decides when the agent should use Patchloom instead of whole-file rewrites or shell text tools. Patchloom provides document-aware operations for JSON, YAML, and TOML; section-aware markdown operations; honest text replacement with match reporting; and atomic transaction plans that can roll back on failure. The skill routes work to Patchloom MCP tools when the server is connected, and to the `patchloom` CLI when only the binary is available.

## When it activates
[ref: #patchloom-when-it-activates]

The skill activates automatically when the `patchloom` binary is detected on `PATH`. The MCP-specific rules are live only while the Patchloom MCP server is connected to the session; otherwise the CLI mandate applies.

Example prompts that should route through Patchloom:

- "Update `server.port` in `config.yaml`."
- "Replace the `## Deployment` section in `README.md`."
- "Rename this key across all JSON files in `schemas/`."
- "Apply these edits atomically and roll back if anything fails."

## How to run / use it
[ref: #patchloom-how-to-run-use-it]

What a human must set up:

1. Install the `patchloom` binary and put it on `PATH`.
2. If you want MCP integration, register the Patchloom MCP server in your host (for example, Zed `context_servers`) and pin `--cwd <project>` so the server root is deterministic. The agent never supplies the root itself.

What the agent does automatically:

- Detects whether the MCP tools are visible in the session toolset.
- Routes JSON/YAML/TOML value edits, markdown section edits, multi-file literal replacements, and coordinated or atomic edits through Patchloom.
- Keeps single small text edits on native tools when they are cheaper.
- Uses the CLI fallback (`patchloom doc set`, `patchloom md replace-section`, `patchloom tx plan.json --apply`, etc.) when the MCP server is not connected.

First-time CLI note: Patchloom previews changes by default. Any write through the CLI must include `--apply`; without it the command exits with `applied: false`.

## What it produces
[ref: #patchloom-what-it-produces]

- Modified structured documents that remain syntactically valid.
- Markdown section replacements that respect heading boundaries.
- Atomic plan results that either apply completely or roll back.
- Backup sessions under `.patchloom/backups/` that can be used for undo.
- Honest apply reports showing `applied`, `files_changed`, `refused`, and `skipped` entries.

## Dependencies and why they matter
[ref: #patchloom-dependencies-and-why-they-matter]

| Dependency | Why it matters |
|---|---|
| `shell-protocol` | Build, test, lint, and general execution hygiene still belong to the shell layer; Patchloom does not run tests or replace `uv`, `ruff`, or `rtk`. |
| `patchloom` binary | The skill is inactive without it; the CLI fallback is unavailable. |
| Patchloom MCP server | Optional; when present it enables the MCP-first golden rule and server-side workspace containment. |

## Strengths and trade-offs
[ref: #patchloom-strengths-and-trade-offs]

- **Strong sides:** Guarantees valid structured output; atomic rollback; honest match reporting prevents silent misses; containment protects against path escapes.
- **Weak sides / limits:** Requires host-side MCP registration if you want MCP mode; out-of-root paths are rejected; plans hard-fail on missing files unless guarded with `if_exists`; document writes may re-emit canonical YAML/JSON presentation.
- **Common pitfalls / gotchas:** Always pass paths relative to the MCP server root. Never try to escape containment with `../` or absolute paths. Never issue parallel write calls against the same file. Branch on `applied`/`files_changed`, not on `ok` alone. When calling the CLI, remember `--apply` for actual writes.

## Repository layout
[ref: #patchloom-repository-layout]

```text
patchloom-protocol/
├── README.md                # Human overview (this file)
└── SKILL.md              # Agent entry point: activation, inventory, traps, CLI mandate, and precedence
```

## Important conventions / gotchas
[ref: #patchloom-important-conventions-and-gotchas]

- MCP-first: when the Patchloom MCP server is connected, structured or multi-file edits must use Patchloom tools, not whole-file rewrites or `sed`/`jq`.
- The core-surface inventory is pinned to `patchloom 0.27.0`; refresh the skill on any upgrade.
- Serena owns memory and symbolic code exploration; Kagi owns web search; `shell-protocol` owns builds and tests. Patchloom must never replace those layers.
- For multi-file literal replacement, prefer `batch_replace` or a single `execute_plan` when Patchloom is connected; fall back to `ruplacer` only when Patchloom is absent or the paths are outside the server root.
