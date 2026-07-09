---
subject: "Go beyond plain `assert` when one mismatch must not stop the run or data is awkward to compare: soft assertions via `pytest-check`, order-agnostic collections with `pytest-unordered`, flexible shape/value matching with `dirty-equals`, per-iteration failures via `pytest-subtests`, and version-controlled regression baselines with `pytest-regressions`; sanitize unstable fields first."
index:
  - anchor: assertion-plugins-pytest-check
    what: "Soft assertions from pytest-check that collect every assertion failure inside a single test and report them all at once instead of stopping at the first mismatch."
    problem: "Several independent assertions live in one test, but plain `assert` aborts at first mismatch and hides every later failure; grouped checks, soft assertions, multiple failures, collect all errors, non-stopping asserts, batch validation, single logical state."
    use_when: "Several independent checks describe one logical state, every failure must surface together, and first mismatch must not hide later mismatches; grouped checks, soft assertions, multiple failures, collect errors, non stopping asserts, batch validation, single state."
    avoid_when: "Do not use them to bundle unrelated behaviors into one test; split those into focused tests or use parametrization."
    expected: "A single test reports every failed field check at once instead of stopping at the first mismatch, while unrelated behaviors stay in separate focused tests."
  - anchor: assertion-plugins-pytest-unordered
    what: "Order-agnostic comparison via `unordered(expected)` that checks membership and multiplicity of ordered collections without enforcing element position."
    problem: "Result collection has non-deterministic or irrelevant order, yet membership and multiplicity must hold while duplicates survive; order-insensitive compare, unhashable elements, multiset equality, preserve duplicates, position-blind match, bag semantics."
    use_when: "Result collection order is irrelevant or unstable, while membership and multiplicity stay meaningful and duplicate elements must survive; order insensitive compare, multiset equality, unhashable elements, preserve duplicates, position blind match, bag semantics, collection invariant."
    avoid_when: "Do not use it when element order is part of the contract under test, because order-agnostic comparison would silently accept a wrongly ordered result."
    expected: "Collections compare equal regardless of element order, duplicates are preserved, and unhashable elements are handled without `set()`."
  - anchor: assertion-plugins-dirty-equals
    what: "Composable shape matchers from dirty-equals that assert structure, types, regex patterns, and approximate values instead of exact equality inside complex objects."
    problem: "Response shape carries auto-generated ids, timestamps, counters that shift every run, so exact equality over-constrains values outside behavior under test; dynamic fields, loose shape match, structural assertion, ignore unstable values, type pattern match, contract boundary."
    use_when: "Response shape carries generated ids, timestamps, counters, or other unstable fields, while structure and types still need assertion; dynamic fields, loose shape match, structural assertion, ignore unstable values, type pattern match, contract boundary, flexible equality."
    avoid_when: "Do not use it when the exact value is the behavior you are testing."
    expected: "Response shapes are validated with dynamic fields matched loosely while exact-value behaviors still use plain equality."
  - anchor: assertion-plugins-pytest-subtests
    what: "The `subtests` fixture that runs the same assertion body against many inputs inside one test and reports each failure individually via `subtests.test(msg=..., **context)`."
    problem: "One assertion body must run against many dynamically produced inputs, reporting each failure alone without repeating expensive shared setup per case; per-input failure, dynamic cases, shared setup once, loop-level reporting, subtest isolation, expensive fixture reuse."
    use_when: "Many dynamically produced inputs share one assertion body, shared setup costs too much to repeat per case, and each input failure must report separately; dynamic cases, per input failure, shared setup once, loop level reporting, subtest isolation, expensive fixture reuse, case context."
    avoid_when: "Do not use subtests for static, independent inputs; prefer `@pytest.mark.parametrize` there."
    expected: "Each input's failure is reported as its own subtest within one run, and expensive shared setup runs only once."
  - anchor: assertion-plugins-pytest-regressions
    what: "Regression testing with the `data_regression` fixture that stores deterministic expected output in version-controlled baselines and compares subsequent runs against them via `data_regression.check(payload)`."
    problem: "Large stable output needs version-controlled baseline instead of verbose manual assertion, while random or environment fields must be sanitized before compare; golden baseline, snapshot review, serialized output, numeric table, deliberate regen, sanitize unstable fields."
    use_when: "Large stable output belongs under reviewable baseline, manual assertion would be verbose, and unstable fields can be sanitized before compare; golden baseline, snapshot review, serialized output, numeric table, deliberate regen, sanitize unstable fields, version controlled expectation."
    avoid_when: "Do not use it for small or frequently changing outputs where a direct assertion is clearer, and never commit baselines with unsanitized unstable fields (IDs, timestamps, hostnames) or unreviewed diffs."
    expected: "Large outputs match reviewable, sanitized baselines stored in version control and are updated only deliberately with `--force-regen`."
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
