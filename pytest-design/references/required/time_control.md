---
subject: "Make time-dependent tests deterministic instead of relying on real time: pin with `@time_machine.travel(destination, tick=True)`, use the `time_machine` fixture/`Traveller` (`move_to`/`shift`), class/module `pytestmark = pytest.mark.time_machine(...)`, choose `tick=True`/`False`, set `naive_mode = NaiveMode.ERROR` in `conftest.py`, timezone-aware datetimes, `freezegun` legacy fallback, `pytest-timeout` safety net, injectable `Clock` Protocol."
index:
  - anchor: time-control-decorator
    what: "`@time_machine.travel(destination, tick=True)` pins an entire test to a single fixed timestamp."
    problem: "Test needing one fixed moment must not depend on real clock or on time progressing; single frozen moment, no real clock, decorator pin, no progress, multi-jump fixture, destination fixed."
    use_when: "Test needs one fixed moment, system reads clock but time must not progress, and decorator pins destination without real clock; single frozen moment, no real clock, decorator pin, no progress, multi jump fixture, destination fixed."
    avoid_when: "Do not stack multiple decorators on the same function to simulate time jumps — use the `time_machine` fixture or context manager instead."
    expected: "The test runs at a single frozen destination with no real-clock dependence; multi-jump scenarios use the fixture."
  - anchor: time-control-fixture
    what: "The `time_machine` fixture yields a `Traveller` for the current test, enabling multiple jumps and relative shifts inside one function."
    problem: "Scenarios like token expiry or retry backoff need clock to advance within test without real-time delays; advance inside test, traveller, instantaneous shift, token expiry, backoff window, no real sleep."
    use_when: "Token expiry or retry backoff needs clock advancement inside test, real time delays would flake, and traveller shifts instantly; advance inside test, traveller, instantaneous shift, token expiry, backoff window, no real sleep."
    avoid_when: "Do not use it to simulate real-time delays — shift the clock instantaneously."
    expected: "Time advances via instantaneous shifts inside the test; no real-time sleeps."
  - anchor: time-control-marker
    what: "`pytest.mark.time_machine(destination)` (or module `pytestmark`) freezes every test in a class/module at one moment without repeating the decorator."
    problem: "Date-driven suites need shared frozen moment without per-test decorator repetition; class module freeze, one moment, date-driven rules, no repeat, one pinning mechanism, marker pin."
    use_when: "Date driven suite needs shared frozen moment, per test decorator repetition is wasteful, and marker pins whole class or module; class module freeze, one moment, date driven rules, no repeat, one pinning mechanism, marker pin."
    avoid_when: "Do not mix the marker with per-test decorators that conflict on the same function — choose one pinning mechanism per test."
    expected: "One pinning mechanism per test; class/module-wide freeze via marker, per-test jumps via fixture."
  - anchor: time-control-traveller
    what: "A `Traveller` jumps to an absolute time with `move_to()` or advances by a relative delta with `shift()`."
    problem: "Tests need both absolute calendar boundaries and relative intervals, applied with consistent units; move_to absolute, shift relative, consistent units, calendar boundary, interval, no mixed units."
    use_when: "Test needs absolute calendar boundary and relative interval, mixed units confuse expectation, and traveller move_to plus shift keeps units consistent; move_to absolute, shift relative, consistent units, calendar boundary, interval, no mixed units."
    avoid_when: "Do not mix units such as raw seconds and `timedelta` inconsistently within the same test."
    expected: "Absolute jumps use `move_to()`, relative advances use `shift()`, with consistent units throughout the test."
  - anchor: time-control-tick
    what: "`tick=True` lets the mocked clock advance naturally from the destination; `tick=False` freezes it completely."
    problem: "Some code needs monotonic or short timeouts to progress, while other assertions need absolutely stable timestamp; tick progress, freeze stable, monotonic, short timeout, no wall-clock measure, match expectation."
    use_when: "Code needs monotonic or short timeout progression, another assertion needs absolutely stable timestamp, and tick choice matches expectation per scenario; tick progress, freeze stable, monotonic, short timeout, no wall clock measure, match expectation."
    avoid_when: "Never rely on `tick=True` to measure real wall-clock durations."
    expected: "Ticking is chosen to match the code's clock expectations; no wall-clock duration is measured via `tick=True`."
  - anchor: time-control-naive-mode
    what: "`time_machine.naive_mode` controls how destinations without tzinfo are interpreted; set to `NaiveMode.ERROR` in `conftest.py` to enforce timezone-aware datetimes."
    problem: "Naive datetimes silently inherit ambiguous local interpretations; error on naive, conftest set, timezone-aware enforce, ambiguous local, runtime error, explicit tzinfo."
    use_when: "Naive datetimes inherit ambiguous local interpretation, timezone aware enforcement must catch them, and conftest error mode sets policy; error on naive, conftest set, timezone aware enforce, ambiguous local, runtime error, explicit tzinfo."
    avoid_when: "Never leave naive datetimes in assertions."
    expected: "Naive destinations raise `RuntimeError`; all test datetimes are timezone-aware."
  - anchor: time-control-timezone-aware
    what: "All datetime values in tests carry an explicit `tzinfo` (`datetime.UTC`, `zoneinfo.ZoneInfo`, or `datetime.timezone.utc`)."
    problem: "Naive and aware mixing and now without timezone produce ambiguous, non-portable assertions; explicit tzinfo, utc zoneinfo, no naive aware mix, now with tz, portable, aware everywhere."
    use_when: "Naive and aware datetimes mix, now without timezone produces non portable assertion, and explicit tzinfo everywhere keeps portable time; explicit tzinfo, utc zoneinfo, no naive aware mix, now with tz, portable, aware everywhere."
    avoid_when: "Do not assert equality between naive and aware datetimes, and never trust `datetime.now()` without a timezone argument."
    expected: "Every datetime in assertions is explicitly timezone-aware; no naive/aware mixing."
  - anchor: time-control-freezegun
    what: "Use `freezegun` only as a legacy fallback or compatibility bridge when `time-machine` cannot be installed or the codebase already depends on it; prefer `time-machine` for new tests."
    problem: "Defaulting to freezegun for new code locks in slower older mocking approach and risks event-loop stalls; legacy bridge, tick false, real async, modern mocker preferred, compatibility, not default new."
    use_when: "New code defaults to freezegun, slower older mocking approach locks in, and time-machine stays preferred unless compatibility requires fallback; legacy bridge, tick false, real async, modern mocker preferred, compatibility, not default new."
    avoid_when: "Do not choose `freezegun` for new tests when `time-machine` is available."
    expected: "`freezegun` appears only as a documented bridge with `tick=False, real_asyncio=True`; new tests use `time-machine`."
  - anchor: time-control-pytest-timeout
    what: "`pytest-timeout` is a safety net against hanging tests (infinite loops, deadlocks, accidental real-time waits), not a timing assertion."
    problem: "Using timeout values to assert timing behavior is flaky; clock mocking is correct tool for timing; hang guardrail, infinite loop, deadlock, accidental wait, not timing assert, mock clock."
    use_when: "Timeout value is used to assert timing behavior, that flakes, and timeout should only guard hangs while clock mocking checks timing; hang guardrail, infinite loop, deadlock, accidental wait, not timing assert, mock clock."
    avoid_when: "Do not use timeout values as the primary way to assert timing behavior — mock the clock instead."
    expected: "Timeouts act purely as hang guardrails; all timing behavior is asserted via mocked clocks."
  - anchor: time-control-clock-provider
    what: "Inject a `Clock` protocol/fake (e.g., `FixedClock`) into components so tests use a fully deterministic fake clock without global side effects, instead of mocking global time."
    problem: "Mocking global time across many components creates global side effects and brittle tests; inject clock protocol, deterministic fake, no global side effect, fixed clock, complex system, trivial use travel."
    use_when: "Global time mocking across many components creates side effects and brittle tests, injected clock protocol gives deterministic fake without global mutation; inject clock protocol, deterministic fake, no global side effect, fixed clock, complex system, trivial use travel."
    avoid_when: "Avoid it for trivial one-off datetime checks where `time-machine` is simpler and less invasive."
    expected: "Complex systems take an injected fake clock; trivial checks use `time-machine`; no global time mocking."
libraries:
  - freezegun
  - pytest-timeout
  - time-machine
---

# TIME CONTROL

## time-machine decorator

[ref: #time-control-decorator]

The decorator is the most compact way to pin an entire test to a single destination timestamp.

```python
from datetime import UTC, timedelta

import pytest
import time_machine
from faker import Faker


TRAVEL_DESTINATION_UTC = "2024-01-15T12:00:00+00:00"
SUBSCRIPTION_START_OFFSET = timedelta(days=-365)
SUBSCRIPTION_END_OFFSET = timedelta(days=-30)
MIN_ACTIVE_DAYS_AHEAD = timedelta(days=1)
MAX_ACTIVE_DAYS_AHEAD = timedelta(days=365)


@pytest.fixture
def expired_subscription(fake: Faker) -> Subscription:
    return Subscription(
        expires_at=fake.date_time_between(
            start_date=SUBSCRIPTION_START_OFFSET,
            end_date=SUBSCRIPTION_END_OFFSET,
            tzinfo=UTC,
        ),
    )


@time_machine.travel(TRAVEL_DESTINATION_UTC, tick=True)
def test_expired_subscription_is_reported_as_expired(
    expired_subscription: Subscription,
) -> None:
    """
    Given: an expired subscription fixture under a frozen UTC timestamp.
    When: expiration is checked.
    Then: it is reported as expired.
    """
    # --- Arrange ---
    # Subscription provided by fixture.

    # --- Act ---
    result = expired_subscription.is_expired()

    # --- Assert ---
    assert result is True


@time_machine.travel(TRAVEL_DESTINATION_UTC, tick=True)
def test_active_subscription_is_not_expired(fake: Faker) -> None:
    """
    Given: an active subscription created under a frozen UTC timestamp.
    When: expiration is checked.
    Then: it is reported as not expired.
    """
    # --- Arrange ---
    subscription = Subscription(
        expires_at=fake.date_time_between(
            start_date=MIN_ACTIVE_DAYS_AHEAD,
            end_date=MAX_ACTIVE_DAYS_AHEAD,
            tzinfo=UTC,
        ),
    )

    # --- Act ---
    result = subscription.is_expired()

    # --- Assert ---
    assert result is False
```

**Variety booster:** Combine the decorator with `@pytest.mark.parametrize` to exercise boundary dates such as leap-year day, month-end, and DST transitions without duplicating test bodies.

## time-machine fixture

[ref: #time-control-fixture]

The `time_machine` fixture gives you a `Traveller` instance for the current test, enabling multiple jumps and relative shifts in a single function.

```python
from datetime import UTC, timedelta

import pytest
from faker import Faker
from time_machine import Traveller


TOKEN_LIFETIME_SECONDS = 300
TOKEN_EARLY_REFRESH_WINDOW = timedelta(seconds=60)
TOKEN_EXPIRY_TOLERANCE = timedelta(seconds=2)


def test_access_token_refreshes_after_expiry(
    fake: Faker,
    time_machine: Traveller,
) -> None:
    """
    Given: access token issued for a generated user.
    When: clock shifts through expiry and token is refreshed.
    Then: validity follows the timeline and refreshed token belongs to user.
    """
    # --- Arrange ---
    user = fake.fake_email()
    token = issue_access_token(user, lifetime_seconds=TOKEN_LIFETIME_SECONDS)

    # --- Act ---
    initial_valid = token.is_valid()

    # --- Assert ---
    assert initial_valid is True

    # --- Act ---
    time_machine.shift(timedelta(seconds=TOKEN_LIFETIME_SECONDS - 1))
    near_expiry_valid = token.is_valid()

    # --- Assert ---
    assert near_expiry_valid is True

    # --- Act ---
    time_machine.shift(TOKEN_EXPIRY_TOLERANCE)
    expired_valid = token.is_valid()

    # --- Assert ---
    assert expired_valid is False

    # --- Act ---
    refreshed = token.refresh()

    # --- Assert ---
    assert refreshed.is_valid() is True
    assert refreshed.issued_to == user


def test_refresh_window_allows_early_rotation(
    fake: Faker,
    time_machine: Traveller,
) -> None:
    """
    Given: access token issued for a generated user.
    When: clock shifts into the early-refresh window.
    Then: token reports it can be refreshed.
    """
    # --- Arrange ---
    token = issue_access_token(
        fake.fake_email(),
        lifetime_seconds=TOKEN_LIFETIME_SECONDS,
    )

    # --- Act ---
    time_machine.shift(TOKEN_EARLY_REFRESH_WINDOW)

    # --- Assert ---
    assert token.can_refresh() is True
```

**Variety booster:** Extract a parametrized fixture that yields several `(lifetime, shift, expected_valid)` tuples, then assert the token state after each shift to cover edge cases with one test body.

## time-machine pytest marker

[ref: #time-control-marker]

The pytest marker applies the travel destination to every test in a class or module without repeating the decorator.

```python
from datetime import UTC, timedelta

import pytest


INVOICE_DUE_DAYS = 30
TRAVEL_DESTINATION_UTC = "2024-03-01T00:00:00+00:00"
ISSUE_DATE_START_OFFSET = timedelta(days=-365)
ISSUE_DATE_END_OFFSET = timedelta(days=-1)


pytestmark = pytest.mark.time_machine(TRAVEL_DESTINATION_UTC)


def test_invoice_is_due_on_due_date(fake: Faker) -> None:
    """
    Given: invoice issued before the frozen timestamp and due in 30 days.
    When: due status is checked.
    Then: invoice is reported as due.
    """
    # --- Arrange ---
    invoice = Invoice(
        issued_at=fake.date_time_between(
            start_date=ISSUE_DATE_START_OFFSET,
            end_date=ISSUE_DATE_END_OFFSET,
            tzinfo=UTC,
        ),
        due_in_days=INVOICE_DUE_DAYS,
    )

    # --- Act ---
    result = invoice.is_due()

    # --- Assert ---
    assert result is True
```

**Variety booster:** Define a module-level `pytestmark` with the frozen date for default cases, then override individual tests with the `time_machine` fixture when they need to jump forward.

## Traveller shift and move_to

[ref: #time-control-traveller]

A `Traveller` instance lets you jump to a new absolute time with `move_to()` or advance by a relative delta with `shift()`.

```python
from datetime import timedelta

from faker import Faker
from time_machine import Traveller


BILLING_ANCHOR_UTC = "2024-01-01T00:00:00+00:00"
MONTH_END_UTC = "2024-01-31T23:59:59+00:00"
MONTHLY_GRACE_PERIOD = timedelta(days=3)
LATE_FEE_DELAY = timedelta(hours=1)


def test_monthly_invoice_transitions_through_grace_period(
    fake: Faker,
    time_machine: Traveller,
) -> None:
    """
    Given: monthly invoice generated at the billing anchor.
    When: clock moves through month-end, grace period, and late-fee delay.
    Then: status transitions from open to overdue and late fee is applied.
    """
    # --- Arrange ---
    account = fake.uuid4()
    invoice = generate_monthly_invoice(account, anchor=BILLING_ANCHOR_UTC)

    # --- Act ---
    initial_status = invoice.status

    # --- Assert ---
    assert initial_status == InvoiceStatus.OPEN

    # --- Act ---
    time_machine.move_to(MONTH_END_UTC)
    after_due_status = invoice.status

    # --- Assert ---
    assert after_due_status == InvoiceStatus.OVERDUE

    # --- Act ---
    time_machine.shift(MONTHLY_GRACE_PERIOD)
    after_grace_status = invoice.status

    # --- Assert ---
    assert after_grace_status == InvoiceStatus.OVERDUE

    # --- Act ---
    time_machine.shift(LATE_FEE_DELAY)

    # --- Assert ---
    assert invoice.late_fee_applied is True
```

**Variety booster:** Parameterize the destination format by passing ISO strings, `datetime` objects, and `zoneinfo.ZoneInfo` destinations to `move_to()` in different tests to document supported inputs.

## tick=True vs tick=False

[ref: #time-control-tick]

`tick=True` lets the mocked clock advance naturally from the destination, while `tick=False` freezes it completely.

```python
from datetime import timedelta

from faker import Faker
from time_machine import Traveller


CACHE_TTL_SECONDS = 2
CACHE_SHIFT_TOLERANCE = timedelta(seconds=1)
TRAVEL_DESTINATION_UTC = "2024-06-01T12:00:00+00:00"


def test_cache_entry_expires_after_ttl_with_ticking_clock(
    fake: Faker,
    time_machine: Traveller,
) -> None:
    """
    Given: cache entry with a short TTL under a ticking frozen clock.
    When: value is set and clock shifts past TTL.
    Then: entry is present before expiry and absent after.
    """
    # --- Arrange ---
    key = fake.uuid4()
    value = fake.sentence()
    cache = Cache(ttl_seconds=CACHE_TTL_SECONDS)

    # --- Act ---
    cache.set(key, value)

    # --- Assert ---
    assert cache.get(key) == value

    # --- Act ---
    time_machine.shift(timedelta(seconds=CACHE_TTL_SECONDS) + CACHE_SHIFT_TOLERANCE)

    # --- Assert ---
    assert cache.get(key) is None
```

**Variety booster:** Write a parametrized test that runs the same scenario with both `tick=True` and `tick=False` to document where each behavior matters, or assert that `datetime.now(UTC)` changes between two reads when ticking is enabled.

## time_machine.naive_mode

[ref: #time-control-naive-mode]

`time_machine.naive_mode` controls how destinations without tzinfo are interpreted.

```python
from datetime import datetime

import pytest
import time_machine
from faker import Faker


NAIVE_DESTINATION = datetime(2024, 1, 15, 12, 0, 0)


def test_naive_mode_error_rejects_awareness_lapse(
    monkeypatch: pytest.MonkeyPatch,
    fake: Faker,
) -> None:
    """
    Given: naive_mode is patched to ERROR for the test scope.
    When: time_machine.travel receives a naive datetime.
    Then: RuntimeError is raised.
    """
    # --- Arrange ---
    monkeypatch.setattr(time_machine, "naive_mode", time_machine.NaiveMode.ERROR)

    # --- Act ---
    with pytest.raises(RuntimeError):
        with time_machine.travel(NAIVE_DESTINATION):
            pass

    # --- Assert ---
    # Exception raised as expected; assertion handled by pytest.raises context.
```

**Variety booster:** Configure `naive_mode` globally per test run and add a regression test that asserts the configured mode rejects naive input, so new team members cannot accidentally introduce ambiguous datetimes.

## Timezone-aware datetimes

[ref: #time-control-timezone-aware]

All datetime values in tests must carry an explicit tzinfo.

```python
from datetime import UTC

import pytest
from faker import Faker
from zoneinfo import ZoneInfo


EXPECTED_ZONES = ["UTC", "America/New_York", "Europe/London", "Asia/Tokyo"]


@pytest.mark.parametrize("zone_name", EXPECTED_ZONES)
def test_event_timestamp_preserves_timezone(
    zone_name: str,
    fake: Faker,
) -> None:
    """
    Given: event datetime generated in a parametrized timezone.
    When: calendar event is created.
    Then: timezone and offset are preserved.
    """
    # --- Arrange ---
    tz = ZoneInfo(zone_name)
    event_at = fake.date_time(tzinfo=tz)

    # --- Act ---
    event = CalendarEvent(title=fake.sentence(), scheduled_at=event_at)

    # --- Assert ---
    assert event.scheduled_at.tzinfo is not None
    assert event.scheduled_at.utcoffset() is not None
    assert event.scheduled_at == event_at
```

**Variety booster:** Parametrize over a representative set of timezones including DST and non-DST offsets, and add a test that converts the same instant to multiple zones to verify offset math.

## freezegun legacy fallback

[ref: #time-control-freezegun]

Use `freezegun` only when `time-machine` cannot be installed or the codebase already depends on it.

```python
from datetime import UTC, timedelta

from faker import Faker
from freezegun import freeze_time


TRAVEL_DESTINATION_UTC = "2024-01-15T12:00:00+00:00"
FREEZEGUN_START_OFFSET = "-2y"
FREEZEGUN_END_OFFSET = "-1y"
SHIFT_SECONDS = 300


@freeze_time(TRAVEL_DESTINATION_UTC, tick=False, real_asyncio=True)
def test_legacy_subscription_expiry_with_freezegun(
    fake: Faker,
) -> None:
    """
    Given: expired subscription under freezegun with ticking disabled.
    When: expiration is checked.
    Then: it is reported as expired.
    """
    # --- Arrange ---
    subscription = Subscription(
        expires_at=fake.date_time_between(
            start_date=FREEZEGUN_START_OFFSET,
            end_date=FREEZEGUN_END_OFFSET,
            tzinfo=UTC,
        ),
    )

    # --- Act ---
    result = subscription.is_expired()

    # --- Assert ---
    assert result is True


@freeze_time(TRAVEL_DESTINATION_UTC, tick=False, real_asyncio=True)
def test_legacy_token_refresh_with_freezegun_tick(
    fake: Faker,
) -> None:
    """
    Given: token issued under frozen freezegun time.
    When: clock ticks forward by a fixed delta.
    Then: shifted timestamp is later than the original issued-at time.
    """
    # --- Arrange ---
    token = issue_access_token(fake.fake_email())
    issued_at_before_shift = token.issued_at

    # --- Act ---
    with freeze_time() as frozen:
        frozen.tick(delta=timedelta(seconds=SHIFT_SECONDS))
        now_after_shift = token.issued_at + timedelta(seconds=SHIFT_SECONDS)

    # --- Assert ---
    assert issued_at_before_shift < now_after_shift
```

**Variety booster:** Keep a single migration test that verifies `freezegun` and `time-machine` produce the same mocked instant for the same destination, making it safe to remove `freezegun` later.

## pytest-timeout hang protection

[ref: #time-control-pytest-timeout]

`pytest-timeout` is a safety net against hanging tests, not a substitute for clock mocking.

Configuration precedence from lowest to highest is: config file / `PYTEST_TIMEOUT` env var / `--timeout` CLI option / `@pytest.mark.timeout()` marker.

```python
import pytest
from faker import Faker
from time_machine import Traveller


def test_slow_operation_completes_under_guardrail(
    fake: Faker,
    time_machine: Traveller,
) -> None:
    """
    Given: batch processor with a one-second timeout under mocked time.
    When: processor runs.
    Then: it reports completion.
    """
    # --- Arrange ---
    processor = BatchProcessor(timeout_seconds=1)

    # --- Act ---
    result = processor.run()

    # --- Assert ---
    assert result.completed is True
```

```toml
[tool.pytest.ini_options]
timeout = 30
timeout_method = "thread"
```

```python
# Per-test override
@pytest.mark.timeout(10, method="signal")
def test_critical_path_must_not_hang() -> None:
    """
    Given: critical path under test.
    When: it runs.
    Then: it completes before timeout.
    """
    ...
```

**Variety booster:** Combine a short `pytest-timeout` marker with `time_machine` fixture shifts to prove that the code reacts to clock advancement before the timeout fires.

## Clock Provider pattern

[ref: #time-control-clock-provider]

For complex systems, inject a clock protocol instead of mocking global time.

```python
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Protocol

import pytest
from faker import Faker


class Clock(Protocol):
    def now(self) -> datetime: ...


@dataclass
class FixedClock:
    frozen_at: datetime

    def now(self) -> datetime:
        return self.frozen_at

    def shift(self, delta: timedelta) -> None:
        self.frozen_at += delta


SCHEDULE_OFFSET = timedelta(minutes=5)
SHIFT_PAST_DUE = timedelta(minutes=6)


@pytest.fixture
def fixed_clock(fake: Faker) -> FixedClock:
    return FixedClock(frozen_at=fake.date_time(tzinfo=UTC))


def test_scheduler_fires_at_expected_time(
    fixed_clock: FixedClock,
    fake: Faker,
) -> None:
    """
    Given: scheduler backed by a fixed fake clock.
    When: task is scheduled and clock shifts past its due time.
    Then: task appears in due tasks.
    """
    # --- Arrange ---
    scheduler = Scheduler(clock=fixed_clock)
    task = fake.sentence()

    # --- Act ---
    scheduler.schedule(task, at=fixed_clock.now() + SCHEDULE_OFFSET)
    fixed_clock.shift(SHIFT_PAST_DUE)

    # --- Assert ---
    assert scheduler.due_tasks() == [task]
```

**Variety booster:** Implement `OffsetClock`, `SequenceClock`, or `SpeedClock` variants to simulate drift, replay a list of instants, or run the suite at accelerated speed.
