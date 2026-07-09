---
subject: "Grab-bag of reusable test recipes for awkward constructs: context managers (entry/exit side effects, exceptions), decorators by wrapping dummies, factory fixtures returning `_make_*` closures, table-driven parametrization with `ids`/`pytest.param`/`indirect=True`/stacked decorators, stubs/spies/mocks/fakes, patch-where-consumed with `monkeypatch`, frozen time, and higher-level fixtures overridable at conftest/module/class."
index:
  - anchor: patterns-context-managers
    what: "Testing a context manager by asserting entry side effects, exit side effects, and exception propagation, using `pytest.raises(...)` when an exception is expected and `contextlib.nullcontext` to parametrize raise versus no-raise paths."
    problem: "Context manager must perform setup and teardown and either propagate or suppress exceptions across both raising and non-raising paths; entry side effect, exit side effect, rollback on raise, close regardless, nullcontext branch, resource cleanup."
    use_when: "Context manager has setup and teardown, raising and non raising paths both matter, and exception policy decides propagation or suppression; entry side effect, exit side effect, rollback on raise, close regardless, nullcontext branch, resource cleanup."
    avoid_when: "Do not test only the happy path; the parametrized example asserts `resource.closed is True` under both `pytest.raises(ValueError)` and `contextlib.nullcontext()`, so cover the exception path too and verify exit side effects such as rollback or close rather than assuming the context ran."
    expected: "Entry and exit side effects are verified and the resource is closed or rolled back in both the raising and non-raising paths, with `pytest.raises` and `nullcontext` covering each branch."
  - anchor: patterns-decorators
    what: "Testing a decorator by applying it to a dummy function and asserting side effects, argument mutation, return value, metadata preservation, and exception handling, with a fake or monkeypatched clock replacing `time.sleep`."
    problem: "Decorator wrapping behavior (args passed, return preserved, metadata kept, policy raised) must verify without slowing suite with real delays; dummy function, return preserved, policy raises, fake clock advance, metadata kept, no real sleep."
    use_when: "Decorator wraps function behavior, arguments return metadata and policy exceptions need assertion, and real delay would slow suite; dummy function, return preserved, policy raises, fake clock advance, metadata kept, no real sleep, decorator contract."
    avoid_when: "Do not call `time.sleep` to assert delays or recovery windows; the example advances a fake monotonic clock with `current_time = period * 2` instead of sleeping."
    expected: "The decorator preserves the wrapped function's return value, enforces its policy by raising on overflow, and recovers after the configured period, all verified without sleeping."
  - anchor: patterns-factory-fixtures
    what: "A fixture that returns a `_make_*` closure building entities on demand, using `faker` for unique data and registering created instances so persistent resources are cleaned up in fixture teardown."
    problem: "Test must create as many isolated uniquely-valued entities as needed without hardcoded data, while guaranteeing persistent resources factory created are released; make closure, override kwargs, unique fields, track created, teardown delete, distinct ids."
    use_when: "Test needs many isolated entities, unique values must generate without hardcoded data, and created persistent resources must release; make closure, override kwargs, unique fields, track created, teardown delete, distinct ids, factory fixture."
    avoid_when: "Do not skip teardown for factories that create persistent resources; the example records every instance in `created` and deletes each in teardown, so leaving created entities undeleted would leak state between tests."
    expected: "Tests build isolated entities with distinct ids via the factory, and every persistent resource the factory created is cleaned up in teardown."
  - anchor: patterns-parametrization
    what: "Table-driven tests with `@pytest.mark.parametrize`, providing `ids` for readable names, `pytest.param(..., id=..., marks=...)` for per-row marks or custom ids, `indirect=True`/`indirect=[...]` to route parameters through fixtures, and stacked decorators for a Cartesian product."
    problem: "Many input/output combinations and fixture configurations must cover with one test body instead of copy-pasting near-identical tests; readable ids, per-row mark, indirect fixture, stacked decorators, cartesian product, table-driven."
    use_when: "Many input output combinations share one body, copy paste near identical tests hides cases, and table ids show intent; readable ids, per row mark, indirect fixture, stacked decorators, cartesian product, table driven, parametrize matrix."
    avoid_when: "Do not duplicate test bodies for each input combination instead of parametrizing, and do not assume stacked `parametrize` decorators filter combinations (they produce the full Cartesian product, e.g. two roles times two flags yields four cases)."
    expected: "One parametrized test body covers every listed combination with readable `ids`, per-row marks via `pytest.param`, fixture-built inputs via `indirect`, and full combination coverage from stacked decorators."
  - anchor: patterns-test-doubles
    what: "Collaborator stand-ins chosen by intent — stubs return canned values, spies record calls, mocks assert interactions, and fakes are lightweight working implementations — with `monkeypatch` preferred for simple replacement and `unittest.mock.Mock`/`MagicMock` for interaction assertions."
    problem: "Unit must isolate from collaborators while verifying right level (return values, recorded calls, exact interactions) without over-specifying test; lightest double, stub return, spy record, mock interaction, fake working, intent match."
    use_when: "Unit must isolate from collaborators, required verification level differs across return values calls and interactions, and lightest double prevents over specification; lightest double, stub return, spy record, mock interaction, fake working, intent match, collaborator boundary."
    avoid_when: "Do not use a mock with interaction assertions when a simple stub return value would keep the test focused on the unit under test, and do not assert interactions with `monkeypatch` (use `Mock`/`MagicMock`); choose the lightest double that proves the behavior."
    expected: "The collaborator is replaced by the lightest double that fits the intent — stub for returns, mock for `assert_called_once_with`-style interaction checks, fake for working behavior — keeping the test focused on the unit."
  - anchor: patterns-monkeypatching
    what: "Replacing attributes, environment variables, and import paths at the point of use with `monkeypatch.setattr`, `monkeypatch.setenv`/`monkeypatch.delenv`, and `monkeypatch.syspath_prepend`, patching the imported name in the module under test rather than where it is defined."
    problem: "Collaborators, config, and import resolution must override temporarily with auto teardown, avoiding patching definition site instead of use site; use-site patch, auto restore, env override, syspath prepend, exact payload, definition-site trap."
    use_when: "Collaborators, config, or import resolution must override temporarily, patch must target use site, and teardown must restore automatically; use site patch, auto restore, env override, syspath prepend, exact payload, definition site trap, monkeypatch."
    avoid_when: "Do not patch where the object is defined instead of where it is used; the body states to patch the imported name in the module under test (e.g. `myapp.storage.upload_blob` as consumed), so patching the original definition module would leave the use site unmocked."
    expected: "The use-site attribute, environment variable, or import path is overridden for the test and auto-restored afterward, with the fake receiving the exact inputs the unit passes."
  - anchor: patterns-freezing-time
    what: "Making time-based code deterministic with `time-machine` (preferred) or `freezegun`, travelling to a fixed moment and shifting forward instead of calling `time.sleep`."
    problem: "Time-dependent transition (token expiry) must assert deterministically and instantly, without real wall-clock delays that slow and destabilize suite; freeze moment, shift forward, instant transition, no sleep, expiry assert, deterministic clock."
    use_when: "Time dependent transition must assert instantly, wall clock delay would flake, and frozen clock can shift deterministically; freeze moment, shift forward, instant transition, no sleep, expiry assert, deterministic clock, time travel."
    avoid_when: "Do not call `time.sleep` in tests to wait for expiry; the example freezes and shifts time with `time_machine.travel`/`traveller.shift(ttl)` so the transition is asserted without sleeping."
    expected: "Time-dependent transitions are asserted instantly and deterministically by freezing and shifting the clock, with no `time.sleep`."
  - anchor: patterns-dependency-injection
    what: "Composing pytest fixtures as the suite's dependency-injection container, building higher-level fixtures from lower-level ones (e.g. `repository` from `settings`) and overriding them at `conftest`, module, or class level when needed."
    problem: "Collaborators must wire into tests declaratively so each test receives fully constructed dependencies, and lower-level fixture swaps at coarser scope without rewriting tests; fixture composition, high-level from low, scope override, declarative wiring, generated config, no inline construct."
    use_when: "Collaborators must wire declaratively, each test receives constructed dependencies, and lower level fixture swaps at coarser scope without rewriting tests; fixture composition, high level from low, scope override, declarative wiring, generated config, no inline construct."
    avoid_when: "Do not construct dependencies inline in every test instead of composing fixtures, and do not hardcode wiring such as a fixed `db_url` (the example sources it from `fake.url()` via the `settings` fixture so the composition stays overridable)."
    expected: "Tests request fully wired dependencies through fixture composition, lower-level fixtures feed higher-level ones, and overrides at coarser scopes rewire behavior without touching test bodies."
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
