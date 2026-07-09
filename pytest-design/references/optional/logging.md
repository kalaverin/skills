---
subject: "Assert that the right events are logged: stdlib logs via `caplog` with `set_level`/`at_level`, inspecting `records`/`record_tuples`/`text`/`messages`/`get_records(when)`/`clear()`; structured events via `pytest-structlog` or `structlog.testing.capture_logs`; JSON output via a custom `StreamHandler`; avoid `logging.config.dictConfig` in tests, configure levels in `pyproject.toml`."
index:
  - anchor: logging-caplog
    what: "The built-in `caplog` fixture captures records emitted by the standard `logging` module, storing `WARNING` or higher by default; the level is changed for a whole test with `caplog.set_level(level, logger=...)` or scoped to a block with the `caplog.at_level(level, logger=...)` context manager, and records are read via `caplog.records`, `caplog.record_tuples`, `caplog.text`, and `caplog.messages`, reset with `caplog.clear()`, and phase-sliced with `caplog.get_records(when)` for 'setup'/'call'/'teardown'."
    problem: "Test must prove what stdlib logging emits during run without installing custom handlers, capturing only level and logger opted into; capture records, level scope, logger filter, phase slice, clear setup noise, auto-restore level, no custom handler."
    use_when: "Test must prove stdlib logging output, custom handlers are unnecessary, and opted level plus logger scope enough; capture records, level scope, logger filter, phase slice, clear setup noise, auto restore level, no custom handler."
    avoid_when: "Do not assert against the default `WARNING`-and-above capture when the log under test is `INFO`/`DEBUG` (lower the level with `at_level`/`set_level` first), and do not read unfiltered `caplog.records` across phases when setup or teardown noise would pollute the assertion (use `caplog.clear()` and `caplog.get_records(when)`)."
    expected: "Only the opted-in level and logger are captured, levels auto-restore after the test, and assertions read the right phase and logger via `records`/`record_tuples`/`get_records` with no setup or teardown noise."
  - anchor: logging-messages-and-exceptions
    what: "Asserting that log messages and exception text carry actionable context and the expected field names, verified with `pytest.raises(Exc, match=...)` and by inspecting `str(exc_info.value)`."
    problem: "Error messages omitting offending field or context make failures hard to diagnose from logs alone; actionable message, field name present, context in text, match fragment, diagnose from log, missing field."
    use_when: "Error text must name offending field and context, logs alone should diagnose failure, and exception string carries that fragment; actionable message, field name present, context in text, match fragment, diagnose from log, missing field, exception text."
    avoid_when: "Do not assert only that an exception type is raised; the example constructs `UserCreate(email=None)` and asserts the field name `email` is present, so verify the actionable field/context in the message rather than the type alone."
    expected: "Raised exceptions and log messages include the offending field name and context, so failures are diagnosable from message text asserted via `match=` and `str(exc_info.value)`."
  - anchor: logging-avoid-dictconfig
    what: "The rule that `logging.config.dictConfig` must not run during a `caplog`-dependent test because it can remove the capture handler pytest installed; configure logging at session or import time, or patch out the runtime reconfiguration in the code under test."
    problem: "Mid-test logging reconfiguration can strip capture handler, so caplog silently records nothing and test gives false negative; capture handler stripped, silent empty capture, patch out reconfigure, session-time config, false negative, handler stays installed."
    use_when: "Runtime logging reconfiguration can strip capture handler, caplog would silently record nothing, and session time config or patch keeps handler installed; capture handler stripped, silent empty capture, patch out reconfigure, session time config, false negative, handler stays installed."
    avoid_when: "Do not call `logging.config.dictConfig` during a test that relies on `caplog`; configure logging at session or import time instead, or neutralize the runtime reconfiguration with a patch."
    expected: "Runtime logging reconfiguration is disabled or moved out of the test path, so pytest's capture handler stays installed and `caplog` keeps recording the expected records."
  - anchor: logging-structured
    what: "Capturing structured structlog events with the `log` fixture from `pytest-structlog`, which exposes `log.events` and the helper `log.has(event, **context)`."
    problem: "Plain caplog hides structured bound context inside formatted message, so structured fields cannot be asserted directly; bound context intact, structured event, has helper, no text parsing, contextvar fields, event list assert."
    use_when: "Structured logging binds context fields, formatted message hides them, and event list or helper can assert fields directly; bound context intact, structured event, has helper, no text parsing, contextvar fields, event list assert, structlog fixture."
    avoid_when: "Do not rely on plain `caplog` to inspect structlog bound context (it is hidden in the formatted message); use the `log` fixture's `log.has(...)` and `log.events` instead."
    expected: "Structured events are captured with bound context intact and asserted via `log.has(...)`/`log.events` rather than by parsing formatted log text."
  - anchor: logging-json
    what: "Capturing raw structlog events without `pytest-structlog` using `structlog.testing.capture_logs()` as a context manager, with `structlog.testing.LogCapture` installable as a custom fixture and `structlog.testing.CapturingLoggerFactory` for low-level logger-call assertions."
    problem: "Structlog emitter behavior must unit-test in projects without structlog plugin, including processor-chain effects like contextvar merging; plugin-free capture, raw events, processors explicit, contextvar merge, json render, logger factory."
    use_when: "Structlog behavior must unit test without plugin, processor chain effects matter, and raw events give direct field assertions; plugin free capture, raw events, processors explicit, contextvar merge, json render, logger factory, testing capture."
    avoid_when: "Do not assume `capture_logs()` runs your processors by default (it disables them); pass a `processors` list when processor behavior such as contextvar merging affects the result."
    expected: "Plugin-free structlog tests capture raw events with processors enabled explicitly when they affect the result, and assert on event fields via `capture_logs()`, `LogCapture`, or `CapturingLoggerFactory`."
  - anchor: logging-cli
    what: "Testing JSON-formatted stdlib logs by configuring a `JSONFormatter` subclass or `python-json-logger`, capturing the formatted output through a `logging.StreamHandler` backed by `io.StringIO`, then parsing each JSON line and asserting on its fields."
    problem: "Emitted JSON log lines must contain expected structured fields (message, level, logger, extras) verified by parsing, not raw string assert; parse json line, field assert, in-memory handler, isolate logger, extras field, no raw string."
    use_when: "Emitted logs are JSON lines, expected fields must verify by parsing, and raw string assertion would miss structure; parse json line, field assert, in memory handler, isolate logger, extras field, no raw string, json formatter."
    avoid_when: "Do not assert on the raw formatted string instead of parsing JSON and checking fields, and do not leave the patched logger propagating to other handlers (the example sets `propagate=False` and replaces `handlers`) so duplicate or differently formatted records do not pollute the stream."
    expected: "JSON log lines are parsed into dicts and their fields (message, level, logger, extras like `request_id`) are asserted, with the test logger isolated to the in-memory handler."
  - anchor: logging-variety-booster
    what: "Pytest's log-visibility controls — CLI options `--log-cli-level`, `--log-cli-format`, `--log-format`, `--log-date-format`, `--log-file`, and `--log-file-level`, with persistent equivalents `log_cli` and `log_level` under `[tool.pytest.ini_options]`."
    problem: "Log display in console or file must tune during run without changing capture semantics that tests rely on; live console output, file output, format tune, capture unchanged, persistent setting, ad-hoc display."
    use_when: "Log display must tune during run, capture semantics tests rely on must stay unchanged, and persistent or ad hoc options control visibility; live console output, file output, format tune, capture unchanged, persistent setting, ad hoc display, log level."
    avoid_when: "Do not expect these CLI options or `log_cli`/`log_level` settings to change how `caplog` captures records; they only affect how logs are displayed or written to files."
    expected: "Log display and file output are tuned via `--log-*` options or `log_cli`/`log_level`, while `caplog` capture semantics remain unchanged."
libraries:
  - pytest-structlog
  - python-json-logger
  - structlog
---

# Logging

## Capturing logs with `caplog`
[ref: #logging-caplog]

The built-in `caplog` fixture captures records emitted by the standard `logging` module.
By default it stores records with level `WARNING` or higher.

Use `caplog.set_level(level, logger=...)` to change the level for an entire test.
Use `caplog.at_level(level, logger=...)` as a context manager when the level change should be scoped to a block.
Levels are restored automatically after the test.

```python
import logging

from faker import Faker
from pytest import LogCaptureFixture


def test_service_logs_retry_attempts(
    caplog: LogCaptureFixture,
    fake: Faker,
) -> None:
    """
    Given: a generated retry attempt count.
    When: the service is called with retry.
    Then: warning-level retry logs are captured.
    """
    # --- Arrange ---
    attempt = fake.pyint(min_value=1, max_value=5)

    # --- Act ---
    with caplog.at_level(logging.WARNING, logger="myapp.service"):
        service.call_with_retry(attempt)

    # --- Assert ---
    assert any("retrying" in r.message for r in caplog.records)
    assert all(r.levelno == logging.WARNING for r in caplog.records)
```

Access captured records through `caplog.records` (a list of `logging.LogRecord`), `caplog.record_tuples` (a list of `(logger_name, levelno, message)`), `caplog.text` (the formatted log text), and `caplog.messages` (just the message strings).

```python
from pytest import LogCaptureFixture


def test_log_record_tuples(
    caplog: LogCaptureFixture,
    fake: Faker,
) -> None:
    """
    Given: a generated worker input.
    When: the worker processes it at ERROR level.
    Then: the expected tuple appears in caplog.record_tuples.
    """
    # --- Arrange ---
    # worker input generated below.

    # --- Act ---
    with caplog.at_level(logging.ERROR, logger="myapp.worker"):
        worker.process(fake.uuid4())

    # --- Assert ---
    assert ("myapp.worker", logging.ERROR, "processing failed") in caplog.record_tuples
```

Call `caplog.clear()` to reset captured records inside a test, for example to ignore setup logs.

```python
from pytest import LogCaptureFixture


def test_only_call_logs_are_asserted(
    caplog: LogCaptureFixture,
    fake: Faker,
) -> None:
    """
    Given: caplog is cleared before the task runs.
    When: the task runs at INFO level.
    Then: only call-stage logs contain the completion message.
    """
    # --- Arrange ---
    # caplog will be cleared inside the context.

    # --- Act ---
    with caplog.at_level(logging.INFO, logger="myapp.task"):
        caplog.clear()
        task.run(fake.word())

    # --- Assert ---
    assert any("completed" in r.message for r in caplog.get_records("call"))
```

Use `caplog.get_records(when)` to access logs from other test phases: `"setup"`, `"call"`, or `"teardown"`.

### Testing log messages and exceptions
[ref: #logging-messages-and-exceptions]

Assert that log messages and exception text include actionable context and the right field names.

```python
import pytest


class ValidationError(ValueError):
    """Raised when input data fails domain validation."""


class UserCreate:
    def __init__(self, email: str | None) -> None:
        if email is None:
            raise ValidationError("field 'email' is required")
        self.email = email


def test_validation_error_includes_field_name() -> None:
    """
    Given: a UserCreate call with email set to None.
    When: the constructor raises ValidationError.
    Then: the message includes the email field name.
    """
    # --- Arrange ---
    # email is intentionally None.

    # --- Act ---
    with pytest.raises(ValidationError, match="field 'email' is required") as exc_info:
        UserCreate(email=None)

    # --- Assert ---
    assert "email" in str(exc_info.value)
```

### Avoiding runtime logging reconfiguration
[ref: #logging-avoid-dictconfig]

Do not call `logging.config.dictConfig` during a test that relies on `caplog`, because it may remove the capture handler that pytest installed.
Configure logging at session or import time instead, or patch out runtime reconfiguration in the code under test.

```python
import pytest
from pytest import LogCaptureFixture


def test_service_still_logs_after_config_patch(
    monkey: pytest.MonkeyPatch,
    caplog: LogCaptureFixture,
    fake: Faker,
) -> None:
    """
    Given: runtime logging reconfiguration is patched out.
    When: the service runs at INFO level.
    Then: the started log is still captured.
    """
    # --- Arrange ---
    monkey.setattr("myapp.logging.configure", lambda: None)

    # --- Act ---
    with caplog.at_level(logging.INFO, logger="myapp.service"):
        service.run(fake.uuid4())

    # --- Assert ---
    assert any("started" in r.message for r in caplog.records)
```

## Structured logging with `structlog`
[ref: #logging-structured]

When the application uses `structlog`, plain `caplog` is usually insufficient because the bound context is hidden in the formatted message.
Use the `log` fixture from `pytest-structlog` to capture structured events.

```python
from typing import Any


def test_service_logs_structured_context(
    log: Any,
    fake: Faker,
) -> None:
    """
    Given: a generated user id.
    When: the service emits a structured event.
    Then: the captured event contains the user id.
    """
    # --- Arrange ---
    user_id = fake.uuid4()

    # --- Act ---
    service.do_thing(user_id=user_id)

    # --- Assert ---
    assert log.has("thing_done", user_id=user_id)
```

The fixture exposes `log.events`, a list of captured events, and the helper `log.has(event, **context)`.

For unit tests that do not use `pytest-structlog`, `structlog.testing.capture_logs()` provides a context manager that captures raw events.
It disables processors by default.
Pass a `processors` list to keep behavior such as contextvar merging.

```python
import structlog
from structlog.testing import capture_logs


def test_processor_chain_keeps_context(fake: Faker) -> None:
    """
    Given: a processor chain that merges contextvars and renders JSON.
    When: the service emits an event with a user id.
    Then: the captured event preserves the context.
    """
    # --- Arrange ---
    user_id = fake.uuid4()
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.JSONRenderer(),
    ]

    # --- Act ---
    with capture_logs(processors=processors) as cap:
        service.do_thing(user_id=user_id)

    # --- Assert ---
    assert any(
        e["event"] == "thing_done" and e.get("user_id") == user_id
        for e in cap
    )
```

`structlog.testing.LogCapture` can be installed as a custom fixture, and `structlog.testing.CapturingLoggerFactory` is useful for low-level unit tests that assert on individual logger calls.

## JSON formatted log output
[ref: #logging-json]

For JSON logging with the stdlib module, configure a `JSONFormatter` subclass or use `python-json-logger`.
In tests, capture the formatted output with a custom `logging.StreamHandler` backed by `io.StringIO`, then parse each JSON line and assert on fields.

```python
import io
import json
import logging
from typing import Any

import pytest
from faker import Faker


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "message": record.getMessage(),
            "level": record.levelname,
            "logger": record.name,
        }
        if hasattr(record, "request_id"):
            payload["request_id"] = record.request_id
        return json.dumps(payload)


def test_json_log_contains_request_id(
    monkey: pytest.MonkeyPatch,
    fake: Faker,
) -> None:
    """
    Given: a JSON formatter attached to a patched logger.
    When: an info record is emitted with a request id.
    Then: the JSON output contains the message and request id.
    """
    # --- Arrange ---
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JsonFormatter())
    logger = logging.getLogger("myapp.api")
    monkey.setattr(logger, "handlers", [handler])
    monkey.setattr(logger, "level", logging.INFO)
    monkey.setattr(logger, "propagate", False)

    # --- Act ---
    request_id = fake.uuid4()
    logger.info("request_started", extra={"request_id": request_id})
    record = json.loads(stream.getvalue().strip())

    # --- Assert ---
    assert record["message"] == "request_started"
    assert record["request_id"] == request_id
```

## CLI and configuration
[ref: #logging-cli]

Pytest exposes several CLI options and configuration keys for log visibility.
Useful options include `--log-cli-level`, `--log-cli-format`, `--log-format`, `--log-date-format`, `--log-file`, and `--log-file-level`.
Equivalent persistent settings live under `log_cli` and `log_level` in `pyproject.toml`.

```ini
[tool.pytest.ini_options]
log_cli = true
log_cli_level = "INFO"
log_cli_format = "%(asctime)s %(levelname)s %(name)s %(message)s"
```

These settings affect how logs are displayed or written to files, not how `caplog` captures them.

## Variety booster
[ref: #logging-variety-booster]

Cover more invariants with less code by combining parameterization, Faker, and tuple-based assertions.
Parameterize the expected level and message fragment, then assert that the captured `record_tuples` contain the expected entry regardless of the randomized input.

```python
import logging

import pytest
from faker import Faker
from pytest import LogCaptureFixture


@pytest.mark.parametrize(
    ("level", "message_fragment"),
    [
        (logging.INFO, "started"),
        (logging.WARNING, "retrying"),
        (logging.ERROR, "failed"),
    ],
)
def test_worker_emits_expected_levels(
    caplog: LogCaptureFixture,
    fake: Faker,
    level: int,
    message_fragment: str,
) -> None:
    """
    Given: a parametrized log level and message fragment.
    When: the worker runs at that level.
    Then: a matching record tuple is captured.
    """
    # --- Arrange ---
    job_id = fake.uuid4()

    # --- Act ---
    with caplog.at_level(level, logger="myapp.worker"):
        worker.run(job_id=job_id)

    # --- Assert ---
    assert any(
        name == "myapp.worker" and lvl == level and message_fragment in msg
        for name, lvl, msg in caplog.record_tuples
    )
```

This pattern checks level routing, logger identity, and message content in a single parameterized test.
