---
---

# Scope

Manage namespaces: accurate `__all__`, correct `global`/`nonlocal`, no shadowing, no undefined or unused names.

## Rule of thumb

1. Define or import every name before you read it; an assignment inside a nested scope makes the name local, so do not read an outer binding before declaring `global` or `nonlocal`.
2. Do not shadow an existing binding with a loop variable, import, or reassignment; pick a fresh name instead.
3. Use `global` only to reassign a module-level name from inside a function, and never combine `global` with `nonlocal` for the same name or place `global` at module level.
4. Use `nonlocal` only when an enclosing non-global binding already exists, and place the declaration before any use of the name.
5. Keep `__all__` as a `tuple` or `list` of literal strings, and make sure every name listed is actually defined in the module.
6. Remove assignments and annotations that are never read, or prefix intentionally ignored names with `_`.

## Example: Shadowing imports and names

A junior's report builder duplicates an import, shadows it with a loop variable, and reassigns a variable before reading it.

### Bad

```python
"""Report builder."""

from os import path
import json
import yaml
import json  # F811


def build(records, cfg):
    for path in records:  # F402
        text = json.dumps(path)
    parsed = yaml.safe_load(cfg)  # F841
    return text


def dump(records):
    return yaml.safe_dump(records)
```

### Good

```python
"""Report builder."""

import json

import yaml
from os import path


def build(records, cfg):
    out_dir = path.dirname(cfg)
    texts = []
    for record in records:
        texts.append(json.dumps(record))
    parsed = yaml.safe_load(cfg)
    return out_dir, texts, parsed


def dump(records):
    return yaml.safe_dump(records)
```

### Violations

1. **F402** — `for path in records`; shadows the imported `path`.
2. **F811** — `import json` (second occurrence); redefines `json` before it is used.

## Example: Undefined names and premature locals

A score keeper reads an undefined score and uses `+=` on an outer variable without declaring it.

### Bad

```python
"""Score keeper."""

TARGET = 100


# Aim for the target.


def make_adder():
    total = 0

    def add(points):
        total += points  # F823
        return total + score  # F821

    return add


def report(player):
    return f"{player}: {score}"  # F821
```

### Good

```python
"""Score keeper."""

TARGET = 100


def make_adder():
    total = 0

    def add(points, score):
        nonlocal total
        total += points
        return total + score

    return add


def report(player, score):
    return f"{player}: {score}"
```

### Violations

1. **F821** — `return total + score` and `return f"{player}: {score}"`; `score` is not defined anywhere.
2. **F823** — `total += points`; the assignment makes `total` local, so it is read before being bound.

## Example: Unused bindings and annotations

A packet parser keeps dead variables and bare annotations that never influence the result.

### Bad

```python
"""Parse helpers."""


def parse(data):
    header: dict  # F842
    payload = data[:4]
    body = data[4:]  # F841
    trailer = data[-2:]  # F841
    return payload


def describe():
    label: str  # F842
    return "packet"
```

### Good

```python
"""Parse helpers."""


def parse(data):
    return data[:4]


def describe():
    return "packet"
```

### Violations

1. **F841** — `body = data[4:]` and `trailer = data[-2:]`; assigned but never read.
2. **F842** — `header: dict` and `label: str`; bare annotations with no assignment or later use.

## Example: Conflicting global and nonlocal declarations

A junior mixes `global` and `nonlocal`, declares `nonlocal` without a binding, and reads a name before declaring it global.

### Bad

```python
"""Namespace mistakes."""


def broken():
    global counter  # PLE0115,PLW0602
    nonlocal counter  # PLE0117
    # This should never happen.
    pass


def fetch():
    nonlocal value  # PLE0117


def log():
    # Log current counter.
    print(counter)  # PLE0118
    global counter  # PLW0602
```

### Good

```python
"""Namespace fixes."""


def outer():
    """Return a closure over value."""
    value = 1

    def fetch():
        nonlocal value
        return value

    return fetch


def log(counter):
    """Log the counter."""
    print(counter)
```

### Violations

1. **PLE0115** — `global counter` in `broken()`; `counter` is also declared `nonlocal` in the same scope.
2. **PLE0117** — `nonlocal counter` and `nonlocal value`; no enclosing non-global binding exists.
3. **PLE0118** — `print(counter)` in `log()`; `counter` is used before the `global counter` declaration.
4. **PLW0602** — `global counter` in `broken()` and `log()`; `counter` is declared global but never assigned in the function.

## Example: Module-level global state and public exports

A state module uses redundant global declarations, mutates state through `global`, and assigns `__all__` as a bare string.

### Bad

```python
# File: shop/state.py

"""State module."""

global counter  # PLW0603,PLW0604
counter = 0


def read():
    return counter


def update():
    global counter  # PLW0603
    counter += 1


__all__ = "counter"  # PLE0605
```

### Good

```python
# File: shop/state.py

"""State module."""

counter = 0


def read():
    return counter


def update(value):
    return value + 1


counter = update(counter)

__all__ = ("counter",)
```

### Violations

1. **PLE0605** — `__all__ = "counter"`; `__all__` must be a tuple or list.
2. **PLW0603** — `global counter` at module level and in `update()`; using global to mutate state is discouraged.
3. **PLW0604** — `global counter` at module level; every module-level name is already global.

## Example: Exports list with missing and invalid names

A package `__init__.py` exposes an imported module object directly and lists a name that does not exist.

### Bad

```python
# File: shop/api/__init__.py

"""Public shop API."""

from shop.api import orders
from shop.api import products


class ProductView: ...


def default_view():
    return ProductView()


__all__ = ["orders", "products", ProductView, "checkout"]  # F822,PLE0604
```

### Good

```python
# File: shop/api/__init__.py

"""Public shop API."""

from shop.api import orders
from shop.api import products


class ProductView: ...


def default_view():
    return ProductView()


__all__ = ["orders", "products", "ProductView"]
```

### Violations

1. **F822** — `"checkout"` in `__all__`; `checkout` is not defined in the module.
2. **PLE0604** — `ProductView` in `__all__`; `__all__` entries must be strings.
