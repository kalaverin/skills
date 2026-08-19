---
name: mandatory-tools
description: "Mandatory skill for CLI, shell execution, filesystem operations, structured edits, and token-optimized commands. Selects the right tool per operation: Serena and Kagi MCP tools first, Patchloom for parser-backed and multi-file edits, RTK for token-optimized shell output, modern UNIX replacements (lsd, fd, rg, ruplacer, uv, ruff, tree) for everything else. Forbids legacy ls, find, grep, sed, pip, black, flake8, isort."
triggers:
  always: true
  reason: "Every CLI, filesystem, search, Python, structured-edit, and token-optimization decision routes through this skill."
requires:
  - frontmatter-protocol
version: 0.2.0
---

# SKILL: Mandatory Tools — Modern CLI, RTK & Patchloom

[ref: #mt-skill]

This skill is a hard gate. Before every operation that touches files, shell, search, Python, or structured data, walk the ladder below and use the first applicable layer. No exceptions, no defaults, no "good enough".

## 1. Tool Selection Ladder

[ref: #mt-ladder]

Answer in this exact order:

1. **Serena MCP?** Memory or symbolic code operation → `read_memory`, `write_memory`, `find_symbol`, `replace_symbol_body`, etc.
2. **Kagi MCP?** Web search or page enrichment → `kagi_search_fetch`, `kagi_fastgpt`, `kagi_extract`, `kagi_summarizer`.
3. **Patchloom?** Structured or multi-file edit → `execute_plan`, `doc_set`, `batch_replace`, `md_replace_section`, etc.
4. **Shell command?** Prefix with `rtk` if available.
5. **Base filesystem/search/Python?** Use the modern replacement from §2.
6. **Legacy tool?** FORBIDDEN. Halt and pick the correct layer.

If you are about to run a command and have not asked these questions, stop and ask them.

## 2. Modern Replacements

[ref: #mt-replacements]

| Legacy | Modern |
|---|---|
| `ls` | `lsd` |
| `find` | `fd` |
| `grep` | `rg` |
| `sed` (bulk replace) | `ruplacer` |
| `pip`, `poetry`, `virtualenv` | `uv` (read-only by default) |
| `black`, `flake8`, `isort` | `ruff` |

`uv` state-changing commands (`init/add/remove/lock/sync/venv/build/publish`, `tool install/uninstall`, `python install`) require the user's explicit request. Read-only safe commands are always allowed.

## 3. RTK

[ref: #mt-rtk]

When `rtk` is on PATH, every shell command starts with `rtk`. This includes commands inside `&&` chains. Choose the modern tool first, then prefix it.

```bash
# Wrong
git status && rg TODO

# Correct
rtk git status && rtk rg TODO
```

Prefer `rtk rg` over plain `rg` when expected output exceeds roughly 20 lines.

Forbidden without explicit user request: `rtk init`, `rtk trust`, `rtk untrust`, `rtk hook`, `rtk telemetry`.

## 4. Patchloom

[ref: #mt-patchloom]

Use Patchloom for any structured or multi-file edit when MCP tools are visible or the `patchloom` binary is present.

| Situation | Tool |
|---|---|
| Same edit across 2+ files | `batch_replace` |
| JSON/YAML/TOML value edit | `doc_set` / `execute_plan` |
| Markdown section by heading | `md_replace_section` |
| Coordinated multi-file edits | `execute_plan` |
| Single small plain-text edit | native edit tool or `ruplacer` dry-run |

Patchloom never replaces Serena, Kagi, or shell build/test steps (`uv`, `ruff`, `rtk`-prefixed commands).

## 5. Hard Rules

[ref: #mt-hard-rules]

1. Never use a legacy tool when a modern replacement exists.
2. Never omit the `rtk` prefix when RTK is available.
3. Never bypass Patchloom for a structured/multi-file edit when Patchloom is available.
4. Never use a non-MCP alternative when an MCP tool fits.
5. `ruplacer` dry-run first; review stdout before any `--go`.
6. Run `ruff check` and `ruff format` after any Python file change.
7. Limit directory listings with depth flags.

## 6. Violation Protocol

[ref: #mt-violation]

If you break any hard rule, halt immediately, disclose the miss in one line, discard the output, and rerun through the correct layer. Do not continue until the rerun succeeds. Record repeated violations in Serena memory under `bugs/project/mandatory-tools-bypass`.

## 7. Reference Routing

[ref: #mt-routing]

| Topic | Reference |
|---|---|
| RTK inventory | `references/rtk.md` |
| Patchloom traps | `references/patchloom.md` |
| File search | `references/fd-find.md` |
| Text search | `references/ripgrep.md` |
| Bulk replace | `references/ruplacer.md` |
| Python lint/format | `references/ruff.md` |
| uv safe commands | `references/uv.md` |
| Directory listing | `references/lsd.md` |
