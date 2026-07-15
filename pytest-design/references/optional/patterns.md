---
subject: "Reusable recipes for awkward test constructs; `contextlib.nullcontext`, `pytest.raises`, decorator dummy wrapping, `_make_*` factory fixtures, `pytest.mark.parametrize` with `ids`/`pytest.param`/`indirect=True`/stacked decorators, stubs/spies/mocks/fakes, patch-where-consumed with `monkeypatch`, `time-machine`/`freezegun` frozen clock, fixture dependency injection, and multi-axis variety booster with per-row oracles."
index:
  - anchor: patterns-context-managers
    what: "Testing a context manager by asserting entry side effects, exit side effects, and exception propagation, using `pytest.raises(...)` for expected exceptions and `contextlib.nullcontext` to parametrize raise versus no-raise paths."
    problem: "Context manager performs setup and teardown and either propagates or suppresses exceptions across raising and non-raising paths, yet happy-path-only tests miss rollback behavior; exception policy, rollback on error, close regardless of raise, nullcontext branch, happy path trap."
    use_when: "The code under test is a context manager; both success and failure exit paths have observable behavior; exception propagation or suppression must be asserted; parametrizing raise versus no-raise paths would reduce duplication."
    avoid_when: "The context manager has no side effects on exit; only the success path is relevant; exceptions are not part of the contract; the recipe is applied only to assert normal return value."
    expected: "Entry and exit side effects are verified under both success and failure branches, and cleanup is asserted via `pytest.raises` and `contextlib.nullcontext`."
  - anchor: patterns-decorators
    what: "Testing a decorator by wrapping a dummy function and asserting side effects, argument mutation, return value preservation, metadata retention, and exception handling, with a fake or monkeypatched clock replacing `time.sleep`."
    problem: "Decorator wraps functions while preserving arguments, return values, metadata, and policy reactions, yet verifying recovery windows with real wall-clock delays slows and destabilizes suite; argument passthrough, return preservation, metadata retention, rate limit rejection, fake clock advance, delay-free recovery."
    use_when: "A decorator wraps callable objects; its behavior depends on arguments, return values, metadata, or exception policy; delay-based logic would require real sleeps without a fake clock."
    avoid_when: "The decorator is a pure syntactic wrapper with no behavior to assert; interaction assertions are needed instead of return or side-effect checks; real sleeps are acceptable in the test."
    expected: "Decorator preserves wrapped function return and metadata, enforces policy by raising on overflow, and recovers after the configured period, all verified without sleeping."
  - anchor: patterns-factory-fixtures
    what: "A fixture that returns a `_make_*` closure building entities on demand, using `faker` for unique data and registering created instances so persistent resources are cleaned up in fixture teardown."
    problem: "Test creates many isolated uniquely-valued entities on demand, but hardcoded values cause collisions and persistent resources created by factory leak when teardown misses them; generated unique values, persistent resource cleanup, custom overrides, builder reuse, factory teardown."
    use_when: "Multiple tests need distinct entities built from generated data; the builder creates persistent resources; teardown cleanup is required; per-test overrides are common."
    avoid_when: "Only one or two static entities are needed; the factory creates no persistent state; a simple fixture returning a single object suffices; generated data is not required."
    expected: "Tests build isolated entities with distinct ids via the factory, and every persistent resource the factory created is cleaned up during teardown."
  - anchor: patterns-parametrization
    what: "Table-driven tests with `@pytest.mark.parametrize`, providing `ids` for readable names, `pytest.param(..., id=..., marks=...)` for per-row marks or custom ids, `indirect=True`/`indirect=[...]` to route parameters through fixtures, and stacked decorators for a Cartesian product."
    problem: "Many input/output combinations and fixture configurations differ only in values, so copy-pasting near-identical tests across suite bloats coverage and hides missing cases; readable node ids, per-row marker, fixture-built parameter, dimension cross product, table-driven matrix."
    use_when: "Several cases share the same assertion body; readable node ids or per-row marks are needed; parameters must be constructed by fixtures; inputs multiply across independent dimensions."
    avoid_when: "Cases have different assertion logic; only one or two cases exist; the matrix would explode into an unmaintainable Cartesian product; fixture indirection is unnecessary."
    expected: "One parametrized test body covers every listed combination with readable `ids`, per-row marks via `pytest.param`, fixture-built inputs via `indirect`, and full combination coverage from stacked decorators."
  - anchor: patterns-test-doubles
    what: "Collaborator stand-ins chosen by intent — stubs return canned values, spies record calls, mocks assert interactions, and fakes are lightweight working implementations — with `monkeypatch` preferred for simple replacement and `unittest.mock.Mock`/`MagicMock` for interaction assertions."
    problem: "Unit depends on collaborators and needs stand-ins, but choosing wrong double over-specifies interactions or under-specifies behavior; unit boundary focus, intent-driven choice, over-specification trap, canned value stub, call recording spy, interaction mock, working implementation fake."
    use_when: "A unit under test has collaborators that must be replaced; the required assertion level is returns, recorded calls, or exact interactions; the lightest possible double should be selected."
    avoid_when: "Integration with the real collaborator is the behavior under test; only interaction counts matter and a stub would under-specify; the collaborator is simple enough to use as-is."
    expected: "Collaborator is replaced by the lightest double that fits the intent — stub for returns, mock for interaction checks, fake for working behavior — keeping the test focused on the unit."
  - anchor: patterns-monkeypatching
    what: "Replacing attributes, environment variables, and import paths at the point of use with `monkeypatch.setattr`, `monkeypatch.setenv`/`monkeypatch.delenv`, and `monkeypatch.syspath_prepend`, patching the imported name in the module under test rather than where it is defined."
    problem: "Collaborators, config, and import resolution require temporary override with automatic teardown, yet patching definition site instead of use site leaves test ineffective; use-site patch, auto restore, env override, import path shim, exact payload, definition-site trap."
    use_when: "A single test needs to temporarily swap an attribute, environment variable, or import path; the replacement must target the imported name inside the module under test; automatic cleanup after the test is required."
    avoid_when: "The patch target is the definition module rather than the imported use site; the test must assert interactions rather than just replace behavior; teardown must remain manual or span multiple tests."
    expected: "The use-site attribute, environment variable, or import path is overridden for the test and auto-restored afterward, with the fake receiving the exact inputs the unit passes."
  - anchor: patterns-freezing-time
    what: "Making time-based code deterministic with `time-machine` (preferred) or `freezegun`, travelling to a fixed moment and shifting forward instead of calling `time.sleep`."
    problem: "Time-dependent transition such as token expiry is hard to assert at exact boundary, and real wall-clock delays slow and destabilize suite; freeze moment, shift forward, instant transition, no real sleep, expiry boundary, predictable timeline, wall-clock flakiness."
    use_when: "Code behavior depends on time progression such as expiry, deadlines, or scheduling; tests must reach exact time boundaries instantly; real sleeps would slow or destabilize the suite."
    avoid_when: "Time is not a factor in the behavior under test; the test can be written with explicit timestamps; real wall-clock delay is acceptable or intended."
    expected: "Time-dependent transitions are asserted instantly and deterministically by freezing and shifting the clock, with no `time.sleep`."
  - anchor: patterns-dependency-injection
    what: "Composing pytest fixtures as the suite's dependency-injection container, building higher-level fixtures from lower-level ones (e.g. `repository` from `settings`) and overriding them at `conftest`, module, or class level when needed."
    problem: "Collaborators need declarative wiring so each test receives fully constructed dependencies, yet lower-level implementation changes force rewriting tests when fixtures are not layered; dependency graph, fixture layering, scope override, generated config, inline construction trap, swap without rewriting."
    use_when: "Multiple tests need the same fully constructed collaborators; lower-level implementations must be swappable at conftest, module, or class scope; test bodies should not contain wiring code."
    avoid_when: "Only one test needs the dependency; the wiring is a simple one-liner; swapping implementations is not anticipated; fixtures would add indirection without value."
    expected: "Tests request fully wired dependencies through fixture composition, lower-level fixtures feed higher-level ones, and overrides at coarser scopes rewire behavior without touching test bodies."
  - anchor: patterns-variety-booster
    what: "Combining parametrization with multiple axes of variation so one test body covers happy paths, edge cases, and error conditions, with each row carrying its own expected outcome and `pytest.param` attaching marks or xfail expectations."
    problem: "Happy path, edge cases, and error conditions often duplicate test shape while differing only in inputs and expected outcome, so suite bloats; multi-axis matrix, row-level expected value, boundary condition sweep, per-row mark, parametrized case table."
    use_when: "The same assertion logic covers happy paths, edge cases, and error conditions; expected outcome differs per row; individual rows need marks, custom ids, or xfail expectations."
    avoid_when: "Different cases require different assertion logic; the table would become too wide to read; per-row outcome cannot be expressed as a simple parameter."
    expected: "One parametrized body exercises every case, each row carries its expected outcome, and individual rows can be marked or xfailed without touching the body."
libraries:
  - pytest-lazy-fixtures
---

# Patterns

## Context Managers Testing

[ref: #patterns-context-managers]

Assert entry side effects, exit side effects, and exception handling.
Use `pytest.raises(...)` when the context manager is expected to propagate an exception.
Use `contextlib.nullcontext` for parametrized tests that toggle between a raising and a non-raising context.

```python
import pytest
from faker import Faker


def test_transaction_rolls_back_on_error(fake: Faker) -> None:
    """
    Given: a transaction context with a record insertion.
    When: a DatabaseError is raised inside the context.
    Then: the transaction rolls back and the record count is zero.
    """
    # --- Arrange ---
    # insert_record is called inside the transaction context.

    # --- Act ---
    with pytest.raises(DatabaseError):
        with transaction():
            insert_record()
            raise DatabaseError(fake.sentence())

    # --- Assert ---
    assert db.count("records") == 0
```

Parametrize "raise or not" with `nullcontext`:

```python
import contextlib
from typing import Any
import pytest
from faker import Faker


@pytest.mark.parametrize(
    "ctx,should_raise",
    [
        (pytest.raises(ValueError), True),
        (contextlib.nullcontext(), False),
    ],
)
def test_resource_closes_in_both_paths(
    fake: Faker,
    ctx: contextlib.AbstractContextManager[Any],
    should_raise: bool,
) -> None:
    """
    Given: a parametrized context and raise flag.
    When: a managed resource is used.
    Then: the resource is closed regardless of whether an exception is raised.
    """
    # --- Arrange ---
    resource = acquire_resource(fake.uuid4())

    # --- Act ---
    with ctx:
        with managed_resource(resource):
            if should_raise:
                raise ValueError(fake.sentence())

    # --- Assert ---
    assert resource.closed is True
```

## Decorators Testing

[ref: #patterns-decorators]

Test decorators by wrapping a dummy function and asserting on side effects, argument mutation, return value, metadata preservation, and exception handling.
Avoid `time.sleep` for delay assertions; inject or monkeypatch a clock.

```python
import time
from collections.abc import Callable
import pytest
from faker import Faker


class RateLimitExceeded(Exception):
    pass


def rate_limit(
    max_calls: int,
    period: float,
) -> Callable[[Callable[[], int]], Callable[[], int]]:
    def decorator(func: Callable[[], int]) -> Callable[[], int]:
        calls: list[float] = []

        def wrapper() -> int:
            now = time.monotonic()
            cutoff = now - period
            while calls and calls[0] < cutoff:
                calls.pop(0)
            if len(calls) >= max_calls:
                raise RateLimitExceeded
            calls.append(now)
            return func()

        return wrapper

    return decorator
```

```python
import time

import pytest
from faker import Faker


def test_rate_limiter_enforces_max_calls_and_recovery(
    fake: Faker,
    monkey: pytest.MonkeyPatch,
) -> None:
    """
    Given: a rate-limited function with a fake monotonic clock.
    When: it is called up to and beyond the limit, then after recovery time.
    Then: calls succeed up to max_calls, exceed raises, and recovery allows one more.
    """
    # --- Arrange ---
    expected = fake.pyint()
    max_calls = fake.pyint(min_value=1, max_value=3)
    period = fake.pyfloat(min_value=0.1, max_value=1.0, positive=True)
    current_time = 0.0

    def fake_monotonic() -> float:
        return current_time

    monkey.setattr(time, "monotonic", fake_monotonic)

    @rate_limit(max_calls=max_calls, period=period)
    def dummy() -> int:
        return expected

    # --- Act / Assert ---
    for _ in range(max_calls):
        assert dummy() == expected

    with pytest.raises(RateLimitExceeded):
        dummy()

    current_time = period * 2
    assert dummy() == expected
```

## Factory Fixtures

[ref: #patterns-factory-fixtures]

Fixtures can return a `_make_*` closure that builds entities on demand.
Use `faker` inside the factory for unique data.
If the factory creates persistent resources, clean them up in fixture teardown.

```python
from collections.abc import Callable
from typing import Any
import pytest
from faker import Faker


class User:
    def __init__(self, id: str, email: str, name: str) -> None:
        self.id = id
        self.email = email
        self.name = name
        self._deleted = False

    def delete(self) -> None:
        self._deleted = True


@pytest.fixture
def make_user(fake: Faker) -> Callable[..., User]:
    created: list[User] = []

    def _make_user(**overrides: Any) -> User:
        user = User(
            id=str(fake.uuid4()),
            email=fake.fake_email(),
            name=fake.name(),
            **overrides,
        )
        created.append(user)
        return user

    yield _make_user
    for user in created:
        user.delete()
```

```python
from collections.abc import Callable

from faker import Faker


def test_factory_creates_isolated_users(
    make_user: Callable[..., User],
    fake: Faker,
) -> None:
    """
    Given: a user factory fixture.
    When: two users are created with different emails.
    Then: they have distinct ids and are not marked deleted.
    """
    # --- Arrange ---
    first = make_user(email=fake.fake_email())
    second = make_user(email=fake.fake_email())

    # --- Act ---
    # Users are already created by the factory.

    # --- Assert ---
    assert first.id != second.id
    assert first._deleted is False
    assert second._deleted is False
```

## Parametrization

[ref: #patterns-parametrization]

Use `@pytest.mark.parametrize` for table-driven tests.
Provide `ids` for readable test names.
Use `pytest.param(..., id=..., marks=...)` for marks or custom ids.
Use `indirect=True` or `indirect=["fixture_name"]` to pass parameters through fixtures.
Multiple `@pytest.mark.parametrize` decorators produce a Cartesian product.

```python
import pytest


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("hello", "HELLO"),
        ("World", "WORLD"),
    ],
    ids=["lowercase", "mixed-case"],
)
def test_normalize_upper(raw: str, expected: str) -> None:
    """
    Given: a parametrized input string.
    When: normalize is called.
    Then: the result is uppercased.
    """
    # --- Arrange ---
    # raw and expected come from parametrization.

    # --- Act ---
    result = normalize(raw)

    # --- Assert ---
    assert result == expected
```

Indirect fixture parametrization:

```python
import pytest


class User:
    def __init__(self, age: int) -> None:
        self.age = age

    def can_vote(self) -> bool:
        return self.age >= 18


@pytest.fixture
def user(request: pytest.FixtureRequest) -> User:
    return User(age=request.param)


@pytest.mark.parametrize("user", [17, 21], indirect=True, ids=["minor", "adult"])
def test_can_vote(user: User) -> None:
    """
    Given: a user with parametrized age via indirect fixture.
    When: can_vote is checked.
    Then: the result matches the age threshold.
    """
    # --- Arrange ---
    # user is built indirectly from the parametrized age.

    # --- Act ---
    result = user.can_vote()

    # --- Assert ---
    assert result == (user.age >= 18)
```

Cartesian product:

```python
import pytest


class Account:
    def __init__(self, role: str, active: bool) -> None:
        self.role = role
        self.active = active

    def can_login(self) -> bool:
        return self.role == "admin" or self.active


@pytest.mark.parametrize("role", ["admin", "member"])
@pytest.mark.parametrize("is_active", [True, False])
def test_access_decision(role: str, is_active: bool) -> None:
    """
    Given: a parametrized role and active flag.
    When: account login permission is evaluated.
    Then: the result matches the business rule.
    """
    # --- Arrange ---
    account = Account(role=role, active=is_active)

    # --- Act ---
    result = account.can_login()

    # --- Assert ---
    assert result == (role == "admin" or is_active)
```

## Test Doubles

[ref: #patterns-test-doubles]

Distinguish by intent: stubs return canned values; spies record calls; mocks assert interactions; fakes are lightweight working implementations.
Prefer `monkeypatch` for simple attribute or environment replacement.
Use `unittest.mock.Mock` or `MagicMock` when you need to verify interactions.

```python
from collections.abc import Callable
from unittest.mock import Mock
import pytest
from faker import Faker


def send_email(to: str, body: str) -> None:
    raise NotImplementedError


class Notifier:
    def __init__(self, sender: Callable[[str, str], None]) -> None:
        self._sender = sender

    def notify(self, to: str, body: str) -> None:
        self._sender(to, body)


def test_notifier_sends_email(fake: Faker) -> None:
    """
    Given: a notifier with a mocked sender.
    When: notify is called with an address and body.
    Then: the sender is called once with the same arguments.
    """
    # --- Arrange ---
    mock_send = Mock(spec=send_email)
    notifier = Notifier(sender=mock_send)
    address = fake.fake_email()
    body = fake.sentence()

    # --- Act ---
    notifier.notify(address, body)

    # --- Assert ---
    mock_send.assert_called_once_with(address, body)
```

A stub keeps the test focused on the unit under test rather than the collaborator:

```python
from collections.abc import Callable
import pytest
from faker import Faker


class PricingCalculator:
    def __init__(self, discount_policy: Callable[[int], float]) -> None:
        self._discount_policy = discount_policy

    def final_price(self, price: int) -> float:
        return price - self._discount_policy(price)


def test_calculator_applies_configured_discount(fake: Faker) -> None:
    """
    Given: a calculator with a stub discount policy.
    When: final_price is computed.
    Then: the result equals price minus the discount amount.
    """
    # --- Arrange ---
    price = fake.pyint(min_value=10, max_value=100)
    discount = fake.pyfloat(min_value=0.0, max_value=1.0)
    calculator = PricingCalculator(discount_policy=lambda p: p * discount)

    # --- Act ---
    result = calculator.final_price(price)

    # --- Assert ---
    assert result == price - (price * discount)
```

## Monkeypatching

[ref: #patterns-monkeypatching]

Patch where the object is used (the imported name in the module under test), not where it is defined.
Use `monkeypatch.setattr` for attributes, `setenv`/`delenv` for environment variables, and `syspath_prepend` for import path manipulation.

```python
import os
import pytest
from faker import Faker


class APIClient:
    def __init__(self) -> None:
        self.api_key = os.getenv("API_KEY", "")


def test_client_reads_api_key_from_env(
    monkey: pytest.MonkeyPatch,
    fake: Faker,
) -> None:
    """
    Given: API_KEY is set in the environment.
    When: an APIClient is instantiated.
    Then: it reads the key from the environment.
    """
    # --- Arrange ---
    key = fake.uuid4()
    monkey.setenv("API_KEY", key)

    # --- Act ---
    client = APIClient()

    # --- Assert ---
    assert client.api_key == key
```

Patch an imported function where it is consumed:

```python
import pytest
from faker import Faker
from myapp.storage import FileService


def test_upload_calls_storage_backend(
    fake: Faker,
    monkey: pytest.MonkeyPatch,
) -> None:
    """
    Given: the storage backend is monkeypatched to a fake.
    When: a payload is stored.
    Then: the fake receives the exact payload.
    """
    # --- Arrange ---
    captured: list[bytes] = []

    def fake_upload(data: bytes) -> str:
        captured.append(data)
        return str(fake.uuid4())

    monkey.setattr("myapp.storage.upload_blob", fake_upload)
    service = FileService()
    payload = fake.binary(length=16)

    # --- Act ---
    service.store(payload)

    # --- Assert ---
    assert captured == [payload]
```

## Freezing Time

[ref: #patterns-freezing-time]

Use `time-machine` (preferred) or `freezegun` to make time-based code deterministic.
Avoid `time.sleep` in tests.

```python
import datetime
from dataclasses import dataclass
import time_machine
import pytest
from faker import Faker


@dataclass
class Token:
    created_at: datetime.datetime
    ttl: datetime.timedelta

    def is_expired(self) -> bool:
        return datetime.datetime.now() > self.created_at + self.ttl


def create_token(created_at: datetime.datetime, ttl: datetime.timedelta) -> Token:
    return Token(created_at=created_at, ttl=ttl)


def test_token_expires_after_ttl(fake: Faker) -> None:
    """
    Given: a token created at a frozen moment with a TTL.
    When: time shifts forward by the TTL.
    Then: the token transitions from not expired to expired.
    """
    # --- Arrange ---
    created_at = fake.date_time()
    ttl_hours = fake.pyint(min_value=1, max_value=24)
    ttl = datetime.timedelta(hours=ttl_hours)

    # --- Act / Assert ---
    with time_machine.travel(created_at, tick=False) as traveller:
        token = create_token(created_at=created_at, ttl=ttl)
        assert token.is_expired() is False

        traveller.shift(ttl)
        assert token.is_expired() is True
```

## Dependency Injection via Fixtures

[ref: #patterns-dependency-injection]

Fixtures are pytest's dependency injection container.
Build higher-level fixtures from lower-level ones and override them at `conftest`, module, or class level when needed.

```python
from dataclasses import dataclass
import pytest
from faker import Faker


@dataclass
class Item:
    id: str
    name: str


class Settings:
    def __init__(self, db_url: str) -> None:
        self.db_url = db_url


class Repository:
    def __init__(self, db_url: str) -> None:
        self.db_url = db_url
        self._items: dict[str, Item] = {}

    def save(self, item: Item) -> None:
        self._items[item.id] = item

    def get(self, item_id: str) -> Item | None:
        return self._items.get(item_id)


@pytest.fixture
def settings(fake: Faker) -> Settings:
    return Settings(db_url=fake.url())


@pytest.fixture
def repository(settings: Settings) -> Repository:
    return Repository(settings.db_url)


def test_repository_saves_and_retrieves_item(
    repository: Repository,
    fake: Faker,
) -> None:
    """
    Given: an in-memory repository.
    When: an item is saved and retrieved.
    Then: the retrieved item equals the saved item.
    """
    # --- Arrange ---
    item = Item(id=str(fake.uuid4()), name=fake.word())

    # --- Act ---
    repository.save(item)

    # --- Assert ---
    assert repository.get(item.id) == item
```

## Variety Booster

[ref: #patterns-variety-booster]

Cover more invariants with less code by combining parametrization with multiple axes of variation.
A single test can exercise happy paths, edge cases, and error conditions when each row carries its own expected outcome.
Use `pytest.param` to attach marks, ids, or xfail expectations to individual rows.

```python
import pytest
from faker import Faker


class Account:
    def __init__(self, account_id: str, role: str, active: bool) -> None:
        self.account_id = account_id
        self.role = role
        self.active = active

    def can_login(self) -> bool:
        return self.role == "admin" or self.active


@pytest.mark.parametrize(
    "role,active,expected",
    [
        ("admin", False, True),
        ("member", True, True),
        ("member", False, False),
        pytest.param(
            "guest",
            True,
            False,
            marks=pytest.mark.xfail(reason="guest role not implemented"),
        ),
    ],
)
def test_login_permission_matrix(
    role: str,
    active: bool,
    expected: bool,
    fake: Faker,
) -> None:
    """
    Given: a parametrized role and active flag.
    When: account login permission is evaluated.
    Then: the result matches the expected boolean.
    """
    # --- Arrange ---
    account = Account(account_id=str(fake.uuid4()), role=role, active=active)

    # --- Act ---
    result = account.can_login()

    # --- Assert ---
    assert result == expected
```
