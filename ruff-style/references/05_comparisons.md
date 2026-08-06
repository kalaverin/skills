---
---

# Comparisons and truthiness

Use identity, membership, isinstance, and truthiness correctly; avoid traps with literals, tuples, and len().

## Rule of thumb

1. Compare `None`, `True`, and `False` with `is` / `is not`, never with `==` or `isinstance`.
2. Prefer truthiness (`if x:`, `if not x:`) over comparisons to `""`, `False`, or `len(x)`.
3. Use `isinstance(x, T)` for type checks; reserve `type(x) is type(y)` for exact-type identity only.
4. Write negated tests idiomatically: `x not in y` and `x is not y`, never `not x in y` or `not x is y`.
5. Compare literals and single-candidate containers with `==` / `!=`, not `is` or `in [...]`.
6. Avoid one-element tuples in `if` conditions and `assert` statements; they are always truthy.

## Example: Access check

A junior's profile normalizer that second-guesses `None`, types, and booleans.

### Bad

```python
# File: auth/profile.py

from typing import Any


class Account:
    active: bool
    locked: bool


def normalize(raw: Any, admins: list[str]) -> dict[str, Any]:
    if raw == None:  # E711
        raise ValueError("missing user")

    if not raw in admins:  # E713
        raise ValueError("not an admin")

    if type(raw) == dict:  # E721
        profile = raw.get("profile")
    else:
        profile = None

    if isinstance(profile, type(None)):  # FURB168
        profile = {}

    if type(profile) is type(None):  # FURB169
        profile = {}

    if not profile is None:  # E714
        profile["seen"] = True

    account = Account()
    account.active = True
    account.locked = False

    if account.active == True:  # E712
        profile_info = "active"
    else:
        profile_info = "inactive"

    if account.locked == False:  # E712
        status = "unlocked"
    else:
        status = "locked"

    return {"info": profile_info, "status": status, "profile": profile}
```

### Good

```python
# File: auth/profile.py

from typing import Any


class Account:
    active: bool
    locked: bool


def normalize(raw: Any, admins: list[str]) -> dict[str, Any]:
    if raw is None:
        raise ValueError("missing user")

    if raw not in admins:
        raise ValueError("not an admin")

    if isinstance(raw, dict):
        profile = raw.get("profile")
    else:
        profile = None

    if profile is not None:
        profile["seen"] = True

    if profile is None:
        profile = {}

    account = Account()
    account.active = True
    account.locked = False

    if account.active:
        profile_info = "active"
    else:
        profile_info = "inactive"

    if not account.locked:
        status = "unlocked"
    else:
        status = "locked"

    return {"info": profile_info, "status": status, "profile": profile}
```

### Violations

1. **E711** — `raw == None`; singletons should be compared with `is` / `is not`.
2. **E712** — `account.active == True`; boolean literals should be tested with truthiness, not equality.
3. **E713** — `not raw in admins`; negated membership should use `not in`.
4. **E714** — `not profile is None`; negated identity should use `is not`.
5. **E721** — `type(raw) == dict`; type comparisons should use `isinstance` (or `is` for exact types).
6. **FURB168** — `isinstance(profile, type(None))`; `None` is a singleton, use `is None`.
7. **FURB169** — `type(profile) is type(None)`; compare against `None` directly with `is`.

## Example: Report builder

A report publisher that misuses truthiness, literal identity, and tuple conditions.

### Bad

```python
# File: reports/builder.py

from dataclasses import dataclass


@dataclass
class Report:
    title: str
    rows: list[dict]
    status: str
    label: str


def publish(report: Report) -> None:
    if report.title == "":  # PLC1901
        report.title = "Untitled"

    collected = list(report.rows)
    if len(collected):  # PLC1802
        header = collected[0]
    else:
        header = {}

    if report.status in ["draft"]:  # FURB171
        if (report.label == "top",):  # F634
            print("featured")
    else:
        print("published")

    assert (len(report.rows) > 0,)  # F631

    if report.label is "top":  # F632
        print("pinned")
```

### Good

```python
# File: reports/builder.py

from dataclasses import dataclass


@dataclass
class Report:
    title: str
    rows: list[dict]
    status: str
    label: str


def publish(report: Report) -> None:
    if not report.title:
        report.title = "Untitled"

    collected = list(report.rows)
    if collected:
        header = collected[0]
    else:
        header = {}

    if report.status == "draft":
        if report.label == "top":
            print("featured")
    else:
        print("published")

    assert report.rows

    if report.label == "top":
        print("pinned")
```

### Violations

1. **F631** — `assert (len(report.rows) > 0,)`; a one-element tuple is always truthy, so the assertion never fails.
2. **F632** — `report.label is "top"`; identity checks literal values instead of equality.
3. **F634** — `if (report.label == "top",):`; a one-element tuple is always truthy, so the branch always runs.
4. **FURB171** — `report.status in ["draft"]`; a single-item membership test is better written as equality.
5. **PLC1802** — `if len(collected):`; non-empty sequences are truthy, so the `len()` call is noise.
6. **PLC1901** — `report.title == ""`; empty strings are falsey, so truthiness is shorter and idiomatic.
