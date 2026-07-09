---
subject: "Exercise modern Python in tests: PEP 695 `type` aliases/generics, `TypedDict` `Required`/`NotRequired`/`Unpack`, `@override`, manual `ExceptionGroup` asserts or `pytest.RaisesGroup` (pytest ≥8.4), frozen dataclass equality/immutability/round-trips, Pydantic validation errors, `@runtime_checkable` protocols, `typing.assert_never` match exhaustiveness, `StrEnum`/`IntEnum`, and 3.13 additions (`ReadOnly`, `TypeIs`, `warnings.deprecated`, `copy.replace`) gated by `sys.version_info`/`typing_extensions`."
index:
  - anchor: version-type-hints
    what: "Use PEP 695 `type` aliases and generic syntax, per-field `Required`/`NotRequired` on `TypedDict`, `Unpack` for typed `**kwargs`, and `typing.override` for intentional overrides."
    problem: "Pre-3.12 typing syntax is verbose and cannot express per-field optionality, typed kwargs, or override intent cleanly; first-class alias, generic syntax, required notrequired, unpack kwargs, override intent, modern typing."
    use_when: "Project uses Python 3.12 typing, modern syntax expresses aliases generics optionality kwargs and overrides cleanly; first class alias, generic syntax, required notrequired, unpack kwargs, override intent, modern typing, pep 695."
    avoid_when: "Do not mix legacy `TypeAlias`/`Generic[T]` syntax with PEP 695 in new code, and do not apply `@override` to methods that are not actual overrides."
    expected: "Type hints use 3.12 first-class idioms (PEP 695, Required/NotRequired, Unpack, override) consistently."
  - anchor: version-exception-groups
    what: "Assert that bulk operations collect every failure into an `ExceptionGroup`/`BaseExceptionGroup`; on pytest >=8.4 use `pytest.RaisesGroup` (gated with `pytest.importorskip('pytest', minversion='8.4')`) instead of inspecting `exc_info.value.exceptions` by hand."
    problem: "Bulk operation must surface all failures at once, and manual exception-list inspection is brittle; all failures group, nested exception assert, version gate, manual inspect fallback, complete group, not first only."
    use_when: "Bulk operation must surface all failures together, manual exception list inspection is brittle, and version gate selects helper; all failures group, nested exception assert, version gate, manual inspect fallback, complete group, not first only."
    avoid_when: "Do not assert only the first failure of a bulk operation, and do not use `pytest.RaisesGroup` without gating on pytest>=8.4."
    expected: "Bulk failures are asserted as a complete ExceptionGroup, using RaisesGroup when available with a version gate."
  - anchor: version-data-class-testing
    what: "Test data-class-like objects through public invariants: equality, immutability expectations, round-trips, and validation failures."
    problem: "Data classes hide correctness in generated methods and validation that must verify via public behavior; equality round-trip, frozen immutability, exact validation, protocol conformance, generated helper, public invariant."
    use_when: "Data class correctness hides in generated methods and validation, public behavior must prove equality immutability round trip and failures; equality round trip, frozen immutability, exact validation, protocol conformance, generated helper, public invariant."
    avoid_when: "Do not accept a generic exception for pydantic validation failures — assert the exact validation error."
    expected: "Data-class invariants (equality, immutability, round-trip, exact validation, protocol conformance) are verified through public behavior."
  - anchor: version-protocols
    what: "Use `@runtime_checkable` only as a quick structural screen because `isinstance` checks method existence, not signatures or semantics; always invoke the protocol method to verify real compliance."
    problem: "isinstance against runtime-checkable protocol passes for objects with same-named method but wrong signature or behavior; structural screen, signature not checked, invoke method, prove compliance, existence only, semantics gap."
    use_when: "Runtime checkable protocol only screens method existence, signature or behavior may still be wrong, and method invocation proves compliance; structural screen, signature not checked, invoke method, prove compliance, existence only, semantics gap."
    avoid_when: "Do not treat `@runtime_checkable` `isinstance` as proof of correctness — it checks method existence only, not signatures or semantics."
    expected: "Protocol conformance is proven by both an `isinstance` screen and an actual method invocation."
  - anchor: version-match-case
    what: "Route the fallback branch of a `match` through `typing.assert_never` to guarantee every variant is handled."
    problem: "Non-exhaustive match silently falls through and lets new variants go unhandled; exhaustiveness, assert never fallback, every variant, new variant fails, unreachable case, parametrized subclass."
    use_when: "Pattern match statement must stay exhaustive, fallback branch should assert never, and new variant must fail loudly during collection; exhaustiveness, assert never fallback, every variant, new variant fails, unreachable case, parametrized subclass, match safety."
    avoid_when: "Do not leave a `match` without an `assert_never` fallback, and do not add a new variant without a matching case."
    expected: "Every variant is handled; adding a variant without a case fails via `assert_never`."
  - anchor: version-enums
    what: "Replace raw string comparisons with `enum.StrEnum` and verify every member round-trips through construction, rejects invalid raw values, and has a corresponding handler/mapping."
    problem: "Raw string comparisons bypass enum safety and let missing handlers or members slip through; member round-trip, reject invalid, handler per member, no raw compare, full coverage, mapping complete."
    use_when: "Raw string comparison bypasses enum safety, every member must round trip and map to handler, and invalid raw values reject; member round trip, reject invalid, handler per member, no raw compare, full coverage, mapping complete."
    avoid_when: "Do not compare against raw strings instead of `StrEnum` members, and do not let a member exist without a corresponding handler."
    expected: "Every `StrEnum` member round-trips, rejects invalid values, and maps to a non-None handler."
  - anchor: version-python-313-additions
    what: "Adopt `typing.ReadOnly`, `typing.TypeIs`, protocol introspection (`get_protocol_members`, `is_protocol`), PEP 696 type-parameter defaults, `warnings.deprecated`, and `copy.replace` — gating imports on `sys.version_info >= (3, 13)` with `typing_extensions` fallbacks (and `skipif` for `copy.replace`)."
    problem: "3.13-only features must not break older interpreters, so imports and tests need version gates and backports; version gate import, backport fallback, skipif older, narrowing, deprecated decorator, copy replace."
    use_when: "Python 3.13 features must not break older interpreters, imports and tests need version gates, and backports cover gaps; version gate import, backport fallback, skipif older, narrowing, deprecated decorator, copy replace, typing extensions."
    avoid_when: "Do not import 3.13-only symbols unconditionally, and do not run `copy.replace` tests on Python <3.13 without a skip gate."
    expected: "3.13 features are exercised with version-gated imports/backports, staying green on both 3.13 and older interpreters."
  - anchor: version-variety-booster
    what: "Pair `@pytest.mark.parametrize` with variant factories and structural assertions to cover more invariants with less code (enum round-trips/handlers, event-subclass exhaustiveness, frozen/mutable data-class matrices)."
    problem: "Hand-written per-variant tests duplicate bodies and miss members or variants; variant factory, enum matrix, event exhaustiveness, frozen mutable matrix, structural assert, compact parametrize."
    use_when: "Per variant hand written tests duplicate bodies, variant factories and matrices cover enum event and data class invariants compactly; variant factory, enum matrix, event exhaustiveness, frozen mutable matrix, structural assert, compact parametrize."
    avoid_when: "Do not write one test per enum member/event subclass/model variant — collapse them into parametrized matrices."
    expected: "All enum members, event variants, and data-class flavors are covered by compact parametrized matrices."
libraries:
  - attrs
  - pydantic
  - pytest>=8.4
  - typing-extensions
---

# Python 3.12+ Specifics

## Type Hints

[ref: #version-type-hints]

Python 3.12 makes modern typing idioms first-class: use PEP 695 `type` aliases and generic syntax, per-field `Required`/`NotRequired` on `TypedDict`, `Unpack` for typed `**kwargs`, and `typing.override` to mark intentional method overrides.

```python
from collections.abc import Callable
from typing import Any, NotRequired, Required, TypedDict, Unpack, override


class UserCreateData(TypedDict):
    first_name: Required[str]
    last_name: Required[str]
    email: Required[str]
    phone: NotRequired[str]
    metadata: NotRequired[dict[str, Any]]


class UpdateOptions(TypedDict, total=False):
    strict: bool
    skip_validation: bool


# PEP 695 type alias — preferred over explicit TypeAliasType construction
type UserId = str
type JsonDict = dict[str, Any]


# PEP 695 generic class
class Container[T]:
    def __init__(self, value: T) -> None:
        self.value = value

    def get(self) -> T:
        return self.value


# PEP 695 generic function with ParamSpec
class User: ...


def create_user[**P](
    factory: Callable[P, User],
    *args: P.args,
    **kwargs: P.kwargs,
) -> User:
    return factory(*args, **kwargs)


class BaseUserService:
    def save(self, user: User) -> User:
        ...


class EnhancedUserService(BaseUserService):
    @override
    def save(self, user: User) -> User:
        ...


def update_user(
    user_id: UserId,
    data: UserCreateData,
    **options: Unpack[UpdateOptions],
) -> User:
    ...
```

## Exception Groups

[ref: #version-exception-groups]

Python 3.12 ships native `ExceptionGroup` / `BaseExceptionGroup`, so tests can assert that a bulk operation collects every failure instead of stopping at the first.

```python
import pytest
from faker import Faker

from myapp.errors import ValidationError


def test_bulk_operation_collects_all_errors(fake: Faker) -> None:
    """
    Given: a batch of items with invalid emails.
    When: the batch is processed.
    Then: an ExceptionGroup collects a ValidationError for every item.
    """
    # --- Arrange ---
    items = [
        {"id": fake.uuid4(), "email": fake.domain_name()},
        {"id": fake.uuid4(), "email": ""},
        {"id": fake.uuid4(), "email": None},
    ]

    # --- Act ---
    with pytest.raises(ExceptionGroup) as exc_info:
        processor.process_batch(items)

    # --- Assert ---
    exceptions = exc_info.value.exceptions
    assert len(exceptions) == len(items)
    assert all(isinstance(exc, ValidationError) for exc in exceptions)
    assert any("email" in str(exc) for exc in exceptions)
```

When pytest 8.4+ is available, use `pytest.RaisesGroup` to declare the expected structure instead of inspecting `exc_info.value.exceptions` by hand.

```python
import pytest
from faker import Faker

from myapp.errors import ValidationError


def test_bulk_operation_with_raises_group(fake: Faker) -> None:
    """
    Given: a batch of items with invalid emails.
    When: the batch is processed with pytest >= 8.4.
    Then: RaisesGroup matches the expected set of ValidationErrors.
    """
    # --- Arrange ---
    pytest.importorskip("pytest", minversion="8.4")
    from pytest import RaisesGroup

    items = [
        {"id": fake.uuid4(), "email": fake.domain_name()},
        {"id": fake.uuid4(), "email": ""},
        {"id": fake.uuid4(), "email": None},
    ]

    # --- Act / Assert ---
    with RaisesGroup(ValidationError, ValidationError, ValidationError):
        processor.process_batch(items)
```

## Data Class Testing

[ref: #version-data-class-testing]

Test data-class-like objects through their public invariants: equality, immutability expectations, round-trips, and validation failures.

```python
from dataclasses import FrozenInstanceError, asdict, dataclass

import pytest
from faker import Faker


@dataclass(frozen=True)
class User:
    id: str
    email: str


def test_frozen_dataclass_equality_with_same_values(fake: Faker) -> None:
    """
    Given: a frozen User instance built with generated data.
    When: the user is rebuilt from its asdict representation.
    Then: equality holds and the email is preserved.
    """
    # --- Arrange ---
    original = User(id=fake.uuid4(), email=fake.fake_email())

    # --- Act ---
    rebuilt = User(**asdict(original))

    # --- Assert ---
    assert original == rebuilt
    assert rebuilt.email == original.email


def test_frozen_dataclass_is_immutable(fake: Faker) -> None:
    """
    Given: a frozen User instance.
    When: an attribute is reassigned.
    Then: a FrozenInstanceError is raised.
    """
    # --- Arrange ---
    user = User(id=fake.uuid4(), email=fake.fake_email())

    # --- Act / Assert ---
    with pytest.raises(FrozenInstanceError):
        user.email = fake.fake_email()
```

For `pydantic` models, assert the exact validation error rather than a generic exception.

```python
import pytest
from faker import Faker
from pydantic import BaseModel, EmailStr, ValidationError


class UserModel(BaseModel):
    email: EmailStr
    name: str


def test_pydantic_model_rejects_invalid_email(fake: Faker) -> None:
    """
    Given: a UserModel that requires a valid email.
    When: it is instantiated with a non-email domain string.
    Then: a ValidationError mentions the invalid email address.
    """
    # --- Arrange ---
    invalid_email = fake.domain_name()
    name = fake.name()

    # --- Act ---
    with pytest.raises(ValidationError) as exc_info:
        UserModel(email=invalid_email, name=name)

    # --- Assert ---
    assert "value is not a valid email address" in str(exc_info.value)
```

For `attrs`, verify both protocol compliance and generated helper behavior.

```python
import pytest
from attrs import field, frozen


@frozen
class DataPacket:
    payload: bytes = field()
    checksum: str = field()


def test_attrs_class_implements_protocol() -> None:
    """
    Given: an attrs-defined DataPacket class.
    When: its protocol conformance is checked.
    Then: it is a subclass of the Sendable protocol.
    """
    # --- Act / Assert ---
    assert issubclass(DataPacket, Sendable)
```

## `typing.Protocol` and `runtime_checkable`

[ref: #version-protocols]

Use `@runtime_checkable` only as a quick structural screen, because `isinstance` checks method existence, not signatures or semantics.

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Serializable(Protocol):
    def to_json(self) -> str: ...


def test_entity_implements_serializable(user: User) -> None:
    """
    Given: a user entity.
    When: its conformance to the Serializable protocol is verified.
    Then: isinstance succeeds and the protocol method returns a string.
    """
    # --- Act / Assert ---
    # isinstance only checks method existence, not signatures
    assert isinstance(user, Serializable)
    # real compliance check: invoke the protocol method
    assert isinstance(user.to_json(), str)
```

## `match-case` Exhaustiveness

[ref: #version-match-case]

Guarantee that every variant is handled by routing the fallback branch through `typing.assert_never`.

```python
from typing import assert_never

import pytest
from faker import Faker


class Event:
    def __init__(self, id: str) -> None:
        self.id = id


class UserCreated(Event): ...
class OrderPlaced(Event): ...


def handle_event(event: Event) -> str:
    match event:
        case UserCreated():
            return "user-created"
        case OrderPlaced():
            return "order-placed"
        case _ as unreachable:
            assert_never(unreachable)


@pytest.mark.parametrize("event_type", [UserCreated, OrderPlaced])
def test_event_handler_is_exhaustive(fake: Faker, event_type: type[Event]) -> None:
    """
    Given: a concrete event subclass.
    When: the event is handled.
    Then: a string tag is returned without reaching assert_never.
    """
    # --- Arrange ---
    event = event_type(id=fake.uuid4())

    # --- Act ---
    result = handle_event(event)

    # --- Assert ---
    assert isinstance(result, str)
```

## `enum.Enum` / `enum.StrEnum` Testing

[ref: #version-enums]

Replace raw string comparisons with `enum.StrEnum` and verify that every member has a corresponding handler or mapping.

```python
import enum

import pytest
from faker import Faker


class Status(enum.StrEnum):
    PENDING = "pending"
    ACTIVE = "active"
    CLOSED = "closed"


def test_status_is_strenum_not_raw_string(fake: Faker) -> None:
    """
    Given: a raw string value taken from a StrEnum member.
    When: the raw value is used to construct the enum.
    Then: the resulting member equals the raw input.
    """
    # --- Arrange ---
    raw = fake.random_element(elements=list(Status))

    # --- Act ---
    status = Status(raw)

    # --- Assert ---
    assert status == raw


def test_status_rejects_invalid_raw_value(fake: Faker) -> None:
    """
    Given: a value that is not a defined Status member.
    When: the value is passed to Status().
    Then: a ValueError is raised.
    """
    # --- Arrange ---
    invalid_value = fake.uuid4()

    # --- Act / Assert ---
    with pytest.raises(ValueError):
        Status(invalid_value)


def handle_pending() -> None: ...
def handle_active() -> None: ...
def handle_closed() -> None: ...


def test_all_statuses_have_handler() -> None:
    """
    Given: a mapping from every Status member to its handler.
    When: the mapping keys are compared to the enum members.
    Then: every member has a corresponding handler.
    """
    # --- Arrange ---
    handlers = {
        Status.PENDING: handle_pending,
        Status.ACTIVE: handle_active,
        Status.CLOSED: handle_closed,
    }

    # --- Assert ---
    assert set(handlers) == set(Status)


@pytest.mark.parametrize("status", list(Status))
def test_every_status_has_non_none_handler(status: Status) -> None:
    """
    Given: a parametrized Status member.
    When: the associated handler is looked up.
    Then: the handler is not None.
    """
    # --- Arrange ---
    handlers = {
        Status.PENDING: handle_pending,
        Status.ACTIVE: handle_active,
        Status.CLOSED: handle_closed,
    }

    # --- Act ---
    handler = handlers[status]

    # --- Assert ---
    assert handler is not None
```

## Python 3.13 Additions

[ref: #version-python-313-additions]

Projects that already run on Python 3.13 — or that can gate/backport features with `typing_extensions` — can adopt the following additions safely.

### `typing.ReadOnly` for `TypedDict` items

```python
import sys

from typing import TypedDict

if sys.version_info >= (3, 13):
    from typing import ReadOnly
else:
    from typing_extensions import ReadOnly


class Band(TypedDict):
    name: str
    members: ReadOnly[list[str]]
```

### `typing.TypeIs` for type narrowing

```python
import sys

if sys.version_info >= (3, 13):
    from typing import TypeIs
else:
    from typing_extensions import TypeIs


class User:
    def __init__(self, name: str) -> None:
        self.name = name


class AdminUser(User):
    is_superuser: bool = True


def is_admin(user: User) -> TypeIs[AdminUser]:
    return isinstance(user, AdminUser)


def test_admin_narrowing(fake: Faker) -> None:
    """
    Given: an AdminUser and a plain User.
    When: the TypeIs narrowing helper is applied.
    Then: it returns True for the admin and False for the guest.
    """
    # --- Arrange ---
    admin = AdminUser(name=fake.name())
    guest = User(name=fake.name())

    # --- Act ---
    admin_is_admin = is_admin(admin)
    guest_is_admin = is_admin(guest)

    # --- Assert ---
    assert admin_is_admin is True
    assert guest_is_admin is False
```

### Protocol introspection

```python
import sys

from typing import Protocol

if sys.version_info >= (3, 13):
    from typing import get_protocol_members, is_protocol
else:
    from typing_extensions import get_protocol_members, is_protocol


class Drawable(Protocol):
    def draw(self) -> bytes: ...


def test_drawable_protocol_introspection() -> None:
    """
    Given: a Drawable protocol with one member.
    When: protocol introspection helpers are used.
    Then: Drawable is recognized and its member set is {"draw"}.
    """
    # --- Act / Assert ---
    assert is_protocol(Drawable) is True
    assert get_protocol_members(Drawable) == {"draw"}
```

### Type parameter defaults (PEP 696)

```python
import sys

if sys.version_info >= (3, 13):
    from typing import TypeVar
else:
    from typing_extensions import TypeVar


T = TypeVar("T", default=str)


class Buffer[T]:
    def __init__(self, data: T) -> None:
        self.data = data


def test_buffer_accepts_string_default(fake: Faker) -> None:
    """
    Given: a string value and a generic Buffer with a string default.
    When: the buffer is instantiated with the text.
    Then: the stored data equals the input text.
    """
    # --- Arrange ---
    text = fake.sentence()

    # --- Act ---
    buffer = Buffer[str](text)

    # --- Assert ---
    assert buffer.data == text
```

### `warnings.deprecated()` decorator (PEP 702)

```python
import sys

import pytest
from faker import Faker

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated


@deprecated("Use create_user_v2 instead.")
def create_user_legacy(email: str) -> dict[str, str]:
    return {"email": email}


def test_legacy_function_emits_deprecation_warning(fake: Faker) -> None:
    """
    Given: the legacy create_user_legacy function.
    When: it is called with a generated email.
    Then: a DeprecationWarning mentioning create_user_v2 is emitted.
    """
    # --- Arrange ---
    email = fake.fake_email()

    # --- Act / Assert ---
    with pytest.warns(DeprecationWarning, match="create_user_v2"):
        create_user_legacy(email)
```

### `copy.replace()` for immutable updates

```python
import sys

import pytest
from faker import Faker


@pytest.mark.skipif(
    sys.version_info < (3, 13),
    reason="copy.replace requires Python 3.13",
)
def test_copy_replace_updates_frozen_dataclass(fake: Faker) -> None:
    """
    Given: a frozen User instance.
    When: copy.replace is used to change the email.
    Then: the id is preserved and the email is updated.
    """
    # --- Arrange ---
    from copy import replace

    original = User(id=fake.uuid4(), email=fake.fake_email())
    new_email = fake.fake_email()

    # --- Act ---
    updated = replace(original, email=new_email)

    # --- Assert ---
    assert updated.id == original.id
    assert updated.email == new_email
    assert updated.email != original.email
```

## Variety booster

[ref: #version-variety-booster]

Cover more invariants with less code by pairing `@pytest.mark.parametrize` with variant factories and structural assertions.
Parametrize over `list(Status)` to assert that every enum member round-trips through construction and has a non-None handler.
Parametrize over every event subclass to verify that `handle_event` returns the expected tag without ever reaching `assert_never`.
For data-class-like objects, parametrize over frozen and mutable model factories and assert equality, round-trip serialization, and immutability expectations in one parameterized matrix.
