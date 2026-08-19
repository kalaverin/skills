---
---

# Iterators

Idiomatic iteration: `zip` with `strict=`, `enumerate` over manual counters, itertools over hand-rolled loops, and never mutating a collection while iterating it.

## Rule of thumb

1. Keep loop variables hygienic: distinct names per nested loop, a `_` prefix for intentionally unused targets, never rebind the name of the collection being iterated, and bind closures to loop values with default arguments.
2. Reach for the builtin before writing a loop: `enumerate` over manual counters, `any`/`all` over hand-rolled search loops, `min`/`max` over `sorted(...)[0]`, `next(iter(...))` over materializing for one element, `.items()`/`.values()` over re-indexing a dict by key.
3. Give every multi-iterable `zip`, `map`, and `itertools.batched` an explicit `strict=`: `strict=True` by default, `strict=False` only when ragged input is intentional.
4. Never mutate the collection being iterated: iterate a copy, rebuild with a comprehension, or collect changes and apply them after the loop — and batch updates (`extend`, `set.update`, `writelines`) instead of per-element loops.
5. Stay lazy: no `list()` cast before a `for` loop, generator expressions inside `any`/`all`/`sum`, stream file objects line by line, flatten with a double comprehension rather than `sum(lists, [])`.
6. Generator discipline: inside a generator use only `yield`, `yield from`, or bare `return` — never `return value`, never `raise StopIteration` — and materialize `groupby` groups with `list()` before reusing them.
7. In stub files, promise protocols, not mechanisms: `__iter__` returns `Iterator`, tuples are `typing.NamedTuple` classes, and `collections.abc.Set` is imported `as AbstractSet`.

## Example: Loop-variable hygiene

A scoreboard printer that leaks, clobbers, and mis-captures its loop variables at every step.

### Bad

```python
"""Game scoreboard helpers."""

matches = [("Ada", "Linus"), ("Grace", "Guido")]
players = ["ada", "grace", "guido", "linus"]

for winner, loser in matches:  # B007
    print(f"Winner: {winner}")

position = 0
for player in players:
    print(f"{position + 1}. {player}")
    position += 1  # SIM113

for index, _ in enumerate(matches):  # FURB148
    print(f"Match {index}")

for player in players:
    for player in matches:  # PLW2901
        print(player)
    print(player)

callbacks = [lambda: print(player) for player in players]  # B023

for players in players:  # B020
    print(players.title())
```

### Good

```python
"""Game scoreboard helpers."""

matches = [("Ada", "Linus"), ("Grace", "Guido")]
players = ["ada", "grace", "guido", "linus"]

for winner, _loser in matches:
    print(f"Winner: {winner}")

for position, player in enumerate(players):
    print(f"{position + 1}. {player}")

for index in range(len(matches)):
    print(f"Match {index}")

for player in players:
    for match in matches:
        print(match)
    print(player)

callbacks = [lambda player=player: print(player) for player in players]

for player in players:
    print(player.title())
```

### Violations

1. **B007** — `for winner, loser in matches`; `loser` is never read in the loop body, so prefix it with `_` or drop it.
2. **B020** — `for players in players`; the loop target rebinds the iterated collection itself, so after the loop `players` holds the last element.
3. **B023** — `lambda: print(player) for player in players`; the closure captures the variable, not its value — every lambda sees the last iteration's `player`.
4. **FURB148** — `for index, _ in enumerate(matches)`; the value half is discarded, so `range(len(matches))` states the intent directly.
5. **PLW2901** — inner `for player in matches`; loops have no own scope, so the nested target clobbers the outer loop variable for the rest of the block.
6. **SIM113** — `position` counter beside `for player in players`; a manually initialized and incremented counter is `enumerate` spelled the long way.

## Example: Strict multi-iterable pairing

**Target:** `py314`

A feed merger that pairs, batches, and starmaps two sensor streams without ever declaring what happens on length mismatch.

### Bad

```python
"""Merge sensor feeds."""

import itertools
from itertools import starmap

names = ["alpha", "beta", "gamma"]
values = [1.5, 2.0, 3.5]


def format_pair(name, value):
    return f"{name}={value}"


pairs = list(zip(names, values))  # B905
labels = list(map(format_pair, names, values))  # B912
again = list(starmap(format_pair, zip(names, values)))  # B905,RUF058
neighbor_diffs = [b - a for a, b in zip(values, values[1:])]  # B905,RUF007

for batch in itertools.batched(names, 2):  # B911
    print(batch)

all_valid = all(format_pair(a, b) for a, b in pairs)  # FURB140
```

### Good

```python
"""Merge sensor feeds."""

from itertools import batched, pairwise, starmap

names = ["alpha", "beta", "gamma"]
values = [1.5, 2.0, 3.5]


def format_pair(name, value):
    return f"{name}={value}"


pairs = list(zip(names, values, strict=True))
labels = list(map(format_pair, names, values, strict=True))
again = list(map(format_pair, names, values, strict=True))
neighbor_diffs = [b - a for a, b in pairwise(values)]

for batch in batched(names, 2, strict=True):
    print(batch)

all_valid = all(starmap(format_pair, pairs))
```

### Violations

1. **B905** — `zip(names, values)` (three call sites, including inside `starmap` and the slice form); bare `zip` silently truncates to the shortest input without `strict=`.
2. **B911** — `itertools.batched(names, 2)`; when the input length is not divisible by `n`, the final batch is silently short without `strict=` (3.13+).
3. **B912** — `map(format_pair, names, values)`; multi-iterable `map` truncates to the shortest input exactly like `zip` without `strict=` (3.14+).
4. **FURB140** — `all(format_pair(a, b) for a, b in pairs)`; a comprehension that only unpacks each tuple straight into a call is `itertools.starmap`'s job.
5. **RUF007** — `zip(values, values[1:])`; iterating successive overlapping pairs is what `itertools.pairwise` names directly.
6. **RUF058** — `starmap(format_pair, zip(names, values))`; zipping iterables only for `starmap` to unpack them again is a round trip — `map` takes the iterables directly.

## Example: Safe mutation and batch updates

A cache pruner that edits collections mid-loop and drips every update one element at a time.

### Bad

```python
"""Prune stale cache entries and write a report."""

from pathlib import Path

entries = ["a.tmp", "b.tmp", "keep.txt"]
seen = {"a.tmp", "b.tmp"}

for entry in entries:
    if entry.endswith(".tmp"):
        entries.remove(entry)  # B909

for entry in seen:  # FURB142,PLE4703
    seen.add(entry.upper())  # B909

cleaned = []
cleaned.append("alpha")  # FURB113
cleaned.append("beta")
cleaned.append("gamma")

keep = set()
for entry in entries:  # FURB142
    keep.add(entry)

with Path("report.txt").open("w") as f:
    for name in cleaned:  # FURB122
        f.write(name + "\n")

with Path("report.txt").open() as f:
    for line in f.readlines():  # FURB129
        print(line.strip())
```

### Good

```python
"""Prune stale cache entries and write a report."""

from pathlib import Path

entries = ["a.tmp", "b.tmp", "keep.txt"]
seen = {"a.tmp", "b.tmp"}

entries = [entry for entry in entries if not entry.endswith(".tmp")]

seen.update({entry.upper() for entry in seen})

cleaned = []
cleaned.extend(("alpha", "beta", "gamma"))

keep = set()
keep.update(entries)

report_path = Path("report.txt")
with report_path.open("w") as f:
    f.writelines(f"{entry}\n" for entry in cleaned)

with report_path.open() as f:
    for line in f:
        print(line.strip())
```

### Violations

1. **B909** — `entries.remove(entry)` and `seen.add(entry.upper())`; mutating the iterated collection corrupts the iteration cursor — deletes skip elements, appends can loop forever.
2. **FURB113** — `cleaned.append("alpha")` (and the two appends that follow); consecutive appends resize the list once per element — one `extend` resizes once.
3. **FURB122** — `f.write(name + "\n")` in a for loop; a loop of bare `write` calls is `writelines` spelled out, and `writelines` accepts any iterable.
4. **FURB129** — `for line in f.readlines()`; `readlines()` eagerly loads the whole file — the file object is already a line iterator.
5. **FURB142** — the `seen.add(...)` and `keep.add(entry)` loops; a loop whose body is only `set.add` is `set.update` spelled the long way.
6. **PLE4703** — `seen.add(entry.upper())`; mutating a set during iteration raises `RuntimeError: Set changed size during iteration` — iterate a copy.

## Example: Dict iteration and ordering ceremony

An inventory report that re-indexes dicts by key, copies collections for nothing, and decorates a loop with a dead `else`.

### Bad

```python
"""Warehouse inventory report."""

inventory = {"bolts": 120, "nuts": 240}
prices = {"bolts": 0.05, "nuts": 0.02}

total = 0.0
for item in inventory:  # PLC0206
    total += inventory[item] * prices[item]

for _item, count in inventory.items():  # PERF102
    print(count)

for item, count in prices:  # PLE1141
    print(f"{item}: {count}")

ordered = list(sorted(inventory))  # C413
descending = reversed(sorted(prices))  # C413
shuffled = set(ordered[::-1])  # C415

names = ("bolts", "nuts")
for name in list(names):  # PERF101
    print(name)
else:  # PLW0120
    print("done")

stock = [1, 2, 3]
stock = list(reversed(stock))  # FURB187
```

### Good

```python
"""Warehouse inventory report."""

inventory = {"bolts": 120, "nuts": 240}
prices = {"bolts": 0.05, "nuts": 0.02}

total = 0.0
for item, count in inventory.items():
    total += count * prices[item]

for count in inventory.values():
    print(count)

for item, price in prices.items():
    print(f"{item}: {price}")

ordered = sorted(inventory)
descending = sorted(prices, reverse=True)
shuffled = set(ordered)

names = ("bolts", "nuts")
for name in names:
    print(name)
print("done")

stock = [1, 2, 3]
stock.reverse()
```

### Violations

1. **C413** — `list(sorted(inventory))` and `reversed(sorted(prices))`; `sorted` already returns a list, and `reverse=True` is a stable reverse sort instead of a wrapped `reversed`.
2. **C415** — `set(ordered[::-1])`; pre-reversing the input is pointless when the consumer re-orders the elements anyway.
3. **FURB187** — `stock = list(reversed(stock))`; rebinding a name to a reversed copy of itself means the original was disposable — reverse in place with `.reverse()`.
4. **PERF101** — `for name in list(names)`; casting a loop iterable to `list` eagerly copies a collection the loop would have iterated anyway.
5. **PERF102** — `for _item, count in inventory.items()`; unpacking `.items()` and discarding the key allocates a tuple per entry for nothing — use `.values()`.
6. **PLC0206** — `inventory[item]` inside `for item in inventory`; iterating keys and re-indexing does two hash lookups per entry — `.items()` fetches both in one pass.
7. **PLE1141** — `for item, count in prices`; unpacking a bare dict iterates keys, so key-and-value pairs only come from `.items()`.
8. **PLW0120** — `else:` on a loop with no `break`; the `else` always runs, so it is decoration that sends readers hunting for a nonexistent `break`.

## Example: Loops that are builtins in disguise

**Target:** `py310`

A reading validator that hand-rolls `any`, sorts to find one extreme, and catches per-element exceptions in a loop (PERF203 fires only below 3.11).

### Bad

```python
"""Validate sensor readings."""

readings = [0.4, 0.9, 1.7, 0.2]


def has_spike(values):
    for value in values:  # SIM110
        if value > 1.5:
            return True
    return False


doubled = list(map(lambda value: value * 2, readings))  # C417
ok = all([value > 0 for value in readings])  # C419
total = sum([value for value in readings])  # C419
lowest = sorted(readings)[0]  # FURB192
highest = sorted(readings, reverse=True)[0]  # FURB192
first = list(readings)[0]  # RUF015
flat = sum([[1, 2], [3, 4]], [])  # RUF017
floor = min(0.0, min(0.5, 0.1))  # PLW3301
third = [0, 1, 2][3]  # PLE0643

parsed = []
for raw in ["1", "2", "x"]:
    try:
        parsed.append(int(raw))
    except ValueError:  # PERF203
        continue
```

### Good

```python
"""Validate sensor readings."""

readings = [0.4, 0.9, 1.7, 0.2]


def has_spike(values):
    return any(value > 1.5 for value in values)


doubled = [value * 2 for value in readings]
ok = all(value > 0 for value in readings)
total = sum(readings)
lowest = min(readings)
highest = max(readings)
first = next(iter(readings))
flat = [item for pair in [[1, 2], [3, 4]] for item in pair]
floor = min(0.0, 0.5, 0.1)
third = [0, 1, 2][2]

parsed = []
for raw in ["1", "2", "x"]:
    if raw.isdigit():
        parsed.append(int(raw))
```

### Violations

1. **C417** — `map(lambda value: value * 2, readings)`; `map` with a lambda pays Python-level call overhead per element — a comprehension is faster and clearer.
2. **C419** — `all([value > 0 for value in readings])` and `sum([value for value in readings])`; a comprehension inside `all`/`sum` builds a full temporary list and kills short-circuiting.
3. **FURB192** — `sorted(readings)[0]` and `sorted(readings, reverse=True)[0]`; sorting the whole sequence O(n log n) to read one extreme where `min`/`max` are O(n).
4. **PERF203** — `try:` inside the parsing loop; per-iteration `try` setup costs time — look before you leap (`isdigit`, `in`, `.get()`) or hoist the `try` around the loop.
5. **PLE0643** — `[0, 1, 2][3]`; with a static literal and a static index, an out-of-bounds access is a certain `IndexError` — a plain bug.
6. **PLW3301** — `min(0.0, min(0.5, 0.1))`; `min`/`max` are variadic — nesting them is noise.
7. **RUF015** — `list(readings)[0]`; materializing the entire collection to read element zero is O(n) time and memory for an O(1) job.
8. **RUF017** — `sum([[1, 2], [3, 4]], [])`; `sum` with a list start copies the growing accumulator on every `+` — flattening goes quadratic.
9. **SIM110** — the `has_spike` loop; a loop that only returns `True` on first hit and `False` at the end is `any`, with the same short-circuit semantics.

## Example: Generator discipline

A log scanner whose generators swallow return values, crash on `StopIteration`, and reuse one-shot `groupby` groups.

### Bad

```python
"""Scan log files for errors."""

import itertools
from pathlib import Path


def iter_paths(root, patterns=None):
    dir_path = Path(root)
    if patterns is None:
        return dir_path.glob("*.log")  # B901
    for pattern in patterns:
        yield from dir_path.glob(pattern)


def read_lines(paths):
    for path in paths:
        with path.open() as f:
            for line in f:  # UP028
                yield line


def first_n(paths, n):
    count = 0
    for path in paths:
        if count >= n:
            raise StopIteration  # PLR1708
        count += 1  # SIM113
        yield path


def marker():
    token = "EOF"
    yield token  # RUF070


records = ["a=1", "a=2", "b=3"]
for _key, group in itertools.groupby(records, key=lambda r: r.split("=")[0]):
    for _ in range(2):
        print(list(group))  # B031
```

### Good

```python
"""Scan log files for errors."""

import itertools
from pathlib import Path


def iter_paths(root, patterns=None):
    dir_path = Path(root)
    if patterns is None:
        yield from dir_path.glob("*.log")
    else:
        for pattern in patterns:
            yield from dir_path.glob(pattern)


def read_lines(paths):
    for path in paths:
        with path.open() as f:
            yield from f


def first_n(paths, n):
    for count, path in enumerate(paths):
        if count >= n:
            return
        yield path


def marker():
    yield "EOF"


records = ["a=1", "a=2", "b=3"]
for _key, group in itertools.groupby(records, key=lambda r: r.split("=")[0]):
    values = list(group)
    for _ in range(2):
        print(values)
```

### Violations

1. **B031** — `print(list(group))` inside the nested loop over a `groupby` group; each group is a one-shot iterator chained to the stream — materialize with `list(group)` before reuse.
2. **B901** — `return dir_path.glob("*.log")`; `return value` in a generator stuffs the value into `StopIteration`, so `list(iter_paths(root))` comes back empty.
3. **PLR1708** — `raise StopIteration`; since PEP 479 this is converted to `RuntimeError` at runtime — bare `return` is the only correct early exit.
4. **RUF070** — `token = "EOF"` immediately before `yield token`; a name assigned solely to be yielded on the next line is dead ceremony.
5. **UP028** — `for line in f:` whose body is only `yield line`; manual delegation — `yield from` is shorter and forwards `send`/`throw`/`close` correctly.

## Example: Generated protocol decoder

A machine-generated decoder module with a double-starred target and dispatch spelled as control flow.

### Bad

```python
"""Generated protocol decoder (do not edit)."""

from typing import NamedTuple

Header = NamedTuple("Header", [("msg_type", int), ("length", int)])  # UP014

MAGIC = "PING".encode("utf-8")  # UP012

TYPE_FIELD = "type"
LENGTH_FIELD = "length"


def describe(msg_type):
    if msg_type == 1:  # SIM116
        return "ping"
    elif msg_type == 2:
        return "pong"
    elif msg_type == 3:
        return "ack"
    else:
        return "unknown"


def is_numeric(field):
    return isinstance(field, int) or isinstance(field, float)  # SIM101


def is_control(field):
    return field == TYPE_FIELD or field == LENGTH_FIELD  # SIM109


payload = b"PING\x01\x00"
*head, *middle, last = payload  # F622
```

### Good

```python
"""Generated protocol decoder (do not edit)."""

from typing import NamedTuple


class Header(NamedTuple):
    msg_type: int
    length: int


MAGIC = b"PING"

TYPE_FIELD = "type"
LENGTH_FIELD = "length"

DESCRIPTIONS = {1: "ping", 2: "pong", 3: "ack"}


def describe(msg_type):
    return DESCRIPTIONS.get(msg_type, "unknown")


def is_numeric(field):
    return isinstance(field, (int, float))


def is_control(field):
    return field in (TYPE_FIELD, LENGTH_FIELD)


payload = b"PING\x01\x00"
head, *rest, last = payload
```

### Violations

1. **F622** — `*head, *middle, last = payload`; with two starred targets the interpreter cannot decide which absorbs the middle — a `SyntaxError`, one starred target per assignment.
2. **SIM101** — `isinstance(field, int) or isinstance(field, float)`; `isinstance` accepts a tuple of types, so repeated calls on one target merge into one.
3. **SIM109** — `field == TYPE_FIELD or field == LENGTH_FIELD`; chained `==` against the same operand is an `in` test against a tuple of candidates.
4. **SIM116** — the `if`/`elif` chain in `describe`; three or more branches that only map a value to a result are a dict plus `.get(key, default)`.
5. **UP012** — `"PING".encode("utf-8")`; for a literal, a `b"..."` literal writes at compile time what `.encode()` builds at runtime.
6. **UP014** — `Header = NamedTuple("Header", ...)`; the functional spelling exists for backwards compatibility — the class form gives the type a real name and real field annotations.

## Example: Stub iterator contracts

A stub file that promises the wrong protocols: mechanism types in `__iter__`, an ambiguous `Set`, and an untyped namedtuple factory.

### Bad

```python
# File: warehouse/models.pyi
import collections.abc
from collections import namedtuple
from collections.abc import Generator, Set  # PYI025

Point = namedtuple("Point", ["x", "y"])  # PYI024


class Deck:
    def __iter__(self) -> collections.abc.Iterable[str]: ...  # PYI045


class Cards:
    def __iter__(self) -> Generator[str, None, None]:  # PYI058
        yield from "abcdefg"
```

### Good

```python
# File: warehouse/models.pyi
import collections.abc
from collections.abc import Iterator
from collections.abc import Set as AbstractSet
from typing import NamedTuple


class Point(NamedTuple):
    x: float
    y: float


class Deck:
    def __iter__(self) -> collections.abc.Iterator[str]: ...


class Cards:
    def __iter__(self) -> Iterator[str]:
        yield from "abcdefg"
```

### Violations

1. **PYI024** — `Point = namedtuple("Point", ["x", "y"])`; in stubs `collections.namedtuple` gives checkers no field types — the `typing.NamedTuple` class form is the only spelling that type-checks precisely.
2. **PYI025** — `from collections.abc import Set`; the ABC is not the `set` builtin, so a bare import leaves every later annotation ambiguous — import it `as AbstractSet`.
3. **PYI045** — `__iter__` returning `collections.abc.Iterable[str]`; the contract of `__iter__` is to return something with `__next__` — an `Iterator`, not merely an `Iterable`.
4. **PYI058** — `__iter__` annotated `Generator[str, None, None]`; that the method is implemented as a generator is an implementation detail — the annotation should promise `Iterator`.
