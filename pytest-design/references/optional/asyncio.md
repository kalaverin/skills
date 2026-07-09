---
subject: "Write reliable async tests: pick `pytest-asyncio` for pure asyncio or `pytest-anyio` for multi-backend, set `asyncio_mode` and matching `scope`/`loop_scope`, share event loops across async fixtures, mock coroutines with `AsyncMock`, guard hangs with `asyncio.timeout`/`pytest-timeout`, and verify gather/TaskGroup/ThreadPoolExecutor race invariants."
index:
  - anchor: asyncio-configuration
    what: "Choosing between `pytest-asyncio` and `pytest-anyio` as the single primary async test plugin for the project."
    problem: "Two async plugins installed with conflicting defaults multiply backend permutations, slow suite, and risk clashing configuration instead of one clear runner; plugin choice, single backend, default conflict, multi-backend, asyncio-only, backend portability, disable other plugin."
    use_when: "Project contains async tests and plugin choice must avoid conflicting backends while keeping one clear runner configuration; plugin choice, single backend, default conflict, asyncio only, multi backend, backend portability, disable other plugin, runner clarity."
    avoid_when: "Never install both plugins with conflicting defaults, and do not use `pytest-anyio` for a pure asyncio project only because it is newer or more generic."
    expected: "One primary async plugin is active with non-conflicting defaults; for `pytest-anyio`, `anyio_backend` starts as `['asyncio']` and adds `'trio'` only after the suite is green on asyncio."
  - anchor: asyncio-configuration
    what: "The `pytest-asyncio` setting that controls whether async tests are auto-detected (`auto`) or require an explicit marker (`strict`)."
    problem: "Leaving `asyncio_mode` unset in project with async tests lets coroutine tests get silently skipped or never awaited; auto mode, strict mode, marker boilerplate, silent skip, coroutine never awaited, discovery policy, explicit control."
    use_when: "Project contains coroutine tests and marker policy must prevent silent skips while keeping discovery explicit or automatic by design; auto mode, strict mode, marker boilerplate, silent skip, coroutine never awaited, discovery policy, explicit control, async collection."
    avoid_when: "Do not leave `asyncio_mode` unset in a project that contains async tests."
    expected: "Async tests are reliably discovered and awaited, with marker boilerplate removed in `auto` mode or explicit control retained in `strict` mode."
  - anchor: asyncio-fixtures-loop-scope
    what: "Declaring an explicit `loop_scope` on every async fixture in `pytest-asyncio>=0.23`, matched to the fixture's `scope`."
    problem: "Fixture declared `scope='session'` without `loop_scope='session'` recreates event loop for every test and breaks resources tied to original loop; loop mismatch, attached future, cross-loop resource, scope alignment, runtime error, shared loop lifetime, reused fixture."
    use_when: "Async fixture scope exceeds function scope under `pytest-asyncio>=0.23`, loop lifetime must match fixture lifetime, and resources attach to one loop; loop scope, scope alignment, session fixture, attached future, cross loop resource, shared loop lifetime, runtime error."
    avoid_when: "Do not declare a `scope='session'` fixture without `loop_scope='session'`."
    expected: "Async fixtures share the correct event loop for their scope and clean up reliably without 'attached to a different loop' errors."
  - anchor: asyncio-test-patterns
    what: "Writing async tests that run sequentially inside one event loop while exercising concurrency through coroutine primitives such as `asyncio.gather` or `asyncio.TaskGroup`."
    problem: "Calling `asyncio.run()` inside async test raises `RuntimeError` because test already runs on loop, and missing marker or wrong loop scope breaks execution; nested loop error, cooperative concurrency, gather tasks, task group, marker scope, existing loop, sequential inside loop."
    use_when: "Async test already runs on event loop and concurrency must stay cooperative inside that loop rather than nested runner; nested loop error, existing loop, cooperative concurrency, gather tasks, task group, marker scope, sequential inside loop, runtime error."
    avoid_when: "Do not call `asyncio.run()` inside an async test."
    expected: "Async tests run on the existing loop with the correct scope and verify concurrent behavior via `gather`/`TaskGroup` without nested-loop errors."
  - anchor: asyncio-mocking
    what: "Using `unittest.mock.AsyncMock` to replace coroutine-returning attributes and methods and asserting on their await calls."
    problem: "Plain `Mock` for async method returns coroutine object never awaited, yielding `RuntimeWarning` and false positives; unawaited coroutine, fake async, discarded awaitable, warning on exit, silent pass, return-value trap, await semantics."
    use_when: "Collaborator returns coroutine and test must verify await semantics instead of treating coroutine object as plain value; unawaited coroutine, fake async, discarded awaitable, warning on exit, silent pass, await semantics, assert awaited, coroutine boundary."
    avoid_when: "Do not use a plain `Mock` for an async method."
    expected: "Awaitable collaborators are mocked with correct await semantics and their await calls are verified without unawaited-coroutine warnings."
  - anchor: asyncio-timeouts-cancellation
    what: "Guarding async tests against hangs with per-operation and suite-level timeouts and verifying cancellation propagation."
    problem: "Coroutine test can deadlock and hang run, while `asyncio.sleep` to fake slow dependency burns wall-clock and flakes under load; hanging coroutine, never-resolving await, deadlock guard, fake delay, slow stub, cancel propagation, bounded budget."
    use_when: "Coroutine can hang, slow dependency must be faked without wall clock delay, and cancellation path needs bounded assertion; hanging coroutine, never resolving await, deadlock guard, fake delay, slow stub, cancel propagation, bounded budget, timeout guardrail."
    avoid_when: "Do not call `asyncio.sleep` in a test to simulate slow dependencies or to give a task time to start."
    expected: "Async tests fail fast on hangs within a bounded budget and correctly assert that cancelling a task raises `asyncio.CancelledError`, without sleeping."
  - anchor: asyncio-race-conditions
    what: "Deterministic and stress-style checks for shared-state corruption across concurrent asyncio tasks and threads."
    problem: "Relying on `time.sleep` to let race happen yields flaky tests and false confidence, while thread exceptions never surface in main thread; shared-state corruption, hidden ordering, stress check, lost exception, invariant after join, flaky interleaving."
    use_when: "Concurrent tasks or threads can corrupt shared state, ordering must surface deterministically, and thread exceptions must reach main thread; shared state corruption, hidden ordering, stress check, lost exception, invariant after join, flaky interleaving, race probe."
    avoid_when: "Do not rely on `time.sleep` to make a race happen."
    expected: "Concurrent runs preserve deterministic invariants (e.g. final counter equals iterations times workers) and thread exceptions surface in the main thread; suspected flaky races are stress-checked with `pytest-repeat --count=50` locally while a deterministic invariant test stays in CI."
  - anchor: asyncio-common-errors
    what: "A symptom-to-cause-to-fix lookup table for frequent asyncio test failures."
    problem: "Async test fails with cause not obvious from failure message, so diagnosis stalls without mapping symptom to cause; symptom lookup, traceback gap, quick triage, regression after fix, failure catalog, debugging aid, cause mapping."
    use_when: "Async failure symptom is known but cause is not obvious from traceback, so lookup table can short path to regression; symptom lookup, traceback gap, quick triage, regression after fix, failure catalog, debugging aid, cause mapping, async diagnosis."
    avoid_when: "Do not use the table as a substitute for reading the actual traceback — match the symptom to a row first, then confirm against the failure."
    expected: "Each failing async test is mapped from symptom to cause and fixed, with a regression test added so it stays fixed."
libraries:
  - anyio
  - httpx
  - pytest-asyncio>=0.23
  - pytest-repeat
  - pytest-timeout
  - sqlalchemy
  - trio
---

# ASYNC TESTING

## Configuration

[ref: #asyncio-configuration]

This section covers global settings that control how pytest discovers and executes async tests and fixtures.

Example `pyproject.toml` for a strict `pytest-asyncio` project:

```toml
[tool.pytest.ini_options]
minversion = "8.0"
asyncio_mode = "strict"
asyncio_default_fixture_loop_scope = "function"
asyncio_default_test_loop_scope = "function"
timeout = 10
```

Example `pyproject.toml` for a `pytest-anyio` project:

```toml
[tool.pytest.ini_options]
minversion = "8.0"
anyio_mode = "auto"
```

Global defaults:
- `asyncio_default_fixture_loop_scope` sets the implicit `loop_scope` for async fixtures when it is omitted.
- `asyncio_default_test_loop_scope` sets the implicit `loop_scope` for `@pytest.mark.asyncio` tests when it is omitted.
- Explicit `loop_scope` on a marker or fixture always overrides the global default.

Variety booster:
- Pin the plugin major version in `dependency-groups` or `pyproject.toml` and add a `pytest --asyncio-mode=strict` smoke step to CI so version upgrades are caught early.

## Async Fixtures and loop_scope

[ref: #asyncio-fixtures-loop-scope]

This section explains how to declare async fixtures so they share the correct event loop and clean up reliably.

Example session-scoped async fixture with cleanup:

```python
from collections.abc import AsyncIterator
from contextlib import AsyncExitStack

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def async_engine() -> AsyncIterator[AsyncEngine]:
    from myapp.config import TEST_DATABASE_URL

    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    yield engine
    await engine.dispose()
```

Example fixture composing multiple async context managers:

```python
from collections.abc import AsyncIterator
from contextlib import AsyncExitStack

import pytest_asyncio
from httpx import AsyncClient, AsyncHTTPTransport


@pytest_asyncio.fixture(loop_scope="session")
async def async_client() -> AsyncIterator[AsyncClient]:
    stack = AsyncExitStack()
    transport = await stack.enter_async_context(AsyncHTTPTransport())
    client = AsyncClient(transport=transport)
    yield client
    await stack.aclose()
```

Cleanup rules:
- Prefer `yield` fixtures over `return` + `addfinalizer` for async resources.
- Keep cleanup in the same fixture that creates the resource.
- Do not share mutable async state between tests unless it is truly immutable after creation.

Variety booster:
- Parameterize the loop scope in a dedicated test to prove that a session-scoped fixture attached to a session-scoped loop survives more than one test case.

## Async Test Patterns

[ref: #asyncio-test-patterns]

This section covers how to write individual async tests that run sequentially inside one event loop while exercising concurrency through coroutine primitives.

Example async repository test:

```python
from collections.abc import Callable

import pytest

from faker import Faker
from myapp.models import User
from myapp.repositories import AsyncUserRepository


@pytest.mark.asyncio(loop_scope="function")
async def test_async_repository_get_returns_entity(
    async_repo: AsyncUserRepository,
    user_factory: Callable[..., User],
    fake: Faker,
) -> None:
    """
    Given: a user created by the factory.
    When: the user is fetched from the async repository.
    Then: the returned entity matches the stored user.
    """
    # --- Arrange ---
    user = user_factory()

    # --- Act ---
    result = await async_repo.get(user.id)

    # --- Assert ---
    assert result is not None
    assert result.id == user.id
```

Example concurrent HTTP requests:

```python
import asyncio
from collections.abc import Callable

import pytest

from faker import Faker
from myapp.clients import AsyncOrderClient
from myapp.models import Order


@pytest.mark.asyncio(loop_scope="function")
async def test_concurrent_requests_do_not_corrupt_state(
    async_client: AsyncOrderClient,
    order_factory: Callable[..., Order],
    fake: Faker,
) -> None:
    """
    Given: multiple orders created by the factory.
    When: they are processed concurrently.
    Then: every result is marked as processed.
    """
    # --- Arrange ---
    count = fake.pyint(min_value=3, max_value=10)
    orders = [order_factory() for _ in range(count)]

    # --- Act ---
    results = await asyncio.gather(*[
        async_client.process(order.id) for order in orders
    ])

    # --- Assert ---
    assert len(results) == count
    assert all(r.status == "processed" for r in results)
```

TaskGroup variant for structured concurrency:

```python
import asyncio
from collections.abc import Callable

import pytest

from faker import Faker
from myapp.models import Order
from myapp.services import AsyncOrderService, OrderNotFoundError


@pytest.mark.asyncio(loop_scope="function")
async def test_task_group_cancels_on_first_failure(
    async_service: AsyncOrderService,
    order_factory: Callable[..., Order],
    fake: Faker,
) -> None:
    """
    Given: one valid order and one invalid order id.
    When: both are submitted to a TaskGroup.
    Then: the group raises OrderNotFoundError and cancels siblings.
    """
    # --- Arrange ---
    valid_order = order_factory()
    invalid_order_id = fake.uuid4()

    # --- Act / Assert ---
    with pytest.raises(OrderNotFoundError):
        async with asyncio.TaskGroup() as tg:
            tg.create_task(async_service.process(valid_order.id))
            tg.create_task(async_service.process(invalid_order_id))
```

Variety booster:
- Replace `asyncio.gather` with `TaskGroup` when the test needs to fail fast and propagate the first exception to the remaining tasks.

## Async Mocking

[ref: #asyncio-mocking]

This section explains how to mock awaitable collaborators without producing unawaited coroutines or false positives.

Example patching an async client method:

```python
from unittest.mock import AsyncMock, patch

import pytest

from faker import Faker
from myapp.services import PaymentGatewayError, PaymentService


@pytest.mark.asyncio(loop_scope="function")
async def test_payment_service_propagates_gateway_error(
    fake: Faker,
) -> None:
    """
    Given: a patched gateway that raises PaymentGatewayError.
    When: the service charges a payment.
    Then: the same error is propagated and the gateway was awaited once.
    """
    # --- Arrange ---
    error_message = fake.sentence()

    # --- Act / Assert ---
    with patch(
        "myapp.services.payment_client.charge",
        new_callable=AsyncMock,
    ) as mock_charge:
        mock_charge.side_effect = PaymentGatewayError(error_message)
        service = PaymentService()

        with pytest.raises(PaymentGatewayError, match=error_message):
            await service.charge(fake.uuid4(), fake.pydecimal(positive=True))

        mock_charge.assert_awaited_once()
```

Example async fixture that returns a preconfigured AsyncMock:

```python
from collections.abc import AsyncIterator
from unittest.mock import AsyncMock

import pytest_asyncio


@pytest_asyncio.fixture(loop_scope="function")
async def mock_notifier(fake: Faker) -> AsyncIterator[AsyncMock]:
    notifier = AsyncMock()
    notifier.notify.return_value = fake.uuid4()
    yield notifier
```

Variety booster:
- Instead of mocking the HTTP client, inject a fake in-memory transport that implements the same async interface; this preserves the await semantics and avoids patching private modules.

## Timeouts and Cancellation

[ref: #asyncio-timeouts-cancellation]

This section shows how to guard async tests against hangs and how to verify cancellation behavior.

Example with `asyncio.timeout`:

```python
import asyncio

import pytest

from faker import Faker
from myapp.workers import AsyncWorker


@pytest.mark.asyncio(loop_scope="function")
async def test_worker_completes_within_budget(
    worker: AsyncWorker,
    fake: Faker,
) -> None:
    """
    Given: a payload and a timeout budget.
    When: the worker processes the payload.
    Then: it finishes within the budget and reports done.
    """
    # --- Arrange ---
    payload = fake.pystr(min_chars=8, max_chars=64)
    budget = fake.pyfloat(min_value=0.1, max_value=1.0)

    # --- Act ---
    async with asyncio.timeout(budget):
        result = await worker.process(payload)

    # --- Assert ---
    assert result.is_done
```

Example asserting cancellation propagation:

```python
import asyncio

import pytest

from myapp.services import AsyncPoller


@pytest.mark.asyncio(loop_scope="function")
async def test_poller_raises_on_cancellation(
    poller: AsyncPoller,
) -> None:
    """
    Given: a running poller task.
    When: the task is cancelled.
    Then: awaiting it raises asyncio.CancelledError.
    """
    # --- Arrange ---
    task = asyncio.create_task(poller.run())

    # --- Act ---
    task.cancel()

    # --- Assert ---
    with pytest.raises(asyncio.CancelledError):
        await task
```

## Race Condition Testing

[ref: #asyncio-race-conditions]

This section covers deterministic and stress-style checks for shared-state corruption in asyncio and threading.

Example asyncio race condition:

```python
import asyncio

import pytest

from faker import Faker
from myapp.counters import AsyncCounter


@pytest.mark.asyncio(loop_scope="function")
async def test_concurrent_async_increments_preserve_total(
    fake: Faker,
) -> None:
    """
    Given: an async counter and several workers.
    When: workers increment concurrently.
    Then: the final value equals iterations multiplied by workers.
    """
    # --- Arrange ---
    counter = AsyncCounter()
    iterations = fake.pyint(min_value=100, max_value=500)
    workers = fake.pyint(min_value=3, max_value=8)

    # --- Act ---
    await asyncio.gather(*[
        counter.increment_many(iterations) for _ in range(workers)
    ])

    # --- Assert ---
    assert counter.value == iterations * workers
```

Example threading race condition:

```python
import concurrent.futures

import pytest

from faker import Faker
from myapp.counters import Counter


def test_concurrent_writes_do_not_corrupt_counter(fake: Faker) -> None:
    """
    Given: a thread-unsafe counter and multiple worker threads.
    When: threads increment concurrently.
    Then: the final value equals iterations multiplied by workers.
    """
    # --- Arrange ---
    counter = Counter()
    iterations = fake.pyint(min_value=500, max_value=2000)
    workers = fake.pyint(min_value=2, max_value=8)

    # --- Act ---
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(counter.increment_many, iterations)
            for _ in range(workers)
        ]
        for future in futures:
            future.result()

    # --- Assert ---
    assert counter.value == iterations * workers
```

Example surfacing a thread exception:

```python
import concurrent.futures

import pytest

from faker import Faker


def test_background_worker_surfaces_exceptions(fake: Faker) -> None:
    """
    Given: a background task that raises RuntimeError.
    When: its future result is retrieved.
    Then: the exception is surfaced in the main thread.
    """
    # --- Arrange ---
    error_message = fake.sentence()

    # --- Act / Assert ---
    with pytest.raises(RuntimeError, match=error_message):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(
                lambda: (_ for _ in ()).throw(RuntimeError(error_message)),
            )
            future.result()
```

Variety booster:
- For suspected flaky races, run the test under `pytest-repeat` with `--count=50` locally, but keep a deterministic invariant test in CI so regressions are caught without randomness.

## Common Errors

[ref: #asyncio-common-errors]

This section maps frequent failures to their causes and fixes.

| Error / Symptom | Cause | Fix |
|---|---|---|
| `coroutine 'test_x' was never awaited` | The async test is missing `@pytest.mark.asyncio` or `pytest-asyncio` is not installed. | Add the marker and ensure the plugin is in dev dependencies. |
| `Mock can't be used in 'await' expression` | A plain `Mock` was used for an async callable. | Replace it with `AsyncMock`. |
| `This event loop is already running` | `asyncio.run()` was called inside an async test or fixture. | Await the coroutine directly; do not start a new loop. |
| `got Future <...> attached to a different loop` | Fixture `scope` and `loop_scope` do not match. | Set `loop_scope` equal to the fixture's `scope`. |
| `Fixture "..." is called directly` | An async fixture was called as a function instead of being injected. | Declare the fixture as a parameter in the test signature. |
| `RuntimeWarning: coroutine ... was never awaited` | An async helper was called without `await`. | Add `await` or mark the helper as sync if it is not a coroutine. |
| Test hangs indefinitely | A task waits for an event that is never set. | Add `asyncio.timeout`, `pytest-timeout`, or inject a mock clock. |
| `DeprecationWarning: ... event_loop fixture` | The deprecated `event_loop` fixture was overridden. | Use `loop_scope` on markers and fixtures instead. |

Variety booster:
- Keep a regression test for each common error your team has hit; a small test that deliberately reproduces the failure and then demonstrates the fix prevents the mistake from returning.
