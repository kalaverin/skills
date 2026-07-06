---
name: shell-protocol
description: >
  MANDATORY skill for CLI, shell execution, and filesystem operations. Use when
  listing files, searching files or text, replacing text, running Python tools,
  linting, or managing dependencies. Enforces modern tools (lsd, fd, rg,
  ruplacer, uv, ruff) over legacy UNIX utilities.
triggers:
  always: true
  reason: "All file/code operations use CLI tools."
---

# SKILL: Modern Shell Tooling & Environment

You are an expert DevSecOps and CLI Architect. You MUST use modern, high-performance CLI tools instead of legacy UNIX utilities. This reduces token usage, speeds up operations, and prevents context flooding.

**Skill Boundary:** This skill governs tool selection and CLI usage for filesystem
and Python operations. For Python language/style rules and the full Ruff
self-linting protocol, consult the `python-lang` skill.

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
| Need syntax examples for ruplacer and capture groups. | `references/ruplacer.md` | Examples | `[ref: #ruplacer-examples]` |

### Python Ecosystem (MANDATORY FOR PYTHON)
| Trigger / Situation | Target File | Section Header | Anchor |
|---|---|---|---|
| Linting, formatting, code quality after Python file edits. | `references/ruff.md` | Agent Linting Protocol | `[ref: #ruff-agent-linting-protocol]` |
| Need command recipes for ruff formatting/linting. | `references/ruff.md` | Agent Recipes | `[ref: #ruff-agent-recipes]` |
| Safe read-only Python ops (checking deps, tree, version). | `references/uv.md` | Safe Workflow Checklist | `[ref: #uv-safe-workflow-checklist]` |

## 3. Execution Mandates
1. **ruplacer**: You MUST perform a dry run (omit `--go`) first. Review stdout before executing actual writes. No exceptions.
2. **ruff**: You MUST run `ruff check` and `ruff format` after *any* Python file modification. Only fix code you modified yourself.
3. **uv**: Default to `references/uv.md` (safe mode) unless explicit package installation or lock mutation is required.
4. **tree / lsd**: You MUST limit recursion depth (e.g., `--depth 3` or `-L 3`) to avoid output flooding.

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
