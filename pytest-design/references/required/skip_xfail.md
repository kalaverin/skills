---
subject: "Manage test exclusion and expected failure: unconditional skip, conditional `skipif`, imperative `pytest.skip`, `pytest.importorskip`, `xfail` markers, runtime `pytest.xfail`, module/class `pytestmark`, parametrized row marks, CLI/configuration toggles, reusable marker definitions, fixture gating, `xfail(..., run=False)`, and dynamic parametrized mark factories."
index:
  - anchor: skip-xfail-mark-skip
    what: "`@pytest.mark.skip(reason=...)` removes a test at collection time so it never runs."
    problem: "Some tests cannot run in given runner at all (need OS-level binary unavailable in CI), and running them errors for reasons unrelated to code under test; runner incompatible, collection remove, clear reason, reusable mark, not broken code, xfail instead."
    use_when: "Test is fundamentally incompatible with current runner; executing it would produce errors unrelated to code under test; removing it at collection time is acceptable."
    avoid_when: "Code under test is broken; skip is used as permanent parking lot for failing assertions; runner is actually capable of executing test."
    expected: "Runner-incompatible tests are removed at collection with an explanatory note, while broken-code cases go through xfail or are fixed."
  - anchor: skip-xfail-mark-skipif
    what: "`@pytest.mark.skipif(condition, reason=...)` skips a test when a collection-time condition is true; multiple decorators act as alternatives, skipping if any condition holds."
    problem: "Platform, version, or feature gates must skip tests declaratively based on collection-time predicates, but scattering inline conditions across files causes drift and hides intent; collection gate, OR combination, shared marker, predicate module, no fixture dependency, declarative skip."
    use_when: "Platform, version, or feature gate evaluates during collection; runtime fixture state is unnecessary; one exported marker covers many suites."
    avoid_when: "Condition depends on fixture values evaluated during collection; skip logic is actually runtime-only; decorator stack becomes unreadable."
    expected: "Tests skip declaratively by collection-time predicates with centralized markers, and no condition depends on runtime fixture state."
  - anchor: skip-xfail-imperative-skip
    what: "Call `pytest.skip(reason)` from a test, fixture, or helper when the skip condition is only available at runtime; use `allow_module_level=True` to skip an entire module."
    problem: "Some skip conditions (schema version, config value) are only knowable at runtime, after collection, and embedding them as inline guards inside every test duplicates boilerplate; runtime condition, inside test fixture, module-level gate, guard fixture, centralize check, collection-knowable declarative."
    use_when: "Skip condition depends on runtime state that collection time cannot know; a shared availability fixture centralizes repeated checks; whole module must be skipped at import."
    avoid_when: "Condition is knowable at collection time; `pytest.skip` is called at module scope without `allow_module_level=True`; skip logic is duplicated in every test body."
    expected: "Runtime-only conditions skip via `pytest.skip` at module scope where needed, while conditions knowable during collection stay declarative."
  - anchor: skip-xfail-importorskip
    what: "`pytest.importorskip(module, minversion=...)` at module scope no-ops the whole test file when a third-party package is absent or outdated, returning the imported module for direct use."
    problem: "Tests for optional integration must no-op cleanly when an integration library is absent or outdated, without failing collection or hiding missing required dependencies; integration library, minversion floor, skip module, loud required missing, wrapper abstraction, clean noop."
    use_when: "Optional integration dependency may be absent; collection must not fail; module-level import gate yields a silent skip when dependency is missing or too old."
    avoid_when: "Dependency is required for project to function; absence should fail loudly; import is hidden inside helper instead of module scope."
    expected: "Optional-dependency test modules skip cleanly when the library is absent/old, and required dependencies still fail loud."
  - anchor: skip-xfail-mark-xfail
    what: "`@pytest.mark.xfail(reason=..., condition=..., raises=..., run=..., strict=...)` marks a test expected to fail, declaring the expected exception and whether an unexpected pass is itself a failure."
    problem: "Known bugs must document without breaking build, but resurface once fixed and must not hide changed failure mode; reason link, raises pinned, strict xpass, run false, no parking lot, failure mode pinned."
    use_when: "Known bug must be documented without breaking build; accidental pass must fail the test once fixed; expected exception must remain stable."
    avoid_when: "Xfail becomes a long-term home for broken tests; `raises` is omitted so any failure counts as xfail; `strict` is false so fixed bugs stay hidden."
    expected: "Known bugs report XFAIL now and XPASS (a failure under `strict=True`) once fixed, with `raises=` pinning the expected failure mode."
  - anchor: skip-xfail-imperative-xfail
    what: "Calling `pytest.xfail(reason)` at runtime marks the current test as expected-failure; the call halts execution, so any following statements are unreachable."
    problem: "Some expected-failure conditions surface only at runtime, so collection-time mark cannot know limitation in advance; `pytest.xfail` must be called before assertions or further code to trigger expected-failure protocol; runtime discover, helper reason, no code after, internal exception, collection-knowable mark, limitation check."
    use_when: "Test detects runtime limitation that prevents meaningful execution; expected failure should be recorded with reason; remaining assertions must be skipped."
    avoid_when: "Condition is knowable at collection time; `pytest.xfail` is called after assertions or inside helpers that hide intent; xfail is used to skip normal test logic."
    expected: "Runtime-discovered limitations report as expected failures via helper-driven checks, with no dead assertions after the call and collection-time conditions using the mark."
  - anchor: skip-xfail-module-class-pytestmark
    what: "Assigning `pytestmark` (a mark or a list) at module or class scope to apply a skip/xfail (or any mark) to every test in that scope."
    problem: "Applying same skip or xfail marker to every test in module or class individually is noisy and error-prone, and newly added tests can silently miss required marker; module-level list, class-level assignment, hierarchical application, repetitive decorators."
    use_when: "Every test in a module or class shares the same skip/xfail condition; applying the marker once avoids per-test repetition and ensures new tests inherit it."
    avoid_when: "Different tests need different conditions; marker is intended for only some tests in module or class; tests should opt in explicitly rather than inherit marker."
    expected: "One `pytestmark` declaration applies the mark to a cohesive module or class, with no per-test decorator duplication and no unrelated tests swept in."
  - anchor: skip-xfail-parametrized-cases
    what: "Attaching `pytest.mark.skip` or `pytest.mark.xfail` to individual cases via `pytest.param(..., marks=...)` so per-case limitations are recorded without splitting the matrix."
    problem: "Some parametrized rows are invalid on certain platforms or expose known bugs, but disabling whole function discards useful coverage; row-level exception, per-row condition, preserves other rows, invalid combinations, known bug rows, precise targeting."
    use_when: "Only specific rows in a parametrized matrix should be skipped or xfailed; the remaining rows must still run; the condition depends on row data or environment."
    avoid_when: "All rows share the same condition; skip/xfail logic is complex enough to deserve separate test function; row-level marks become unreadable due to stacking."
    expected: "The matrix stays compact while each limited case carries its own skip/xfail mark with a reason."
  - anchor: skip-xfail-configuration-cli
    what: "Enabling `xfail_strict = true` in config and using the summary flag `-rxXs` (and `--runxfail` to force xfail-marked tests to run) to surface and validate expected failures."
    problem: "Markers baked into source files are hard to change across CI jobs or local workflows, and environment-specific skips/xfails need centralized control without editing every test module; config file, CLI override, marker selection, per-environment behavior, xfail strict, summary reasons, runxfail force."
    use_when: "Skip/xfail rules must vary by environment, CI job, or local config; centralized control is preferred over scattered decorators; command-line marker filtering is needed."
    avoid_when: "Condition is stable and tied to test logic; configuration files become hidden layer that obscures why tests are skipped; every environment needs the same behavior."
    expected: "Accidental passes surface as failures under `xfail_strict`, skip/xfail reasons are visible in the summary, and every xfail carries a reason."
  - anchor: skip-xfail-reusable-markers
    what: "A shared module such as `tests/_compat.py` that exports reusable `skipif` mark objects so one gate covers many suites."
    problem: "Complex skipif conditions are repeated across tests and drift out of sync, and magic reason strings hide intent; define once, reuse via decorator, shared `skip_*` constants, centralized marker module, version checks, platform detection."
    use_when: "The same skipif condition appears in many tests; reason or predicate should be maintained in one place; gates for version or platform are needed."
    avoid_when: "The condition is used only once; the shared predicates file becomes a dumping ground for unrelated predicates; reasons are duplicated or omitted."
    expected: "One shared module owns every collection-time gate, and test files compose them without duplication."
  - anchor: skip-xfail-runtime-fixture-gating
    what: "Call `pytest.skip` or `pytest.xfail` inside a fixture to gate every dependent test when the condition is only available after collection."
    problem: "Fixture or resource is unavailable at collection time, but skipping logic belongs outside test body so tests stay readable and skip reason stays close to resource check; fixture-level skip, autouse guard, runtime resource, one check, collection-knowable declarative, no per-test duplicate."
    use_when: "A skip decision depends on runtime state produced by a fixture; the fixture is the natural owner of the skip; keeping the check in the fixture avoids cluttering test bodies."
    avoid_when: "Condition is knowable at collection time; the skip is better expressed as a declarative marker; skips inside fixtures hide why a broad set of tests is absent."
    expected: "One fixture gates all dependent tests at runtime, and conditions knowable during collection stay declarative."
  - anchor: skip-xfail-mark-xfail-condition-runfalse
    what: "Using `condition=` on `@pytest.mark.xfail` to mark a test expected to fail only when a collection-time predicate holds, and `run=False` to skip execution while still reporting xfail."
    problem: "Test is expected to fail only under specific condition, and running it otherwise should produce normal pass without false xfail when condition is absent; conditional xfail, `run=False`, skip outcome when condition false, evaluate at collection, targeted expectation."
    use_when: "Expected failure is tied to specific environment or feature flag; when condition is false the test should run normally; collection-time evaluation is sufficient."
    avoid_when: "Condition is dynamic at runtime; `run=False` would mask a regression in normal path; test should always execute regardless of condition."
    expected: "Version- or platform-scoped xfails are declared declaratively, and non-runnable tests still surface as xfail without executing."
  - anchor: skip-xfail-parametrized-mark-factories
    what: "Building reusable mark factories such as `xfail_for_issue(issue_id)` and attaching them (and `skip` marks) to individual `pytest.param` cases."
    problem: "Parametrize cases need different skip/xfail policies based on row values, but decorating whole function or hard-coding `pytest.param` for many rows is repetitive; dynamic marker factory, callable `marks=` argument, row-derived condition, logic driven by parameter values."
    use_when: "Each parametrized row requires a skip/xfail decision derived from its own values; `pytest.param` per row is too verbose; a callable can compute the marks from row data."
    avoid_when: "Marker rule is simple and uniform; `pytest.param` is readable; introducing a factory obscures which rows are skipped."
    expected: "Mark factories keep parametrized tables compact and consistent, with per-case limitations recorded in one place."
libraries:
  - pydantic
---



# SKIP, XFAIL, AND IMPORTORSKIP

## pytest.mark.skip (Unconditional Collection-Time Skip)

[ref: #skip-xfail-mark-skip]

`pytest.mark.skip(reason=...)` removes a test at collection time.

Use it when the test is fundamentally incompatible with the current runner, not when the code under test is broken.

```python
import pytest
from faker import Faker


PDF_EXTENSION = "pdf"
PDF_MIME_TYPE = "application/pdf"
SKIP_CHROMIUM_REASON = "Requires OS-level Chromium binary; unavailable in CI unit job."


@pytest.mark.skip(reason=SKIP_CHROMIUM_REASON)
def test_pdf_preview_renders(fake: Faker) -> None:
    """
    Given: generated PDF document name.
    When: PDF preview is rendered.
    Then: preview MIME type matches PDF.
    """
    # --- Arrange ---
    document = fake.file_name(extension=PDF_EXTENSION)

    # --- Act ---
    preview = render_pdf_preview(document)  # provided by project code

    # --- Assert ---
    assert preview.mime_type == PDF_MIME_TYPE
```

**Variety booster:** Attach a reusable skip mark variable to whole groups of tests and combine it with module-level `pytestmark` so one reason controls every related test.

## pytest.mark.skipif (Conditional Collection-Time Skip)

[ref: #skip-xfail-mark-skipif]

`pytest.mark.skipif(condition, reason=...)` skips a test only when a collection-time condition is true.

The condition is evaluated while pytest collects tests, so it must not depend on fixture values.

```python
import os
import sys

import pytest
from faker import Faker


WINDOWS_PLATFORM = "win32"
REQUIRED_FEATURE_FLAG = "MYAPP_ENABLE_LEGACY_IMPORTER"
LEGACY_IMPORTER_REASON = "Legacy importer is not supported on Windows."
FLAG_MISSING_REASON = "MYAPP_ENABLE_LEGACY_IMPORTER environment variable is not set."


skip_if_windows = pytest.mark.skipif(
    sys.platform == WINDOWS_PLATFORM,
    reason=LEGACY_IMPORTER_REASON,
)

skip_if_flag_missing = pytest.mark.skipif(
    REQUIRED_FEATURE_FLAG not in os.environ,
    reason=FLAG_MISSING_REASON,
)


@skip_if_windows
@skip_if_flag_missing
def test_legacy_importer_handles_large_files(fake: Faker) -> None:
    """
    Given: generated binary payload.
    When: legacy importer processes it.
    Then: result is marked complete.
    """
    # --- Arrange ---
    payload_size = fake.pyint(min_value=1024, max_value=8192)

    # --- Act ---
    result = legacy_import(fake.binary(length=payload_size))  # provided by project code

    # --- Assert ---
    assert result.is_complete
```

Multiple `skipif` decorators are combined with OR semantics: the test is skipped if any condition is true.

**Variety booster:** Define reusable `skipif` markers in a shared module and import them into test files so the same platform or feature gate covers many suites without copying conditions.

## Reusable skipif markers

[ref: #skip-xfail-reusable-markers]

A shared module exports reusable `skipif` mark objects so one gate covers many suites.

Import the marks into test files instead of redeclaring the condition inline.

```python
# tests/_compat.py
import os
import sys

import pytest


WINDOWS_PLATFORM = "win32"
LEGACY_IMPORTER_FLAG = "MYAPP_ENABLE_LEGACY_IMPORTER"
WINDOWS_REASON = "Legacy importer is not supported on Windows."
FLAG_MISSING_REASON = "MYAPP_ENABLE_LEGACY_IMPORTER environment variable is not set."


skip_if_windows = pytest.mark.skipif(
    sys.platform == WINDOWS_PLATFORM,
    reason=WINDOWS_REASON,
)

skip_if_legacy_flag_missing = pytest.mark.skipif(
    LEGACY_IMPORTER_FLAG not in os.environ,
    reason=FLAG_MISSING_REASON,
)
```

```python
from faker import Faker

from tests._compat import skip_if_legacy_flag_missing, skip_if_windows


LARGE_PAYLOAD_MIN = 1024
LARGE_PAYLOAD_MAX = 8192


@skip_if_windows
@skip_if_legacy_flag_missing
def test_legacy_importer_handles_large_files(fake: Faker) -> None:
    """
    Given: generated binary payload.
    When: legacy importer processes it.
    Then: result is marked complete.
    """
    # --- Arrange ---
    payload_size = fake.pyint(min_value=LARGE_PAYLOAD_MIN, max_value=LARGE_PAYLOAD_MAX)

    # --- Act ---
    result = legacy_import(fake.binary(length=payload_size))

    # --- Assert ---
    assert result.is_complete
```

**Variety booster:** Put every collection-time gate in `tests/_compat.py` and treat it as the single source of truth for platform, version, and feature gating across the suite.

## Imperative pytest.skip (Runtime Skip)

[ref: #skip-xfail-imperative-skip]

`pytest.skip(reason)` is called inside a test, fixture, or helper when the skip condition cannot be evaluated at collection time.

Unlike `pytest.mark.skipif`, it can inspect runtime state such as a schema version or a configuration value.

```python
import pytest
from faker import Faker


SCHEMA_VERSION_REQUIRED = 2
SCHEMA_TOO_OLD_REASON = "Test requires schema version 2 or newer."


def get_current_schema_version() -> int:
    # Placeholder: real code reads from the migration registry at runtime.
    raise NotImplementedError


def test_new_column_stores_generated_value(
    monkey: pytest.MonkeyPatch,
    fake: Faker,
) -> None:
    """
    Given: the database schema version is patched to a supported value.
    When: the schema is new enough to have the column.
    Then: a generated value is stored and retrieved.
    """
    # --- Arrange ---
    monkey.setattr(
        f"{__name__}.get_current_schema_version",
        lambda: SCHEMA_VERSION_REQUIRED,
    )
    if get_current_schema_version() < SCHEMA_VERSION_REQUIRED:
        pytest.skip(SCHEMA_TOO_OLD_REASON)
    value = fake.word()

    # --- Act ---
    stored = store_value(value)  # provided by project code

    # --- Assert ---
    assert stored == value
```

Use `pytest.skip(reason, allow_module_level=True)` at module scope when the entire file is invalid in the current environment.

```python
import sys

import pytest


WINDOWS_PLATFORM = "win32"
MODULE_SKIP_REASON = "Unix socket tests do not apply on Windows."


if sys.platform == WINDOWS_PLATFORM:
    pytest.skip(MODULE_SKIP_REASON, allow_module_level=True)
```

**Variety booster:** Centralize runtime availability checks in a fixture that calls `pytest.skip` for every dependent test, so the same guard is reused across the suite.

## Runtime fixture gating

[ref: #skip-xfail-runtime-fixture-gating]

A fixture can call `pytest.skip` to gate every dependent test when the condition depends on a runtime resource.

Make the guard fixture autouse when the entire module depends on the resource.

```python
import pytest
from faker import Faker


SCHEMA_VERSION_REQUIRED = 2
CURRENT_SCHEMA_VERSION = 2
SCHEMA_TOO_OLD_REASON = "Test requires schema version 2 or newer."


def get_current_schema_version() -> int:
    # Placeholder: real code reads from the migration registry at runtime.
    return CURRENT_SCHEMA_VERSION


@pytest.fixture(autouse=True)
def require_schema_version() -> None:
    if get_current_schema_version() < SCHEMA_VERSION_REQUIRED:
        pytest.skip(SCHEMA_TOO_OLD_REASON)


def test_new_column_stores_generated_value(fake: Faker) -> None:
    """
    Given: the autouse schema version guard fixture is active.
    When: the schema is new enough to have the column.
    Then: a generated value is stored and retrieved.
    """
    # --- Arrange ---
    value = fake.word()

    # --- Act ---
    stored = store_value(value)  # provided by project code

    # --- Assert ---
    assert stored == value
```

**Variety booster:** Use a non-autouse guard fixture as an explicit dependency when only some tests in the module need the runtime resource, so unrelated tests are not gated.

## pytest.importorskip (Optional Dependency Gating)

[ref: #skip-xfail-importorskip]

`pytest.importorskip(module, minversion=...)` skips the entire test module if an optional dependency is missing or too old.

It returns the imported module so the test can use it directly.

```python
import pytest
from faker import Faker


MIN_OPTIONAL_LIB_VERSION = "2.0"


pydantic = pytest.importorskip("pydantic", minversion=MIN_OPTIONAL_LIB_VERSION)


class _UserPayload(pydantic.BaseModel):
    name: str
    email: str


def test_pydantic_model_validates_optional_dependency(fake: Faker) -> None:
    """
    Given: generated name and email.
    When: pydantic model is instantiated.
    Then: name is truthy and email contains @.
    """
    # --- Arrange ---
    payload = _UserPayload(name=fake.name(), email=fake.fake_email())

    # --- Act ---
    name = payload.name
    email = payload.email

    # --- Assert ---
    assert name
    assert "@" in email
```

**Variety booster:** Place `importorskip` at module scope and define a small wrapper or model class immediately after it, so every test in the file exercises the optional library through the same abstraction.

## pytest.mark.xfail (Expected Failures)

[ref: #skip-xfail-mark-xfail]

`pytest.mark.xfail(reason=..., condition=..., raises=..., run=..., strict=...)` marks a test that is expected to fail.

Use `raises` to declare the expected exception, `run=False` for tests that should not execute at all, and `strict=True` so an unexpected pass becomes a failure.

```python
import pytest
from faker import Faker


MIN_NAME_LENGTH = 3
BUG_SHORT_NAME_REASON = "Bug #1234: create_user rejects names shorter than MIN_NAME_LENGTH."


@pytest.mark.xfail(
    reason=BUG_SHORT_NAME_REASON,
    strict=True,
    raises=ValueError,
)
def test_create_user_accepts_short_name(fake: Faker) -> None:
    """
    Given: generated short name and email.
    When: user is created.
    Then: created user has the short name.
    """
    # --- Arrange ---
    short_name = fake.pystr(min_chars=1, max_chars=MIN_NAME_LENGTH - 1)

    # --- Act ---
    user = create_user(  # provided by project code
        name=short_name,
        email=fake.fake_email(),
    )

    # --- Assert ---
    assert user["name"] == short_name
```

When the bug is present, the function raises `ValueError` and the test reports `XFAIL`.

When the bug is fixed, the assertion passes and `strict=True` reports `XPASS`, reminding you to remove the mark.

**Variety booster:** Use `xfail` with `strict=True` as a temporary contract for known bugs, and pair it with `raises` to ensure the failure mode does not silently change.

## xfail with condition and run=False

[ref: #skip-xfail-mark-xfail-condition-runfalse]

Use `condition=` to mark a test expected to fail only when a collection-time predicate holds.

Use `run=False` when the test must not execute but should still appear as xfail.

The predicate can be any collection-time expression, such as a `sys.version_info` check, a `sys.platform` check, or a feature flag.

```python
import pytest
from faker import Faker


MIN_NAME_LENGTH = 3
BUG_PRESENT = True
BUG_SHORT_NAME_REASON = "Bug #1234: create_user rejects names shorter than MIN_NAME_LENGTH."
BUG_ASYNC_REASON = "Bug #1235: async user creation deadlocks the runner."


@pytest.mark.xfail(
    condition=BUG_PRESENT,
    reason=BUG_SHORT_NAME_REASON,
    strict=True,
    raises=ValueError,
)
def test_create_user_accepts_short_name(fake: Faker) -> None:
    """
    Given: generated short name and email.
    When: user is created on Python below 3.12.
    Then: created user has the short name.
    """
    # --- Arrange ---
    short_name = fake.pystr(min_chars=1, max_chars=MIN_NAME_LENGTH - 1)

    # --- Act ---
    user = create_user(  # provided by project code
        name=short_name,
        email=fake.fake_email(),
    )

    # --- Assert ---
    assert user["name"] == short_name


@pytest.mark.xfail(
    run=False,
    reason=BUG_ASYNC_REASON,
)
def test_create_user_async_does_not_deadlock(fake: Faker) -> None:
    """
    Given: generated email.
    When: async user creation runs.
    Then: coroutine completes without deadlocking.
    """
    # --- Arrange ---
    email = fake.fake_email()

    # --- Act ---
    result = create_user_async(email=email)  # provided by project code

    # --- Assert ---
    assert result.is_complete
```

**Variety booster:** Combine `condition=` with `raises=` so a version-scoped xfail still pins the exact failure mode you expect.

## Imperative pytest.xfail (Runtime Expected Failure)

[ref: #skip-xfail-imperative-xfail]

`pytest.xfail(reason)` is the runtime counterpart to `pytest.mark.xfail`.

It raises an internal exception, so no code after it runs.

```python
from typing import Protocol

import pytest
from faker import Faker


MIN_SUPPORTED_API_VERSION = "3.0"
PAGINATION_XFAIL_REASON = "Server version lacks pagination support."


class _ApiClient(Protocol):
    version: str

    def list_users(self, page_size: int) -> object: ...


def pagination_xfail_reason(version: str) -> str | None:
    if version < MIN_SUPPORTED_API_VERSION:
        return PAGINATION_XFAIL_REASON
    return None


def test_new_endpoint_paginates(fake: Faker, api_client: _ApiClient) -> None:
    """
    Given: API client version is checked.
    When: users are listed with pagination.
    Then: page has a next token.
    """
    # --- Arrange ---
    reason = pagination_xfail_reason(api_client.version)
    if reason is not None:
        pytest.xfail(reason)
    page_size = fake.pyint(min_value=1, max_value=10)

    # --- Act ---
    page = api_client.list_users(page_size=page_size)

    # --- Assert ---
    assert page.next_token is not None
```

**Variety booster:** Extract the version check into a helper that returns a reason string or `None`, then call `pytest.xfail(reason)` only when the helper reports a limitation.

## Module/Class-wide pytestmark

[ref: #skip-xfail-module-class-pytestmark]

Assigning `pytestmark` at module or class scope applies the mark to every test in that scope.

This removes repetitive decorators and keeps skip reasons in one place.

```python
import os
import sys

import pytest


WINDOWS_PLATFORM = "win32"
MIGRATION_ENV_VAR = "MYAPP_RUN_LEGACY_MIGRATIONS"
MODULE_SKIP_REASON = "Unix socket support is unavailable on Windows."
CLASS_SKIP_REASON = "Legacy migration tests require explicit opt-in."
USER_TABLE_NAME = "users"


pytestmark = pytest.mark.skipif(
    sys.platform == WINDOWS_PLATFORM,
    reason=MODULE_SKIP_REASON,
)


class TestLegacyMigration:
    pytestmark = pytest.mark.skipif(
        os.getenv(MIGRATION_ENV_VAR) != "enabled",
        reason=CLASS_SKIP_REASON,
    )

    def test_migration_adds_user_table(self) -> None:
        """
        Given: legacy migration context.
        When: migration is applied.
        Then: users table exists.
        """
        # --- Arrange ---
        # Migration context provided by class pytestmark.

        # --- Act ---
        has_table = schema.has_table(USER_TABLE_NAME)  # provided by project code

        # --- Assert ---
        assert has_table
```

**Variety booster:** Use a list for `pytestmark` to apply both a skip reason and a fixture decorator or marker to every test in a class.

## Parametrized cases

[ref: #skip-xfail-parametrized-cases]

Attach `skip` or `xfail` to individual parametrized values with `pytest.param(..., marks=...)`.

This keeps the test matrix compact while recording known limitations per case.

```python
from http import HTTPStatus

import pytest
from faker import Faker


VALID_DOMAIN = "example.test"
INVALID_DOMAIN = "not_a_domain"
IPV6_DOMAIN = "[2001:db8::1]"
BUG_999_ISSUE_ID = "#999"
SKIP_IPV6_REASON = "IPv6 literal domains are not supported by the validator."


def xfail_for_issue(issue_id: str) -> pytest.MarkDecorator:
    return pytest.mark.xfail(
        reason=f"Bug {issue_id}: known limitation tracked in the issue tracker.",
        strict=True,
    )


@pytest.mark.parametrize(
    ("domain", "expected_status"),
    [
        pytest.param(VALID_DOMAIN, HTTPStatus.OK, id="valid-domain"),
        pytest.param(
            INVALID_DOMAIN,
            HTTPStatus.BAD_REQUEST,
            id="invalid-domain",
            marks=xfail_for_issue(BUG_999_ISSUE_ID),
        ),
        pytest.param(
            IPV6_DOMAIN,
            HTTPStatus.OK,
            id="ipv6-domain",
            marks=pytest.mark.skip(reason=SKIP_IPV6_REASON),
        ),
    ],
)
def test_email_domain_validation(domain: str, expected_status: HTTPStatus, fake: Faker) -> None:
    """
    Given: parametrized domain and expected HTTP status.
    When: email domain is validated.
    Then: response status matches expected.
    """
    # --- Arrange ---
    email = f"{fake.user_name()}@{domain}"

    # --- Act ---
    response = validate_email(email)  # provided by project code

    # --- Assert ---
    assert response.status_code == expected_status
```

**Variety booster:** Build reusable mark factories such as `xfail_for_issue(issue_id)` and pass them into `pytest.param` to keep the matrix readable across many tests.

## Parametrized mark factories

[ref: #skip-xfail-parametrized-mark-factories]

Reusable mark factories keep parametrized tables compact and consistent.

Define a factory that returns a mark and reuse it in every table.

```python
from http import HTTPStatus

import pytest


HEALTH_ENDPOINT = "/health"
READY_ENDPOINT = "/ready"
ISSUE_MAINTENANCE = "#1236"
SKIP_MAINTENANCE_REASON = "Endpoint is disabled during the maintenance window."


def xfail_for_issue(issue_id: str) -> pytest.MarkDecorator:
    return pytest.mark.xfail(
        reason=f"Bug {issue_id}: known limitation tracked in the issue tracker.",
        strict=True,
    )


@pytest.mark.parametrize(
    ("endpoint", "expected_status"),
    [
        pytest.param(HEALTH_ENDPOINT, HTTPStatus.OK, id="health"),
        pytest.param(
            READY_ENDPOINT,
            HTTPStatus.OK,
            id="ready",
            marks=[
                pytest.mark.skip(reason=SKIP_MAINTENANCE_REASON),
                xfail_for_issue(ISSUE_MAINTENANCE),
            ],
        ),
    ],
)
def test_status_endpoints(endpoint: str, expected_status: HTTPStatus) -> None:
    """
    Given: parametrized status endpoint.
    When: endpoint is requested.
    Then: response status matches expected.
    """
    # --- Arrange ---
    # Endpoint and expected status are provided by parametrization.

    # --- Act ---
    response = fetch_status(endpoint)  # provided by project code

    # --- Assert ---
    assert response.status_code == expected_status
```

**Variety booster:** Keep `xfail_for_issue` in a shared `tests/marks.py` module and import it wherever a known issue limits a parametrized case.

## Configuration and CLI

[ref: #skip-xfail-configuration-cli]

Make `xfail` strict by default so accidental passes surface as failures.

```toml
[tool.pytest.ini_options]
xfail_strict = true
```

Use `-rxXs` to show detailed reasons for `xfailed`, `xpassed`, and `skipped` tests in the summary.

```bash
pytest -rxXs
```

Force xfail-marked tests to run normally with `--runxfail`.

```bash
pytest --runxfail
```

**Variety booster:** Keep `xfail_strict = true` in `pyproject.toml` and require every `xfail` mark to carry a `reason` and, when possible, an expected exception.
