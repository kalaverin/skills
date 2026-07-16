# shell-protocol

Defines the modern CLI toolkit the agent uses when it works with files, search, and Python projects.

## What it does

This skill replaces legacy UNIX utilities with fast, modern alternatives.
It tells the agent to use `lsd` instead of `ls`, `fd` instead of `find`, `rg` instead of `grep`, `ruplacer` instead of `sed` for bulk replacements, `uv` instead of `pip`/`poetry`/`virtualenv`, and `ruff` instead of `black`/`flake8`/`isort`.
It also ships tool-specific recipes so the agent picks the right flags for listing, searching, replacing, linting, formatting, and dependency management.

## When it activates

No action needed — loaded automatically in every session.

It applies whenever you ask the agent to:

- list directory contents
- search the filesystem by name, extension, or type
- grep or search text inside files
- lint or format Python code
- replace text across multiple files
- run Python tools or manage dependencies

Example prompts:

- "List the top-level files in this repo."
- "Find all Python files that import `temporalio`."
- "Search for `TODO` across the codebase."
- "Format and lint the changed Python files."
- "Replace `old_name` with `new_name` everywhere."

## How to use it

You do not need to configure anything.
Just ask the agent for the file or code operation you want.
The skill will route the request to the modern tool and apply safety rules, such as running a dry run before a `ruplacer` write and running `ruff` after Python edits.

## What it produces

- Consistent tool selection across every session.
- Safe bulk edits via dry-run-first replacement.
- Cleaner Python code through `ruff check` and `ruff format`.
- Manageable directory listings with depth limits.

## Repository layout

```text
shell-protocol/
├── references/           # Per-tool reference manuals with lazy-load anchors
│   ├── fd-find.md
│   ├── lsd.md
│   ├── ripgrep.md
│   ├── ruff.md
│   ├── ruplacer.md
│   ├── tree.md
│   ├── uv-full.md
│   └── uv.md
└── SKILL.md              # Agent entry point: tool-replacement rules and routing index
```

## Reference overview

| File | What it covers |
|------|----------------|
| `references/fd-find.md` | Finding files by name, extension, type, size, and modified time |
| `references/lsd.md` | Colorized directory listings and git-aware displays |
| `references/ripgrep.md` | Searching text and symbols inside files |
| `references/ruff.md` | Linting and formatting Python code |
| `references/ruplacer.md` | Bulk find/replace with dry-run safety |
| `references/tree.md` | Directory-tree visualization |
| `references/uv.md` | Safe, read-only `uv` commands |
| `references/uv-full.md` | Complete `uv` command reference |

## Important conventions / gotchas

- This skill governs tool selection, not Python language rules; for full Python style guidance use the `python-lang` skill.
- The agent always performs a `ruplacer` dry run before writing.
- The agent runs `ruff check` and `ruff format` after any Python file change.
- Directory listings and tree views are limited in depth to avoid flooding the context.
