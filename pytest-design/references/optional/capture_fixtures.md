---
subject: "Capture and assert on program output without `-s`: Python streams via `capsys`/`capsysbinary`, OS file-descriptor output via `capfd`/`capfdbinary`, and logs via `caplog` with `at_level`/`set_level`; inspect `records`, `text`, `record_tuples`, `get_records`, bypass capture with `capsys.disabled()`, build an `assert_log_contains` helper."
index:
  - anchor: capture-fixtures-capsys
    what: "Pytest fixtures that capture text written to `sys.stdout`/`sys.stderr` (`capsys`) and the same streams as bytes (`capsysbinary`), both exposing `readouterr()` for incremental snapshots."
    problem: "Code under test writes to `sys.stdout`/`sys.stderr`, and assertion must read that text without `-s` or external log inspection; captured output, printed text, stream inspection, stdout content, stderr content, buffered writes, console output, line-buffered output."
    use_when: "Code writes text to Python stdout or stderr, assertion needs that content, and capture must stay enabled without external logs; captured output, printed text, stream inspection, stdout content, stderr content, buffered writes, console output, readouterr snapshot."
    avoid_when: "Do not assert exact terminal formatting as the primary invariant unless the component is a CLI renderer."
    expected: "Python-level stdout and stderr are captured incrementally via `readouterr()` as text or bytes, with assertions on content rather than exact terminal formatting."
  - anchor: capture-fixtures-capfd
    what: "Pytest fixtures that capture writes to OS file descriptors 1 and 2 as text (`capfd`) or bytes (`capfdbinary`) when output bypasses `sys.stdout`."
    problem: "Output originates from native code, `os.write`, or subprocess that bypasses `sys.stdout`, so Python-level capture sees nothing and assertion needs file-descriptor layer; fd-level capture, native output, subprocess writes, bypass sys streams, bytes vs text, low-level capture."
    use_when: "Output bypasses Python streams through native code, subprocess, or descriptor write, while assertion still needs captured text or bytes; fd capture, native output, subprocess write, descriptor write, bytes versus text, low level stream, bypass sys stdout."
    avoid_when: "Prefer `capsys` for pure Python code because it is slightly faster and avoids fd-level noise."
    expected: "Fd-level output from native code or subprocesses is captured and asserted as text or bytes, while pure Python output stays on the faster `capsys` layer."
  - anchor: capture-fixtures-caplog
    what: "The `caplog` fixture attaches a handler to the root logger and captures `LogRecord` objects, exposing level filtering, formatted text, record tuples, and per-stage retrieval."
    problem: "Code under test logs via stdlib logging, and test must prove expected records, levels, and logger name without reading external log files; log record capture, level filtering, logger identity, message assertion, record tuples, phase slicing, handler-free verify."
    use_when: "Code emits stdlib logging records, test must prove level, logger, and message without external files, and handler installation must stay intact; log record capture, level filtering, logger identity, message assertion, record tuples, phase slicing, handler free verify."
    avoid_when: "Do not assert exact formatting if the production handler customizes the layout, and do not reconfigure the root logger inside the test without restoring it."
    expected: "Log records are captured at the configured level with content, level, and logger name asserted via `records`/`record_tuples`/`text`, while exact handler formatting and root-logger reconfiguration are left out of the assertions."
---

# CAPTURE FIXTURES

## capsys and capsysbinary

[ref: #capture-fixtures-capsys]

`capsys` captures text written to `sys.stdout` and `sys.stderr`, while `capsysbinary` captures the same streams as bytes, and both expose `readouterr()` for incremental inspection.

```python
import sys

from faker import Faker
from pytest import CaptureFixture


def _emit_to_stdout(text: str) -> None:
    sys.stdout.write(f"{text}\n")


def test_stdout_capture_is_incremental(
    capsys: CaptureFixture[str],
    fake: Faker,
) -> None:
    """
    Given: two sentences written to stdout.
    When: capsys reads the output after each write.
    Then: each read returns only the delta written since the previous read.
    """
    # --- Arrange ---
    first = fake.sentence()
    second = fake.sentence()

    # --- Act ---
    _emit_to_stdout(first)
    first_capture = capsys.readouterr()
    _emit_to_stdout(second)
    second_capture = capsys.readouterr()

    # --- Assert ---
    assert first_capture.out.strip() == first
    assert second_capture.out.strip() == second
    assert second_capture.err == ""
```

Use `capsys.disabled()` as a context manager when you temporarily need output to reach the real terminal.

```python
def test_disabled_capture_bypasses_capture(
    capsys: CaptureFixture[str],
    fake: Faker,
) -> None:
    """
    Given: capture is disabled inside a context manager.
    When: text is written to stdout.
    Then: capsys does not capture the output.
    """
    # --- Arrange ---
    text = fake.sentence()

    # --- Act ---
    with capsys.disabled():
        _emit_to_stdout(text)

    # --- Assert ---
    assert capsys.readouterr().out == ""
```

For raw byte output, use `capsysbinary` and compare `bytes` values.

```python
def test_stdout_bytes_capture_is_incremental(
    capsysbinary: CaptureFixture[bytes],
    fake: Faker,
) -> None:
    """
    Given: two byte payloads written to stdout.buffer.
    When: capsysbinary reads the output after each write.
    Then: each read returns only the delta written since the previous read.
    """
    # --- Arrange ---
    first = fake.sentence().encode()
    second = fake.sentence().encode()

    # --- Act ---
    sys.stdout.buffer.write(first + b"\n")
    first_capture = capsysbinary.readouterr()
    sys.stdout.buffer.write(second + b"\n")
    second_capture = capsysbinary.readouterr()

    # --- Assert ---
    assert first_capture.out.strip() == first
    assert second_capture.out.strip() == second
```

**Variety booster:** parametrize the stream target and payload length, and assert that each `readouterr()` call snapshots only the delta written since the previous call.

## capfd and capfdbinary

[ref: #capture-fixtures-capfd]

`capfd` captures writes to OS file descriptors 1 and 2, and `capfdbinary` captures the same descriptors as bytes, which is necessary when the code under test invokes subprocesses or C extensions that bypass `sys.stdout`.

```python
import os

from faker import Faker
from pytest import CaptureFixture


def test_fd_level_stdout_is_captured(
    capfd: CaptureFixture[str],
    fake: Faker,
) -> None:
    """
    Given: a message written directly to file descriptor 1.
    When: capfd reads the captured output.
    Then: stdout contains the message and stderr is empty.
    """
    # --- Arrange ---
    message = fake.sentence()

    # --- Act ---
    os.write(1, (message + "\n").encode())
    captured = capfd.readouterr()

    # --- Assert ---
    assert captured.out.strip() == message
    assert captured.err == ""
```

For fd-level byte output, use `capfdbinary`.

```python
def test_fd_level_bytes_are_captured(
    capfdbinary: CaptureFixture[bytes],
    fake: Faker,
) -> None:
    """
    Given: raw bytes written directly to file descriptor 1.
    When: capfdbinary reads the captured output.
    Then: stdout contains the exact bytes and stderr is empty.
    """
    # --- Arrange ---
    data = fake.sentence().encode()

    # --- Act ---
    os.write(1, data + b"\n")
    captured = capfdbinary.readouterr()

    # --- Assert ---
    assert captured.out.strip() == data
    assert captured.err == b""
```

**Variety booster:** parametrize the file descriptor (`1` vs `2`) and payload type (text vs non-UTF-8 bytes) to cover stdout, stderr, and binary edge cases in one test.

## caplog

[ref: #capture-fixtures-caplog]

`caplog` attaches a handler to the root logger and captures `LogRecord` objects, supporting level filtering, formatted text, record tuples, and per-stage retrieval.

```python
import logging

from faker import Faker
from pytest import LogCaptureFixture


logger = logging.getLogger(__name__)


def _retry_for_user(user_id: str) -> None:
    logger.warning("retry for user %s", user_id)


def test_retry_logs_warning_with_user_id(
    caplog: LogCaptureFixture,
    fake: Faker,
) -> None:
    """
    Given: a user id and a warning-level logger.
    When: the retry helper logs a warning for that user.
    Then: caplog captures one warning record with the expected details.
    """
    # --- Arrange ---
    user_id = fake.uuid4()

    # --- Act ---
    with caplog.at_level(logging.WARNING, logger=logger.name):
        _retry_for_user(user_id)

    # --- Assert ---
    assert len(caplog.records) == 1
    assert caplog.records[0].levelno == logging.WARNING
    assert user_id in caplog.text
    expected_tuple = (logger.name, logging.WARNING, caplog.records[0].message)
    assert expected_tuple in caplog.record_tuples
```

Per-stage records are available through `caplog.get_records("setup")`, `"call"`, and `"teardown"`, so you can also assert log output produced during fixture setup or teardown.

```python
def test_call_stage_records_are_available(
    caplog: LogCaptureFixture,
    fake: Faker,
) -> None:
    """
    Given: a log message emitted at INFO level during the test call.
    When: caplog.get_records is asked for call-stage records.
    Then: the message appears in the returned records.
    """
    # --- Arrange ---
    prefix = fake.word()
    user_id = fake.uuid4()
    message = f"{prefix} {user_id}"

    # --- Act ---
    with caplog.at_level(logging.INFO, logger=logger.name):
        logger.info("%s", message)
    call_records = caplog.get_records("call")

    # --- Assert ---
    assert any(message in record.message for record in call_records)
```

**Variety booster:** write a small `assert_log_contains(caplog, level, substring)` helper that checks `caplog.records`, `caplog.record_tuples`, and `caplog.text` so one assertion covers level, logger name, and message content.

## Anti-patterns

[ref: #capture-fixtures-anti-patterns]

Capture fixtures verify observable side effects, but they should not become the primary contract for logic that should be tested through return values, state, or dedicated logging APIs.

- Do not test `print()` output as the main behavior unless the component under test is a CLI renderer.
- Do not rely on running tests with `pytest -s` to see output; capture fixtures make output assertions deterministic and CI-friendly.
- Do not reconfigure the root logger with `logging.config.dictConfig` during a test without restoring it, because `caplog` cannot capture records after a full reconfiguration.

Prefer asserting the return value first, and only then check the captured stream for a human-readable summary.

```python
import sys

from faker import Faker
from pytest import CaptureFixture


def _cli_echo(token: str) -> None:
    sys.stdout.write(f"{token}\n")


def test_cli_output_includes_token(
    capsys: CaptureFixture[str],
    fake: Faker,
) -> None:
    """
    Given: a CLI token.
    When: the CLI helper echoes it to stdout.
    Then: the captured output contains the token and the helper returns None.
    """
    # --- Arrange ---
    token = fake.word()

    # --- Act ---
    result = _cli_echo(token)
    captured = capsys.readouterr()

    # --- Assert ---
    assert result is None
    assert token in captured.out
```

**Variety booster:** split CLI tests into two groups—one that asserts the structured return value or exit code, and one that asserts only the human-readable summary line.

## Common Errors

[ref: #capture-fixtures-common-errors]

Most capture-fixture surprises come from choosing the wrong capture layer, comparing bytes to text, or letting logger levels hide the records you expected.

| Symptom | Cause | Fix |
|---|---|---|
| `capsys.readouterr()` is empty | Output bypassed `sys.stdout` and went to the OS file descriptor | Switch to `capfd` |
| `capfd.readouterr()` is empty | Output went through `sys.stdout` and pytest captured it at the sys layer | Switch to `capsys` |
| `caplog.text` is empty | Root logger level is above the emitted level, or the logger was reconfigured | Use `caplog.set_level` or `caplog.at_level`, and avoid `logging.config.dictConfig` |
| `caplog` captures too many records | Default WARNING level lets noisy libraries through | Scope `caplog` to a named logger or raise the level |
| Binary output does not match the expected string | File-descriptor bytes are compared against a `str` | Compare `bytes` values and decode only when necessary |

The most frequent `caplog` fix is to lower the captured level for the test or for a specific logger.

```python
import logging

from faker import Faker
from pytest import LogCaptureFixture


logger = logging.getLogger(__name__)


def test_debug_record_appears_after_level_change(
    caplog: LogCaptureFixture,
    fake: Faker,
) -> None:
    """
    Given: caplog is configured to capture DEBUG records.
    When: a debug message is logged with a user id.
    Then: the message appears in the captured records.
    """
    # --- Arrange ---
    user_id = fake.uuid4()
    caplog.set_level(logging.DEBUG, logger=logger.name)

    # --- Act ---
    logger.debug("charged %s", user_id)

    # --- Assert ---
    assert any(user_id in record.message for record in caplog.records)
```

**Variety booster:** centralize an `assert_log_contains(caplog, level, substring)` helper that calls `caplog.clear()` between operations and asserts across `records`, `record_tuples`, and `text` to catch level, logger, and message mismatches in one place.
