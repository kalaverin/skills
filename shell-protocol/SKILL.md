---
name: shell-protocol
description: Mandatory skill for CLI, shell execution, and filesystem operations. Applies when the user asks to list directory contents, search the disk/directory (fd-find), search inside files or grep (ripgrep), lint or format Python code (ruff), replace text, run Python tools, or manage dependencies. Natural-language triggers include 'поищи на диске', 'поищи в каталоге', 'посмотри содержимое каталога', 'грепни', 'прогрепай', 'проверь стайл', 'причеши код', 'поправь форматирование', and equivalent phrases. Enforces modern tools (lsd, fd, rg, ruplacer, uv, ruff) over legacy UNIX utilities.
triggers:
  always: true
  reason: "All file/code operations use CLI tools."
---

# SKILL: Modern Shell Tooling & Environment

You are an expert DevSecOps and CLI Architect. You MUST use modern, high-performance CLI tools instead of legacy UNIX utilities. This reduces token usage, speeds up operations, and prevents context flooding.

**Skill Boundary:** This skill governs tool selection and CLI usage for filesystem
and Python operations. For Python language/style rules and the full Ruff
self-linting protocol, consult the `python-lang` skill.

## User Intent Mapping

Map common user phrases to the correct modern tool:

| User phrase or intent | Target tool | Example phrases |
|---|---|---|
| Search for files by name, extension, type, or location. | `fd` (fd-find) | "поищи на диске", "поищи в каталоге", "find files", "search the filesystem" |
| List directory contents with details. | `lsd` | "посмотри содержимое каталога", "посмотри в директории", "list files", "show directory" |
| Search text or symbols inside files. | `rg` (ripgrep) | "поищи в файлах", "грепни", "прогрепай", "grep for", "search text in files" |
| Lint or format Python code. | `ruff` | "проверь стайл", "прочекай стиль", "причеши код", "поправь форматирование", "lint Python", "format Python" |

If a phrase is ambiguous, prefer the tool whose primary domain matches the context.
For example, "поищи" in a filesystem context means `fd`; in a text-search context means `rg`.

## ⚠️ STRICT RULE: TOOL REPLACEMENTS
You MUST NEVER use the legacy tools on the left. You MUST ALWAYS use the modern tools on the right.
* `ls` ➔ FORBIDDEN. Use `lsd`.
* `find` ➔ FORBIDDEN. Use `fd`.
* `grep` ➔ FORBIDDEN. Use `rg` (ripgrep).
* `sed` (for symbol bulk replaces) ➔ FORBIDDEN. Use `ruplacer`.
* `pip`, `poetry`, `virtualenv` ➔ FORBIDDEN. Use `uv`.
* `black`, `flake8`, `isort` ➔ FORBIDDEN. Use `ruff`.

## 1. Compliance and Lazy-Load Protocol (CRITICAL)
You MUST NOT read the tool manuals in `references/` in their entirety. You MUST use partial extraction via `rg` to preserve context memory.

* `CORE FILESYSTEM:` Usage of `fd`, `rg`, `lsd`, and `tree` is **ALWAYS MANDATORY** when navigating or searching the filesystem.
* `PYTHON ECOSYSTEM:` Usage of `uv` and `ruff` is **ALWAYS MANDATORY** when the workspace contains Python code.

**Extraction Workflow:**
1. Match your task to the routing table below."
2. Execute an `rg` command to extract the exact section."
   *Example CLI command:* `rg -A 40 "\\[ref: #fd-agent-recipes\\]" references/fd-find.md`
3. Apply the extracted flags and commands strictly.

## 2. Mandatory Routing Table

### Core Filesystem & Search (ALWAYS MANDATORY)
| Trigger / Situation | Target File | Section Header | Anchor |
|---|---|---|---|
| First-pass project layout; folder skeleton; depth limits. | `references/tree.md` | Agent Recipes | `[ref: #tree-agent-recipes]` |
| Detailed listing; sizes, permissions, git status. | `references/lsd.md` | Agent Recipes | `[ref: #lsd-agent-recipes]` |
| Finding files by name, extension, type, size, modified time. | `references/fd-find.md` | Agent Recipes | `[ref: #fd-agent-recipes]` |
| Narrowing search scope or filtering file types. | `references/fd-find.md` | Scope and Type Filters | `[ref: #fd-scope-and-type-filters]` |
| Searching text/code inside files; finding imports/usages. | `references/ripgrep.md` | Agent Recipes | `[ref: #rg-agent-recipes]` |
| Formatting rg output for pipelines or disabling colors. | `references/ripgrep.md` | Output Modes | `[ref: #rg-output-modes]` |

### Bulk Code Operations
| Trigger / Situation | Target File | Section Header | Anchor |
|---|---|---|---|
| Replacing text in multiple files across the codebase. | `references/ruplacer.md` | Absolute Rule: DRY RUN First, Always | `[ref: #ruplacer-dry-run]` |
| Renaming symbols or checking collision safety before a rename. | `references/ruplacer.md` | Symbol Renaming and Naming Collision Prevention | `[ref: #ruplacer-rename-collision-check]` |
| Need syntax examples for ruplacer and capture groups. | `references/ruplacer.md` | Examples | `[ref: #ruplacer-examples]` |

### Python Ecosystem (MANDATORY FOR PYTHON)
| Trigger / Situation | Target File | Section Header | Anchor |
|---|---|---|---|
| Linting, formatting, code quality after Python file edits. | `references/ruff.md` | Agent Linting Protocol | `[ref: #ruff-agent-linting-protocol]` |
| Need command recipes for ruff formatting/linting. | `references/ruff.md` | Agent Recipes | `[ref: #ruff-agent-recipes]` |
| Safe read-only Python ops (checking deps, tree, version). | `references/uv.md` | Safe Workflow Checklist | `[ref: #uv-safe-workflow-checklist]` |

## 3. Execution Mandates
1. **ruplacer**: You MUST perform a dry run (omit `--go`) first. Review stdout before executing actual writes. No exceptions.
2. **ruplacer rename safety**: Before any rename-like `ruplacer` operation, even a dry run, you MUST run `rg` to confirm the target name does not already exist in the codebase. If it exists, stop or choose a different name. See `[ref: #ruplacer-rename-collision-check]`.
3. **renaming hierarchy**: For global renames across documentation, configuration, strings, or multiple file types, use `ruplacer`. For renaming code symbols (functions, classes, methods, variables, fields, etc.), first try the Serena `rename_symbol` tool; fall back to `ruplacer` only when Serena cannot handle the target language or symbol. NEVER use `sed`, `awk`, or similar text tools for any rename.
4. **ruff**: You MUST run `ruff check` and `ruff format` after *any* Python file modification. Only fix code you modified yourself.
5. **uv**: Default to `references/uv.md` (safe mode) unless explicit package installation or lock mutation is required.
6. **tree / lsd**: You MUST limit recursion depth (e.g., `--depth 3` or `-L 3`) to avoid output flooding.

---

## 4. Master Execution Workflow
1. **Analyze Task:** Determine which modern tool(s) are needed.
2. **Consult Routing Table:** Find the relevant `[ref: #...]` marker.
3. **Extract:** Run `rg` to read only the relevant section of the reference file.
4. **Execute:** Apply the extracted flags and commands strictly.
5. **Verify:**
   - Confirm the command uses the modern tool, not the legacy equivalent.
   - Confirm `ruplacer` was dry-run before any write.
   - Confirm no unmodified files were changed.
