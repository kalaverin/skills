---
---

# Numbers

Handle numeric literals and precision correctly: Decimal, float comparison, int casts, octal permissions.

## Example: Price constants and permissions

A junior's price updater that gets every numeric literal wrong: float-based `Decimal`, a pointless `round`, a direct float equality check, and a decimal file mode.

### Bad

```python
"""Price updater."""

import os
from decimal import Decimal

RATE = Decimal(0.2)  # RUF032
FLAT = round(100, 0)  # RUF057


def apply(path, amount):
    if 0.1 + 0.2 == 0.3:  # RUF069
        return amount
    os.chmod(path, 644)  # RUF064
    return amount * RATE + FLAT
```

### Good

```python
"""Price updater."""

import math
import os
from decimal import Decimal

RATE = Decimal("0.2")
FLAT = 100


def apply(path, amount):
    if math.isclose(0.1 + 0.2, 0.3, abs_tol=1e-9):
        return amount
    os.chmod(path, 0o644)
    return amount * RATE + FLAT
```

### Violations

1. **RUF032** — `RATE = Decimal(0.2)`; `Decimal` should be built from a string literal to keep exact precision.
2. **RUF057** — `FLAT = round(100, 0)`; rounding an integer is a no-op.
3. **RUF064** — `os.chmod(path, 644)`; permission modes are octal, so write `0o644`.
4. **RUF069** — `if 0.1 + 0.2 == 0.3:`; float equality is unreliable, use `math.isclose`.

## Example: Indices, increments, and version parsing

A compatibility shim that confuses string and integer indices, tries C-style prefix increments, parses versions with `map(int, ...)`, and wraps `len()` in `int()`.

### Bad

```python
"""Compatibility shim."""

__version__ = "1.2.0"


class LegacyLoader:
    def __init__(self, rows):
        self.rows = rows
        self.index = 0

    def next_row(self):
        ++self.index  # B002
        return self.rows[self.index]

    def version_parts(self):
        major, minor = map(int, __version__.split("."))  # RUF048
        return [major, minor]["0"]  # RUF016

    def count(self):
        return int(len(self.rows))  # RUF046
```

### Good

```python
"""Compatibility shim."""

from packaging import version as pkg

__version__ = "1.2.0"


class LegacyLoader:
    def __init__(self, rows):
        self.rows = rows
        self.index = -1

    def next_row(self):
        self.index += 1
        return self.rows[self.index]

    def version_parts(self):
        parsed = pkg.parse(__version__)
        return parsed.major, parsed.minor

    def count(self):
        return len(self.rows)
```

### Violations

1. **B002** — `++self.index`; Python has no prefix `++`, use `+= 1`.
2. **RUF016** — `[major, minor]["0"]`; indexing a list with a string raises `TypeError`, use an integer index.
3. **RUF046** — `int(len(self.rows))`; `len()` already returns an integer.
4. **RUF048** — `map(int, __version__.split("."))`; version strings may contain non-numeric segments, parse with a dedicated version parser.

## Rule of thumb

1. Build `Decimal` from string literals, never from float literals.
2. Compare floats with `math.isclose` (or `cmath.isclose`) instead of `==` or `!=`.
3. Write file permission modes as octal literals (`0o644`, `0o755`).
4. Remove pointless `round(x, 0)` and `int(len(...))` when the value is already an integer.
5. Use integer indices and slices for sequences; parse `__version__` with a proper version parser.
6. Mutate counters with `+= 1` or `-= 1`; Python does not have prefix `++` or `--`.
