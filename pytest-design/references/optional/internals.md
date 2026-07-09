---
subject: "Extend pytest itself: read options/ini via `pytestconfig`, pass typed hook-to-hook data with `pytest.StashKey`, persist across runs with `config.cache`, add JUnit metadata via `record_property`, control hook ordering (`tryfirst`/`trylast`/`firstresult`), write wrapper/custom hooks (`pytest_addhooks`), modify collection with `pytest_collection_modifyitems`+`pytest_deselected`, register markers dynamically, and test plugins with `pytester`."
index:
  - anchor: internals-config-stash
    what: "The built-in `pytestconfig` fixture exposes the same `pytest.Config` instance that hooks receive, letting fixtures and tests read CLI options, ini values, and the active `pytest.Session`."
    problem: "Fixture or test must read CLI options, ini values, and session metadata without hardcoding environment assumptions or silently defaulting required value to empty; read config, fail fast missing, option fallback ini, no hardcoded default, explicit exception, environment agnostic."
    use_when: "Fixture or test must read option, ini, or session metadata, missing required value must fail fast, and environment assumptions stay explicit; read config, fail fast missing, option fallback ini, no hardcoded default, explicit exception, environment agnostic, config access."
    avoid_when: "Do not hardcode environment assumptions or let a required option silently default to an empty value; the `api_base_url` fixture raises `ValueError` when neither `--api-base-url` nor the `api_base_url` ini key is set."
    expected: "Configuration is read from CLI options and ini values through `pytestconfig`, with missing required values failing fast via an explicit exception instead of a hardcoded default."
  - anchor: internals-config-stash
    what: "The built-in `request` fixture exposes the current `pytest.FixtureRequest`, carrying `request.node`, `request.module`, `request.function`, `request.path`, `request.nodeid`, `request.keywords`, `request.session`, `request.addfinalizer`, `request.applymarker`, and `request.getfixturevalue`."
    problem: "Fixture or test needs current node identity and fixture-scoped helpers (finalizer, dynamic marker, other fixture) without reaching for global state; node identity, register teardown, runtime marker, dynamic fixture pull, defensive optional attr, request-scoped helper."
    use_when: "Fixture or test needs current node identity and request scoped helpers, global state is unnecessary, and optional attributes must be handled defensively; node identity, register teardown, runtime marker, dynamic fixture pull, defensive optional attr, request scoped helper."
    avoid_when: "Do not assume `request.module` is always present; the example guards it with `request.module.__name__ if request.module else ''`, so handle a missing module rather than dereferencing it blindly."
    expected: "Fixtures and tests read the current node identity and use fixture-scoped helpers through `request`, with optional attributes such as `request.module` accessed defensively."
  - anchor: internals-config-stash
    what: "A per-object stash on `config.stash`, `session.stash`, or any node/item stash, keyed by a typed `pytest.StashKey[T]()` created at module scope, used to pass data between hooks and fixtures."
    problem: "Hook must pass typed data to later hook or fixture (value captured at configure, read by fixture) without module-level globals that collide under parallel runs; cross-hook state, typed stash key, no global variable, parallel safe handoff, configure to fixture, ownership clear."
    use_when: "Hook captures value at configure time, later hook or fixture must read same typed value, and module globals would collide under parallel runs; cross hook state, typed stash key, no global variable, parallel safe handoff, configure to fixture, ownership clear."
    avoid_when: "Do not use module-level global variables to pass data between hooks; use a typed `pytest.StashKey[T]()` on the appropriate stash instead."
    expected: "Inter-hook and hook-to-fixture state travels through a typed stash key with no global variables, so a value set once in `pytest_configure` is readable from any fixture."
  - anchor: internals-config-stash
    what: "The `pytestconfig.cache` object that persists JSON-serializable data across test runs via `cache.get`, `cache.set`, and `cache.mkdir`."
    problem: "Expensive session-scoped value must stay stable across invocations until cache cleared, instead of recomputing on every run; persist across runs, compute once reuse, json serializable, cache disabled guard, seeded instance stable, clear on demand."
    use_when: "Expensive session value should persist across invocations until cache clears, recomputing every run wastes time, and cache disabled case must be guarded; persist across runs, compute once reuse, json serializable, cache disabled guard, seeded instance stable, clear on demand."
    avoid_when: "Do not assume the cache is always available or store non-JSON-serializable values; the example raises `RuntimeError` when `pytestconfig.cache` is `None`, and `config.cache` only persists JSON-serializable data via `get`/`set`/`mkdir`."
    expected: "Expensive session-scoped values are computed once and reused across runs through `config.cache`, with a clear failure when caching is disabled."
  - anchor: internals-config-stash
    what: "The `record_property(name, value)` fixture that attaches metadata to the current test node, and `record_testsuite_property(name, value)` that attaches metadata to the whole suite, both surfaced in JUnit XML reports."
    problem: "Deterministic identifier (order id, build tag) must attach to node or whole suite so it surfaces in machine-readable report; node property, suite property, report metadata, derived value, no hardcoded literal, user properties assert."
    use_when: "Deterministic identifier must attach to node or suite, machine readable report should surface it, and hardcoded literal would mislead consumers; node property, suite property, report metadata, derived value, user properties assert, build tag."
    avoid_when: "Do not record hardcoded literals as JUnit properties; keep values deterministic and derived from the test or configuration (a generated `order_id` or a `build_tag` from config) rather than fixed strings."
    expected: "Deterministic, configuration- or test-derived properties are attached to the node or suite and appear in JUnit XML, assertable through `request.node.user_properties`."
  - anchor: internals-hooks
    what: "Ordering options on `@pytest.hookimpl` — `tryfirst=True` runs before other implementations of the same hook, `trylast=True` runs after them, and `firstresult=True` stops at the first non-None result and skips the rest."
    problem: "Hook implementation order relative to peers and whether later implementations are skipped must be explicit instead of relying on registration order; run before peers, run after peers, short-circuit first result, declared order, skip remaining, single result intent."
    use_when: "Hook order relative to peers changes behavior, first result may short circuit, and registration order must not be hidden dependency; run before peers, run after peers, short circuit first result, declared order, skip remaining, single result intent."
    avoid_when: "Do not set `firstresult=True` on a hook whose every result you need, because it stops at the first non-None result and skips the remaining implementations."
    expected: "Hook implementations run in an explicitly declared order, and `firstresult` short-circuits only where a single result is intended."
  - anchor: internals-hooks
    what: "A `@pytest.hookimpl(wrapper=True)` function that executes around all other implementations of the same hook: it `yield`s to run them, then inspects or replaces the `outcome` after `yield` returns."
    problem: "Result of every other implementation of a hook must be observed or transformed (re-raise with context) from one central place without losing original exception; wrap around peers, inspect outcome, preserve exception chain, central re-raise, yield required, outcome replace."
    use_when: "Every peer hook outcome must be observed or transformed centrally, original exception chain must survive, and wrapper controls yield point; wrap around peers, inspect outcome, preserve exception chain, central re raise, yield required, outcome replace."
    avoid_when: "Do not omit the `yield` (the remaining implementations would never run) and do not discard `outcome.excinfo`; the example re-raises with `raise AssertionError(...) from exc` so the original failure is preserved."
    expected: "One wrapper surrounds every implementation of the hook, inspects the outcome, and re-raises or returns results without losing the original exception chain."
  - anchor: internals-hooks
    what: "User-defined hooks declared as empty `pytest_*` functions with docstrings in a hookspecs module, registered via `pytest_addhooks(pluginmanager)` with `pluginmanager.add_hookspecs(module)`, and invoked through `config.hook.<hook_name>(...)`."
    problem: "Plugin or project must define its own extension points that other code implements and calls through same hook machinery pytest uses internally; custom hook spec, register spec, keyword-only args, call through config hook, empty spec function, add hookspecs."
    use_when: "Project needs own extension point, outside code implements spec, and call must pass through same hook machinery pytest uses; custom hook spec, register spec, keyword only args, call through config hook, empty spec function, add hookspecs."
    avoid_when: "Do not define custom hook specs with positional parameters (hooks receive only keyword arguments and pytest prunes unused ones), and do not call a hook before registering its spec with `pluginmanager.add_hookspecs(module)`."
    expected: "The custom hook is declared, registered, and callable through `config.hook.<hook_name>(...)` from anywhere with a `pytest.Config`, with keyword-only arguments."
  - anchor: internals-hooks
    what: "The ordered pytest hooks that span a run — `pytest_addoption`, `pytest_configure`, `pytest_sessionstart`, `pytest_runtest_setup`, `pytest_runtest_call`, `pytest_runtest_teardown`, `pytest_sessionfinish` — used as extension points for each phase."
    problem: "Behavior must inject at correct run phase (option, configure, session start, per-test setup/call/teardown, session finish) rather than earlier or later; lifecycle phase, pick matching hook, no cross-phase leak, option setup, per-test call, session finish."
    use_when: "Behavior must inject at one lifecycle phase, earlier or later placement leaks cross phase state, and hook choice decides correctness; lifecycle phase, pick matching hook, no cross phase leak, option setup, per test call, session finish."
    avoid_when: "Do not implement a hook in an earlier or later phase than the work requires — pick the hook whose phase matches the task."
    expected: "The chosen hook runs at the correct lifecycle phase with no cross-phase state leakage."
  - anchor: internals-collection-plugins
    what: "The `pytest_collection_modifyitems(config, items)` hook that runs after collection to sort, deselect, dynamically mark, or skip tests before execution."
    problem: "Collected tests must reorder, filter, or relabel centrally (deselect integration unless flag passed) while reports and plugins stay aware of every deselection; central deselect, report removal, mutate in place, partition items, notify deselected, final set visible."
    use_when: "Collected tests must reorder, filter, or relabel centrally, deselected items must stay reported, and items list mutates in place; central deselect, report removal, mutate in place, partition items, notify deselected, final set visible, collection hook."
    avoid_when: "Do not remove items without calling `config.hook.pytest_deselected(items=deselected)` (reports and plugins would not observe the change), and do not rebind `items` (mutate it in place with `items[:] = ...`)."
    expected: "Collected tests are sorted, deselected, or marked centrally, every deselection is reported via `pytest_deselected`, and `items` is updated in place so all plugins see the final set."
  - anchor: internals-collection-plugins
    what: "Registering markers at runtime in `pytest_configure` with `config.addinivalue_line('markers', 'name: description')` (or statically in `pyproject.toml`), reading them closest-first with `item.iter_markers(name=...)`, and adding them at runtime with `item.add_marker(pytest.mark.<name>)`."
    problem: "Tests discovered at runtime must auto-label (every test under integration path) while marker vocabulary stays registered, documented, and free of unknown warnings; runtime marker add, register marker, closest-first read, self-documenting list, no unknown warning, path-based mark."
    use_when: "Runtime discovered tests need labels by path, marker vocabulary must stay registered, and unknown marker warnings must not appear; runtime marker add, register marker, closest first read, self documenting list, no unknown warning, path based mark."
    avoid_when: "Do not apply markers at runtime without registering them (unregistered markers trigger unknown-marker warnings and are absent from `pytest --markers`), and do not read marks by inspecting `item.keywords` directly (use `item.iter_markers(name=...)`)."
    expected: "Runtime-applied markers are registered and self-documenting under `pytest --markers`, read closest-first via `iter_markers`, and added via `add_marker` without unknown-marker warnings."
  - anchor: internals-collection-plugins
    what: "The choice between shipping hook implementations as local `conftest.py` files inside the test tree or as an installable package that exposes a `pytest11` entry point."
    problem: "Plugin code location must keep project-specific hooks local while reusable behavior ships across repositories; local conftest, installable plugin, entry point reuse, share across repos, project hook local, packaging choice."
    use_when: "Hook behavior is project specific, reusable behavior must ship across repositories, and packaging choice decides local versus installable plugin; local conftest, installable plugin, entry point reuse, share across repos, project hook local, packaging choice."
    avoid_when: "Do not keep reusable, cross-repository behavior only in a local `conftest.py` (it cannot be shared), and do not ship project-specific hooks as an installable `pytest11` plugin."
    expected: "Project-specific hooks live in local `conftest.py` files, while reusable behavior ships as an installable `pytest11` plugin consumable across repositories."
  - anchor: internals-collection-plugins
    what: "The `pytester` fixture (enabled with `pytest_plugins = ['pytester']`) that runs a plugin inside an isolated pytest subprocess: files are created with `makeconftest`/`makepyfile`, executed with `pytester.runpytest()`, and inspected with `result.assert_outcomes(...)` and `result.stdout.str()`."
    problem: "Plugin hook behavior must verify without interfering with host pytest process, by running in its own sandboxed subprocess; isolated subprocess, sandbox files, assert outcomes, no host pollution, enable fixture first, runpytest inspect."
    use_when: "Plugin hook behavior must verify in sandbox, host pytest process must stay clean, and assertions inspect subprocess outcomes; isolated subprocess, sandbox files, assert outcomes, no host pollution, enable fixture first, runpytest inspect, plugin test."
    avoid_when: "Do not test a plugin by importing it into the same pytest process (use `pytester` to run it in an isolated subprocess), and do not omit `pytest_plugins = ['pytester']` (the fixture must be enabled before use)."
    expected: "The plugin runs in an isolated subprocess and its outcomes are verified with `assert_outcomes`, so hook behavior is tested without polluting the host run."
  - anchor: internals-collection-plugins
    what: "Registering a helper module with `pytest.register_assert_rewrite('package.helper')` before importing it, so that `assert` statements inside the helper produce clear failure messages."
    problem: "Assertions inside shared helper modules must report clear rewritten failure messages instead of opaque assert failures; rewrite before import, clear failure message, helper assert rewrite, register timing, no opaque assert, module-scope register."
    use_when: "Shared helper module contains assertions, rewritten failure messages must stay clear, and import timing decides whether rewrite applies; rewrite before import, clear failure message, helper assert rewrite, register timing, no opaque assert, module scope register."
    avoid_when: "Do not import a helper module before calling `pytest.register_assert_rewrite(...)`; rewriting only applies to modules imported after registration, so a late registration leaves helper assertions opaque."
    expected: "Helper modules are registered before import, so assertions inside them are rewritten and produce clear failure messages like test-module assertions."
---

# Advanced pytest Internals

Use pytest internals when you need to extend collection, enforce suite-wide policies, persist state across runs, or build custom plugins.

## Config, session, and stash

[ref: #internals-config-stash]

The `pytestconfig` fixture exposes the same `pytest.Config` instance that hooks receive, and the `request` fixture exposes the current `pytest.FixtureRequest`.
Use these objects to read CLI options, ini values, node metadata, and the active `pytest.Session` instead of hardcoding environment assumptions.

Read CLI options and ini values through `pytestconfig` or `request.config`, and fail with an explicit exception when a required value is missing.
The `request` fixture also carries `request.node`, `request.module`, `request.function`, `request.path`, `request.nodeid`, `request.keywords`, `request.session`, `request.addfinalizer`, `request.applymarker`, and `request.getfixturevalue`.

```python
import pytest
from faker import Faker


@pytest.fixture(scope="session")
def api_base_url(pytestconfig: pytest.Config) -> str:
    url = pytestconfig.getoption("api_base_url") or pytestconfig.getini("api_base_url")
    if not isinstance(url, str) or not url:
        raise ValueError("api_base_url must be provided via --api-base-url or the api_base_url ini key")
    return url


@pytest.fixture
def test_trace_context(request: pytest.FixtureRequest, fake: Faker) -> dict[str, str]:
    return {
        "nodeid": request.node.nodeid,
        "module": request.module.__name__ if request.module else "",
        "trace_id": fake.uuid4(),
    }
```

Use `pytest.StashKey[T]()` to create a typed key for `config.stash`, `session.stash`, `item.stash`, or any node stash.
Stash is the preferred mechanism for passing data between hooks without global variables.

```python
import pytest

_BUILD_TAG_KEY = pytest.StashKey[str]()


def pytest_configure(config: pytest.Config) -> None:
    build_tag = config.getoption("build_tag") or config.getini("build_tag")
    if isinstance(build_tag, str):
        config.stash[_BUILD_TAG_KEY] = build_tag


@pytest.fixture
def build_tag(request: pytest.FixtureRequest) -> str | None:
    return request.config.stash.get(_BUILD_TAG_KEY, None)
```

`config.cache` persists JSON-serializable data across test runs via `get`, `set`, and `mkdir`.
Use it for expensive session-scoped values that should remain stable between invocations until the cache is cleared.

```python
import pytest
from faker import Faker

_SEED_CACHE_KEY = "faker/session_seed"


@pytest.fixture(scope="session")
def deterministic_faker(pytestconfig: pytest.Config, fake: Faker) -> Faker:
    cache = pytestconfig.cache
    if cache is None:
        raise RuntimeError("pytest cache is unavailable")
    seed = cache.get(_SEED_CACHE_KEY, None)
    if seed is None:
        seed = fake.pyint(min_value=0, max_value=2**32)
        cache.set(_SEED_CACHE_KEY, seed)
    fake.seed_instance(seed)
    return fake
```

`record_property` attaches metadata to the current test node in JUnit XML reports, and `record_testsuite_property` attaches metadata to the entire suite.
Keep property values deterministic and derived from the test or configuration rather than hardcoded literals.

```python
import pytest
from faker import Faker


@pytest.fixture(scope="session", autouse=True)
def suite_build_metadata(
    record_testsuite_property: pytest.Callable[[str, object], None],
    pytestconfig: pytest.Config,
) -> None:
    build_tag = pytestconfig.getoption("build_tag") or pytestconfig.getini("build_tag")
    if isinstance(build_tag, str) and build_tag:
        record_testsuite_property("build_tag", build_tag)


def test_recorded_property_is_stored_on_node(
    record_property: pytest.Callable[[str, object], None],
    request: pytest.FixtureRequest,
    fake: Faker,
) -> None:
    """
    Given: a generated order id.
    When: it is recorded as a test property.
    Then: the property appears on the test node.
    """
    # --- Arrange ---
    order_id = fake.uuid4()

    # --- Act ---
    record_property("order_id", order_id)

    # --- Assert ---
    assert ("order_id", order_id) in request.node.user_properties
```

## Hooks and hook wrappers

[ref: #internals-hooks]

Hooks are the primary extension mechanism for pytest.
A hook implementation is any function named `pytest_*` decorated with `@pytest.hookimpl`.
The decorator accepts ordering options: `tryfirst=True` runs before other implementations of the same hook, and `trylast=True` runs after them.
Use `firstresult=True` when pytest should stop at the first non-None result and skip remaining implementations.

```python
import pytest


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    items.sort(key=lambda item: item.nodeid)
```

Hook wrappers execute around all other implementations of the same hook.
Decorate the function with `@pytest.hookimpl(wrapper=True)`, then `yield` to invoke the remaining implementations.
After `yield` returns, the wrapper can inspect or replace the result.

```python
from collections.abc import Generator

import pytest


@pytest.hookimpl(wrapper=True)
def pytest_runtest_call(item: pytest.Item) -> Generator[object, object, object]:
    outcome = yield
    if outcome.excinfo is not None:
        _exc_type, exc, _tb = outcome.excinfo
        raise AssertionError(f"Failure in {item.nodeid}") from exc
    return outcome.get_result()
```

Custom hooks are declared as empty `pytest_*` functions with docstrings in a dedicated module.
Register them via `pytest_addhooks(pluginmanager)` using `pluginmanager.add_hookspecs(module)`.
Hooks receive only keyword arguments; pytest dynamically prunes unused parameters, so spec functions can accept a superset of what callers provide.

```python
# myproject/hookspecs.py
import pytest


def pytest_my_custom_event(*, payload: dict[str, object]) -> None:
    """Signal that a custom event occurred."""
```

```python
# conftest.py
import pytest

from myproject import hookspecs


def pytest_addhooks(pluginmanager: pytest.PytestPluginManager) -> None:
    pluginmanager.add_hookspecs(hookspecs)


@pytest.hookimpl
def pytest_my_custom_event(*, payload: dict[str, object]) -> None:
    ...
```

Once registered, custom hooks are called through `config.hook.<hook_name>(...)`.
This works from fixtures, other hooks, or anywhere you have access to a `pytest.Config` instance.

```python
import pytest


@pytest.fixture
def emit_event(request: pytest.FixtureRequest):
    def _emit(payload: dict[str, object]) -> None:
        request.config.hook.pytest_my_custom_event(payload=payload)

    return _emit
```

Important lifecycle hooks include `pytest_addoption`, `pytest_configure`, `pytest_sessionstart`, `pytest_runtest_setup`, `pytest_runtest_call`, `pytest_runtest_teardown`, and `pytest_sessionfinish`.

## Collection, markers, and plugins

[ref: #internals-collection-plugins]

The `pytest_collection_modifyitems(config, items)` hook runs after collection and is the standard place to sort, deselect, dynamically mark, or skip tests before execution.
Call `config.hook.pytest_deselected(items=deselected)` whenever you remove items so that reports and plugins observe the change.

Register custom markers in `pytest_configure` with `config.addinivalue_line("markers", "slow: marks tests as slow")` or declare them statically under `[tool.pytest.ini_options]` in `pyproject.toml`.
Registered markers surface in `pytest --markers`, prevent unknown-marker warnings, and keep the suite self-documenting.

Read markers from closest scope to farthest with `item.iter_markers(name="slow")`.
Add markers dynamically with `item.add_marker(pytest.mark.slow)` to label tests discovered at runtime.

Plugins can live as local `conftest.py` files in the test tree or as installable packages exposing a `pytest11` entry point.
Local plugins are perfect for project-specific hooks; installable plugins ship reusable behavior across repositories.

Use the `pytester` fixture to test plugins in isolated pytest subprocesses.
Enable it with `pytest_plugins = ["pytester"]`, then create files via `pytester.makeconftest`, `pytester.makepyfile`, and run them with `pytester.runpytest()`.
Inspect results with `result.assert_outcomes(passed=1)` and `result.stdout.str()`.

Assertion rewriting only applies to modules imported after `pytest.register_assert_rewrite("package.helper")`.
Register helper modules before importing them so that test assertions inside those helpers produce clear failure messages.

### Example: deselecting and sorting during collection

```python
import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--integration", action="store_true", help="run integration tests")


def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    run_integration = config.getoption("--integration")
    deselected: list[pytest.Item] = []
    remaining: list[pytest.Item] = []

    for item in items:
        if item.get_closest_marker("integration") and not run_integration:
            deselected.append(item)
        else:
            remaining.append(item)

    if deselected:
        config.hook.pytest_deselected(items=deselected)

    items[:] = remaining
    items.sort(key=lambda item: 1 if item.get_closest_marker("slow") else 0)
```

### Example: registering and applying markers dynamically

```python
from pathlib import Path

import pytest


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "slow: tests that should run only on CI or on demand")
    config.addinivalue_line("markers", "integration: tests that need external services")


def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    for item in items:
        rel_path = Path(item.path).relative_to(config.rootpath)
        if rel_path.parts[0] == "integration":
            item.add_marker(pytest.mark.integration)
```

### Example: testing a plugin with pytester

```python
from textwrap import dedent

import pytest

pytest_plugins = ["pytester"]


def test_deselected_count(pytester: pytest.Pytester) -> None:
    """
    Given: a conftest that deselects one test and a pyfile with two tests.
    When: pytest runs inside the pytester sandbox.
    Then: one test passes and one is deselected.
    """
    # --- Arrange ---
    pytester.makeconftest(dedent("""
        def pytest_collection_modifyitems(config, items):
            deselected = [item for item in items if item.name == "test_skip_me"]
            items[:] = [item for item in items if item not in deselected]
            config.hook.pytest_deselected(items=deselected)
    """))
    pytester.makepyfile(dedent("""
        def test_skip_me(): assert False
        def test_run_me(): assert True
    """))

    # --- Act ---
    result = pytester.runpytest()

    # --- Assert ---
    result.assert_outcomes(passed=1, deselected=1)
```

### Example: assertion rewriting for helper modules

```python
import pytest

pytest.register_assert_rewrite("myproject.test_helpers")

from myproject import test_helpers


def test_via_helper() -> None:
    """
    Given: a helper module with registered assertion rewriting.
    When: a valid payload is asserted through the helper.
    Then: the helper assertion passes.
    """
    # --- Arrange ---
    payload = {"ok": True}

    # --- Act / Assert ---
    test_helpers.assert_valid_payload(payload)
```
