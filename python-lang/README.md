# python-lang

Enforces strict Python language and style rules based on the Google Python Style Guide and Ruff.

## What it does

This skill governs how Python code is written, edited, refactored, and reviewed in the project.
It covers language-level rules such as imports, packages, exceptions, comprehensions, generators, decorators, threading, type annotations, and modern Python idioms.
It also covers style-level rules such as line length, indentation, whitespace, comments, docstrings, naming, and function length.
After every edit, the agent unconditionally runs a mandatory two-stage Ruff pipeline (`ruff format` + `ruff check`) on every file it wrote or edited — independently of any project-level linting — and restores any foreign code the formatter touched.

## When it activates

Activates automatically when the project contains `.py` or `.pyi` files.

Example prompts:

- "Refactor this module to use dataclasses."
- "Add type annotations to the payment service."
- "Review my Python code for style issues."
- "Write a pytest fixture for this test suite."

## How to use it

Ask the agent to write, edit, refactor, or review Python code.
The agent checks the relevant language and style rules, respects local file consistency, and runs Ruff on the files it changed.
You do not need to configure Ruff or invoke it yourself.

If the project root contains a `.sdk/` directory, the agent also checks for reusable components before writing new code.

## What it produces

- Python code that follows the project style guide.
- Ruff-clean, black-compatibly formatted files scoped to the agent's own changes, with foreign code restored byte-identical.
- Optional reuse of existing `.sdk/` components.

## Repository layout

```text
python-lang/
├── references/           # Language and style rule references
│   ├── 01_language_rules.md
│   └── 02_style_rules.md
└── SKILL.md              # Agent entry point: manifest, triggers, and routing index
```

## Reference overview

| File | What it covers |
|------|----------------|
| `references/01_language_rules.md` | Lint, imports, packages, exceptions, mutable global state, nested classes, comprehensions, iterators, generators, lambdas, conditional expressions, default arguments, properties, truthiness, lexical scoping, decorators, threading, power features, modern Python, and type-annotated code. |
| `references/02_style_rules.md` | Semicolons, line length, parentheses, indentation, blank lines, whitespace, shebang, comments and docstrings, strings, files and sockets, TODO comments, import formatting, statements, accessors, naming, main entry points, function length, and type annotations. |

## Important conventions / gotchas

- Requires the `read-for-comments` skill automatically for RFC 2119 / RFC 8174 verb semantics.
- Ruff is the mandatory linter and formatter; `black`, `flake8`, and `isort` are not used.
- `uv` is the mandatory Python project tool; `pip`, `poetry`, and `virtualenv` are not used.
- The agent formats and fixes only code it explicitly modified, ignores pre-existing violations in untouched code, and reverts any formatter hunks that bleed into foreign lines so foreign code returns byte-identical to its prior state.
- All timestamps use UTC ISO 8601 format.
