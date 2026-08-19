---
subject: "Prove warning behavior: assert specific warning with `pytest.warns(Category, match=...)` and inspect record, assert clean paths emit none via `warnings.catch_warnings(record=True)`/`recwarn`, inspect multiple ordered warnings with `recwarn` (`clear`/`pop`/indexing), scope policy per-test with `@pytest.mark.filterwarnings` or project-wide in `pyproject.toml`, custom warning classes, Python 3.13 `@warnings.deprecated`, and `stacklevel` verification."
index:
  - anchor: warnings-basic-assertions
    what: "`pytest.warns(WarningCategory, match='regex')` asserts a block emits at least one warning of the category whose message matches the regex; the context manager returns a record collection exposing `category`, `message`, `filename`, `lineno`."
    problem: "Test must prove right warning category and message emit, with inspectable record metadata, otherwise regressions can swap warnings silently; category match, message regex, record filename, record lineno, escape literal, tuple of categories."
    use_when: "A test must assert that a code block emits a warning of a specific category; the message must match a regex; record metadata needs inspection."
    avoid_when: "The message contains unescaped regex metacharacters; a single category is pinned when any subclass is acceptable; only presence is checked."
    expected: "The expected warning category and message are asserted, record metadata is inspectable, and literal matches are escaped."
  - anchor: warnings-no-warnings
    what: "Prove a code path is clean by capturing warnings (`warnings.catch_warnings(record=True)` or the `recwarn` fixture) and asserting the list is empty, or by running pytest with `-W error`."
    problem: "Path assumed warning-free may silently emit warnings without explicit capture or escalation, hiding regressions in dependency upgrades and cluttering CI logs; capture empty list, escalate to error, prove clean, simplefilter always, warning-free assert, no silent warn."
    use_when: "A code path must be proven warning-free; warnings can be captured to an empty list or escalated to errors; CI policy requires clean output."
    avoid_when: "Warning output is ignored; the path is known to emit warnings; global `-W error` is not feasible."
    expected: "Clean paths are proven warning-free via an empty captured list or `-W error` escalation."
  - anchor: warnings-multiple-warnings
    what: "The `recwarn` fixture records every warning in a test and supports `clear()`, `pop()`, indexing, and iteration for per-record category/message inspection."
    problem: "Several call sites each emit warning, requiring ordered or categorized per-record checks, and uncaptured warnings hide which site produced which message; ordered records, category count, clear between phases, pop index, per-record inspect, order not guaranteed."
    use_when: "Multiple warnings are emitted in one test; per-record category/message checks are needed; order may or may not be guaranteed."
    avoid_when: "Warning order is assumed stable when not guaranteed; only total count matters; warnings are not separated by phase."
    expected: "Each emitted warning is checked by category/message with order-dependent or category-counted assertions as appropriate."
  - anchor: warnings-filterwarnings
    what: "`@pytest.mark.filterwarnings('error')`, `'ignore::DeprecationWarning'`, or `'default::UserWarning'` suppresses or escalates warnings for a single test without changing project defaults."
    problem: "Single test may need warning-free or intentionally noisy behavior without altering global policy, and scattered inline filters are hard to discover; per-test marker, error action, ignore action, default action, project default unchanged, document policy."
    use_when: "One test must deviate from project warning defaults; the test should be warning-free or intentionally noisy; global policy must stay unchanged."
    avoid_when: "Project-wide defaults are changed for one test; the deviation is not documented; every test duplicates the same filter."
    expected: "Per-test warning behavior is explicit via markers; project defaults stay unchanged."
  - anchor: warnings-project-config
    what: "Set `filterwarnings` under `[tool.pytest.ini_options]` in `pyproject.toml` to promote warnings to errors in CI or ignore third-party noise; still overridable per test."
    problem: "Global policy must escalate warnings project-wide while silencing known third-party noise, otherwise CI either misses regressions or drowns in irrelevant warnings; escalate to error, targeted ignore, ci policy, local override, external noise, one file policy."
    use_when: "Project-wide warning policy must be defined in one place; known third-party noise should be ignored; CI should treat warnings as errors."
    avoid_when: "Warning rules are copied into every test; third-party noise fails CI without an explicit ignore; per-test overrides are impossible."
    expected: "CI escalates warnings to errors project-wide with explicit third-party ignores, and per-test overrides remain possible."
  - anchor: warnings-custom-classes
    what: "Define domain-specific warnings inheriting from `UserWarning` or `DeprecationWarning` and assert by category so tests survive message rewording."
    problem: "Asserting only on message text breaks tests when wording changes, forcing noisy refactors, masking real warning regressions, and slowing code review; stable category, survive reword, subclass warning, category assert, optional regex, reword robust."
    use_when: "Warning message text is expected to change; a fixed category is available; assertions should survive message rewording."
    avoid_when: "Assertions rely solely on exact message text; no custom warning category exists; rewording should break tests."
    expected: "Tests key on stable warning categories, staying robust across message rewording while remaining precise."
  - anchor: warnings-deprecated-decorator
    what: "Python 3.13 `warnings.deprecated()` emits `DeprecationWarning` when the decorated function is called; use the `typing_extensions` backport on older versions and test with `pytest.warns(DeprecationWarning, match=...)."
    problem: "Deprecation decorator must test like manual warn, with version-correct imports, otherwise tests fail on older interpreters or miss deprecation signal; deprecation warning, backport import, match notice, version gate, decorated callable, older interpreter."
    use_when: "A callable is decorated with `warnings.deprecated` or its backport; the test must verify emitted `DeprecationWarning`; Python version varies."
    avoid_when: "`warnings.deprecated` is imported unconditionally on Python <3.13; no `typing_extensions` backport is used; the message is not asserted."
    expected: "Deprecated callables emit `DeprecationWarning` verified by `pytest.warns`, with version-appropriate imports."
  - anchor: warnings-variety-booster
    what: "Vary the data flowing through warning-producing code and assert on warning record metadata; parametrize the input condition with the expected category and message."
    problem: "Single-input message-only checks miss category, metadata regressions, and edge inputs, leaving warning behavior under-tested across domains and slowing debugging; vary input, category metadata, stacklevel filename, rotate domains, custom subclass, clear between phases."
    use_when: "Warning-producing code has multiple input conditions; category and metadata must be asserted alongside message; parametrization can cover the matrix."
    avoid_when: "Only one input is tested; message text is the only assertion; metadata and category are ignored."
    expected: "Warnings are verified across varied inputs with category and metadata (filename/stacklevel) assertions, not just message text."
libraries:
  - typing-extensions
---


# Warning Testing

Quick reference for asserting, suppressing, inspecting, and configuring warnings in pytest tests.

## Basic Warning Assertions

[ref: #warnings-basic-assertions]

`pytest.warns(WarningCategory, match="regex")` asserts that a block of code emits at least one warning of the given category and that its message matches the supplied regular expression.
The context manager returns a `warnings.WarningMessage` record collection, so you can also inspect `category`, `message`, `filename`, and `lineno` after the assertion succeeds.
Pass a tuple of categories when the exact subclass does not matter.

```python
import warnings
import pytest
from faker import Faker


DEPRECATION_MESSAGE = "v2 API will be removed in v3"
MISSING_TIMEOUT_MESSAGE = "optional field 'timeout' not set"


class LegacyClient:
    def get(self, path: str) -> None:
        warnings.warn(f"{path}: {DEPRECATION_MESSAGE}", DeprecationWarning, stacklevel=2)


class ConfigLoader:
    def __init__(self, filename: str) -> None:
        if "timeout" not in filename:
            warnings.warn(MISSING_TIMEOUT_MESSAGE, UserWarning, stacklevel=2)


def test_legacy_endpoint_emits_deprecation_warning() -> None:
    """
    Given: a LegacyClient and a legacy endpoint.
    When: the endpoint is requested.
    Then: a DeprecationWarning with the expected message is emitted.
    """
    # --- Arrange ---
    client = LegacyClient()
    endpoint = "/api/v1/users"

    # --- Act / Assert ---
    with pytest.warns(DeprecationWarning, match=DEPRECATION_MESSAGE):
        client.get(endpoint)


def test_config_loader_warns_on_missing_optional_field(fake: Faker) -> None:
    """
    Given: a ConfigLoader and a filename without a timeout marker.
    When: the loader is instantiated.
    Then: a UserWarning about the missing timeout is emitted.
    """
    # --- Arrange ---
    filename = fake.file_name(extension="yaml")

    # --- Act / Assert ---
    with pytest.warns(UserWarning, match=MISSING_TIMEOUT_MESSAGE):
        ConfigLoader(filename)


def test_warning_record_exposes_metadata(fake: Faker) -> None:
    """
    Given: a ConfigLoader that emits a missing-timeout warning.
    When: the warning is captured.
    Then: the record exposes category, message, filename, and line metadata.
    """
    # --- Arrange ---
    filename = fake.file_name(extension="yaml")

    # --- Act ---
    with pytest.warns(UserWarning, match="not set") as warning_record:
        ConfigLoader(filename)

    # --- Assert ---
    assert len(warning_record) == 1
    assert issubclass(warning_record[0].category, UserWarning)
    assert "timeout" in str(warning_record[0].message)
    assert warning_record[0].filename.endswith("test_config.py")
```

Adjust the `endswith` check to match the actual test module name.
Use `re.escape()` when the intended match is a literal string that contains regex metacharacters.

## Asserting No Warnings

[ref: #warnings-no-warnings]

To prove that a code path stays clean, capture warnings and assert the list is empty.
Use `warnings.catch_warnings(record=True)` for a focused context, or rely on the `recwarn` fixture to capture warnings for the whole test.

```python
import warnings
import pytest
from faker import Faker


class StableApi:
    def process(self, email: str) -> dict[str, str]:
        return {"email": email}


def test_clean_context_emits_no_warnings(fake: Faker) -> None:
    """
    Given: a StableApi and a generated email.
    When: the API is called inside a warnings capture context.
    Then: no warnings are recorded.
    """
    # --- Arrange ---
    api = StableApi()
    email = fake.fake_email()

    # --- Act ---
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        api.process(email)

    # --- Assert ---
    assert len(captured) == 0


def test_clean_api_emits_no_warnings(
    fake: Faker,
    recwarn: pytest.WarningsRecorder,
) -> None:
    """
    Given: a StableApi and the recwarn fixture.
    When: the API processes a generated email.
    Then: the recwarn list remains empty.
    """
    # --- Arrange ---
    api = StableApi()

    # --- Act ---
    api.process(fake.fake_email())

    # --- Assert ---
    assert len(recwarn) == 0
```

Alternatively, run pytest with `-W error` so any unexpected warning becomes a test failure without writing extra assertions.

## Inspecting Multiple Warnings

[ref: #warnings-multiple-warnings]

The `recwarn` fixture records every warning emitted during a test.
It supports `clear()`, `pop()`, indexing, and iteration, which makes it convenient when several call sites should each produce a warning.

```python
import warnings
import pytest


class OldApi:
    def method_a(self) -> None:
        warnings.warn("method_a is deprecated; use new_api", DeprecationWarning, stacklevel=2)

    def method_b(self) -> None:
        warnings.warn("method_b is deprecated; use new_api", DeprecationWarning, stacklevel=2)


def test_deprecated_methods_emit_correct_warnings(
    recwarn: pytest.WarningsRecorder,
) -> None:
    """
    Given: an OldApi instance that emits a warning per method call.
    When: both deprecated methods are called.
    Then: two DeprecationWarnings are recorded with the correct method names.
    """
    # --- Arrange ---
    old_api = OldApi()

    # --- Act ---
    old_api.method_a()
    old_api.method_b()

    # --- Assert ---
    assert len(recwarn) == 2
    first, second = recwarn[0], recwarn[1]
    assert issubclass(first.category, DeprecationWarning)
    assert "method_a" in str(first.message)
    assert issubclass(second.category, DeprecationWarning)
    assert "method_b" in str(second.message)
    assert first.filename.endswith("test_legacy.py")
```

When order matters, compare each record individually.
When order does not matter, sort or count by category.

## Per-Test Warning Policy

[ref: #warnings-filterwarnings]

`@pytest.mark.filterwarnings` suppresses or escalates warnings for a single test without changing project defaults.
Use `"error"` to turn warnings into failures, `"ignore::DeprecationWarning"` to silence legacy noise, and `"default::UserWarning"` to restore normal display.

```python
import warnings
import pytest
from faker import Faker


class StableApi:
    def process(self, email: str) -> dict[str, str]:
        return {"email": email}


class LegacyApi:
    def call(self) -> None:
        warnings.warn("legacy endpoint", DeprecationWarning, stacklevel=2)


@pytest.mark.filterwarnings("error")
def test_clean_path_is_warning_free(fake: Faker) -> None:
    """
    Given: a StableApi under filterwarnings("error").
    When: it processes a generated email.
    Then: no warning is raised.
    """
    # --- Arrange ---
    api = StableApi()
    email = fake.fake_email()

    # --- Act / Assert ---
    api.process(email)


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_legacy_feature_still_works() -> None:
    """
    Given: a LegacyApi under filterwarnings("ignore::DeprecationWarning").
    When: its deprecated method is called.
    Then: no exception is raised and the call succeeds.
    """
    # --- Act / Assert ---
    LegacyApi().call()
```

Use this marker to document tests that are intentionally noisy or that must remain warning-free.

## Project-Wide Warning Policy

[ref: #warnings-project-config]

Configure a global warnings policy in `pyproject.toml` under `[tool.pytest.ini_options]`.
This is the right place to promote warnings to errors in CI or to ignore third-party noise.

```toml
[tool.pytest.ini_options]
filterwarnings = [
    "error",
    "ignore::DeprecationWarning:thirdparty.*",
    "ignore::UserWarning:some_legacy_library.*",
]
```

You can still override this policy per test with `@pytest.mark.filterwarnings`.

## Custom Warning Classes

[ref: #warnings-custom-classes]

Domain-specific warnings should inherit from `UserWarning` or `DeprecationWarning`.
Testing by category makes tests robust against message rewording.

```python
import warnings
import pytest
from faker import Faker


MISSING_TIMEOUT_MESSAGE = "optional field 'timeout' not set"


class MissingTimeoutWarning(UserWarning):
    """Emitted when a configuration omits an optional timeout value."""


class ConfigLoader:
    def __init__(self, filename: str) -> None:
        if "timeout" not in filename:
            warnings.warn(MISSING_TIMEOUT_MESSAGE, MissingTimeoutWarning, stacklevel=2)


def test_config_loader_uses_custom_warning_category(fake: Faker) -> None:
    """
    Given: a ConfigLoader that emits a custom warning.
    When: the loader is instantiated with a filename lacking a timeout marker.
    Then: a MissingTimeoutWarning with the expected message is emitted.
    """
    # --- Arrange ---
    filename = fake.file_name(extension="yaml")

    # --- Act / Assert ---
    with pytest.warns(MissingTimeoutWarning, match=MISSING_TIMEOUT_MESSAGE):
        ConfigLoader(filename)
```

Combine custom categories with message regexes to keep assertions both stable and precise.

## Python 3.13 `warnings.deprecated()`

[ref: #warnings-deprecated-decorator]

Python 3.13 introduces `warnings.deprecated()`, a standard decorator that emits `DeprecationWarning` when a decorated callable is called.
The same behavior is available on older Python versions through the `typing_extensions` backport.
Test it exactly like a manual `warnings.warn`.

```python
import pytest
from faker import Faker
from warnings import deprecated


DEPRECATION_NOTICE = "Use create_user_v2 instead."


@deprecated(DEPRECATION_NOTICE)
def create_user_v1(email: str) -> dict[str, str]:
    return {"email": email}


def test_deprecated_decorator_emits_deprecation_warning(fake: Faker) -> None:
    """
    Given: a deprecated create_user_v1 function.
    When: it is called with a generated email.
    Then: a DeprecationWarning containing the deprecation notice is emitted.
    """
    # --- Arrange ---
    email = fake.fake_email()

    # --- Act / Assert ---
    with pytest.warns(DeprecationWarning, match=DEPRECATION_NOTICE):
        create_user_v1(email)
```

On Python older than 3.13, import `deprecated` from `typing_extensions` instead.

## Variety Booster

[ref: #warnings-variety-booster]

Increase coverage by varying the data that flows through the warning-producing code and by asserting on the warning record metadata.
Parametrize the input condition together with the expected warning category and message.

```python
import warnings
import pytest
from faker import Faker


LOUD_MODE_WARNING = "loud mode is experimental"


class Greeter:
    def greet(self, name: str, loud: bool) -> str:
        if loud:
            warnings.warn(LOUD_MODE_WARNING, UserWarning, stacklevel=2)
        return f"Hello, {name}"


@pytest.mark.parametrize(
    "loud,expected_category,expected_message",
    [
        (True, UserWarning, LOUD_MODE_WARNING),
        (False, None, ""),
    ],
)
def test_greeter_warning_depends_on_mode(
    fake: Faker,
    loud: bool,
    expected_category: type[Warning] | None,
    expected_message: str,
) -> None:
    """
    Given: a Greeter and a parametrized loud flag.
    When: the greeter is invoked.
    Then: a warning is emitted only when loud is True.
    """
    # --- Arrange ---
    greeter = Greeter()
    name = fake.first_name()

    # --- Act / Assert ---
    if expected_category is not None:
        with pytest.warns(expected_category, match=expected_message):
            greeter.greet(name, loud=loud)
    else:
        with warnings.catch_warnings(record=True) as captured:
            warnings.simplefilter("always")
            greeter.greet(name, loud=loud)
        assert len(captured) == 0
```

Other ways to add variety:

- Assert `warning_record[0].filename` ends with the test module to verify `stacklevel`.
- Rotate Faker providers for warning messages, identifiers, and RFC 2606 test domains.
- Use custom warning subclasses so tests are tied to semantics rather than exact wording.
- Clear `recwarn` between phases with `recwarn.clear()` and verify warnings per phase.
