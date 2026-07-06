# python-lang

Mandatory Python style and language rule skill for agents writing, editing, refactoring, and reviewing Python code.

## What this skill does

`python-lang` codifies the Google Python Style Guide plus project-specific strictures. It is consumed as Markdown documentation and is triggered automatically when `.py` or `.pyi` files are present in the workspace. The skill covers:

- Language-level rules: lint, imports, packages, exceptions, global state, nested scopes, comprehensions, iterators, generators, lambdas, conditionals, default arguments, properties, truthiness, decorators, threading, power features, modern Python, and type-annotated code.
- Style-level rules: semicolons, line length, parentheses, indentation, blank lines, whitespace, shebang, comments, docstrings, strings, files/sockets, TODOs, import formatting, statements, accessors, naming, `main`, function length, and type annotations.
- A mandatory four-step Ruff self-linting protocol after any Python file edit.

## When to use it

This skill is loaded automatically when the workspace contains `.py` or `.pyi` files, or when the request explicitly involves Python, Ruff, or `uv`.

## Repository layout

```text
python-lang/
├── references/           # Language and style rule references
│   ├── 01_language_rules.md
│   └── 02_style_rules.md
└── SKILL.md              # Skill entry point, triggers, and self-linting protocol
```

## How to use this skill

1. Open `SKILL.md` for the compliance preamble, lazy-load index, and self-linting protocol.
2. Match the current task to a section in the routing index.
3. Extract only the relevant `[ref: #...]` section from `references/01_language_rules.md` or `references/02_style_rules.md`.
4. Apply the rules to the Python code under review or edit.
5. After any Python file modification, run the four-step Ruff protocol:
   - `ruff check .`
   - `ruff check --fix .`
   - `ruff format .`
   - `ruff check .` again to confirm a clean state.

## Reference index

| File | Sections |
|------|----------|
| `references/01_language_rules.md` | 1.1 Lint — 1.21 Type Annotated Code |
| `references/02_style_rules.md` | 2.1 Semicolons — 2.19 Type Annotations |

Key topics include:

- Imports and package layout.
- Exceptions and error handling.
- Comprehensions and generator expressions.
- Default argument values and mutable defaults.
- Properties and descriptors.
- Threading and concurrency.
- Modern Python 3.10+ generic types (`list[int]`, `X \| None`).
- `from __future__ import annotations` for forward declarations.
- Line length, indentation, and blank-line rules.
- Google-style docstrings (PEP 257).
- Naming conventions.
- Type annotations and import style.

## Conventions

- `SKILL.md` is the single entry point.
- Requirement verbs follow RFC 2119 / RFC 8174 (BCP 14).
- Ruff is the mandatory linter and formatter; `black`, `flake8`, and `isort` are not used.
- `uv` is the mandatory Python project tool; `pip`, `poetry`, and `virtualenv` are not used.
- Only fix code that you modified yourself.
