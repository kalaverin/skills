
# Patchloom Structured Editing

[ref: #patchloom-reference]

Patchloom is a parser-backed editing toolkit: JSON/YAML/TOML `doc` ops that always emit valid documents, markdown-section-aware `md` ops, text replace with match honesty, and `execute_plan` (tx) — multi-operation atomic plans with rollback. As an MCP server it enforces workspace containment server-side: the root is the workspace the host pinned at server start (`server_info.cwd` reports it), and every call is checked against it — `../` escapes and out-of-root absolute paths are rejected. This reference owns when and how the agent uses Patchloom tools (MCP-first) or the `patchloom` CLI (fallback).

## Activation

[ref: #patchloom-activation]

- **MCP live check (per session):** the Patchloom MCP tools (`execute_plan`, `doc_set`, `replace_text`, ...) are either visible in the session toolset or not. If they are NOT visible, every MCP rule in this reference is INERT — apply the CLI mandate ([ref: #patchloom-cli-mandate]) and never call the missing tools.
- **Server registration note (host-side):** the MCP root follows the server's spawn cwd unless pinned explicitly with `--cwd <project>` in the host's server entry. The explicit pin is the recommended form: the host pins `--cwd`, the model never supplies it.
- **CLI fallback:** when the MCP tools are not visible but `patchloom` is in PATH, use the CLI commands from [ref: #patchloom-cli-mandate].
- **Native fallback:** when neither MCP nor CLI is available, use native/shell tools and say so.

## Golden Rule

[ref: #patchloom-golden-rule]

Structured edits and multi-file/multi-op changes go through Patchloom tools, not through whole-file rewrites, not through shell `sed`/`jq`/`yq`. Single small text edits MAY still use the native edit tool (cheaper) — but any of these MUST be Patchloom:

1. JSON/YAML/TOML value edits → `doc_set` / `execute_plan` with `doc.set`.
2. Markdown section/bullet/table edits by heading → `md_replace_section` (or plan `md.*` ops).
3. The same edit across 2+ files → `batch_replace`.
4. 2+ coordinated edits or anything needing atomic rollback → `execute_plan` (one call, all-or-nothing).
5. Freeform snippet apply with a known anchor → plan op `apply.fragment` (never anchor-less).

## Version Pin

[ref: #patchloom-version-pin]

- This inventory and the trap list ([ref: #patchloom-apply-honesty]) are generated from `patchloom agent-rules` of **patchloom 0.27.0** (captured 2026-08-07T10:40:00Z).
- On ANY patchloom upgrade: run `patchloom agent-rules`, diff against this reference, update, and bump the pin. An installed patchloom NEWER than the pin means this reference may be stale — treat the mismatch as a refresh trigger and tell the user.
- The canonical, always-current rule dump is `patchloom agent-rules` (574 lines at 0.27.0); consult it lazily for anything not covered here — do NOT paste it into the session preemptively.

## Core-Surface Inventory

[ref: #patchloom-core-inventory]

| Tool | Use for |
|------|---------|
| `execute_plan` | Multi-op atomic plan (`{"version":1,"operations":[...]}`); full op catalog available (`doc.*`, `md.*`, `replace`, `ast.*`, `file.*`, `patch.apply`, `tidy.fix`, `apply.fragment`). Rollback on hard failure. Multi-file fan-out uses the TOP-LEVEL plan field `for_each` with a required `glob` — it is NOT an op, never put it inside `operations` and never pass a bare path array; placeholders `{path}`/`{dir}`/`{stem}`/`{ext}`/`{name}`. |
| `replace_text` | Literal replace in one file. Params: `path`, `old`, `new`; flags `require_change`, `fuzzy`, `min_fuzzy_score`, `command_position`. |
| `batch_replace` | The SAME replacement across many files. |
| `doc_set` | Set a value at a single selector path (`server.port`, `items.0.v`). Predicates/wildcards → plan `doc.update`. |
| `doc_get`, `doc_query` | Read structured values by selector without dumping the file. |
| `md_replace_section` | Replace a markdown section body by heading (section ends at the next same-or-higher-level heading — nested children included). |
| `read_file` | Read with optional line range (prefer ranges over full dumps). |
| `search_files` | Regex-by-default search; `paths` array for multi-root; mind `truncated: true`. |
| `list_files` | Ignore-aware inventory; prefer over shell `find`/`ls` for exploration. |
| `server_info` | Reports `cwd` (the enforced root), `surface`, `tool_count`, package `version`, and MCP `protocol_version`. Call once per session if the root is in doubt. |

## Apply-Honesty Traps

[ref: #patchloom-apply-honesty]

1. **Branch on `applied` / `files_changed`, never on `ok` alone.** Soft refuse / no match returns `error_kind: no_matches` with overall success possible; partial multi-path results list `refused[]` / `skipped[]` — read them before claiming full coverage.
2. **Containment:** pass paths RELATIVE to the server root. `../` escapes and absolute paths outside the root are rejected (`guard_rejected`). Outside-root work is simply out of scope — fall back to native/shell tools.
3. **No parallel write calls against the same path(s)** — per-call success does not guarantee a coherent combined result. Serialize or merge into one `execute_plan`.
4. **`doc.set` value typing:** CLI/batch values are strings parsed as JSON first — an unquoted `2.0` becomes a number; force a string with nested quotes (`"\"2.0\""`). In plan JSON, `value` is natively typed — the quoting pain disappears there, prefer plans when quoting gets ugly.
5. **Canonical names:** `old`/`new` (replace), `selector` (doc ops). Legacy aliases `from`/`to`/`key` are accepted but never emit them. CLI differs: positional `OLD` + `--new NEW`; AST `rename`/`replace` path-first, `refs`/`impact` symbol-first.
6. **Fuzzy fails closed:** with `old` absent, fuzzy refuses even above `min_fuzzy_score` unless `allow_absent_old` is set; on fuzzy/anchored matches check `matched_text` before treating the edit as semantically correct.
7. **CLI writes need `--apply`** — without it the CLI previews and exits 2 (`applied: false`). When shelling out to the CLI, always confirm `applied: true` in the JSON.
8. **Backups:** successful writes create `.patchloom/backups` sessions (in this repo the `/.*` gitignore rule hides them — in other repos verify before relying on that, or rely on the tool side: patchloom's own `git_status` omits backup dirs); `undo` is dry-run without `--apply`. Report `backup_session` when an undo might be needed.
9. **Plans hard-fail on missing paths:** in `execute_plan`/batch, a missing file is a hard `not_found` and rolls back the WHOLE plan (atomic) — set `if_exists` on optional files to soft-skip them instead. `strict: false` only tolerates soft content misses (`no_matches` on existing paths); it never continues past hard errors. CLI multi-path replace is the mirror image: missing paths soft-skip under `skipped[]`.
10. **`doc.*` re-emit honesty:** doc writes may re-emit canonical YAML presentation (e.g. collapse block-sequence indentation) while keeping values correct. When the result reports `style_changed: true`, say the file was canonically re-emitted — never claim a pure surgical text edit.

## CLI Mandate

[ref: #patchloom-cli-mandate]

When the MCP tools are not in the session but `patchloom` is in PATH, the golden-rule items map to the CLI: `patchloom doc set ... --apply`, `patchloom md replace-section ... --apply`, `patchloom batch --apply <<'EOF'` (3+ edits, one round-trip), `patchloom tx plan.json --apply` (atomic), `patchloom apply-fragment --old|--after|--before ... --apply`. All traps ([ref: #patchloom-apply-honesty]) apply; `rtk` prefixing is pass-through only.

## Precedence Contract

[ref: #patchloom-precedence]

1. **mandatory-tools owns tool selection and execution hygiene.** Build/test/run stays shell (`uv`, `ruff`, `rtk`-prefixed). Patchloom never runs tests or linters for the agent.
2. **Serena owns memory and symbolic code exploration.** `read_memory`/`write_memory`, `find_symbol`, `find_referencing_symbols` etc. never route through Patchloom (core surface has no AST tools anyway; plan-level `ast.*` ops are for mechanical edits, not exploration).
3. **kagi-search owns web** (the `kagimcp` tools) — untouched.
4. **Multi-file literal replace — the ruplacer overlap, arbitrated:** when the Patchloom MCP is connected and the target files live inside the server root, `batch_replace` (or one `execute_plan`) wins for the same literal change across files — atomicity plus match honesty. `ruplacer` (mandatory-tools, dry-run first) remains canonical when Patchloom is absent, the paths are outside the server root, or the replace needs ruplacer's own preview loop. One edit — one chosen layer, never both on the same files.
5. **Native tools keep the cheap tail:** single-line reads/edits with no structure semantics MAY stay native; the moment the golden-rule items apply, Patchloom is mandatory. The whole-file rewrite (`WriteFile` overwrite of an existing structured file) is the anti-pattern this reference replaces.
6. **Containment wins silently:** if Patchloom rejects a path, do NOT retry with escapes — use the native/shell layer and say so.

## Violation Protocol

[ref: #patchloom-violation-protocol]

If you edited a structured file or ran a multi-file change through whole-file rewrites or `sed`/`jq` while Patchloom was available, disclose the miss in one line and route the next edit through Patchloom. If the installed patchloom is NEWER than the version pin ([ref: #patchloom-version-pin]) and the reference was not refreshed, say so and propose the refresh. Never weaken the precedence contract ([ref: #patchloom-precedence]): a Patchloom call that replaces a Serena symbolic op, a kagi-search lookup, or a shell build/test step is a violation — halt, discard, rerun through the correct layer.
