---
---

# Functions

Define functions and lambdas with clean signatures: keyword-only booleans, no unused args, correct singledispatch and kwargs.

## Rule of thumb

1. Remove unused arguments or prefix them with `_`; every parameter must earn its place.
2. Make boolean parameters keyword-only; never pass `True`/`False` positionally.
3. Prefer `def` over assigning a lambda; inline one-shot expressions and pass callables directly.
4. Use functions from the `operator` module instead of wrapper lambdas.
5. Choose `@singledispatch` for standalone functions and `@singledispatchmethod` for methods.
6. Do not repeat keyword arguments or let dict unpacking collide with explicit kwargs.

## Example: Unused arguments

A junior's report builder declares parameters everywhere but only uses some of them.

### Bad

```python
class ReportBuilder:
    def __init__(self, title):
        self.title = title

    def header(self, prefix, suffix):  # ARG002
        return f"{prefix}: {self.title}"

    @classmethod
    def from_text(cls, text, tags):  # ARG003
        return cls(text)

    @staticmethod
    def merge(left, right):  # ARG004
        return left


def format_name(first, last):  # ARG001
    return f"Hello, {first}!"


scores = [1, 2, 3]
scaled = list(map(lambda x, factor: x * 2, scores))  # ARG005
```

### Good

```python
class ReportBuilder:
    def __init__(self, title):
        self.title = title

    def header(self, prefix):
        return f"{prefix}: {self.title}"

    @classmethod
    def from_text(cls, text):
        return cls(text)

    @staticmethod
    def merge(left):
        return left


def format_name(first):
    return f"Hello, {first}!"


scores = [1, 2, 3]
scaled = list(map(lambda x: x * 2, scores))
```

### Violations

1. **ARG001** — `def format_name(first, last):`; `last` is declared but never used.
2. **ARG002** — `def header(self, prefix, suffix):`; `suffix` is declared but never used.
3. **ARG003** — `def from_text(cls, text, tags):`; `tags` is declared but never used.
4. **ARG004** — `def merge(left, right):`; `right` is declared but never used.
5. **ARG005** — `lambda x, factor: x * 2`; `factor` is declared but never used.

## Example: Boolean trap

A text formatter that exposes positional boolean flags and calls them with bare literals.

### Bad

```python
def render(text: str, bold: bool) -> str:  # FBT001
    return f"<b>{text}</b>" if bold else text


def wrap_line(text: str, trim=True) -> str:  # FBT002
    return text.strip() if trim else text


print(render("Hi", True))  # FBT003
```

### Good

```python
def render(text: str, *, bold: bool) -> str:
    return f"<b>{text}</b>" if bold else text


def wrap_line(text: str, *, trim: bool = True) -> str:
    return text.strip() if trim else text


print(render("Hi", bold=True))
```

### Violations

1. **FBT001** — `def render(text: str, bold: bool) -> str:`; a type-hinted boolean parameter is positional.
2. **FBT002** — `def wrap_line(text: str, trim=True) -> str:`; a boolean default is positional.
3. **FBT003** — `render("Hi", True)`; a boolean literal is passed positionally.

## Example: Lambdas and operators

A small data pipeline that assigns, wraps, and reimplements what Python already provides.

### Bad

```python
import functools


double = lambda x: x * 2  # E731


radius = 5
area = (lambda r: 3.14 * r ** 2)(radius)  # PLC3002


names = ["Ada", "Grace"]
upper = list(map(lambda n: str(n), names))  # PLW0108


values = [1, 2, 3]
total = functools.reduce(lambda a, b: a + b, values)  # FURB118
```

### Good

```python
import functools
import operator


def double(x: int) -> int:
    return x * 2


radius = 5
area = 3.14 * radius ** 2


names = ["Ada", "Grace"]
upper = list(map(str, names))


values = [1, 2, 3]
total = functools.reduce(operator.add, values)
```

### Violations

1. **E731** — `double = lambda x: x * 2`; prefer a `def` with a real name and traceback.
2. **FURB118** — `functools.reduce(lambda a, b: a + b, values)`; reimplements `operator.add`.
3. **PLC3002** — `(lambda r: 3.14 * r ** 2)(radius)`; the lambda is created and called directly.
4. **PLW0108** — `lambda n: str(n)`; the lambda only forwards its argument to `str`.

## Example: singledispatch

A processor that picks the wrong singledispatch decorator for methods and functions.

### Bad

```python
from functools import singledispatch, singledispatchmethod


class Processor:
    @singledispatch  # PLE1519
    def handle(self, arg):
        return f"default: {arg}"


@singledispatchmethod  # PLE1520
def process(arg):
    return f"default: {arg}"
```

### Good

```python
from functools import singledispatch, singledispatchmethod


class Processor:
    @singledispatchmethod
    def handle(self, arg):
        return f"default: {arg}"


@singledispatch
def process(arg):
    return f"default: {arg}"
```

### Violations

1. **PLE1519** — `@singledispatch` on `handle`; use `@singledispatchmethod` for methods.
2. **PLE1520** — `@singledispatchmethod` on `process`; use `@singledispatch` for standalone functions.

## Example: Repeated keyword arguments

A move command that unpacks a dict whose key collides with an explicit keyword argument.

### Bad

```python
def move(x: int, y: int) -> None:
    print(f"move to {x},{y}")


move(1, y=2, **{"y": 3})  # PLE1132
```

### Good

```python
def move(x: int, y: int) -> None:
    print(f"move to {x},{y}")


move(1, y=2)
```

### Violations

1. **PLE1132** — `move(1, y=2, **{"y": 3})`; `y` is supplied twice and will raise `TypeError`.
