# python-lang
[ref: #py-intro]

Mandatory Python language and style rules based on the Google Python Style Guide and Ruff.

## What it does
[ref: #py-what]

This skill enforces strict Python engineering in the codebase. It mandates type annotations, explicit visibility via naming, modern dependency and environment management, and a Ruff-based format and lint pipeline. It also forbids older tools such as `pip`, `poetry`, `black`, `flake8`, and `isort` in favor of `uv` and `ruff`.

## When it activates
[ref: #py-when]

Activates whenever the agent writes, edits, refactors, or reviews Python code, modules, packages, classes, functions, type annotations, imports, exceptions, comprehensions, decorators, or docstrings.

Examples:

- "Refactor this Python module."
- "Add a Python API client."
- "Fix this function's type annotations."
- "Review the Python code."

## How to run / use it
[ref: #py-how]

The skill applies automatically as the agent edits Python files. The Ruff pipeline is unconditional and scoped strictly to files you touched:

```bash
uvx ruff format <changed_files>
uvx ruff check --fix --target-version <PYVER> <changed_files>
uvx ruff check --target-version <PYVER> --diff <changed_files>
```

`<changed_files>` is the explicit list of files you wrote or edited; never run the pipeline against the whole project or a directory. Determine `<PYVER>` with:

```bash
uv run python -c "import sys; print(f'py{sys.version_info.major}{sys.version_info.minor}')"
```

Reusable SDK utilities live under `.sdk/sdk/` and should be imported instead of reinvented.

## What it produces
[ref: #py-produces]

- Consistent, formatted Python code that passes `ruff`.
- Type annotations and docstrings aligned with the Google style.
- Minimal, correct imports.
- No forbidden toolchain usage.

## Dependencies and why they matter
[ref: #py-deps]

- `frontmatter-protocol` — provides the lazy-load routing used to consume the `references/` corpus.
- `read-for-comments` — archives the RFC 2119/8174 normative-keyword standards that govern the skill's requirement-level language.
- `.sdk/sdk/` — in-project reusable Python components shared across skills.

## Strengths and trade-offs
[ref: #py-tradeoffs]

### Strong sides
[ref: #py-strong]

- Modern, opinionated toolchain reduces bike-shedding.
- Ruff is fast and unified; one tool replaces black, flake8, isort, and many plugins.
- Strong typing and explicit visibility make large codebases easier to maintain.
- Reusable `.sdk/sdk/` components avoid duplication.

### Weak sides / limits
[ref: #py-weak]

- Assumes `uv` and `ruff` are installed and configured.
- Migrating an existing project can require a large reformatting pass.
- Some legacy patterns are forbidden even when they would be expedient.

### Common pitfalls / gotchas
[ref: #py-pitfalls]

- Never use `pip`, `poetry`, `black`, `flake8`, `isort`, `pyflakes`, `pycodestyle`, `pylint`, or `autopep8`.
- Always run `ruff format` and `ruff check --fix` on files you touch.
- Prefer absolute imports inside packages and relative imports only within a single module.
- Use `typing.Self` and modern generics; avoid `from __future__ import annotations` tricks.
- Do not put production logic in `__init__.py`.

## Repository layout
[ref: #py-layout]

```text
python-lang/
├── prompts/              # Generation and review prompts
├── references/           # Google Python Style Guide excerpts and cheat sheets
├── README.md                # Human overview (this file)
└── SKILL.md              # Agent entry point: rules, forbidden tools, and routing index
```

## Important conventions / gotchas
[ref: #py-conventions]

- Every Python file you touch must be formatted and linted with `ruff`.
- Target the Python version declared in `pyproject.toml` or `.python-version`.
- Use `uv run python` for script execution and dependency management.
- Prefer `.sdk/sdk/` utilities over inline reinvention.
- Follow the Google Python Style Guide for docstrings, naming, and structure.
