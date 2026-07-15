---
subject: "Parallelize with `pytest-xdist` only after proving isolation: `-n auto`/`logical`/`<n>`, start `--dist=loadfile` then `load`/`worksteal`/`loadscope`/`loadgroup` with `@pytest.mark.xdist_group`, `serial` marker run separately via `-p no:xdist`, once-per-session fixtures via `filelock`+`worker_id`+`tmp_path_factory`, detect workers with `xdist.is_xdist_worker()`, tag resources with `testrun_uid`, coverage with `pytest-cov>=5.0`."
index:
  - anchor: xdist-basic-usage
    what: "Run the suite across workers with `-n auto`/`logical`/`N`/`0`; add xdist options to `pyproject.toml` only after proving full test isolation under parallel execution."
    problem: "Parallel execution shortens feedback but hides ordering and shared-state bugs; enabling it by default before isolation is proven causes flaky failures across CI and local runs; concurrency default, isolation gate, core choice, safe baseline, serial backup."
    use_when: "The suite is large enough for parallel speedup, isolation has already been demonstrated, and a safe serial fallback is required."
    avoid_when: "Enabling parallel execution in `addopts` before proving isolation; the suite has known shared-state or ordering dependencies."
    expected: "Parallel mode is enabled by default only after isolation proof, with a serial fallback and `loadfile` baseline."
  - anchor: xdist-distribution-modes
    what: "`--dist` selects how tests are assigned to workers: `load` (default), `loadfile`, `loadscope`, `loadgroup` (with `@pytest.mark.xdist_group`), `worksteal`."
    problem: "Scheduler choice trades coupling safety against long-tail utilization; forcing aggressive distribution before isolation groups leaks state across workers and produces nondeterministic failures; coupling boundary, utilization balance, progressive wideness, grouping contract."
    use_when: "Tests are grouped by module/class or explicit markers, long-tail runtime dominates, and isolation evidence supports moving beyond `loadfile`."
    avoid_when: "Using `load`/`worksteal` while isolation is unproven; relying on `loadgroup` without the corresponding `@pytest.mark.xdist_group` markers."
    expected: "Coupled tests stay on one worker through the chosen mode, and more aggressive schedulers are adopted only after isolation proof."
  - anchor: xdist-serial-tests
    what: "Register a custom `serial` marker and run serial tests with `pytest -m serial -p no:xdist` and parallel tests with `pytest -m 'not serial' -n auto`."
    problem: "Shared mutable resources such as file-backed state or singleton services cannot be safely mutated by concurrent tests; running them under xdist causes races and cross-test corruption; shared mutable, concurrent mutation, race window, cross-test corruption, explicit exclusion."
    use_when: "Certain tests mutate unshareable resources, concurrent execution would corrupt results, and the rest of the suite benefits from parallelization."
    avoid_when: "Running serial tests under `-n auto`; omitting marker registration in `pyproject.toml`."
    expected: "Serial tests execute in a separate non-parallel run while all other tests run concurrently."
  - anchor: xdist-session-scoped-fixtures-once
    what: "Workers run in separate processes so session fixtures run once per worker by default; use `filelock` plus shared storage (`tmp_path_factory.getbasetemp().parent`) to execute them exactly once."
    problem: "Session-scoped setup repeats on every worker, wasting time and racing to create same expensive shared artifact, corrupting template when multiple workers write without coordination; duplicate initialization, worker race, shared artifact, lock coordination, single source, template integrity."
    use_when: "A session fixture initializes an expensive template that must exist exactly once and be visible to every worker."
    avoid_when: "Assuming a session fixture runs once across the whole run under xdist; using worker-local storage as the only artifact source."
    expected: "The template is initialized once and all workers receive the same path."
  - anchor: xdist-worker-identification
    what: "Detect xdist and the current worker via the `worker_id` fixture, `xdist.is_xdist_worker()`, `xdist.get_xdist_worker_id()`, and `PYTEST_XDIST_WORKER`."
    problem: "Tests that allocate per-worker namespaces or branch on execution mode need reliable worker identity; misidentifying master process leads to duplicate work or missing resources; worker identity, execution mode, namespace allocation, master branch, resource routing."
    use_when: "Per-worker resource names or mode-specific branches are required, and master-versus-worker role must be resolved reliably."
    avoid_when: "Hard-coding a `gwN` pattern for worker identifiers; ignoring the `master` value when xdist is not active."
    expected: "Tests correctly branch between master and worker roles and scope resources by worker identifier."
  - anchor: xdist-test-run-uid
    what: "Use the `testrun_uid` fixture or `PYTEST_XDIST_TESTRUNUID` to tag shared resources belonging to a single invocation; the same id is visible to every worker in the run."
    problem: "Different test runs reuse global resource names and leave behind stale data, causing collisions and leaked state between invocations; run-level tag, shared namespace, stale data, cross-invocation collision, resource lifecycle, unique namespace."
    use_when: "Shared resources are created per invocation and must remain isolated from other runs while visible to every worker in the same run."
    avoid_when: "Using untagged global resource names across independent xdist invocations."
    expected: "Every worker sees the same run identifier and resources are namespaced per invocation."
  - anchor: xdist-coverage
    what: "Use `pytest-cov>=5.0` with `[tool.coverage.run] source` declared and run `pytest -n auto --cov=src`; pytest-cov merges per-worker data into one report."
    problem: "Coverage fragments collected by each worker must be combined accurately; outdated tooling or missing source mapping drops branches and yields incomplete merged reports; fragmented coverage, worker merge, source path, version compatibility, report completeness."
    use_when: "Coverage is measured during parallel runs and a single combined report with correct source mapping is required."
    avoid_when: "Measuring xdist coverage with `pytest-cov` below version 5.0 or without declaring `[tool.coverage.run] source`."
    expected: "Per-worker coverage fragments merge into one complete and accurate report under parallel execution."
  - anchor: xdist-debugging-parallel-failures
    what: "If tests pass serially but fail under xdist, hidden shared state or ordering dependencies exist; expose them with `-n 1` or `pytest-randomly`, and run the serial subset separately."
    problem: "Failures that appear only during parallel runs are usually caused by hidden coupling rather than product defects; treating them as ordinary bugs hides real shared-state or ordering root cause; parallel-only symptom, hidden coupling, ordering dependence, shared-state defect, diagnostic bisection."
    use_when: "Tests pass in serial mode but fail with xdist, and the cause must be isolated to ordering or shared-state assumptions."
    avoid_when: "Treating a parallel-only failure as a product bug before ruling out shared-state or ordering leakage."
    expected: "Parallel-only failures are traced to shared state or ordering assumptions, with serial and parallel subsets both green."
  - anchor: xdist-variety-booster
    what: "Rotate the distribution mode across CI runs (e.g., alternate `--dist=load` and `--dist=worksteal` on different agents/jobs) to surface hidden ordering assumptions."
    problem: "Any scheduler that always passes can mask brittle ordering assumptions; rotating distribution strategies reveals hidden coupling before it becomes flaky in production; scheduler variety, hidden coupling, brittle ordering, production flakiness, isolation validation, multi-scheduler proof."
    use_when: "The suite already passes under one scheduler and the team wants to prove robustness against different work assignment strategies."
    avoid_when: "Relying on a single distribution mode in CI; accepting a suite that only passes under one scheduler."
    expected: "The suite remains green under multiple distribution modes, confirming isolation independent of scheduling."
libraries:
  - filelock
  - pytest-cov>=5.0
  - pytest-xdist
---

# Parallel Execution with pytest-xdist

## Basic Usage

[ref: #xdist-basic-usage]

Run the suite across workers with `-n`.

```bash
pytest -n auto      # one worker per physical core
pytest -n logical   # one worker per logical core
pytest -n 4         # fixed worker count
pytest -n 0         # disables xdist; equivalent to a serial run
```

Add xdist options to `pyproject.toml` only after proving full test isolation under parallel execution.

```toml
[tool.pytest.ini_options]
addopts = [
    # ... core addopts ...
    # "-n=auto",                # parallel execution — enable after proving isolation
    "--dist=loadfile",           # xdist distribution: start here
]
```

## Distribution Modes

[ref: #xdist-distribution-modes]

`--dist` controls how tests are assigned to workers.

| Mode | Behavior |
| --- | --- |
| `load` | Default scheduler that sends each test to the next idle worker. |
| `loadfile` | Keeps all tests from one file on the same worker. |
| `loadscope` | Keeps module or class groups together. |
| `loadgroup` | Respects `@pytest.mark.xdist_group(name)`. |
| `worksteal` | Dynamically rebalances remaining work for long-tail speedups. |

Start with `loadfile` when the suite has module-level state or expensive file-scoped setup.

Move to `load` or `worksteal` after proving every test is fully isolated.

```python
import pytest
from faker import Faker


@pytest.mark.xdist_group("database")
def test_user_creation_with_group(fake: Faker) -> None:
    """
    Given: a generated email and an xdist group marker.
    When: the test runs.
    Then: the email contains an "@" symbol.
    """
    # --- Arrange ---
    email = fake.fake_email()

    # --- Assert ---
    assert "@" in email
```

## Serial Tests

[ref: #xdist-serial-tests]

Some tests cannot run concurrently because they touch shared mutable state.

Register a custom `serial` marker in `pyproject.toml`.

```toml
[tool.pytest.ini_options]
markers = [
    "serial: Tests that cannot run in parallel",
]
```

Mark the affected tests.

```python
import pytest
from faker import Faker

@pytest.mark.serial
def test_database_migration_is_idempotent(fake: Faker) -> None:
    """
    Given: a generated schema name and the serial marker.
    When: the migration is checked for idempotency.
    Then: the schema name is non-empty.
    """
    # --- Arrange ---
    schema_name = fake.word()

    # --- Assert ---
    assert schema_name
```

Run serial tests separately.

```bash
pytest -m serial -p no:xdist
pytest -m "not serial" -n auto
```

`-p no:xdist` disables the plugin for a serial-only run.

## Session-Scoped Fixtures Once

[ref: #xdist-session-scoped-fixtures-once]

xdist runs each worker in its own process, so a `session`-scoped fixture executes once per worker by default.

Use a file lock and shared storage to execute it exactly once across all workers.

```python
from pathlib import Path

import filelock
import pytest


def _create_database(db_path: Path) -> None:
    db_path.write_text("-- shared template database\n")


@pytest.fixture(scope="session")
def shared_database_template(
    tmp_path_factory: pytest.TempPathFactory,
    worker_id: str,
) -> Path:
    if worker_id == "master":
        root = tmp_path_factory.getbasetemp()
    else:
        root = tmp_path_factory.getbasetemp().parent

    lock_path = root / "db-template.lock"
    db_path = root / "db-template.sqlite"

    with filelock.FileLock(str(lock_path)):
        if not db_path.exists():
            _create_database(db_path)

    return db_path
```

The fixture returns the same path on every worker while the lock guarantees a single initializer.

## Worker Identification

[ref: #xdist-worker-identification]

Tests can detect whether they are running under xdist and on which worker.

```python
import os

import xdist
from faker import Faker


def test_worker_metadata(worker_id: str, fake: Faker) -> None:
    """
    Given: the xdist worker_id fixture and a generated account identifier.
    When: the worker metadata is inspected.
    Then: the worker_id matches the xdist environment when running under xdist.
    """
    # --- Arrange ---
    account = fake.fake_email()

    # --- Act ---
    is_worker = xdist.is_xdist_worker()

    # --- Assert ---
    assert "@" in account
    if is_worker:
        assert worker_id != "master"
        assert os.environ["PYTEST_XDIST_WORKER"] == worker_id
    else:
        assert worker_id == "master"
```

`worker_id` is `"master"` when the plugin is not active.

`xdist.get_xdist_worker_id()` returns the same value as the fixture.

## Test Run UID

[ref: #xdist-test-run-uid]

Use `testrun_uid` to tag shared resources that belong to a single invocation.

```python
import os

from faker import Faker


def test_shared_resource_is_tagged(testrun_uid: str, fake: Faker) -> None:
    """
    Given: a testrun_uid and a generated word.
    When: a shared resource name is built from both values.
    Then: the uid is non-empty, present in the environment, and the name starts with the word.
    """
    # --- Arrange ---
    word = fake.word()
    resource_name = f"{word}-{testrun_uid}"

    # --- Assert ---
    assert testrun_uid
    assert "PYTEST_XDIST_TESTRUNUID" in os.environ
    assert resource_name.startswith(word)
```

The same identifier is visible to every worker in the run.

## Coverage

[ref: #xdist-coverage]

Use `pytest-cov>=5.0` when measuring coverage under xdist.

```toml
[tool.coverage.run]
source = ["src"]
```

```bash
pytest -n auto --cov=src
```

pytest-cov collects coverage data from each worker and merges it into a single report.

## Debugging Parallel Failures

[ref: #xdist-debugging-parallel-failures]

If tests pass serially but fail with xdist, the suite has hidden shared state or ordering dependencies.

Run with `-n 1` or use `pytest-randomly` to expose ordering assumptions.

Run the serial subset separately to confirm non-parallel tests are not the cause.

## Variety Booster

[ref: #xdist-variety-booster]

Rotate the distribution mode across CI runs to surface hidden ordering assumptions.

For example, alternate `--dist=load` and `--dist=worksteal` on different agents or scheduled jobs.

A suite that only passes under one scheduler likely contains shared mutable state.
