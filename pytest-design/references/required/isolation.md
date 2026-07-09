---
subject: "Keep tests independent of shared, mutable, external state: `yield` teardown and context managers, transactional rollback, `monkeypatch.setenv`/`delenv`/`setattr`/`setitem`/`syspath_prepend`/`chdir`, `pytest-env` in `pyproject.toml`, disable sockets with `pytest_socket.disable_socket`, fake subprocesses with `pytest-subprocess`/`fake_process`, and `tmp_path`/`tmp_path_factory`; no leaked env vars, open sockets, or cross-test pollution."
index:
  - anchor: isolation-core-principles
    what: "The rule that each test starts from a known clean state, depends on no other test's mutable state, rolls back database changes (via a begin/yield/rollback fixture), and leaves the environment unchanged."
    problem: "Shared mutable state between tests creates order-dependent flaky failures hard to reproduce; clean state, no cross-test state, rollback per test, resource teardown, any order pass, deterministic."
    use_when: "Shared mutable state creates order dependent failures, each test must start clean, and rollback plus teardown leaves environment unchanged; clean state, no cross test state, rollback per test, resource teardown, any order pass, deterministic."
    avoid_when: "Never let a test depend on mutable state created by another test, never leave database changes committed after a test, and never allocate resources in a fixture without teardown."
    expected: "Tests pass in any order and in isolation, database state is rolled back per test, and every allocated resource is torn down deterministically."
  - anchor: isolation-environment-variables
    what: "Per-test environment overrides via `monkeypatch.setenv`/`monkeypatch.delenv` (auto-reverted), plus optional global defaults through the `pytest-env` plugin's `[tool.pytest_env]`."
    problem: "Tests need controlled environment without leaking changes into process for later tests; per-test override, auto revert, run-wide default, no direct environ, declared config, no leaked var."
    use_when: "Environment values need per test control, direct environ mutation leaks into later tests, and declared defaults cover run wide config; per test override, auto revert, run wide default, no direct environ, declared config, no leaked var."
    avoid_when: "Do not mutate `os.environ` directly (it leaks across tests), and do not rely on `pytest-env` without confirming it is installed (ask the user if missing)."
    expected: "Per-test env changes vanish after the test, run-wide defaults come from declared config, and no environment state leaks between tests."
  - anchor: isolation-monkeypatching-global-state
    what: "Using the built-in `monkeypatch` fixture (`setattr`, `setitem`, `setenv`/`delenv`, `syspath_prepend`, `chdir`) to temporarily modify global state with automatic revert."
    problem: "Tests must alter globals (attributes, dicts, env, sys path, cwd) without poisoning runtime for subsequent tests; temporary global, auto revert, setattr setitem, syspath chdir, no direct assignment, never poisoned."
    use_when: "Globals such as attributes dicts env sys path or cwd must change temporarily, automatic revert prevents poisoning later tests after every test; temporary global, auto revert, setattr setitem, syspath chdir, no direct assignment, never poisoned."
    avoid_when: "Do not patch global state by direct assignment or manual mutation, which bypasses automatic revert and can poison later tests."
    expected: "Every global mutation is scoped to one test and reverted afterward, so the runtime is never poisoned for subsequent tests."
  - anchor: isolation-network-isolation-pytest-socket
    what: "Disabling socket access globally in the unit-test conftest with `pytest-socket` (`pytest_socket.disable_socket()` in `pytest_configure`), then selectively re-enabling per test via `@pytest.mark.usefixtures('socket_enabled')` or `@pytest.mark.allow_hosts([...])`."
    problem: "Unit tests must be fast and deterministic, so real network calls (slow and flaky) must be impossible by default; sockets disabled, no real network, allow host, integration layer, public internet excluded, verify install."
    use_when: "Unit tests must block real network by default, sockets stay disabled unless test explicitly allows host, and public internet stays excluded; sockets disabled, no real network, allow host, integration layer, public internet excluded, verify install."
    avoid_when: "Do not make real network calls in unit tests, do not place public-internet tests in the unit layer (they belong to integration/e2e), and do not rely on `pytest-socket` without verifying installation."
    expected: "Unit tests cannot reach the network by default, with any exception scoped to one test or an explicit allow-list, and public-internet coverage lives in higher layers."
  - anchor: isolation-subprocess-isolation
    what: "Replacing real shell execution with `pytest-subprocess`'s `fake_process` (register expected commands and outputs) or, when that is too heavy, monkeypatching `subprocess.run`/`subprocess.Popen`."
    problem: "Unit tests must never run real shell commands, which are slow, environment-dependent, and unsafe; fake process, register command, no real shell, success nonzero timeout, verify install, environment safe."
    use_when: "Unit test would run shell command, real subprocess is slow unsafe and environment dependent, and fake process registers expected command; fake process, register command, no real shell, success nonzero timeout, verify install, environment safe."
    avoid_when: "Never execute real shell commands in unit tests, and do not rely on `pytest-subprocess` without verifying it is installed."
    expected: "No unit test spawns a real process; command behavior is declared via `fake_process` or a monkeypatched stub, covering success, non-zero exit, and timeout paths."
  - anchor: isolation-filesystem-isolation
    what: "Using `tmp_path` for a per-test unique temporary directory (removed after the run) and `tmp_path_factory` for directories that must outlive a single test."
    problem: "Tests need filesystem scratch space that never collides across tests and never touches repository; per-test temp, auto removed, shared factory, no repo write, unique dir, longer-lived explicit."
    use_when: "Filesystem scratch space must stay unique per test, repository writes are forbidden, and longer lived directories need explicit factory; per test temp, auto removed, shared factory, no repo write, unique dir, longer lived explicit, tmp path."
    avoid_when: "Do not write to the repository or a shared/global path in tests, and do not use `tmp_path` for a directory that must outlive one test (use `tmp_path_factory`)."
    expected: "Each test writes only under its own auto-removed temp dir, with any longer-lived directory created explicitly via `tmp_path_factory`."
  - anchor: isolation-runtime-type-collection-monkeytype
    what: "Using the pytest suite as a trace corpus to retrofit type annotations onto legacy/dynamic code, with the trace store isolated under `tmp_path` and the CLI faked via `pytest-subprocess`."
    problem: "Static analysis cannot infer runtime types for dynamic code, but naive tracing writes store into repo and risks in-place rewrite; trace corpus, isolated store, chdir temp, fake cli, no in-place, no real tracing."
    use_when: "Dynamic code needs runtime type corpus, naive tracing writes store into repo, and isolated temp store plus faked CLI prevents in place rewrite; trace corpus, isolated store, chdir temp, fake cli, no in place, no real tracing."
    avoid_when: "Never let the trace store land in the repository or be shared across tests, and never run `monkeytype apply` against the repo in a unit test; do not perform real tracing inside the unit test."
    expected: "Tracing produces an isolated, `tmp_path`-scoped store cleaned up by the fixture, and no real tracing or in-place rewrite touches the repository during a unit test."
  - anchor: isolation-annotation-drift-guard-monkeytype
    what: "Asserting that `monkeytype stub --diff` is empty (preserving vs ignoring existing annotations), proving checked-in annotations still match runtime-observed types."
    problem: "Checked-in annotations silently drift from runtime reality as code evolves, and non-empty diff must fail build rather than hide; stub diff empty, drift fails build, preserve annotations, no apply, runtime match, fail loud."
    use_when: "Checked in annotations drift from runtime reality, diff must stay empty, and build should fail loudly on mismatch; stub diff empty, drift fails build, preserve annotations, no apply, runtime match, fail loud, annotation guard."
    avoid_when: "Never paper over a non-empty diff by running `monkeytype apply` inside a unit test, and do not let a non-empty diff pass the build."
    expected: "Clean builds yield an empty `--diff` and pass, while any annotation drift produces a non-empty diff that fails the build without rewriting the repo."
  - anchor: isolation-stub-generation-sourceless-monkeytype
    what: "Emitting `.pyi` stubs for C extensions or modules without Python source by reading `monkeytype stub` from stdout and writing the result under `tmp_path`."
    problem: "Modules with no Python source type only from recorded calls, but generating stubs must never rewrite repository in place; pyi from stdout, sourceless module, write under temp, trace isolated, no apply, c extension."
    use_when: "Sourceless or C extension module types only from recorded calls, stub generation must write under temp, and repository must stay untouched; pyi from stdout, sourceless module, write under temp, trace isolated, no apply, c extension."
    avoid_when: "Never run `monkeytype apply` (in-place rewrite) against the repository in a unit test — it is the anti-pattern here."
    expected: "A `.pyi` is materialized under `tmp_path` for each sourceless module, and the repository is never rewritten during a unit test."
  - anchor: isolation-snapshot-syrupy
    what: "Locking a large or deeply nested output with `assert value == snapshot` (typed as `syrupy.assertion.SnapshotAssertion`), generating/refreshing via the CLI `pytest --snapshot-update`, and committing `__snapshots__/`."
    problem: "Hand-writing expected values for large nested output is brittle and unreadable, while snapshots must stay reproducible and reviewable; snapshot lock, cli update, commit snapshots, seed freeze, reproducible, regression radar."
    use_when: "Large nested output needs reviewable expected value, hand written assertion is brittle, and snapshot CLI updates baselines deliberately; snapshot lock, cli update, commit snapshots, seed freeze, reproducible, regression radar, nested output."
    avoid_when: "Never run `--snapshot-update` inside a test, do not hand-write a huge expected value when a snapshot fits, do not reuse a snapshot name within one test, and do not commit a non-reproducible snapshot."
    expected: "Large outputs are pinned by committed, reproducible snapshots whose diffs act as a regression radar, with updates driven only by the CLI."
  - anchor: isolation-snapshot-deterministic-matchers
    what: "Sanitizing dynamic fields (server ids, timestamps, UUIDs) in a snapshot with `syrupy.matchers.path_type` (and `replacer`/`compose_matchers`) so `== snapshot` stays deterministic."
    problem: "Raw snapshot flakes when payload carries values changing every run that cannot be reproduced; dynamic field sanitize, type matcher, freeze seed, replacer compose, verify matcher api, stable snapshot."
    use_when: "Snapshot payload carries server ids timestamps or UUIDs, raw compare flakes, and matchers sanitize dynamic fields deterministically; dynamic field sanitize, type matcher, freeze seed, replacer compose, verify matcher api, stable snapshot."
    avoid_when: "Do not assert raw `== snapshot` on payloads with dynamic server-generated fields, do not use matchers for fields you can control (freeze/seed instead), and do not assume matcher semantics without verifying against the pinned syrupy and payload shape."
    expected: "Snapshots with dynamic fields stay stable across runs by combining seeding/freezing for controlled fields with verified type matchers for the rest."
  - anchor: isolation-snapshot-json
    what: "A `snapshot_json` fixture built with `snapshot.with_defaults(extension_class=JSONSnapshotExtension)` so JSON-shaped payloads are stored as readable, diff-friendly JSON instead of Python repr."
    problem: "API responses stored as Python repr are hard to read and diff in review; json extension, readable diff, dedicated fixture, seed reproducible, no repr, diff-friendly."
    use_when: "API response stored as Python repr is hard to review, JSON snapshot gives readable diff, and seeded data keeps reproducible; json extension, readable diff, dedicated fixture, seed reproducible, no repr, diff friendly, api payload."
    avoid_when: "Do not store JSON-shaped snapshots as Python repr when the JSON extension is available, and do not commit unstable JSON (seed faker)."
    expected: "API responses are snapshotted as readable, stable, diff-friendly JSON through a dedicated `snapshot_json` fixture."
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
