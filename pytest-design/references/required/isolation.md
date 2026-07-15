---
subject: "Keep tests independent of shared, mutable, external state: `yield` teardown and context managers, transactional rollback, `monkeypatch.setenv`/`delenv`/`setattr`/`setitem`/`syspath_prepend`/`chdir`, `pytest-env` in `pyproject.toml`, disable sockets with `pytest_socket.disable_socket`, fake subprocesses with `pytest-subprocess`/`fake_process`, `tmp_path`/`tmp_path_factory`; retrofit types with `monkeytype` trace corpus + `stub --diff` drift guard, lock output with `syrupy` snapshots + `path_type` matchers + JSON extension."
index:
  - anchor: isolation-core-principles
    what: "The rule that each test starts from a known clean state, depends on no other test's mutable state, rolls back database changes (via a begin/yield/rollback fixture), and leaves the environment unchanged."
    problem: "Suite shares mutable fixtures and database rows between tests, so execution order decides pass or fail and rerunning single test gives different result than full run; polluted shared row, hidden test coupling, committed write leak, unreproducible locally, fixture residue, ci-only failure."
    use_when: "Any suite with shared database, filesystem, or service state; test outcome must not depend on execution order; every fixture allocation needs guaranteed teardown path."
    avoid_when: "Test depends on rows or objects created by another test; database writes committed beyond test boundary; fixture allocates resource with no teardown or context manager."
    expected: "Tests pass in any order and alone, database changes roll back per test, and every allocated resource is deterministically torn down."
  - anchor: isolation-environment-variables
    what: "Per-test environment overrides via `monkeypatch.setenv`/`monkeypatch.delenv` (auto-reverted), plus optional global defaults through the `pytest-env` plugin's `[tool.pytest_env]`."
    problem: "Test reads configuration from process environment, and mutating `os.environ` directly leaks override into every later test within same worker process; missing variable keyerror, run-wide default layer, declared pyproject config, unicode value sweep, shell metachar value, env plugin installed."
    use_when: "Test needs specific env var present, changed, or absent; override must vanish after test; suite-wide defaults should live in declared configuration."
    avoid_when: "`os.environ` mutated directly (bypasses auto-revert); `pytest-env` relied on without confirming installation (ask user when missing); per-test values stuffed into global plugin config."
    expected: "Env overrides revert automatically after each test, run-wide defaults arrive from declared plugin config, and no variable leaks into neighbors."
  - anchor: isolation-monkeypatching-global-state
    what: "Using the built-in `monkeypatch` fixture (`setattr`, `setitem`, `setenv`/`delenv`, `syspath_prepend`, `chdir`) to temporarily modify global state with automatic revert."
    problem: "Code under test depends on mutable global (module attribute, dict entry, sys.path, cwd, env var), and direct assignment in one test poisons runtime state for everything executing afterward; leftover patched value, silent global drift, manual revert gap, import path pollution, working dir leak, class attribute swap."
    use_when: "Global attribute, mapping entry, path entry, working directory, or env var must differ for one test only; automatic revert after test is required; patch target is known by dotted path."
    avoid_when: "Direct assignment or manual mutation used instead of fixture (no automatic revert); patch left active beyond its test; string target misspelled and silently failing `raising=True` check."
    expected: "Every temporary mutation is scoped to one test and reverted automatically, leaving runtime globals untouched for whatever runs next."
  - anchor: isolation-network-isolation-pytest-socket
    what: "Disabling socket access globally in the unit-test conftest with `pytest-socket` (`pytest_socket.disable_socket()` in `pytest_configure`), then selectively re-enabling per test via `@pytest.mark.usefixtures('socket_enabled')` or `@pytest.mark.allow_hosts([...])`."
    problem: "Unit suite accidentally performs real network call, making run slow, flaky under outages, and dependent on external services that may not exist in CI; loopback-only exception, internet test misplaced, dns resolution blocked, socket plugin installed, e2e layer relocation."
    use_when: "Unit layer must guarantee zero network access; one test needs loopback or specific host exception; internet-dependent coverage exists and must land in correct layer."
    avoid_when: "Real network call tolerated inside unit test; public-internet test placed in unit layer instead of integration/e2e; `pytest-socket` assumed installed without verification."
    expected: "Socket access is disabled suite-wide by default, exceptions stay scoped per test or per allow-listed host, and internet coverage lives in higher layers."
  - anchor: isolation-subprocess-isolation
    what: "Replacing real shell execution with `pytest-subprocess`'s `fake_process` (register expected commands and outputs) or, when that is too heavy, monkeypatching `subprocess.run`/`subprocess.Popen`."
    problem: "Code under test shells out to real command, so suite slows down, depends on installed binaries, and can damage developer machine or CI agent on destructive flags; nonzero exit path, timeout branch, unregistered command error, stdout stderr capture, lighter stub fallback, subprocess plugin installed."
    use_when: "Unit test would spawn real process; command output, exit code, and timeout behavior must be declared deterministically; lighter monkeypatched stub suffices when plugin is unavailable."
    avoid_when: "Shelling out for real inside unit test; unregistered invocation allowed to slip through silently; `pytest-subprocess` assumed present without install check."
    expected: "No real process spawns during unit run; success, non-zero exit, and timeout paths are covered through declared fake or stubbed behavior."
  - anchor: isolation-filesystem-isolation
    what: "Using `tmp_path` for a per-test unique temporary directory (removed after the run) and `tmp_path_factory` for directories that must outlive a single test."
    problem: "Test writes scratch files, and shared or repository-relative path collides with other tests and pollutes working tree; outliving single test, nested tree generation, symlink edge case, path normalization stress, session-scoped asset, fixture-shared directory."
    use_when: "Test needs writable scratch directory unique to itself; artifact must survive across several tests or session; repository and shared paths are off limits."
    avoid_when: "Writes land in repository or any shared/global path; `tmp_path` used for directory needed beyond one test (reach for `tmp_path_factory`); cleanup left to manual deletion."
    expected: "Each test writes under own auto-removed directory, longer-lived artifacts come from explicit factory, and working tree stays clean."
  - anchor: isolation-runtime-type-collection-monkeytype
    what: "Using the pytest suite as a trace corpus to retrofit type annotations onto legacy/dynamic code, with the trace store isolated under `tmp_path` and the CLI faked via `pytest-subprocess`."
    problem: "Legacy dynamic module resists static type inference, and retrofitting annotations needs runtime-observed call data, yet naive trace run writes its sqlite store into repository tree; accidental in-place rewrite, stub stdout capture, inferred signature check, per-module retrofit sweep."
    use_when: "Annotations must be retrofitted onto dynamic or legacy code; test suite can serve as tracing corpus; trace artifacts and CLI interaction must stay off repository."
    avoid_when: "Trace store allowed into repository or shared between tests; `monkeytype apply` executed against repo in unit test; real tracing performed instead of faked CLI."
    expected: "Trace artifacts stay scoped to `tmp_path` via fixture cleanup, stub output is read from faked CLI, and repository remains untouched."
  - anchor: isolation-annotation-drift-guard-monkeytype
    what: "Asserting that `monkeytype stub --diff` is empty (preserving vs ignoring existing annotations), proving checked-in annotations still match runtime-observed types."
    problem: "Checked-in annotations age silently as implementation evolves, and without guard drift between declared signatures and runtime-observed types surfaces only as confusing production type errors; preserve existing annotations, stub diff non-empty, apply rewrite temptation, ci gate placement, signature changed output."
    use_when: "Module carries checked-in annotations worth guarding; runtime tracing corpus already exists; build should fail loudly when signatures stop matching observed types."
    avoid_when: "`monkeytype apply` run inside unit test to silence diff (rewrites repo); non-empty diff allowed through build; guard executed without isolated trace store."
    expected: "Clean state yields empty `--diff` and green build, while any drift produces non-empty diff that fails loudly without rewriting repository."
  - anchor: isolation-stub-generation-sourceless-monkeytype
    what: "Emitting `.pyi` stubs for C extensions or modules without Python source by reading `monkeytype stub` from stdout and writing the result under `tmp_path`."
    problem: "C extension or shipped-binary module exposes no Python source for static analysis, so only recorded runtime calls reveal its signatures, and materializing `.pyi` must not rewrite repository; per-extension stub sweep, expected symbol assertion, type stub deliverable, binary module documentation."
    use_when: "Module lacks Python source (C extension, binary wheel); signatures must come from recorded calls; stub output belongs under temp directory, never inside repository."
    avoid_when: "In-place rewrite via `monkeytype apply` attempted against repository; stub written into source tree; generation attempted without recorded trace data."
    expected: "`.pyi` file materializes under `tmp_path` per sourceless module, content comes from recorded calls, and repository is never rewritten."
  - anchor: isolation-snapshot-syrupy
    what: "Locking a large or deeply nested output with `assert value == snapshot` (typed as `syrupy.assertion.SnapshotAssertion`), generating/refreshing via the CLI `pytest --snapshot-update`, and committing `__snapshots__/`."
    problem: "Large deeply nested output makes hand-written expected value unreadable and brittle on every intentional change, while unmanaged snapshot without seeding flakes across runs; committed snapshot dir, unique name per assert, regression radar, partial shape pin, multi-snapshot test."
    use_when: "Output is large, nested, and stable enough to pin wholesale; reviewing committed baseline beats maintaining literal; intentional changes deserve explicit refresh step."
    avoid_when: "`--snapshot-update` executed inside test body; snapshot name reused within one test; non-reproducible output committed as baseline (seed or freeze first); giant literal maintained where baseline fits better."
    expected: "Large outputs are pinned by committed reproducible baselines whose diffs flag regressions, refreshed only through deliberate CLI update."
  - anchor: isolation-snapshot-deterministic-matchers
    what: "Sanitizing dynamic fields (server ids, timestamps, UUIDs) in a snapshot with `syrupy.matchers.path_type` (and `replacer`/`compose_matchers`) so `== snapshot` stays deterministic."
    problem: "Payload carries server-generated ids, timestamps, and UUIDs that change every run, so raw snapshot comparison fails despite unchanged contract; contract versus churn, matcher semantics unverified, seeded controlled field, field without contract, controlled versus dynamic split."
    use_when: "Snapshot payload mixes controllable fields with server-generated ones; raw comparison flakes every run; matcher behavior gets re-verified against installed version and payload shape."
    avoid_when: "Raw `== snapshot` asserted on payload with per-run fields; matchers applied to fields seeding or freezing already controls (over-sanitization hides real changes); matcher semantics assumed without verification."
    expected: "Snapshots stay stable across runs: controlled fields pinned by seeding, dynamic fields matched by type or replaced with stable tokens."
  - anchor: isolation-snapshot-json
    what: "A `snapshot_json` fixture built with `snapshot.with_defaults(extension_class=JSONSnapshotExtension)` so JSON-shaped payloads are stored as readable, diff-friendly JSON instead of Python repr."
    problem: "JSON-shaped API response persisted as Python repr snapshot reads poorly in review and produces noisy diffs that hide real contract changes; empty single multi sweep, nested payload variants, seeded response data, diff review ceremony."
    use_when: "Payload is JSON-shaped and snapshot review happens in diffs; readable storage format matters to reviewers; response data stays reproducible through seeding."
    avoid_when: "Python repr storage kept although JSON extension exists; unstable unseeded JSON committed; `snapshot_json` fixture rebuilt per test instead of shared `with_defaults` definition."
    expected: "API responses snapshot as readable, diff-friendly JSON through dedicated extension fixture, staying stable across seeded runs."
libraries:
  - pytest-env
  - pytest-socket
  - pytest-subprocess
  - python-monkeytype
  - syrupy
---

# ISOLATION & ENVIRONMENT — CORE

## Core Isolation Principles

[ref: #isolation-core-principles]

Database changes must be rolled back or executed inside isolated transactions.
Use a fixture that begins a transaction, yields the connection, and rolls back during teardown.

```python
from collections.abc import Iterator

import pytest
from sqlalchemy import Connection


@pytest.fixture
def db_transaction(db_engine: Connection) -> Iterator[Connection]:
    conn = db_engine.connect()
    transaction = conn.begin()
    yield conn
    transaction.rollback()
    conn.close()
```

Any fixture that allocates resources must clean them up via `yield` teardown or a context manager.
The teardown block runs even if the test raises an exception.

```python
from collections.abc import Iterator

import pytest
from faker import Faker


@pytest.fixture
def isolated_schema(fake: Faker) -> Iterator[str]:
    name = fake.word()
    create_schema(name)
    yield name
    drop_schema(name)
```

**Variety booster:** Parametrize a cleanup fixture over resource types and failure modes so the same test body exercises rollback, deletion, and close paths.

## Environment Variables

[ref: #isolation-environment-variables]

```python
import os
import re

import pytest
from faker import Faker


def test_client_uses_env_base_url(monkeypatch: pytest.MonkeyPatch, fake: Faker) -> None:
    """
    Given: environment variable API_BASE_URL is set to a generated URL.
    When: client is built.
    Then: client uses the configured base URL.
    """
    # --- Arrange ---
    base_url = fake.url()
    monkeypatch.setenv("API_BASE_URL", base_url)

    # --- Act ---
    client = build_client()

    # --- Assert ---
    assert client.base_url == base_url


def test_missing_env_raises_on_access(monkeypatch: pytest.MonkeyPatch, fake: Faker) -> None:
    """
    Given: environment variable is set and then removed.
    When: the variable is accessed.
    Then: KeyError is raised.
    """
    # --- Arrange ---
    var_name = fake.word().upper()
    monkeypatch.setenv(var_name, fake.word())
    monkeypatch.delenv(var_name)

    # --- Act ---
    with pytest.raises(KeyError, match=re.escape(var_name)):
        _ = os.environ[var_name]

    # --- Assert ---
    # Exception raised as expected; assertion handled by pytest.raises context.
```

For environment variables needed across the whole run, the `pytest-env` plugin can set them via `pyproject.toml`.
Before relying on it, verify the plugin is installed; if it is missing, ask the user.
Replace literal values with references to application-level configuration sources.

```toml
[tool.pytest_env]
API_BASE_URL = "http://api.example.test"
```

**Variety booster:** Parametrize the variable name and generated value to cover empty strings, unicode, very long strings, and values that look like shell meta-characters in a single test.

## Monkeypatching Global State

[ref: #isolation-monkeypatching-global-state]

Use `monkeypatch.setattr` to replace module attributes, class attributes, or functions.

```python
import pytest
from faker import Faker


def test_service_uses_patched_timeout(monkeypatch: pytest.MonkeyPatch, fake: Faker) -> None:
    """
    Given: app.config.DEFAULT_TIMEOUT is patched to a generated value.
    When: service is instantiated.
    Then: service uses the patched timeout.
    """
    # --- Arrange ---
    timeout = fake.pyfloat(min_value=0.1, max_value=10.0)
    monkeypatch.setattr("app.config.DEFAULT_TIMEOUT", timeout)

    # --- Act ---
    service = Service()

    # --- Assert ---
    assert service.timeout == timeout
```

Use `monkeypatch.setitem` to override dictionary entries.

```python
import pytest
from faker import Faker


def test_handler_uses_patched_setting(monkeypatch: pytest.MonkeyPatch, fake: Faker) -> None:
    """
    Given: config dictionary has a patched entry.
    When: setting is resolved.
    Then: patched value is returned.
    """
    # --- Arrange ---
    config = app.settings.load_defaults()
    key = fake.word()
    value = fake.sentence()
    monkeypatch.setitem(config, key, value)

    # --- Act ---
    resolved = app.settings.resolve(config)

    # --- Assert ---
    assert resolved[key] == value
```

Use `monkeypatch.setenv` and `monkeypatch.delenv` for environment variables, as shown in the Environment Variables section.

Use `monkeypatch.syspath_prepend` to inject a temporary directory into `sys.path`.

```python
import pathlib
import sys

import pytest
from faker import Faker


def test_loader_finds_local_package(monkeypatch: pytest.MonkeyPatch, fake: Faker, tmp_path: pathlib.Path) -> None:
    """
    Given: temporary directory is prepended to sys.path.
    When: sys.path is inspected.
    Then: directory is present.
    """
    # --- Arrange ---
    local_dir = tmp_path / fake.word()
    local_dir.mkdir()
    monkeypatch.syspath_prepend(str(local_dir))

    # --- Act ---
    path_entries = sys.path

    # --- Assert ---
    assert str(local_dir) in path_entries
```

Use `monkeypatch.chdir` to change the working directory for one test.

```python
import pathlib

import pytest
from faker import Faker


def test_loader_resolves_relative_to_workdir(monkeypatch: pytest.MonkeyPatch, fake: Faker, tmp_path: pathlib.Path) -> None:
    """
    Given: working directory is changed to a generated path.
    When: current working directory is queried.
    Then: generated path is returned.
    """
    # --- Arrange ---
    workdir = tmp_path / fake.word()
    workdir.mkdir()
    monkeypatch.chdir(workdir)

    # --- Act ---
    cwd = pathlib.Path.cwd()

    # --- Assert ---
    assert cwd == workdir
```

**Variety booster:** Create a small `patch_factory` fixture that yields several targets so one test exercises `setattr`, `setitem`, and `delenv` paths without duplicating setup.

## Network Isolation with pytest-socket

[ref: #isolation-network-isolation-pytest-socket]

```python
import pytest
import pytest_socket


def pytest_configure(config: pytest.Config) -> None:
    pytest_socket.disable_socket()
```

If a specific unit test genuinely needs socket access, re-enable it for that test only.

```python
from http import HTTPStatus

import pytest


@pytest.mark.usefixtures("socket_enabled")
def test_local_server_health_check() -> None:
    """
    Given: local server is running with socket access enabled.
    When: health endpoint is requested.
    Then: OK status is returned.
    """
    # --- Arrange ---
    endpoint = app.server.HEALTH_ENDPOINT

    # --- Act ---
    response = local_server.get(endpoint)

    # --- Assert ---
    assert response.status_code == HTTPStatus.OK
```

To allow only specific hosts, use the `allow_hosts` marker.

```python
import pytest


LOOPBACK_HOSTS = ["127.0.0.1", "::1"]


@pytest.mark.allow_hosts(LOOPBACK_HOSTS)
def test_resolver_hits_loopback() -> None:
    """
    Given: resolver is allowed to query loopback hosts.
    When: localhost is resolved.
    Then: loopback address is returned.
    """
    # --- Arrange ---
    host = "localhost"

    # --- Act ---
    result = resolver.resolve(host)

    # --- Assert ---
    assert result == "127.0.0.1"
```

If a test needs the public internet, it belongs in an integration or end-to-end layer, not in unit tests.

**Variety booster:** Combine `pytest-socket` with `@pytest.mark.parametrize` to run the same assertion against disabled socket, loopback-only, and explicitly allowed hosts.

## Subprocess Isolation

[ref: #isolation-subprocess-isolation]

```python
import pytest
from faker import Faker
from pytest_subprocess import FakeProcess


def test_updater_reads_version(fake_process: FakeProcess, fake: Faker) -> None:
    """
    Given: subprocess is registered to return a generated version.
    When: updater reads version.
    Then: returned result contains the version.
    """
    # --- Arrange ---
    version = fake.numerify("#.#.#")
    fake_process.register_subprocess(
        updater.VERSION_COMMAND,
        stdout=f"v{version}\n".encode(),
    )

    # --- Act ---
    result = updater.get_version()

    # --- Assert ---
    assert version in result
```

When `pytest-subprocess` is unavailable or too heavy, mock `subprocess.run` or `subprocess.Popen` directly with `monkeypatch`.

```python
from collections.abc import Sequence
from typing import Any

import pytest
import subprocess
from faker import Faker


EXIT_SUCCESS = 0


def test_executor_returns_stdout_on_success(monkeypatch: pytest.MonkeyPatch, fake: Faker) -> None:
    """
    Given: subprocess.run is patched to return generated stdout.
    When: executor runs a command.
    Then: executor returns the expected stdout.
    """
    # --- Arrange ---
    expected_stdout = fake.sentence()

    def fake_run(cmd: Sequence[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(args=list(cmd), returncode=EXIT_SUCCESS, stdout=expected_stdout)

    monkeypatch.setattr(subprocess, "run", fake_run)

    # --- Act ---
    result = executor.run([fake.word(), fake.word()])

    # --- Assert ---
    assert result.stdout == expected_stdout
```

**Variety booster:** Register multiple subprocess behaviors in one test, or parametrize `returncode`, `stdout`, and `stderr` to cover success, non-zero exit, and timeout paths with the same high-level assertion.

## Filesystem Isolation

[ref: #isolation-filesystem-isolation]

```python
import pathlib
import re

import pytest
from faker import Faker


def test_writer_creates_file(tmp_path: pathlib.Path, fake: Faker) -> None:
    """
    Given: target path and content are generated.
    When: writer writes the file.
    Then: file contains the expected content.
    """
    # --- Arrange ---
    extension = fake.file_extension()
    target = tmp_path / fake.file_name(extension=extension)
    content = fake.paragraph()

    # --- Act ---
    writer.write(target, content)

    # --- Assert ---
    assert target.read_text() == content


def test_reader_rejects_missing_file(tmp_path: pathlib.Path, fake: Faker) -> None:
    """
    Given: missing file path is generated.
    When: reader loads the file.
    Then: FileNotFoundError is raised with path in message.
    """
    # --- Arrange ---
    extension = fake.file_extension()
    missing = tmp_path / fake.file_name(extension=extension)

    # --- Act ---
    with pytest.raises(FileNotFoundError, match=re.escape(str(missing))):
        reader.load(missing)

    # --- Assert ---
    # Exception raised as expected; assertion handled by pytest.raises context.
```

Use `tmp_path_factory` for directories that must outlive a single test.

```python
import pathlib

import pytest
from faker import Faker


@pytest.fixture
def shared_asset(tmp_path_factory: pytest.TempPathFactory, fake: Faker) -> pathlib.Path:
    root = tmp_path_factory.mktemp("assets")
    extension = fake.file_extension()
    asset = root / fake.file_name(extension=extension)
    asset.write_text(fake.paragraph())
    return asset
```

**Variety booster:** Generate nested directory trees, relative paths, and symlink edge cases through a faker-driven path factory to stress path normalization and traversal logic with minimal additional tests.

## Runtime Type Collection with monkeytype

[ref: #isolation-runtime-type-collection-monkeytype]

```python
import pathlib
import re
import subprocess
from collections.abc import Iterator

import pytest
from faker import Faker
from pytest_subprocess import FakeProcess


TRACE_DB_FILENAME = "monkeytype.sqlite3"
MONKEYTYPE_COMMAND = "monkeytype"
EXIT_SUCCESS = 0


@pytest.fixture
def isolated_trace_store(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> Iterator[pathlib.Path]:
    monkeypatch.chdir(tmp_path)
    db_path = tmp_path / TRACE_DB_FILENAME
    yield db_path
    if db_path.exists():
        db_path.unlink()


def test_stub_is_generated_from_isolated_trace_store(
    fake_process: FakeProcess,
    isolated_trace_store: pathlib.Path,
    tmp_path: pathlib.Path,
    fake: Faker,
) -> None:
    """
    Given: the working directory is redirected to a temporary path and the CLI is faked.
    When: a stub is generated for a traced module.
    Then: the trace database is scoped to tmp_path and the inferred return type is emitted.
    """
    # --- Arrange ---
    module_name = fake.word()
    inferred_return = fake.word()
    fake_process.register_subprocess(
        [MONKEYTYPE_COMMAND, "stub", module_name],
        stdout=f"def run(x: int) -> {inferred_return}: ...\n".encode(),
        returncode=EXIT_SUCCESS,
    )

    # --- Act ---
    completed = subprocess.run(
        [MONKEYTYPE_COMMAND, "stub", module_name],
        capture_output=True,
        check=True,
    )

    # --- Assert ---
    assert isolated_trace_store.is_relative_to(tmp_path)
    assert re.search(rf"->\s+{re.escape(inferred_return)}", completed.stdout.decode())
```

**Variety booster:** Parametrize over target modules and the expected inferred return type so one test verifies trace-store isolation and stub readout for every module slated for retrofit.

## Annotation-Drift Guard with monkeytype

[ref: #isolation-annotation-drift-guard-monkeytype]

```python
import pathlib
import subprocess

import pytest
from faker import Faker
from pytest_subprocess import FakeProcess


MONKEYTYPE_COMMAND = "monkeytype"
EXIT_SUCCESS = 0


def test_checked_in_annotations_match_runtime(
    fake_process: FakeProcess,
    isolated_trace_store: pathlib.Path,
    tmp_path: pathlib.Path,
    fake: Faker,
) -> None:
    """
    Given: the trace store is isolated and the preserving-versus-ignoring diff is empty.
    When: the drift guard runs monkeytype stub --diff for a module.
    Then: the command exits successfully and emits no diff output.
    """
    # --- Arrange ---
    module_name = fake.word()
    fake_process.register_subprocess(
        [MONKEYTYPE_COMMAND, "stub", "--diff", module_name],
        stdout=b"",
        returncode=EXIT_SUCCESS,
    )

    # --- Act ---
    completed = subprocess.run(
        [MONKEYTYPE_COMMAND, "stub", "--diff", module_name],
        capture_output=True,
        check=True,
    )

    # --- Assert ---
    assert isolated_trace_store.is_relative_to(tmp_path)
    assert completed.stdout == b""


def test_drift_guard_flags_stale_annotations(
    fake_process: FakeProcess,
    isolated_trace_store: pathlib.Path,
    fake: Faker,
) -> None:
    """
    Given: the preserving-versus-ignoring diff is non-empty.
    When: the drift guard runs monkeytype stub --diff for a module.
    Then: the emitted diff contains the changed signature.
    """
    # --- Arrange ---
    module_name = fake.word()
    new_param = fake.word()
    fake_process.register_subprocess(
        [MONKEYTYPE_COMMAND, "stub", "--diff", module_name],
        stdout=f"-def run(x):\n+def run(x: int, {new_param}: str):\n".encode(),
        returncode=EXIT_SUCCESS,
    )

    # --- Act ---
    completed = subprocess.run(
        [MONKEYTYPE_COMMAND, "stub", "--diff", module_name],
        capture_output=True,
        check=True,
    )

    # --- Assert ---
    assert new_param.encode() in completed.stdout
```

Reuse the `isolated_trace_store` fixture from the Runtime Type Collection section so the path-under-`tmp_path` invariant is asserted once and shared.

**Variety booster:** Parametrize over modules and over empty versus non-empty diffs so one body proves the guard both passes clean builds and fails on drift.

## Stub Generation for Sourceless Modules

[ref: #isolation-stub-generation-sourceless-monkeytype]

```python
import pathlib
import subprocess

import pytest
from faker import Faker
from pytest_subprocess import FakeProcess


MONKEYTYPE_COMMAND = "monkeytype"
EXIT_SUCCESS = 0
STUB_SUFFIX = ".pyi"


def test_pyi_stub_is_written_without_touching_repo(
    fake_process: FakeProcess,
    isolated_trace_store: pathlib.Path,
    tmp_path: pathlib.Path,
    fake: Faker,
) -> None:
    """
    Given: the trace store is isolated and the CLI returns a generated stub on stdout.
    When: a .pyi is materialized for a sourceless extension module via monkeytype stub.
    Then: the stub file is written under tmp_path and the repository is never rewritten.
    """
    # --- Arrange ---
    module_name = fake.word()
    symbol = fake.word()
    fake_process.register_subprocess(
        [MONKEYTYPE_COMMAND, "stub", module_name],
        stdout=f"def {symbol}(x: bytes) -> int: ...\n".encode(),
        returncode=EXIT_SUCCESS,
    )

    # --- Act ---
    completed = subprocess.run(
        [MONKEYTYPE_COMMAND, "stub", module_name],
        capture_output=True,
        check=True,
    )
    stub_path = tmp_path / f"{module_name}{STUB_SUFFIX}"
    stub_path.write_text(completed.stdout.decode())

    # --- Assert ---
    assert isolated_trace_store.is_relative_to(tmp_path)
    assert stub_path.is_relative_to(tmp_path)
    assert stub_path.read_text().startswith(f"def {symbol}")
```

**Variety booster:** Parametrize over extension module names and expected stub symbols so one test covers `.pyi` materialization for every sourceless module without touching the repo.

## Snapshot Isolation with syrupy

[ref: #isolation-snapshot-syrupy]

```python
from datetime import UTC, datetime

import pytest
from faker import Faker
from syrupy.assertion import SnapshotAssertion


SEED = 20260710
FROZEN_NOW = datetime(2026, 7, 10, 10, 30, 0, tzinfo=UTC)
REPORT_LINE_COUNT = 3


def build_report(*, title: str, owner: str, generated_at: str, lines: list[str]) -> dict[str, object]:
    return {"title": title, "owner": owner, "generated_at": generated_at, "lines": lines}


def test_large_report_is_locked_by_snapshot(fake: Faker, snapshot: SnapshotAssertion) -> None:
    """
    Given: faker is seeded and the clock is frozen so the report is reproducible.
    When: the large nested report is rendered.
    Then: the full shape and a focused view are locked under distinct snapshot names.
    """
    # --- Arrange ---
    fake.seed_instance(SEED)
    generated_at = FROZEN_NOW.isoformat()

    # --- Act ---
    report = build_report(
        title=fake.sentence(),
        owner=fake.email(),
        generated_at=generated_at,
        lines=[fake.sentence() for _ in range(REPORT_LINE_COUNT)],
    )

    # --- Assert ---
    assert report == snapshot(name="report-full")
    assert report["lines"] == snapshot(name="report-lines-only")
```

Multiple snapshots per test are supported, but a name must not be reused within a single test.

**Variety booster:** Parametrize the builder over empty, single, and many-line payloads so one test pins the shape across sizes without extra assertions.

## Deterministic Snapshots with Matchers

[ref: #isolation-snapshot-deterministic-matchers]

```python
from datetime import UTC, datetime
from uuid import uuid4

import pytest
from faker import Faker
from syrupy.assertion import SnapshotAssertion
from syrupy.matchers import path_type


SEED = 20260710
NOTE_COUNT = 2


def build_event(*, actor: str, notes: list[str]) -> dict[str, object]:
    return {
        "request_id": str(uuid4()),
        "created_at": datetime.now(tz=UTC).isoformat(),
        "actor": actor,
        "notes": notes,
    }


def test_dynamic_payload_snapshot_is_deterministic(fake: Faker, snapshot: SnapshotAssertion) -> None:
    """
    Given: faker is seeded so the controlled fields are reproducible.
    When: an event with server-generated id and timestamp is snapshot with type matchers.
    Then: the snapshot stays stable across runs despite the dynamic fields.
    """
    # --- Arrange ---
    fake.seed_instance(SEED)

    # --- Act ---
    event = build_event(actor=fake.email(), notes=[fake.sentence() for _ in range(NOTE_COUNT)])

    # --- Assert ---
    assert event == snapshot(matcher=path_type({"request_id": (str,), "created_at": (str,)}))
```

Use a `replacer` in `path_type` to substitute a stable token for a dynamic value, or drop an irrelevant field entirely when it carries no contract.

**Variety booster:** Parametrize the set of matched paths so one test verifies pinning by type versus replacing by `replacer` across the same payload shape.

## JSON Snapshots via JSONSnapshotExtension

[ref: #isolation-snapshot-json]

```python
import pytest
from faker import Faker
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.json import JSONSnapshotExtension


SEED = 20260710
ITEM_COUNT = 2


@pytest.fixture
def snapshot_json(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    return snapshot.with_defaults(extension_class=JSONSnapshotExtension)


def build_api_response(*, trace: str, items: list[dict[str, object]]) -> dict[str, object]:
    return {"trace": trace, "items": items}


def test_api_response_snapshot_is_readable_json(fake: Faker, snapshot_json: SnapshotAssertion) -> None:
    """
    Given: faker is seeded so the API response is reproducible.
    When: the response is asserted against the JSON snapshot extension.
    Then: the snapshot is stored as readable JSON for review.
    """
    # --- Arrange ---
    fake.seed_instance(SEED)

    # --- Act ---
    response = build_api_response(
        trace=fake.uuid4(),
        items=[{"sku": fake.bothify(text="SKU-#####"), "qty": fake.pyint(min_value=1, max_value=9)} for _ in range(ITEM_COUNT)],
    )

    # --- Assert ---
    assert response == snapshot_json
```

**Variety booster:** Parametrize item counts and nested shapes so one JSON snapshot test covers empty, single, and multi-item responses.
