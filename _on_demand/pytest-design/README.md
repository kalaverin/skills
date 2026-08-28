# pytest-design
[ref: #ptd-intro]

Mandatory rules for writing, editing, running, and reviewing Python tests with pytest.

## What it does
[ref: #ptd-what]

This skill defines how the agent creates pytest-based unit and integration tests. It enforces clean fixture design, isolation, deterministic behavior, and a strict no-legacy rule set: no `unittest`, no `mock` for external APIs, and no real network in unit tests. Tests are written in plain pytest with `pytest` idioms, arranged by domain, and run with the correct interpreter and dependencies.

## When it activates
[ref: #ptd-when]

Activates whenever the agent writes, edits, runs, or reviews Python unit tests, integration tests, fixtures, `conftest.py`, parametrization, markers, mocks, async tests, or pytest plugins.

Examples:

- "Add unit tests for this module."
- "Review the pytest suite."
- "Create fixtures for the database."
- "Run tests with coverage."

## How to run / use it
[ref: #ptd-how]

Tests are written with pytest and run through `uv`:

```bash
uv run pytest
uv run pytest -q
uv run pytest -x
uv run pytest --cov=src --cov-report=term-missing
```

Use markers for slow, network, integration, or property-based tests.
Put shared fixtures in `conftest.py` files located near the tests that use them.
Mock external services with `responses` or `respx`, not `unittest.mock`.

## What it produces
[ref: #ptd-produces]

- Fast, deterministic pytest suites.
- Clean fixtures that are easy to reuse and reason about.
- Parametrized tests where appropriate.
- Separate integration tests that require real resources.

## Dependencies and why they matter
[ref: #ptd-deps]

- `python-lang` — provides the underlying Python style rules.
- `frontmatter-protocol` — provides the lazy-load routing for the `references/` corpus.
- `pytest-planner` consumes this skill when generating repo-specific test plans.
- `pytest`, `pytest-asyncio`, `responses`, `respx`, `freezegun`, `faker` — modern pytest ecosystem.

## Strengths and trade-offs
[ref: #ptd-tradeoffs]

### Strong sides
[ref: #ptd-strong]

- Plain pytest is simpler and more flexible than `unittest`.
- Strong isolation rules keep unit tests fast and deterministic.
- Shared fixtures reduce boilerplate.
- Clear separation between unit and integration tests.

### Weak sides / limits
[ref: #ptd-weak]

- Requires discipline to avoid leaking state between tests.
- Async and database tests need extra care and markers.
- Rewriting legacy `unittest` suites is manual work.

### Common pitfalls / gotchas
[ref: #ptd-pitfalls]

- Do not use `unittest.TestCase`, `unittest.mock`, `mock`, `nose`, or `doctest`.
- Never call real external APIs from unit tests; use `responses` / `respx`.
- Avoid broad `autouse=True` fixtures; prefer explicit fixtures.
- Do not share mutable state via module-level variables.
- Parametrize edge cases and boundary conditions, not happy paths only.

## Repository layout
[ref: #ptd-layout]

```text
_on_demand/pytest-design/
├── assets/               # Example test fixtures and reference snippets
├── prompts/              # Test-generation prompts
├── references/           # Detailed pytest guidance and anti-patterns
├── README.md                # Human overview (this file)
└── SKILL.md              # Agent entry point: rules, markers, fixtures, and routing index
```

## Reference overview
[ref: #ptd-refs]

| Path | What it covers |
|---|---|
| `references/required/*.md` | Core pytest rules: fixtures, isolation, markers, mocking, parametrization, assertions, exceptions, faker, temporary files, time control, skip/xfail, pyproject config, and testing practices. |
| `references/optional/*.md` | Optional and advanced topics: async, database mocking, CLI testing, logging, patterns, performance, xdist, assertion plugins, postgres, reporting, version-specific guidance, internals, and warning testing. |

## Important conventions / gotchas
[ref: #ptd-conventions]

- Run tests with `uv run pytest`.
- Use markers for slow, integration, network, and property-based tests.
- Place shared fixtures in `conftest.py` near the consumers.
- Mock HTTP with `responses` (sync) or `respx` (async).
- Integration tests may require real resources; mark them clearly and run them separately.
