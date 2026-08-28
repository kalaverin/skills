---
---

# Control flow

Keep functions flat and bounded: explicit returns, no superfluous `else`, limited branches/returns/nesting/complexity.

## Rule of thumb

1. Flatten first: guard clauses, lookup tables, and decomposition beat nested `if`/`elif` towers.
2. A branch that leaves the function (`return`/`raise`/`continue`/`break`) ends the current path — never indent the rest inside `else`.
3. Return explicitly on every path that can produce a value; bare returns are only acceptable when every path yields `None`.
4. Respect the metrics: too many arguments, locals, statements, branches, returns, nested blocks, or boolean expressions means the function is doing too much.
5. Keep control-flow statements in their proper scope: `break`/`continue`/`yield`/`return` only inside loops or functions; a bare `except:` must be the last handler.
6. Do not shadow a parameter with a loop/`try`/`with` variable; rename the inner binding.
7. Put newer Python version branches first in `sys.version_info` conditionals.

## Example: Illegal control-flow placement

A junior copy-pastes snippets into places where the control-flow keywords have no meaning.

### Bad

```python
# File: broken_flow.py

class Stream:
    yield 1  # F704


def stopper():
    break  # F701


def skipper():
    continue  # F702


class Value:
    return 1  # F706


def fragile():
    try:
        return 1 / 0
    except:  # F707
        print("catch-all")
    except ZeroDivisionError:
        print("specific")
```

### Good

```python
# File: broken_flow.py


def stream():
    yield 1


def stopper(items):
    for item in items:
        if item.done:
            break


def skipper(items):
    for item in items:
        if not item.active:
            continue


def one():
    return 1


def fragile():
    try:
        return 1 / 0
    except ZeroDivisionError:
        print("specific")
    except:
        print("catch-all")
```

### Violations

1. **F701** — `break` inside `stopper`; not inside a loop.
2. **F702** — `continue` inside `skipper`; not inside a loop.
3. **F704** — `yield 1` inside `Stream`; `yield` is only allowed inside functions.
4. **F706** — `return 1` inside `Value`; `return` is only allowed inside functions.
5. **F707** — bare `except:` before `except ZeroDivisionError`; the catch-all handler must be last.

## Example: Complexity and branching

A status resolver and a guard clause grow into long `if`/`elif` chains and boolean walls.

### Bad

```python
# File: branches.py


def resolve_status(status):  # C901,PLR0911,PLR0912
    if status == "new":
        return "queued"
    elif status == "queued":  # RET505
        return "running"
    elif status == "running":
        return "done"
    elif status == "failed":
        return "retry"
    elif status == "cancelled":
        return "closed"
    elif status == "pending":
        return "waiting"
    elif status == "archived":
        return "stored"
    elif status == "deleted":
        return "removed"
    elif status == "merged":
        return "combined"
    elif status == "split":
        return "divided"
    elif status == "locked":
        return "frozen"
    elif status == "unlocked":
        return "thawed"
    else:
        return "unknown"


def is_ready(a, b, c, d, e):  # RET503
    if a and b and c and d and e and True:  # PLR0916
        return True
```

### Good

```python
# File: branches.py


STATUS_MAP = {
    "new": "queued",
    "queued": "running",
    "running": "done",
    "failed": "retry",
    "cancelled": "closed",
    "pending": "waiting",
    "archived": "stored",
    "deleted": "removed",
    "merged": "combined",
    "split": "divided",
    "locked": "frozen",
    "unlocked": "thawed",
}


def resolve_status(status: str) -> str:
    return STATUS_MAP.get(status, "unknown")


def is_ready(parts: list[bool]) -> bool:
    return all(parts)
```

### Violations

1. **C901** — `def resolve_status(status):`; 13 branches make the control-flow graph too complex.
2. **PLR0911** — `def resolve_status(status):`; 13 return statements exceed the default limit.
3. **PLR0912** — `def resolve_status(status):`; 13 branches exceed the default limit.
4. **PLR0916** — `if a and b and c and d and e and True:`; 6 boolean expressions exceed the default limit.

## Example: Function sizing

A physics helper, a totals function, and a pipeline all ignore the size gauges.

### Bad

```python
# File: metrics.py


def calculate_position(x_pos, y_pos, z_pos, x_vel, y_vel, z_vel, time):  # PLR0913,PLR0917
    new_x = x_pos + x_vel * time
    new_y = y_pos + y_vel * time
    new_z = z_pos + z_vel * time
    return new_x, new_y, new_z


def summarize(data):  # PLR0914
    a = data.a
    b = data.b
    c = data.c
    d = data.d
    e = data.e
    f = data.f
    g = data.g
    h = data.h
    i = data.i
    j = data.j
    k = data.k
    l = data.l
    m = data.m
    n = data.n
    o = data.o
    p = data.p
    return a + b + c + d + e + f + g + h + i + j + k + l + m + n + o + p


def run_pipeline(data):  # PLR0915
    data.load()
    data.validate()
    data.clean()
    data.normalize()
    data.enrich()
    data.deduplicate()
    data.filter_active()
    data.sort()
    data.group()
    data.aggregate()
    data.compute_metrics()
    data.add_metadata()
    data.format_dates()
    data.format_numbers()
    data.convert_units()
    data.apply_rules()
    data.check_constraints()
    data.log_start()
    data.log_progress()
    data.log_end()
    data.notify()
    data.save()
    data.archive()
    data.purge()
    data.report()
    data.emit()
    data.flush()
    data.close()
    data.commit()
    data.rollback_if_needed()
    data.cleanup()
    data.release()
    data.finalize()
    data.summary()
    data.validate_output()
    data.compare()
    data.sync()
    data.publish()
    data.subscribe()
    data.broadcast()
    data.index()
    data.refresh()
    data.compact()
    data.rebuild()
    data.snapshot()
    data.restore()
    data.recheck()
    data.reindex()
    data.reformat()
    data.requeue()
    data.resync()
    data.recompute()
    data.revalidate()
    data.rearchive()
    data.reopen()
    data.reexport()
    return data
```

### Good

```python
# File: metrics.py
from typing import NamedTuple


class Vector(NamedTuple):
    x: float
    y: float
    z: float


class State(NamedTuple):
    position: Vector
    velocity: Vector


def calculate_position(state: State, time: float) -> Vector:
    return Vector(*(p + v * time for p, v in zip(state.position, state.velocity)))


def summarize(data):
    fields = "abcdefghijklmnop"
    return sum(getattr(data, name) for name in fields)


def run_pipeline(data):
    data.load()
    data.validate()
    data.process()
    return data
```

### Violations

1. **PLR0913** — `def calculate_position(x_pos, y_pos, z_pos, x_vel, y_vel, z_vel, time):`; 7 arguments exceed the default limit.
2. **PLR0914** — `def summarize(data):`; 16 local variables exceed the default limit.
3. **PLR0915** — `def run_pipeline(data):`; 58 statements exceed the default limit.
4. **PLR0917** — `def calculate_position(x_pos, y_pos, z_pos, x_vel, y_vel, z_vel, time):`; 7 positional arguments exceed the default limit.

## Example: Control-flow flattening

A cell finder, a parameter shadow, a sign check, and several redundant `else` blocks all add unnecessary indentation.

### Bad

```python
# File: flattening.py


def find_cell(rows, target):
    for row in rows:  # PLR1702
        if row.active:
            for cell in row.cells:
                if cell.visible:
                    if cell.value is not None:
                        if cell.value == target:
                            return cell
    return None


def show(host_id=10.11):
    for host_id, host in [[12.13, "Venus"], [14.15, "Mars"]]:  # PLR1704
        print(host_id, host)


def check_sign(value):
    if value > 0:
        print("positive")
    else:  # PLR5501
        if value < 0:
            print("negative")
        else:
            print("zero")


def pick_positive(value, fallback):
    if value > 0:
        return value
    else:  # RET505
        return fallback


def require_active(is_active, reason):
    if not is_active:
        raise RuntimeError(reason)
    else:  # RET506
        raise RuntimeError("already active")


def skip_small(values, threshold):
    for value in values:
        if value < threshold:
            continue
        else:  # RET507
            print(value)


def stop_at_large(values, threshold):
    for value in values:
        if value > threshold:
            break
        else:  # RET508
            print(value)
```

### Good

```python
# File: flattening.py


def find_cell(rows, target):
    for row in rows:
        if not row.active:
            continue
        for cell in row.cells:
            if not cell.visible:
                continue
            if cell.value is not None and cell.value == target:
                return cell
    return None


def show(host_id=10.11):
    for inner_host_id, host in [[12.13, "Venus"], [14.15, "Mars"]]:
        print(host_id, inner_host_id, host)


def check_sign(value):
    if value > 0:
        print("positive")
    elif value < 0:
        print("negative")
    else:
        print("zero")


def pick_positive(value, fallback):
    if value > 0:
        return value
    return fallback


def require_active(is_active, reason):
    if not is_active:
        raise RuntimeError(reason)
    raise RuntimeError("already active")


def skip_small(values, threshold):
    for value in values:
        if value < threshold:
            continue
        print(value)


def stop_at_large(values, threshold):
    for value in values:
        if value > threshold:
            break
        print(value)
```

### Violations

1. **PLR1702** — `def find_cell(rows, target):`; six nested blocks exceed the default limit.
2. **PLR1704** — `for host_id, host in ...`; the loop variable shadows the `host_id` parameter.
3. **PLR5501** — `else:` in `check_sign`; an `else` containing only an `if` should be `elif`.
4. **RET505** — `else:` in `pick_positive`; the `if` branch returns, so the `else` is dead indentation.
5. **RET506** — `else:` in `require_active`; the `if` branch raises, so the `else` is dead indentation.
6. **RET507** — `else:` in `skip_small`; the `if` branch continues, so the `else` is dead indentation.
7. **RET508** — `else:` in `stop_at_large`; the `if` branch breaks, so the `else` is dead indentation.

## Example: Return discipline

Several helpers confuse explicit, implicit, and useless returns.

### Bad

```python
# File: returns.py


def show(event):
    print(event)
    return None  # PLR1711,RET501


def baz(bar):
    if not bar:
        return  # RET502
    return 1


def foo(bar):  # RET503
    if not bar:
        return 1


def answer():
    value = 42
    return value  # RET504
```

### Good

```python
# File: returns.py


def show(event):
    print(event)


def baz(bar):
    if not bar:
        return None
    return 1


def foo(bar):
    if not bar:
        return 1
    return None


def answer():
    return 42
```

### Violations

1. **PLR1711** — `return None` in `show`; useless explicit `None` at the end of a function with no other returns.
2. **RET501** — `return None` in `show`; explicit `None` is redundant when every path returns `None`.
3. **RET502** — `return` in `baz`; bare return in a function that can return non-`None` elsewhere.
4. **RET503** — `def foo(bar):`; missing explicit return at the end of a function that can return a non-`None` value.
5. **RET504** — `return value` after `value = 42`; unnecessary assignment before return.

## Example: Stub version branches

A compatibility stub puts the older Python branch first.

### Bad

```python
# File: _compat.pyi

import sys

if sys.version_info < (3, 10):  # PYI066
    def read_data(x, *, preserve_order=True): ...

else:
    def read_data(x): ...
```

### Good

```python
# File: _compat.pyi

import sys

if sys.version_info >= (3, 10):
    def read_data(x): ...

else:
    def read_data(x, *, preserve_order=True): ...
```

### Violations

1. **PYI066** — `if sys.version_info < (3, 10):`; the older Python branch comes before the newer branch.
