---
subject: "Categorize tests and steer selection/CI: register markers in `pyproject.toml` under `strict_markers = true`, built-ins `skip`/`skipif`/`xfail`/`filterwarnings`, boolean `-m` expressions plus `-k` fallback and node IDs, class/module `pytestmark` with per-param marks, orthogonal category markers for CI suite splits, plugin markers `flaky`/`timeout`/`no_cover` from `pytest-rerunfailures`/`pytest-timeout`/`pytest-cov`."
index:
  - anchor: markers-registering-custom-markers
    what: "User-defined `@pytest.mark.<name>` labels attached to tests to carry metadata for selection and for hook/plugin behavior. Marks apply to tests only, never to fixtures."
    problem: "Suite needs small queryable vocabulary so developers and CI select subsets, gate plugin behavior, and document intent without encoding category into test names or bodies; orthogonal axis, silent typo skip, registry bloat drift, fixture immunity, combo marker temptation."
    use_when: "New orthogonal category earns consumers across people and CI jobs; intent otherwise leaks into test names or helper logic; vocabulary stays small enough to review at glance."
    avoid_when: "Marker proposed to carry input data (parametrize's job), wire resources (fixture's job), or one-off platform gate (inline skipif's job); candidate duplicates existing or built-in mark; `a_and_b` combination needed instead of composed `-m`; fixture marked expecting selection effect."
    expected: "Registry yields `-m`-selectable vocabulary with typo safety under `strict_markers`, self-documented via `pytest --markers`."
  - anchor: markers-built-in-markers
    what: "Markers with native pytest semantics: `skip` and `skipif` exclude a test, `xfail` marks an expected failure, `filterwarnings` adds a warning filter, alongside `parametrize` and `usefixtures`."
    problem: "Conditional collection, known-failure tracking, and warning expectations must live in declarative metadata instead of imperative branches hidden inside bodies; xfail parking lot, unpinned raises blind, project-wide warning silence, platform version predicates, issue-referenced reason."
    use_when: "Skip or xfail decision carries traceable reason; expected failure pinned to specific exception; warning expectation scoped per test rather than globally."
    avoid_when: "`xfail` used as permanent parking for broken tests (fix or delete instead); `raises=` omitted so any failure counts as xfail and hides regressions; branches buried in bodies that marker would express; warnings silenced project-wide for green build."
    expected: "Conditional collection, known failures, and warning expectations live in metadata, so bodies contain only arrange-act-assert logic."
  - anchor: markers-selecting-with-m-expressions
    what: "Three selection mechanisms: `-m <expr>` matches marker names and keyword arguments, `-k <expr>` substring-matches test and parent names and attributes, and positional node IDs select exact `module.py::class::method[param]` nodes."
    problem: "Developer or CI job needs precisely chosen subset executed without collecting rest of suite, and selection vocabulary must stay exact under growth; positional args invisible, literal-only matching, substring over-selection, names misused as categories, ci marker gate."
    use_when: "Job definition demands repeatable subset; marker expression over keyword arguments reaches needed precision; `-k` suffices only for ad-hoc name exploration, node IDs for single-target runs."
    avoid_when: "`-m` expected to see positional marker args or computed values (only int/str/bool/None keyword literals match); selection intent encoded in test names where marker reads clearer; `-k` trusted for exact categorization despite substring semantics."
    expected: "Exactly intended subset runs and nothing else, combining marker names with keyword args and `-k` reserved for ad-hoc exploration."
  - anchor: markers-pytestmark
    what: "Module-level `pytestmark` (a single `MarkDecorator` or a list) and class-level application that propagates a marker to every test in that scope; per-instance marks via `pytest.param(..., marks=...)`."
    problem: "Marker belongs to cohesive class or module scope, yet repeating identical decorator on every test method duplicates intent and invites drift; unrelated sweep hazard, subclass merge gotcha, list or single decorator, keystroke misuse, inherited category params."
    use_when: "Every method in scope genuinely shares category; single declaration replaces per-test repetition; per-instance variation covered by `pytest.param(marks=...)`."
    avoid_when: "Unrelated tests module-marked to save keystrokes, hiding intent and over-selecting; class-level `pytestmark` assumed to merge with subclass marks (inheritance varies by pytest version — verify); scope marked when only few members belong."
    expected: "One declaration marks cohesive scope with no repeated decorators and no unrelated tests swept into category."
  - anchor: markers-plugin-markers
    what: "`@pytest.mark.flaky(reruns=N, only_rerun=[...], condition=...)` from pytest-rerunfailures re-runs a failing test up to N times to absorb transient failures; resolution priority is marker, then CLI `--reruns`, then config `reruns`."
    problem: "CI job must stay green against genuinely transient failures of external resources while deterministic bugs still need loud failure; retry delay slowdown, blanket retries mask regressions, stabilization substitute, third-party flakiness, exception-scoped retry."
    use_when: "Failure source is external and genuinely transient; retry limited to expected exception list; underlying flaky behavior already tracked for stabilization."
    avoid_when: "`flaky` masking deterministic failure or substituting stabilization work; `reruns_delay` added (sleeps between retries, slows suite); blanket `--reruns` without `only_rerun` letting real regressions pass."
    expected: "Only transient failures retried within bounded exception-scoped count, deterministic bugs still fail build."
  - anchor: markers-plugin-markers
    what: "`@pytest.mark.timeout(seconds[, method=...])` from pytest-timeout aborts a test that exceeds a duration; the `thread` or `signal` method is set via the marker, `--timeout_method`, or config, and the marker overrides config."
    problem: "Deadlock or infinite hang must not let one stuck test block entire suite run until CI job-level cancellation kills everything; network lock subprocess hang, slow-test papering, windows thread blind, guarded sla budget."
    use_when: "Test reaches network, lock, or subprocess that can legitimately stall; abort value mirrors guarded SLA, not speed claim; signal method available on platform (Unix) when native code involved."
    avoid_when: "`timeout` asserting performance or disguising slow tests; Windows `thread` method trusted against C-extension hangs (it cannot interrupt native code); generous value hiding real stalls."
    expected: "Stuck test aborted before blocking run; passing timing never asserted by marker."
  - anchor: markers-plugin-markers
    what: "`@pytest.mark.no_cover` from pytest-cov excludes a test's lines from the coverage context; the canonical line-level exclusion is coverage.py's `# pragma: no cover`."
    problem: "Coverage metric loses meaning when tests exercising uninteresting lines count toward percentage, so selective exclusion keeps signal honest; health probe exclusion, coverage inflation misuse, coverageexception conflict, pragma line alternative, attribution per test."
    use_when: "Test exists to probe external service health rather than exercise project code; per-test context attribution matters under `--cov-context=test`; exclusion stays rare and justified."
    avoid_when: "`no_cover` hiding undertested code to inflate metric; combination with `--cov-context=test` assumed safe (known `CoverageException: Cannot switch context` conflict — verify pinned version); marker used where line-level pragma expresses intent."
    expected: "Coverage reflects only meaningful code: external-service probes excluded, per-test context attributed correctly."
  - anchor: markers-category-markers-and-ci-splits
    what: "Splitting the suite into CI jobs by an orthogonal category marker set: fast parallel job `-n auto -m \"unit and not serial\"`, resource-dependent job `-m \"integration and not serial\"`, serial job `-m \"serial\"`, plus scheduled `-m \"slow\"` and pre-commit `unit and not slow` gates."
    problem: "Whole suite in one CI job wastes runner parallelism and mixes fast feedback with resource-heavy tests, so splits need category vocabulary mapping to job shapes; fast lane split, serial quarantine, scheduled slow sweep, pre-commit gate, parallel worker lane."
    use_when: "CI pipeline has multiple runner slots and suite mixes fast unit with resource-dependent tests; jobs need stable definitions beyond one developer's ad-hoc `-m`; feedback latency matters for pre-commit."
    avoid_when: "Category axes multiplied per job until expressions become unreadable; serial tests mixed into parallel lane (ordering assumptions break); slow threshold undocumented so marker rots."
    expected: "Suite runs as fast parallel lane, resource-dependent lane, and serial lane with slow tier on scheduled job, each defined by stable marker expression."
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
