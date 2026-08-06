---
---

# Simplification

Delete dead statements, fold tautologies and double negations, collapse verbose conditionals into single expressions, and let literals, builtins, and membership tests do the talking.

## Rule of thumb

1. Make every statement do something: assign the result, return it, assert it, or delete the line.
2. Say negations directly: `!=` instead of `not ==`, `==` instead of `not !=`, the bare expression instead of `not (not x)`.
3. Write the result of what never varies: constant comparisons, `x and not x`, `x or True`, and identical ternary arms all fold to a literal or a shorter expression.
4. Select values with expressions, not branches: ternary for two-way assignment, `or` for fallback, `min`/`max` for clamping, `bool()`/`not` for boolean arms, `return cond` for predicates.
5. Never write the same test twice: collapse nested `if` with `and`, merge identical arms with `or`, turn equality chains into `in {...}`, pass one tuple to `startswith`, chain ranges as `a < b < c`.
6. Use the native spelling: literals instead of constructors, builtins instead of wrapper lambdas, operators instead of dunder calls, `range(n)`, `x += 1`, tuple-unpacking swaps, plain keywords instead of `**{...}`.
7. Keep names and constants honest: `_`-prefix only what is truly unused, name magic values as module constants, test NaN with `math.isnan`, and put the variable left of the comparison.

## Example: Dead statements and placeholders

A half-finished job-processing module: leftover scaffolding, discarded expressions, and asserts that cannot fail.

### Bad

```python
import sys

if sys.version_info >= (3, 11):  # RUF050
    pass


def audit_job(job, limit):
    """Check the job against its retry limit."""
    pass  # PIE790


def sync_job(job, cache):
    if job.dirty:
        cache.save(job)
    else:  # RUF047
        pass

    job.retries = 3
    job.retries  # B018
    job.retries == cache.limit  # B015
    retries = job.retries
    if retries == retries:  # PLR0124
        cache.promote(job)

    verbose = 1 < 2  # PLR0133
    assert "job is always valid"  # PLW0129
    (level := 42)  # PLW0131
    return verbose, level
```

### Good

```python
def audit_job(job, limit):
    """Check the job against its retry limit."""
    return job.retries <= limit


def sync_job(job, cache):
    if job.dirty:
        cache.save(job)

    job.retries = 3
    if job.retries == cache.limit:
        cache.promote(job)

    verbose = True
    level = 42
    assert job.is_valid, "job must be valid"
    return verbose, level
```

### Violations

1. **B015** — `job.retries == cache.limit`; the comparison is computed and discarded — `assert` it, return it, or delete it.
2. **B018** — `job.retries`; an attribute-access statement with no effect.
3. **PIE790** — `pass` after the docstring in `audit_job`; a placeholder is redundant once the block has any content.
4. **PLR0124** — `job.retries == job.retries`; a name compared with itself is always true (or a disguised NaN check).
5. **PLR0133** — `verbose = 1 < 2`; two constants always resolve the same way — write the result literal.
6. **PLW0129** — `assert "job is always valid"`; a non-empty string is always truthy, so the assert can never fail.
7. **PLW0131** — `(level := 42)`; a bare walrus statement is a plain assignment in costume — use `=`.
8. **RUF047** — `else: pass`; an empty `else` clause adds a branch readers must parse for zero behavior.
9. **RUF050** — `if sys.version_info >= (3, 11): pass`; an empty `if` skeleton left behind by stripped conditional imports.

## Example: Assignments that lie

A badge builder whose bindings contradict themselves: self-assignments, double-bound targets, "unused" names that are read, and constructors spelled the long way.

### Bad

```python
def build_badge(pair, scores):
    kind = type(1)  # UP003
    label = str("raw")  # UP018
    factor = float(1.0)  # UP018

    first, second, first = pair  # PLW0128,RUF059
    winner, loser = scores  # RUF059
    label = label  # PLW0127

    _bonus = 10  # RUF052
    total = winner + _bonus
    if total:
        total = -total
    return kind, label, factor, first, second, total  # RUF054
```

### Good

```python
def build_badge(pair, scores):
    kind = int
    label = "raw"
    factor = 1.0

    first, second, _ = pair
    winner, _ = scores

    bonus = 10
    total = winner + bonus
    if total:
        total = -total
    return kind, label, factor, first, second, total
```

### Violations

1. **PLW0127** — `label = label`; self-assignment is a no-op, almost always a copy-paste slip.
2. **PLW0128** — `first, second, first = pair`; `first` is bound twice in one statement and the first binding is silently lost.
3. **RUF052** — `total = winner + _bonus`; `_bonus` is named as intentionally unused but is read — give it a real name.
4. **RUF054** — the form feed (`\f`) inside the indent before `total = -total`; a form feed after spaces has an undefined effect on indentation counting.
5. **RUF059** — `winner, loser = scores`; `loser` is unpacked but never read — prefix intentionally-unused targets with `_`.
6. **UP003** — `kind = type(1)`; the type of a literal is known at write time — name `int` directly.
7. **UP018** — `str("raw")`, `float(1.0)`; calling a builtin on a literal of its own type returns an equal value — write the literal.

## Example: Boolean algebra

An access-control decider that stacks `not` over operators and chains constants into conditions the interpreter has already resolved.

### Bad

```python
def decide_access(user, cached, token, retries):
    allowed = not (not user.is_active)  # SIM208
    if not user.role == "admin":  # SIM201
        reject(user)
    if not user.role != "guest":  # SIM202
        grant(user)

    active = user.is_active
    if active and not active:  # SIM220
        sync(user)
    if cached or not cached:  # SIM221
        render(user)

    if retries or [1] or token:  # SIM222
        proceed()
    if retries and [] and token:  # SIM223
        audit()

    mode = user.is_active or cached and token  # RUF021
    return allowed, mode
```

### Good

```python
def decide_access(user, cached, token, retries):
    allowed = user.is_active
    if user.role != "admin":
        reject(user)
    if user.role == "guest":
        grant(user)

    render(user)  # `cached or not cached` was always true.
    proceed()  # `retries or [1] or token` was always true.

    mode = user.is_active or (cached and token)
    return allowed, mode
```

### Violations

1. **RUF021** — `user.is_active or cached and token`; mixed `and`/`or` without parentheses makes precedence a guessing game.
2. **SIM201** — `not user.role == "admin"`; negated `==` states non-equality the long way — use `!=`.
3. **SIM202** — `not user.role != "guest"`; `not !=` is a double negation — use `==`.
4. **SIM208** — `not (not user.is_active)`; two `not`s cancel out.
5. **SIM220** — `user.is_active and not user.is_active`; always false, so the branch is dead code.
6. **SIM221** — `cached or not cached`; always true, so the condition guards nothing.
7. **SIM222** — `retries or [1] or token`; `or` with a truthy constant short-circuits — the whole condition is constant.
8. **SIM223** — `retries and [] and token`; `and` with a falsey constant short-circuits — the branch never runs.

## Example: Value-selecting conditionals

A scoring module that spends four-line blocks picking one of two values and returns `True`/`False` from predicates.

### Bad

```python
def pick_label(plan, handle):
    if plan:  # SIM108
        label = plan
    else:
        label = "free"

    nickname = handle if handle else "anon"  # FURB110
    return label, nickname


def best_score(left, right):
    a, b = 4, 9
    best = a if a > b else b  # FURB136
    worst = b if not a else a  # SIM212
    flag = a > 0
    chosen = a if flag else a  # RUF034
    return best, worst, chosen


def flags(token):
    allowed = True if token else False  # SIM210
    blocked = False if token else True  # SIM211
    return allowed, blocked


def notify(code):
    if code == 1:  # SIM114
        ping()
    elif code == 2:  # PLR2004
        ping()


def evaluate(usage, cap, score):
    if usage < cap:  # SIM102
        if score > 0:
            track(usage)

    highest = 0
    if score > highest:  # PLR1730
        highest = score

    if usage > 0:  # SIM103
        return True
    return False
```

### Good

```python
def pick_label(plan, handle):
    label = plan or "free"
    nickname = handle or "anon"
    return label, nickname


def best_score(left, right):
    a, b = 4, 9
    best = max(a, b)
    worst = a or b
    chosen = a
    return best, worst, chosen


def flags(token):
    allowed = bool(token)
    blocked = not token
    return allowed, blocked


def notify(code):
    if code in {1, 2}:
        ping()


def evaluate(usage, cap, score):
    if usage < cap and score > 0:
        track(usage)

    highest = max(0, score)
    return usage > 0, highest
```

### Violations

1. **FURB110** — `handle if handle else "anon"`; the ternary repeats the condition to spell what `or` means.
2. **FURB136** — `a if a > b else b`; picking the greater of two values is precisely `max(a, b)`.
3. **PLR1730** — `if score > highest: highest = score`; statement-form clamping where `max(highest, score)` is one expression.
4. **RUF034** — `a if flag else a`; both arms produce the same value, so the condition is decorative.
5. **SIM102** — `if usage < cap:` wrapping only `if score > 0:`; a nested `if` with no `else` is an `and` wearing indentation.
6. **SIM103** — `if usage > 0: return True` / `return False`; return the condition directly.
7. **SIM108** — `if plan: label = plan else: label = "free"`; both branches assign the same target — that is a ternary.
8. **SIM114** — `if code == 1: ... elif code == 2:` with identical bodies; one action for several conditions — merge with `or` (or `in {...}`).
9. **SIM210** — `True if token else False`; "true if truthy" is the definition of `bool()`.
10. **SIM211** — `False if token else True`; "false if truthy" is `not` spelled out.
11. **SIM212** — `b if not a else a`; a ternary keyed on `not a` flips the condition and swaps the arms mentally — test the positive condition (here further reducible to `a or b`).

## Example: Comparisons and membership

A request router that or-chains equality, scans list literals, splits range checks, sprinkles magic numbers, and compares against NaN.

### Bad

```python
def route(status, http_code, a, b, c, latency_ms, ratio):
    if status == "ok" or status == "fine" or status == "good":  # PLR1714
        accept()
    if http_code in [200, 201, 204]:  # PLR6201
        accept()
    if a < b and b < c:  # PLR1716
        ordered()
    if latency_ms > 200:  # PLR2004
        boost()
    if "fast" == status:  # SIM300
        prioritize()
    if ratio == float("NaN"):  # PLW0177
        reset()
```

### Good

```python
import math

MAX_LATENCY_MS = 200


def route(status, http_code, a, b, c, latency_ms, ratio):
    if status in {"ok", "fine", "good"}:
        accept()
    if http_code in {200, 201, 204}:
        accept()
    if a < b < c:
        ordered()
    if latency_ms > MAX_LATENCY_MS:
        boost()
    if status == "fast":
        prioritize()
    if math.isnan(ratio):
        reset()
```

### Violations

1. **PLR1714** — `status == "ok" or status == "fine" or status == "good"`; repeated equality against one name is a membership test — use `in {...}`.
2. **PLR1716** — `a < b and b < c`; Python chains comparisons natively — write `a < b < c`.
3. **PLR2004** — `latency_ms > 200`; a bare number in a comparison forces readers to reverse-engineer its meaning — name it as a constant.
4. **PLR6201** — `http_code in [200, 201, 204]`; membership against a list literal scans linearly — a set literal is constant-time.
5. **PLW0177** — `ratio == float("NaN")`; NaN equals nothing, including itself, so the check never fires — use `math.isnan`.
6. **SIM300** — `"fast" == status`; Yoda conditions buy nothing in Python — subject left, constant right.

## Example: Redundant idioms

A report builder that re-implements what the language spells natively: wrapper lambdas, re-indexed loops, temp-variable swaps, dunder calls, and dict-splat kwargs.

### Bad

```python
from dataclasses import dataclass, field


@dataclass
class Config:
    tags: list[str] = field(default_factory=lambda: [])  # PIE807


def build_report(client, rows, fruits, letters, directions, limit):
    total = 0
    total = total + len(rows)  # PLR6104

    for i in range(0, len(rows)):  # PIE808
        render(rows[i])

    for name, count in fruits.items():
        print(fruits[name])  # PLR1733

    for index, letter in enumerate(letters):
        print(letters[index])  # PLR1736

    options = {"A": 1, "B": 2}
    merged = {**options, **{"C": 3}}  # PIE800

    client.send(mode="sync", *rows)  # B026
    client.configure(**{"retries": 3})  # PIE804

    name = client.name
    if name.startswith("acme") or name.startswith("foo"):  # PIE810
        greet()

    if total.__gt__(limit):  # PLC2801
        celebrate()

    cell = directions[(0, 1)]  # RUF031

    x, y = 1, 2
    if x > y:
        temp = x  # PLR1712
        x = y
        y = temp
    return total, merged, cell, x, y
```

### Good

```python
from dataclasses import dataclass, field


@dataclass
class Config:
    tags: list[str] = field(default_factory=list)


def build_report(client, rows, fruits, letters, directions, limit):
    total = 0
    total += len(rows)

    for i in range(len(rows)):
        render(rows[i])

    for name, count in fruits.items():
        print(count)

    for index, letter in enumerate(letters):
        print(letter)

    options = {"A": 1, "B": 2}
    merged = {**options, "C": 3}

    client.send(*rows, mode="sync")
    client.configure(retries=3)

    if client.name.startswith(("acme", "foo")):
        greet()

    if total > limit:
        celebrate()

    cell = directions[0, 1]

    x, y = 1, 2
    if x > y:
        x, y = y, x
    return total, merged, cell, x, y
```

### Violations

1. **B026** — `client.send(mode="sync", *rows)`; star-unpacking after a keyword argument silently fills positional slots — unpack first.
2. **PIE800** — `{**options, **{"C": 3}}`; spreading a dict literal into a dict display unwraps what you just wrapped.
3. **PIE804** — `client.configure(**{"retries": 3})`; identifier keys splatted via a dict hide parameter names from type checkers — pass keywords.
4. **PIE807** — `field(default_factory=lambda: [])`; the lambda is the `list` constructor with extra steps.
5. **PIE808** — `range(0, len(rows))`; `0` is the default start — omit it.
6. **PIE810** — `client.name.startswith("acme") or client.name.startswith("foo")`; `startswith` accepts a tuple of prefixes — one call, one scan.
7. **PLC2801** — `total.__gt__(limit)`; dunders are the protocol behind operators, not call sites — write `total > limit`.
8. **PLR1712** — `temp = x; x = y; y = temp`; tuple unpacking swaps atomically in one line without a plumbing variable.
9. **PLR1733** — `print(fruits[name])` inside an `.items()` loop; the value is already in hand as `count` — use it.
10. **PLR1736** — `print(letters[index])` inside an `enumerate()` loop; the item is already in hand as `letter` — use it.
11. **PLR6104** — `total = total + len(rows)`; `x = x + y` repeats the target — use augmented assignment (`+=`).
12. **RUF031** — `directions[(0, 1)]`; inside a subscript the tuple needs no parentheses (default convention).
