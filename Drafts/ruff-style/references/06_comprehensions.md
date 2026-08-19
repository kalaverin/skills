---
---

# Comprehensions

Prefer comprehensions and generator expressions over manual loops and wrapper calls; keep them readable and direct.

## Rule of thumb

1. Build collections with literal syntax and comprehensions; never wrap a generator or list comprehension in `list()`, `set()`, or `dict()`.
2. If a comprehension only forwards items unchanged, drop it and use `list()`, `set()`, `dict()`, or `dict.fromkeys()`.
3. Avoid empty constructor calls and literal-wrapping constructors; write `{}`, `[]`, `()`, `set()`, and direct literals instead.
4. Never double-cast or double-process an iterable with nested `list`/`set`/`tuple`/`sorted`/`reversed` calls.
5. Keep dict keys unique in a literal; repeated keys silently overwrite earlier values.
6. Replace simple accumulation loops with comprehensions, and use `extend()`/`update()` with generator expressions when adding to existing collections.

## Example: Generators and comprehensions inside constructors

A junior's data-cleaning script keeps wrapping generator expressions and list comprehensions in collection constructors.

### Bad

```python
"""Normalize sample data."""


def summarize(nums, pairs):
    squares = list(x * x for x in nums)  # C400
    seen = set(x * x for x in nums)  # C401
    lookup = dict((x, x * x) for x in nums)  # C402
    unique = set([x * x for x in nums])  # C403
    labels = dict([(k, v.upper()) for k, v in pairs])  # C404
    flat = list([x * 2 for x in nums])  # C411
    return squares, seen, lookup, unique, labels, flat
```

### Good

```python
"""Normalize sample data."""


def summarize(nums, pairs):
    squares = [x * x for x in nums]
    seen = {x * x for x in nums}
    lookup = {x: x * x for x in nums}
    unique = {x * x for x in nums}
    labels = {k: v.upper() for k, v in pairs}
    flat = [x * 2 for x in nums]
    return squares, seen, lookup, unique, labels, flat
```

### Violations

1. **C400** — `list(x * x for x in nums)`; a generator expression inside `list()` should be a list comprehension.
2. **C401** — `set(x * x for x in nums)`; a generator expression inside `set()` should be a set comprehension.
3. **C402** — `dict((x, x * x) for x in nums)`; a key-value generator inside `dict()` should be a dict comprehension.
4. **C403** — `set([x * x for x in nums])`; building a list only to pass it to `set()` is wasteful.
5. **C404** — `dict([(k, v.upper()) for k, v in pairs])`; a list of pairs inside `dict()` is a verbose dict comprehension.
6. **C411** — `list([x * 2 for x in nums])`; a list comprehension is already a list.

## Example: Literal wrappers and empty constructors

A junior writes every collection through a constructor call, even when a literal is shorter and faster.

### Bad

```python
"""Literal wrappers."""


def build_collections():
    tags = set(["a", "b", "c"])  # C405
    mapping = dict([(1, 2), (3, 4)])  # C406
    blank = dict()  # C408
    empty = list()  # C408
    zero = tuple()  # C408
    point = tuple([1, 2])  # C409
    items = list((1, 2))  # C410
    clone = dict({"a": 1})  # C418
    return tags, mapping, blank, empty, zero, point, items, clone
```

### Good

```python
"""Literal wrappers."""


def build_collections():
    tags = {"a", "b", "c"}
    mapping = {1: 2, 3: 4}
    blank = {}
    empty = []
    zero = ()
    point = (1, 2)
    items = [1, 2]
    clone = {"a": 1}
    return tags, mapping, blank, empty, zero, point, items, clone
```

### Violations

1. **C405** — `set(["a", "b", "c"])`; a list or tuple literal inside `set()` should be a set literal.
2. **C406** — `dict([(1, 2), (3, 4)])`; a list or tuple of pairs inside `dict()` should be a dict literal.
3. **C408** — `dict()`, `list()`, `tuple()`; empty collection constructor calls should be literal syntax.
4. **C409** — `tuple([1, 2])`; a list or tuple literal inside `tuple()` should be a tuple literal.
5. **C410** — `list((1, 2))`; a list or tuple literal inside `list()` should be a list literal.
6. **C418** — `dict({"a": 1})`; a dict literal inside `dict()` adds no value.

## Example: Redundant processing and identity comprehensions

A junior copies data by iterating over it explicitly and adds extra casts that do nothing.

### Bad

```python
"""Redundant processing."""


def copy_and_flag(nums, pairs, keys):
    unique_sorted = set(sorted(nums))  # C414
    as_list = list(tuple(nums))  # C414
    copy_list = [x for x in nums]  # C416
    copy_set = {x for x in nums}  # C416
    copy_dict = {k: v for k, v in pairs}  # C416
    flags = {k: None for k in keys}  # C420
    return unique_sorted, as_list, copy_list, copy_set, copy_dict, flags
```

### Good

```python
"""Redundant processing."""


def copy_and_flag(nums, pairs, keys):
    unique_sorted = set(nums)
    as_list = list(nums)
    copy_list = list(nums)
    copy_set = set(nums)
    copy_dict = dict(pairs)
    flags = dict.fromkeys(keys)
    return unique_sorted, as_list, copy_list, copy_set, copy_dict, flags
```

### Violations

1. **C414** — `set(sorted(nums))`, `list(tuple(nums))`; double-casting or double-processing an iterable repeats work without changing the result.
2. **C416** — `[x for x in nums]`, `{x for x in nums}`, `{k: v for k, v in pairs}`; identity comprehensions should be replaced with the matching constructor.
3. **C420** — `{k: None for k in keys}`; use `dict.fromkeys()` for a dict with one static value per key.

## Example: Repeated dictionary keys

A junior copies config blocks around and accidentally repeats a key.

### Bad

```python
"""Build config."""


def build_config(name, label):
    config = {
        "host": "localhost",
        "port": 8080,
        "port": 9090,  # F601
    }
    settings = {
        name: 1,
        label: 2,
        label: 3,  # F602
    }
    return config, settings
```

### Good

```python
"""Build config."""


def build_config(name, label):
    config = {
        "host": "localhost",
        "port": 9090,
    }
    settings = {
        name: 1,
        label: 3,
    }
    return config, settings
```

### Violations

1. **F601** — `"port": 9090`; repeated literal key silently overwrites the earlier value.
2. **F602** — `label: 3`; repeated variable key silently overwrites the earlier value.

## Example: Manual loops that should be comprehensions

A junior falls back to `for` loops for simple list and dict construction.

### Bad

```python
"""Manual loops."""


def build_lookup(nums, pairs):
    evens = []
    for n in nums:
        if n % 2 == 0:
            evens.append(n)  # PERF401

    copy = []
    for n in nums:
        copy.append(n)  # PERF402

    lookup = {}
    for x, y in pairs:
        if y % 2:
            lookup[x] = y  # PERF403

    return evens, copy, lookup
```

### Good

```python
"""Manual loops."""


def build_lookup(nums, pairs):
    evens = [n for n in nums if n % 2 == 0]
    copy = list(nums)
    lookup = {x: y for x, y in pairs if y % 2}
    return evens, copy, lookup
```

### Violations

1. **PERF401** — `evens.append(n)` in a filtering loop; the append loop should be a list comprehension.
2. **PERF402** — `copy.append(n)` in a copying loop; use `list()` or `list.copy()` instead.
3. **PERF403** — `lookup[x] = y` in a key-value loop; the loop should be a dict comprehension.
