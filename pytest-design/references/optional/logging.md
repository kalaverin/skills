---
subject: "Assert logged events and exception text carry expected content: stdlib capture via `caplog` with `set_level`/`at_level` and `records`/`record_tuples`/`text`/`messages`/`get_records(when)`/`clear()`, field-named error messages via `pytest.raises(match=...)`, structured events via `pytest-structlog` `log.events`/`log.has` or `structlog.testing.capture_logs`/`LogCapture`/`CapturingLoggerFactory`, JSON output via custom `StreamHandler`+`io.StringIO` parsed per line, `logging.config.dictConfig` runtime ban, `--log-cli-level`/`log_cli` display tuning."
index:
  - anchor: logging-caplog
    what: "The built-in `caplog` fixture captures records emitted by the standard `logging` module, storing `WARNING` or higher by default; the level is changed for a whole test with `caplog.set_level(level, logger=...)` or scoped to a block with the `caplog.at_level(level, logger=...)` context manager, and records are read via `caplog.records`, `caplog.record_tuples`, `caplog.text`, and `caplog.messages`, reset with `caplog.clear()`, and phase-sliced with `caplog.get_records(when)` for 'setup'/'call'/'teardown'."
    problem: "Test must prove what stdlib logging emits during run without installing custom handlers, capturing only level and logger opted into; default warning threshold, invisible info debug, setup teardown pollution, record tuple shape, formatted text versus messages, phase-scoped read."
    use_when: "Assertion concerns stdlib logging output; capture default would hide INFO/DEBUG record under test; capture must narrow to specific level, logger, or test phase."
    avoid_when: "Default WARNING-only capture asserted against INFO/DEBUG emission; unfiltered `caplog.records` read across phases although setup/teardown noise pollutes assertion; custom handler installed where built-in fixture suffices."
    expected: "Only opted-in level and logger are captured, levels restore after test, and assertions read correct phase via `records`/`record_tuples`/`get_records` with no setup or teardown noise."
  - anchor: logging-messages-and-exceptions
    what: "Asserting that log messages and exception text carry actionable context and the expected field names, verified with `pytest.raises(Exc, match=...)` and by inspecting `str(exc_info.value)`."
    problem: "Error message omits offending field name and context, so diagnosing failure from logs alone turns into guesswork once only records remain; type-only assertion gap, production log diagnosis, required-field message, message as contract, support ticket reading, offending value echoed."
    use_when: "Error contract includes message content, not just type; log text must suffice for diagnosis without reproducing; specific field or context fragment belongs in output."
    avoid_when: "Assertion stops at exception type with no message check; vague message without field name or context accepted as contract; `match=` fragment so broad it passes on any text."
    expected: "Raised errors and log messages name offending field with context, so message text alone supports diagnosis via `match=` and `str(exc_info.value)`."
  - anchor: logging-avoid-dictconfig
    what: "The rule that `logging.config.dictConfig` must not run during a `caplog`-dependent test because it can remove the capture handler pytest installed; configure logging at session or import time, or patch out the runtime reconfiguration in the code under test."
    problem: "Code under test reconfigures logging mid-run, which can remove capture handler pytest installed, so caplog records nothing while suite stays green; dictconfig at runtime, false green build, handler ownership, configure timing choice, reconfigure hidden in fixture."
    use_when: "Code under test calls logging configuration at runtime; `caplog` assertions exist in same suite; empty capture must be distinguishable from genuine no-log."
    avoid_when: "`logging.config.dictConfig` executes on test path relying on `caplog`; reconfiguration left active where patching it out is one line; logging configured repeatedly per test instead of once at session/import time."
    expected: "Runtime reconfiguration is patched out or moved to session/import time, capture handler survives, and `caplog` keeps recording expected records."
  - anchor: logging-structured
    what: "Capturing structured structlog events with the `log` fixture from `pytest-structlog`, which exposes `log.events` and the helper `log.has(event, **context)`."
    problem: "Plain caplog flattens structlog bound context into formatted message string, so key-value fields like user_id escape direct assertion and force fragile text parsing; event dict shape, plugin fixture present, bound user id field, event list membership."
    use_when: "Application logs through structlog with bound context; assertion targets individual fields rather than formatted text; `pytest-structlog` available in environment."
    avoid_when: "Plain `caplog` expected to expose bound context (it lands inside formatted message); field assertions done through string parsing of `caplog.text`; stdlib-only logging under test (fixture adds nothing there)."
    expected: "Structured events arrive with bound context intact, asserted per field via `log.has(...)` or `log.events` membership instead of text parsing."
  - anchor: logging-structured
    what: "Capturing raw structlog events without `pytest-structlog` using `structlog.testing.capture_logs()` as a context manager, with `structlog.testing.LogCapture` installable as a custom fixture and `structlog.testing.CapturingLoggerFactory` for low-level logger-call assertions."
    problem: "Structlog emitter behavior needs unit-level verification in project without `pytest-structlog` plugin, and processor-chain effects like contextvar merging must survive capture intact; processors disabled gotcha, low-level logger calls, dict-style event access, custom capture fixture."
    use_when: "Structlog behavior needs unit tests and `pytest-structlog` is absent or unwanted; processor chain affects emitted event; assertions target raw event fields."
    avoid_when: "`capture_logs()` expected to run processors (they are disabled unless passed explicitly); contextvar-dependent events asserted without enabling chain; plugin fixture available but bypassed for hand-rolled capture."
    expected: "Raw events captured plugin-free with processors enabled explicitly when they shape the result, asserted via `capture_logs()`, `LogCapture`, or `CapturingLoggerFactory`."
  - anchor: logging-json
    what: "Testing JSON-formatted stdlib logs by configuring a `JSONFormatter` subclass or `python-json-logger`, capturing the formatted output through a `logging.StreamHandler` backed by `io.StringIO`, then parsing each JSON line and asserting on its fields."
    problem: "Emitted JSON log lines must carry expected structured fields (message, level, logger, extras like request_id), and asserting on raw formatted string instead of parsed document misses structure-level regressions; propagation duplicate records, request id extra, formatter under test, json line schema."
    use_when: "Service emits JSON-formatted logs; field-level verification matters more than string matching; formatted output can route through in-memory stream."
    avoid_when: "Raw formatted string asserted instead of parsed fields; patched logger left propagating to other handlers so records duplicate or mix formats; formatter behavior assumed rather than exercised through `StreamHandler`."
    expected: "Each emitted line parses into dict whose message, level, logger, and extras fields assert cleanly, with test logger isolated to in-memory handler."
  - anchor: logging-cli
    what: "Pytest's log-visibility controls — CLI options `--log-cli-level`, `--log-cli-format`, `--log-format`, `--log-date-format`, `--log-file`, and `--log-file-level`, with persistent equivalents `log_cli` and `log_level` under `[tool.pytest.ini_options]`."
    problem: "Console shows too little during failure triage and persistent display preferences scatter across developer machines, yet tuning display must never alter capture semantics assertions depend on; ci log artifact, live debugging visibility, post-mortem log review, date format control."
    use_when: "Console or file display needs adjustment for one run or persistently; `caplog`-based assertions exist and their semantics must stay untouched; team shares ini-level logging preferences."
    avoid_when: "Display options expected to change what `caplog` records (they only affect presentation and file writes); per-developer flags relied on where shared ini setting expresses team default; capture tuning attempted through `--log-*` flags."
    expected: "Visibility is tuned via `--log-*` options or `log_cli`/`log_level` settings while `caplog` keeps capturing exactly as before."
  - anchor: logging-variety-booster
    what: "Covering level routing, logger identity, and message content in one parametrized test by combining `@pytest.mark.parametrize` over `(level, message_fragment)` with `caplog.at_level` and `record_tuples` membership assertions."
    problem: "Level, logger name, and message fragment each deserve coverage, yet separate test per combination triples body count with identical arrange and assert logic; tuple membership proof, randomized input stability, info warning error ladder, fragment substring match, tuple name level message."
    use_when: "Several level/message combinations need identical assertion logic; captured tuples must match regardless of randomized input; one body should cover level routing, logger name, and content."
    avoid_when: "One test cloned per level or fragment; assertion tied to specific random value instead of stable fragment; `record_tuples` ignored while re-parsing `caplog.text` manually."
    expected: "Single parametrized body proves every level routes with expected fragment on right logger, independent of faker-generated inputs."
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
