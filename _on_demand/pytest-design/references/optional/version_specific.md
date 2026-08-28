---
subject: "Exercise modern Python in tests: PEP 695 `type` aliases/generics, `TypedDict` `Required`/`NotRequired`/`Unpack`, `@override`, manual `ExceptionGroup` asserts or `pytest.RaisesGroup` (pytest >=8.4), frozen dataclass equality/immutability/round-trips, Pydantic validation errors, `@runtime_checkable` protocols, `typing.assert_never` match exhaustiveness, `StrEnum`/`IntEnum`, and 3.13 additions (`ReadOnly`, `TypeIs`, `warnings.deprecated`, `copy.replace`) gated by `sys.version_info`/`typing_extensions`."
index:
  - anchor: version-type-hints
    what: "Use PEP 695 `type` aliases and generic syntax, per-field `Required`/`NotRequired` on `TypedDict`, `Unpack` for typed `**kwargs`, and `typing.override` for intentional overrides."
    problem: "Pre-3.12 typing syntax is verbose and cannot express per-field optionality, typed kwargs, or override intent cleanly, leading to boilerplate and accidental mismatches; first-class alias, type parameter, required notrequired, unpack kwargs, override decorator, modern typing."
    use_when: "The project runs Python 3.12+; type aliases, generics, optional TypedDict fields, typed kwargs, or override markers are needed."
    avoid_when: "Legacy `TypeAlias`/`Generic[T]` syntax must be preserved; `@override` is not available; the code targets Python <3.12."
    expected: "Type hints use 3.12 first-class idioms (PEP 695, Required/NotRequired, Unpack, override) consistently."
  - anchor: version-exception-groups
    what: "Assert that bulk operations collect every failure into an `ExceptionGroup`/`BaseExceptionGroup`; on pytest >=8.4 use `pytest.RaisesGroup` (gated with `pytest.importorskip('pytest', minversion='8.4')`) instead of inspecting `exc_info.value.exceptions` by hand."
    problem: "Bulk operation must surface all failures at once, and manual exception-list inspection is brittle, letting hidden exceptions slip through; all failures group, nested exception assert, version guard, manual inspect fallback, complete group, not first only."
    use_when: "A bulk operation may raise multiple exceptions; pytest >=8.4 is available; `RaisesGroup` can replace hand-written inspection."
    avoid_when: "Only the first failure is asserted; `pytest.RaisesGroup` is used without a version gate; pytest <8.4 has no fallback."
    expected: "Bulk failures are asserted as a complete ExceptionGroup, using RaisesGroup when available with a version gate."
  - anchor: version-data-class-testing
    what: "Test data-class-like objects through public invariants: equality, immutability expectations, round-trips, and validation failures."
    problem: "Data classes hide correctness in generated methods and validation that must be verified via public behavior, so silent regressions pass unnoticed; equality round-trip, frozen immutability, exact validation, protocol conformance, generated helper, public invariant."
    use_when: "A dataclass, Pydantic model, or attrs class needs public invariants verified; equality, round-trip, immutability, or validation errors matter."
    avoid_when: "Generic exceptions are accepted for validation failures; private generated methods are tested directly; the model has no public invariants."
    expected: "Data-class invariants (equality, immutability, round-trip, precise validation errors, protocol adherence) are verified through public behavior."
  - anchor: version-protocols
    what: "Use `@runtime_checkable` only as a quick structural screen because `isinstance` checks method existence, not signatures or semantics; always invoke the protocol method to verify real compliance."
    problem: "isinstance against runtime-checkable protocol passes for objects with same-named method but wrong signature or behavior, giving false confidence in polymorphic code; shape screen, signature not checked, invoke method, prove compliance, existence only, semantics gap."
    use_when: "A protocol is runtime-checkable and used as a structural screen; real compliance must be proven by calling the method; signature and semantics matter."
    avoid_when: "`isinstance` against the protocol is treated as full correctness proof; the method is never invoked; signatures are assumed to match."
    expected: "Protocol conformance is proven by both an `isinstance` screen and an actual method invocation."
  - anchor: version-match-case
    what: "Route the fallback branch of a `match` through `typing.assert_never` to guarantee every variant is handled."
    problem: "Non-exhaustive match silently falls through and lets new variants go unhandled, causing runtime errors instead of early collection failures; exhaustiveness, assert never fallback, each variant, new variant fails, unreachable case, parametrized subclass."
    use_when: "A `match` statement must be exhaustive; adding a new variant should fail early; `typing.assert_never` is available."
    avoid_when: "The match has a catch-all that swallows variants; exhaustiveness is not required; variants are added without updating cases."
    expected: "Every variant is handled; adding a variant without a case fails via `assert_never`."
  - anchor: version-enums
    what: "Replace raw string comparisons with `enum.StrEnum` and verify every member round-trips through construction, rejects invalid raw values, and has a corresponding handler/mapping."
    problem: "Raw string comparisons bypass enum safety and let missing handlers or members slip through, causing silent default paths and incomplete mappings; roundtrip per member, invalid value rejected, handler per member, no raw compare, full coverage, mapping complete."
    use_when: "Enums are used for domain values; every member must construct from its raw value, reject invalid values, and map to a handler; raw string comparisons remain."
    avoid_when: "Raw strings are compared instead of enum members; members exist without handlers; invalid values are silently accepted."
    expected: "Every `StrEnum` member round-trips, rejects invalid values, and maps to a non-None handler."
  - anchor: version-python-313-additions
    what: "Adopt `typing.ReadOnly`, `typing.TypeIs`, protocol introspection (`get_protocol_members`, `is_protocol`), PEP 696 type-parameter defaults, `warnings.deprecated`, and `copy.replace` — gating imports on `sys.version_info >= (3, 13)` with `typing_extensions` fallbacks (and `skipif` for `copy.replace`)."
    problem: "3.13-only features must not break older interpreters, so imports and tests need version gates and backports to keep CI green across versions; version gate import, backport fallback, skipif older, narrowing, deprecated decorator, copy replace."
    use_when: "The project supports Python 3.13 while keeping older interpreters green; new 3.13 typing or `copy.replace` features are used; `typing_extensions` backports are available."
    avoid_when: "3.13-only symbols are imported unconditionally; `copy.replace` tests run on older Python without a skip; no fallback is provided."
    expected: "3.13 features are exercised with version-gated imports/backports, staying green on both 3.13 and older interpreters."
  - anchor: version-variety-booster
    what: "Pair `@pytest.mark.parametrize` with variant factories and structural assertions to cover more invariants with less code (enum round-trips/handlers, event-subclass exhaustiveness, frozen/mutable data-class matrices)."
    problem: "Hand-written per-variant tests duplicate bodies and miss members or variants, bloating suite, hiding gaps in coverage, and slowing development; variant factory, enum matrix, event exhaustiveness, frozen mutable matrix, shape assert, compact parametrize."
    use_when: "Many enum members, event subclasses, or dataclass variants need coverage; parametrized matrices can replace repetitive tests; structural assertions are available."
    avoid_when: "Variants are few and distinct enough for separate tests; parametrization would obscure the scenario; no structural matcher is available."
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
