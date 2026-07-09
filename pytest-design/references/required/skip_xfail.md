---
subject: "Manage environment-specific, runtime, and known-failure cases: `@pytest.mark.skip` for incompatibility, `@pytest.mark.skipif` for platform/version/env (stacked = OR), `pytest.skip` inside tests/fixtures, module-level `pytest.skip(..., allow_module_level=True)`, `pytest.importorskip` with `minversion`, `@pytest.mark.xfail(reason=..., strict=True, raises=...)`, runtime `pytest.xfail`, `pytestmark`, `pytest.param(..., marks=...)`, `xfail_strict = true`, `--runxfail`."
index:
  - anchor: skip-xfail-mark-skip
    what: "`@pytest.mark.skip(reason=...)` removes a test at collection time so it never runs."
    problem: "Some tests cannot run in given runner at all (need OS-level binary unavailable in CI), and running them errors for reasons unrelated to code under test; runner incompatible, collection remove, clear reason, reusable mark, not broken code, xfail instead."
    use_when: "Test cannot run in current runner, running would error for reasons outside code under test, and collection time skip removes it cleanly; runner incompatible, collection remove, clear reason, reusable mark, not broken code, xfail instead, skip mark."
    avoid_when: "Do not use `skip` when the code under test is broken — that is an `xfail` or a fix, not a skip."
    expected: "Runner-incompatible tests are removed at collection with a clear reason, while broken-code cases go through xfail or are fixed."
  - anchor: skip-xfail-mark-skipif
    what: "`@pytest.mark.skipif(condition, reason=...)` skips a test when a collection-time condition is true; multiple decorators combine with OR semantics."
    problem: "Platform, version, or feature gates must skip declaratively without depending on runtime fixture state; collection-time gate, or semantics, reusable marker, shared module, no fixture value, declarative skip."
    use_when: "Platform version or feature gate evaluates at collection time, runtime fixture state is unnecessary, and reusable marker shares gate across suites; collection time gate, or semantics, reusable marker, shared module, no fixture value, declarative skip, skipif."
    avoid_when: "Do not make the condition depend on fixture values — it is evaluated during collection, before fixtures exist."
    expected: "Tests skip declaratively by collection-time gates with reusable markers, and no condition depends on runtime fixture state."
  - anchor: skip-xfail-imperative-skip
    what: "Calling `pytest.skip(reason)` inside a test, fixture, or helper when the skip condition depends on runtime state; `pytest.skip(reason, allow_module_level=True)` gates a whole module."
    problem: "Some skip conditions (schema version, config value) are only knowable at runtime, after collection; runtime condition, inside test fixture, module-level gate, guard fixture, centralize check, collection-knowable declarative."
    use_when: "Skip condition depends on runtime state, collection time cannot know it, and guard fixture centralizes repeated checks; runtime condition, inside test fixture, module level gate, guard fixture, centralize check, collection knowable declarative."
    avoid_when: "Do not use `pytest.skip` for conditions knowable at collection time (use `mark.skipif`), and do not call it at module scope without `allow_module_level=True`."
    expected: "Runtime-only conditions skip via `pytest.skip` with module-level gating where needed, while collection-knowable conditions stay declarative."
  - anchor: skip-xfail-importorskip
    what: "`pytest.importorskip(module, minversion=...)` at module scope skips the entire test module if an optional dependency is missing or too old, returning the imported module for direct use."
    problem: "Tests for optional integration must no-op cleanly when dependency is absent, without failing collection; optional dependency, minversion floor, skip module, loud required missing, wrapper abstraction, clean noop."
    use_when: "Optional integration dependency may be absent, collection must not fail, and module scope skip returns clean noop when missing; optional dependency, minversion floor, skip module, loud required missing, wrapper abstraction, clean noop, importorskip."
    avoid_when: "Do not use `importorskip` for required dependencies — let those imports fail loudly so a missing requirement is visible."
    expected: "Optional-dependency test modules skip cleanly when the library is absent/old, and required dependencies still fail loud."
  - anchor: skip-xfail-mark-xfail
    what: "`@pytest.mark.xfail(reason=..., condition=..., raises=..., run=..., strict=...)` marks a test expected to fail, declaring the expected exception and whether an unexpected pass is itself a failure."
    problem: "Known bugs must document without breaking build, but resurface once fixed and must not hide changed failure mode; reason link, raises pinned, strict xpass, run false, no parking lot, failure mode pinned."
    use_when: "Known bug must document without breaking build, fix must resurface through strict xpass, and failure mode must stay pinned; reason link, raises pinned, strict xpass, run false, no parking lot, failure mode pinned, xfail mark."
    avoid_when: "Do not use `xfail` as a permanent parking lot for broken tests (fix or delete), and do not omit `raises=` — otherwise any failure counts as xfail and a changed failure mode goes unnoticed."
    expected: "Known bugs report XFAIL now and XPASS (a failure under `strict=True`) once fixed, with `raises=` pinning the expected failure mode."
  - anchor: skip-xfail-imperative-xfail
    what: "Calling `pytest.xfail(reason)` at runtime to mark the current test as expected-failure when the limitation is discovered inside the test; it raises an internal exception, so no code after it runs."
    problem: "Some expected-failure conditions (server version lacking feature) surface only at runtime; runtime discover, helper reason, no code after, internal exception, collection-knowable mark, limitation check."
    use_when: "Expected failure condition surfaces only at runtime, collection mark cannot know it, and helper returns reason only when limitation holds; runtime discover, helper reason, no code after, internal exception, collection knowable mark, limitation check, pytest xfail."
    avoid_when: "Do not place assertions after `pytest.xfail` (they never run), and do not use the runtime form when the limitation is known at collection (use `mark.xfail`)."
    expected: "Runtime-discovered limitations report as xfail via a helper-driven check, with no dead assertions after the call and collection-knowable cases using the mark."
  - anchor: skip-xfail-module-class-pytestmark
    what: "Assigning `pytestmark` (a mark or a list) at module or class scope to apply a skip/xfail (or any mark) to every test in that scope."
    problem: "Repeating same skip or xfail decorator on every test in file or class duplicates reasons and drifts out of sync; module pytestmark, class pytestmark, list combine, one reason, no repeat, no sweep unrelated."
    use_when: "Same skip or xfail repeats across file or class, reasons drift out of sync, and one scoped pytestmark applies cleanly; module pytestmark, class pytestmark, list combine, one reason, no repeat, no sweep unrelated, scoped mark."
    avoid_when: "Do not duplicate the same decorator on every test when `pytestmark` covers the scope, and do not apply a mark so broadly that it sweeps in unrelated tests."
    expected: "One `pytestmark` declaration applies the mark to a cohesive module or class, with no repeated decorators and no unrelated tests swept in."
  - anchor: skip-xfail-parametrized-cases
    what: "Attaching `pytest.mark.skip` or `pytest.mark.xfail` to individual cases via `pytest.param(..., marks=...)` so per-case limitations are recorded without splitting the matrix."
    problem: "Known limitation on one parametrized case should not force duplicating whole test or dropping case; per-case mark, param marks, compact matrix, reusable factory, no duplicate test, keep limited case."
    use_when: "One parametrized case has known limitation, duplicating whole test or dropping case is wasteful, and param marks record per case state; per case mark, param marks, compact matrix, reusable factory, no duplicate test, keep limited case."
    avoid_when: "Do not duplicate the entire test just to mark one case, and do not drop a limited case from the matrix when a per-case mark records the limitation."
    expected: "The matrix stays compact while each limited case carries its own skip/xfail mark with a reason."
  - anchor: skip-xfail-configuration-cli
    what: "Enabling `xfail_strict = true` in config and using the summary flag `-rxXs` (and `--runxfail` to force xfail-marked tests to run) to surface and validate expected failures."
    problem: "Without strict xfail, fixed bugs hide as XPASS; without reason reporting, skips and xfails are opaque in summary; xfail strict, summary reasons, runxfail force, require reason, surface xpass, opaque skip."
    use_when: "Fixed bugs hide as XPASS without strict xfail, skips and xfails are opaque without reasons, and runxfail forces marked tests to run; xfail strict, summary reasons, runxfail force, require reason, surface xpass, opaque skip."
    avoid_when: "Do not leave xfail non-strict (XPASS hides fixed bugs), and do not ship xfail marks without a `reason`."
    expected: "Accidental passes surface as failures under `xfail_strict`, skip/xfail reasons are visible in the summary, and every xfail carries a reason."
  - anchor: skip-xfail-reusable-markers
    what: "A shared module such as `tests/_compat.py` that exports reusable `skipif` mark objects so one gate covers many suites."
    problem: "Copying same skipif condition into every test file drifts out of sync and bloats suite; shared module, define once, import mark, or combine, no inline redefine, no fixture logic."
    use_when: "Same skipif condition copies into every file, drift desyncs suite, and shared module exports one reusable mark; shared module, define once, import mark, or combine, no inline redefine, no fixture logic, reusable skipif."
    avoid_when: "Do not redefine the same condition inline in each test file, and do not put fixture-dependent logic into a shared mark."
    expected: "One shared module owns every collection-time gate, and test files compose them without duplication."
  - anchor: skip-xfail-runtime-fixture-gating
    what: "Calling `pytest.skip` or `pytest.xfail` from a fixture (including an autouse guard fixture) to gate every dependent test when the condition depends on a runtime resource."
    problem: "Runtime check (schema version, service reachability) gating many tests should not duplicate into every test body; fixture gate, autouse guard, runtime resource, one check, collection-knowable declarative, no per-test duplicate."
    use_when: "Runtime resource gates many tests, duplicating check into every body wastes code, and autouse guard fixture applies one skip or xfail; fixture gate, autouse guard, runtime resource, one check, collection knowable declarative, no per test duplicate."
    avoid_when: "Do not duplicate the runtime check into every test, and do not use an autouse guard for a condition knowable at collection time."
    expected: "One fixture gates all dependent tests at runtime, and collection-knowable conditions stay declarative."
  - anchor: skip-xfail-mark-xfail-condition-runfalse
    what: "Using `condition=` on `@pytest.mark.xfail` to mark a test expected to fail only when a collection-time predicate holds, and `run=False` to skip execution while still reporting xfail."
    problem: "Some known bugs apply only on specific versions or platforms, and some broken tests crash runner and must not execute at all; condition predicate, version platform scope, run false, segfault guard, still report xfail, no runtime fixture."
    use_when: "Known bug applies only on specific version or platform, broken test may crash runner, and condition plus run false reports xfail safely; condition predicate, version platform scope, run false, segfault guard, still report xfail, no runtime fixture."
    avoid_when: "Do not use `condition=` with a runtime fixture value, and do not use `run=False` to hide a test that should be fixed."
    expected: "Version- or platform-scoped xfails are declared declaratively, and non-runnable tests still surface as xfail without executing."
  - anchor: skip-xfail-parametrized-mark-factories
    what: "Building reusable mark factories such as `xfail_for_issue(issue_id)` and attaching them (and `skip` marks) to individual `pytest.param` cases."
    problem: "Per-case limitations repeated across many parametrized tables duplicate reason strings and drift out of sync; mark factory, linked reason, reuse factory, mix skip xfail, compact table, no pasted mark."
    use_when: "Per case limitations repeat across parametrized tables, reason strings drift, and mark factory with linked issue keeps compact table; mark factory, linked reason, reuse factory, mix skip xfail, compact table, no pasted mark."
    avoid_when: "Do not paste the same `pytest.mark.xfail(reason=...)` into every table, and do not drop a limited case instead of marking it."
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
    monkeypatch: pytest.MonkeyPatch,
    fake: Faker,
) -> None:
    """
    Given: the database schema version is patched to a supported value.
    When: the schema is new enough to have the column.
    Then: a generated value is stored and retrieved.
    """
    # --- Arrange ---
    monkeypatch.setattr(
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
