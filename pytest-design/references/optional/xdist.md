---
subject: "Parallelize with `pytest-xdist` only after proving isolation: `-n auto`/`logical`/`<n>`, start `--dist=loadfile` then `load`/`worksteal`/`loadscope`/`loadgroup` with `@pytest.mark.xdist_group`, a `serial` marker run separately via `-p no:xdist`, once-per-session fixtures via `filelock`+`worker_id`+`tmp_path_factory`, detect workers with `xdist.is_xdist_worker()`, tag resources with `testrun_uid`, coverage with `pytest-cov≥5.0`."
index:
  - anchor: xdist-basic-usage
    what: "Run the suite across workers with `-n auto`/`logical`/`N`/`0`; add xdist options to `pyproject.toml` only after proving full test isolation under parallel execution."
    problem: "Parallel run speeds suite but requires proven isolation before enabled by default; core-count workers, fixed count, disable serial, loadfile start, prove isolation first, local and ci."
    use_when: "Parallel run can speed suite, isolation must be proven first, and worker count choices plus loadfile start define safe default; core count workers, fixed count, disable serial, loadfile start, prove isolation first, local and ci."
    avoid_when: "Do not add `-n=auto` to `pyproject.toml` `addopts` before proving full isolation under parallel execution."
    expected: "The suite runs in parallel locally and in CI only after isolation is proven, with `loadfile` as the starting distribution."
  - anchor: xdist-distribution-modes
    what: "`--dist` selects how tests are assigned to workers: `load` (default), `loadfile`, `loadscope`, `loadgroup` (with `@pytest.mark.xdist_group`), `worksteal`."
    problem: "Scheduler must keep coupled tests together while still rebalancing long-tail work; keep together, loadfile, loadscope, loadgroup, worksteal, rebalance tail, widen after isolation."
    use_when: "Scheduler must keep coupled tests together, long tail work still rebalances safely, and mode choice widens after isolation proof; keep together, loadfile, loadscope, loadgroup, worksteal, rebalance tail, widen after isolation."
    avoid_when: "Do not use `load`/`worksteal` before every test is fully isolated; do not rely on `loadgroup` without the matching `@pytest.mark.xdist_group` markers."
    expected: "Coupled tests stay on one worker via the chosen mode, and the scheduler is widened only after isolation is proven."
  - anchor: xdist-serial-tests
    what: "Register a custom `serial` marker and run serial tests with `pytest -m serial -p no:xdist` and parallel tests with `pytest -m 'not serial' -n auto`."
    problem: "Some tests touch shared mutable state and cannot run concurrently; serial marker, run without plugin, rest parallel, shared state isolate, register marker, split subsets."
    use_when: "Some tests touch shared mutable state, concurrent execution would corrupt them, and serial subset splits from parallel run; serial marker, run without plugin, rest parallel, shared state isolate, register marker, split subsets."
    avoid_when: "Do not let shared-state tests run under `-n auto`; do not forget to register the `serial` marker in `pyproject.toml`."
    expected: "Shared-state tests run serially in isolation while the rest of the suite runs in parallel."
  - anchor: xdist-session-scoped-fixtures-once
    what: "Workers run in separate processes so session fixtures run once per worker by default; use `filelock` plus shared storage (`tmp_path_factory.getbasetemp().parent`) to execute them exactly once."
    problem: "Per-worker session setup duplicates expensive shared resources and races on initialization; run exactly once, file lock, shared storage, master root, worker parent, no duplicate init."
    use_when: "Session scoped setup runs per worker, expensive shared resource duplicates, and file lock plus shared storage ensures once only init; run exactly once, file lock, shared storage, master root, worker parent, no duplicate init."
    avoid_when: "Do not assume a session-scoped fixture runs once across the run under xdist — without a lock it runs once per worker."
    expected: "The shared resource is initialized exactly once across all workers and every worker receives the same path."
  - anchor: xdist-worker-identification
    what: "Detect xdist and the current worker via the `worker_id` fixture, `xdist.is_xdist_worker()`, `xdist.get_xdist_worker_id()`, and `PYTEST_XDIST_WORKER`."
    problem: "Tests managing per-worker resources must know whether under xdist and on which worker; worker id, detect plugin, master outside, per-worker naming, branch on worker, gw value."
    use_when: "Tests manage per worker resources, worker identity must be known for naming and branching, and master outside plugin behaves differently; worker id, detect plugin, master outside, per worker naming, branch on worker, gw value, xdist worker."
    avoid_when: "Do not assume `worker_id` is always a `gwN` value — it is `'master'` outside xdist."
    expected: "Tests correctly distinguish master from workers and scope per-worker resources by `worker_id`."
  - anchor: xdist-test-run-uid
    what: "Use the `testrun_uid` fixture or `PYTEST_XDIST_TESTRUNUID` to tag shared resources belonging to a single invocation; the same id is visible to every worker in the run."
    problem: "Shared resources from different invocations collide without per-run tag; per-run tag, same id all workers, namespace per invocation, suffix resource, separate runs isolated, no untagged global."
    use_when: "Shared resources from different invocations collide, per run tag namespaces them, and every worker sees same id; per run tag, same id all workers, namespace per invocation, suffix resource, separate runs isolated, no untagged global."
    avoid_when: "Do not share untagged global resource names across xdist runs."
    expected: "Every worker sees the same `testrun_uid`, and resources are namespaced per invocation."
  - anchor: xdist-coverage
    what: "Use `pytest-cov>=5.0` with `[tool.coverage.run] source` declared and run `pytest -n auto --cov=src`; pytest-cov merges per-worker data into one report."
    problem: "Coverage must collect from every worker and merge, requiring recent coverage tooling; per-worker data, merge report, source declared, version floor, accurate report, parallel coverage."
    use_when: "Coverage must collect from every worker and merge, source declaration is required, and recent coverage tooling supports parallel mode; per worker data, merge report, source declared, version floor, accurate report, parallel coverage, pytest cov."
    avoid_when: "Do not measure xdist coverage with `pytest-cov<5.0` (incomplete worker merge)."
    expected: "Per-worker coverage is collected and merged into a single accurate report under `-n auto`."
  - anchor: xdist-debugging-parallel-failures
    what: "If tests pass serially but fail under xdist, hidden shared state or ordering dependencies exist; expose them with `-n 1` or `pytest-randomly`, and run the serial subset separately."
    problem: "Parallel-only failures mask shared mutable state and ordering assumptions; reproduce single worker, randomize order, serial subset alone, hidden state, order leak, not product bug."
    use_when: "Tests pass serially but fail under xdist, hidden shared state or ordering assumptions exist, and single worker plus random order reproduces; reproduce single worker, randomize order, serial subset alone, hidden state, order leak, not product bug."
    avoid_when: "Do not treat a parallel-only failure as a product bug before proving it is not shared-state/order leakage."
    expected: "Parallel-only failures are isolated to shared state/ordering, with serial and parallel subsets each green on their own."
  - anchor: xdist-variety-booster
    what: "Rotate the distribution mode across CI runs (e.g., alternate `--dist=load` and `--dist=worksteal` on different agents/jobs) to surface hidden ordering assumptions."
    problem: "Suite passing under only one scheduler likely hides shared mutable state; rotate mode, alternate ci jobs, load versus worksteal, scheduler coupling, green across modes, prove isolation."
    use_when: "Suite passes under one scheduler only, hidden coupling may remain, and rotating modes across CI jobs exposes it; rotate mode, alternate ci jobs, load versus worksteal, scheduler coupling, green across modes, prove isolation."
    avoid_when: "Do not rely on a single distribution mode in CI; a suite green only under one scheduler is not fully isolated."
    expected: "The suite stays green across multiple distribution modes, proving isolation regardless of scheduling."
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
