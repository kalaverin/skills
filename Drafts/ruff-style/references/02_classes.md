---
---

# Classes

Design classes Python itself understands: explicit dunder contracts, dot access instead of `getattr`/`setattr` with constants, slots discipline, dataclass and ABC hygiene, and no reaching into private names.

## Rule of thumb

1. Honor the dunder contract: `__init__` stores values and returns nothing, `__len__`/`__index__`/`__hash__` return ints, `__bool__` a bool, `__str__` a str, `__bytes__` bytes — and pair every `__eq__` with a `__hash__`.
2. Write modern class syntax: bare `class C:`, no `__metaclass__` or `metaclass=type`, zero-arg `super()` with parentheses, each base listed once.
3. Access attributes with dot syntax when the name is constant; reserve `getattr`/`setattr`/`delattr` for computed names, test callability with `callable()`, and never touch `_private` members from outside.
4. Declare `__slots__` as a sorted tuple covering every assigned attribute; subclasses declare only new slots, and `str`/`tuple`/namedtuple subclasses set `__slots__ = ()`.
5. Model data with `@dataclass` (annotate shared state as `ClassVar`) and choices with enums that have unique values (`enum.StrEnum` on 3.11+); never decorate an enum with `@dataclass`.
6. Keep ABCs honest: at least one `@abstractmethod`, placed innermost under `@property`/`@classmethod`, composed from modern decorators instead of `abstractclassmethod` and friends.
7. Keep the public surface tidy: methods declared with decorators, properties that take no parameters and always return, a sorted duplicate-free `__all__`, near-empty `__init__.py` files, and classes small enough to name their job.

## Example: Constructor and dunder contracts

A junior's geometry module where constructors compute and return, and every dunder quietly breaks the data-model contract.

### Bad

```python
"""Geometry helpers."""


class Vector:  # PLW1641
    def __init__(self, x, y):
        yield x  # PLE0100
        self.y = y

    def __str__(self):
        return 42  # PLE0307

    def __bytes__(self):
        return "Vector"  # PLE0308

    def __eq__(self, other):
        return isinstance(other, Vector) and (self.x, self.y) == (other.x, other.y)


class IntBox:
    def __init_(self, value):  # PLW3201
        self.value = value

    def __len__(self, strict):  # PLE0302
        return "5"  # PLE0303

    def __bool__(self):
        return 2  # PLE0304

    def __index__(self):
        return "0"  # PLE0305

    def __hash__(self):
        return "hash"  # PLE0309


class Config:
    def __init__(self, path):
        self.path = path
        return self.path.read_text()  # PLE0101
```

### Good

```python
"""Geometry helpers."""


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __bytes__(self):
        return str(self).encode()

    def __eq__(self, other):
        return isinstance(other, Vector) and (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def items(self):
        yield self.x
        yield self.y


class IntBox:
    def __init__(self, value):
        self.value = value

    def __len__(self):
        return self.value

    def __bool__(self):
        return bool(self.value)

    def __index__(self):
        return self.value

    def __hash__(self):
        return hash(self.value)


class Config:
    def __init__(self, path):
        self.path = path
        self.text = path.read_text()

    def reload(self):
        self.text = self.path.read_text()
```

### Violations

1. **PLE0100** — `yield x` in `__init__`; yielding turns the constructor into a generator, and instantiation raises `TypeError`.
2. **PLE0101** — `return self.path.read_text()` in `__init__`; `__init__` must return `None`, so store the value on the instance.
3. **PLE0302** — `def __len__(self, strict)`; the interpreter calls `__len__` with no extra arguments, so the dunder is unusable through `len()`.
4. **PLE0303** — `return "5"` in `__len__`; `__len__` must return a non-negative `int`.
5. **PLE0304** — `return 2` in `__bool__`; `__bool__` must return a `bool`.
6. **PLE0305** — `return "0"` in `__index__`; `__index__` must return an `int`.
7. **PLE0307** — `return 42` in `__str__`; `__str__` must return a `str`.
8. **PLE0308** — `return "Vector"` in `__bytes__`; `__bytes__` must return `bytes`.
9. **PLE0309** — `return "hash"` in `__hash__`; `__hash__` must return an `int`.
10. **PLW1641** — `class Vector` defines `__eq__` but no `__hash__`; Python sets `__hash__` to `None`, making every instance unhashable.
11. **PLW3201** — `def __init_(self, value)`; a misspelled dunder has no special meaning, so the "constructor" silently never runs.

## Example: Inheritance and super()

An animal hierarchy written with Python 2 fossils, duplicated bases, and a `super` that was never called.

### Bad

```python
"""Animal hierarchy."""


class Animal(object):  # UP004
    __metaclass__ = type  # UP001

    def speak(self):
        return f"{self.name} makes a sound"


class Dog(Animal, Animal):  # PLE0241
    def speak(self):
        return super(Dog, self).speak() + " Woof!"  # UP008


class Cat(Animal, metaclass=type):  # UP050
    def speak(self):
        base = super.speak()  # PLW0245
        return f"{base} Meow!"


class Bird(Animal):
    def fly(self):
        return f"{self.name} flies"
```

### Good

```python
"""Animal hierarchy."""


class Animal:
    def speak(self):
        return f"{self.name} makes a sound"


class Dog(Animal):
    def speak(self):
        return super().speak() + " Woof!"


class Cat(Animal):
    def speak(self):
        return super().speak() + " Meow!"


class Bird(Animal):
    def fly(self):
        return f"{self.name} flies"
```

### Violations

1. **PLE0241** — `class Dog(Animal, Animal)`; a duplicate base raises `TypeError` at class-creation time.
2. **PLW0245** — `super.speak()`; bare `super` is the builtin type, not a proxy to the parent — call `super()` first.
3. **UP001** — `__metaclass__ = type`; a Python 2 spelling that is ignored in Python 3.
4. **UP004** — `class Animal(object)`; every Python 3 class already inherits `object`.
5. **UP008** — `super(Dog, self).speak()`; zero-arg `super()` resolves the class and instance automatically.
6. **UP050** — `class Cat(Animal, metaclass=type)`; `type` is the default metaclass, so naming it is redundant ceremony.

## Example: Attribute access and privacy

A plugin runner that pokes at its plugin through dynamic builtins with constant names and reaches into private state.

### Bad

```python
"""Plugin runner."""


class Plugin:
    def __init__(self, name):
        self.name = name
        self._state = "idle"

    def status(self):
        return f"{self.name}: {self._state}"


def run_plugin(plugin):
    if hasattr(plugin, "__call__"):  # B004
        plugin()
    label = getattr(plugin, "name")  # B009
    setattr(plugin, "label", label)  # B010
    plugin._state = "active"  # SLF001
    if plugin._state == "crashed":  # SLF001
        delattr(plugin, "label")  # B043
    return plugin.status()
```

### Good

```python
"""Plugin runner."""


class Plugin:
    def __init__(self, name):
        self.name = name
        self.label = name
        self._state = "idle"

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    def discard_label(self):
        del self.label

    def status(self):
        return f"{self.name}: {self._state}"


def run_plugin(plugin):
    if callable(plugin):
        plugin()
    plugin.label = plugin.name
    plugin.state = "active"
    if plugin.state == "crashed":
        plugin.discard_label()
    return plugin.status()
```

### Violations

1. **B004** — `hasattr(plugin, "__call__")`; an unreliable callable check (modules and `__getattr__` lie) — use `callable(plugin)`.
2. **B009** — `getattr(plugin, "name")`; with a constant name it is obfuscated dot access, invisible to grep and type checkers.
3. **B010** — `setattr(plugin, "label", label)`; a constant name means plain assignment, statically visible and refactor-friendly.
4. **B043** — `delattr(plugin, "label")`; constant-name `delattr` is just `del plugin.label` spelled dynamically.
5. **SLF001** — `plugin._state = "active"` and `plugin._state == "crashed"`; underscore members are internal — use or extend the public interface.

## Example: Slots discipline

A value-objects module where slots are unsorted, under-declared, re-declared in subclasses, or simply forgotten.

### Bad

```python
"""Value objects."""

from collections import namedtuple


class Label(str):  # SLOT000
    pass


class Coords(tuple):  # SLOT001
    pass


class Size(namedtuple("Size", ["w", "h"])):  # SLOT002
    pass


class Point:
    __slots__ = "y", "x"  # RUF023

    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label  # PLE0237

    def move(self, dx):
        self.x += dx


class Named(Point):
    __slots__ = ("name", "x")  # PLW0244


class Token:
    __slots__ = "kind"  # PLC0205

    def __init__(self, kind):
        self.kind = kind

    def matches(self, other):
        return self.kind == other
```

### Good

```python
"""Value objects."""

from collections import namedtuple


class Label(str):
    __slots__ = ()


class Coords(tuple):
    __slots__ = ()


class Size(namedtuple("Size", ["w", "h"])):
    __slots__ = ()


class Point:
    __slots__ = ("label", "x", "y")

    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label

    def move(self, dx):
        self.x += dx


class Named(Point):
    __slots__ = ("name",)


class Token:
    __slots__ = ("kind",)

    def __init__(self, kind):
        self.kind = kind

    def matches(self, other):
        return self.kind == other
```

### Violations

1. **PLC0205** — `__slots__ = "kind"`; a bare string works as one slot but iterates as characters — always wrap slot names in a tuple.
2. **PLE0237** — `self.label = label`; with `__slots__` there is no instance `__dict__`, so assigning an undeclared attribute raises `AttributeError`.
3. **PLW0244** — `__slots__ = ("name", "x")` in `Named`; redefining the base-class slot `"x"` shadows its descriptor — subclasses declare only new slots.
4. **RUF023** — `__slots__ = "y", "x"`; keep slot lists in natural-sort order.
5. **SLOT000** — `class Label(str)` without `__slots__`; immutable `str` subclasses never use the per-instance `__dict__` they carry.
6. **SLOT001** — `class Coords(tuple)` without `__slots__`; same wasted `__dict__` for `tuple` subclasses.
7. **SLOT002** — `class Size(namedtuple(...))` without `__slots__`; silently re-adds the per-instance `__dict__` you subclassed a namedtuple to avoid.

## Example: Dataclasses and enums

A shop domain module with a boilerplate record class, an implicit class variable, and enums that alias, mix `str`, or wear a dataclass costume.

### Bad

```python
"""Shop domain types."""

import enum
from dataclasses import dataclass


class Point:  # B903
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


@dataclass
class Product:
    category = "misc"  # RUF045
    name: str = ""
    price: float = 0.0


@dataclass  # RUF049
class Status(enum.Enum):
    OK = 1  # RUF045
    FAIL = 2  # RUF045


class Color(enum.Enum):
    RED = 1
    GREEN = 2
    CRIMSON = 1  # PIE796


class Label(str, enum.Enum):  # UP042
    __slots__ = ()

    SALE = "sale"
    NEW = "new"
```

### Good

```python
"""Shop domain types."""

import enum
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Product:
    name: str = ""
    price: float = 0.0
    category: ClassVar[str] = "misc"


class Status(enum.Enum):
    OK = 1
    FAIL = 2


@enum.unique
class Color(enum.Enum):
    RED = 1
    GREEN = 2
    CRIMSON = 3


class Label(enum.StrEnum):
    SALE = "sale"
    NEW = "new"
```

### Violations

1. **B903** — `class Point` with only an argument-shuttling `__init__`; a `@dataclass` generates the init plus `__repr__`/`__eq__` for free.
2. **PIE796** — `CRIMSON = 1`; the duplicated value silently turns `CRIMSON` into an alias of `RED`.
3. **RUF045** — `category = "misc"` (and `OK = 1`/`FAIL = 2` inside the dataclass-decorated enum); an unannotated assignment in a dataclass body is an implicit class variable, not a field — annotate it `ClassVar`.
4. **RUF049** — `@dataclass` on `class Status(enum.Enum)`; the generated `__eq__` corrupts enum equality (e.g. `Status.OK == Status.FAIL`).
5. **UP042** — `class Label(str, enum.Enum)`; on Python 3.11+ the dedicated `enum.StrEnum` base gives the right `str()` behavior.

## Example: Abstract base classes

A storage-interface module where one ABC abstracts nothing and another stacks its decorators in the wrong order with deprecated spellings.

### Bad

```python
"""Storage interfaces."""

import abc


class Validator(abc.ABC):  # B024
    def validate(self):  # B027
        ...


class Repository(abc.ABC):
    @abc.abstractclassmethod  # UP051
    def connect(cls):
        ...

    @abc.abstractmethod  # RUF074
    @property
    def url(self):
        ...
```

### Good

```python
"""Storage interfaces."""

import abc


class Validator(abc.ABC):
    @abc.abstractmethod
    def validate(self):
        ...


class Repository(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def connect(cls):
        ...

    @property
    @abc.abstractmethod
    def url(self):
        ...
```

### Violations

1. **B024** — `class Validator(abc.ABC)` with no abstract members; it cannot be instantiated yet forces subclasses to implement nothing.
2. **B027** — empty `def validate(self)` in an ABC without `@abstractmethod`; a forgotten override silently inherits a no-op.
3. **RUF074** — `@abc.abstractmethod` placed over `@property`; decorators apply bottom-up, so `@abstractmethod` belongs innermost to wrap the function.
4. **UP051** — `@abc.abstractclassmethod`; deprecated since Python 3.3 — compose `@classmethod` with `@abc.abstractmethod` instead.

## Example: Methods and properties

A report helper where method kinds are declared by assignment, properties take arguments and forget to return, and `self` means three different things.

### Bad

```python
"""Report helpers."""

import warnings


class Registry:
    def create(cls):  # PLR0202
        return cls()

    create = classmethod(create)

    def normalize(text):  # PLR0203
        return text.strip().lower()

    normalize = staticmethod(normalize)


class Report:
    def title(self):  # PLR6301
        return "Quarterly report"

    def extend(self, suffix):
        self = self.title() + suffix  # PLW0642
        return self

    @staticmethod
    def footer(self):  # PLW0211
        return f"page of {self}"

    @property
    def summary(self, verbose):  # PLR0206
        return self.render(verbose)

    @property
    def header(self):  # RUF066
        f"== {self.title()} =="

    @property
    def legacy_name(self):
        warnings.warn("use title instead")  # B028
        return self.title()

    def render(self, verbose=False):
        return self.title()
```

### Good

```python
"""Report helpers."""

import warnings


class Registry:
    @classmethod
    def create(cls):
        return cls()

    @staticmethod
    def normalize(text):
        return text.strip().lower()


class Report:
    @staticmethod
    def title():
        return "Quarterly report"

    def extend(self, suffix):
        extended = self.title() + suffix
        return extended

    @staticmethod
    def footer(page):
        return f"page of {page}"

    @property
    def header(self):
        return f"== {self.title()} =="

    @property
    def legacy_name(self):
        warnings.warn("use title instead", stacklevel=2)
        return self.title()

    def summary(self, verbose=False):
        return self.render(verbose)

    def render(self, verbose=False):
        return self.title()
```

### Violations

1. **B028** — `warnings.warn("use title instead")` without `stacklevel`; the warning blames a line inside the library instead of the caller — pass `stacklevel=2`.
2. **PLR0202** — `create = classmethod(create)`; declare the method kind with `@classmethod` at the definition, where readers look.
3. **PLR0203** — `normalize = staticmethod(normalize)`; same legacy assignment form — use `@staticmethod`.
4. **PLR0206** — `@property def summary(self, verbose)`; properties are accessed as attributes with no way to pass arguments — parameterized behavior is a method.
5. **PLR6301** — `def title(self)` never touches `self`; make it a `@staticmethod` or module function so the signature tells the truth.
6. **PLW0211** — `@staticmethod def footer(self)`; static methods receive no implicit first argument, so naming one `self` is a lie.
7. **PLW0642** — `self = self.title() + suffix`; rebinding `self` loses the original instance and swaps what the name means mid-method.
8. **RUF066** — `@property def header(self)` discards the f-string; a property without `return` always evaluates to `None`.

## Example: Public surface and `__init__` modules

**Config:** pair8

A package `__init__.py` that grew a god class, a duplicated class field, and an unsorted manifest with a repeated export.

### Bad

```python
# File: shop/__init__.py
"""Shop package."""

__all__ = [  # RUF022
    "Linter",
    "helper",
    "Config",
    "Linter",  # RUF068
]


class Config:  # RUF067
    theme = "light"
    indent = 4
    theme = "dark"  # PIE794


class Linter:  # PLR0904,RUF067
    def __init__(self):
        self.results = []

    def run(self, tool):
        return f"{tool}: {len(self.results)} issues"

    def bandit(self): return self.run("bandit")
    def black(self): return self.run("black")
    def flake8(self): return self.run("flake8")
    def isort(self): return self.run("isort")
    def mypy(self): return self.run("mypy")
    def pydocstyle(self): return self.run("pydocstyle")
    def pyright(self): return self.run("pyright")
    def pylint(self): return self.run("pylint")
    def ruff(self): return self.run("ruff")
    def vulture(self): return self.run("vulture")
    def bandit_settings(self): return self.run("bandit -v")
    def black_settings(self): return self.run("black -v")
    def flake8_settings(self): return self.run("flake8 -v")
    def isort_settings(self): return self.run("isort -v")
    def mypy_settings(self): return self.run("mypy -v")
    def pydocstyle_settings(self): return self.run("pydocstyle -v")
    def pyright_settings(self): return self.run("pyright -v")
    def pylint_settings(self): return self.run("pylint -v")
    def ruff_settings(self): return self.run("ruff -v")
    def vulture_settings(self): return self.run("vulture -v")
```

### Good

```python
# File: shop/__init__.py
"""Shop package."""

from shop.linters import Linter
from shop.settings import Config, helper

__all__ = [
    "Config",
    "Linter",
    "helper",
]
```

### Violations

1. **PIE794** — `theme = "dark"` re-defines `theme`; one assignment is dead code and the survivor may not be the intended one.
2. **PLR0904** — `class Linter` with 22 public methods; past the threshold the class has absorbed several responsibilities — split collaborators out and compose them.
3. **RUF022** — `__all__` out of order; keep isort-style order (constants, then CamelCase, then the rest; natural sort within).
4. **RUF067** — `shop/__init__.py` defines `Config` and `Linter`; keep `__init__.py` to docstrings, re-exports, and `__all__` — real code lives in submodules.
5. **RUF068** — `"Linter"` listed twice in `__all__`; duplicates signal incomplete refactoring — list each export once.

## Example: Stub comparison contracts

A type stub for the geometry module where comparison operators hide behind `Any` and old class syntax lingers.

### Bad

```python
# File: geometry.pyi
from typing import Any


class Shape(object):  # UP004
    def sides(self) -> int: ...


class Square(Shape, Shape):  # PLE0241
    side: float


class Point:
    x: float
    y: float

    def __eq__(self, obj: Any) -> bool: ...  # PYI032
    def __ne__(self, obj: Any) -> bool: ...  # PYI032
    def __hash__(self) -> int: ...
```

### Good

```python
# File: geometry.pyi
class Shape:
    def sides(self) -> int: ...


class Square(Shape):
    side: float


class Point:
    x: float
    y: float

    def __eq__(self, obj: object) -> bool: ...
    def __ne__(self, obj: object) -> bool: ...
    def __hash__(self) -> int: ...
```

### Violations

1. **PYI032** — `def __eq__(self, obj: Any)` and `def __ne__(self, obj: Any)`; `==`/`!=` must accept any object safely, so annotate the second parameter as `object`, not the type-checker escape hatch `Any`.
