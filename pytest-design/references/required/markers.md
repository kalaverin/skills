---
subject: "Categorize tests and steer selection/CI: register markers in `pyproject.toml` with `strict_markers = true`, built-ins `@pytest.mark.skip`/`skipif`/`xfail`/`filterwarnings`, compose `-m` boolean expressions, class/module `pytestmark`, orthogonal category markers for suite splits, plus `pytest-rerunfailures`/`pytest-timeout`/`pytest-cov`; keep the registry sorted and composable, combine markers with parametrization."
index:
  - anchor: markers-registering-custom-markers
    what: "User-defined `@pytest.mark.<name>` labels attached to tests to carry metadata for selection and for hook/plugin behavior. Marks apply to tests only, never to fixtures."
    problem: "Suite needs small queryable vocabulary so developers and CI select subsets, gate behavior, and document intent without encoding in names or bodies; orthogonal axis, multiple consumers, strict markers, typo fail, self-document, selectable."
    use_when: "Suite needs small queryable marker vocabulary, selection gating and documentation must not encode in names or bodies inside test code; orthogonal axis, multiple consumers, strict markers, typo fail, self document, selectable, custom marker."
    avoid_when: "Do not add a marker to carry test input data (use `parametrize`), to wire a resource (use a fixture or `usefixtures`), for a one-off platform/version gate (use inline `skipif` with a named predicate), when it duplicates an existing marker or a built-in, when you would need `a_and_b` combos (keep axes separate and compose with `-m`), or on a fixture expecting selection (marks do not affect fixtures)."
    expected: "A registered, `-m`-selectable vocabulary with typo safety under `strict_markers` and self-documentation via `pytest --markers`."
  - anchor: markers-built-in-markers
    what: "Markers with native pytest semantics: `skip` and `skipif` exclude a test, `xfail` marks an expected failure, `filterwarnings` adds a warning filter, alongside `parametrize` and `usefixtures`."
    problem: "Conditional collection, known-failure, and warning expectations must express as declarative metadata instead of imperative branches inside bodies; skip reason, expected failure strict, exception pinned, warning policy, metadata not branch, no silence."
    use_when: "Conditional collection, expected failure, and warning policy belong in declarative metadata, imperative branches inside bodies hide intent from readers; skip reason, expected failure strict, exception pinned, warning policy, metadata not branch, no silence."
    avoid_when: "Do not use `xfail` as a permanent parking lot for broken tests (fix or delete), do not omit `raises=` (any failure would then count as xfail and hide regressions), do not hide branches in bodies that a marker could express, and do not silence warnings project-wide to make tests green."
    expected: "Conditional collection, known failures, and warning expectations live in metadata, so test bodies contain only arrange-act-assert logic."
  - anchor: markers-selecting-with-m-expressions
    what: "Three selection mechanisms: `-m <expr>` matches marker names and keyword arguments, `-k <expr>` substring-matches test and parent names and attributes, and positional node IDs select exact `module.py::class::method[param]` nodes."
    problem: "Run precisely subset developer or CI job needs without collecting or executing rest; marker select, boolean expr, keyword arg match, substring fallback, node id, exact subset."
    use_when: "Developer or CI needs exact subset for runs, marker expression keyword match substring fallback and node id give precise selection; marker select, boolean expr, keyword arg match, substring fallback, node id, exact subset, run selection."
    avoid_when: "Do not assume `-m` sees positional marker args or non-literal values (only int, str, bool, None keyword args match); do not encode selection intent in test names when a marker would be clearer; do not rely on `-k` for exact categorization because it matches substrings and can over-select."
    expected: "The exact intended subset runs and nothing else, combining marker names and keyword args with `-k` as the substring fallback."
  - anchor: markers-pytestmark
    what: "Module-level `pytestmark` (a single `MarkDecorator` or a list) and class-level application that propagates a marker to every test in that scope; per-instance marks via `pytest.param(..., marks=...)`."
    problem: "Marker must attach once to cohesive class or module instead of repeating same decorator on every test; module mark, class mark, shared category, per-instance param mark, no repeat, no over-select."
    use_when: "Cohesive class or module shares one marker, repeating decorator on every test duplicates intent, and param marks cover per instance cases; module mark, class mark, shared category, per instance param mark, no repeat, no over select."
    avoid_when: "Do not module-mark unrelated tests just to save keystrokes (it hides intent and over-selects), and do not assume class-level `pytestmark` merges with subclass marks by default (verify inheritance behavior in your pytest version)."
    expected: "One declaration marks a cohesive scope, with no repeated decorators and no unrelated tests swept into the category."
  - anchor: markers-plugin-markers
    what: "`@pytest.mark.flaky(reruns=N, only_rerun=[...], condition=...)` from pytest-rerunfailures re-runs a failing test up to N times to absorb transient failures; resolution priority is marker, then CLI `--reruns`, then config `reruns`."
    problem: "CI must stay green against genuinely transient external failures without hiding deterministic bugs; transient retry, only rerun scope, bounded count, fix first, no reruns delay, real bug fails."
    use_when: "External resource failure is genuinely transient, deterministic bugs must not hide, and rerun stays scoped to expected exceptions; transient retry, only rerun scope, bounded count, fix first, no reruns delay, real bug fails."
    avoid_when: "Do not use `flaky` to mask deterministic failures or as a substitute for stabilizing the test; avoid `reruns_delay` (it sleeps between retries and slows the suite) and blanket `--reruns` without `only_rerun`, which hides real regressions."
    expected: "Only transient failures are retried within a bounded, exception-scoped count, while deterministic bugs still fail the build."
  - anchor: markers-plugin-markers
    what: "`@pytest.mark.timeout(seconds[, method=...])` from pytest-timeout aborts a test that exceeds a duration; the `thread` or `signal` method is set via the marker, `--timeout_method`, or config, and the marker overrides config."
    problem: "Deadlocks and hangs must abort stuck test so it cannot block whole run; hang abort, safety net, sla value, signal thread, not performance, native code limit."
    use_when: "Test can hang on network lock or subprocess, timeout must abort stuck run, and value matches guarded SLA rather than performance claim; hang abort, safety net, sla value, signal thread, not performance, native code limit."
    avoid_when: "Do not use `timeout` to assert performance or to paper over slow tests; on Windows the default `thread` method cannot interrupt C extensions, so do not rely on it for native-code hangs."
    expected: "A stuck test is aborted before it can block the run, and passing timing is never asserted by the marker."
  - anchor: markers-plugin-markers
    what: "`@pytest.mark.no_cover` from pytest-cov excludes a test's lines from the coverage context; the canonical line-level exclusion is coverage.py's `# pragma: no cover`."
    problem: "Coverage metric must stay meaningful by excluding tests whose exercised lines are not worth measuring; exclude probe, per-test context, external service noise, no inflate, context switch conflict, meaningful coverage."
    use_when: "Coverage metric loses meaning when probe or external service noise inflates lines, and per test context keeps attribution correct; exclude probe, per test context, external service noise, no inflate, context switch conflict, meaningful coverage."
    avoid_when: "Do not use `no_cover` to inflate coverage by hiding undertested code; note the known conflict where `@pytest.mark.no_cover` together with `--cov-context=test` can raise `CoverageException: Cannot switch context`, so verify it in your pinned pytest-cov."
    expected: "Coverage reflects only meaningful code, with external-service probes excluded and per-test context attributed correctly."
libraries:
  - pytest-rerunfailures
  - pytest-timeout
  - pytest-cov
---

# MARKERS

## Registering custom markers

[ref: #markers-registering-custom-markers]

Register every project-specific marker in `pyproject.toml` and enable `strict_markers` so misspelled marks surface as collection errors rather than silent skips.

```toml
[tool.pytest.ini_options]
markers = [
    "api: HTTP API tests",
    "cache: Tests that need a cache",
    "db: Tests that need a database",
    "integration: Tests that need external services",
    "performance: Load or performance tests",
    "security: Security-focused tests",
    "serial: Tests that cannot run in parallel",
    "slow: Tests taking more than one second",
    "unit: Fast tests with no external dependencies",
]
strict_markers = true
```

**Variety booster:** Keep the marker list sorted alphabetically and review it whenever a new category appears, so the set stays small and composable.

## Built-in markers (`skip`, `skipif`, `xfail`, `filterwarnings`)

[ref: #markers-built-in-markers]

Use `skip`, `skipif`, `xfail`, and `filterwarnings` to encode platform, Python-version, feature-flag, and warning expectations directly in test metadata.

```python
import os
import sys
import warnings

import pytest
from faker import Faker

_IS_PY311_OR_OLDER: bool = sys.version_info < (3, 12)
_ASYNC_TRANSPORT_ENABLED: bool = os.getenv("ASYNC_TRANSPORT", "0") == "1"

@pytest.mark.skip(reason="Blocked by upstream CVE-2024-9999")
def test_legacy_signature_verification(fake: Faker) -> None:
    """
    Given: skip marker is applied.
    When: test runs.
    Then: it is skipped by pytest.
    """
    # --- Arrange ---
    data = fake.binary(length=32)

    # --- Act ---
    result = isinstance(data, bytes)

    # --- Assert ---
    assert result

@pytest.mark.skipif(
    _IS_PY311_OR_OLDER,
    reason="Requires Python 3.12 tomllib support",
)
def test_config_loader_reads_toml(fake: Faker) -> None:
    """
    Given: generated TOML text.
    When: config loader reads it.
    Then: text is a string.
    """
    # --- Arrange ---
    text = fake.sentence()

    # --- Act ---
    result = isinstance(text, str)

    # --- Assert ---
    assert result

@pytest.mark.skipif(
    not _ASYNC_TRANSPORT_ENABLED,
    reason="Async transport is behind a feature flag",
)
def test_async_transport_round_trip(fake: Faker) -> None:
    """
    Given: generated payload.
    When: async transport sends and receives.
    Then: payload remains a string.
    """
    # --- Arrange ---
    payload = fake.sentence()

    # --- Act ---
    result = isinstance(payload, str)

    # --- Assert ---
    assert result

def _normalize_email(email: str) -> str:
    return email.upper()  # Known bug: should be lower-cased.

@pytest.mark.xfail(
    reason="Issue #99: email normalization upper-cases addresses",
    strict=True,
)
def test_normalize_email_lowercases_input(fake: Faker) -> None:
    """
    Given: generated email address.
    When: email is normalized.
    Then: result equals the lower-cased address.
    """
    # --- Arrange ---
    email = fake.fake_email()

    # --- Act ---
    normalized = _normalize_email(email)

    # --- Assert ---
    assert normalized == email.lower()

@pytest.mark.filterwarnings("always::DeprecationWarning")
def test_legacy_tokenizer_emits_deprecation(fake: Faker) -> None:
    """
    Given: deprecation warning message.
    When: warning is emitted.
    Then: pytest.warns captures DeprecationWarning.
    """
    # --- Arrange ---
    message = fake.sentence()

    # --- Act ---
    with pytest.warns(DeprecationWarning):
        warnings.warn(message, DeprecationWarning)

    # --- Assert ---
    # Warning captured as expected; assertion handled by pytest.warns context.
```

**Variety booster:** Combine `skipif` with `@pytest.mark.parametrize` to gate only one parameter combination, or move platform/version predicates into a shared `tests/_compat.py` module.

## Selecting tests with `-m` expressions

[ref: #markers-selecting-with-m-expressions]

Compose `-m` expressions from marker names, boolean operators, and parentheses to run exactly the subset a developer or CI job needs.

```python
import pytest
from faker import Faker

@pytest.mark.device(serial="123", env="prod")
def test_provisioning_endpoint_accepts_valid_serial(fake: Faker) -> None:
    """
    Given: a generated serial identifier and a prod device marker.
    When: the serial is inspected.
    Then: it contains dashes.
    """
    # --- Arrange ---
    serial = fake.uuid4()

    # --- Act ---
    result = "-" in serial

    # --- Assert ---
    assert result

@pytest.mark.device(serial="123", env="staging")
def test_provisioning_endpoint_rejects_staging_serial(fake: Faker) -> None:
    """
    Given: a generated serial identifier and a staging device marker.
    When: the serial is inspected.
    Then: it contains dashes.
    """
    # --- Arrange ---
    serial = fake.uuid4()

    # --- Act ---
    result = "-" in serial

    # --- Assert ---
    assert result
```

```bash
pytest -m "device"
pytest -m "unit and not slow"
pytest -m "integration or api"
pytest -m "not (db or cache)"
```

**Variety booster:** Add a `ci` marker to tests that are safe in resource-constrained runners and split jobs with `-m "ci and not serial"`.

## Applying markers to classes and modules (`pytestmark`)

[ref: #markers-pytestmark]

Attach a marker once to a class or module so every method in that scope inherits it without repeating decorators.

```python
import pytest
from faker import Faker

pytestmark: list[pytest.MarkDecorator] = [pytest.mark.integration, pytest.mark.db]

class TestCacheInvalidation:
    pytestmark: pytest.MarkDecorator = pytest.mark.serial

    def test_eviction_policy_removes_oldest_first(self, fake: Faker) -> None:
        """
        Given: generated key and value.
        When: cache stores the entry.
        Then: key and value are strings.
        """
        # --- Arrange ---
        key = fake.word()
        value = fake.sentence()

        # --- Act ---
        key_is_str = isinstance(key, str)
        value_is_str = isinstance(value, str)

        # --- Assert ---
        assert key_is_str
        assert value_is_str

    def test_ttl_expires_stale_entries(self, fake: Faker) -> None:
        """
        Given: generated TTL value.
        When: TTL is inspected.
        Then: it is a positive integer.
        """
        # --- Arrange ---
        ttl = fake.pyint(min_value=1, max_value=60)

        # --- Act ---
        result = isinstance(ttl, int)

        # --- Assert ---
        assert result
```

**Variety booster:** Combine `pytestmark` with class-scoped fixtures and `@pytest.mark.parametrize` so every method exercises multiple inputs under the same inherited category.

## Plugin markers: `flaky`, `timeout`, `no_cover`

[ref: #markers-plugin-markers]

Use `pytest-rerunfailures`, `pytest-timeout`, and `pytest-cov` markers when their behavior is not already covered by project-wide configuration.

```python
import pytest
from faker import Faker

@pytest.mark.flaky(
    reruns=3,
    only_rerun=[ConnectionError, TimeoutError],
)
def test_third_party_quote_api_returns_price(fake: Faker) -> None:
    """
    Given: generated stock symbol.
    When: symbol length is checked.
    Then: it has exactly three characters.
    """
    # --- Arrange ---
    symbol = fake.lexify(text="???", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    # --- Act ---
    length = len(symbol)

    # --- Assert ---
    assert length == 3

@pytest.mark.timeout(30)
def test_report_generation_completes_within_budget(fake: Faker) -> None:
    """
    Given: generated row count.
    When: row count is inspected.
    Then: it satisfies the minimum budget.
    """
    # --- Arrange ---
    rows = fake.pyint(min_value=10, max_value=100)

    # --- Act ---
    result = rows >= 10

    # --- Assert ---
    assert result

@pytest.mark.no_cover
def test_health_probe_checks_external_service(fake: Faker) -> None:
    """
    Given: generated HTTPS endpoint.
    When: endpoint scheme is inspected.
    Then: it starts with https://.
    """
    # --- Arrange ---
    endpoint = fake.url(schemes=["https"])

    # --- Act ---
    result = endpoint.startswith("https://")

    # --- Assert ---
    assert result
```

**Variety booster:** Pair `flaky` with `@pytest.mark.parametrize` to retry only the parameter combinations that hit unreliable resources, and keep `timeout` values next to the SLA they enforce.

## Practical category markers and CI splits

[ref: #markers-category-markers-and-ci-splits]

Define a small orthogonal set of category markers and use them to split the suite into fast parallel jobs, resource-dependent jobs, and serial jobs.

```python
import pytest
from faker import Faker

@pytest.mark.unit
def test_calculator_commutes_for_integers(fake: Faker) -> None:
    """
    Given: two generated positive integers.
    When: addition is compared in both orders.
    Then: addition commutes.
    """
    # --- Arrange ---
    a = fake.pyint(min_value=1, max_value=100)
    b = fake.pyint(min_value=1, max_value=100)

    # --- Act ---
    left = a + b
    right = b + a

    # --- Assert ---
    assert left == right
```

```bash
pytest -n auto -m "unit and not serial"
pytest -m "integration and not serial"
pytest -m "serial"
```

**Variety booster:** Add a `slow` marker threshold and run `-m "slow"` on a scheduled job while keeping the pre-commit job limited to `unit and not slow`.
