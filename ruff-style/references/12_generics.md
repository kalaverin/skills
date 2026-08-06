---
---

# Generics and type variables

Design generic APIs with TypeVar/ParamSpec, Self, Protocol, TypedDict, and PEP 695 inline type parameters.

## Rule of thumb

1. In stubs, keep type parameters private (`_T`), use or remove them, and replace a custom bound `TypeVar` for `self`/`cls` with `Self`.
2. Return `Self` from `__new__`, `__enter__`, `__aenter__`, and in-place dunders so subclasses stay accurately typed.
3. Reference every private `Protocol` and `TypedDict` you define, or delete them.
4. Prefer class syntax for `TypedDict` and `NamedTuple`; use PEP 695 inline type parameters for generic classes and functions on Python 3.12+.
5. Put `Generic[...]` last in base-class lists when you must use the old form.
6. Don't add leading underscores to PEP 695 type parameters; their scope is already private.

## Example: Type parameters in a stub

A junior's first stub for a fluent builder, mixing public type parameters, dead ParamSpecs, and a hand-rolled TypeVar for `self`.

### Bad

```python
# File: builder.pyi
"""Fluent builder stub.

This module defines the builder interface used by the rest of the package.
"""

from typing import ParamSpec, TypeVar

T = TypeVar("T")  # PYI001
_P = ParamSpec("_P")  # PYI018
_S = TypeVar("_S", bound="Builder")


class Builder:
    """Builds things."""

    def __init__(self, name: str) -> None: ...
    def chain(self: _S) -> _S: ...  # PYI019
    def duplicate(self: _S) -> _S: ...  # PYI019
    def configure(self: _S, *args: object, **kwargs: object) -> _S: ...  # PYI019
    def merge(self: _S, other: Builder) -> _S: ...  # PYI019
    def take(self, obj: T) -> T: ...
    def build(self) -> object: ...
```

### Good

```python
# File: builder.pyi
"""Fluent builder stub.

This module defines the builder interface used by the rest of the package.
"""

from typing import Self


class Builder:
    """Builds things."""

    def __init__(self, name: str) -> None: ...
    def chain(self) -> Self: ...
    def duplicate(self) -> Self: ...
    def configure(self, *args: object, **kwargs: object) -> Self: ...
    def merge(self, other: Builder) -> Self: ...
    def build(self) -> object: ...
```

### Violations

1. **PYI001** — `T = TypeVar("T")`; stub type parameters must be prefixed with `_`.
2. **PYI018** — `_P = ParamSpec("_P")`; unused private type variable.
3. **PYI019** — `def chain(self: _S) -> _S: ...`; custom TypeVar for `self` should be `Self`.

## Example: Self returns and dead shapes

A stub context manager that returns its own class name and defines private Protocol/TypedDict types it never uses.

### Bad

```python
# File: connection.pyi
"""Connection context manager stub.

Defines the connection interface plus internal marker/payload shapes.
"""

from typing import Protocol, TypedDict

class _Marker(Protocol):  # PYI046
    value: int

class _Payload(TypedDict):  # PYI049
    data: bytes

class Connection:
    """A context manager you can accumulate in place."""

    def __enter__(self) -> Connection: ...  # PYI034
    def __iadd__(self, other: Connection) -> Connection: ...  # PYI034
    def connect(self) -> None: ...
    def read(self) -> bytes: ...
    def close(self) -> None: ...
```

### Good

```python
# File: connection.pyi
"""Connection context manager stub.

Defines the connection interface plus internal marker/payload shapes.
"""

from typing import Protocol, Self, TypedDict

class Marker(Protocol):
    value: int

class Payload(TypedDict):
    data: bytes

class Connection:
    """A context manager you can accumulate in place."""

    def __enter__(self) -> Self: ...
    def __iadd__(self, other: Connection) -> Self: ...
    def connect(self) -> None: ...
    def read(self) -> bytes: ...
    def close(self) -> None: ...

def handshake(marker: Marker, payload: Payload) -> Connection: ...
```

### Violations

1. **PYI034** — `def __enter__(self) -> Connection: ...`; fixed return type collapses subclasses to `Connection`.
2. **PYI046** — `class _Marker(Protocol)`; private protocol is never referenced.
3. **PYI049** — `class _Payload(TypedDict)`; private TypedDict is never referenced.

## Example: Generic containers

A stub collection of generic containers written with old-style `TypeVar` and `Generic`, then ordered wrong in the base list.

### Bad

```python
# File: containers.pyi
"""Generic container stubs.

A tiny collection of stack and helper signatures.
"""

from collections.abc import Sized
from typing import Generic, TypeVar

_T = TypeVar("_T")

class Stack(Generic[_T], Sized):  # PYI059,UP046
    """Last-in, first-out container."""

    def push(self, item: _T) -> None: ...
    def pop(self) -> _T: ...
    def peek(self) -> _T: ...
    def __len__(self) -> int: ...

def first(items: list[_T]) -> _T: ...  # UP047
```

### Good

```python
# File: containers.pyi
"""Generic container stubs.

A tiny collection of stack and helper signatures.
"""

from collections.abc import Sized

class Stack[T](Sized):
    """Last-in, first-out container."""

    def push(self, item: T) -> None: ...
    def pop(self) -> T: ...
    def peek(self) -> T: ...
    def __len__(self) -> int: ...

def first[T](items: list[T]) -> T: ...
```

### Violations

1. **PYI059** — `class Stack(Generic[_T], Sized):`; `Generic[...]` must be the last base class.
2. **UP046** — `class Stack(Generic[_T], Sized):`; generic class should use PEP 695 type parameters.
3. **UP047** — `def first(items: list[_T]) -> _T: ...`; generic function should use PEP 695 type parameters.

## Example: Records and private inline type parameters

A runtime module that uses functional `TypedDict`/`NamedTuple` syntax and a PEP 695 generic with a private parameter name.

### Bad

```python
# File: records.py
"""Record types and a generic wrapper.

Exposes simple data shapes and a generic value holder.
"""

from typing import NamedTuple, TypedDict

Movie = TypedDict("Movie", {"title": str, "year": int})  # UP013
Point = NamedTuple("Point", [("x", int), ("y", int)])  # UP014

class Wrapper[_T]:  # UP049
    value: _T

    def __init__(self, value: _T) -> None:
        self.value = value

    def get(self) -> _T:
        return self.value


def clone[_T](obj: _T) -> _T:  # UP049
    return obj
```

### Good

```python
# File: records.py
"""Record types and a generic wrapper.

Exposes simple data shapes and a generic value holder.
"""

from typing import NamedTuple, TypedDict

class Movie(TypedDict):
    title: str
    year: int

class Point(NamedTuple):
    x: int
    y: int

class Wrapper[T]:
    value: T

    def __init__(self, value: T) -> None:
        self.value = value

    def get(self) -> T:
        return self.value


def clone[T](obj: T) -> T:
    return obj
```

### Violations

1. **UP013** — `Movie = TypedDict("Movie", {"title": str, "year": int})`; use class syntax for `TypedDict`.
2. **UP014** — `Point = NamedTuple("Point", [("x", int), ("y", int)])`; use class syntax for `NamedTuple`.
3. **UP049** — `class Wrapper[_T]:`; PEP 695 type parameters should not be private.
