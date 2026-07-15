---
subject: "Extend plain `assert` for awkward comparisons; soft assertions via `pytest-check`, order-agnostic collection equality via `pytest-unordered`, flexible shape and value matchers via `dirty-equals`, per-input failure reporting via `pytest-subtests`, version-controlled output baselines via `pytest-regressions`."
index:
  - anchor: assertion-plugins-pytest-check
    what: "Soft assertions via the `check` context manager and `check.*` helpers from `pytest-check` that register every failed check inside one test and report them together at teardown."
    problem: "Several independent assertions live in one test, but plain `assert` aborts at first mismatch and hides every later failure; grouped checks, batch validation, non-stopping asserts, single logical state, hidden defects, independent invariants."
    use_when: "Asserting several independent properties of one object or state; every failure must surface in the same run; checks belong to one logical invariant set."
    avoid_when: "Unrelated behaviors bundled into one test — split those into focused tests or parametrize inputs instead."
    expected: "One run surfaces every failed check at once, so no defect hides behind an earlier failure."
  - anchor: assertion-plugins-pytest-unordered
    what: "Order-agnostic comparison via `unordered(expected)` that checks membership and multiplicity of ordered collections without enforcing element position."
    problem: "Query or API result collection arrives in non-deterministic order across runs, yet every expected element must be present with exact occurrence count and duplicates carry meaning; naive sequence equality flakes whenever backend shuffles rows; order-insensitive compare, unhashable elements, multiset equality, permutation tolerance, collection invariant."
    use_when: "Collection arrangement varies across runs or is unspecified by contract; repeated occurrences carry meaning; equality must ignore arrangement but not content."
    avoid_when: "Element order is part of the contract under test — order-agnostic comparison silently accepts wrongly ordered results."
    expected: "Results pass for any permutation of expected content while missing or extra occurrences still fail the test."
  - anchor: assertion-plugins-dirty-equals
    what: "Composable matchers from `dirty-equals` (`IsPartialDict`, `IsStr(regex=...)`, `IsNow`, `IsPositiveInt`) that assert structure, types, and approximate values inside complex objects."
    problem: "Response payload carries auto-generated ids, timestamps, and counters shifting every run, so exact equality over-constrains values outside behavior under test; dynamic fields, structural assertion, type pattern match, contract boundary, partial compare."
    use_when: "Payload field values change between executions while shape and typing stay contractual; only selected fields need exact matching."
    avoid_when: "Exact field values are the behavior under test; approximate matching would weaken the assertion."
    expected: "Payloads validate structurally every time, with only genuinely contractual values pinned exactly."
  - anchor: assertion-plugins-pytest-subtests
    what: "The `subtests` fixture that runs the same assertion body against many inputs inside one test and reports each failure individually via `subtests.test(msg=..., **context)`."
    problem: "One assertion body must run against many inputs produced only at runtime, with each failure reported alone and expensive shared setup executing once per run; per-input failure, dynamic case set, loop-level reporting, subtest isolation, costly arrangement reuse."
    use_when: "Case set is known only at runtime; preparing common state costs too much to redo per input; every input needs its own report entry and context."
    avoid_when: "Static, independent inputs — `@pytest.mark.parametrize` gives clearer per-case ids there."
    expected: "Each input failure appears as a separate named entry in one test run, and the costly arrangement executes a single time."
  - anchor: assertion-plugins-pytest-regressions
    what: "Regression testing with the `data_regression` fixture that stores deterministic expected output in git-tracked baselines and compares subsequent runs against them via `data_regression.check(payload)`."
    problem: "Large stable output demands version-controlled baseline instead of verbose hand-written assertion, while random and environment fields must be sanitized before compare; golden baseline, snapshot review, serialized output, deliberate regen, reviewable diff, unstable field masking."
    use_when: "Output is large and stable; hand-writing full expectation would drown test body; run-varying fields can be replaced with stable placeholders ahead of comparison."
    avoid_when: "Small or frequently changing outputs where direct assertion reads clearer; baselines containing raw ids, timestamps, or hostnames; regeneration without reviewing the diff."
    expected: "Baselines live under git as reviewable records of correct output; changes land only through deliberate `--force-regen` with a reviewed diff."
libraries:
  - dirty-equals
  - pytest-check
  - pytest-regressions
  - pytest-subtests
  - pytest-unordered
---

# DATA & ASSERTIONS — EXTENDED

## pytest-check (Soft Assertions)

[ref: #assertion-plugins-pytest-check]

Collect every assertion failure inside a single test and report them all at once instead of stopping at the first mismatch.

```python
from collections.abc import Callable
from datetime import datetime
from typing import Any

from pytest_check import check


def test_created_user_has_all_required_fields(
    new_user: dict[str, Any],
) -> None:
    """
    Given: a newly created user record.
    When: required fields are checked with soft assertions.
    Then: every required field passes its invariant.
    """
    # --- Arrange ---
    # new_user is supplied by the caller's fixture.

    # --- Act ---
    with check:
        assert isinstance(new_user["id"], str)
        assert new_user["status"] is not None
    check.is_in("email", new_user)
    check.is_in("name", new_user)
    check.is_instance(new_user["created_at"], datetime)

    # --- Assert ---
    # All soft assertions are registered above; pytest-check reports them collectively.
```

**Variety booster:** Decorate a reusable multi-field validator with `@check.check_func` and call it from several response-shape tests, or pass `xfail="reason"` to individual helpers when one invariant is temporarily unreliable.

## pytest-unordered (Order-Agnostic Collections)

[ref: #assertion-plugins-pytest-unordered]

Compare ordered collections without enforcing element position when order is not part of the contract.

```python
from collections.abc import Callable
from typing import Any

from faker import Faker
from pytest_unordered import unordered


def test_query_returns_all_created_users(
    user_factory: Callable[..., Any],
    fake: Faker,
) -> None:
    """
    Given: a collection of users created by the factory.
    When: all users are queried.
    Then: the result contains exactly the expected users in any order.
    """
    # --- Arrange ---
    count = fake.pyint(min_value=2, max_value=5)
    expected = [user_factory() for _ in range(count)]

    # --- Act ---
    result = query_all()

    # --- Assert ---
    assert result == unordered(expected)
```

**Variety booster:** Combine with `@pytest.mark.parametrize` to vary the collection size and the factory variant (e.g., active vs. pending users) while keeping the assertion identical.

## dirty-equals (Flexible Shape Matching)

[ref: #assertion-plugins-dirty-equals]

Assert structure, types, regex patterns, and approximate values instead of exact equality inside complex objects.

```python
from datetime import timedelta
from typing import Any

from dirty_equals import IsNow, IsPartialDict, IsPositiveInt, IsStr


def test_api_user_response_matches_shape(existing_user_id: str) -> None:
    """
    Given: an existing user id.
    When: the user is fetched from the API.
    Then: the response matches the expected shape with dynamic fields ignored.
    """
    # --- Arrange ---
    # existing_user_id is supplied by the caller's fixture.

    # --- Act ---
    response = fetch_user(existing_user_id)

    # --- Assert ---
    assert response == IsPartialDict({
        "id": IsStr(regex=r"^usr_[a-z0-9]{12}$"),
        "email": IsStr(regex=r"^.+@example\.(com|org|net)$"),
        "created_at": IsNow(delta=timedelta(seconds=5)),
        "login_count": IsPositiveInt(),
    })
```

**Variety booster:** Compose matchers with `&` and `|` (for example `HasLen(3) & Contains("admin")`) and extract a shared `api_object_shape` dict that you reuse across endpoints with only the field names changed.

## pytest-subtests (Per-Iteration Reporting)

[ref: #assertion-plugins-pytest-subtests]

Run the same assertion body against many inputs inside one test and report each failure individually without stopping at the first.

```python
from typing import Any


def test_all_created_users_have_email(
    subtests: Any,
    users: list[dict[str, Any]],
) -> None:
    """
    Given: a list of created users.
    When: each user is checked for an email address.
    Then: every user has a non-null email reported as a separate subtest.
    """
    # --- Arrange ---
    # users supplied by the caller's fixture.

    # --- Act / Assert ---
    for user in users:
        with subtests.test(msg=f"user-{user['id']}", user=user):
            assert user["email"] is not None
```

**Variety booster:** Build the input collection from a parametrized fixture so the same subtest loop exercises different sizes and content distributions without duplicating the test body.

## pytest-regressions (Deterministic Baselines)

[ref: #assertion-plugins-pytest-regressions]

Store deterministic expected output in version-controlled baselines and compare subsequent runs against them, updating deliberately with `--force-regen`.

```python
from typing import Any


def _sanitize_for_regression(payload: dict[str, Any]) -> dict[str, Any]:
    """Replace unstable fields with stable placeholders for baseline comparison."""
    payload = dict(payload)
    payload["request_id"] = "<request-id>"
    payload["timestamp"] = "<timestamp>"
    return payload


def test_config_endpoint_regression(
    api_client: Any,
    data_regression: Any,
) -> None:
    """
    Given: a running API client.
    When: the config endpoint is requested and sanitized.
    Then: the payload matches the stored regression baseline.
    """
    # --- Arrange ---
    # api_client and data_regression supplied by the caller's fixtures.

    # --- Act ---
    response = api_client.get("/api/config")
    payload = _sanitize_for_regression(response.json())

    # --- Assert ---
    data_regression.check(payload)
```

**Variety booster:** Write a small `_sanitize_for_regression(data)` helper that replaces IDs, timestamps, and hostnames with stable placeholders, then reuse it across every regression test to keep baselines reviewable.
