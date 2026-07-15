---
subject: "Assert error contracts precisely: `pytest.raises(Exc, match=...)` with specific regex (`re.escape` for literals), capture `ExceptionInfo` and inspect `.type`/`.value`/attributes (`exc_info.type is ExactException`), parametrize cases, `pytest.deprecated_call`/`pytest.warns`, `xfail(raises=...)`, and manual `ExceptionGroup` inspection; never `match='.*'`, broad `Exception`, or `exc_info.typename`."
index:
  - anchor: exceptions-raises-match
    what: "`pytest.raises(ExpectedExc, match=<regex>)` asserts the block raises the expected exception type and that `str(exc.value)` matches the `match` regex via `re.search`."
    problem: "Asserting only exception type passes when right type carries wrong message, so message fragment must pin exact failure; type and message, escape literal, broad pattern trap, regex search, wrong text slip."
    use_when: "Asserting an exception where the type alone could pass with the wrong message; only a message fragment pins the exact failure; literal text needs `re.escape` before matching."
    avoid_when: "Broad patterns such as `match='.*'` or `match='error'` — they mask unintended exceptions."
    expected: "The test passes only when the exact exception type is raised with the pinned message text, and unrelated messages fail."
  - anchor: exceptions-exc-info
    what: "Capturing the raised exception via `with pytest.raises(Exc) as exc_info` and inspecting its `.type`, `.value`, and `.traceback` for attributes beyond the message."
    problem: "Some exceptions carry structured state (custom attributes, args) that message fragment cannot assert, so failure cause stays hidden without deeper inspection; type identity, traceback, typename trap, attribute contract, args payload, nested state."
    use_when: "Exception carries structured state beyond its message; non-message state like attributes, `args`, or traceback must be asserted; type check needs identity rather than a name string."
    avoid_when: "`exc_info.typename` asserted for type checks — it is a mostly-informational string; use `exc_info.type is ExpectedException`."
    expected: "Precise assertions on type and structured attributes pass, with type checks done via identity on `exc_info.type`."
  - anchor: exceptions-parametrize
    what: "Combining `@pytest.mark.parametrize` with `pytest.raises` so many invalid inputs that share an exception type and message pattern reuse one assertion body."
    problem: "Hand-writing one test per invalid input duplicates same raises boilerplate and discourages adding failure modes; shared exception pattern, control labels, generate values, one body many inputs, add mode by label, invalid matrix."
    use_when: "Many invalid inputs share one exception type and message pattern; per-input tests duplicate the same raises boilerplate; new failure modes should cost one label."
    avoid_when: "Near-identical `pytest.raises` tests duplicated for each invalid input when a parametrized label set would cover them with one body."
    expected: "Adding a new failure mode requires only a new label, while one assertion body covers every parametrized invalid input."
  - anchor: exceptions-warnings
    what: "`pytest.deprecated_call()` asserts a block emits a `DeprecationWarning`/`PendingDeprecationWarning`, and `pytest.warns(WarningClass, match=...)` asserts a specific warning class plus matching message text."
    problem: "Warning emission must assert without coupling tests to unrelated warning classes or to exception-raising tools, so deprecation signal stays precise across releases; class match, message regex, release drift, overfit coupling, pending deprecation, emission contract."
    use_when: "Block must emit a specific warning class; warning text must match a pattern; coupling to unrelated warning classes would overfit the implementation."
    avoid_when: "Warning helpers applied to assert expected exceptions — they are for warnings only."
    expected: "Warning assertions target the exact class (and fragment) required, and exception contracts are never asserted through warning helpers."
  - anchor: exceptions-xfail
    what: "`@pytest.mark.xfail(raises=ExpectedException)` documents a known unfixed bug, whereas `pytest.raises` enforces behavior that is already correct."
    problem: "Using xfail for intended behavior hides contract, while using raises for unfixed bug breaks suite on known-bad code; known bug document, issue link, strict xfail, fix detection, xpass signal, build stability."
    use_when: "Known unfixed bug needs documentation without breaking the build; correct behavior must be enforced instead; unexpected pass must signal the bug is fixed."
    avoid_when: "`xfail` used as a substitute for `pytest.raises` when the exception is the intended contract."
    expected: "Known bugs are documented as xfail with a linked issue while correct behavior is enforced by pytest.raises, so the suite stays green without hiding contracts."
  - anchor: exceptions-anti-patterns
    what: "A reference lookup table of common exception-testing anti-patterns, each paired with the harm it causes and the preferred alternative."
    problem: "Teams repeatedly ship confidence-reducing exception assertions because no shared checklist of known-bad patterns exists, so reviews miss recurring mistakes; broad match, typename assert, broad exception, legacy callable form, bare except, hidden bugs, masked regression, vague regex."
    use_when: "Reviewing exception tests for known-bad patterns; assertions pass for unrelated failures; tightening loose patterns and type checks."
    avoid_when: "`match='.*'`, asserting `exc_info.typename`, catching the over-wide `Exception` base in `pytest.raises`, the legacy `pytest.raises(Exc, func, *args, **kwargs)` call style, and unqualified `except:` or `except Exception:` in production code."
    expected: "Every exception assertion is specific (type, message fragment, or attribute) and would fail on an unintended exception, with the table backing the review process."
  - anchor: exceptions-exception-group
    what: "Manually inspecting `exc_info.value.exceptions` to assert on individual members of an `ExceptionGroup` (Python 3.11+), with `pytest.RaisesGroup` available on pytest 8.0+."
    problem: "ExceptionGroup bundles multiple exceptions, so single type and message assertion cannot verify individual inner errors and suite loses failure detail; group inspect, version gate, member assertion, bundled failures, subgroup match, manual iteration."
    use_when: "`ExceptionGroup` bundles inner errors; type-plus-message on the group cannot verify individuals; choosing between manual inspection and `pytest.RaisesGroup` by pytest version."
    avoid_when: "`ExceptionGroup` asserted as if it were a single exception (type+message only) when the bundled members are the real invariant."
    expected: "Each inner exception's type and message is asserted from the captured group, working across pytest versions."
---

# EXCEPTION TESTING — CORE

## `pytest.raises` with Specific `match`

[ref: #exceptions-raises-match]

```python
import re

import pytest
from faker import Faker


NEGATIVE_RADIUS_MESSAGE = "negative radius not allowed"


class Circle:
    def __init__(self, radius: float) -> None:
        if radius < 0:
            raise ValueError(f"{NEGATIVE_RADIUS_MESSAGE}: {radius}")
        self.radius = radius


def test_circle_rejects_negative_radius(fake: Faker) -> None:
    """
    Given: a circle with a negative radius.
    When: the circle is instantiated.
    Then: ValueError is raised with the expected message.
    """
    # --- Arrange ---
    negative_radius = -fake.pyfloat(min_value=0.1, max_value=100.0, positive=True)

    # --- Act ---
    with pytest.raises(ValueError, match=NEGATIVE_RADIUS_MESSAGE):
        Circle(radius=negative_radius)

    # --- Assert ---
    # Exception raised as expected; assertion handled by pytest.raises context.


def test_circle_rejects_negative_radius_with_literal_match(fake: Faker) -> None:
    """
    Given: a negative radius and its escaped literal error fragment.
    When: the circle is instantiated.
    Then: ValueError is raised matching the escaped literal message.
    """
    # --- Arrange ---
    negative_radius = -fake.pyfloat(min_value=0.1, max_value=100.0, positive=True)
    literal_fragment = re.escape(f"{NEGATIVE_RADIUS_MESSAGE}: {negative_radius}")

    # --- Act ---
    with pytest.raises(ValueError, match=literal_fragment):
        Circle(radius=negative_radius)

    # --- Assert ---
    # Exception raised as expected; assertion handled by pytest.raises context.
```

**Variety booster:** Combine `match` with `@pytest.mark.parametrize` to exercise many invalid inputs that share the same exception message pattern, or use `re.escape` to tighten literal-string matches when the message contains dynamic values.

## Deep Inspection with `ExceptionInfo`

[ref: #exceptions-exc-info]

```python
from typing import Any

import pytest
from faker import Faker


QUANTITY_FIELD = "quantity"
INTEGER_REASON = "must be an integer"


class ValidationError(Exception):
    def __init__(self, field: str, value: Any, reason: str) -> None:
        super().__init__(f"invalid {field}: {value!r} ({reason})")
        self.field = field
        self.value = value
        self.reason = reason


class BatchProcessor:
    def process(self, items: list[dict[str, Any]]) -> None:
        for item in items:
            if not isinstance(item.get(QUANTITY_FIELD), int):
                raise ValidationError(QUANTITY_FIELD, item.get(QUANTITY_FIELD), INTEGER_REASON)


def test_validation_error_exposes_attributes(fake: Faker) -> None:
    """
    Given: a batch item with a non-integer quantity.
    When: the batch is processed.
    Then: a ValidationError with the expected attributes is raised.
    """
    # --- Arrange ---
    bad_value = fake.word()
    items = [{"id": fake.uuid4(), QUANTITY_FIELD: bad_value}]

    # --- Act ---
    with pytest.raises(ValidationError) as exc_info:
        BatchProcessor().process(items)

    # --- Assert ---
    assert exc_info.type is ValidationError
    assert exc_info.value.field == QUANTITY_FIELD
    assert exc_info.value.value == bad_value
    assert INTEGER_REASON in exc_info.value.reason
```

**Variety booster:** Assert on both the exception type and one structural invariant (e.g., a custom attribute or `args`) in the same test, then parametrize the input shape so the same inspection logic covers multiple failure modes.

## Parametrized Exception Tests

[ref: #exceptions-parametrize]

```python
from typing import Any

import pytest
from faker import Faker


MIN_PORT = 0
MAX_PORT = 65535
INVALID_PORT_MESSAGE = "invalid port"
PORT_OUT_OF_RANGE_MESSAGE = "port out of range"


class PortParser:
    def parse(self, value: Any) -> int:
        try:
            port = int(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{INVALID_PORT_MESSAGE}: {value!r}") from exc
        if not MIN_PORT <= port <= MAX_PORT:
            raise ValueError(f"{PORT_OUT_OF_RANGE_MESSAGE}: {port}")
        return port


@pytest.mark.parametrize(
    "case",
    [
        pytest.param("negative", id="negative"),
        pytest.param("above_max", id="above_max"),
        pytest.param("non_numeric", id="non_numeric"),
        pytest.param("none", id="none"),
    ],
)
def test_parse_port_rejects_invalid_values(case: str, fake: Faker) -> None:
    """
    Given: a parametrized invalid port case.
    When: the port parser attempts to parse it.
    Then: ValueError is raised with the matching message pattern.
    """
    # --- Arrange ---
    invalid_value: Any
    match_pattern: str

    if case == "negative":
        invalid_value = -fake.pyint(min_value=1, max_value=MAX_PORT)
        match_pattern = PORT_OUT_OF_RANGE_MESSAGE
    elif case == "above_max":
        invalid_value = fake.pyint(min_value=MAX_PORT + 1, max_value=70000)
        match_pattern = PORT_OUT_OF_RANGE_MESSAGE
    elif case == "non_numeric":
        invalid_value = fake.word()
        match_pattern = INVALID_PORT_MESSAGE
    else:
        invalid_value = None
        match_pattern = INVALID_PORT_MESSAGE

    # --- Act ---
    with pytest.raises(ValueError, match=match_pattern):
        PortParser().parse(invalid_value)

    # --- Assert ---
    # Exception raised as expected; assertion handled by pytest.raises context.
```

**Variety booster:** Vary the parametrized label set to include edge cases such as boundary values, malformed types, and empty inputs, and reuse the same assertion body so adding a new failure mode only requires a new label.

## `pytest.deprecated_call` and `pytest.warns`

[ref: #exceptions-warnings]

```python
import warnings

import pytest
from faker import Faker


DEPRECATION_MESSAGE = "fetch_data is deprecated, use fetch_data_v2"
RATE_LIMIT_THRESHOLD = 10
THRESHOLD_EXCEEDED_MESSAGE = "exceeds threshold"


class LegacyApi:
    def fetch_data(self) -> str:
        warnings.warn(DEPRECATION_MESSAGE, DeprecationWarning, stacklevel=2)
        return "legacy-data"


class RateLimitWarning(UserWarning):
    pass


class ThrottledApi:
    def call(self, burst_size: int) -> None:
        if burst_size > RATE_LIMIT_THRESHOLD:
            warnings.warn(
                f"burst size {burst_size} {THRESHOLD_EXCEEDED_MESSAGE}",
                RateLimitWarning,
                stacklevel=2,
            )


def test_legacy_api_emits_deprecation_warning() -> None:
    """
    Given: a legacy API instance.
    When: a deprecated method is called.
    Then: a deprecation warning is emitted and a result is returned.
    """
    # --- Arrange ---
    api = LegacyApi()

    # --- Act ---
    with pytest.deprecated_call():
        result = api.fetch_data()

    # --- Assert ---
    assert result is not None


def test_throttled_api_emits_specific_warning(fake: Faker) -> None:
    """
    Given: a burst size above the rate-limit threshold.
    When: the throttled API is called.
    Then: a RateLimitWarning with the expected message is emitted.
    """
    # --- Arrange ---
    burst_size = fake.pyint(min_value=RATE_LIMIT_THRESHOLD + 1, max_value=100)

    # --- Act ---
    with pytest.warns(RateLimitWarning, match=THRESHOLD_EXCEEDED_MESSAGE):
        ThrottledApi().call(burst_size=burst_size)

    # --- Assert ---
    # Warning emitted as expected; assertion handled by pytest.warns context.
```

**Variety booster:** Parametrize the warning payload and the matching regex so one `pytest.warns` block covers multiple message variants, or combine `pytest.deprecated_call` with the `recwarn` fixture to assert the exact deprecation message when the warning class is generic.

## `@pytest.mark.xfail(raises=...)` vs `pytest.raises`

[ref: #exceptions-xfail]

```python
import pytest
from faker import Faker


class IntegerParser:
    def parse(self, value: str) -> int:
        return int(value)


def test_parse_int_rejects_non_numeric_input(fake: Faker) -> None:
    """
    Given: a non-numeric string input.
    When: the integer parser attempts to parse it.
    Then: ValueError is raised with an invalid literal message.
    """
    # --- Arrange ---
    invalid_input = fake.word()

    # --- Act ---
    with pytest.raises(ValueError, match="invalid literal"):
        IntegerParser().parse(invalid_input)

    # --- Assert ---
    # Exception raised as expected; assertion handled by pytest.raises context.


@pytest.mark.xfail(
    raises=ValueError,
    reason="bug #123: non-numeric input should raise ParseError instead of ValueError",
)
def test_parse_int_non_numeric_raises_parse_error_not_value_error(fake: Faker) -> None:
    """
    Given: a non-numeric string input.
    When: the integer parser attempts to parse it.
    Then: the known bug causes ValueError instead of ParseError.
    """
    # --- Arrange ---
    invalid_input = fake.word()

    # --- Act ---
    IntegerParser().parse(invalid_input)

    # --- Assert ---
    # Expected failure documented by xfail marker.
```

**Variety booster:** Pair `xfail(raises=...)` with a linked issue number in the reason string, and add a `pytest.raises` test for the current behavior so the suite documents both the present reality and the intended contract.

## Common Anti-Patterns

[ref: #exceptions-anti-patterns]

Avoid these patterns because they reduce confidence, hide real bugs, or make failures harder to diagnose.

| Anti-pattern | Why it is harmful | Preferred alternative |
|---|---|---|
| `match=".*"` | Matches any message, masking unintended exceptions. | Use a specific message fragment or `re.escape`. |
| Asserting `exc_info.typename` | `typename` is a string and is informational; `type is` is precise. | `assert exc_info.type is ExpectedException`. |
| Catching broad `Exception` in `pytest.raises` | Hides real bugs and makes failures harder to diagnose. | Catch the exact expected exception type. |
| Legacy `pytest.raises(Exc, func, *args, **kwargs)` | Less readable and harder to extend with additional assertions. | Use the context-manager form `with pytest.raises(Exc):`. |
| `except:` or `except Exception:` in production code | Swallows unexpected errors and violates explicit exception handling. | Catch specific exception types and re-raise or handle appropriately. |

```python
import pytest
from faker import Faker


def risky_operation(x: int) -> None:
    if x < 0:
        raise ValueError("negative input")
    if x == 0:
        raise RuntimeError("zero input")


def test_risky_operation_bad_broad_match(fake: Faker) -> None:
    """
    Given: a negative input to a risky operation.
    When: the operation is called.
    Then: the anti-pattern broad match is shown.
    """
    # --- Arrange ---
    x = -fake.pyint(min_value=1, max_value=100)

    # --- Act ---
    # BAD — match=".*" would also pass if RuntimeError were raised.
    with pytest.raises(ValueError, match=".*"):
        risky_operation(x)

    # --- Assert ---
    # Anti-pattern demonstration; broad match masks unintended exceptions.


def test_risky_operation_good_specific_match(fake: Faker) -> None:
    """
    Given: a negative input to a risky operation.
    When: the operation is called.
    Then: ValueError with the specific message is raised.
    """
    # --- Arrange ---
    x = -fake.pyint(min_value=1, max_value=100)

    # --- Act ---
    with pytest.raises(ValueError, match="negative input"):
        risky_operation(x)

    # --- Assert ---
    # Exception raised as expected; assertion handled by pytest.raises context.
```

**Variety booster:** For every exception test, ask whether a more specific assertion (type, `match`, or attribute) would catch a regression; if the current assertion would pass for multiple unrelated failures, tighten it before moving on.

## Advanced: `ExceptionGroup` Assertions

[ref: #exceptions-exception-group]

```python
import pytest
from faker import Faker


GROUP_MESSAGE = "validation failed"


def raise_group_with_validation_errors(messages: list[str]) -> None:
    raise ExceptionGroup(
        GROUP_MESSAGE,
        [ValueError(messages[0]), TypeError(messages[1])],
    )


def test_exception_group_contains_expected_errors(fake: Faker) -> None:
    """
    Given: a list of validation error messages.
    When: an ExceptionGroup is raised from those messages.
    Then: the group contains the expected ValueError and TypeError.
    """
    # --- Arrange ---
    email_message = fake.sentence()
    age_message = fake.sentence()

    # --- Act ---
    with pytest.raises(ExceptionGroup, match=GROUP_MESSAGE) as exc_info:
        raise_group_with_validation_errors([email_message, age_message])

    # --- Assert ---
    exceptions = exc_info.value.exceptions
    assert len(exceptions) == 2
    assert isinstance(exceptions[0], ValueError)
    assert str(exceptions[0]) == email_message
    assert isinstance(exceptions[1], TypeError)
    assert str(exceptions[1]) == age_message
```

**Variety booster:** When testing exception groups, parametrize the set of expected inner exception types and messages, and reuse a single helper that builds the assertion list from the captured group.
