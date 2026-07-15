---
subject: "Organize reusable test dependencies: mirror `src/` under `tests/unit/`, place shared fixtures at lowest applicable `conftest.py`, choose `function`/`class`/`module`/`session` scope, deduplicate before creating, `yield` cleanup, restrict `conftest.py` content, `@pytest.fixture(name=...)`, factory fixtures with nested rollback, `params`/`pytest.param`, `@pytest.mark.usefixtures`, autouse telemetry; zero-tolerance anti-patterns and `__init__.py` policy."
index:
  - anchor: fixtures-directory-layout
    what: "Mirroring the source tree under `tests/unit/` so every source module has a same-relative-path test file, with domain fixtures in local `conftest.py` and shared fixtures promoted up the tree or into importable `tests/fixtures/` modules."
    problem: "Without mirrored layout, tests become hard to discover, far from code they cover, and fixtures duplicate or dump into one file; mirror source tree, co-located coverage, lowest covering scope, single-file dump, split large module."
    use_when: "Source tree has many modules; tests must mirror relative paths to the code they cover; shared fixtures serve several sub-packages and need promotion."
    avoid_when: "Flat dumps such as `tests/unit/test_everything.py` or `test_all_services.py`; tests for different source modules (e.g. `channels/service.py` and `contacts/service.py`) combined into a single `test_services.py`."
    expected: "Every source module maps to one discoverable, co-located test file, and shared fixtures live exactly at the lowest scope that covers all consumers."
  - anchor: fixtures-scope-placement
    what: "Choosing the narrowest pytest fixture scope (`function`/`class`/`module`/`session`) that satisfies a need, and placing the fixture at the matching conftest level."
    problem: "Over-wide scopes leak state and slow suite; over-narrow scopes repeat expensive setup and hide sharing; narrowest scope, isolation default, costly immutable, session resource, repeated setup, sharing boundary, mutable state, per-test fresh."
    use_when: "Fixture scope choice must balance isolation against setup cost; too wide would leak state across tests; too narrow would repeat expensive setup."
    avoid_when: "Wider scope than the need requires (never mutable or cheap setup in `session`); expensive read-only resource duplicated at a narrower scope."
    expected: "Each fixture uses the narrowest sufficient scope, so isolation is preserved by default and only genuinely expensive read-only resources are shared."
  - anchor: fixtures-deduction-protocol
    what: "A pre-creation checklist that searches existing context/conftest for similar fixtures, parameterized variants, and composability before adding a new fixture."
    problem: "Creating fixtures blindly without checking conftest hierarchy duplicates existing ones and fragments fixture surface across conftests; search existing, parameterizable variant, composability, eighty percent extend, document purpose, creation gate, same need, optional parameter."
    use_when: "New fixture request appears; existing conftest hierarchy may already cover it; blind creation would fragment the fixture surface."
    avoid_when: "New fixture created when an existing one covers 80% or more of the need; search for similar or parameterizable existing fixtures skipped."
    expected: "New fixtures are created only when no existing fixture can be extended, and each is placed at the minimal covering scope with a documented purpose."
  - anchor: fixtures-anti-patterns
    what: "A zero-tolerance lookup table pairing common fixture anti-patterns with the correct approach."
    problem: "Teams repeatedly introduce numbered, duplicated, or wrapper fixtures that fragment suite and hide canonical pattern; lookup correction, hard ban, review gate, smell catalog, factory parameterize, single definition, import once, role override."
    use_when: "Fixture review finds numbered, duplicated, or wrapper fixtures; canonical pattern is hidden; lookup table gives the correction."
    avoid_when: "Numbered fixtures (`test_user`/`test_user_2`); multiple similar fixtures (e.g. `admin_user_factory` next to `user_factory`); `db_session` duplicated across conftests; wrapper fixtures with no added value; per-module `fake`."
    expected: "Every fixture maps to a canonical pattern (factory with overrides, single shared definition), with the table acting as the review checklist and zero tolerance for the listed forms."
  - anchor: fixtures-yield-cleanup
    what: "The setup/`yield`/teardown fixture lifecycle, where code before `yield` is setup, the yielded value is the resource, and code after `yield` is teardown."
    problem: "Resources must tear down reliably after test without leaking cleanup logic into test bodies; setup yield teardown, cleanup in fixture, prefer yield, no try finally, resource lifecycle, after-test guarantee, failure path, exception safe, leaked handle."
    use_when: "Fixture allocates a resource; cleanup must run after test success or failure; test bodies should stay free of teardown logic."
    avoid_when: "`try/finally` used when a plain `yield` teardown suffices; teardown skipped or leaked into the test."
    expected: "Every resource fixture yields and tears down deterministically, with cleanup living entirely in the fixture."
  - anchor: fixtures-conftest-discovery
    what: "pytest's upward discovery of `conftest.py`, the directory-scoped visibility of its fixtures, and the rule that a conftest holds only fixtures, hooks, and their imports."
    problem: "Misplaced fixtures become invisible to consumers or leak to siblings, and bloated conftests mix concerns belonging in modules; upward lookup, directory visibility, fixtures hooks imports only, no business logic, content restriction, closest conftest, helper module, import chain."
    use_when: "Fixture placement decides consumer visibility; misplaced fixture becomes invisible or leaks to siblings; conftest content needs auditing."
    avoid_when: "Utility functions, constants, or business logic in `conftest.py` (move them to modules such as `tests/fixtures/utils.py`); fixture assumed visible to sibling or parent test directories."
    expected: "Fixtures are discovered exactly where their consumers live, and conftests contain only fixtures, hooks, and imports."
  - anchor: fixtures-init-policy
    what: "Guidance on where `__init__.py` belongs in the test tree given PEP 420 implicit namespace packages (Python 3.12+)."
    problem: "Reflexively adding or omitting init file either clutters leaf directories or breaks package-style absolute imports where needed; package-less dir, cross-package import, leaf optional, package boundary, namespace semantics, clutter-free, explicit marker, move-safe module."
    use_when: "Package-style absolute imports need an explicit boundary; leaf directories may stay namespace packages; reflexive init files would clutter the tree."
    avoid_when: "`__init__.py` added to every leaf test directory by reflex; init file omitted where absolute imports cross package boundaries."
    expected: "`__init__.py` appears exactly where imports cross package boundaries, keeping package boundaries explicit without cluttering leaf test dirs."
  - anchor: fixtures-typing
    what: "Typing session/module/class-scoped teardown fixtures as `Generator[X, None, None]` and no-teardown function fixtures as `-> X`."
    problem: "Wrong return type hides setup yield teardown semantics and lets type checkers miss misuse of yielded value; generator type, direct return, factory callable, honest lifecycle, annotation honesty, checker signal, typed builder."
    use_when: "Fixture return type must reveal its lifecycle; teardown fixtures are annotated as generators; factories expose a callable type."
    avoid_when: "Teardown fixture typed as `-> X` (hides the teardown); no-teardown function fixture typed as `Generator`."
    expected: "Each fixture's annotation honestly reflects its lifecycle, so type checkers and readers see setup/yield/teardown vs plain return."
  - anchor: fixtures-fixture-name
    what: "Using `@pytest.fixture(name=...)` to expose a readable public fixture name while keeping the implementation function private (underscore-prefixed)."
    problem: "Exposing builder function name couples tests to implementation detail and clutters public fixture surface; readable public name, hidden builder, underscore impl, one builder overrides, stable name, renaming decorator, scenario name, test-facing alias."
    use_when: "Builder implementation name leaks into the public fixture surface; readable fixture name should stabilize tests; the underscore function hides the detail."
    avoid_when: "Underscore-prefixed builder name exposed to tests; separate public fixtures created by duplicating the builder instead of reusing one private builder with overrides."
    expected: "Tests depend on stable readable names while the implementation stays private and single."
  - anchor: fixtures-factory-rollback
    what: "Factory fixtures that return a callable accepting `**overrides`, paired with a `db_session` that uses a nested transaction (savepoint) rolled back after each test for database-backed factories."
    problem: "Multiple similar fixtures duplicate object shapes, and manual cleanup lists are slow, error-prone, and require tracking; one factory overrides, nested transaction rollback, shape coverage, auto-rollback, per-test savepoint, tracking burden, join mode."
    use_when: "Similar fixtures duplicate object shapes; manual cleanup lists track resources badly; a savepoint-wrapped session can isolate database factories."
    avoid_when: "Multiple similar fixtures created instead of one factory with overrides; manual cleanup lists used where a savepoint-rollback session applies."
    expected: "One factory with overrides covers every object shape, and database state is isolated per test by automatic rollback with no cleanup tracking."
  - anchor: fixtures-parameterized
    what: "`@pytest.fixture(params=...)` (optionally with `pytest.param(..., id=..., marks=...)`) that turns each parameter into a separate test case for an identical test body."
    problem: "Writing one test per variant duplicates identical bodies across suite and discourages adding cases later; fixture params surface, param marks, case matrix, add parameter, body differs separate, id label, xfail attach, case explosion."
    use_when: "Test body stays identical across fixture variants; each parameter should become a case automatically; marks attach per parameter."
    avoid_when: "Fixture `params` used when test bodies differ per variant (use separate tests); near-identical fixtures duplicated where a parameter surface would do."
    expected: "Adding a variant means adding a parameter, while one test body covers every case and the parameter surface forms a reusable matrix."
  - anchor: fixtures-usefixtures
    what: "Applying a fixture for its side effects via `@pytest.mark.usefixtures('name')` when the test does not use the fixture's return value."
    problem: "Declaring fixture as test argument solely for side effects clutters signature with unused value; side-effect only, marker apply, declarative setup, stack markers, env flag, apply by name, argument noise, no return needed, signature hygiene."
    use_when: "Fixture only provides a side effect; test argument would stay unused; marker applies the setup declaratively without return noise."
    avoid_when: "`@pytest.mark.usefixtures` used when the test needs the fixture's return value — declare it as a test argument instead."
    expected: "Test signatures list only the data they assert, while side-effect fixtures are applied declaratively via the marker."
  - anchor: fixtures-telemetry
    what: "An autouse fixture that logs setup and teardown of every fixture via `logging` (optionally with node ID and scope), captured through `caplog` or `--log-cli-level=DEBUG`."
    problem: "Flaky tests caused by fixture ordering are hard to diagnose without visibility into setup teardown lifecycle; lifecycle log, autouse logger, capture debug, no print, triage visibility, node identity, scope tag, log stream, log-cli flag."
    use_when: "Fixture ordering causes flaky tests; setup/teardown lifecycle needs visibility during triage; diagnosis should work without print statements."
    avoid_when: "`print()` used in fixtures or tests — route through `logging`."
    expected: "Fixture lifecycle is observable via structured logs, so ordering bugs across scopes can be diagnosed without `print`."
libraries:
  - pytest-faker
---

# FIXTURE HIERARCHY — CORE

## Directory Layout and Segmentation Rules

[ref: #fixtures-directory-layout]

Mirror the source tree: if the source file lives at `src/app/core/channels/service.py`, its unit tests live at `tests/unit/core/channels/test_service.py`.
One test file per source module: do not combine tests for `channels/service.py` and `contacts/service.py` into a single `test_services.py`.
Group shared fixtures by domain: if multiple test modules in `tests/unit/core/channels/` need the same fixtures, place them in `tests/unit/core/channels/conftest.py`.
If the fixtures are reused across multiple sub-packages, promote them up the tree to `tests/unit/conftest.py` or to importable helper modules under `tests/fixtures/` that are imported by `tests/conftest.py`.
Test file naming is `test_<module_name>.py` where `<module_name>` matches the source file name without `.py`.
For packages with many public symbols, you may split into `test_<module_name>_<aspect>.py` only when the module is large enough to justify it.
No flat dumps: a single `tests/unit/test_everything.py` or `tests/unit/test_all_services.py` is a critical failure.

Example directory structure for a project with `src/app/core/channels/service.py`, `src/app/domain/channel.py`, and `src/app/grpc_api/servicers/channel.py`:

```text
tests/
├── conftest.py                    # root: imports helpers from tests/fixtures
├── fixtures/                      # reusable fixture helper modules
│   ├── __init__.py
│   ├── databases.py               # db_engine, db_session helpers
│   ├── domains.py                 # domain factories
│   └── utils.py                   # faker_config, clock helpers
└── unit/
    ├── conftest.py               # mocker, isolated, no_io
    ├── core/
    │   └── channels/
    │       └── test_service.py
    ├── domain/
    │   └── test_channel.py
    └── grpc_api/
        └── servicers/
            └── test_channel.py
```

**Variety booster:** when a module has several public behaviors, split tests by aspect (`test_service_create.py`, `test_service_delete.py`) and reuse the same domain fixtures across the aspects to exercise the same invariants through different entry points.

## Scope Placement Rules

[ref: #fixtures-scope-placement]

| Scope | Where to define | Examples |
|---|---|---|
| `session` | `tests/conftest.py` or imported helper modules | `db_engine`, `app_instance`, `faker_config` |
| `module` | `tests/<level>/<component>/conftest.py` | module-level mocks, shared test data schemas |
| `class` | `tests/<level>/<component>/conftest.py` or inline in test class | class-specific state, grouped setup |
| `function` | closest `conftest.py` or inline `@pytest.fixture` | fresh instances, isolated mutations |

**Variety booster:** place a read-only `session` fixture in the root conftest and override it with a `function` fixture in a local conftest when one package needs isolated mutations; this lets the same resource model serve both shared and isolated test families.

## Fixture Deduction Protocol

[ref: #fixtures-deduction-protocol]

1. Check available context and existing conftest files for fixtures that serve the same or similar purpose.
2. Check for parameterized variants of existing fixtures before creating new ones.
3. Check for composability: can the desired fixture be built from existing fixtures?
4. If an existing fixture covers 80% or more of the need, extend it with optional parameters rather than creating a new one.
5. If you must create a new fixture, place it at the lowest scope conftest that covers all consumers.
6. Document the fixture's purpose and why it differs from similar existing fixtures in its docstring.

**Variety booster:** prefer adding one optional parameter to an existing factory over adding a second fixture; a single `notification_factory(channel_type=...)` can cover email, sms, and push variants without multiplying files.

## Anti-Patterns

[ref: #fixtures-anti-patterns]

| Anti-pattern | Correct approach |
|---|---|
| Creating `admin_user_factory` alongside `user_factory` | Parameterize: `user_factory(role=Role.ADMIN)` |
| Creating `test_user` and `test_user_2` in the same conftest | Use `user_factory()` for distinct instances |
| Duplicating `db_session` in multiple conftest files | Define once in `tests/fixtures/databases.py` and import it from `tests/conftest.py` |
| Creating a fixture that wraps another fixture with no added value | Use the original fixture directly |
| Defining `fake` per-module | Define one `fake` in `tests/fixtures/utils.py` |

**Variety booster:** when you catch yourself about to create `_fixture_2`, turn it into a factory call with an override; the override exercises edge cases while keeping the test body identical.

## `yield` Cleanup Pattern

[ref: #fixtures-yield-cleanup]

```python
from collections.abc import Generator

import pytest
from faker import Faker


class Client:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self._connected = False

    def connect(self) -> None:
        self._connected = True

    def disconnect(self) -> None:
        self._connected = False


@pytest.fixture
def connected_client(fake: Faker) -> Generator[Client, None, None]:
    """Create a client, yield it, then disconnect."""
    client = Client(base_url=fake.url())
    client.connect()
    yield client
    client.disconnect()
```

**Variety booster:** yield a tuple `(resource, helper)` from a single fixture so tests can perform controlled mutations and the fixture can still tear everything down; this reduces the number of fixtures a test must declare.

## `conftest.py` Discovery and Content Restrictions

[ref: #fixtures-conftest-discovery]

`conftest.py` must contain only:
- `@pytest.fixture` definitions
- pytest hook implementations (`pytest_configure`, `pytest_collection_modifyitems`, etc.)
- imports required by the above

No utility functions, no constants, no business logic.
Those belong in regular Python modules such as `tests/fixtures/utils.py`.

**Variety booster:** move reusable helper functions into regular modules and import them from the conftest; the same helpers can then be used by tests, fixtures, and factory defaults without bloating the conftest.

## `__init__.py` Policy

[ref: #fixtures-init-policy]

**Variety booster:** keep `__init__.py` only where imports cross directory boundaries; this makes the package boundary explicit and lets you move fixture modules between packages without changing import paths.

## Fixture Typing

[ref: #fixtures-typing]

```python
from collections.abc import Generator

import pytest
from sqlalchemy import Engine


@pytest.fixture(scope="session")
def db_engine() -> Generator[Engine, None, None]:
    """Create a shared engine and dispose it after the session."""
    engine = create_engine("sqlite:///:memory:")
    yield engine
    engine.dispose()
```

**Variety booster:** type factory fixtures as `Callable[..., X]` and their internal builders as nested functions; the explicit signature documents the override surface and catches accidental positional argument drift.

## `@pytest.fixture(name=...)` Renaming

[ref: #fixtures-fixture-name]

```python
from collections.abc import Callable
from enum import StrEnum

import pytest


class Role(StrEnum):
    ADMIN = "admin"
    MEMBER = "member"


class User:
    def __init__(self, role: Role) -> None:
        self.role = role


@pytest.fixture(name="admin_user")
def _make_admin_user(
    user_factory: Callable[..., User],
) -> User:
    """Provide an admin user without exposing the builder name."""
    return user_factory(role=Role.ADMIN)
```

**Variety booster:** create one private builder per domain concept and expose multiple named fixtures (`admin_user`, `pending_user`, `deleted_user`) by calling the same factory with different overrides; each name documents the scenario while the implementation stays single.

## Factory Fixtures and Nested Transaction Rollback

[ref: #fixtures-factory-rollback]

```python
from collections.abc import Callable, Generator
from datetime import UTC
from typing import Any

import pytest
from faker import Faker
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


ACTIVATION_CHANCE = 90


@pytest.fixture(scope="session")
def db_engine() -> Generator[Engine, None, None]:
    """Shared database engine with automatic disposal."""
    engine = create_engine("sqlite:///:memory:")
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(db_engine: Engine) -> Generator[Session, None, None]:
    """Isolated database session with automatic rollback."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )()
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def user_factory(fake: Faker) -> Callable[..., dict[str, Any]]:
    """Return a factory that builds randomized user data dicts."""

    def _create(**overrides: Any) -> dict[str, Any]:
        return {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.fake_email(),
            "phone": fake.phone_number(),
            "is_active": fake.boolean(chance_of_getting_true=ACTIVATION_CHANCE),
            "created_at": fake.date_time_between(
                start_date="-1y",
                end_date="now",
                tzinfo=UTC,
            ),
            **overrides,
        }

    return _create
```

Tests use the factory to create objects and rely on `db_session` rollback for cleanup.

```python
from collections.abc import Callable
from enum import StrEnum
from typing import Any


class Role(StrEnum):
    ADMIN = "admin"
    MEMBER = "member"


def test_user_factory_accepts_overrides(
    user_factory: Callable[..., dict[str, Any]],
) -> None:
    """
    Given: a user factory.
    When: it is called with role and is_active overrides.
    Then: the generated dict contains the overridden values.
    """
    # --- Arrange ---
    # user_factory fixture is provided.

    # --- Act ---
    user = user_factory(role=Role.ADMIN, is_active=False)

    # --- Assert ---
    assert user["role"] == Role.ADMIN
    assert user["is_active"] is False
```

**Variety booster:** expose a `count` parameter in the factory and generate small collections with `fake.pyint(min_value=2, max_value=5)` so a single test can assert both singleton and list behaviors without separate fixtures.

## Parameterized Fixtures

[ref: #fixtures-parameterized]

```python
from enum import StrEnum

import pytest


class Role(StrEnum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


@pytest.fixture(
    params=[
        pytest.param(Role.ADMIN, id="role-admin"),
        pytest.param(Role.EDITOR, id="role-editor"),
        pytest.param(Role.VIEWER, id="role-viewer"),
    ],
)
def user_role(request: pytest.FixtureRequest) -> Role:
    """Provide each supported user role in turn."""
    return request.param
```

Use `pytest.param(..., marks=...)` to attach markers such as `pytest.mark.xfail` to individual parameters.

**Variety booster:** combine a parameterized fixture with a factory override so the same test runs against multiple roles, statuses, or channel types; the parameter surface becomes a reusable test matrix.

## `@pytest.mark.usefixtures`

[ref: #fixtures-usefixtures]

```python
import os

import pytest


@pytest.fixture
def feature_flag_enabled(monkey: pytest.MonkeyPatch) -> None:
    """Enable the feature flag for tests that only need the side effect."""
    monkey.setenv("FEATURE_FLAG", "1")


@pytest.mark.usefixtures("feature_flag_enabled")
def test_feature_flag_is_set() -> None:
    """
    Given: the feature flag fixture is applied.
    When: the environment is inspected.
    Then: the feature flag is set to "1".
    """
    # --- Arrange ---
    # feature_flag_enabled fixture sets the environment variable.

    # --- Act ---
    flag_value = os.environ["FEATURE_FLAG"]

    # --- Assert ---
    assert flag_value == "1"
```

**Variety booster:** stack `@pytest.mark.usefixtures("fixture_a", "fixture_b")` with `@pytest.mark.parametrize` to apply the same side-effect setup across a matrix of inputs without changing the test signature.

## Fixture Telemetry via Logging

[ref: #fixtures-telemetry]

```python
import logging
from collections.abc import Generator

import pytest


@pytest.fixture(autouse=True)
def _log_fixture_lifecycle(
    request: pytest.FixtureRequest,
) -> Generator[None, None, None]:
    """Emit DEBUG logs for every fixture setup and teardown."""
    logger = logging.getLogger("pytest.fixtures")
    logger.debug("Setting up %s", request.fixturename)
    yield
    logger.debug("Tearing down %s", request.fixturename)
```

Configure `caplog` or run pytest with `--log-cli-level=DEBUG` to capture these logs.

**Variety booster:** include the test node ID and fixture scope in log messages so a single autouse telemetry fixture can diagnose ordering bugs across `session`, `module`, and `function` scopes.
