---
---

# Datetime

Always produce timezone-aware datetimes; avoid naive APIs that create ambiguous instants.

## Example: Event logger

A junior's timestamp helpers for an event logger, using every naive `datetime` constructor they could find.

### Bad

```python
# File: analytics/event_logger.py

"""Event logger helpers."""

import datetime


DEFAULT_DEADLINE = datetime.datetime(2025, 6, 15, 9, 0)  # DTZ001


def local_now():
    return datetime.datetime.today()  # DTZ002


def utc_now():
    return datetime.datetime.utcnow()  # DTZ003


def current_marker():
    return datetime.datetime.now()  # DTZ005


def posix_to_naive(ts):
    return datetime.datetime.fromtimestamp(ts)  # DTZ006


def legacy_posix_to_naive(ts):
    return datetime.datetime.utcfromtimestamp(ts)  # DTZ004


def parse_event_time(value):
    return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")  # DTZ007
```

### Good

```python
# File: analytics/event_logger.py

"""Event logger helpers."""

import datetime


DEFAULT_DEADLINE = datetime.datetime(
    2025, 6, 15, 9, 0, tzinfo=datetime.timezone.utc
)


def local_now():
    return datetime.datetime.now(tz=datetime.timezone.utc)


def utc_now():
    return datetime.datetime.now(tz=datetime.timezone.utc)


def current_marker():
    return datetime.datetime.now(tz=datetime.timezone.utc)


def posix_to_naive(ts):
    return datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)


def legacy_posix_to_naive(ts):
    return datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)


def parse_event_time(value):
    return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
```

### Violations

1. **DTZ001** — `datetime.datetime(2025, 6, 15, 9, 0)`; constructor called without `tzinfo`.
2. **DTZ002** — `datetime.datetime.today()`; `today()` returns a naive local datetime.
3. **DTZ003** — `datetime.datetime.utcnow()`; `utcnow()` returns a naive datetime.
4. **DTZ004** — `datetime.datetime.utcfromtimestamp(ts)`; `utcfromtimestamp()` returns a naive datetime.
5. **DTZ005** — `datetime.datetime.now()`; `now()` called without a `tz` argument.
6. **DTZ006** — `datetime.datetime.fromtimestamp(ts)`; `fromtimestamp()` called without a `tz` argument.
7. **DTZ007** — `datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")`; parsing without `%z` produces a naive datetime.

## Example: Retention bounds

A retention service that picks naive calendar dates and uses `datetime.max` as a "never" sentinel.

### Bad

```python
# File: catalog/retention.py

"""Retention rules for catalog items."""

import datetime


NEVER = datetime.datetime.max  # DTZ901


def cutoff_date():
    return datetime.date.today()  # DTZ011


def day_from_published(ts):
    return datetime.date.fromtimestamp(ts)  # DTZ012


def is_archived(item):
    return item["archived_at"] is None or item["archived_at"] < NEVER
```

### Good

```python
# File: catalog/retention.py

"""Retention rules for catalog items."""

import datetime


NEVER = datetime.datetime.max.replace(tzinfo=datetime.timezone.utc)


def cutoff_date():
    return datetime.datetime.now(tz=datetime.timezone.utc).date()


def day_from_published(ts):
    return datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc).date()


def is_archived(item):
    return item["archived_at"] is None or item["archived_at"] < NEVER
```

### Violations

1. **DTZ011** — `datetime.date.today()`; `date.today()` is naive and ignores timezone boundaries.
2. **DTZ012** — `datetime.date.fromtimestamp(ts)`; treats the timestamp as local time.
3. **DTZ901** — `datetime.datetime.max`; `datetime.max` is naive and can fail on conversion or comparison.

## Rule of thumb

1. Always pass `tzinfo=` to `datetime.datetime(...)` or use an aware factory.
2. Use `datetime.datetime.now(tz=...)` for the current instant; never use `today()`, `utcnow()`, or bare `now()`.
3. Convert POSIX timestamps with `fromtimestamp(ts, tz=...)`; never use `utcfromtimestamp()` or the bare form.
4. After `strptime(...)`, attach a timezone with `.replace(tzinfo=...)` or parse a format that includes `%z`.
5. Derive calendar dates from an aware datetime via `.date()`, not from `date.today()` or `date.fromtimestamp()`.
6. Treat `datetime.min` and `datetime.max` as naive sentinels — attach a timezone before using them.
