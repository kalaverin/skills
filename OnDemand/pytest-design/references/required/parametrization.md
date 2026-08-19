---
subject: "Scale coverage while shrinking test code: `@pytest.mark.parametrize` with `pytest.param(..., id=..., marks=...)`, stacked decorators for Cartesian products, `fixture(params=...)` with custom `ids`, `indirect=True`, `lazy_fixture` from `pytest-lazy-fixtures`, `pytest_generate_tests` driven by CLI/env/files, combine with Hypothesis, and collapse `if/elif` ladders and duplicated tests into one parametrized body."
index:
  - anchor: parametrization-parametrize-basics
    what: "`@pytest.mark.parametrize` with `pytest.param(..., id=..., marks=...)` that runs one assertion body against a declared list of concrete cases with explicit identifiers and per-case markers."
    problem: "Writing one test per case duplicates identical bodies and hides which cases share assertion, while branching on labels inside test buries inputs in branches; case label branching, row-level marker, stable node ids, finite static vectors, shared assertion body."
    use_when: "Cases are static, finite, and known at import time; one assertion body serves every row; rows need stable ids or per-case marks."
    avoid_when: "Branch logic reconstructs inputs from case labels inside test body; separate tests cloned for each row; inputs stored in branches instead of parameter or fixture."
    expected: "One parametrized body covers every declared case with stable ids and per-case marks, inputs live in parameters or fixtures rather than in-branch reconstruction."
  - anchor: parametrization-cartesian-product
    what: "Stacking multiple `@pytest.mark.parametrize` decorators so pytest generates the full Cartesian product of independent dimensions."
    problem: "Multi-dimensional contracts (access-control matrices, feature-flag combos) need every dimension combination covered without hand-writing each row, yet invalid combinations must not hide intent; access matrix oracle, feature flag combos, invalid combination trap, combinatorial explosion, explicit row clarity, dimension independence."
    use_when: "Contract dimensions multiply independently; full cross-product carries business meaning; invalid combinations are few enough to filter via explicit rows."
    avoid_when: "Most product combinations invalid or nonsensical for business; stacked decorators used where explicit rows would give clearer failure message; dimensions are not independent."
    expected: "Every combination of independent dimensions runs as its own case, while mostly-invalid spaces are expressed as explicit rows for clearer failures."
  - anchor: parametrization-parametrized-fixtures
    what: "Moving shared parameter variations into `@pytest.fixture(params=..., ids=...)` so one declaration feeds many tests with the same matrix."
    problem: "Cross-cutting variations (backends, formats, transports) declared per-test duplicate same matrix across suite and drift out of sync; backend format transport sweep, per-test matrix duplication, fixture chain multiplication, local variation only, custom ids function, suite-wide consistency."
    use_when: "Same matrix feeds many tests across modules; fixture chaining multiplies dimensions without touching bodies; ids need consistent naming everywhere."
    avoid_when: "Parametrized fixture created for variation only one test cares about; matrix duplicated locally because shared fixture was not extracted; ids ad-hoc and inconsistent."
    expected: "A single parametrized fixture feeds the whole suite's shared matrix, and one-off variations stay local to their test."
  - anchor: parametrization-indirect
    what: "`indirect=True` (or `indirect=['fixture_name']`) routes the parameterized value into a fixture (via `request.param`) that builds a complex dependency instead of passing it straight to the test."
    problem: "Complex dependencies (authenticated clients, databases, feature-flag configs) must construct per case, which test cannot do from raw scalar; authenticated client matrix, database per case, feature flag config, raw scalar limit, request param access, guard hasattr misuse."
    use_when: "Dependency construction needs fixtures, config, or teardown that test should not duplicate; parameter value is raw scalar that cannot stand alone; same fixture reused with different parameters."
    avoid_when: "Indirect route used for simple scalar the test could consume directly; fixture logic duplicated because indirect was skipped; `request.param` assumed present without guard."
    expected: "The parameterized value drives a fixture that builds the complex dependency per case, while simple scalars are still passed directly to the test."
  - anchor: parametrization-lazy-fixtures
    what: "`lazy_fixture('fixture_name')` (from `pytest-lazy-fixtures`, which must be installed) lets a parameterized value resolve to a fully initialized fixture instance at collection/runtime."
    problem: "Parameter sometimes needs to be fixture instance (admin versus guest user), which plain values cannot express without running fixture setup; admin guest user switch, initialized fixture state, collection runtime resolution, external plugin dependency, ordinary value parameter."
    use_when: "Parameter must be fully initialized fixture object (e.g., user with role); same table mixes fixture instances with static values; plugin available in environment."
    avoid_when: "`lazy_fixture` used for plain values that are not fixtures; plugin not installed or not declared as dependency; fixture instance needed but resolved too late."
    expected: "Fixture instances participate as parameters alongside static values, with non-fixture values kept as ordinary parameters."
  - anchor: parametrization-dynamic
    what: "The `pytest_generate_tests(metafunc)` hook that builds test cases at collection time from CLI options, environment variables, external files, or runtime discovery via `metafunc.parametrize`."
    problem: "Some case lists are not known until collection time and cannot be written as static decorator rows, so data sources outside code must drive cases; cli option driven, env var driven, external file dataset, runtime enumeration, fixture name filter, static matrix alternative."
    use_when: "Case list comes from CLI, environment, file, or runtime scan; matrix cannot be expressed statically; cases filtered by fixture names for focused suites."
    avoid_when: "Static matrix expressible directly in decorators is pushed into `pytest_generate_tests`; external data source required for trivial cases; hook logic untested or duplicates fixture filtering."
    expected: "Collection-time data drives parametrization for genuinely dynamic case lists, while static matrices stay in decorators."
  - anchor: parametrization-anti-patterns
    what: "Replacing in-test `if`/`elif` input-reconstruction ladders and copy-pasted near-identical tests with builder/expected mappings and parametrized fixtures."
    problem: "Branching on case labels inside test and duplicating tests per backend, role, or environment both hide variation and bloat suite; if elif ladder, copy pasted clone, builder expected mapping, case library dataclass, backend role environment sweep."
    use_when: "Test body contains if/elif branches on case labels or near-identical tests per backend/role/environment; builder/expected mappings or parametrized fixtures can replace both smells."
    avoid_when: "Tests cloned per backend or role instead of folded into parametrization; branch logic reconstructed inside parametrized body; parametrization table so large it needs its own CaseLibrary dataclass but none extracted."
    expected: "Case logic lives in builder/expected mappings and parametrized fixtures, so one test body covers every backend, role, and environment with no in-test branching or duplication."
libraries:
  - pytest-lazy-fixtures
---

# PARAMETRIZATION

Parametrization lets one test declaration exercise many concrete cases, so the suite stays small while coverage grows.

## `@pytest.mark.parametrize` with `pytest.param` and IDs

[ref: #parametrization-parametrize-basics]

Use `@pytest.mark.parametrize` with `pytest.param` to run the same assertion body against a declared list of concrete cases while controlling identifiers and per-case markers.

Use this for static, finite test vectors whose expected results are known at import time.

Avoid embedding `if`/`elif` logic that reconstructs inputs from a case label; put the real input into the parameter or into a fixture.

```python
from enum import StrEnum

import pytest
from faker import Faker


class Tier(StrEnum):
    STANDARD = "standard"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


class Priority(StrEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


# In a real project this mapping lives in application-level constants.
TIER_PRIORITIES: dict[Tier, Priority] = {
    Tier.STANDARD: Priority.NORMAL,
    Tier.PREMIUM: Priority.HIGH,
}


def priority_for_tier(tier: Tier) -> Priority:
    try:
        return TIER_PRIORITIES[tier]
    except KeyError as exc:
        raise LookupError(
            f"priority not configured for tier {tier.value!r}",
        ) from exc


@pytest.mark.parametrize(
    "tier,expected_priority",
    [
        pytest.param(Tier.STANDARD, Priority.NORMAL, id="standard-is-normal"),
        pytest.param(Tier.PREMIUM, Priority.HIGH, id="premium-is-high"),
        pytest.param(
            Tier.ENTERPRISE,
            Priority.HIGH,
            id="enterprise-is-high",
            marks=pytest.mark.xfail(
                raises=LookupError,
                reason="enterprise tier mapping still under review",
            ),
        ),
    ],
)
def test_priority_for_tier_returns_expected_value(
    tier: Tier,
    expected_priority: Priority,
    fake: Faker,
) -> None:
    """
    Given: parametrized tier and expected priority.
    When: priority is resolved for the tier.
    Then: result matches expected priority.
    """
    # --- Arrange ---
    request_id = fake.uuid4()

    # --- Act ---
    result = priority_for_tier(tier)

    # --- Assert ---
    assert result is expected_priority, request_id
```

**Variety booster:** combine `pytest.param` with `pytest.mark.skipif` to skip cases on specific platforms, or with `pytest.mark.xfail` to document known bugs while keeping the test body identical.

## Cartesian Product by Stacking Decorators

[ref: #parametrization-cartesian-product]

Stack multiple `@pytest.mark.parametrize` decorators to generate the full Cartesian product of independent dimensions.

Use this for access-control matrices, feature-flag combinations, or any contract whose dimensions multiply.

Avoid stacking when most combinations are invalid; explicit rows keep failure messages closer to business intent.

```python
from enum import StrEnum

import pytest
from faker import Faker


class Role(StrEnum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class Resource(StrEnum):
    DOCUMENT = "document"
    IMAGE = "image"
    SPREADSHEET = "spreadsheet"


class Action(StrEnum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"


# Application-level oracle; the real service must match it.
def is_allowed(role: Role, resource: Resource, action: Action) -> bool:
    if role is Role.ADMIN:
        return True
    if role is Role.VIEWER and action is Action.READ:
        return True
    if role is Role.EDITOR and action in (Action.READ, Action.WRITE):
        return True
    return False


class AccessControl:
    def check(self, actor_id: str, role: Role, resource: Resource, action: Action) -> bool:
        return is_allowed(role, resource, action)


@pytest.mark.parametrize(
    "role",
    [
        pytest.param(Role.ADMIN, id="role-admin"),
        pytest.param(Role.EDITOR, id="role-editor"),
        pytest.param(Role.VIEWER, id="role-viewer"),
    ],
)
@pytest.mark.parametrize(
    "resource",
    [
        pytest.param(Resource.DOCUMENT, id="res-document"),
        pytest.param(Resource.IMAGE, id="res-image"),
        pytest.param(Resource.SPREADSHEET, id="res-spreadsheet"),
    ],
)
@pytest.mark.parametrize(
    "action",
    [
        pytest.param(Action.READ, id="act-read"),
        pytest.param(Action.WRITE, id="act-write"),
        pytest.param(Action.DELETE, id="act-delete"),
    ],
)
def test_permission_matrix_matches_oracle(
    role: Role,
    resource: Resource,
    action: Action,
    fake: Faker,
) -> None:
    """
    Given: parametrized role, resource, action, and generated actor.
    When: access control checks the permission.
    Then: result matches the oracle.
    """
    # --- Arrange ---
    actor_id = fake.uuid4()
    service = AccessControl()

    # --- Act ---
    result = service.check(actor_id, role, resource, action)

    # --- Assert ---
    expected = is_allowed(role, resource, action)
    assert result is expected
```

**Variety booster:** extract an application-level `is_allowed` oracle and run the matrix against both the service and the oracle; the same test body then validates correctness and prevents implementation drift.

## Parametrized Fixtures (`fixture(params=...)`)

[ref: #parametrization-parametrized-fixtures]

Move parameter variations into a fixture when many tests need the same matrix, so a single declaration feeds the whole suite.

Use this for cross-cutting concerns such as storage backends, serialization formats, or transport clients.

Avoid creating a parametrized fixture for a variation that only one test cares about; keep local knowledge local.

```python
from enum import StrEnum

import pytest
from faker import Faker


class Backend(StrEnum):
    MEMORY = "memory"
    SQLALCHEMY = "sqlalchemy"


class Repository:
    def __init__(self, backend: Backend, namespace: str) -> None:
        self._backend = backend
        self._namespace = namespace
        self._items: dict[str, str] = {}

    def add(self, key: str, value: str) -> None:
        self._items[key] = value

    def get(self, key: str) -> str:
        try:
            return self._items[key]
        except KeyError as exc:
            raise KeyError(f"no item for key {key!r}") from exc


@pytest.fixture(
    params=[Backend.MEMORY, Backend.SQLALCHEMY],
    ids=lambda backend: backend.value,
)
def backend(request: pytest.FixtureRequest) -> Backend:
    return request.param


@pytest.fixture
def repo(backend: Backend, fake: Faker) -> Repository:
    return Repository(backend=backend, namespace=fake.pystr(min_chars=8, max_chars=16))


def test_repo_persists_item(repo: Repository, fake: Faker) -> None:
    """
    Given: parametrized repository backend and generated key/value.
    When: item is added and retrieved.
    Then: stored value is returned.
    """
    # --- Arrange ---
    key = fake.uuid4()
    value = fake.sentence()

    # --- Act ---
    repo.add(key, value)

    # --- Assert ---
    assert repo.get(key) == value
```

**Variety booster:** chain parametrized fixtures, for example `repo(repo_backend, namespace)` or `client(auth_backend, api_version)`, so each new dimension multiplies coverage without touching test bodies.

## Indirect Parametrization

[ref: #parametrization-indirect]

Use `indirect=True` (or `indirect=["fixture_name"]`) when the parameterized value should be consumed by a fixture that builds a test dependency, not passed directly to the test function.

Use this to vary the construction of complex objects such as authenticated clients, databases, or feature-flag configurations.

Avoid indirect parametrization for simple scalar values that the test can use unchanged.

```python
from dataclasses import dataclass
from enum import StrEnum
from typing import Final

import pytest
from faker import Faker


class Role(StrEnum):
    ADMIN = "admin"
    EDITOR = "editor"


USER_ENDPOINT: Final[str] = "/users"
OK_STATUS: Final[int] = 200
FORBIDDEN_STATUS: Final[int] = 403


@dataclass(frozen=True)
class Response:
    status_code: int


@dataclass(frozen=True)
class Client:
    role: Role
    base_url: str
    token: str

    def get(self, path: str) -> Response:
        if self.role in (Role.ADMIN, Role.EDITOR):
            return Response(status_code=OK_STATUS)
        return Response(status_code=FORBIDDEN_STATUS)


@pytest.fixture
def authenticated_client(request: pytest.FixtureRequest, fake: Faker) -> Client:
    if not hasattr(request, "param"):
        pytest.fail("authenticated_client must be used with indirect parametrization")
    role = request.param
    return Client(role=role, base_url=fake.uri_path(), token=fake.uuid4())


@pytest.mark.parametrize(
    "authenticated_client",
    [
        pytest.param(Role.ADMIN, id="role-admin"),
        pytest.param(Role.EDITOR, id="role-editor"),
    ],
    indirect=True,
)
def test_user_endpoint_returns_ok_for_privileged_role(
    authenticated_client: Client,
) -> None:
    """
    Given: authenticated client with a privileged role.
    When: user endpoint is requested.
    Then: response status is OK.
    """
    # --- Arrange ---
    # Client built by indirect parametrized fixture.

    # --- Act ---
    response = authenticated_client.get(USER_ENDPOINT)

    # --- Assert ---
    assert response.status_code == OK_STATUS
```

**Variety booster:** compose indirect parametrization with fixture caching by scope, for example a session-scoped `database_url` fixture indirectly parameterized to run the whole suite against PostgreSQL and SQLite.

## `pytest-lazy-fixtures`

[ref: #parametrization-lazy-fixtures]

**Plugin:** `pytest-lazy-fixtures` must be installed.

Use `lazy_fixture("fixture_name")` when a parameterized value must be a fixture instance resolved at collection or runtime.

Use this to switch between fully initialized fixtures, such as an admin user versus a guest user, inside the same `@pytest.mark.parametrize` table.

Avoid `lazy_fixture` for values that are not fixtures; pass them as ordinary parameters.

```python
from dataclasses import dataclass
from enum import StrEnum

import pytest
from faker import Faker
from pytest_lazy_fixtures import lf as lazy_fixture


class Role(StrEnum):
    ADMIN = "admin"
    GUEST = "guest"
    SYSTEM = "system"


@dataclass(frozen=True)
class User:
    role: Role
    name: str


@dataclass(frozen=True)
class Dashboard:
    def render_for(self, user: User) -> str:
        return f"dashboard for {user.name}"


@pytest.fixture
def admin_user(fake: Faker) -> User:
    return User(role=Role.ADMIN, name=fake.name())


@pytest.fixture
def guest_user(fake: Faker) -> User:
    return User(role=Role.GUEST, name=fake.name())


@pytest.fixture
def system_user(fake: Faker) -> User:
    return User(role=Role.SYSTEM, name=fake.name())


@pytest.fixture
def dashboard() -> Dashboard:
    return Dashboard()


@pytest.mark.parametrize(
    "user",
    [
        pytest.param(lazy_fixture("admin_user"), id="admin-user"),
        pytest.param(lazy_fixture("guest_user"), id="guest-user"),
    ],
)
def test_dashboard_renders_for_any_user(user: User, dashboard: Dashboard) -> None:
    """
    Given: parametrized user and dashboard fixtures.
    When: dashboard is rendered for the user.
    Then: rendered output is not None.
    """
    # --- Arrange ---
    # Parameters provided by fixtures and parametrization.

    # --- Act ---
    rendered = dashboard.render_for(user)

    # --- Assert ---
    assert rendered is not None
```

**Variety booster:** pair `lazy_fixture` with a parametrized fixture to mix dynamic fixture values with static matrix values, such as `[lazy_fixture("admin_user"), lazy_fixture("guest_user"), lazy_fixture("system_user")]`.

## Dynamic Parametrization with `pytest_generate_tests`

[ref: #parametrization-dynamic]

Use `pytest_generate_tests(metafunc)` to build test cases from CLI options, environment variables, external files, or runtime discovery.

Use this when the case list is not known until collection time.

Avoid it for static matrices that can be expressed directly in decorators; explicit decorators are easier to trace and reuse.

```python
import json
import os
from pathlib import Path
from typing import Any, Final

import pytest
from faker import Faker


TEST_DATA_DIR_OPTION: Final[str] = "--test-data-dir"
TEST_DATA_DIR_ENV: Final[str] = "PYTEST_TEST_DATA_DIR"
WITHDRAWAL_FILE: Final[str] = "withdrawals.json"
CASE_ID_FIELD: Final[str] = "id"
CASE_EXPECTED_FIELD: Final[str] = "expected"
CASE_AMOUNT_FIELD: Final[str] = "amount"
SUCCESS_VALUE: Final[str] = "success"
REJECTED_VALUE: Final[str] = "rejected"
INSUFFICIENT_FUNDS_MESSAGE: Final[str] = "insufficient funds"


def pytest_addoption(parser: pytest.Parser) -> None:
    default_dir = os.environ.get(TEST_DATA_DIR_ENV)
    parser.addoption(
        TEST_DATA_DIR_OPTION,
        action="store",
        default=default_dir,
        help="Directory that contains JSON test-case files.",
    )


def _load_cases(metafunc: pytest.Metafunc) -> list[dict[str, Any]]:
    data_dir = metafunc.config.getoption(TEST_DATA_DIR_OPTION)
    if not data_dir:
        raise RuntimeError(
            f"{TEST_DATA_DIR_OPTION} or {TEST_DATA_DIR_ENV} is required",
        )
    cases_path = Path(data_dir) / WITHDRAWAL_FILE
    return json.loads(cases_path.read_text())


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    cases = _load_cases(metafunc)

    if "successful_withdrawal_case" in metafunc.fixturenames:
        success_cases = [
            case for case in cases if case[CASE_EXPECTED_FIELD] == SUCCESS_VALUE
        ]
        metafunc.parametrize(
            "successful_withdrawal_case",
            success_cases,
            ids=[case[CASE_ID_FIELD] for case in success_cases],
        )

    if "rejected_withdrawal_case" in metafunc.fixturenames:
        rejected_cases = [
            case for case in cases if case[CASE_EXPECTED_FIELD] == REJECTED_VALUE
        ]
        metafunc.parametrize(
            "rejected_withdrawal_case",
            rejected_cases,
            ids=[case[CASE_ID_FIELD] for case in rejected_cases],
        )


class WithdrawalError(Exception):
    ...


class Account:
    def __init__(self, balance: int) -> None:
        self.balance = balance

    def withdraw(self, amount: int) -> None:
        if amount > self.balance:
            raise WithdrawalError(INSUFFICIENT_FUNDS_MESSAGE)
        self.balance -= amount


def test_successful_withdrawal_is_accepted(
    successful_withdrawal_case: dict[str, Any],
    fake: Faker,
) -> None:
    """
    Given: withdrawal case with amount and account with surplus balance.
    When: withdrawal is executed.
    Then: account balance remains non-negative.
    """
    # --- Arrange ---
    amount = successful_withdrawal_case[CASE_AMOUNT_FIELD]
    account = Account(balance=amount + fake.pyint(min_value=1, max_value=1000))

    # --- Act ---
    account.withdraw(amount)

    # --- Assert ---
    assert account.balance >= 0


def test_rejected_withdrawal_raises_insufficient_funds(
    rejected_withdrawal_case: dict[str, Any],
    fake: Faker,
) -> None:
    """
    Given: withdrawal case with amount and account with insufficient balance.
    When: withdrawal is executed.
    Then: WithdrawalError is raised with insufficient funds message.
    """
    # --- Arrange ---
    amount = rejected_withdrawal_case[CASE_AMOUNT_FIELD]
    headroom = fake.pyint(min_value=1, max_value=max(1, amount))
    account = Account(balance=amount - headroom)

    # --- Act ---
    with pytest.raises(WithdrawalError, match=INSUFFICIENT_FUNDS_MESSAGE):
        account.withdraw(amount)

    # --- Assert ---
    # Exception raised as expected; assertion handled by pytest.raises context.
```

**Variety booster:** filter cases inside `pytest_generate_tests` by tags in the external file, so the same dataset drives focused suites such as `smoke`, `regression`, or `edge` without duplicating test code.

## Anti-patterns: if/elif Ladders and Duplicated Tests

[ref: #parametrization-anti-patterns]

Do not let `if`/`elif` ladders reconstruct test inputs inside a parametrized test; the branch logic belongs in a fixture, a factory, or the parametrization table itself.

Do not copy and paste near-identical test functions for each backend, role, or environment; extract the variation into a parametrized fixture.

### Replacing if/elif ladders

Replace branching on case labels with a mapping of case to builder, and let a parametrized fixture or `@pytest.mark.parametrize` table drive the cases.

```python
from collections.abc import Callable
from enum import StrEnum

import pytest
from faker import Faker


class EmailCase(StrEnum):
    VALID = "valid"
    MISSING_AT = "missing-at"
    SPACES = "spaces"
    EMPTY = "empty"
    NONE = "none"


def is_valid_email(value: str | None) -> bool:
    if value is None:
        return False
    parts = value.split("@")
    return len(parts) == 2 and all(parts) and " " not in parts[0]


_EMAIL_BUILDERS: dict[EmailCase, Callable[[Faker], str | None]] = {
    EmailCase.VALID: lambda fake: fake.fake_email(),
    EmailCase.MISSING_AT: lambda fake: fake.domain_name(),
    EmailCase.SPACES: lambda fake: f"{fake.user_name()} {fake.fake_email()}",
    EmailCase.EMPTY: lambda fake: fake.pystr(min_chars=0, max_chars=0),
    EmailCase.NONE: lambda fake: None,
}

_EMAIL_EXPECTED: dict[EmailCase, bool] = {
    EmailCase.VALID: True,
    EmailCase.MISSING_AT: False,
    EmailCase.SPACES: False,
    EmailCase.EMPTY: False,
    EmailCase.NONE: False,
}


@pytest.fixture(params=list(EmailCase), ids=lambda case: case.value)
def email_case(
    request: pytest.FixtureRequest,
    fake: Faker,
) -> tuple[EmailCase, str | None, bool]:
    case = request.param
    return case, _EMAIL_BUILDERS[case](fake), _EMAIL_EXPECTED[case]


def test_email_validator_accepts_valid_and_rejects_invalid(
    email_case: tuple[EmailCase, str | None, bool],
) -> None:
    """
    Given: parametrized email case, value, and expected validity.
    When: value is validated.
    Then: result matches expected validity.
    """
    # --- Arrange ---
    _case, value, expected = email_case

    # --- Act ---
    result = is_valid_email(value)

    # --- Assert ---
    assert result is expected
```

**Variety booster:** extract the builder and expected mappings into a shared `CaseLibrary` dataclass, then reuse the same pattern for phone numbers, URLs, or identifiers by swapping only the enum and builder functions.

### Replacing duplicated tests

Before: two nearly identical tests that differ only by the backend they instantiate.

```python
from enum import StrEnum

import pytest
from faker import Faker


class Backend(StrEnum):
    MEMORY = "memory"
    SQLALCHEMY = "sqlalchemy"


class Repository:
    def __init__(self, backend: Backend, namespace: str) -> None:
        self._backend = backend
        self._namespace = namespace
        self._items: dict[str, str] = {}

    def add(self, key: str, value: str) -> None:
        self._items[key] = value

    def get(self, key: str) -> str:
        try:
            return self._items[key]
        except KeyError as exc:
            raise KeyError(f"no item for key {key!r}") from exc


def test_repo_persists_item_in_memory(fake: Faker) -> None:
    """
    Given: in-memory repository backend and generated key/value.
    When: item is added and retrieved.
    Then: stored value is returned.
    """
    # --- Arrange ---
    repo = Repository(Backend.MEMORY, namespace=fake.pystr(min_chars=8, max_chars=16))
    key = fake.uuid4()
    value = fake.sentence()

    # --- Act ---
    repo.add(key, value)

    # --- Assert ---
    assert repo.get(key) == value


def test_repo_persists_item_in_sqlalchemy(fake: Faker) -> None:
    """
    Given: sqlalchemy repository backend and generated key/value.
    When: item is added and retrieved.
    Then: stored value is returned.
    """
    # --- Arrange ---
    repo = Repository(Backend.SQLALCHEMY, namespace=fake.pystr(min_chars=8, max_chars=16))
    key = fake.uuid4()
    value = fake.sentence()

    # --- Act ---
    repo.add(key, value)

    # --- Assert ---
    assert repo.get(key) == value
```

After: one test fed by a parametrized `backend` fixture.

```python
from enum import StrEnum

import pytest
from faker import Faker


class Backend(StrEnum):
    MEMORY = "memory"
    SQLALCHEMY = "sqlalchemy"


class Repository:
    def __init__(self, backend: Backend, namespace: str) -> None:
        self._backend = backend
        self._namespace = namespace
        self._items: dict[str, str] = {}

    def add(self, key: str, value: str) -> None:
        self._items[key] = value

    def get(self, key: str) -> str:
        try:
            return self._items[key]
        except KeyError as exc:
            raise KeyError(f"no item for key {key!r}") from exc


@pytest.fixture(params=[Backend.MEMORY, Backend.SQLALCHEMY], ids=lambda backend: backend.value)
def backend(request: pytest.FixtureRequest) -> Backend:
    return request.param


@pytest.fixture
def repo(backend: Backend, fake: Faker) -> Repository:
    return Repository(backend=backend, namespace=fake.pystr(min_chars=8, max_chars=16))


def test_repo_persists_item(repo: Repository, fake: Faker) -> None:
    """
    Given: parametrized repository backend and generated key/value.
    When: item is added and retrieved.
    Then: stored value is returned.
    """
    # --- Arrange ---
    key = fake.uuid4()
    value = fake.sentence()

    # --- Act ---
    repo.add(key, value)

    # --- Assert ---
    assert repo.get(key) == value
```

**Variety booster:** chain parametrized fixtures, for example `repo(repo_backend, namespace)` or `client(auth_backend, api_version)`, so each new dimension multiplies coverage without touching test bodies.
