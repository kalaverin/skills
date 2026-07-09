---
subject: "Keep suites fast and detect regressions: memory ceilings with `limit_memory`, leak detection with `limit_leaks`, allocation reports via `--memray`, benchmarking with the `benchmark` fixture/`pedantic`/`--benchmark-compare-fail`, per-test and session timeouts with `pytest-timeout`, slow-test triage via `--durations`, profiling with `--profile`/`cProfile`/`py-spy`, broader fixture scopes for immutable resources, in-memory fakes, parametrized input sizes."
index:
  - anchor: performance-memray
    what: "The `@pytest.mark.limit_memory('24 MB')` marker from pytest-memray that sets a hard peak-memory ceiling on a single test and fails it if the budget is exceeded."
    problem: "Long-running or batch test must fail when peak memory crosses explicit ceiling instead of letting growth pass silently; peak ceiling, fail on exceed, headroom allocator, exclude background thread, memory budget, catch regression."
    use_when: "Long running or batch test has memory ceiling, growth must fail explicitly, and background threads may need exclusion; peak ceiling, fail on exceed, headroom allocator, exclude background thread, memory budget, catch regression, memray marker."
    avoid_when: "Do not set the limit so tight that normal CPython allocator retention trips it (leave headroom), and do not let unrelated background threads inflate the reading when they are irrelevant (use `current_thread_only=True`)."
    expected: "A test that exceeds its peak-memory ceiling fails while tests within budget pass; background threads are excluded with `current_thread_only=True` and the limit tolerates CPython allocator retention."
  - anchor: performance-memray
    what: "The `@pytest.mark.limit_leaks('1 MB')` marker from pytest-memray that runs the test body in a loop so interpreter noise does not hide real growth, failing the test if leaked memory exceeds the budget."
    problem: "Genuine memory leaks that single peak ceiling misses must surface by measuring growth across many iterations; per-iteration growth, leak budget, loop inside test, interpreter noise averaged, allocation report, steady state."
    use_when: "Single peak ceiling misses leaks, repeated processing must measure growth across iterations, and interpreter noise must average out; per iteration growth, leak budget, loop inside test, interpreter noise averaged, allocation report, steady state."
    avoid_when: "Do not rely on a single `limit_memory` ceiling to catch leaks (it measures peak, not growth across iterations), and do not hoist the per-iteration payload out of the loop (the example generates `fake.pydict(...)` inside the loop so growth is measured across repeated calls)."
    expected: "Real per-iteration growth is surfaced as a failure above the leak budget while steady interpreter noise is averaged out, and `pytest --memray` provides the allocation report for diagnosis."
  - anchor: performance-benchmark
    what: "The `benchmark` fixture that runs a target function and records timing statistics, called as `benchmark(func, *args)`, with per-test tuning via `@pytest.mark.benchmark(min_rounds=...)`."
    problem: "Function must microbenchmark and detect timing regressions without mixing timing into functional correctness assertions; timing statistics, regression detect, min rounds tune, separate correctness, target function, stable rounds."
    use_when: "Function needs microbenchmark, timing regression must detect from measured results, and functional correctness assertions stay separate from timing; timing statistics, regression detect, min rounds tune, separate correctness, target function, stable rounds, benchmark fixture."
    avoid_when: "Do not use `pytest-benchmark` for functional correctness (the section states it is for microbenchmarks and regression detection, not functional correctness), and do not set per-test `min_rounds` where a global benchmark configuration would suffice."
    expected: "Timing statistics are recorded for the target function, functional behavior is asserted elsewhere, and individual tests can raise their round count via the marker when needed."
  - anchor: performance-benchmark
    what: "The `benchmark.pedantic(target, args=..., rounds=..., iterations=..., warmup_rounds=...)` calling convention that runs setup outside the timed region and controls rounds, iterations, and warmup rounds."
    problem: "Expensive arrange must stay outside measured region so timing reflects only target, stabilized by explicit round and warmup counts; setup excluded, warmup rounds, cold cache, iterations, timed region, build input first."
    use_when: "Expensive arrange must sit outside timed region, explicit rounds and warmup stabilize timing, and built input prevents measurement distortion; setup excluded, warmup rounds, cold cache, iterations, timed region, build input first, pedantic benchmark."
    avoid_when: "Do not build the timed input inside the callable passed to `pedantic` (the example constructs `items` before the call so list construction is not measured), and do not skip `warmup_rounds` when cold-cache effects would skew the first rounds."
    expected: "Only the target function is timed, with setup excluded and results stabilized by the configured `rounds`, `iterations`, and `warmup_rounds`."
  - anchor: performance-benchmark
    what: "The `--benchmark-only`, `--benchmark-disable`, `--benchmark-autosave`, `--benchmark-compare`, and `--benchmark-compare-fail=ratio:0.1` command-line options that select, skip, persist, compare, and gate benchmark runs."
    problem: "Benchmark runs must select, skip, persist, compare, and fail CI when regression exceeds tolerated deviation, without changing test code; only benchmarks, disable fast run, autosave, compare baseline, compare fail ratio, no code change."
    use_when: "Benchmark run must select, skip, persist, compare, and fail CI on deviation, all without changing test code; only benchmarks, disable fast run, autosave, compare baseline, compare fail ratio, no code change, benchmark cli."
    avoid_when: "Do not compare against a baseline that `--benchmark-autosave` never produced, and do not set `--benchmark-compare-fail` so tightly that interpreter or runner noise fails an otherwise stable build."
    expected: "Benchmarks run or are skipped as intended, results are saved and compared across runs, and CI fails only when a regression exceeds the configured ratio."
  - anchor: performance-timeout
    what: "The `@pytest.mark.timeout(N)` marker (with optional `method='signal'` or `method='thread'`) and the global `timeout = N` default in `pyproject.toml` that abort a test exceeding a duration; `signal` is the POSIX default and allows teardown, while `thread` always works but terminates the whole process."
    problem: "Deadlocks and hangs must abort stuck test so it cannot block run, used strictly as last-resort safety net not precise performance assertion; hang guardrail, signal method, teardown runs, thread method, sla value, not performance."
    use_when: "Test can deadlock or hang under load, timeout must abort stuck run quickly, and precise performance assertion belongs elsewhere; hang guardrail, signal method, teardown runs, thread method, sla value, not performance, stuck test."
    avoid_when: "Do not use the timeout as a precise performance assertion (the section states it is a last-resort safety net, not a performance assertion), do not rely on `method='thread'` when teardown must run (it terminates the whole process), and do not apply it to merely slow tests that are not at risk of hanging, since it guards hangs rather than duration."
    expected: "A hung test is aborted before it blocks the run, teardown still runs under `signal` on POSIX, and passing timing is never asserted by the marker."
  - anchor: performance-timeout
    what: "The `--session-timeout` option that caps the entire pytest session so a CI job cannot run indefinitely."
    problem: "Whole run must bound so CI job cannot run indefinitely even when per-test timeouts absent or insufficient; session cap, terminate runaway, alongside per-test, prevent infinite job, global ceiling, ci bound."
    use_when: "Whole CI job must bound, per test timeouts may be absent or insufficient, and session cap prevents runaway run; session cap, terminate runaway, alongside per test, prevent infinite job, global ceiling, ci bound, session timeout."
    avoid_when: "Do not rely on `--session-timeout` as a substitute for per-test timeouts on tests that can hang (it caps the whole session, not the offending test), and do not leave long CI jobs uncapped."
    expected: "The session is bounded so CI jobs terminate within the cap, while per-test markers continue to catch individual hangs."
  - anchor: performance-durations
    what: "The `pytest --durations=N --durations-min=S` report that lists the N slowest tests, setups, and teardowns exceeding the threshold S."
    problem: "Slowest tests, setups, and teardowns must surface so they triage for optimization; slowest list, threshold, triage target, broader fixture, move to integration, regular review."
    use_when: "Slow tests, setups, and teardowns need triage list, threshold filters noise, and review decides fixture or integration move; slowest list, threshold, triage target, broader fixture, move to integration, regular review, durations report."
    avoid_when: "Do not treat `--durations` output as a pass/fail gate by itself — use it to prioritize fixture, fake, or marker improvements."
    expected: "Tests above the durations threshold are reviewed regularly and refactored via broader fixtures, fakes, or an integration marker."
  - anchor: performance-profiling
    what: "Per-test and deeper profiling options: `pytest --profile --profile-svg` via pytest-profiling for per-test cProfile output, `cProfile` with `snakeviz` for flamegraph-style exploration, and `py-spy` for low-overhead sampling of production-like behavior."
    problem: "Where test spends time must capture, choosing deterministic per-test attribution versus low-overhead sampling of production-like runs; per-test profile, flamegraph explore, low-overhead sample, svg output, investigation depth, normal run fast."
    use_when: "Test time attribution must capture, deterministic per test profile or low overhead sampling fits investigation depth; per test profile, flamegraph explore, low overhead sample, svg output, investigation depth, normal run fast, profiling."
    avoid_when: "Do not use low-overhead `py-spy` sampling when you need deterministic per-test cProfile attribution (use pytest-profiling instead), and do not capture `--profile-svg` artifacts on the default fast path where profiling tests are gated out."
    expected: "The chosen profiler yields per-test cProfile data, flamegraph exploration, or low-overhead samples appropriate to the investigation depth, without slowing normal runs."
  - anchor: performance-profiling
    what: "Keeping profiling tests separate and optional behind `@pytest.mark.profile` and `@pytest.mark.slow`, then running them selectively with `pytest -m profile` or `pytest -m slow`."
    problem: "Expensive profiling runs must not slow normal suite while still runnable on demand; marker gated, run selectively, default fast, slow marker, on demand, separate suite."
    use_when: "Profiling runs are expensive, default suite must stay fast locally and in CI, and marker selection keeps them runnable on demand; marker gated, run selectively, default fast, slow marker, on demand, separate suite, optional profiling."
    avoid_when: "Do not let profiling tests execute in the normal unmarked run (the section keeps them separate and optional so they do not slow normal runs), and do not forget to run the `profile`/`slow` selection explicitly when profiling is needed."
    expected: "Profiling tests run only when their marker is selected, so normal runs stay fast and profiling remains available on demand."
  - anchor: performance-design
    what: "Widening a fixture to a broader scope such as `scope='session'` for an expensive resource so setup is amortized across tests, valid only when the resource is immutable or properly reset between tests."
    problem: "Expensive resource setup must amortize across tests while preserving isolation; broader scope, setup once, immutable resource, reset between tests, session fixture, no shared mutable."
    use_when: "Expensive resource can amortize across tests, isolation must remain intact, and immutable or resettable state prevents sharing bugs; broader scope, setup once, immutable resource, reset between tests, session fixture, no shared mutable."
    avoid_when: "Do not broaden the scope of a mutable resource that is not reset between tests (the section allows broader scope only when the resource is immutable or properly reset), since shared mutable state would leak between tests."
    expected: "Expensive setup runs once per scope instead of once per test, and isolation holds because the shared resource is immutable or reset between tests."
  - anchor: performance-design
    what: "Replacing real network or disk calls with fakes or in-memory implementations in unit tests when the test target is the business logic rather than the I/O layer."
    problem: "Unit test must stay fast and deterministic by removing heavy I/O that is not behavior under test; in-memory fake, remove network, remove disk, business logic target, real io integration, fast deterministic."
    use_when: "Unit targets business logic, heavy network or disk is not behavior under test, and in memory fake keeps run deterministic; in memory fake, remove network, remove disk, business logic target, real io integration, fast deterministic."
    avoid_when: "Do not perform real network or disk I/O in unit tests whose target is business logic (the section replaces heavy I/O with fakes or in-memory implementations), reserving real I/O for integration tests that exercise the I/O layer itself."
    expected: "Unit tests run against in-memory fakes and stay fast and deterministic, while real I/O is confined to tests that target the I/O layer."
  - anchor: performance-variety-booster
    what: "Applying custom markers (for example a `unit` marker) to slow or integration tests and running those subsets selectively so the fast path stays fast."
    problem: "Default run must stay fast by excluding slow or integration tests unless explicitly selected; marker exclude, selective run, fast default path, integration subset, broader fixture fake, on demand."
    use_when: "Default run must stay fast, slow or integration subsets run only when selected, and markers encode that split; marker exclude, selective run, fast default path, integration subset, broader fixture fake, on demand, suite speed."
    avoid_when: "Do not run slow or integration tests on the fast default path (the section marks them and runs them selectively), and do not leave them unmarked so they cannot be excluded."
    expected: "The default run excludes slow or integration tests via markers, and those tests run only when their subset is selected."
libraries:
  - py-spy
  - pytest-benchmark
  - pytest-memray
  - pytest-profiling
  - pytest-timeout
  - snakeviz
---

# Performance

Performance reference for pytest: memory tracking, benchmarking, timeouts, profiling, and test design that keeps the suite fast.

## Memory tracking with pytest-memray

[ref: #performance-memray]

Use `pytest-memray` to detect memory leaks and unexpected allocations in long-running or batch-processing tests.

Set a hard ceiling with `@pytest.mark.limit_memory`:

```python
import pytest
from faker import Faker


@pytest.mark.limit_memory("24 MB")
def test_large_file_processing_does_not_leak(fake: Faker) -> None:
    """
    Given: a generated filename.
    When: a large file is processed.
    Then: memory usage stays within the memray limit.
    """
    # --- Arrange ---
    filename = f"{fake.pystr(min_chars=3, max_chars=10)}.json"

    # --- Act ---
    process_large_file(filename)

    # --- Assert ---
    # Memory assertion handled by the limit_memory marker.
```

Detect leaks by running the body in a loop so interpreter noise does not hide real growth:

```python
import pytest
from faker import Faker


@pytest.mark.limit_leaks("1 MB")
def test_batch_processor_does_not_accumulate_memory(fake: Faker) -> None:
    """
    Given: repeated batch processing calls.
    When: many batches are processed.
    Then: leaked memory stays within the memray limit.
    """
    # --- Arrange ---
    # payloads will be generated inside the loop.

    # --- Act ---
    for _ in range(100):
        payload = fake.pydict(value_types=["str", "int", "float"])
        process_batch(payload)

    # --- Assert ---
    # Leak assertion handled by the limit_leaks marker.
```

Run with the `--memray` flag to get allocation reports:

```bash
pytest --memray
```

Restrict tracking to the current thread when background threads are unrelated:

```python
import pytest


@pytest.mark.limit_memory("24 MB", current_thread_only=True)
def test_worker_thread_stays_within_budget() -> None:
    """
    Given: a worker that runs in the current thread.
    When: the worker is executed.
    Then: memory usage stays within the limit for the current thread.
    """
    # --- Arrange ---
    # Worker is ready to run.

    # --- Act ---
    run_worker()

    # --- Assert ---
    # Memory assertion handled by the limit_memory marker.
```

Leave headroom in memory limits because CPython's object allocator may not return freed memory to the OS immediately.

## Benchmarking with pytest-benchmark

[ref: #performance-benchmark]

Use `pytest-benchmark` for microbenchmarks and regression detection, not for functional correctness.

The `benchmark` fixture runs the target function and records timing statistics:

```python
from typing import Any

from faker import Faker


def test_serialize_payload_is_fast_enough(
    benchmark: Any,
    fake: Faker,
) -> None:
    """
    Given: a generated payload.
    When: serialization is benchmarked.
    Then: the benchmark runs without functional failure.
    """
    # --- Arrange ---
    payload = fake.pydict(value_types=["str", "int", "float"])

    # --- Act / Assert ---
    benchmark(serialize_payload, payload)
```

Use `benchmark.pedantic` when setup must happen outside the timed region:

```python
from typing import Any

from faker import Faker


def test_sort_stays_fast_across_sizes(
    benchmark: Any,
    fake: Faker,
) -> None:
    """
    Given: a large list of generated integers.
    When: sorting is benchmarked with controlled warmup and rounds.
    Then: the benchmark completes without functional failure.
    """
    # --- Arrange ---
    items = [fake.pyint(min_value=0, max_value=1_000_000) for _ in range(10_000)]

    # --- Act / Assert ---
    benchmark.pedantic(
        sorted,
        args=(items,),
        rounds=20,
        iterations=5,
        warmup_rounds=2,
    )
```

Control benchmark execution from the CLI:

```bash
pytest --benchmark-only              # run only benchmark tests
pytest --benchmark-disable           # skip benchmarks entirely
pytest --benchmark-autosave          # store results to disk
pytest --benchmark-compare           # compare against saved results
pytest --benchmark-compare-fail=ratio:0.1  # fail if deviation exceeds 10%
```

Tune individual tests with the benchmark marker:

```python
from typing import Any

import pytest


@pytest.mark.benchmark(min_rounds=50)
def test_hash_lookup_is_consistent(benchmark: Any) -> None:
    """
    Given: a stable input string.
    When: hash is benchmarked repeatedly.
    Then: the benchmark completes without functional failure.
    """
    # --- Arrange ---
    input_value = "stable-input"

    # --- Act / Assert ---
    benchmark(hash, input_value)
```

## Timeouts with pytest-timeout

[ref: #performance-timeout]

Use `pytest-timeout` as a last-resort safety net against hanging tests, not as a precise performance assertion.

Set a per-test timeout with a marker:

```python
import pytest


@pytest.mark.timeout(30)
def test_report_generation_completes(fake: Faker) -> None:
    """
    Given: a generated company name.
    When: a report is generated.
    Then: the operation completes within the timeout.
    """
    # --- Arrange ---
    company = fake.company()

    # --- Act ---
    generate_report(company)

    # --- Assert ---
    # Timeout assertion handled by the timeout marker.
```

Set global defaults in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
timeout = 60
```

Two timeout methods are available.
`signal` is the default on POSIX and allows teardown to run.
`thread` always works but terminates the whole process, so prefer `signal` on POSIX and reserve `thread` for platforms or cases where `signal` cannot be used.

```python
import pytest


@pytest.mark.timeout(10, method="thread")
def test_blocking_call_fails_fast() -> None:
    """
    Given: a call that may block indefinitely.
    When: it is invoked under a thread-based timeout.
    Then: the test is terminated before the global timeout expires.
    """
    # --- Arrange ---
    # call_that_may_block_forever is expected to hang.

    # --- Act ---
    call_that_may_block_forever()

    # --- Assert ---
    # Timeout assertion handled by the timeout marker.
```

Protect the entire session with `--session-timeout` to prevent CI jobs from running indefinitely.

## Identifying slow tests

[ref: #performance-durations]

Use `--durations=10` in CI to surface the 10 slowest tests and target them for optimization:

```bash
pytest --durations=10 --durations-min=1.0
```

This lists the slowest tests, setups, and teardowns that exceed the threshold.
Review the output regularly to spot regressions and decide which slow tests deserve broader fixtures, fakes, or a move to an integration marker.

## Profiling

[ref: #performance-profiling]

Use the `pytest-profiling` plugin to capture per-test `cProfile` output:

```bash
pytest --profile --profile-svg
```

For deeper investigation, use `cProfile` with `snakeviz` for flamegraph-style exploration or sampling profilers like `py-spy` to inspect production-like behavior with low overhead.

Keep profiling tests separate and optional so they do not slow normal runs:

```python
import pytest


@pytest.mark.profile
@pytest.mark.slow
@pytest.mark.limit_memory("64 MB")
def test_end_to_end_import_profile(fake: Faker) -> None:
    """
    Given: a list of generated filenames.
    When: documents are ingested end-to-end.
    Then: the operation stays within the memory limit and completes for profiling.
    """
    # --- Arrange ---
    filenames = [fake.file_name() for _ in range(100)]

    # --- Act ---
    ingest_documents(filenames)

    # --- Assert ---
    # Memory and profiling assertions handled by markers.
```

Run profiling markers selectively:

```bash
pytest -m profile
pytest -m slow
```

## Performance-friendly test design

[ref: #performance-design]

Prefer broader fixture scopes for expensive resources, but only when the resource is immutable or properly reset between tests.
Avoid heavy I/O in unit tests by using fakes or in-memory implementations.
Mark slow or integration tests with custom markers and run them selectively.

```python
import pytest
from faker import Faker


@pytest.fixture(scope="session")
def search_index() -> SearchIndex:
    index = build_search_index()
    yield index
    index.close()


@pytest.mark.unit
def test_search_returns_matches_for_word(
    fake: Faker,
    search_index: SearchIndex,
) -> None:
    """
    Given: a session-scoped search index and a generated document.
    When: the document is added and searched by its first word.
    Then: the index returns a match.
    """
    # --- Arrange ---
    document = fake.sentence()

    # --- Act ---
    search_index.add(document)

    # --- Assert ---
    assert search_index.find(document.split()[0])
```

Use in-memory fakes instead of real network or disk calls when the test target is the business logic:

```python
from faker import Faker


def test_price_calculation_uses_fake_rates(fake: Faker) -> None:
    """
    Given: a fake rate provider with generated rates.
    When: a conversion is computed.
    Then: the result is positive.
    """
    # --- Arrange ---
    rates = FakeRateProvider({fake.currency_code(): fake.pyfloat(positive=True)})
    calculator = PriceCalculator(rates)
    amount = fake.pyint(min_value=1, max_value=1000)

    # --- Act ---
    result = calculator.convert(amount, "USD", "EUR")

    # --- Assert ---
    assert result > 0
```

## Variety booster

[ref: #performance-variety-booster]

You can cover more invariants with less code by parametrizing benchmark or allocation tests over input sizes and implementation variants.
Let pytest-benchmark or pytest-memray run each variant, and assert that growth stays bounded rather than asserting exact numbers that depend on the interpreter version.

```python
from typing import Any

import pytest
from faker import Faker


@pytest.mark.parametrize("size", [10, 100, 1_000])
def test_merge_sort_scales_linearly(
    benchmark: Any,
    fake: Faker,
    size: int,
) -> None:
    """
    Given: a parametrized list size.
    When: sorting is benchmarked.
    Then: the benchmark completes without functional failure.
    """
    # --- Arrange ---
    items = [fake.pyint(min_value=0, max_value=size) for _ in range(size)]

    # --- Act / Assert ---
    benchmark.pedantic(sorted, args=(items,), rounds=10, iterations=3)
```
