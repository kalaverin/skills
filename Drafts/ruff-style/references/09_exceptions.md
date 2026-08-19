---
---

# Exceptions

Precise exception handling: narrow excepts, explicit chaining, clean messages, and no exception abuse for control flow.

## Rule of thumb

1. Raise only exception classes or instances: a precise builtin or a named subclass — `TypeError` for wrong types, `ValueError` for wrong values, `NotImplementedError` for stubs — never literals, never bare `Exception`.
2. Build messages away from the raise site: assign to a variable first, and move parameterized messages into the exception class's `__init__`.
3. Catch only what you can handle: name specific exceptions in a plain tuple, keep one handler per exception, and let everything else propagate.
4. Never swallow errors silently: no bare `except`, no `except Exception: pass/continue`; log with `logging.exception`, or use `contextlib.suppress(SpecificError)` when suppression is deliberate.
5. Chain explicitly inside handlers: bare `raise` to re-raise, otherwise `raise NewError(...) from exc` or `from None`.
6. Keep `try`/`finally` tight: only fallible statements inside `try`, success path in `else`, `finally` reserved for cleanup (no jumps, never empty), and `yield` in a `@contextmanager` always wrapped in `try`/`finally`.
7. Treat `assert` as a debug tool that vanishes under `python -O`; in tests use the `pytest.raises(SpecificError, match=...)` context manager with an escaped pattern.

## Example: Raising the right thing

A junior's profile validator that throws whatever is at hand and fumbles re-raising.

### Bad

```python
"""User profile validation."""


class Profile:
    def rename(self, name):
        if not name:
            raise "empty name"  # B016
        self.name = name

    def save(self):
        raise NotImplemented  # F901


def check_age(age):
    if age < 0:
        ValueError("negative age")  # PLW0133
    if age is None:
        raise  # PLE0704
    if age > 150:
        raise ValueError()  # RSE102
    return age


def load_profile(raw):
    try:
        age = int(raw["age"])
    except KeyError:
        msg = "missing age field"
        raise ValueError(msg)  # B904
    except ValueError as exc:
        raise exc  # TRY201
    return age
```

### Good

```python
"""User profile validation."""


class Profile:
    def rename(self, name):
        if not name:
            msg = "empty name"
            raise ValueError(msg)
        self.name = name

    def save(self):
        raise NotImplementedError


def check_age(age):
    if age is None:
        msg = "age cannot be None"
        raise ValueError(msg)
    if age < 0:
        msg = "negative age"
        raise ValueError(msg)
    if age > 150:
        raise ValueError
    return age


def load_profile(raw):
    try:
        age = int(raw["age"])
    except KeyError as exc:
        msg = "missing age field"
        raise ValueError(msg) from exc
    return age
```

### Violations

1. **B016** — `raise "empty name"`; raising a literal fails at runtime with `TypeError`, masking the real failure.
2. **B904** — `raise ValueError(msg)` inside `except KeyError`; a raise without `from` leaves the cause ambiguous — use `from exc` or `from None`.
3. **F901** — `raise NotImplemented`; `NotImplemented` is a sentinel for binary special methods, not an exception — raise `NotImplementedError`.
4. **PLE0704** — bare `raise` in `check_age`; there is no active exception outside a handler, so it fails with `RuntimeError`.
5. **PLW0133** — `ValueError("negative age")`; constructing an exception without `raise` is a no-op, almost always a forgotten `raise`.
6. **RSE102** — `raise ValueError()`; empty parentheses on an argument-less raise are noise.
7. **TRY201** — `raise exc`; re-raising by name resets the traceback to this line — bare `raise` preserves it.

## Example: Choosing the type and the message

An order validator with vanilla classes, the wrong error type, and messages baked into raise sites.

### Bad

```python
"""Order validation."""


class OrderError(Exception):
    pass


def validate_order(order, quantity):
    if not isinstance(quantity, int):
        msg = f"quantity must be int, got {type(quantity).__name__}"
        raise ValueError(msg)  # TRY004
    if quantity <= 0:
        raise OrderError(f"quantity {quantity} is not positive")  # EM102,TRY003
    if not order:
        raise Exception  # TRY002
    if order.get("closed"):
        raise RuntimeError("order is already closed")  # EM101,TRY003
    if order.get("total") is None:
        raise OrderError("order {} has no total".format(order["id"]))  # EM103
    return quantity
```

### Good

```python
"""Order validation."""


class OrderError(Exception):
    pass


class NonPositiveQuantity(OrderError):
    def __init__(self, quantity):
        super().__init__(f"quantity {quantity} is not positive")


def validate_order(order, quantity):
    if not isinstance(quantity, int):
        msg = f"quantity must be int, got {type(quantity).__name__}"
        raise TypeError(msg)
    if quantity <= 0:
        raise NonPositiveQuantity(quantity)
    if not order:
        raise OrderError
    if order.get("closed"):
        msg = "order is already closed"
        raise OrderError(msg)
    if order.get("total") is None:
        msg = f"order {order['id']} has no total"
        raise OrderError(msg)
    return quantity
```

### Violations

1. **EM101** — `raise RuntimeError("order is already closed")`; the literal is echoed twice in the traceback — assign it to a variable first.
2. **EM102** — `raise OrderError(f"quantity {quantity} is not positive")`; the f-string is echoed twice in the traceback — assign it first.
3. **EM103** — `raise OrderError("order {} has no total".format(...))`; the `.format` call makes the echoed traceback line longest of all — assign it first.
4. **TRY002** — `raise Exception`; a vanilla class leaves callers no precise handle — define a named subclass.
5. **TRY003** — `raise OrderError(f"quantity {quantity} is not positive")` and `raise RuntimeError("order is already closed")`; long messages formatted at raise sites drift apart — build them in the exception's `__init__`.
6. **TRY004** — `raise ValueError(msg)` under an `isinstance` check; a wrong *type* means `TypeError` — `ValueError` is for wrong values.

## Example: Catch-clause shape

A config loader whose handlers are mangled in every way the `except` clause allows.

### Bad

```python
"""Load and normalize plugin configuration."""

import json


def load_config(path):
    try:
        text = path.read_text()
    except (OSError, OSError):  # B014
        text = ""
    except ValueError:
        text = ""
    except ValueError:  # B025
        text = "default"
    try:
        data = json.loads(text)
    except ():  # B029
        data = {}
    try:
        key = data["key"]
    except "KeyError":  # B030
        key = ""
    try:
        return int(data["timeout"]) or key
    except ValueError or TypeError:  # B030,PLW0711
        return 0


def normalize_record(client, record_id):
    try:
        return client.get(record_id)
    except (ValueError,):  # B013
        return None
```

### Good

```python
"""Load and normalize plugin configuration."""

import json


def load_config(path):
    try:
        text = path.read_text()
    except OSError:
        text = ""
    except ValueError:
        text = "default"
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        data = {}
    key = data.get("key", "")
    try:
        return int(data["timeout"]) or key
    except (ValueError, TypeError):
        return 0


def normalize_record(client, record_id):
    try:
        return client.get(record_id)
    except ValueError:
        return None
```

### Violations

1. **B013** — `except (ValueError,)`; a one-element tuple is redundant punctuation — catch the class directly.
2. **B014** — `except (OSError, OSError)`; the same class listed twice in one handler is dead code — de-duplicate.
3. **B025** — the second `except ValueError`; the first matching handler wins, so the duplicate is unreachable.
4. **B029** — `except ()`; an empty tuple matches nothing and the handler is dead code.
5. **B030** — `except "KeyError"` and `except ValueError or TypeError`; catching a non-exception raises `TypeError: catching classes that do not inherit from BaseException`.
6. **PLW0711** — `except ValueError or TypeError`; `or` evaluates to the first class, so only `ValueError` is ever caught — multiple exceptions go in a tuple.

## Example: Swallowed and blind errors

A nightly sync worker that hides every failure it meets.

### Bad

```python
"""Nightly sync worker."""

import contextlib


def sync_all(client, jobs):
    for job in jobs:
        try:
            client.push(job)
        except:  # E722
            print("push failed")
        try:  # SIM105
            client.notify(job)
        except Exception:  # BLE001,S110
            pass
        try:  # SIM105
            job.archive()
        except OSError:
            pass
    while client.has_pending():
        try:
            client.flush()
        except Exception:  # BLE001,S112
            continue
    with contextlib.suppress():  # B022
        client.close()
```

### Good

```python
"""Nightly sync worker."""

import contextlib
import logging


def sync_all(client, jobs):
    for job in jobs:
        try:
            client.push(job)
        except OSError as exc:
            logging.warning("push failed: %s", exc)
        try:
            client.notify(job)
        except Exception:
            logging.exception("notify failed")
        with contextlib.suppress(OSError):
            job.archive()
    while client.has_pending():
        try:
            client.flush()
        except Exception:
            logging.exception("flush failed")
            break
    client.close()
```

### Violations

1. **B022** — `contextlib.suppress()`; no arguments means nothing is suppressed — name the exception or drop the wrapper.
2. **BLE001** — both `except Exception` handlers; blind catches hide bugs you never anticipated — catch what you expect, or log with `logging.exception`.
3. **E722** — bare `except`; catches `KeyboardInterrupt` and `SystemExit`, breaking Ctrl-C and shutdown.
4. **S110** — `except Exception: pass`; silently discards every error — log it, or suppress a specific exception explicitly.
5. **S112** — `except Exception: continue`; the same silent swallow in a loop — a permanently broken iteration spins forever untraced.
6. **SIM105** — the `try`/`except ...: pass` blocks around `client.notify(job)` and `job.archive()`; deliberate suppression is one line of `contextlib.suppress(...)`.

## Example: finally and context managers

**Target:** `py37`

A batch importer that lets `finally` drive control flow and leaks a cursor on error.

### Bad

```python
"""Batch import of legacy records."""

from contextlib import contextmanager


@contextmanager
def db_transaction(conn):
    cursor = conn.cursor()
    yield cursor  # RUF075
    cursor.close()


def import_batch(conn, rows):
    imported = 0
    for row in rows:
        try:
            conn.execute("INSERT INTO legacy VALUES (?)", row)
        except ValueError:
            mark_skipped(row)
        finally:
            continue  # B012,PLE0116
        imported += 1
    try:
        conn.commit()
    except OSError:
        queue_retry(conn)
    finally:  # RUF072
        pass
    try:
        return imported / len(rows)
    except ZeroDivisionError:
        msg = "no rows to import"
        raise ValueError(msg) from None
    finally:
        return 0.0  # B012,SIM107
```

### Good

```python
"""Batch import of legacy records."""

from contextlib import contextmanager


@contextmanager
def db_transaction(conn):
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        cursor.close()


def import_batch(conn, rows):
    if not rows:
        msg = "no rows to import"
        raise ValueError(msg)
    imported = 0
    for row in rows:
        try:
            conn.execute("INSERT INTO legacy VALUES (?)", row)
        except ValueError:
            mark_skipped(row)
            continue
        imported += 1
    try:
        conn.commit()
    except OSError:
        queue_retry(conn)
    return imported / len(rows)
```

### Violations

1. **B012** — `continue` and `return 0.0` inside `finally`; jump statements in `finally` execute unconditionally and silently discard in-flight exceptions.
2. **PLE0116** — `continue` inside `finally`; a `SyntaxError` before Python 3.8 and the same swallowing hazard after it — move loop control into `else` or the handler.
3. **RUF072** — `finally: pass` after `conn.commit()`; an empty `finally` is a no-op — delete it.
4. **RUF075** — `yield cursor` unprotected; when the `with` body raises, `cursor.close()` never runs — wrap `yield` in `try`/`finally`.
5. **SIM107** — `return 0.0` in `finally` alongside a `return` in `try`; the `finally` return overrides every branch and swallows exceptions — assign in branches, return once.

## Example: try-body hygiene

A report helper whose `try` blocks do far too much.

### Bad

```python
"""Usage report generation."""

from random import randint


def random_ratio() -> float:
    try:  # PLW0717
        a = randint(-100, 100)
        b = randint(-100, 100)
        c = randint(-100, 100)
        d = randint(-100, 100)
        scale = randint(1, 5)
        res = scale * (a + b) / (c + d)
    except ZeroDivisionError:
        return random_ratio()
    else:
        return res


def reciprocal(n):
    try:
        rec = 1 / n
        print(f"reciprocal of {n} is {rec}")
        return rec  # TRY300
    except ZeroDivisionError:
        return float("nan")


def ensure_token(user):
    try:
        token = user.token
        if token is None:
            raise ValueError  # TRY301
    except ValueError:  # TRY203
        raise
```

### Good

```python
"""Usage report generation."""

from random import randint


def random_ratio() -> float:
    a = randint(-100, 100)
    b = randint(-100, 100)
    c = randint(-100, 100)
    d = randint(-100, 100)
    scale = randint(1, 5)
    try:
        res = scale * (a + b) / (c + d)
    except ZeroDivisionError:
        return random_ratio()
    return res


def reciprocal(n):
    try:
        rec = 1 / n
    except ZeroDivisionError:
        return float("nan")
    else:
        print(f"reciprocal of {n} is {rec}")
        return rec


def ensure_token(user):
    token = user.token
    if token is None:
        raise ValueError
    return token
```

### Violations

1. **PLW0717** — the six-statement `try` in `random_ratio`; fat `try` bodies hide which line raised and over-guard innocent statements — keep only fallible statements inside (default limit: 5).
2. **TRY203** — `except ValueError: raise` in `ensure_token`; catching only to re-raise immediately changes nothing — delete the handler and let it propagate.
3. **TRY300** — `return rec` at the end of the `try`; success-path code inside `try` is guarded by handlers written for the fallible line — move it to `else`.
4. **TRY301** — `raise ValueError` inside the `try` that itself catches `ValueError`; raising and catching in one `try` is control flow cosplaying as error handling.

## Example: Asserts and testing exceptions

A test module that misuses `assert` and the legacy pytest API.

### Bad

```python
"""Tests for the cart module."""

import pytest

from shop.cart import Cart


def check_cart(cart):
    assert (total := cart.total()) >= 0  # RUF018
    assert total == cart.expected, print("total mismatch")  # RUF030
    items = cart.items()
    assert len(items), 3  # RUF040
    if cart.broken:
        assert False  # B011
    return total


def test_cart_errors():
    cart = Cart()
    with pytest.raises(Exception):  # B017
        cart.checkout()
    with pytest.raises(ValueError, match="total (USD)."):  # RUF043
        cart.total()
    pytest.raises(KeyError, cart.apply, "code")  # RUF061
```

### Good

```python
"""Tests for the cart module."""

import pytest

from shop.cart import Cart


def check_cart(cart):
    total = cart.total()
    assert total >= 0
    assert total == cart.expected, "total mismatch"
    items = cart.items()
    assert len(items) == 3
    if cart.broken:
        raise AssertionError
    return total


def test_cart_errors():
    cart = Cart()
    with pytest.raises(ValueError):
        cart.checkout()
    with pytest.raises(ValueError, match=r"total \(USD\)\."):
        cart.total()
    with pytest.raises(KeyError):
        cart.apply("code")
```

### Violations

1. **B011** — `assert False`; `python -O` strips asserts, so it silently becomes a no-op — raise `AssertionError`.
2. **B017** — `pytest.raises(Exception)`; passes when the code fails for the wrong reason — assert a specific exception, plus `match=` to pin the message.
3. **RUF018** — `assert (total := cart.total()) >= 0`; under `-O` the walrus is skipped, leaving `total` undefined.
4. **RUF030** — `assert total == cart.expected, print("total mismatch")`; `print` returns `None`, so the raised `AssertionError` carries no message.
5. **RUF040** — `assert len(items), 3`; the literal `3` is a forgotten comparison — this asserts non-emptiness, not length 3.
6. **RUF043** — `match="total (USD)."`; `match` is a regex, so `.` and `(...)` match far more than intended — escape metacharacters in a raw string.
7. **RUF061** — `pytest.raises(KeyError, cart.apply, "code")`; the legacy callable form cannot take `match=` or keyword arguments — use the context-manager form.
