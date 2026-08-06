---
---

# Mutable Defaults

Never share mutable state across calls or instances: factories, immutable defaults, per-instance initialization.

## Rule of thumb

1. Use `None` as the default for mutable function arguments, then build a fresh object inside the function body.
2. In dataclasses, use `field(default_factory=...)` for mutable or computed defaults.
3. Put init-only defaults on `InitVar` fields, not on `__post_init__` parameters.
4. Initialize per-instance mutable state in `__init__`, or annotate it as `ClassVar` when sharing is intentional.
5. Do not use mutable objects as `ContextVar` defaults; use `None` and set per context.
6. Do not pass mutable values to `dict.fromkeys`; build distinct objects with a comprehension.
7. Do not cache instance methods with `lru_cache`/`cache`; cache pure functions that take only arguments.

## Example: Request pipeline

A junior's request-processing module that shares mutable state through argument defaults, a context variable, and a `fromkeys` shortcut.

### Bad

```python
# File: app/pipeline.py
from contextvars import ContextVar


def load_defaults() -> dict[str, int]:
    return {"timeout": 30}


REQUEST_CTX: ContextVar[dict[str, str]] = ContextVar("request_ctx", default={})  # B039


def process(data={}, overrides=load_defaults()):  # B006,B008
    data.update(overrides)
    return data


def make_buckets(keys):
    buckets = dict.fromkeys(keys, [])  # RUF024
    buckets["read"].append(1)
    return buckets
```

### Good

```python
# File: app/pipeline.py
from contextvars import ContextVar


def load_defaults() -> dict[str, int]:
    return {"timeout": 30}


REQUEST_CTX: ContextVar[dict[str, str] | None] = ContextVar("request_ctx", default=None)


def process(data=None, overrides=None):
    if data is None:
        data = {}
    if overrides is None:
        overrides = load_defaults()
    data.update(overrides)
    return data


def make_buckets(keys):
    buckets = {key: [] for key in keys}
    buckets["read"].append(1)
    return buckets
```

### Violations

1. **B006** — `data={}` in `process`; mutable dict default is shared across calls.
2. **B008** — `overrides=load_defaults()` in `process`; function call runs once at definition time.
3. **B039** — `ContextVar("request_ctx", default={})`; mutable default is shared across `.get()` calls.
4. **RUF024** — `dict.fromkeys(keys, [])`; every key stores the same list instance.

## Example: Configuration types

A junior's configuration types that reuse mutable objects across dataclass instances, leak class attributes between objects, and cache an instance method.

### Bad

```python
# File: app/types.py
from dataclasses import InitVar, dataclass
from functools import lru_cache


def load_items() -> list[str]:
    return ["a", "b"]


@dataclass
class AppConfig:
    name: str = "service"
    tags: list[str] = []  # RUF008
    items: list[str] = load_items()  # RUF009
    debug: InitVar[bool] = False
    verbose: InitVar[bool] = True

    def __post_init__(self, debug: bool = False, verbose: bool = True) -> None:  # RUF033
        self.debug = debug
        self.verbose = verbose


class StateManager:
    handlers: list[str] = []  # RUF012
    lookup: dict[str, int] = {}  # RUF012

    @lru_cache  # B019
    def rank(self, key: str) -> int:
        return self.lookup.get(key, 0)
```

### Good

```python
# File: app/types.py
from dataclasses import InitVar, dataclass, field


def load_items() -> list[str]:
    return ["a", "b"]


@dataclass
class AppConfig:
    name: str = "service"
    tags: list[str] = field(default_factory=list)
    items: list[str] = field(default_factory=load_items)
    debug: InitVar[bool] = False
    verbose: InitVar[bool] = True

    def __post_init__(self, debug: bool, verbose: bool) -> None:
        self.debug = debug
        self.verbose = verbose


class StateManager:
    def __init__(self) -> None:
        self.handlers: list[str] = []
        self.lookup: dict[str, int] = {}

    def rank(self, key: str) -> int:
        return self.lookup.get(key, 0)
```

### Violations

1. **B019** — `@lru_cache` on `StateManager.rank`; cache retains `self` and leaks memory.
2. **RUF008** — `tags: list[str] = []`; mutable default is shared across dataclass instances.
3. **RUF009** — `items: list[str] = load_items()`; function-call default is evaluated once.
4. **RUF012** — `handlers: list[str] = []` and `lookup: dict[str, int] = {}`; mutable class attributes are shared across instances.
5. **RUF033** — `debug: bool = False` and `verbose: bool = True` in `__post_init__`; defaults do not propagate to the generated `__init__`.
