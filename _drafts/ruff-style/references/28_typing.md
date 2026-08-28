---
---

# Typing

Write complete, modern, minimal annotations: full signatures, PEP 604/585/695 syntax, disciplined quotes, and `TYPE_CHECKING` hygiene.

## Rule of thumb

1. Annotate every signature completely: parameters, `*args` (element type), `**kwargs` (value type), and every return — public, private, static, class, and `__init__ -> None`; `self`/`cls` stay bare.
2. Prefer `object` over `Any` for "any value"; reserve `Any` for the genuinely inexpressible, and give special methods their canonical signatures.
3. Spell types the modern way the target allows: `list[int]`, `X | Y`, `X | None`, `type` aliases (3.12+), `*tuple[...]` (3.11+), `Generator[int]` (3.13+) — no `List`/`Union`/`Optional`/`Text`/`Unpack` ghosts.
4. Make nullability explicit and ordered: `T | None = None`, `None` last in the union, no `Never` members, no string fragments inside `|`.
5. Quote only what runtime evaluation would break: drop quotes under deferred evaluation, in function bodies, and in stubs; quote `cast()` targets and aliases referencing `TYPE_CHECKING`-only symbols — whole, never one member.
6. Keep `if TYPE_CHECKING:` a one-way door: annotation-only imports (stdlib, third-party, first-party) move in, runtime imports move out, empty blocks get deleted.
7. Keep unions, literals, and type parameters honest: no duplicate or nested members, no numeric-tower or supertype redundancy, bare `Final`, `_co`/`_contra` suffixes matching variance, `TypeVar` name matching the variable, PEP 570 `/` for positional-only, no mixing PEP 695 lists with `Generic[...]`.

## Example: Complete signatures

A junior's inventory module: half-typed functions, an `Any` escape hatch, a colon slipped where an assignment was meant, and annotations scraped from `__dict__`.

### Bad

```python
# File: shop/inventory.py
"""Inventory tracking."""

from typing import Any


def add_item(name, price, *tags, **meta):  # ANN001,ANN002,ANN003,ANN201
    return {"name": name, "price": price, "tags": tags, "meta": meta}


def _slugify(text):  # ANN001,ANN202
    return text.lower().replace(" ", "-")


class Item:
    def __init__(self, name, stock):  # ANN001,ANN204
        self.name = name
        self.stock = stock

    @staticmethod
    def from_barcode(code):  # ANN001,ANN205
        return Item("unknown", 0)

    @classmethod
    def default(cls):  # ANN206
        return cls("placeholder", 0)

    def describe(self, prefix: Any) -> str:  # ANN401
        return f"{prefix}: {self.name}"


stock_levels = {}
stock_levels["apples"]: 10  # B032


def annotation_names(obj: object) -> dict:
    return obj.__dict__.get("__annotations__", {})  # RUF063
```

### Good

```python
# File: shop/inventory.py
"""Inventory tracking."""

import inspect


def add_item(name: str, price: float, *tags: str, **meta: str) -> dict:
    return {"name": name, "price": price, "tags": tags, "meta": meta}


def _slugify(text: str) -> str:
    return text.lower().replace(" ", "-")


class Item:
    def __init__(self, name: str, stock: int) -> None:
        self.name = name
        self.stock = stock

    @staticmethod
    def from_barcode(code: str) -> "Item":
        return Item("unknown", 0)

    @classmethod
    def default(cls) -> "Item":
        return cls("placeholder", 0)

    def describe(self, prefix: str) -> str:
        return f"{prefix}: {self.name}"


stock_levels = {}
stock_levels["apples"] = 10


def annotation_names(obj: object) -> dict:
    return inspect.get_annotations(obj)
```

### Violations

1. **ANN001** — `name`, `price`, `text`, `code`, `stock`; a bare parameter is an unchecked `Any` at every call site.
2. **ANN002** — `*tags`; varargs need the type of each element.
3. **ANN003** — `**meta`; kwargs need the type of each value.
4. **ANN201** — `def add_item(...)`; a public function without a return annotation forfeits checking for callers.
5. **ANN202** — `def _slugify(...)`; private helpers need return annotations too.
6. **ANN204** — `def __init__(self, name, stock)`; special methods carry an explicit `-> None`.
7. **ANN205** — `def from_barcode(code)`; a staticmethod is still a signature and needs its return type.
8. **ANN206** — `def default(cls)`; classmethods need return annotations (`cls` itself stays bare).
9. **ANN401** — `prefix: Any`; `Any` opts the value out of all checking where a concrete type or `object` would do.
10. **B032** — `stock_levels["apples"]: 10`; a colon on a subscript is a no-op annotated statement, not the intended assignment.
11. **RUF063** — `obj.__dict__.get("__annotations__", {})`; `__dict__` scraping breaks on 3.14, use `inspect.get_annotations`.

## Example: Legacy typing syntax

**Target:** `py313`

A module written from old memory: `typing` ghosts everywhere, verbose aliases, and sloppy unions, on a project targeting Python 3.13.

### Bad

```python
# File: shop/legacy.py
"""Legacy-typed helpers."""

from collections.abc import Generator
from typing import Dict, List, Never, Optional, Text, TypeAlias, Union, Unpack

IntMap: TypeAlias = dict[str, int]  # UP040


def find(items: List[int], target: Optional[int]) -> Union[int, str]:  # UP006,UP007,UP045
    ...


def title(text: Text) -> Dict[str, Text]:  # UP006,UP019
    ...


def stream() -> Generator[int, None, None]:  # UP043
    yield 1


def run(*args: Unpack[tuple[int, ...]]) -> None:  # UP044
    pass


def resize(width: int = None) -> None:  # RUF013
    pass


def clamp(value: None | int) -> int:  # RUF036
    ...


def fail() -> Never | int:  # RUF020
    ...
```

### Good

```python
# File: shop/legacy.py
"""Modern-typed helpers."""

from collections.abc import Generator

type IntMap = dict[str, int]


def find(items: list[int], target: int | None) -> int | str:
    ...


def title(text: str) -> dict[str, str]:
    ...


def stream() -> Generator[int]:
    yield 1


def run(*args: *tuple[int, ...]) -> None:
    pass


def resize(width: int | None = None) -> None:
    pass


def clamp(value: int | None) -> int:
    ...


def fail() -> int:
    ...
```

### Violations

1. **RUF013** — `width: int = None`; a `None` default forces an explicit `int | None`, PEP 484 bans the implicit form.
2. **RUF020** — `Never | int`; `Never` has no values, so the union member is dead weight.
3. **RUF036** — `None | int`; put the informative type first and `None` last.
4. **UP006** — `List[int]`, `Dict[str, Text]`; PEP 585 builtin generics replace the deprecated `typing` aliases.
5. **UP007** — `Union[int, str]`; PEP 604 spells it `int | str` with no import.
6. **UP019** — `Text`; a Python 2 compatibility alias for `str`, deprecated since 3.11.
7. **UP040** — `IntMap: TypeAlias = dict[str, int]`; on 3.12+ the `type` statement is the native alias form.
8. **UP043** — `Generator[int, None, None]`; since 3.13 the send/return parameters default to `None`, spelling them out is noise.
9. **UP044** — `Unpack[tuple[int, ...]]`; PEP 646 gives unpacking real syntax on 3.11+: `*tuple[int, ...]`.
10. **UP045** — `Optional[int]`; exactly `int | None` with an extra import and an extra concept.

## Example: Quoted annotations and aliases

**Target:** `py311`

A models module where a junior quotes defensively, pastes garbage into a forward reference, and mixes runtime aliases with `TYPE_CHECKING`-only symbols. (Pinned to py311 so the PEP 613 aliases here do not trip the 3.12+ `type`-statement rule from the previous example.)

### Bad

```python
# File: shop/report_models.py
"""Report model glue."""

from typing import TYPE_CHECKING, TypeAlias, cast

if TYPE_CHECKING:
    from shop.db import Row  # TC004

Record: TypeAlias = Row | None
OptInt: TypeAlias = "int | None"  # TC008


def build(raw: object) -> Record:
    report: "Report" = cast(Report, raw)  # TC006,UP037
    return report


def version() -> "/":  # F722
    ...


pending: "Report" | None  # TC010


class Report:
    pass
```

### Good

```python
# File: shop/report_models.py
"""Report model glue."""

from typing import TYPE_CHECKING, TypeAlias, cast

if TYPE_CHECKING:
    from shop.db import Row

Record: TypeAlias = "Row | None"
OptInt: TypeAlias = int | None


def build(raw: object) -> Record:
    report: Report = cast("Report", raw)
    return report


def version() -> str:
    return "1.0"


pending: "Report | None"


class Report:
    pass
```

### Violations

1. **F722** — `-> "/"`; a quoted annotation must still parse as a Python expression, or the checker blows up on what the compiler accepted.
2. **TC006** — `cast(Report, raw)`; quote the type expression so every `cast()` is consistent and never evaluates types at runtime.
3. **TC007** — `Record: TypeAlias = Row | None`; the alias RHS runs at import time but `Row` exists only under `TYPE_CHECKING` — guaranteed `NameError`, quote the whole expression. (Fires when TC004 is not selected; with both selected ruff reports the import as TC004 instead — the two rules are rival fixes for the same runtime reference.)
4. **TC008** — `OptInt: TypeAlias = "int | None"`; every name is available at runtime, so the quotes are pure parsing overhead (preview rule).
5. **TC010** — `"Report" | None`; a string member inside a `|` union is evaluated as `str.__or__` and raises `TypeError` — quote the whole union or defer evaluation.
6. **UP037** — `report: "Report"`; function-body annotations are never evaluated, so the quotes do nothing but add noise.

## Example: Type-checking imports

A sales-analytics module that pays startup cost for annotation-only imports and hides a runtime dependency inside the `TYPE_CHECKING` block.

### Bad

```python
# File: shop/analytics.py
"""Sales analytics."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pathlib import Path  # TC003

import pandas as pd  # TC002

from . import local_module  # TC001

if TYPE_CHECKING:
    import requests  # TC004

if TYPE_CHECKING:
    pass  # TC005


def stats(df: pd.DataFrame, root: Path, box: local_module.Container) -> int:
    return len(df)


def fetch(url: str) -> bytes:
    return requests.get(url).content
```

### Good

```python
# File: shop/analytics.py
"""Sales analytics."""

from __future__ import annotations

from typing import TYPE_CHECKING

import requests

if TYPE_CHECKING:
    from pathlib import Path

    import pandas as pd

    from . import local_module


def stats(df: pd.DataFrame, root: Path, box: local_module.Container) -> int:
    return len(df)


def fetch(url: str) -> bytes:
    return requests.get(url).content
```

### Violations

1. **TC001** — `from . import local_module`; a first-party import used only in annotations still executes at import time and feeds import cycles.
2. **TC002** — `import pandas as pd`; a heavy third-party import paid on every startup just to spell an annotation.
3. **TC003** — `from pathlib import Path`; stdlib imports used only for typing belong in the block too.
4. **TC004** — `import requests` inside `if TYPE_CHECKING:`; the block vanishes at runtime, so `fetch` hits a `NameError` — runtime names stay top-level.
5. **TC005** — the second `if TYPE_CHECKING:` block is empty scaffolding; delete it.

## Example: Type parameters

A generics module where `TypeVar` names lie about variance, one parameter wants to be everything at once, and a PEP 695 class also inherits `Generic`.

### Bad

```python
# File: shop/generics.py
"""Generic containers."""

from typing import Generic, TypeVar

T = TypeVar("U")  # PLC0132
Both = TypeVar("Both", covariant=True, contravariant=True)  # PLC0131
V = TypeVar("V", covariant=True)  # PLC0105
W_contra = TypeVar("W_contra")  # PLC0105


class Box[T](Generic[V]):  # RUF053
    """A box that is generic twice over."""

    def __init__(self, item: T) -> None:
        self.item = item

    def replace(self, item: T) -> "Box[T]":
        return Box(item)


class Pair(Generic[T, W_contra]):
    def __init__(self, first: T, second: W_contra) -> None:
        self.first = first
        self.second = second
```

### Good

```python
# File: shop/generics.py
"""Generic containers."""

from typing import Generic, TypeVar

T = TypeVar("T")
V_co = TypeVar("V_co", covariant=True)
W = TypeVar("W")


class Box[T, V_co]:
    """All type parameters live in the bracket list."""

    def __init__(self, item: T) -> None:
        self.item = item

    def replace(self, item: T) -> "Box[T]":
        return Box(item)


class Pair(Generic[T, W]):
    def __init__(self, first: T, second: W) -> None:
        self.first = first
        self.second = second
```

### Violations

1. **PLC0105** — `V = TypeVar("V", covariant=True)` and `W_contra = TypeVar("W_contra")`; PEP 484 encodes variance in the name: `_co`, `_contra`, or bare for invariant.
2. **PLC0131** — `TypeVar("Both", covariant=True, contravariant=True)`; a parameter is covariant, contravariant, or invariant — never two at once.
3. **PLC0132** — `T = TypeVar("U")`; the string name must equal the variable name.
4. **RUF053** — `class Box[T](Generic[V])`; a PEP 695 parameter list already makes the class generic, and adding `Generic[...]` raises `TypeError` at runtime.

## Example: Stub signatures

A hand-written stub for a shop client with quoted annotations, `Any` comparisons, a wrong `__exit__`, PEP 484 positional-only hacks, and deprecated types.

### Bad

```python
# File: shop/client.pyi
from types import TracebackType
from typing import Any, ByteString, NoReturn  # PYI057


class Client:
    """Stub for the shop client."""

    def __eq__(self, other: Any) -> bool: ...  # ANN401,PYI032
    def __ne__(self, other: Any) -> bool: ...  # ANN401,PYI032
    def __exit__(self, typ: BaseException, exc: BaseException, tb: TracebackType) -> None: ...  # PYI036
    async def __aexit__(self, typ: BaseException, exc: BaseException, tb: TracebackType) -> None: ...  # PYI036
    def read(self, __n: int) -> ByteString: ...  # PYI063
    def write(self, __data: bytes, flush: bool) -> int: ...  # PYI063
    def close(self) -> "None": ...  # PYI020,UP037
    def open(self) -> "Client": ...  # PYI020,UP037


def assert_never(x: NoReturn) -> NoReturn: ...  # PYI050


def connect(__host: str, port: int) -> Client: ...  # PYI063
```

### Good

```python
# File: shop/client.pyi
from types import TracebackType
from typing import Never


class Client:
    """Stub for the shop client."""

    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __exit__(
        self,
        typ: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None: ...
    async def __aexit__(
        self,
        typ: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None: ...
    def read(self, n: int, /) -> bytes | bytearray | memoryview: ...
    def write(self, data: bytes, flush: bool, /) -> int: ...
    def close(self) -> None: ...
    def open(self) -> Client: ...


def assert_never(x: Never) -> Never: ...


def connect(host: str, port: int, /) -> Client: ...
```

### Violations

1. **PYI020** — `-> "None"` and `-> "Client"`; stubs are never executed, so forward references always work unquoted.
2. **PYI032** — `other: Any` in `__eq__`/`__ne__`; comparing arbitrary objects must never raise, and `object` expresses that contract soundly.
3. **PYI036** — `typ: BaseException, exc: BaseException, tb: TracebackType` in `__exit__`/`__aexit__`; on clean exit all three arguments are `None`, so each needs its `| None` (and `typ` its `type[...]`).
4. **PYI050** — `x: NoReturn`; a parameter cannot "return" — `Never` names the bottom type correctly in argument position.
5. **PYI057** — `ByteString` imported from `typing` for `-> ByteString`; deprecated with unclear semantics, name the concrete buffer types or `collections.abc.Buffer`.
6. **PYI063** — `__n`, `__data`, `__host`; the `__` prefix was a checker-only convention, PEP 570's `/` is real syntax Python enforces.

## Example: Stub unions and literals

A constants stub where every union and `Literal` carries members the checker already knows are implied.

### Bad

```python
# File: shop/consts.pyi
"""Constants and literal-heavy fields."""

from typing import Final, Literal

mode: Literal["r", "r", "w"]  # PYI062
all_modes: Literal[Literal["r", "r+"], Literal["w", "w+"]]  # RUF041
fallback: Literal[None]  # PYI061
level: Literal[1, 2, None]  # PYI061
flag: Literal[True, False]  # RUF038
tag: Literal["A", b"B"] | str  # PYI051
field: Literal[1] | Literal[2] | str  # PYI030
name: str | str  # PYI016
factory: type[int] | type[float] | str  # PYI055
LIMIT: Final[Literal[42]] = 42  # PYI064


class Options:
    """Literal-heavy options."""

    debug: Literal[True, False]  # RUF038
    state: Literal[None]  # PYI061


def clamp(value: float | int | str) -> float: ...  # PYI041
def parse(raw: complex | float | bytes) -> bytes: ...  # PYI041
def pick(choice: bytes | bytes) -> bytes: ...  # PYI016
```

### Good

```python
# File: shop/consts.pyi
"""Constants and literal-heavy fields."""

from typing import Final, Literal

mode: Literal["r", "w"]
all_modes: Literal["r", "r+", "w", "w+"]
fallback: None
level: Literal[1, 2] | None
flag: bool
tag: Literal[b"B"] | str
field: Literal[1, 2] | str
name: str
factory: type[int | float] | str
LIMIT: Final = 42


class Options:
    """Literal-light options."""

    debug: bool
    state: None


def clamp(value: float | str) -> float: ...
def parse(raw: complex | bytes) -> bytes: ...
def pick(choice: bytes) -> bytes: ...
```

### Violations

1. **PYI016** — `str | str` and `bytes | bytes`; a repeated union member changes nothing — usually a merge artifact or a typo.
2. **PYI030** — `Literal[1] | Literal[2] | str`; one `Literal` slice with several members means the same minus the noise.
3. **PYI041** — `float | int` and `complex | float`; a `float` parameter already accepts `int` (and `complex` accepts both) — parameter annotations only.
4. **PYI051** — `Literal["A", b"B"] | str`; `Literal["A"]` is a subtype of `str`, so the union already includes it.
5. **PYI055** — `type[int] | type[float] | str`; identical to `type[int | float] | str` with one wrapper.
6. **PYI061** — `Literal[None]` and `Literal[1, 2, None]`; `None` is already a type — write `None` or `Literal[...] | None`.
7. **PYI062** — `Literal["r", "r", "w"]`; duplicate literal members are dead, typically paste errors.
8. **PYI064** — `Final[Literal[42]]`; a `Final` constant is already inferred as its literal value, use bare `Final`.
9. **RUF038** — `Literal[True, False]`; `bool` has exactly two inhabitants — spell it `bool` (preview rule).
10. **RUF041** — `Literal[Literal["r", "r+"], Literal["w", "w+"]]`; nested `Literal` flattens to the same set, write it flat.

## Example: Stub aliases

**Target:** `py311`

A shared-types stub with bare assignments, snake_case and `T`-suffixed aliases, a dead private alias, and Python 2-era type comments. (Pinned to py311 so these PEP 613 aliases do not trip the 3.12+ `type`-statement rule.)

### Bad

```python
# File: shop/types.pyi
"""Shared aliases for the shop package."""

from collections.abc import Callable
from typing import TypeAlias

Vector = list[float]  # PYI026
IntMap = dict[str, int]  # PYI026
user_id: TypeAlias = int  # PYI042
json_value: TypeAlias = dict[str, object]  # PYI042
_CallbackT: TypeAlias = Callable[[int], None]  # PYI043
_OldName: TypeAlias = str  # PYI047
count = 0  # type: int  # PYI033
retries = 3  # type: int  # PYI033


def register(cb: _CallbackT) -> None: ...


def lookup(uid: user_id) -> Vector: ...
```

### Good

```python
# File: shop/types.pyi
"""Shared aliases for the shop package."""

from collections.abc import Callable
from typing import TypeAlias

Vector: TypeAlias = list[float]
IntMap: TypeAlias = dict[str, int]
UserId: TypeAlias = int
JsonValue: TypeAlias = dict[str, object]
_Callback: TypeAlias = Callable[[int], None]
count: int
retries: int


def register(cb: _Callback) -> None: ...


def lookup(uid: UserId) -> Vector: ...
```

### Violations

1. **PYI026** — `Vector = list[float]` and `IntMap = dict[str, int]`; a bare assignment is ambiguous between value and alias, annotate with `TypeAlias`.
2. **PYI033** — `count = 0  # type: int` and `retries = 3  # type: int`; type comments are a soft-deprecated Python 2-era form, write real annotations.
3. **PYI042** — `user_id` and `json_value`; aliases name types, and types are CamelCase.
4. **PYI043** — `_CallbackT`; a trailing `T` is the `TypeVar` convention and promises a type variable that is not there.
5. **PYI047** — `_OldName: TypeAlias = str`; a private alias with no use site is dead code — use it, publish it, or delete it.
