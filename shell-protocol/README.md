# shell-protocol

Mandatory CLI tooling conventions for this agent workspace.

## What this skill does

`shell-protocol` replaces legacy UNIX utilities with modern, high-performance alternatives and provides a routing table so agents know which reference section to extract for a given filesystem, search, replacement, or Python-ecosystem task. It governs:

- Core filesystem and search tools.
- Bulk code replacement.
- Python ecosystem tooling.
- Tool-specific recipes for agents.

The skill contains no executable code; it is a prose guidance module consumed by the agent prompt system.

## When to use it

This skill is loaded automatically (`triggers: always: true`) because every file/code operation uses CLI tools.

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
└ SKILL.md                # Entry point, tool-replacement rules, and routing table
```

## Mandatory tool replacements

| Legacy tool | Modern replacement |
|-------------|-------------------|
| `ls` | `lsd` |
| `find` | `fd` |
| `grep` | `rg` (ripgrep) |
| `sed` (bulk symbol replaces) | `ruplacer` |
| `pip`, `poetry`, `virtualenv` | `uv` |
| `black`, `flake8`, `isort` | `ruff` |

## How to use this skill

1. Open `SKILL.md` for the tool-replacement rules and master routing table.
2. Match the task to a routing-table entry.
3. Extract the relevant `[ref: #...]` section from the target reference file using `rg`.
4. Execute the command using the modern tool.
5. Verify the output and confirm no unmodified files were changed.

## Reference index

| File | Topic |
|------|-------|
| `references/tree.md` | Directory-tree visualization |
| `references/lsd.md` | Directory listing with sizes, permissions, git status |
| `references/fd-find.md` | Finding files by name, extension, type, size, modified time |
| `references/ripgrep.md` | Searching text/code inside files; finding imports/usages |
| `references/ruplacer.md` | Bulk find/replace with mandatory dry-run-first rule |
| `references/ruff.md` | Python linting and formatting |
| `references/uv.md` | Safe, read-only `uv` command subset |
| `references/uv-full.md` | Complete `uv` command reference |

## Core execution mandates

- **`ruplacer`**: perform a dry run (omit `--go`) first, review stdout, then execute writes.
- **`ruff`**: run `ruff check` and `ruff format` after any Python file modification; only fix code you modified.
- **`uv`**: prefer the safe workflow (`uv run --no-sync`, `--frozen`, `--locked`) unless explicit package installation or lock mutation is required.
- **`tree` / `lsd`**: limit recursion depth (e.g., `--depth 3` or `-L 3`) to avoid output flooding.

## Conventions

- `SKILL.md` begins with a YAML frontmatter block declaring `name`, `description`, and `triggers: always: true`.
- Reference files use `[ref: #...]` anchors for lazy extraction.
- Agents are forbidden from reading full reference manuals; they must extract only the relevant section.
