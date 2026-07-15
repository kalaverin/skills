---
subject: "Extend pytest itself: read options/ini via `pytestconfig`, pass typed hook-to-hook data with `pytest.StashKey`, persist across runs with `config.cache`, add JUnit metadata via `record_property`, control hook ordering (`tryfirst`/`trylast`/`firstresult`), write wrapper/custom hooks (`pytest_addhooks`), modify collection with `pytest_collection_modifyitems`+`pytest_deselected`, register markers dynamically, and test plugins with `pytester`."
index:
  - anchor: internals-config-stash
    what: "The built-in `pytestconfig` fixture exposes the same `pytest.Config` instance that hooks receive, letting fixtures and tests read CLI options, ini values, and the active `pytest.Session`."
    problem: "Fixture or test cannot locate required CLI option or ini value at runtime, and quietly defaulting to empty string postpones failure to distant confusing error; fail-fast config read, cli option precedence, ini fallback chain, explicit exception raise, environment-agnostic suite, early misconfig detection."
    use_when: "Required option or ini key gates fixture setup; absent value must raise immediately rather than coast on empty default; suite must run identically across environments."
    avoid_when: "Empty-string default accepted for required value; environment assumptions hardcoded instead of read through `pytestconfig`; `ValueError` omitted when neither CLI flag nor ini key supplies the setting."
    expected: "Configuration arrives via CLI option or ini key through `pytestconfig`, and missing required values fail at fixture setup with explicit error instead of surfacing downstream."
  - anchor: internals-config-stash
    what: "The built-in `request` fixture exposes the current `pytest.FixtureRequest`, carrying `request.node`, `request.module`, `request.function`, `request.path`, `request.nodeid`, `request.keywords`, `request.session`, `request.addfinalizer`, `request.applymarker`, and `request.getfixturevalue`."
    problem: "Test or fixture needs identity of currently executing node (nodeid, module, function) plus scoped helpers like finalizer registration and dynamic marker application; sibling fixture pull, defensive module attr, node keywords map, filesystem path inspect, owning session reach."
    use_when: "Node identity or nodeid must be known inside fixture or test; teardown, marker, or fixture retrieval must happen relative to current request; global state would be wrong tool."
    avoid_when: "`request.module` dereferenced blindly although it can be missing (guard like `request.module.__name__ if request.module else ''`); helpers fetched through global registry instead of `request`."
    expected: "Fixtures read node identity and invoke scoped helpers through `request`, with optional attributes guarded against absence."
  - anchor: internals-config-stash
    what: "A per-object stash on `config.stash`, `session.stash`, or any node/item stash, keyed by a typed `pytest.StashKey[T]()` created at module scope, used to pass data between hooks and fixtures."
    problem: "Value captured inside one hook (build tag at configure time) must reach later hooks and fixtures, and module-level global would collide when workers run in parallel; per-object namespace, typed key ownership, plugin data bus, session value share, key lifetime control."
    use_when: "One hook produces value that later hook or fixture consumes; sharing through module global risks divergence across workers; ownership and lifetime of shared value must stay explicit."
    avoid_when: "Module-global variable passed between hooks (diverges across xdist workers); untyped attribute smuggled onto `config` instead of typed `pytest.StashKey[T]()`."
    expected: "Value set once during `pytest_configure` travels to any fixture or hook through typed stash key, with no global state involved."
  - anchor: internals-config-stash
    what: "The `pytestconfig.cache` object that persists JSON-serializable data across test runs via `cache.get`, `cache.set`, and `cache.mkdir`."
    problem: "Session-scoped computation (seed generation, expensive lookup) repeats on every invocation and slows suite, yet naive module attribute cannot persist across separate runs; json-only payload, disabled cache blowup, invalidation trigger, seeded value stability, cache directory layout, mkdir artifact store."
    use_when: "Expensive session value costs noticeable time per run; stability across invocations matters (deterministic seed); stored content stays JSON-serializable."
    avoid_when: "Non-JSON-serializable payload stored; `pytestconfig.cache` dereferenced without `None` guard although `-p no:cacheprovider` disables it; run-varying value cached that should change between invocations."
    expected: "Expensive value computes once and reloads across runs until cache clears, with explicit `RuntimeError` when caching provider is unavailable."
  - anchor: internals-config-stash
    what: "The `record_property(name, value)` fixture that attaches metadata to the current test node, and `record_testsuite_property(name, value)` that attaches metadata to the whole suite, both surfaced in JUnit XML reports."
    problem: "Build tag or order identifier must land inside machine-readable JUnit report for downstream tooling, and hardcoded literal would mislead every consumer of that report; junit xml metadata, ci report ingestion, suite-level attachment, node-level attachment, user properties readback."
    use_when: "External tooling consumes JUnit output; identifier must be queryable per test or per suite; value derives from run context rather than fixed string."
    avoid_when: "Fixed literal recorded as property (misleads report consumers); value with no deterministic source attached; metadata expected outside JUnit XML (properties surface only there)."
    expected: "Deterministic run-derived properties appear on node or suite inside JUnit XML and stay assertable through `request.node.user_properties`."
  - anchor: internals-hooks
    what: "Ordering options on `@pytest.hookimpl` — `tryfirst=True` runs before other implementations of the same hook, `trylast=True` runs after them, and `firstresult=True` stops at the first non-None result and skips the rest."
    problem: "Several implementations of one hook coexist, and implicit registration order hides which one runs first or whether remainder gets skipped; must run earliest, must run last, stop at first answer, collect all results, override plugin behavior."
    use_when: "One implementation must precede or follow peers (`tryfirst`/`trylast`); only first non-None answer should matter (`firstresult`); registration order currently carries hidden behavioral weight."
    avoid_when: "`firstresult=True` set on hook whose every result is needed (remainder never executes); ordering left implicit where outcome depends on sequence."
    expected: "Hook execution sequence reads explicitly from decorator flags, and short-circuiting happens only where single answer is intended."
  - anchor: internals-hooks
    what: "A `@pytest.hookimpl(wrapper=True)` function that executes around all other implementations of the same hook: it `yield`s to run them, then inspects or replaces the `outcome` after `yield` returns."
    problem: "Plugin must react to outcome of every implementation of one hook from single central place, since scattered per-peer handling duplicates logic and loses unified error context; yield-forget hazard, teardown-phase wrap, cross-cutting concern, result substitution path, original traceback kept."
    use_when: "All peer outcomes need central observation or transformation; failure must re-raise with added context while original exception stays chained; one hook phase needs surrounding before/after logic."
    avoid_when: "`yield` omitted so remaining implementations never execute; `outcome.excinfo` discarded instead of re-raising via `raise ... from exc`; wrapper used where plain hook implementation suffices."
    expected: "Single wrapper surrounds every implementation, inspects or replaces outcome after `yield`, and re-raised failures keep original exception chain."
  - anchor: internals-hooks
    what: "User-defined hooks declared as empty `pytest_*` functions with docstrings in a hookspecs module, registered via `pytest_addhooks(pluginmanager)` with `pluginmanager.add_hookspecs(module)`, and invoked through `config.hook.<hook_name>(...)`."
    problem: "Project-specific event needs extension point that external plugins implement and project itself invokes through same machinery pytest uses internally; domain event signal, decoupled emit point, keyword-only signature, spec docstring contract, stable extension contract."
    use_when: "Suite or plugin owns event that outside code should react to; call sites hold `pytest.Config`; contract deserves documentation through spec docstrings."
    avoid_when: "Spec declared with positional parameters (hook calls pass keywords only and pytest prunes extras); hook invoked before `pluginmanager.add_hookspecs(module)` registers it; custom spec used where existing built-in hook already covers phase."
    expected: "Custom event is declared, registered, and callable as `config.hook.<hook_name>(...)` with keyword arguments from anywhere holding config."
  - anchor: internals-hooks
    what: "The ordered pytest hooks that span a run — `pytest_addoption`, `pytest_configure`, `pytest_sessionstart`, `pytest_runtest_setup`, `pytest_runtest_call`, `pytest_runtest_teardown`, `pytest_sessionfinish` — used as extension points for each phase."
    problem: "Setup work lands in wrong run phase when chosen hook fires earlier or later than task requires, leaking state across phases or missing its window; configure-time wiring, session bootstrap, per-test boundary, option parsing stage, teardown ordering."
    use_when: "Behavior belongs to exactly one run phase; placement too early or late would smear state into neighboring phase; task maps to option, configure, session, per-test, or session-finish boundary."
    avoid_when: "Hook picked by habit rather than phase semantics; work split across two hooks where one phase-matched hook suffices; fixture-solvable setup forced into hook."
    expected: "Chosen hook fires at matching lifecycle phase with state contained inside that phase."
  - anchor: internals-collection-plugins
    what: "The `pytest_collection_modifyitems(config, items)` hook that runs after collection to sort, deselect, dynamically mark, or skip tests before execution."
    problem: "Suite needs central filtering (integration tests skipped unless flag present) and ordering after collection, but silent removal would hide deselected tests from reports and other plugins; slow-test deprioritization, bulk skip injection, marker-driven selection, ci fast lane."
    use_when: "Execution set depends on runtime flags or markers; ordering policy must apply suite-wide; removals need observability through standard notification channel."
    avoid_when: "`items` rebound instead of mutated via `items[:] = ...`; removal performed without `config.hook.pytest_deselected(items=...)` so plugins observe nothing; per-test `pytest.mark.skip` scattered where one central filter expresses policy."
    expected: "Final execution set is mutated in place after collection, every removal announced through `pytest_deselected`, and ordering applies uniformly across suite."
  - anchor: internals-collection-plugins
    what: "Registering markers at runtime in `pytest_configure` with `config.addinivalue_line('markers', 'name: description')` (or statically in `pyproject.toml`), reading them closest-first with `item.iter_markers(name=...)`, and adding them at runtime with `item.add_marker(pytest.mark.<name>)`."
    problem: "Runtime-discovered tests carry no labels for selective execution, and ad-hoc marks pollute output with warnings while staying undocumented; closest-first precedence, ci-only slow label, integration folder tag, strict-markers gate, keyword cli filter, dynamic mark apply."
    use_when: "Selection by `-m` expression must cover runtime-generated tests; marker list should read self-documented under `pytest --markers`; labels attach per path or per rule during collection."
    avoid_when: "Marker applied without registration (warning noise, absent from listing); `item.keywords` inspected directly instead of `item.iter_markers(name=...)`; static `pyproject.toml` declaration forgotten for permanently used marks."
    expected: "Every runtime label is registered and visible under `pytest --markers`, reads closest-first through `iter_markers`, and emits no unknown-marker warnings."
  - anchor: internals-collection-plugins
    what: "The choice between shipping hook implementations as local `conftest.py` files inside the test tree or as an installable package that exposes a `pytest11` entry point."
    problem: "Hook code sits in wrong place: project-specific logic shipped inside installable package (or reusable logic trapped in local conftest), so consumers either cannot import it or inherit irrelevant behavior; repo boundary, team-local convention, distribution cost, accidental global behavior, importable test utility."
    use_when: "Behavior serves only this project's suite; other repositories would benefit from same hooks; activation scope must stay deliberate."
    avoid_when: "Cross-repository behavior locked inside local `conftest.py` where nothing else can consume it; project-only policy packaged into `pytest11` plugin that activates in every consumer's run."
    expected: "Project-only hooks stay in local `conftest.py`, and reusable behavior ships as installable plugin discovered through `pytest11` entry point across repositories."
  - anchor: internals-collection-plugins
    what: "The `pytester` fixture (enabled with `pytest_plugins = ['pytester']`) that runs a plugin inside an isolated pytest subprocess: files are created with `makeconftest`/`makepyfile`, executed with `pytester.runpytest()`, and inspected with `result.assert_outcomes(...)` and `result.stdout.str()`."
    problem: "Plugin logic verified inside host pytest process would pollute host state and produce flaky interference, so verification demands separate sandboxed run with own files; plugin dogfood loop, run outcome contract, stdout result scrape, exit code matrix, temporary test module."
    use_when: "Hook or plugin behavior needs end-to-end verification; test must observe pytest's own reporting of outcomes; host run state must stay untouched."
    avoid_when: "Plugin imported directly into host process for testing; `pytest_plugins = ['pytester']` declaration missing so fixture stays unavailable; assertion limited to exit code while reported outcomes carry the real signal."
    expected: "Plugin executes inside isolated subprocess with generated files, and outcomes are asserted through `assert_outcomes` plus captured stdout without touching host run."
  - anchor: internals-collection-plugins
    what: "Registering a helper module with `pytest.register_assert_rewrite('package.helper')` before importing it, so that `assert` statements inside the helper produce clear failure messages."
    problem: "Shared helper module performs assertions whose bare failure output gives no introspected detail, because plain import bypasses pytest's rewrite machinery; import-before-register hazard, library-style assert reuse, helper boundary blindness, conftest registration spot, registered module list."
    use_when: "Assertion lives outside test module inside shared helper; failure output must show introspected values like test-module asserts; import order can be controlled from conftest."
    avoid_when: "Helper imported before `pytest.register_assert_rewrite(...)` runs (rewrite applies only to later imports); registration scattered per test module instead of single conftest-level call; helpers rewritten although they contain no assertions."
    expected: "Helpers register before first import, and their assertion failures render with full introspection identical to test-module output."
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
