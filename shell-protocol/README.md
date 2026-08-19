# mandatory-tools
[ref: #mandatory-tools]

Defines the modern CLI toolkit the agent uses when it works with files, search, and Python projects.

## What it does
[ref: #shell-what-it-does]

This skill is the agent's tool-selection layer for filesystem and Python work. It replaces slow, verbose legacy UNIX utilities with fast, modern equivalents and adds safety hygiene such as dry-run-first bulk replacements and automatic Python linting after edits. The moving parts are a hard replacement table, a routing index into per-tool reference cards, and execution mandates that apply after every relevant tool call.

## When it activates
[ref: #shell-when-it-activates]

No action is needed — it is loaded automatically in every session.

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

## How to run / use it
[ref: #shell-how-to-run-use-it]

You do not configure the skill directly. Just describe the file or code operation you want, and the agent routes it to the right tool.

What the agent does automatically:

- Maps your request to `lsd`, `fd`, `rg`, `ruplacer`, `uv`, or `ruff` instead of legacy tools.
- Runs a `ruplacer` dry run before any bulk write and asks you to review the preview.
- Runs `ruff check` and `ruff format` after any Python file change, scoped to what it actually touched.
- Limits directory-tree depth to avoid flooding the context.

What a human must ensure:

- The modern tools are installed and on `PATH`. On most developer machines they are already present; if one is missing, the agent will tell you which command failed.
- For `ruplacer` renames, confirm the dry-run output before the agent applies the change.

## What it produces
[ref: #shell-what-it-produces]

- Consistent tool selection across every session.
- Safe bulk edits via dry-run-first replacement.
- Cleaner Python code through `ruff check` and `ruff format`.
- Manageable directory listings with depth limits.
- Lazy-loaded reference cards that keep detailed flags and recipes out of the main context until they are needed.

## Dependencies and why they matter
[ref: #shell-dependencies-and-why-they-matter]

| Dependency | Why it matters |
|---|---|
| `frontmatter-protocol` | Skill headers and reference-card routing are frontmatter-driven; this protocol is the shared loader and schema authority. |
| `lsd` | Modern, colorized, git-aware directory listings that replace `ls`. |
| `fd` | Fast, user-friendly file search that replaces `find`. |
| `rg` (ripgrep) | Fast text and symbol search that replaces `grep`. |
| `ruplacer` | Safe, multi-file find/replace that replaces `sed` for bulk edits. |
| `uv` | Modern Python project and dependency management that replaces `pip`, `poetry`, and `virtualenv`. |
| `ruff` | Unified Python linter and formatter that replaces `black`, `flake8`, and `isort`. |
| `tree` | Hierarchical directory visualization used with a depth limit. |

## Strengths and trade-offs
[ref: #shell-strengths-and-trade-offs]

- **Strong sides:** Speed, token efficiency, consistent safety habits, and a single routing table that every agent session follows.
- **Weak sides / limits:** Assumes the modern toolchain is installed; it does not teach legacy-tool workflows; non-Python ecosystems are covered only indirectly.
- **Common pitfalls / gotchas:** Do not ask the agent to use `ls`, `find`, `grep`, `sed`, `pip`, or `black` — those paths are explicitly forbidden. Bulk replacements without a dry run are also forbidden. The agent may refuse to run a command that would change unmodified files.

## Repository layout
[ref: #shell-repository-layout]

```text
mandatory-tools/
├── references/           # Per-tool reference manuals with lazy-load anchors
│   ├── fd-find.md
│   ├── lsd.md
│   ├── ripgrep.md
│   ├── ruff.md
│   ├── ruplacer.md
│   ├── tree.md
│   ├── uv-full.md
│   └── uv.md
├── README.md                # Human overview (this file)
└── SKILL.md              # Agent entry point: tool-replacement rules and routing index
```

## Reference overview
[ref: #shell-reference-overview]

| File | What it covers |
|---|---|
| `references/fd-find.md` | Finding files by name, extension, type, size, and modified time |
| `references/lsd.md` | Colorized directory listings and git-aware displays |
| `references/ripgrep.md` | Searching text and symbols inside files |
| `references/ruff.md` | Linting and formatting Python code |
| `references/ruplacer.md` | Bulk find/replace with dry-run safety |
| `references/tree.md` | Directory-tree visualization |
| `references/uv.md` | Safe, read-only `uv` commands |
| `references/uv-full.md` | Complete `uv` command reference |

## Important conventions / gotchas
[ref: #shell-important-conventions-and-gotchas]

- This skill governs tool selection, not Python language rules; for full Python style guidance use the `python-lang` skill.
- The agent always performs a `ruplacer` dry run before writing.
- The agent runs `ruff check` and `ruff format` after any Python file change.
- Directory listings and tree views are limited in depth to avoid flooding the context.
- Skill files are read from `.kimi/mirror/` first so every agent sees the same committed version.
- `ReadFile` is scoped to the working directory; genuinely external files must be verified with a shell command before reading.
