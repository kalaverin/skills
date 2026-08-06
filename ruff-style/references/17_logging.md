---
---

# Logging

Keep formatting lazy, loggers module-scoped, and exception handling explicit: never pre-build log messages or log the root logger.

## Rule of thumb

1. Create one module-level logger with `logging.getLogger(__name__)` and log through it; never call the `logging` top-level convenience functions.
2. Pass raw values with `%s`-style placeholders to logging methods; defer formatting so skipped levels do no work.
3. Inside an `except` handler, use `logger.exception(...)` to capture the traceback; do not pass `exc_info` or embed the exception in the message.
4. Outside exception handlers, use `error()` or `warning()` without `exc_info`; never call `.exception()` there.
5. Match every `%` placeholder to exactly one argument and keep `extra` keys away from `LogRecord` attribute names.
6. Prefer `warning`/`WARNING` over `warn`/`WARN`, and add the `f` prefix when a string is meant to interpolate variables.

## Example: Logger setup and configuration

A junior's bootstrap module that instantiates loggers by hand, configures the root logger, and clobbers a `LogRecord` attribute.

### Bad

```python
"""Worker setup."""

import logging


def make_logger():
    # Hand-crafted because getLogger is "too magic".
    return logging.Logger(__name__)  # LOG001


log = make_logger()
app_log = logging.getLogger(__file__)  # LOG002


def boot():
    logging.basicConfig(level=logging.WARN)  # LOG009
    logging.info("service started")  # LOG015

    # Heartbeat loop.
    log.warn("still running")  # G010

    # Authentication event.
    user = "Maria"
    logging.info("login", extra={"name": user})  # G101,LOG015
    log.debug("finished boot for %s", user)
```

### Good

```python
"""Worker setup."""

import logging

logger = logging.getLogger(__name__)


def boot():
    logging.basicConfig(level=logging.WARNING)
    logger.info("service started")
    logger.warning("still running")

    user = "Maria"
    logger.info("login", extra={"user_id": user})
    logger.debug("finished boot for %s", user)
```

### Violations

1. **G010** — `log.warn("still running")`; `warn` is a deprecated alias for `warning`.
2. **G101** — `extra={"name": user}`; `name` clashes with a `LogRecord` attribute.
3. **LOG001** — `logging.Logger(__name__)`; loggers should be created with `getLogger`.
4. **LOG002** — `logging.getLogger(__file__)`; `__file__` is a path, not a module namespace.
5. **LOG009** — `logging.basicConfig(level=logging.WARN)`; `logging.WARN` is an undocumented alias.
6. **LOG015** — `logging.info("service started")` and `logging.info("login", extra={"name": user})`; root-logger calls lose source information.

## Example: Message formatting

A telemetry helper that builds its messages every way except the lazy one.

### Bad

```python
"""User action logging."""

import logging

logger = logging.getLogger(__name__)


def log_action(name, day, value):
    # Built from a template, but the f-prefix is missing.
    message = "Hello {name}! It is {day} today!"  # RUF027
    logger.info(message)

    # Every eager formatting style known to Python.
    logger.info("{} - Something happened".format(name))  # G001
    logger.info("%s - Something happened" % name)  # G002
    logger.info(name + " - Something happened")  # G003
    logger.info(f"{name} - Something happened")  # G004
    logger.info("value is %s", str(value))  # RUF065

    # Caller only wants to know we logged.
    return True
```

### Good

```python
"""User action logging."""

import logging

logger = logging.getLogger(__name__)


def log_action(name, day, value):
    logger.info("Hello %s! It is %s today!", name, day)
    logger.info("%s - Something happened", name)
    logger.info("value is %s", value)

    return True
```

### Violations

1. **G001** — `"{} - Something happened".format(name)`; eager `str.format` in a logging call.
2. **G002** — `"%s - Something happened" % name`; eager `%` formatting in a logging call.
3. **G003** — `name + " - Something happened"`; eager string concatenation in a logging call.
4. **G004** — `f"{name} - Something happened"`; f-strings evaluate before the level is checked.
5. **RUF027** — `message = "Hello {name}! It is {day} today!"`; missing `f` prefix on an f-string-like literal.
6. **RUF065** — `str(value)`; logging already converts `%s` arguments to strings.

## Example: Exception handling

A service method that mishandles tracebacks, placeholder counts, and `exc_info`.

### Bad

```python
"""Service exception handling."""

import logging

logger = logging.getLogger(__name__)


def handle(value):
    try:
        result = int(value)
    except ValueError:
        logger.exception("parse failed", exc_info=True)  # G202

    try:
        1 / 0
    except ZeroDivisionError:
        logger.error("division failed", exc_info=True)  # G201

    try:
        open("missing.txt")
    except OSError:
        logger.error("cannot open file")  # TRY400

    try:
        raise RuntimeError("boom")
    except RuntimeError:
        logger.exception("boom", exc_info=False)  # LOG007

    try:
        raise TypeError("bad type")
    except TypeError as e:
        logger.exception(f"Found an error: {e}")  # G004,TRY401

    logger.exception("not in an except block")  # LOG004
    logger.warning("something looks wrong", exc_info=True)  # LOG014


def report(error):
    logger.error("%s error occurred: %s", error)  # PLE1206
    logger.error("Error occurred: %s", type(error), error)  # PLE1205
```

### Good

```python
"""Service exception handling."""

import logging

logger = logging.getLogger(__name__)


def handle(value):
    try:
        result = int(value)
    except ValueError:
        logger.exception("parse failed")

    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("division failed")

    try:
        open("missing.txt")
    except OSError:
        logger.exception("cannot open file")

    try:
        raise RuntimeError("boom")
    except RuntimeError:
        logger.exception("boom")

    try:
        raise TypeError("bad type")
    except TypeError:
        logger.exception("Found an error")

    logger.error("not in an except block")
    logger.warning("something looks wrong")


def report(error):
    logger.error("%s error occurred: %s", type(error), error)
```

### Violations

1. **G201** — `logger.error("division failed", exc_info=True)`; use `exception()` instead of `error(..., exc_info=True)`.
2. **G202** — `logger.exception("parse failed", exc_info=True)`; `exception()` already includes `exc_info=True`.
3. **LOG004** — `logger.exception("not in an except block")`; `.exception()` only makes sense inside an `except` handler.
4. **LOG007** — `logger.exception("boom", exc_info=False)`; falsy `exc_info` defeats `exception()`, use `error()`.
5. **LOG014** — `logger.warning("something looks wrong", exc_info=True)`; `exc_info=True` is useless outside an `except` handler.
6. **PLE1205** — `logger.error("Error occurred: %s", type(error), error)`; more arguments than `%s` placeholders.
7. **PLE1206** — `logger.error("%s error occurred: %s", error)`; fewer arguments than `%s` placeholders.
8. **TRY400** — `logger.error("cannot open file")`; inside an `except` handler, prefer `exception()` over `error()`.
9. **TRY401** — `logger.exception(f"Found an error: {e}")`; `exception()` already logs the exception object.
