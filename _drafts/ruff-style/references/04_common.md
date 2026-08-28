---
---

# Common

Write against the current stdlib and syntax: dedicated modern APIs, zero Python 2 residue, and version guards that survive Python 3.10+ and a hypothetical Python 4.

## Rule of thumb

1. Slurp and write whole files with `Path.read_text`/`write_text`, resolve the cwd with `Path.cwd()`, and pass only non-default modes to `open`.
2. Name the operation instead of hand-rolling it: `.clear()`, `.discard()`, `.copy()`, `removeprefix`/`removesuffix`, `.hexdigest()`, `int.bit_count()`, `math.log2`/`log10`.
3. Reference stdlib constants — `math.pi`, `string.digits`, `re.IGNORECASE`, `datetime.UTC` — never retype them as literals.
4. Call constructors directly (`Decimal(0)`, `Fraction(x)`, `int(s, 0)` for prefixed numbers) instead of factory classmethods, string casts, or manual prefix slicing.
5. Import every name from its modern home (`collections.abc`, `unittest.mock`, `ElementTree`, from-import submodule form) and use current call spellings: `text=True`, `capture_output=True`, `sys.exit`, builtin `OSError`/`TimeoutError`; delete Python 2 residue on sight (coding cookies, stale `__future__` imports, `u""` prefixes, `io.open`, `builtins` shims).
6. Shape classes and statements minimally: `class C(ABC)`, `UserDict`/`UserList`/`UserString` bases, one comma-separated `global`, no empty parens, no bare `#` comments.
7. Compare versions as tuples — `sys.version_info >= (3, 11)` — never slice or string-compare `sys.version`, never test the minor alone, delete guards below the project minimum; in `.pyi` stubs use only flat `<`/`>=` checks against two-element tuples.

## Example: Whole-file I/O and path lookup

A junior's report tool that wraps one-shot file operations in handle ceremony and finds the cwd by accident.

### Bad

```python
import io
from pathlib import Path


def load_template():
    with open("template.txt") as f:  # FURB101
        return f.read()


def write_report(text):
    with open("report.txt", "w") as f:  # FURB103
        f.write(text)


def count_lines():
    total = 0
    with open("report.txt", "r") as f:  # UP015
        for line in f:
            total += 1
    return total


def schema_lines():
    lines = []
    with io.open("schema.json") as f:  # UP020
        for line in f:
            lines.append(line.rstrip())
    return lines


def here():
    return Path().resolve()  # FURB177
```

### Good

```python
from pathlib import Path


def load_template():
    return Path("template.txt").read_text()


def write_report(text):
    Path("report.txt").write_text(text)


def count_lines():
    total = 0
    with open("report.txt") as f:
        for line in f:
            total += 1
    return total


def schema_lines():
    lines = []
    with open("schema.json") as f:
        for line in f:
            lines.append(line.rstrip())
    return lines


def here():
    return Path.cwd()
```

### Violations

1. **FURB101** — `with open("template.txt") ... f.read()`; whole-file slurps are one `Path.read_text` call.
2. **FURB103** — `with open("report.txt", "w") ... f.write(text)`; one-shot writes are one `Path.write_text` call.
3. **FURB177** — `Path().resolve()`; cwd-by-side-effect, `Path.cwd()` states the intent.
4. **UP015** — `open("report.txt", "r")`; `"r"` is the default mode, keep only load-bearing modes.
5. **UP020** — `io.open("schema.json")`; Python 2 compatibility alias of the builtin `open`.

## Example: Container and string idioms

Cleanup helpers that hand-roll operations the stdlib already names.

### Bad

```python
import re


def reset_board():
    grid = [[0, 1], [1, 0]]
    scores = {"alice": 10}
    del grid[:]  # FURB131
    del scores[:]  # FURB131
    return grid, scores


def normalize_tags():
    tags = {"news", "temp", "local"}
    if "temp" in tags:  # FURB132
        tags.remove("temp")
    return tags


def snapshot():
    history = [1, 2, 3]
    backup = history[:]  # FURB145
    return backup


def is_digit(char):
    return char in "0123456789"  # FURB156


def is_hello(text):
    return bool(re.search("^hello", text, re.I))  # FURB167


def trim(name, text):
    name = name[:-4] if name.endswith(".txt") else name  # FURB188
    if text.startswith("pre"):  # FURB188
        text = text[3:]
    return name, text
```

### Good

```python
import re
import string


def reset_board():
    grid = [[0, 1], [1, 0]]
    scores = {"alice": 10}
    grid.clear()
    scores.clear()
    return grid, scores


def normalize_tags():
    tags = {"news", "temp", "local"}
    tags.discard("temp")
    return tags


def snapshot():
    history = [1, 2, 3]
    backup = history.copy()
    return backup


def is_digit(char):
    return char in string.digits


def is_hello(text):
    return bool(re.search("^hello", text, re.IGNORECASE))


def trim(name, text):
    name = name.removesuffix(".txt")
    text = text.removeprefix("pre")
    return name, text
```

### Violations

1. **FURB131** — `del grid[:]` and `del scores[:]`; `.clear()` is the named empty-the-container operation.
2. **FURB132** — `if "temp" in tags: tags.remove("temp")`; the guard exists only to dodge `KeyError`, `discard` is remove-if-present.
3. **FURB145** — `backup = history[:]`; unbounded slice copies by accident, `.copy()` declares intent.
4. **FURB156** — `"0123456789"`; hand-typed charsets drift, `string.digits` is canonical.
5. **FURB167** — `re.I`; one-letter flag alias, the long name `re.IGNORECASE` is self-documenting.
6. **FURB188** — `name[:-4] if name.endswith(".txt")` and `text[3:]` after `startswith`; 3.9+ `removesuffix`/`removeprefix` encode check and removal.

## Example: Numeric, decimal, and hashing shortcuts

An analytics helper that retypes constants, round-trips values through strings, and reimplements library methods.

### Bad

```python
import math
from decimal import Decimal
from fractions import Fraction
from hashlib import sha512


def circle_area(radius):
    return 3.141592 * radius**2  # FURB152


def zero_price():
    return Decimal("0")  # FURB157


def infinite_limit():
    return Decimal.from_float(float("inf"))  # FURB164


def popcount(mask):
    return bin(mask).count("1")  # FURB161


def scales(value):
    return math.log(value, 2), math.log(value, 10)  # FURB163


def ratio(price):
    return Fraction.from_float(price)  # FURB164


def parse_color():
    text = "0xFF00AA"
    return int(text[2:], 16)  # FURB166


def checksum(data):
    return sha512(data).digest().hex()  # FURB181
```

### Good

```python
import math
from decimal import Decimal
from fractions import Fraction
from hashlib import sha512


def circle_area(radius):
    return math.pi * radius**2


def zero_price():
    return Decimal(0)


def infinite_limit():
    return Decimal("inf")


def popcount(mask):
    return mask.bit_count()


def scales(value):
    return math.log2(value), math.log10(value)


def ratio(price):
    return Fraction(price)


def parse_color():
    text = "0xFF00AA"
    return int(text, 0)


def checksum(data):
    return sha512(data).hexdigest()
```

### Violations

1. **FURB152** — `3.141592`; hardcoded pi loses precision and hides intent, `math.pi` is exact and named.
2. **FURB157** — `Decimal("0")`; the constructor takes ints and `"inf"` directly (quoted float literals like `"0.1"` stay quoted).
3. **FURB161** — `bin(mask).count("1")`; `int.bit_count()` (3.10+) is the direct population count.
4. **FURB163** — `math.log(value, 2)` and `math.log(value, 10)`; dedicated `log2`/`log10` variants are more accurate (base `e` is the default).
5. **FURB164** — `Decimal.from_float(...)` and `Fraction.from_float(price)`; constructors accept floats directly since 3.2, `from_*` survives only for type validation.
6. **FURB166** — `int(text[2:], 16)`; base `0` lets `int` read the `0x`/`0o`/`0b` prefix itself.
7. **FURB181** — `.digest().hex()`; reimplements `.hexdigest()` in two steps.

## Example: Datetime and caching

A small service module with memoized helpers and timestamp parsing, written with pre-3.11 habits.

### Bad

```python
import functools
from datetime import datetime, timezone


@functools.lru_cache()  # UP011
def default_timeout():
    return 30


@functools.lru_cache(maxsize=None)  # UP033
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def parse_timestamp(raw):
    return datetime.fromisoformat(raw.replace("Z", "+00:00"))  # FURB162


def utc_now():
    return datetime.now(timezone.utc)  # UP017
```

### Good

```python
import functools
from datetime import UTC, datetime


@functools.lru_cache
def default_timeout():
    return 30


@functools.cache
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def parse_timestamp(raw):
    return datetime.fromisoformat(raw)


def utc_now():
    return datetime.now(UTC)
```

### Violations

1. **FURB162** — `raw.replace("Z", "+00:00")`; 3.11+ parses `Z` natively, the string surgery is dead code.
2. **UP011** — `@functools.lru_cache()`; bare decoration works since 3.8, empty parens are pre-3.8 muscle memory.
3. **UP017** — `timezone.utc`; `datetime.UTC` (3.11+) is the short canonical alias.
4. **UP033** — `lru_cache(maxsize=None)`; `functools.cache` (3.9+) is exactly that, with a name that says unbounded.

## Example: Class and statement shape

A plugin registry with metaclass ritual, builtin subclassing, repeated globals, and punctuation noise.

### Bad

```python
import abc

COUNT = 0
REGISTRY = {}


class Plugin(metaclass=abc.ABCMeta):  # FURB180
    pass


class Config():  # UP039
    pass


class CaseDict(dict):  # FURB189
    def __setitem__(self, key, value):
        super().__setitem__(key.lower(), value)


def register(name):  #  # PLR2044
    global COUNT  # FURB154
    global REGISTRY
    COUNT += 1
    REGISTRY[name] = name
    print((name))  # UP034
    return CaseDict({name: COUNT})
```

### Good

```python
from abc import ABC
from collections import UserDict

COUNT = 0
REGISTRY = {}


class Plugin(ABC):
    pass


class Config:
    pass


class CaseDict(UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key.lower(), value)


def register(name):
    global COUNT, REGISTRY
    COUNT += 1
    REGISTRY[name] = name
    print(name)
    return CaseDict({name: COUNT})
```

### Violations

1. **FURB154** — consecutive `global COUNT` / `global REGISTRY`; one statement accepts comma-separated names.
2. **FURB180** — `metaclass=abc.ABCMeta`; inheriting `abc.ABC` is semantically identical and shorter.
3. **FURB189** — `class CaseDict(dict)`; builtin containers bypass overridden dunders (`dict.__init__` skips `__setitem__`), `UserDict` delegates faithfully.
4. **PLR2044** — `def register(name):  #`; a bare comment marker is clutter with zero information.
5. **UP034** — `print((name))`; parens around a sole call argument are pure noise.
6. **UP039** — `class Config()`; a baseless class needs no parentheses.

## Example: Legacy imports and Python 2 residue

An inventory module ported from Python 2 whose header and import block are pure compatibility fossils.

### Bad

```python
# -*- coding: utf-8 -*-  # UP009
from __future__ import print_function  # UP010

import concurrent.futures as futures  # PLR0402
import mock  # UP026
from builtins import str  # UP029
from collections import Mapping  # UP035
from xml.etree import cElementTree as ET  # UP023

TITLE = u"inventory"  # UP025


def parse_catalog(path):
    return ET.parse(path).getroot()


def merge_settings(defaults, overrides):
    merged = dict(defaults)
    if isinstance(overrides, Mapping):
        merged.update(overrides)
    return merged


def render_items(items):
    with futures.ThreadPoolExecutor() as pool:
        return list(pool.map(str, items))


def fake_catalog():
    return mock.Mock(name="catalog")
```

### Good

```python
from collections.abc import Mapping
from concurrent import futures
from unittest import mock
from xml.etree import ElementTree as ET

TITLE = "inventory"


def parse_catalog(path):
    return ET.parse(path).getroot()


def merge_settings(defaults, overrides):
    merged = dict(defaults)
    if isinstance(overrides, Mapping):
        merged.update(overrides)
    return merged


def render_items(items):
    with futures.ThreadPoolExecutor() as pool:
        return list(pool.map(str, items))


def fake_catalog():
    return mock.Mock(name="catalog")
```

### Violations

1. **PLR0402** — `import concurrent.futures as futures`; aliasing a submodule to its own name is what `from concurrent import futures` spells.
2. **UP009** — `# -*- coding: utf-8 -*-`; UTF-8 has been the default source encoding since PEP 3120.
3. **UP010** — `from __future__ import print_function`; the feature is already live at the project's target version.
4. **UP023** — `cElementTree`; deprecated since 3.3, the C accelerator is automatic inside `ElementTree`.
5. **UP025** — `u"inventory"`; every Python 3 string is Unicode, the prefix says nothing.
6. **UP026** — `import mock`; the backport is a needless dependency, `mock` lives in the stdlib as `unittest.mock` since 3.3.
7. **UP029** — `from builtins import str`; a Python 2 shim that shadows the real builtin for nothing.
8. **UP035** — `from collections import Mapping`; ABCs moved to `collections.abc` in 3.3 and the re-exports were removed in 3.10.

## Example: Legacy runtime spellings

A nightly maintenance module using renamed subprocess flags, removed unittest aliases, merged error classes, and a REPL-only exit.

### Bad

```python
"""Nightly maintenance jobs."""
import asyncio
import subprocess
from unittest import TestCase


def run_backup():
    return subprocess.run(["backup.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # UP022


def fetch_text(url):
    proc = subprocess.run(["curl", "-s", url], universal_newlines=True)  # UP021
    return proc.stdout


class JobsTest(TestCase):
    def test_fetch(self):
        self.assertEquals(fetch_text("example.com"), "ok")  # UP005


def load_state(path):
    try:
        with open(path) as fh:
            return [line.strip() for line in fh]
    except EnvironmentError:  # UP024
        raise IOError("state unreadable")  # UP024


async def fetch_job(coro):
    try:
        return await asyncio.wait_for(coro, timeout=5)
    except asyncio.TimeoutError:  # UP041
        return None


if __name__ == "__main__":
    exit()  # PLR1722
```

### Good

```python
"""Nightly maintenance jobs."""
import asyncio
import subprocess
import sys
from unittest import TestCase


def run_backup():
    return subprocess.run(["backup.sh"], capture_output=True)


def fetch_text(url):
    proc = subprocess.run(["curl", "-s", url], capture_output=True, text=True)
    return proc.stdout


class JobsTest(TestCase):
    def test_fetch(self):
        self.assertEqual(fetch_text("example.com"), "ok")


def load_state(path):
    try:
        with open(path) as fh:
            return [line.strip() for line in fh]
    except OSError:
        raise OSError("state unreadable")


async def fetch_job(coro):
    try:
        return await asyncio.wait_for(coro, timeout=5)
    except TimeoutError:
        return None


if __name__ == "__main__":
    sys.exit()
```

### Violations

1. **PLR1722** — `exit()`; a `site`-module REPL convenience that may `NameError` (`python -S`), `sys.exit` always exists.
2. **UP005** — `self.assertEquals(...)`; deprecated unittest alias, removed in 3.12.
3. **UP021** — `universal_newlines=True`; renamed to `text` in 3.7 and kept only for backcompat.
4. **UP022** — `stdout=subprocess.PIPE, stderr=subprocess.PIPE`; `capture_output=True` (3.7+) is exactly that in one flag.
5. **UP024** — `EnvironmentError` and `IOError`; aliases merged into `OSError` in 3.3, use the builtin.
6. **UP041** — `asyncio.TimeoutError`; alias of the builtin `TimeoutError` since 3.11, the builtin is future-proof.

## Example: Runtime version guards

A feature-gate module that slices and string-compares `sys.version`, equality-tests version components, and keeps dead compatibility branches.

### Bad

```python
"""Feature gates for the worker."""
import sys

import six

IS_PY3 = six.PY3  # YTT202
SHORT = sys.version[:3]  # YTT101
MINOR_DIGIT = sys.version[2]  # YTT102
MAJOR_CHAR = sys.version[0]  # YTT301
MAJOR_SLICE = sys.version[:1]  # YTT303


def uses_walrus():
    if sys.version > "3.9":  # YTT103
        return True
    return False


def supported():
    if sys.version >= "3":  # YTT302
        return True
    return False


def is_modern():
    if sys.version_info[0] == 3:  # UP036,YTT201
        return "py3"
    return "py2"


def needs_legacy():
    if sys.version_info[1] < 7:  # YTT203
        return True
    if sys.version_info.minor < 8:  # YTT204
        return True
    return False


if sys.version_info < (3, 0):  # UP036
    print("py2 compat")
else:
    print("py3")
```

### Good

```python
"""Feature gates for the worker."""
import sys

IS_PY3 = sys.version_info >= (3,)
SHORT = sys.version_info[:2]
MINOR = sys.version_info.minor
MAJOR = sys.version_info.major
USES_WALRUS = sys.version_info >= (3, 8)
SUPPORTED = sys.version_info >= (3, 12)
NEEDS_LEGACY = sys.version_info < (3, 8)
```

### Violations

1. **UP036** — `if sys.version_info < (3, 0)`; the branch is unreachable at the project's minimum version, delete the dead compat code.
2. **YTT101** — `sys.version[:3]`; fixed-width slicing truncates two-digit minors (`"3.10"` becomes `"3.1"`).
3. **YTT102** — `sys.version[2]`; picks one character, not the minor number — `.minor` is the real value.
4. **YTT103** — `sys.version > "3.9"`; lexicographic comparison is `False` on 3.10 (`"3.10" < "3.9"`).
5. **YTT201** — `sys.version_info[0] == 3`; equality encodes "exactly 3" and misfires on Python 4, `>= (3,)` says "3 or later".
6. **YTT202** — `six.PY3`; defined as `version_info[0] == 3`, so `False` on Python 4 — drop `six` and compare tuples.
7. **YTT203** — `sys.version_info[1] < 7`; minor-only comparison ignores the major, a 4.0 interpreter takes the wrong branch.
8. **YTT204** — `sys.version_info.minor < 8`; same trap via the named attribute, compare the full `(major, minor)` tuple.
9. **YTT301** — `sys.version[0]`; one character is not the major version on Python 10, `.major` is immune.
10. **YTT302** — `sys.version >= "3"`; lexicographic ordering puts `"10..."` before `"3"`, only tuple comparison is correct.
11. **YTT303** — `sys.version[:1]`; hardcodes a one-digit major, structured fields don't care about digit count.

## Example: Stub version guards

**Target:** `py39`

A `.pyi` stub whose version conditionals fall outside the grammar type checkers understand.

### Bad

```python
# File: geometry.pyi
import sys

if (3, 10) <= sys.version_info < (3, 12):  # PYI002
    def circumference(radius: float) -> float: ...
if sys.version_info[0] == "2":  # PYI003
    def legacy_unit() -> str: ...
if sys.version_info >= (3, 4, 3):  # PYI004,UP036
    def area(radius: float) -> float: ...
if sys.version_info[:2] == (3,):  # PYI005
    def diameter(radius: float) -> float: ...
if sys.version_info > (3, 8):  # PYI006,UP036
    def volume(radius: float) -> float: ...
```

### Good

```python
# File: geometry.pyi
import sys

if sys.version_info >= (3, 10) and sys.version_info < (3, 12):
    def circumference(radius: float) -> float: ...
if sys.version_info >= (3, 11):
    def area(radius: float) -> float: ...
    def diameter(radius: float) -> float: ...
    def volume(radius: float) -> float: ...
```

### Violations

1. **PYI002** — `if (3, 10) <= sys.version_info < (3, 12)`; chained comparisons are outside the recognized grammar, join flat tests with `and`.
2. **PYI003** — `sys.version_info[0] == "2"`; comparing version components to strings is never true and unrecognized.
3. **PYI004** — `sys.version_info >= (3, 4, 3)`; checkers model versions as `(major, minor)` only, patch components are uninterpretable.
4. **PYI005** — `sys.version_info[:2] == (3,)`; mismatched tuple lengths make a constant-false condition the checker can't use.
5. **PYI006** — `sys.version_info > (3, 8)`; stubs allow only `<` and `>=` — `>`, `<=`, `==` have edge-case semantics (3.8.10 is neither `==` nor `<=` `(3, 8)`).
