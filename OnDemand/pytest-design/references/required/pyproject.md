---
subject: "Centralize pytest config in `pyproject.toml`: native `[tool.pytest]` (pytest ≥9.0) vs legacy `[tool.pytest.ini_options]`, set `minversion`/`testpaths`/`pythonpath`/`addopts`(as a TOML list)/`markers`/`filterwarnings`(`'error'` first)/`required_plugins`/`norecursedirs`/`xfail_strict`/`console_output_style`, coverage under `[tool.coverage.*]`, and xdist `-n=auto --dist=loadfile` only after isolation; plugin keys only for installed plugins."
index:
  - anchor: pyproject-config-format-policy
    what: "Keeping all pytest configuration in `pyproject.toml` under `[tool.pytest]` or `[tool.pytest.ini_options]` as the single source of truth."
    problem: "Scattering pytest settings across ini, tox, cfg fragments runner config and hides it from one discoverable file; single source, one file, no legacy ini, discoverable config, modern packaging, no setup cfg."
    use_when: "Pytest settings scatter across ini tox cfg fragments, runner config hides, and one discoverable file should own them; single source, one file, no legacy ini, discoverable config, modern packaging, no setup cfg, pyproject."
    avoid_when: "Do NOT create or maintain `pytest.ini`, `tox.ini`, or `setup.cfg` for pytest settings."
    expected: "All pytest config lives in one `pyproject.toml`, discoverable from a single file, with no legacy INI/CFG files for the runner."
  - anchor: pyproject-tool-pytest-vs-ini-options
    what: "Choosing between the native TOML table `[tool.pytest]` (pytest >=9.0, real TOML types) and the legacy `[tool.pytest.ini_options]` table (INI-style string coercion)."
    problem: "Older pytest cannot parse native table, while legacy table forces string coercion for lists and booleans; native table, ini options, version floor, real toml types, string coercion, minimum version."
    use_when: "Project supports older pytest, native table may not parse, and legacy table forces string coercion for lists and booleans; native table, ini options, version floor, real toml types, string coercion, minimum version, pytest config."
    avoid_when: "Do not use the native `[tool.pytest]` table when the project must support pytest <9.0, and do not keep INI string quoting once the minimum version crosses 9.0."
    expected: "The table matches the project's minimum pytest, with native TOML types on >=9.0 and legacy coercion only when required."
  - anchor: pyproject-core-options
    what: "The bootstrap set (`minversion`, `testpaths`, `pythonpath`, `addopts`, `markers`, `filterwarnings`, `required_plugins`, `norecursedirs`, `xfail_strict`, `console_output_style`) that gives deterministic collection, safe defaults, and fast failure."
    problem: "Without core options, collection wanders, missing plugins fail late, and XPASS results silently pass; scoped collection, required plugins fail fast, xfail strict, deterministic, console style, no wander."
    use_when: "Collection wanders without core options, missing plugins fail late, and XPASS results silently pass unless strict defaults exist; scoped collection, required plugins fail fast, xfail strict, deterministic, console style, no wander, core options."
    avoid_when: "Do not rely on defaults for collection scope or plugin presence (use `testpaths`/`required_plugins`), and do not let XPASS pass (set `xfail_strict = true`)."
    expected: "Collection is scoped and deterministic, mandatory plugins fail fast when missing, and XPASS results fail the build."
  - anchor: pyproject-addopts
    what: "Prefer a TOML list for `addopts` (each option a separate element, spaces handled); typical flags `-ra`, `--strict-markers`, `--strict-config`, `--timeout=60`, `--tb=short`, `--randomly-seed=auto`, `-n=auto`, `--dist=loadfile`."
    problem: "Single string addopts mishandles spaces; coverage thresholds belong in CI, not default runner invocation; toml list, strict markers config, short traceback, randomized seed, xdist default, no fail_under."
    use_when: "Single addopts string mishandles spaces, coverage thresholds belong in CI, and TOML list keeps strict marker config and seed defaults; toml list, strict markers config, short traceback, randomized seed, xdist default, no fail under, addopts."
    avoid_when: "Do not set a coverage `fail_under` in `addopts` (enforce thresholds in CI), and do not use a single space-delimited string when a list is clearer."
    expected: "`addopts` is a clean TOML list of runner flags; coverage thresholds are enforced in CI, not in the default invocation."
  - anchor: pyproject-markers
    what: "Registering every custom marker in the `markers` array and including `--strict-markers` in `addopts` so typos become collection errors."
    problem: "Unregistered markers are silently ignored, so typo in marker name skips tests without warning; register every, strict markers, description, naming prefix, typo fails collection, no unused marker."
    use_when: "Custom marker typo skips tests silently, unregistered marker gives no warning, and strict markers turn typos into collection errors; register every, strict markers, description, naming prefix, typo fails collection, no unused marker, marker config."
    avoid_when: "Do not register markers that are not actually used, and do not rely on marker auto-discovery (unregistered markers fail under `--strict-markers`)."
    expected: "Every marker in use is registered and described, and a misspelled marker fails collection instead of silently skipping tests."
  - anchor: pyproject-filterwarnings
    what: "The `filterwarnings` list applied top-down, with `error` first to turn unexpected warnings into failures and targeted `ignore::...` entries for known third-party noise."
    problem: "Broad ignore placed before error suppresses warnings meant to catch, while no filter lets warning debt accumulate silently; error first, targeted ignore, third-party noise, drive to error, no broad ignore, warning policy."
    use_when: "Broad ignore before error suppresses useful warnings, no filter lets debt accumulate, and targeted ignores silence known third party noise; error first, targeted ignore, third party noise, drive to error, no broad ignore, warning policy."
    avoid_when: "Never place a broad ignore before `error` (it suppresses warnings you intended to catch), and do not leave the suite without a warning policy."
    expected: "Unexpected warnings fail the build, only known third-party noise is ignored, and warning debt is driven down toward `error`."
  - anchor: pyproject-plugin-specific-options
    what: "Plugin keys (e.g. `asyncio_mode = 'strict'`, `asyncio_default_fixture_loop_scope = 'function'`, `timeout = 60`) declared in the same pytest table, only for installed/required plugins."
    problem: "Enabling options for missing plugin is silently ignored or confusing, while undeclared plugins leave async and timeout behavior unspecified; installed only, required plugins, fail fast, clear message, same table, no silent ignore."
    use_when: "Plugin option belongs only to installed or required plugin, missing plugin option is ignored, and async timeout behavior must stay specified; installed only, required plugins, fail fast, clear message, same table, no silent ignore, plugin keys."
    avoid_when: "Do not enable plugin options for plugins that are not installed — add the plugin to `required_plugins` so the runner fails fast with a clear message."
    expected: "Every configured plugin key has a corresponding installed/required plugin, and missing plugins fail fast rather than being silently ignored."
  - anchor: pyproject-logging-options
    what: "Sparingly used logging keys (`log_cli`, `log_cli_level`, `log_format`, `log_cli_format`, `log_date_format`), with `caplog` preferred in tests over default console output."
    problem: "Enabling log cli by default floods output, and print in tests bypasses capture machinery; caplog preferred, log cli off default, raise level env, no print, temporary diagnosis, capture fixture."
    use_when: "Default log cli floods output, print bypasses capture machinery, and caplog remains preferred inside tests; caplog preferred, log cli off default, raise level env, no print, temporary diagnosis, capture fixture, logging options."
    avoid_when: "Avoid `log_cli` by default, and do not add `print()` calls to tests — use `capsys`, `capfd`, or `caplog`."
    expected: "Tests assert logs via `caplog`, console logging is off by default, and live output is enabled only temporarily for diagnosis."
  - anchor: pyproject-coverage-configuration
    what: "Coverage settings under `[tool.coverage.run]` (`source`, `branch`, `concurrency`, `omit`) and `[tool.coverage.report]` (`fail_under`, `show_missing`, `exclude_lines`), bridged to pytest via `pytest-cov>=5.0`."
    problem: "Coverage thresholds and report settings do not belong in pytest addopts, and line-only coverage masks missing branch paths; own tables, branch coverage, enforce in ci, never in addopts, fail_under goal, source omit."
    use_when: "Coverage thresholds and report settings do not belong in addopts, line only coverage masks branches, and own tables enforce CI gate; own tables, branch coverage, enforce in ci, never in addopts, fail under goal, source omit."
    avoid_when: "Do not place coverage thresholds or report settings inside `addopts`, and do not treat `fail_under` as an agent constraint on every local run (it is a project goal)."
    expected: "Coverage is configured in its own tables with branch coverage, enforced in CI, and never encoded in pytest `addopts`."
  - anchor: pyproject-xdist-options
    what: "Adding `-n auto` and `--dist=loadfile` to `addopts` for `pytest-xdist` parallel execution, gated on proven test isolation."
    problem: "Parallel runs amplify any shared mutable state or fixture-ordering bug into flaky, hard-to-reproduce failures; after isolation, loadfile, coverage source, random seed, order leak, one worker per cpu."
    use_when: "Parallel options amplify shared mutable state and ordering bugs, isolation proof must come first, and coverage source plus random seed surface leaks; after isolation, loadfile, coverage source, random seed, order leak, one worker per cpu, xdist options."
    avoid_when: "Do not enable xdist before fixing shared mutable state or fixture-ordering bugs."
    expected: "Parallel execution runs one worker per CPU with whole-file distribution, and only after the suite is provably isolated and order-independent."
  - anchor: pyproject-cli-options-reference
    what: "Quick reference for common flags: `-ra`, `--strict-markers`, `--strict-config`, `--tb`, `--lf`/`--last-failed`, `--ff`, `--sw`, `--randomly-seed`, `--durations`, `-k`, `-m`, `-x`, `--pdb`, `--cov`."
    problem: "Developers need fast lookup for most-used pytest CLI flags and effects when tuning addopts or iterating locally; last failed, failed first, reproduce order, durations, select subset, stop debug, flag lookup."
    use_when: "Developer tunes addopts or iterates locally, common flags need fast lookup, and failure selection reproduction durations stop debug matter; last failed, failed first, reproduce order, durations, select subset, stop debug, flag lookup, cli reference."
    avoid_when: "Do not use `--last-failed`/`--failed-first` as a substitute for fixing order-dependent failures, do not leave `--pdb` in CI invocations, and do not add a flag to `addopts` merely because it appears in the table."
    expected: "Common CLI flags are used for focused iteration, reproduction, and selection without masking underlying isolation bugs."
  - anchor: pyproject-variety-booster
    what: "Combine config defaults with composable markers so defaults themselves probe invariants: `filterwarnings = ['error']`, `--randomly-seed=auto`, `-n=auto` + `--dist=loadfile`, `--durations=10`."
    problem: "Without probing defaults, regressions hide behind warning noise, fixed order, serial state, and slow fixtures; error on warnings, randomized order, parallel loadfile, durations probe, invariant default, hidden regression."
    use_when: "Defaults hide regressions behind warning noise fixed order serial state and slow fixtures, probing defaults turn them into invariant checks; error on warnings, randomized order, parallel loadfile, durations probe, invariant default, hidden regression."
    avoid_when: "Do not leave warnings non-error, order fixed, runs serial-only, or durations unobserved — each un-probed default hides a class of regression."
    expected: "Default config options multiply coverage by surfacing warning, ordering, isolation, and performance regressions without new test cases."
libraries:
  - pytest
  - pytest-asyncio
  - pytest-benchmark
  - pytest-cov
  - pytest-env
  - pytest-randomly
  - pytest-timeout
  - pytest-xdist
---

# PYPROJECT.TOML

## Config Format Policy

[ref: #pyproject-config-format-policy]

All pytest configuration MUST live in `pyproject.toml` under `[tool.pytest]` or `[tool.pytest.ini_options]`.
Do NOT create or maintain `pytest.ini`, `tox.ini`, or `setup.cfg` for pytest settings.
Centralising configuration in `pyproject.toml` aligns the test runner with modern Python packaging standards and makes the setup discoverable from a single file.

```toml
[tool.pytest]
minversion = "9.0"
testpaths = ["tests"]
pythonpath = ["src"]
```

**Variety booster:** Keep a single source of truth by also declaring build metadata, dependency groups, and tool configurations in the same `pyproject.toml` file.

## [tool.pytest] vs [tool.pytest.ini_options]

[ref: #pyproject-tool-pytest-vs-ini-options]

Pytest 9.0 introduced the native TOML table `[tool.pytest]` alongside the legacy `[tool.pytest.ini_options]` table.
The native table supports real TOML types, so `addopts` is a list, booleans stay booleans, and `markers` is an array of strings.
The legacy table remains available for projects that must support pytest versions older than 9.0 or that rely on INI-style string coercion.

- Prefer `[tool.pytest]` for new projects when all consumers run pytest >=9.0. It supports native TOML types, so `addopts` can be a list, booleans stay booleans, and lists of markers are parsed as TOML arrays.
- Use `[tool.pytest.ini_options]` for compatibility with pytest <9 or when you must express INI-style string values, such as colon-separated `filterwarnings` entries that rely on exact INI parsing.

```toml
[tool.pytest]
minversion = "9.0"
testpaths = ["tests"]
pythonpath = ["src"]
asyncio_mode = "strict"
asyncio_default_fixture_loop_scope = "function"
addopts = [
    "-ra",
    "--strict-markers",
    "--strict-config",
    "--timeout=60",
    "--tb=short",
]
markers = [
    "unit: Tests with no external dependencies, fast (< 1s)",
    "slow: Tests taking > 1s",
    "flaky: Known unstable tests requiring retries",
    "serial: Tests that cannot run in parallel",
]
filterwarnings = [
    "error",
    "ignore::DeprecationWarning:some_third_party",
]
required_plugins = [
    "pytest-asyncio",
    "pytest-timeout",
]
norecursedirs = [".git", "node_modules", ".tox", ".venv", "build", "dist"]
xfail_strict = true
console_output_style = "progress"
```

Equivalent legacy form for pytest <9.0:

```toml
[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
pythonpath = ["src"]
asyncio_mode = "strict"
asyncio_default_fixture_loop_scope = "function"
addopts = [
    "-ra",
    "--strict-markers",
    "--strict-config",
    "--timeout=60",
    "--tb=short",
]
markers = [
    "unit: Tests with no external dependencies, fast (< 1s)",
    "slow: Tests taking > 1s",
]
filterwarnings = [
    "error",
    "ignore::DeprecationWarning:some_third_party",
]
required_plugins = [
    "pytest-asyncio",
    "pytest-timeout",
]
norecursedirs = [".git", "node_modules", ".tox", ".venv", "build", "dist"]
xfail_strict = true
console_output_style = "progress"
```

**Variety booster:** Switch a project to `[tool.pytest]` and delete INI string quoting once the minimum pytest version crosses 9.0, then rely on native boolean and array validation from TOML itself.

## Core Options

[ref: #pyproject-core-options]

A small set of core options bootstraps a quality pytest project with deterministic collection, safe defaults, and fast failure.

```toml
[tool.pytest]
minversion = "9.0"
testpaths = ["tests"]
pythonpath = ["src"]
addopts = [
    "-ra",
    "--strict-markers",
    "--strict-config",
    "--timeout=60",
    "--tb=short",
]
markers = [
    "unit: Tests with no external dependencies, fast (< 1s)",
    "slow: Tests taking > 1s",
    "flaky: Known unstable tests requiring retries",
    "serial: Tests that cannot run in parallel",
]
filterwarnings = ["error"]
console_output_style = "progress"
required_plugins = ["pytest-asyncio", "pytest-timeout", "pytest-randomly"]
norecursedirs = [".git", "node_modules", ".tox", ".venv", "build", "dist"]
xfail_strict = true
```

- `minversion` refuses to run the suite on older pytest versions.
- `testpaths` restricts collection to the listed directories.
- `pythonpath` adds the source tree to `sys.path` without requiring an editable install.
- `console_output_style` controls progress output; choose `progress`, `count`, or `classic` based on CI readability needs.
- `required_plugins` fails fast when a mandatory plugin is missing.
- `xfail_strict = true` makes any XPASS result a failure.
- `norecursedirs` prevents collection from descending into dependency or build directories.

**Variety booster:** Combine `required_plugins` with a strict `minversion` so the runner aborts immediately with a clear message instead of producing cryptic failures later in the session.

## addopts

[ref: #pyproject-addopts]

`addopts` can be a single string or a TOML list.
Prefer a list in `pyproject.toml` because each option is a separate element and spaces are handled correctly.

```toml
[tool.pytest]
addopts = [
    "-ra",                      # show all test outcomes
    "--strict-markers",         # undefined markers = error
    "--strict-config",          # unknown config = error
    "--timeout=60",             # per-test timeout
    "--tb=short",               # CI-friendly tracebacks
    "--randomly-seed=auto",     # deterministic but randomized order per run
    "-n=auto",                  # run tests in parallel via xdist
    "--dist=loadfile",          # distribute whole test files across workers
]
```

Do not set a coverage `fail_under` value in `addopts`.
Coverage is a side effect of quality tests, not the target, and the threshold should be enforced in CI rather than in the default runner invocation.

## Markers and --strict-markers

[ref: #pyproject-markers]

Custom markers MUST be registered in the `markers` array, and `--strict-markers` MUST be present in `addopts` so typos become collection errors instead of silent skips.

```toml
[tool.pytest]
markers = [
    "unit: Tests with no external dependencies, fast (< 1s)",
    "slow: Tests taking > 1s",
    "flaky: Known unstable tests requiring retries",
    "serial: Tests that cannot run in parallel",
    "integration: Tests that require external services",
]
addopts = [
    "-ra",
    "--strict-markers",
    "--strict-config",
    "--timeout=60",
    "--tb=short",
]
```

Do not register markers that are not actually used in the suite.
Do not rely on marker auto-discovery; unregistered markers fail under `--strict-markers`.

**Variety booster:** Define a naming convention for marker prefixes, such as `scope_*` for collection selectors and `needs_*` for external dependencies, so marker expressions remain self-documenting across the suite.

For a complete marker strategy, see `required/markers.md`.

## filterwarnings

[ref: #pyproject-filterwarnings]

The `filterwarnings` list is applied top-down, so place `"error"` first to turn unexpected warnings into test failures, then add targeted ignores for known third-party noise.

```toml
[tool.pytest]
filterwarnings = [
    "error",
    "ignore::DeprecationWarning:legacy_third_party",
    "ignore::PendingDeprecationWarning",
]
```

Start with `"default"` while clearing legacy warning debt, then migrate toward `"error"` as the codebase becomes warning-free.
Never place a broad ignore before `"error"` because it will suppress warnings you intended to catch.

**Variety booster:** Pair `filterwarnings = ["error"]` with a scheduled CI job that runs without ignores, so newly introduced warnings surface before they become entrenched.

## Plugin-Specific Options

[ref: #pyproject-plugin-specific-options]

Plugin-specific keys belong in the same pytest table as core options, but only include keys for plugins that are declared in `required_plugins` or project dependencies.

```toml
[tool.pytest]
asyncio_mode = "strict"
asyncio_default_fixture_loop_scope = "function"
timeout = 60
randomly_seed = "auto"
benchmark_max_time = 1.0
benchmark_min_rounds = 5
```

- `asyncio_mode = "strict"` requires every async test or fixture to be explicitly marked, preventing accidental async collection.
- `asyncio_default_fixture_loop_scope = "function"` sets the loop scope for async fixtures when no explicit scope is given.
- `timeout = 60` sets a per-test timeout through `pytest-timeout`.
- `asyncio_mode` and `asyncio_default_fixture_loop_scope` come from `pytest-asyncio`.
- `timeout` comes from `pytest-timeout`.
- `randomly_seed` comes from `pytest-randomly`.
- `benchmark_*` keys come from `pytest-benchmark`.

Do not enable plugin options for plugins that are not installed; instead, add the plugin to `required_plugins` so the runner fails fast with a clear message.

**Variety booster:** Use `asyncio_mode = "strict"` together with explicit `@pytest.mark.asyncio` markers to make async boundaries visible during code review.

## Logging Options

[ref: #pyproject-logging-options]

Logging configuration should be used sparingly; prefer the `caplog` fixture in tests instead of enabling console output by default.

```toml
[tool.pytest]
log_cli = true
log_cli_level = "INFO"
log_format = "%(asctime)s %(levelname)s %(name)s: %(message)s"
log_cli_format = "%(asctime)s %(levelname)s %(name)s: %(message)s"
log_date_format = "%Y-%m-%d %H:%M:%S"
```

Enable `log_cli` only when diagnosing a failing suite or when CI explicitly needs live output.
Do not add `print()` calls to tests; use `capsys`, `capfd`, or `caplog` instead.

**Variety booster:** Set `log_cli_level = "DEBUG"` temporarily in a failing CI job by overriding it with `PYTEST_LOG_CLI_LEVEL`, then revert to the quieter default once the incident is resolved.

## Coverage Configuration

[ref: #pyproject-coverage-configuration]

Coverage configuration lives under `[tool.coverage.run]` and `[tool.coverage.report]`, not under pytest options.
Use `pytest-cov` to bridge pytest and coverage.

```toml
[tool.coverage.run]
source = ["src"]
branch = true
concurrency = ["multiprocess"]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "*/__init__.py",
    "*/if TYPE_CHECKING:*",
]

[tool.coverage.report]
fail_under = 90
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
    "pass",
]
```

The `fail_under` threshold is a project goal, not an agent constraint on every local run.
Do not place coverage thresholds or report settings inside `addopts`.
Run coverage in CI with a command such as `pytest --cov=src --cov-report=term-missing --cov-branch --cov-fail-under=90`.

**Variety booster:** Run the full suite under `pytest-cov` with branch coverage enabled to reveal missing branch paths in conditionals that line coverage alone would mask.

## xdist Options

[ref: #pyproject-xdist-options]

Parallel execution with `pytest-xdist` can be added to `addopts` only after proving that the suite is fully isolated under parallel runs.
The same options can also be passed at the CLI instead of `addopts`.

```toml
[tool.pytest]
addopts = [
    "-ra",
    "--strict-markers",
    "--strict-config",
    "--timeout=60",
    "--tb=short",
    "-n",
    "auto",
    "--dist=loadfile",
]
```

- `-n=auto` starts one worker per CPU core.
- `--dist=loadfile` keeps an entire test file on a single worker, which reduces ordering surprises.

When running with `-n auto` and coverage, coverage is collected from subprocesses, so ensure `pytest-cov>=5.0` and a proper `[tool.coverage.run] source` configuration.
Do not enable xdist before fixing shared mutable state or fixture ordering bugs.

**Variety booster:** Run the suite with `--dist=loadfile` and `--randomly-seed=auto` together to surface both file-level isolation bugs and order-dependent state leaks.

## CLI Options Reference

[ref: #pyproject-cli-options-reference]

The following flags are commonly added to `addopts` or used at the CLI for CI-friendly defaults and focused iteration.

| Option | Purpose |
|--------|---------|
| `-ra` | Show all test outcomes, including skipped and xfailed reasons |
| `--strict-markers` | Treat unregistered markers as errors |
| `--strict-config` | Treat unknown config keys as errors |
| `--tb=short` / `--tb=long` / `--tb=line` / `--tb=native` | Traceback verbosity |
| `--lf` / `--last-failed` | Run only tests that failed last run |
| `--ff` / `--failed-first` | Run failed tests first, then the rest |
| `--sw` / `--stepwise` | Stop on first failure, continue from there on next run |
| `--randomly-seed=N` | Reproduce a specific test order from pytest-randomly |
| `--randomly-seed=auto` | Use a deterministic but randomized order per run |
| `--durations=10` | Show the 10 slowest tests |
| `-k EXPRESSION` | Select tests by substring or boolean expression |
| `-m MARK` | Select tests by marker |
| `-x` | Stop after the first failure |
| `--pdb` | Drop into the debugger on failure |
| `--cov=src` | Measure coverage for the `src` package |

**Variety booster:** Add `--durations=10` to a scheduled CI job to detect slow tests and fixtures that silently inflate feedback loops.

## Variety Booster

[ref: #pyproject-variety-booster]

**Cover more invariants with less code by combining configuration defaults with composable markers.**
Use `filterwarnings = ["error"]` to catch unintended regressions that would otherwise hide behind warning noise.
Use `--randomly-seed=auto` to exercise order-dependent isolation bugs without writing new tests.
Use `-n=auto` plus `--dist=loadfile` in CI to surface shared mutable state across tests.
Use `--durations=10` regularly to identify slow tests that may signal inefficient fixtures or missing isolation.
Each default option turns the existing suite into a broader invariant probe, multiplying coverage without adding test cases.
