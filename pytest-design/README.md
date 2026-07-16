# pytest-design

Makes the agent write, edit, run, and review pytest suites the same way your project expects.

## What it does

This skill encodes the project's pytest engineering standards.
It turns ad-hoc test generation into consistent, maintainable pytest code.
It solves flakiness caused by shared state, hardcoded test data, unverified Faker calls, and duplicate fixtures.
It also provides recipes for fixtures, parametrization, markers, mocking, async tests, database substitutions, CLI testing, logging capture, and parallel execution.

## When it activates

Activates when the project contains Python or TOML files and you ask about testing, or when you mention pytest-related topics.

Examples of prompts that trigger it:

- "Write unit tests for the billing module."
- "Add integration tests for the payment webhook handler."
- "Review our pytest suite for missing isolation."
- "Create fixtures for user accounts and orders."
- "Parametrize these tests for each supported currency."
- "Add async tests for the notification worker."

## How to use it

Ask the agent to write, refactor, or review tests for a Python project.
The agent inspects the production code, existing `tests/` tree, and `conftest.py` hierarchy before writing anything.
It generates isolated tests that use Faker for all data, avoid `print()` and `time.sleep()`, and clean up every monkeypatch.
It runs the mandatory Ruff verification protocol only on the files it changed.
You can give it additional constraints, such as "use SQLite instead of PostgreSQL in tests" or "keep coverage above 60%".

## What it produces

- New or updated test files under `tests/`.
- New or updated `conftest.py` files and factory fixtures.
- Parametrized tests, markers, and skip/xfail annotations.
- Mocking and isolation boundaries for external I/O.
- Ruff-clean code that targets the project's Python version.

## Repository layout

```text
pytest-design/
├── references/           # Recipe cards for specific pytest topics
│   ├── required/         # Universal baseline recipes
│   │   ├── data_assertions.md
│   │   ├── exceptions.md
│   │   ├── faker.md
│   │   ├── fixtures.md
│   │   ├── isolation.md
│   │   ├── markers.md
│   │   ├── mocking.md
│   │   ├── parametrization.md
│   │   ├── pyproject.md
│   │   ├── skip_xfail.md
│   │   ├── temporary_files.md
│   │   ├── testing_practices.md
│   │   └── time_control.md
│   └── optional/         # Situational or advanced recipes
│       ├── assertion_plugins.md
│       ├── asyncio.md
│       ├── capture_fixtures.md
│       ├── cli_testing.md
│       ├── database_mocking.md
│       ├── frameworks.md
│       ├── internals.md
│       ├── logging.md
│       ├── patterns.md
│       ├── performance.md
│       ├── postgres.md
│       ├── reporting.md
│       ├── version_specific.md
│       ├── warning_testing.md
│       └── xdist.md
├── assets/               # Reusable templates such as Faker and PostgreSQL fakes
├── prompts/              # Helpers for authoring new reference cards
└── SKILL.md              # Agent entry point: manifest, triggers, and routing index
```

## Reference overview

| File | What it covers |
|------|----------------|
| `references/required/data_assertions.md` | Comparing test data without flakiness or opaque failures |
| `references/required/exceptions.md` | Asserting error contracts with `pytest.raises` and `ExceptionInfo` |
| `references/required/faker.md` | Generating realistic, deterministic test data with Faker |
| `references/required/fixtures.md` | Organizing reusable test dependencies and `conftest.py` layout |
| `references/required/isolation.md` | Keeping tests independent of shared, mutable, external state |
| `references/required/markers.md` | Categorizing tests and steering selection or CI |
| `references/required/mocking.md` | Picking the lightest double and isolating boundaries |
| `references/required/parametrization.md` | Scaling coverage while shrinking test code |
| `references/required/pyproject.md` | Centralizing pytest configuration in `pyproject.toml` |
| `references/required/skip_xfail.md` | Managing test exclusion and expected failure |
| `references/required/temporary_files.md` | Creating isolated, reproducible filesystem fixtures |
| `references/required/testing_practices.md` | Baseline style for concise, high-quality tests |
| `references/required/time_control.md` | Making time-dependent tests deterministic |
| `references/optional/assertion_plugins.md` | Extending plain `assert` for awkward comparisons |
| `references/optional/asyncio.md` | Writing reliable async tests |
| `references/optional/capture_fixtures.md` | Capturing stdout, stderr, and logs without `-s` |
| `references/optional/cli_testing.md` | Exercising command-line interfaces in tests |
| `references/optional/database_mocking.md` | Choosing the lightest realistic database backend |
| `references/optional/frameworks.md` | Testing Django, FastAPI, and Flask |
| `references/optional/internals.md` | Extending pytest itself with hooks, stashes, and plugins |
| `references/optional/logging.md` | Asserting logged events and structured output |
| `references/optional/patterns.md` | Reusable recipes for awkward test constructs |
| `references/optional/performance.md` | Keeping suites fast and detecting regressions |
| `references/optional/postgres.md` | Substituting PostgreSQL with SQLite for fast SQLAlchemy 2.0 tests |
| `references/optional/reporting.md` | Producing human and machine test evidence |
| `references/optional/version_specific.md` | Exercising modern Python in tests |
| `references/optional/warning_testing.md` | Proving warning behavior |
| `references/optional/xdist.md` | Parallelizing with `pytest-xdist` |

## Important conventions / gotchas

- Requires `python-lang` to be active and only applies to Python 3.12+ projects.
- It does not apply to non-Python test frameworks.
- All test data must come from Faker with specific, verified provider methods; hardcoded values are forbidden.
- The standard-library `random` module is forbidden outside the Faker seed fixture.
- Every test must be isolated; shared mutable state and leaked side effects are critical failures.
- The agent must check the existing `conftest.py` hierarchy before creating a new fixture to avoid duplicates.
- The agent runs Ruff only on files it modified; it ignores warnings in untouched code.
